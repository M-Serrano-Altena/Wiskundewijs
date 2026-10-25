"""Labels in matplotlib-figuren automatisch zo plaatsen dat ze nergens overheen vallen.

Gebruik `label(...)` tijdens het tekenen en roep `place_labels(fig)` aan vlak voor het opslaan.
Voor elk label proberen we een reeks plekken rond het ankerpunt (eerst in de voorkeursrichting)
en kiezen we de eerste plek waar de tekst geen lijn, rand of ander label raakt.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from matplotlib.backend_bases import RendererBase
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox

Array = npt.NDArray[np.float64]
Point = tuple[float, float]

RADII_PT = (7.0, 11.0, 15.0, 20.0, 27.0, 36.0, 48.0)  # afstanden (in punten) die we proberen
MARGIN_PX = 6.0                                    # minimale vrije ruimte rond de tekst


@dataclass
class PendingLabel:
    ax: Axes
    anchor: Point
    text: str
    color: str
    size: float
    prefer: Point
    rotation: float


PENDING: list[PendingLabel] = []


def label(ax: Axes, anchor: Point, text: str, color: str, size: float = 15,
          prefer: Point = (0.0, 1.0), rotation: float = 0.0) -> None:
    """Label bij `anchor` (data-coördinaten); `prefer` is de richting waar het bij voorkeur komt."""
    PENDING.append(PendingLabel(ax, anchor, text, color, size, prefer, rotation))


def densify(points: Array, step: float = 2.0) -> Array:
    """Extra punten langs een polylijn, om de paar pixels."""
    pieces: list[Array] = [points[:1]]
    for a, b in zip(points[:-1], points[1:]):
        n = max(1, int(np.linalg.norm(b - a) / step))
        t = np.linspace(0, 1, n + 1)[1:, None]
        pieces.append(a + t * (b - a))
    return np.vstack(pieces)


def obstacle_points(ax: Axes) -> Array:
    """Alle lijnen en randen van vormen, als punten in schermcoördinaten (pixels)."""
    polylines: list[Array] = []
    for line in ax.get_lines():
        xy = np.asarray(line.get_xydata(), dtype=np.float64)
        polylines.append(ax.transData.transform(xy))
    for patch in ax.patches:
        if to_rgba(patch.get_edgecolor())[3] == 0 or patch.get_linewidth() == 0:
            continue
        for polygon in patch.get_path().to_polygons(patch.get_transform()):
            polylines.append(np.asarray(polygon, dtype=np.float64))
    if not polylines:
        return np.zeros((0, 2))
    return np.vstack([densify(p) for p in polylines if len(p)])


def candidates(prefer: Point) -> list[Point]:
    base = float(np.arctan2(prefer[1], prefer[0]))
    turns = [0.0] + [s * k * np.pi / 8 for k in range(1, 9) for s in (1, -1)]
    return [(r * float(np.cos(base + d)), r * float(np.sin(base + d))) for r in RADII_PT for d in turns]


@dataclass(frozen=True)
class TextFrame:
    """Een (eventueel gedraaid) tekstvak op het scherm: midden, halve breedte/hoogte en hoek."""

    centre: Array
    half_w: float
    half_h: float
    angle: float  # in graden

    def local(self, points: Array) -> Array:
        """Punten in het assenstelsel van het tekstvak (zodat het vak niet meer gedraaid is)."""
        c, s = np.cos(np.radians(-self.angle)), np.sin(np.radians(-self.angle))
        rel = points - self.centre
        return np.column_stack([c * rel[:, 0] - s * rel[:, 1], s * rel[:, 0] + c * rel[:, 1]])

    def hits(self, points: Array) -> bool:
        if not len(points):
            return False
        q = self.local(points)
        inside = (np.abs(q[:, 0]) <= self.half_w + MARGIN_PX) & (np.abs(q[:, 1]) <= self.half_h + MARGIN_PX)
        return bool(np.any(inside))

    def corners(self) -> Array:
        c, s = np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle))
        local = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]]) * [self.half_w, self.half_h]
        return self.centre + local @ np.array([[c, s], [-s, c]])


def box_points(box: Bbox, step: float = 2.0) -> Array:
    """De rand en het midden van een ander tekstvak, als punten."""
    corners = np.array([[box.x0, box.y0], [box.x1, box.y0], [box.x1, box.y1], [box.x0, box.y1], [box.x0, box.y0]])
    return np.vstack([densify(corners, step), [[(box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2]]])


def is_free(frame: TextFrame, obstacles: Array, placed: list[Bbox]) -> bool:
    if frame.hits(obstacles):
        return False
    for other in placed:
        if frame.hits(box_points(other)):
            return False
        xs, ys = frame.corners()[:, 0], frame.corners()[:, 1]
        if np.any((xs >= other.x0) & (xs <= other.x1) & (ys >= other.y0) & (ys <= other.y1)):
            return False
    return True


def measure(item: PendingLabel, renderer: RendererBase) -> tuple[float, float]:
    """Halve breedte en hoogte van de tekst als hij niet gedraaid is (in pixels)."""
    probe = item.ax.annotate(item.text, xy=item.anchor, ha="center", va="center", fontsize=item.size)
    box = probe.get_window_extent(renderer)
    probe.remove()
    return box.width / 2, box.height / 2


def place_one(item: PendingLabel, renderer: RendererBase, obstacles: Array, placed: list[Bbox], dpi: float) -> Bbox:
    half_w, half_h = measure(item, renderer)
    anchor = item.ax.transData.transform(np.array([item.anchor], dtype=np.float64))[0]
    px_per_pt = dpi / 72
    options = candidates(item.prefer)
    chosen = next((o for o in options
                   if is_free(TextFrame(anchor + np.array(o) * px_per_pt, half_w, half_h, item.rotation), obstacles, placed)),
                  None)
    if chosen is None:
        print(f"  let op: geen vrije plek gevonden voor label '{item.text}'")
        chosen = options[0]
    artist = item.ax.annotate(item.text, xy=item.anchor, xytext=chosen, textcoords="offset points",
                              ha="center", va="center", color=item.color, fontsize=item.size,
                              rotation=item.rotation, rotation_mode="anchor")
    return artist.get_window_extent(renderer)


def place_labels(fig: Figure) -> None:
    """Zet alle wachtende labels van deze figuur op een vrije plek."""
    mine = [p for p in PENDING if p.ax.figure is fig]
    if not mine:
        return
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()  # type: ignore[attr-defined]
    obstacles = {id(ax): obstacle_points(ax) for ax in {id(p.ax): p.ax for p in mine}.values()}
    # tekst die er al vast staat (zonder automatische plaatsing) telt ook als bezet
    placed: list[Bbox] = [t.get_window_extent(renderer) for ax in {id(p.ax): p.ax for p in mine}.values()
                          for t in ax.texts]
    for item in mine:
        placed.append(place_one(item, renderer, obstacles[id(item.ax)], placed, fig.dpi))
        PENDING.remove(item)
