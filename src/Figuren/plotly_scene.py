"""Hulpfuncties voor de 3D-figuren: camera, labels zonder overlap, en opslaan.

Labels (zoals de nummers van hoekpunten) worden als scène-annotaties getekend. Die staan
altijd bovenop de figuur, dus ze verdwijnen niet achter een vlak. Om te voorkomen dat
labels over ribben of over elkaar heen vallen, rekenen we zelf uit waar alles op het scherm
terechtkomt en kiezen we voor elk label een verschuiving zonder overlap.
"""

from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt
import plotly.graph_objects as go
from PIL import Image

Array = npt.NDArray[np.float64]
Trace = go.Mesh3d | go.Scatter3d | go.Surface

REPO = Path(__file__).resolve().parents[2]
ASSETS = REPO / "mkdocs" / "assets"
IMG_DIR = ASSETS / "images" / "figuren"
HTML_DIR = ASSETS / "interactive_images" / "figuren"

PAGE_BACKGROUND = "#2e303e"  # achtergrond van de losse HTML-pagina (slate)
CAMERA_DISTANCE = 2.6        # afstand van de camera tot het midden (genormaliseerde scène-eenheden)
WIDTH, HEIGHT = 700, 560     # grootte van de figuur in pixels (vóór schaal 2)
PNG_SCALE = 2
PNG_PADDING = 18             # lege rand rond de figuur in de PNG (pixels, vóór schaal)
PNG_ASPECT = 5 / 4           # alle PNG's krijgen dezelfde verhouding (mooi in het raster)

CONFIG = {
    "modeBarButtonsToRemove": ["orbitRotation", "resetCameraDefault"],
    "displaylogo": False,
    "scrollZoom": True,
}


@dataclass(frozen=True)
class Label:
    """Tekst bij een punt in 3D. Met fixed=True komt het label precies op het punt."""

    position: tuple[float, float, float]
    text: str
    color: str
    size: int = 18
    fixed: bool = False


@dataclass(frozen=True)
class View:
    """Alles wat nodig is om een 3D-punt naar een pixel op het scherm om te rekenen."""

    middle: Array
    span: Array
    ratio: Array
    eye: Array
    scale: float = 1.0
    offset: tuple[float, float] = (0.0, 0.0)

    def normalise(self, points: Array) -> Array:
        return (points - self.middle) / self.span * self.ratio

    def camera_plane(self, points: Array) -> Array:
        """Perspectiefprojectie (zonder schaal) van punten in data-coördinaten."""
        view_dir = -self.eye / np.linalg.norm(self.eye)
        right = np.cross(view_dir, np.array([0.0, 0.0, 1.0]))
        right /= np.linalg.norm(right)
        up = np.cross(right, view_dir)
        rel = self.normalise(points) - self.eye
        depth = rel @ view_dir
        return np.column_stack([rel @ right / depth, rel @ up / depth])

    def pixels(self, points: Array) -> Array:
        plane = self.camera_plane(points)
        return np.column_stack([plane[:, 0] * self.scale + self.offset[0],
                                -plane[:, 1] * self.scale + self.offset[1]])


# ------------------------------------------------------------ geometrie

def coordinates(trace: Trace, axis: str) -> Array:
    values = np.asarray(getattr(trace, axis), dtype=object).ravel()
    return np.array([v for v in values if v is not None], dtype=np.float64)


def geometry_points(traces: list[Trace]) -> Array:
    """Alle punten van de figuur zelf (tekst-traces tellen niet mee)."""
    shapes = [t for t in traces if not (isinstance(t, go.Scatter3d) and t.mode == "text")]
    return np.column_stack([np.concatenate([coordinates(t, a) for t in shapes]) for a in ("x", "y", "z")])


def edge_segments(traces: list[Trace]) -> list[tuple[Array, Array]]:
    """De lijnstukken van alle lijn-traces (None scheidt de stukken)."""
    segments: list[tuple[Array, Array]] = []
    for t in traces:
        if not (isinstance(t, go.Scatter3d) and t.mode == "lines"):
            continue
        xs, ys, zs = (list(np.asarray(getattr(t, a), dtype=object).ravel()) for a in ("x", "y", "z"))
        for k in range(len(xs) - 1):
            if xs[k] is None or xs[k + 1] is None:
                continue
            segments.append((np.array([xs[k], ys[k], zs[k]], dtype=np.float64),
                             np.array([xs[k + 1], ys[k + 1], zs[k + 1]], dtype=np.float64)))
    return segments


def marker_points(traces: list[Trace]) -> Array:
    points = [np.column_stack([coordinates(t, a) for a in ("x", "y", "z")])
              for t in traces if isinstance(t, go.Scatter3d) and t.mode == "markers"]
    return np.vstack(points) if points else np.zeros((0, 3))


def base_view(points: Array, eye: tuple[float, float, float]) -> View:
    low, high = points.min(axis=0), points.max(axis=0)
    span = np.maximum(high - low, 1e-9)
    ratio = span / span.max()
    direction = np.array(eye, dtype=np.float64)
    return View(middle=(low + high) / 2, span=span, ratio=ratio,
                eye=direction / np.linalg.norm(direction) * CAMERA_DISTANCE)


def scene_layout(view: View, low: Array, high: Array) -> dict[str, object]:
    axes = [dict(visible=False, showspikes=False, range=[lo - 0.02, hi + 0.02]) for lo, hi in zip(low, high)]
    return dict(xaxis=axes[0], yaxis=axes[1], zaxis=axes[2], aspectmode="manual",
                aspectratio=dict(x=view.ratio[0], y=view.ratio[1], z=view.ratio[2]),
                camera=dict(eye=dict(x=view.eye[0], y=view.eye[1], z=view.eye[2])))


# ------------------------------------------------- van 3D naar pixels

def rendered_bbox(fig: go.Figure) -> tuple[int, int, int, int]:
    """Het gebied (in pixels) waar echt iets getekend is."""
    png = fig.to_image(format="png", width=WIDTH, height=HEIGHT, scale=1)
    alpha = Image.open(io.BytesIO(png)).convert("RGBA").getchannel("A")
    box = alpha.getbbox()
    return box if box is not None else (0, 0, WIDTH, HEIGHT)


def calibrate(view: View, points: Array, bbox: tuple[int, int, int, int]) -> View:
    """Schaal en verschuiving zo kiezen dat onze projectie op de echte afbeelding past."""
    plane = view.camera_plane(points)
    lo, hi = plane.min(axis=0), plane.max(axis=0)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    scale = float(np.mean([width / (hi[0] - lo[0]), height / (hi[1] - lo[1])]))
    offset_x = (bbox[0] + bbox[2]) / 2 - scale * (lo[0] + hi[0]) / 2
    offset_y = (bbox[1] + bbox[3]) / 2 + scale * (lo[1] + hi[1]) / 2
    return View(view.middle, view.span, view.ratio, view.eye, scale, (offset_x, offset_y))


# ------------------------------------------------------ labels plaatsen

@dataclass(frozen=True)
class Box:
    cx: float
    cy: float
    half_w: float
    half_h: float

    def contains(self, p: Array, margin: float = 6.0) -> bool:
        return abs(p[0] - self.cx) <= self.half_w + margin and abs(p[1] - self.cy) <= self.half_h + margin

    def overlaps(self, other: Box, margin: float = 3.0) -> bool:
        return (abs(self.cx - other.cx) <= self.half_w + other.half_w + margin
                and abs(self.cy - other.cy) <= self.half_h + other.half_h + margin)


def text_box(label: Label, centre: Array) -> Box:
    return Box(float(centre[0]), float(centre[1]), 0.31 * label.size * len(label.text), 0.62 * label.size)


def sampled_segments(view: View, segments: list[tuple[Array, Array]]) -> Array:
    """Punten om de paar pixels langs elke ribbe (om overlap mee te testen)."""
    samples: list[Array] = []
    for a, b in segments:
        pa, pb = view.pixels(np.vstack([a, b]))
        n = max(2, int(np.linalg.norm(pb - pa) / 2))
        t = np.linspace(0, 1, n)[:, None]
        samples.append(pa + t * (pb - pa))
    return np.vstack(samples) if samples else np.zeros((0, 2))


def conflicts(box: Box, obstacles: Array, placed: list[Box]) -> int:
    hits = sum(1 for p in obstacles if box.contains(p))
    return hits + 50 * sum(1 for other in placed if box.overlaps(other))


def candidate_shifts(direction: Array) -> list[Array]:
    """Mogelijke verschuivingen, de meest 'naar buiten' gerichte eerst."""
    base = float(np.arctan2(direction[1], direction[0]))
    turns = [0.0] + [s * k * np.pi / 8 for k in range(1, 9) for s in (1, -1)]
    return [r * np.array([np.cos(base + d), np.sin(base + d)]) for r in (18.0, 26.0, 36.0, 48.0) for d in turns]


def best_shift(label: Label, anchor: Array, outward: Array, obstacles: Array, placed: list[Box]) -> Array:
    best, best_score = np.zeros(2), float("inf")
    for rank, shift in enumerate(candidate_shifts(outward)):
        score = conflicts(text_box(label, anchor + shift), obstacles, placed) * 1000 + rank
        if score < best_score:
            best, best_score = shift, score
        if score < 1000:
            break
    return best


def place_labels(view: View, labels: list[Label], traces: list[Trace]) -> list[dict[str, object]]:
    obstacles = sampled_segments(view, edge_segments(traces))
    dots = view.pixels(marker_points(traces)) if len(marker_points(traces)) else np.zeros((0, 2))
    obstacles = np.vstack([obstacles, dots])
    centre = view.pixels(geometry_points(traces)).mean(axis=0)
    placed: list[Box] = []
    annotations: list[dict[str, object]] = []
    for label in labels:
        anchor = view.pixels(np.array([label.position], dtype=np.float64))[0]
        if label.fixed:
            shift = np.zeros(2)
        else:
            outward = anchor - centre if np.linalg.norm(anchor - centre) > 1e-6 else np.array([1.0, -1.0])
            shift = best_shift(label, anchor, outward, obstacles, placed)
        placed.append(text_box(label, anchor + shift))
        annotations.append(dict(x=label.position[0], y=label.position[1], z=label.position[2], text=label.text,
                                showarrow=False, xshift=float(shift[0]), yshift=float(-shift[1]),
                                xanchor="center", yanchor="middle", font=dict(color=label.color, size=label.size)))
    return annotations


# --------------------------------------------------------- figuur maken

def make_figure(traces: list[Trace], eye: tuple[float, float, float], labels: list[Label] | None = None) -> go.Figure:
    """Figuur met verborgen assen, echte verhoudingen en labels zonder overlap."""
    points = geometry_points(traces)
    view = base_view(points, eye)
    fig = go.Figure(data=traces)
    fig.update_layout(scene=scene_layout(view, points.min(axis=0), points.max(axis=0)),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=0, r=0, t=0, b=0), showlegend=False, width=WIDTH, height=HEIGHT)
    if labels:
        view = calibrate(view, points, rendered_bbox(fig))
        fig.update_layout(scene_annotations=place_labels(view, labels, traces))
    return fig


# --------------------------------------------------------------- opslaan

def add_page_style(html_file: Path) -> None:
    """Donkere achtergrond voor de losse pagina, zodat de lichte ribben goed te zien zijn."""
    style = (f'<meta name="color-scheme" content="light dark"><style>html, body {{ margin: 0; '
             f'background: {PAGE_BACKGROUND}; height: 100%; }} .plotly-graph-div {{ height: 100vh !important; '
             f'width: 100vw !important; }}</style>')
    text = html_file.read_text(encoding="utf-8")
    html_file.write_text(text.replace("<head>", "<head>" + style, 1), encoding="utf-8")


def tight_png(fig: go.Figure) -> Image.Image:
    """PNG zonder overbodige lege rand, aangevuld tot een vaste verhouding."""
    png = fig.to_image(format="png", width=WIDTH, height=HEIGHT, scale=PNG_SCALE)
    image = Image.open(io.BytesIO(png)).convert("RGBA")
    box = image.getchannel("A").getbbox() or (0, 0, image.width, image.height)
    pad = PNG_PADDING * PNG_SCALE
    cropped = image.crop(box)
    width = max(cropped.width + 2 * pad, int((cropped.height + 2 * pad) * PNG_ASPECT))
    height = max(cropped.height + 2 * pad, int(width / PNG_ASPECT))
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas.paste(cropped, ((width - cropped.width) // 2, (height - cropped.height) // 2))
    return canvas


def save(fig: go.Figure, name: str) -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    html_file = HTML_DIR / f"{name}.html"
    interactive = go.Figure(fig)
    interactive.update_layout(width=None, height=None, autosize=True)
    # plotly.js via CDN, anders wordt elk bestand ~4 MB
    interactive.write_html(html_file, config=CONFIG, include_plotlyjs="cdn", full_html=True)
    add_page_style(html_file)
    tight_png(fig).save(IMG_DIR / f"{name}.png")
    print(f"opgeslagen: {name}")
