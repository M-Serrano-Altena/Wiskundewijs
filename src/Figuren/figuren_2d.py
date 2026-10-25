"""Platte afbeeldingen (SVG, matplotlib) voor VWO 1, hoofdstuk 1 Figuren.

Uitslagen, tekeningen van een kubus en balk, begrippen bij de cirkel, veelhoeken,
diagonalen en het tekenen van een driehoek met een passer.
Alles wordt opgeslagen in mkdocs/assets/images/figuren/.
Labels worden automatisch zo geplaatst dat ze geen lijnen of andere tekst raken (zie mpl_labels).

Draaien vanuit de root van de repo:  python -m src.Figuren.figuren_2d
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Arc, Circle, Polygon, Rectangle  # noqa: E402

from src.Figuren.mpl_labels import label, place_labels  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
IMG_DIR = REPO / "mkdocs" / "assets" / "images" / "figuren"

# zelfde stijl als de andere afbeeldingen op de site (donker thema, lichte lijnen)
LINE = "#D3D3D3"
BODY = "#26a69a"
BODY_LIGHT = "#4db6ac"
ACCENT = "#ef5350"
ACCENT_2 = "#42a5f5"
ACCENT_3 = "#ffca28"
FONT_SIZE = 15

Point = tuple[float, float]


# ------------------------------------------------------------------ helpers

def new_axes(width: float, height: float) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=(width, height), facecolor="none")
    ax.set_facecolor("none")
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig: Figure, name: str) -> None:
    place_labels(fig)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMG_DIR / f"{name}.svg", transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(f"opgeslagen: {name}")


def text(ax: Axes, xy: Point, s: str, color: str = LINE, size: int = FONT_SIZE) -> None:
    """Tekst precies op een plek (bijvoorbeeld midden in een vlak)."""
    ax.text(xy[0], xy[1], s, color=color, fontsize=size, ha="center", va="center")


def segment(ax: Axes, a: Point, b: Point, color: str = LINE, width: float = 2.0, dashed: bool = False) -> None:
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=width, ls="--" if dashed else "-",
            solid_capstyle="round")


def dot(ax: Axes, p: Point, color: str = LINE, size: float = 6) -> None:
    ax.plot([p[0]], [p[1]], "o", color=color, markersize=size)


def square(ax: Axes, x: float, y: float, w: float, h: float, color: str = BODY) -> None:
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=LINE, lw=2))


def right_angle(ax: Axes, corner: Point, d1: Point, d2: Point, size: float = 0.25) -> None:
    """Klein vierkantje dat een rechte hoek aangeeft (d1, d2 zijn eenheidsrichtingen)."""
    c = np.array(corner)
    p1, p2 = c + size * np.array(d1), c + size * np.array(d2)
    p3 = p1 + size * np.array(d2)
    ax.plot([p1[0], p3[0], p2[0]], [p1[1], p3[1], p2[1]], color=LINE, lw=1.2)


def right_angles(ax: Axes, w: float, h: float, size: float) -> None:
    for corner, d1, d2 in [((0, 0), (1, 0), (0, 1)), ((w, 0), (-1, 0), (0, 1)),
                           ((w, h), (-1, 0), (0, -1)), ((0, h), (1, 0), (0, -1))]:
        right_angle(ax, corner, d1, d2, size)


def regular_polygon(n: int, radius: float, centre: Point = (0.0, 0.0), phase: float = np.pi / 2) -> list[Point]:
    angles = phase + 2 * np.pi * np.arange(n) / n
    return [(centre[0] + radius * float(np.cos(a)), centre[1] + radius * float(np.sin(a))) for a in angles]


def on_circle(r: float, deg: float, centre: Point = (0.0, 0.0)) -> Point:
    return (centre[0] + r * float(np.cos(np.radians(deg))), centre[1] + r * float(np.sin(np.radians(deg))))


def midpoint(a: Point, b: Point) -> Point:
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


# --------------------------------------------------------------- uitslagen

PIPS: dict[int, list[Point]] = {
    1: [(0, 0)],
    2: [(-0.25, 0.25), (0.25, -0.25)],
    3: [(-0.25, 0.25), (0, 0), (0.25, -0.25)],
    4: [(-0.25, -0.25), (-0.25, 0.25), (0.25, -0.25), (0.25, 0.25)],
    5: [(-0.25, -0.25), (-0.25, 0.25), (0, 0), (0.25, -0.25), (0.25, 0.25)],
    6: [(-0.25, -0.25), (-0.25, 0), (-0.25, 0.25), (0.25, -0.25), (0.25, 0), (0.25, 0.25)],
}


def die_face(ax: Axes, x: float, y: float, value: int) -> None:
    square(ax, x, y, 1, 1, color="#f5f5f5")
    for px, py in PIPS[value]:
        ax.add_patch(Circle((x + 0.5 + px, y + 0.5 + py), 0.08, color="#212121"))


def uitslag_dobbelsteen() -> None:
    """Kruisvormige uitslag; overstaande vlakken zijn samen 7 (zelfde dobbelsteen als in 3D)."""
    fig, ax = new_axes(6, 4.5)
    layout = {(0, 1): 3, (1, 1): 1, (2, 1): 4, (3, 1): 6, (1, 2): 2, (1, 0): 5}
    for (cx, cy), value in layout.items():
        die_face(ax, cx, cy, value)
    ax.set_xlim(-0.1, 4.1)
    ax.set_ylim(-0.1, 3.1)
    save(fig, "uitslag dobbelsteen")


# de 11 uitslagen van een kubus, als (kolom, rij) van elk vierkant
CUBE_NETS: list[list[tuple[int, int]]] = [
    [(0, 1), (1, 1), (2, 1), (3, 1), (top, 2), (bottom, 0)]
    for top, bottom in [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2)]
] + [
    [(0, 2), (1, 2), (1, 1), (2, 1), (3, 1), (b, 0)] for b in (1, 2, 3)
] + [
    [(0, 2), (1, 2), (1, 1), (2, 1), (2, 0), (3, 0)],
    [(0, 1), (1, 1), (2, 1), (2, 0), (3, 0), (4, 0)],
]


def uitslagen_kubus() -> None:
    """Alle 11 verschillende uitslagen van een kubus naast elkaar."""
    fig, ax = new_axes(11, 6.5)
    size = 0.5
    for index, cells in enumerate(CUBE_NETS):
        col, row = index % 4, index // 4
        for cx, cy in cells:
            square(ax, col * 2.9 + cx * size, (2 - row) * 2.0 + cy * size, size, size)
    ax.set_xlim(-0.1, 11.4)
    ax.set_ylim(-0.1, 5.6)
    save(fig, "uitslagen kubus (alle 11)")


def geen_uitslag() -> None:
    """Zes vierkanten op een rij: geen uitslag van een kubus."""
    fig, ax = new_axes(7, 1.6)
    for k in range(6):
        square(ax, k, 0, 1, 1)
    segment(ax, (-0.1, -0.15), (6.1, 1.15), color=ACCENT, width=3)
    segment(ax, (-0.1, 1.15), (6.1, -0.15), color=ACCENT, width=3)
    ax.set_xlim(-0.2, 6.2)
    ax.set_ylim(-0.3, 1.3)
    save(fig, "geen uitslag kubus (rij van 6)")


# uitslag met getallen: (kolom, rij) -> getal (zelfde getallen als 'kubus met getallen' in figuren_3d)
NUMBERED_NET: dict[tuple[int, int], int] = {(0, 2): 1, (1, 2): 2, (1, 1): 3, (2, 1): 4, (3, 1): 5, (2, 0): 6}


def uitslag_met_getallen() -> None:
    fig, ax = new_axes(5, 4)
    for (cx, cy), number in NUMBERED_NET.items():
        square(ax, cx, cy, 1, 1)
        text(ax, (cx + 0.5, cy + 0.5), str(number), size=22)
    ax.set_xlim(-0.1, 4.1)
    ax.set_ylim(-0.1, 3.1)
    save(fig, "uitslag met getallen")


def fmt(value: float) -> str:
    return f"{value:g}"


def uitslag_balk(name: str, length: float, width: float, height: float, missing: int | None = None) -> None:
    """Uitslag van een balk (lengte × breedte × hoogte). `missing` kleurt één rechthoek geel met een '?'."""
    fig, ax = new_axes(8, 5.5)
    lw_, lh, wh = f"{fmt(length)} × {fmt(width)}", f"{fmt(length)} × {fmt(height)}", f"{fmt(width)} × {fmt(height)}"
    pieces: list[tuple[float, float, float, float, str, str]] = [
        (0, width, width, height, wh, BODY),                            # links
        (width, width, length, height, lh, BODY),                       # voor
        (width + length, width, width, height, wh, BODY),               # rechts
        (2 * width + length, width, length, height, lh, BODY),          # achter
        (width, width + height, length, width, lw_, BODY_LIGHT),        # boven
        (width, 0, length, width, lw_, BODY_LIGHT),                     # onder
    ]
    for index, (x, y, w, h, s, color) in enumerate(pieces):
        is_missing = index == missing
        square(ax, x, y, w, h, color=ACCENT_3 if is_missing else color)
        text(ax, (x + w / 2, y + h / 2), s, color="#212121" if is_missing else LINE)
    ax.set_xlim(-0.2, 2 * width + 2 * length + 0.2)
    ax.set_ylim(-0.2, 2 * width + height + 0.2)
    save(fig, name)


def uitslag_cilinder() -> None:
    """Twee cirkels en een rechthoek; de breedte van de rechthoek is de omtrek van de cirkel."""
    fig, ax = new_axes(7, 5)
    r, h = 1.0, 2.2
    w = 2 * np.pi * r
    square(ax, 0, 0, w, h)
    ax.add_patch(Circle((w / 2, h + r), r, facecolor=BODY_LIGHT, edgecolor=LINE, lw=2))
    ax.add_patch(Circle((w / 2, -r), r, facecolor=BODY_LIGHT, edgecolor=LINE, lw=2))
    segment(ax, (0.08, h / 2), (w - 0.08, h / 2), color=ACCENT_3, width=1.8)
    ax.annotate("", xy=(w, h / 2), xytext=(0, h / 2), arrowprops=dict(arrowstyle="<->", color=ACCENT_3, lw=1.8))
    label(ax, (w / 2, h / 2), "omtrek van de cirkel", ACCENT_3, prefer=(0, 1))
    ax.set_xlim(-0.2, w + 0.2)
    ax.set_ylim(-2 * r - 0.2, h + 2 * r + 0.2)
    save(fig, "uitslag cilinder")


def uitslag_piramide() -> None:
    """Vierkant grondvlak met aan elke zijde een driehoek."""
    fig, ax = new_axes(5.5, 5.5)
    s, apex = 2.0, 1.8
    square(ax, 0, 0, s, s, color=BODY_LIGHT)
    triangles: list[list[Point]] = [
        [(0, 0), (s, 0), (s / 2, -apex)],
        [(s, 0), (s, s), (s + apex, s / 2)],
        [(s, s), (0, s), (s / 2, s + apex)],
        [(0, s), (0, 0), (-apex, s / 2)],
    ]
    for tri in triangles:
        ax.add_patch(Polygon(tri, closed=True, facecolor=BODY, edgecolor=LINE, lw=2))
    ax.set_xlim(-apex - 0.2, s + apex + 0.2)
    ax.set_ylim(-apex - 0.2, s + apex + 0.2)
    save(fig, "uitslag piramide")


# ------------------------------------------------- kubus en balk tekenen

def oblique_box(name: str, length: float, height: float, depth: float) -> None:
    """Een balk in 'schuine' tekening: verborgen ribben gestippeld."""
    fig, ax = new_axes(5.5, 4.5)
    d = (0.5 * depth * np.cos(np.pi / 4), 0.5 * depth * np.sin(np.pi / 4))
    a, b, c, e = (0.0, 0.0), (length, 0.0), (length, height), (0.0, height)
    a2, b2, c2, e2 = ((p[0] + d[0], p[1] + d[1]) for p in (a, b, c, e))
    ax.add_patch(Polygon([a, b, c, e], closed=True, facecolor=BODY, edgecolor="none"))
    ax.add_patch(Polygon([e, c, c2, e2], closed=True, facecolor=BODY_LIGHT, edgecolor="none"))
    ax.add_patch(Polygon([b, b2, c2, c], closed=True, facecolor="#1f8a80", edgecolor="none"))
    for p, q in [(a, b), (b, c), (c, e), (e, a), (b, b2), (c, c2), (e, e2), (b2, c2), (c2, e2)]:
        segment(ax, p, q)
    for p, q in [(a, a2), (a2, b2), (a2, e2)]:
        segment(ax, p, q, dashed=True, width=1.6)
    ax.set_xlim(-0.2, length + d[0] + 0.2)
    ax.set_ylim(-0.2, height + d[1] + 0.2)
    save(fig, name)


def vierhoek_diagonalen(name: str, w: float, h: float) -> None:
    """Vierkant of rechthoek met rechte hoeken en beide diagonalen."""
    fig, ax = new_axes(5, 5 * h / w if w > h else 5)
    square(ax, 0, 0, w, h)
    right_angles(ax, w, h, 0.25)
    segment(ax, (0, 0), (w, h), color=ACCENT_3, width=2.2)
    segment(ax, (w, 0), (0, h), color=ACCENT_3, width=2.2)
    dot(ax, (w / 2, h / 2), color=ACCENT_3)
    ax.set_xlim(-0.2, w + 0.2)
    ax.set_ylim(-0.2, h + 0.2)
    save(fig, name)


def rechthoek_maten(name: str, w: float, h: float, label_w: str, label_h: str) -> None:
    """Rechthoek (of vierkant) met rechte hoeken en de lengte van de zijden erbij."""
    fig, ax = new_axes(4.5, 4.5 * (h + 1) / (w + 1.5))
    square(ax, 0, 0, w, h)
    right_angles(ax, w, h, 0.06 * max(w, h))
    label(ax, (w / 2, 0), label_w, LINE, prefer=(0, -1))
    label(ax, (w, h / 2), label_h, LINE, prefer=(1, 0))
    ax.set_xlim(-0.2, w + 0.2)
    ax.set_ylim(-0.2, h + 0.2)
    save(fig, name)


# ---------------------------------------------------------------- cirkel

def cirkel_begrippen() -> None:
    """Middelpunt, straal, diameter en koorde."""
    fig, ax = new_axes(5.5, 5.5)
    r = 2.0
    ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor=LINE, lw=2.2))
    dot(ax, (0, 0))
    straal_end, d1, d2 = on_circle(r, 50), on_circle(r, 200), on_circle(r, 20)
    k1, k2 = on_circle(r, 110), on_circle(r, 165)
    segment(ax, (0, 0), straal_end, color=ACCENT, width=2.5)
    segment(ax, d1, d2, color=ACCENT_2, width=2.5)
    segment(ax, k1, k2, color=ACCENT_3, width=2.5)
    label(ax, (0, 0), "M", LINE, prefer=(0.3, -1))
    label(ax, midpoint((0, 0), straal_end), "straal", ACCENT, prefer=(-1, 0.6))
    label(ax, midpoint(d1, (0, 0)), "diameter", ACCENT_2, prefer=(0.2, -1))
    label(ax, midpoint(k1, k2), "koorde", ACCENT_3, prefer=on_circle(1, 137))
    label(ax, on_circle(r, -50), "omtrek", LINE, prefer=on_circle(1, -50))
    ax.set_xlim(-r - 0.4, r + 0.4)
    ax.set_ylim(-r - 0.4, r + 0.4)
    save(fig, "cirkel begrippen")


def cirkel_maten(name: str, straal: str, diameter: str) -> None:
    """Cirkel met een straal en een diameter, met hun lengte erbij."""
    fig, ax = new_axes(4.5, 4.5)
    r = 2.0
    straal_end = on_circle(r, 60)
    ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor=LINE, lw=2.2))
    segment(ax, (-r, 0), (r, 0), color=ACCENT_2, width=2.5)
    segment(ax, (0, 0), straal_end, color=ACCENT, width=2.5)
    dot(ax, (0, 0))
    label(ax, (-r / 2, 0), f"diameter = {diameter}", ACCENT_2, size=13, prefer=(0, -1))
    # anker iets onder het midden van de straal: zo past de tekst dicht langs de lijn zonder de cirkel te raken
    label(ax, on_circle(0.42 * r, 60), f"straal = {straal}", ACCENT, size=13, prefer=(-0.87, 0.5), rotation=60)
    ax.set_xlim(-r - 0.3, r + 0.3)
    ax.set_ylim(-r - 0.3, r + 0.3)
    save(fig, name)


def cirkel_in_vierkant() -> None:
    """Cirkel die precies in een vierkant van 10 bij 10 past."""
    fig, ax = new_axes(4.5, 4.5)
    square(ax, -2, -2, 4, 4, color="none")
    ax.add_patch(Circle((0, 0), 2, facecolor="none", edgecolor=LINE, lw=2.2))
    segment(ax, (-2, 0), (2, 0), color=ACCENT_2, width=2.5)
    segment(ax, (0, 0), (0, 2), color=ACCENT, width=2.5)
    dot(ax, (0, 0))
    label(ax, (-1.0, 0), "diameter = 10 cm", ACCENT_2, size=13, prefer=(0, -1))
    label(ax, (0, 1.0), "straal = 5 cm", ACCENT, size=13, prefer=(-1, 0), rotation=90)
    label(ax, (0, -2), "10 cm", LINE, prefer=(0, -1))
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.3, 2.3)
    save(fig, "cirkel in vierkant")


# -------------------------------------------------------------- veelhoeken

POLYGON_NAMES = {3: "driehoek", 4: "vierhoek", 5: "vijfhoek", 6: "zeshoek", 8: "achthoek"}


def veelhoeken() -> None:
    """Regelmatige veelhoeken naast elkaar, met hun naam eronder."""
    fig, ax = new_axes(7.5, 2.0)
    for k, (n, name) in enumerate(POLYGON_NAMES.items()):
        centre = (k * 2.6, 0.0)
        phase = np.pi / 2 + (np.pi / n if n % 2 == 0 else 0.0)
        ax.add_patch(Polygon(regular_polygon(n, 1.0, centre, phase), closed=True,
                             facecolor=BODY, edgecolor=LINE, lw=2))
        text(ax, (centre[0], -1.35), name)
    ax.set_xlim(-1.2, 4 * 2.6 + 1.2)
    ax.set_ylim(-1.7, 1.2)
    save(fig, "regelmatige veelhoeken")


def veelhoek_diagonalen(n: int, name: str) -> None:
    """Regelmatige n-hoek: de diagonalen vanuit één hoekpunt gekleurd, de rest gestippeld."""
    fig, ax = new_axes(5, 5)
    pts = regular_polygon(n, 2.0, phase=np.pi / 2)
    ax.add_patch(Polygon(pts, closed=True, facecolor=BODY, edgecolor=LINE, lw=2))
    for i in range(n):
        for j in range(i + 2, n):
            if (i, j) == (0, n - 1):
                continue  # dat is een zijde
            from_first = i == 0
            segment(ax, pts[i], pts[j], color=ACCENT_3 if from_first else LINE,
                    width=2.4 if from_first else 1.3, dashed=not from_first)
    dot(ax, pts[0], color=ACCENT_3, size=8)
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.3, 2.3)
    save(fig, name)


def driehoek_construeren() -> None:
    """Driehoek met zijden 5, 4 en 3 tekenen met een passer."""
    fig, ax = new_axes(6.5, 4)
    a, b = (0.0, 0.0), (5.0, 0.0)
    c = (3.2, 2.4)  # snijpunt van de cirkel om A met straal 4 en om B met straal 3
    ax.add_patch(Arc(a, 8, 8, theta1=20, theta2=55, color=ACCENT_2, lw=1.8, ls="--"))
    ax.add_patch(Arc(b, 6, 6, theta1=105, theta2=150, color=ACCENT, lw=1.8, ls="--"))
    segment(ax, a, b, width=2.5)
    segment(ax, a, c, color=ACCENT_2, width=2.2)
    segment(ax, b, c, color=ACCENT, width=2.2)
    for p in (a, b, c):
        dot(ax, p, size=7)
    label(ax, a, "A", LINE, prefer=(-1, -1))
    label(ax, b, "B", LINE, prefer=(1, -1))
    label(ax, c, "C", LINE, prefer=(0, 1))
    label(ax, midpoint(a, b), "5 cm", LINE, prefer=(0, -1))
    label(ax, midpoint(a, c), "4 cm", ACCENT_2, prefer=(-0.6, 0.8))
    label(ax, midpoint(b, c), "3 cm", ACCENT, prefer=(0.8, 0.6))
    ax.set_xlim(-0.6, 5.6)
    ax.set_ylim(-0.6, 3.2)
    save(fig, "driehoek construeren met passer")


def driehoek_onmogelijk() -> None:
    """Zijden 8, 3 en 4: de twee cirkelbogen raken elkaar nooit."""
    fig, ax = new_axes(6.5, 3)
    a, b = (0.0, 0.0), (8.0, 0.0)
    ax.add_patch(Arc(a, 6, 6, theta1=0, theta2=90, color=ACCENT_2, lw=1.8, ls="--"))
    ax.add_patch(Arc(b, 8, 8, theta1=90, theta2=180, color=ACCENT, lw=1.8, ls="--"))
    segment(ax, a, b, width=2.5)
    segment(ax, a, (3.0, 0.0), color=ACCENT_2, width=3)
    segment(ax, b, (4.0, 0.0), color=ACCENT, width=3)
    for p in (a, b):
        dot(ax, p, size=7)
    label(ax, a, "A", LINE, prefer=(-1, -1))
    label(ax, b, "B", LINE, prefer=(1, -1))
    label(ax, (4.0, 0.0), "8 cm", LINE, prefer=(0, -1))
    label(ax, (1.5, 0.0), "3 cm", ACCENT_2, prefer=(0, 1))
    label(ax, (6.0, 0.0), "4 cm", ACCENT, prefer=(0, 1))
    ax.set_xlim(-0.7, 8.7)
    ax.set_ylim(-0.8, 4.2)
    save(fig, "driehoek onmogelijk (3, 4 en 8)")


# ------------------------------------------------------------------ main

def main() -> None:
    uitslag_dobbelsteen()
    uitslagen_kubus()
    geen_uitslag()
    uitslag_met_getallen()
    uitslag_balk("uitslag balk", 5, 3, 2)
    uitslag_balk("uitslag balk 6 bij 4 bij 2 (ontbrekend)", 6, 4, 2, missing=3)
    uitslag_cilinder()
    uitslag_piramide()
    oblique_box("kubus tekenen", 2.0, 2.0, 2.0)
    oblique_box("balk tekenen", 3.5, 2.0, 2.4)
    vierhoek_diagonalen("vierkant diagonalen", 3.0, 3.0)
    vierhoek_diagonalen("rechthoek diagonalen", 4.5, 2.6)
    rechthoek_maten("vierkant 7 cm", 7, 7, "7 cm", "7 cm")
    rechthoek_maten("rechthoek 6 bij 4", 6, 4, "6 cm", "4 cm")
    rechthoek_maten("rechthoek 9 bij 4", 9, 4, "9 cm", "4 cm")
    cirkel_begrippen()
    cirkel_maten("cirkel diameter 14", "7 cm", "14 cm")
    cirkel_maten("cirkel straal 6.5", "6.5 cm", "13 cm")
    cirkel_in_vierkant()
    veelhoeken()
    veelhoek_diagonalen(6, "zeshoek diagonalen")
    veelhoek_diagonalen(5, "vijfhoek diagonalen")
    veelhoek_diagonalen(8, "achthoek diagonalen")
    driehoek_construeren()
    driehoek_onmogelijk()


if __name__ == "__main__":
    main()
