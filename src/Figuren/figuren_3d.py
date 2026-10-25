"""Interactieve 3D-figuren (plotly) voor VWO 1, hoofdstuk 1 Figuren.

Elke figuur wordt twee keer opgeslagen:
- als interactieve HTML in mkdocs/assets/interactive_images/figuren/
- als PNG (de afbeelding op de pagina) in mkdocs/assets/images/figuren/

Draaien vanuit de root van de repo:  python -m src.Figuren.figuren_3d
(PNG-export heeft het pakket `kaleido` nodig.)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go

from src.Figuren.plotly_scene import Array, Label, Trace, make_figure, save

# kleuren passend bij het donkere thema van de site
BODY = "#26a69a"        # teal: de figuur zelf
EDGE = "#D3D3D3"        # lichtgrijs: ribben
HIGHLIGHT_FACE = "#ffca28"
HIGHLIGHT_EDGE = "#ef5350"
HIGHLIGHT_VERTEX = "#42a5f5"
DIE_WHITE = "#f5f5f5"
DIE_INK = "#212121"
LIGHTING = dict(ambient=0.55, diffuse=0.7, specular=0.15, roughness=0.6)
WHITE_LIGHTING = dict(ambient=0.8, diffuse=0.35, specular=0.05, roughness=0.8)  # witte kubus niet te donker

Figure3D = tuple[list[Trace], list[Label]]


@dataclass(frozen=True)
class Polyhedron:
    """Een veelvlak: hoekpunten plus vlakken (lijsten met indices, tegen de klok in)."""

    vertices: Array
    faces: list[list[int]]


# ---------------------------------------------------------------- veelvlakken

def box(length: float, width: float, height: float) -> Polyhedron:
    """Balk met een hoekpunt in de oorsprong (een kubus is een balk met gelijke ribben)."""
    v = np.array(
        [[0, 0, 0], [length, 0, 0], [length, width, 0], [0, width, 0],
         [0, 0, height], [length, 0, height], [length, width, height], [0, width, height]],
        dtype=np.float64,
    )
    faces = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return Polyhedron(v, faces)


def regular_polygon(n: int, radius: float, z: float = 0.0, phase: float = 0.0) -> Array:
    """Hoekpunten van een regelmatige n-hoek in het vlak op hoogte z."""
    angles = phase + 2 * np.pi * np.arange(n) / n
    return np.column_stack([radius * np.cos(angles), radius * np.sin(angles), np.full(n, z)])


def prism(n: int, radius: float, height: float) -> Polyhedron:
    """Recht prisma met een regelmatige n-hoek als grondvlak."""
    bottom = regular_polygon(n, radius, 0.0, np.pi / 2)
    top = regular_polygon(n, radius, height, np.pi / 2)
    faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    faces += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return Polyhedron(np.vstack([bottom, top]), faces)


def pyramid(n: int, radius: float, height: float) -> Polyhedron:
    """Piramide met een regelmatige n-hoek als grondvlak en de top recht boven het midden."""
    base = regular_polygon(n, radius, 0.0, np.pi / 4 if n == 4 else np.pi / 2)
    top = np.array([[0.0, 0.0, height]])
    faces = [list(range(n - 1, -1, -1))] + [[i, (i + 1) % n, n] for i in range(n)]
    return Polyhedron(np.vstack([base, top]), faces)


def unique_edges(faces: list[list[int]]) -> list[tuple[int, int]]:
    """Alle ribben van een veelvlak, elke ribbe één keer."""
    edges: set[tuple[int, int]] = set()
    for face in faces:
        for a, b in zip(face, face[1:] + face[:1]):
            edges.add((min(a, b), max(a, b)))
    return sorted(edges)


def face_mesh(vertices: Array, faces: list[list[int]], color: str, opacity: float = 1.0,
              lighting: dict[str, float] | None = None) -> go.Mesh3d:
    """Vlakken als driehoeken (waaier vanuit het eerste hoekpunt; werkt voor bolle vlakken)."""
    triangles = [(f[0], f[k], f[k + 1]) for f in faces for k in range(1, len(f) - 1)]
    i, j, k = (list(t) for t in zip(*triangles))
    return go.Mesh3d(
        x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2], i=i, j=j, k=k,
        color=color, opacity=opacity, flatshading=True, lighting=lighting or LIGHTING, hoverinfo="skip",
    )


def polyline(points: Array, color: str = EDGE, width: float = 6) -> go.Scatter3d:
    return go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="lines",
                        line=dict(color=color, width=width), hoverinfo="skip", showlegend=False)


def edge_lines(vertices: Array, edges: list[tuple[int, int]], color: str = EDGE, width: float = 6) -> go.Scatter3d:
    """Ribben als lijnstukken (None scheidt de losse stukken)."""
    xs: list[float | None] = []
    ys: list[float | None] = []
    zs: list[float | None] = []
    for a, b in edges:
        xs += [vertices[a, 0], vertices[b, 0], None]
        ys += [vertices[a, 1], vertices[b, 1], None]
        zs += [vertices[a, 2], vertices[b, 2], None]
    return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color=color, width=width),
                        hoverinfo="skip", showlegend=False)


def vertex_dots(vertices: Array, color: str = HIGHLIGHT_VERTEX, size: float = 6) -> go.Scatter3d:
    return go.Scatter3d(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2], mode="markers",
                        marker=dict(size=size, color=color), hoverinfo="skip", showlegend=False)


def solid(shape: Polyhedron) -> Figure3D:
    return [face_mesh(shape.vertices, shape.faces, BODY), edge_lines(shape.vertices, unique_edges(shape.faces))], []


# --------------------------------------------------------- gebogen figuren

def single_colour_surface(x: Array, y: Array, z: Array, color: str = BODY) -> go.Surface:
    return go.Surface(x=x, y=y, z=z, colorscale=[[0, color], [1, color]], showscale=False,
                      lighting=LIGHTING, hoverinfo="skip")


def circle_line(radius: float, z: float, color: str = EDGE) -> go.Scatter3d:
    t = np.linspace(0, 2 * np.pi, 120)
    return polyline(np.column_stack([radius * np.cos(t), radius * np.sin(t), np.full_like(t, z)]), color)


def disk(radius: float, z: float) -> go.Surface:
    r, t = np.meshgrid(np.linspace(0.0, radius, 2), np.linspace(0.0, 2 * np.pi, 80))
    x = np.asarray(r * np.cos(t), dtype=np.float64)
    y = np.asarray(r * np.sin(t), dtype=np.float64)
    return single_colour_surface(x, y, np.full_like(r, z))


def cylinder(radius: float, height: float) -> Figure3D:
    t, z = np.meshgrid(np.linspace(0, 2 * np.pi, 80), np.linspace(0, height, 2))
    side = single_colour_surface(radius * np.cos(t), radius * np.sin(t), z)
    return [side, disk(radius, 0.0), disk(radius, height), circle_line(radius, 0.0), circle_line(radius, height)], []


def cone(radius: float, height: float) -> Figure3D:
    t, s = np.meshgrid(np.linspace(0, 2 * np.pi, 80), np.linspace(0, 1, 2))
    side = single_colour_surface((1 - s) * radius * np.cos(t), (1 - s) * radius * np.sin(t), s * height)
    return [side, disk(radius, 0.0), circle_line(radius, 0.0)], []


def sphere(radius: float) -> Figure3D:
    t, p = np.meshgrid(np.linspace(0, 2 * np.pi, 80), np.linspace(0, np.pi, 40))
    surface = single_colour_surface(radius * np.sin(p) * np.cos(t), radius * np.sin(p) * np.sin(t), radius * np.cos(p))
    return [surface, circle_line(radius, 0.0, color="#9e9e9e")], []


# ------------------------------------------------------ vlakken van een kubus

@dataclass(frozen=True)
class CubeFace:
    """Een zijvlak van de kubus [0, s]^3: midden, normaal (naar buiten) en twee richtingen in het vlak.

    u_axis x v_axis = normal, dus tekst in (u, v) is van buitenaf gewoon leesbaar.
    """

    centre: tuple[float, float, float]
    normal: tuple[float, float, float]
    u_axis: tuple[float, float, float]
    v_axis: tuple[float, float, float]

    def point(self, u: float, v: float, side: float, lift: float = 0.004) -> Array:
        c, n = np.array(self.centre) * side, np.array(self.normal, dtype=np.float64)
        return c + lift * side * n + side * (u * np.array(self.u_axis) + v * np.array(self.v_axis))


FRONT = CubeFace((0.5, 0.0, 0.5), (0, -1, 0), (1, 0, 0), (0, 0, 1))
BACK = CubeFace((0.5, 1.0, 0.5), (0, 1, 0), (-1, 0, 0), (0, 0, 1))
TOP = CubeFace((0.5, 0.5, 1.0), (0, 0, 1), (1, 0, 0), (0, 1, 0))
BOTTOM = CubeFace((0.5, 0.5, 0.0), (0, 0, -1), (1, 0, 0), (0, -1, 0))
LEFT = CubeFace((0.0, 0.5, 0.5), (-1, 0, 0), (0, -1, 0), (0, 0, 1))
RIGHT = CubeFace((1.0, 0.5, 0.5), (1, 0, 0), (0, 1, 0), (0, 0, 1))


def white_cube(side: float) -> list[Trace]:
    cube = box(side, side, side)
    return [face_mesh(cube.vertices, cube.faces, DIE_WHITE, lighting=WHITE_LIGHTING),
            edge_lines(cube.vertices, unique_edges(cube.faces), color="#9e9e9e", width=4)]


# ------------------------------------------------------ dobbelsteen

PIP_LAYOUT: dict[int, list[tuple[float, float]]] = {
    1: [(0, 0)],
    2: [(-0.25, -0.25), (0.25, 0.25)],
    3: [(-0.25, -0.25), (0, 0), (0.25, 0.25)],
    4: [(-0.25, -0.25), (-0.25, 0.25), (0.25, -0.25), (0.25, 0.25)],
    5: [(-0.25, -0.25), (-0.25, 0.25), (0, 0), (0.25, -0.25), (0.25, 0.25)],
    6: [(-0.25, -0.25), (-0.25, 0), (-0.25, 0.25), (0.25, -0.25), (0.25, 0), (0.25, 0.25)],
}

# Overstaande vlakken zijn samen 7, net als bij een echte dobbelsteen.
DIE_FACES: list[tuple[int, CubeFace]] = [(1, FRONT), (6, BACK), (2, TOP), (5, BOTTOM), (3, LEFT), (4, RIGHT)]


def pip_mesh(face: CubeFace, value: int, radius: float = 0.075) -> go.Mesh3d:
    """De ogen van één vlak als platte rondjes, net boven het vlak."""
    t = np.linspace(0, 2 * np.pi, 25)[:-1]
    points: list[Array] = []
    triangles: list[tuple[int, int, int]] = []
    for pu, pv in PIP_LAYOUT[value]:
        start = len(points)
        points.append(face.point(pu, pv, 1.0))
        points += [face.point(pu + radius * np.cos(a), pv + radius * np.sin(a), 1.0) for a in t]
        triangles += [(start, start + 1 + k, start + 1 + (k + 1) % len(t)) for k in range(len(t))]
    p = np.array(points)
    i, j, k = (list(x) for x in zip(*triangles))
    return go.Mesh3d(x=p[:, 0], y=p[:, 1], z=p[:, 2], i=i, j=j, k=k, color=DIE_INK, hoverinfo="skip")


def die() -> Figure3D:
    return white_cube(1.0) + [pip_mesh(face, value) for value, face in DIE_FACES], []


# ---------------------------------------------- kubus met cijfers erop

# Cijfers als pennenstreken in een vakje van 1 breed en 1.6 hoog (midden onderaan is (0.5, 0)).
DIGIT_STROKES: dict[int, list[list[tuple[float, float]]]] = {
    1: [[(0.25, 1.25), (0.55, 1.6), (0.55, 0.0)], [(0.25, 0.0), (0.85, 0.0)]],
    2: [[(0.12, 1.22), (0.22, 1.47), (0.47, 1.6), (0.74, 1.54), (0.88, 1.32), (0.84, 1.05), (0.6, 0.72), (0.12, 0.0)],
        [(0.12, 0.0), (0.92, 0.0)]],
    3: [[(0.12, 1.42), (0.36, 1.6), (0.68, 1.57), (0.86, 1.36), (0.8, 1.04), (0.46, 0.88)],
        [(0.46, 0.88), (0.82, 0.7), (0.9, 0.36), (0.72, 0.06), (0.38, 0.0), (0.1, 0.14)]],
    4: [[(0.7, 0.0), (0.7, 1.6), (0.05, 0.45), (0.95, 0.45)]],
    5: [[(0.85, 1.6), (0.24, 1.6), (0.17, 0.9)],
        [(0.17, 0.9), (0.48, 1.0), (0.78, 0.88), (0.9, 0.52), (0.8, 0.16), (0.5, 0.0), (0.12, 0.1)]],
    6: [[(0.8, 1.5), (0.52, 1.6), (0.26, 1.42), (0.13, 0.92), (0.12, 0.42), (0.28, 0.06), (0.55, 0.0),
         (0.8, 0.12), (0.9, 0.45), (0.78, 0.76), (0.5, 0.86), (0.25, 0.76), (0.13, 0.5)]],
}
STRAIGHT_DIGITS = {1, 4}  # deze cijfers hebben alleen rechte streken


def smooth(points: list[tuple[float, float]], rounds: int = 3) -> list[tuple[float, float]]:
    """Chaikin: hoekjes afronden, de begin- en eindpunten blijven staan."""
    pts = np.array(points, dtype=np.float64)
    for _ in range(rounds):
        q = 0.75 * pts[:-1] + 0.25 * pts[1:]
        r = 0.25 * pts[:-1] + 0.75 * pts[1:]
        middle = np.empty((2 * len(q), 2))
        middle[0::2], middle[1::2] = q, r
        pts = np.vstack([pts[:1], middle, pts[-1:]])
    return [(float(x), float(y)) for x, y in pts]


DIGIT_HEIGHT = 0.45  # hoogte van een cijfer als deel van de zijde van de kubus


def digit_traces(face: CubeFace, digit: int, side: float) -> list[Trace]:
    """Een cijfer plat op een zijvlak, zoals de ogen van een dobbelsteen."""
    s = DIGIT_HEIGHT / 1.6
    traces: list[Trace] = []
    for stroke in DIGIT_STROKES[digit]:
        if digit not in STRAIGHT_DIGITS and len(stroke) > 2:
            stroke = smooth(stroke)
        pts = np.array([face.point((x - 0.5) * s, (y - 0.8) * s, side, lift=0.006) for x, y in stroke])
        traces.append(polyline(pts, color=DIE_INK, width=11))
    return traces


# getallen op de kubus die je krijgt als je de genummerde uitslag (figuren_2d) dichtvouwt
FOLDED_NUMBERS: list[tuple[int, CubeFace]] = [(4, BOTTOM), (1, TOP), (6, FRONT), (2, BACK), (3, LEFT), (5, RIGHT)]


def numbered_cube() -> Figure3D:
    traces = white_cube(2.0)
    for number, face in FOLDED_NUMBERS:
        traces += digit_traces(face, number, 2.0)
    return traces, []


# --------------------------------------------- hoekpunt, ribbe, zijvlak

def cube_parts() -> Figure3D:
    """Kubus met één zijvlak, één ribbe en één hoekpunt gemarkeerd."""
    cube = box(2, 2, 2)
    v = cube.vertices
    front = [0, 1, 5, 4]
    others = [f for f in cube.faces if f != front]
    traces: list[Trace] = [
        face_mesh(v, others, BODY),
        face_mesh(v, [front], HIGHLIGHT_FACE),
        edge_lines(v, unique_edges(cube.faces)),
        edge_lines(v, [(2, 6)], color=HIGHLIGHT_EDGE, width=14),
        vertex_dots(v[[6]], size=10),
    ]
    labels = [
        Label((1.0, 0.0, 1.0), "zijvlak", "#212121", size=22, fixed=True),
        Label((2.0, 2.0, 1.0), "ribbe", HIGHLIGHT_EDGE, size=22),
        Label(tuple(v[6]), "hoekpunt", HIGHLIGHT_VERTEX, size=22),
    ]
    return traces, labels


# ------------------------------------------- figuren bij de uitwerkingen

def numbered(shape: Polyhedron) -> Figure3D:
    """Draadmodel met genummerde hoekpunten: zonder vlakken zie je ook de achterkant."""
    traces: list[Trace] = [edge_lines(shape.vertices, unique_edges(shape.faces)), vertex_dots(shape.vertices)]
    labels = [Label((float(p[0]), float(p[1]), float(p[2])), str(i + 1), HIGHLIGHT_VERTEX, size=20)
              for i, p in enumerate(shape.vertices)]
    return traces, labels


EDGE_GROUP_COLOURS = (HIGHLIGHT_EDGE, HIGHLIGHT_VERTEX, HIGHLIGHT_FACE)  # lengte, breedte, hoogte


def box_edge_groups(length: float, width: float, height: float) -> Figure3D:
    """Balk (draadmodel) waarbij de 4 ribben van dezelfde lengte dezelfde kleur hebben."""
    shape = box(length, width, height)
    v = shape.vertices
    edges = unique_edges(shape.faces)
    traces: list[Trace] = []
    for axis, color in enumerate(EDGE_GROUP_COLOURS):
        group = [(a, b) for a, b in edges if abs(v[a, axis] - v[b, axis]) > 1e-9]
        traces.append(edge_lines(v, group, color=color, width=10))
    labels = [
        Label((length / 2, 0.0, 0.0), f"{length:g} cm", HIGHLIGHT_EDGE),
        Label((length, width / 2, 0.0), f"{width:g} cm", HIGHLIGHT_VERTEX),
        Label((length, 0.0, height / 2), f"{height:g} cm", HIGHLIGHT_FACE),
    ]
    return traces, labels


# ------------------------------------------------------------------ main

DEFAULT_EYE = (1.65, -1.05, 0.85)   # de kijker staat iets rechts van de figuur


def all_figures() -> dict[str, tuple[Figure3D, tuple[float, float, float]]]:
    """Naam -> (figuur, camerarichting)."""
    return {
        "kubus": (solid(box(2, 2, 2)), DEFAULT_EYE),
        "balk": (solid(box(3, 1.6, 1.2)), (1.45, -1.3, 0.85)),
        "cilinder": (cylinder(1.0, 2.2), DEFAULT_EYE),
        "kegel": (cone(1.0, 2.2), DEFAULT_EYE),
        "bol": (sphere(1.0), DEFAULT_EYE),
        "piramide": (solid(pyramid(4, 1.4, 1.8)), (1.8, -0.5, 0.9)),
        "prisma": (solid(prism(3, 1.0, 2.6)), (1.9, -0.55, 0.85)),
        "dobbelsteen": (die(), (1.6, -1.2, 1.05)),
        "kubus hoekpunt ribbe zijvlak": (cube_parts(), DEFAULT_EYE),
        "kubus met getallen": (numbered_cube(), (0.8, -1.55, 1.2)),
        "balk genummerd": (numbered(box(3, 1.6, 1.2)), (1.65, -1.05, 1.1)),
        "balk ribben": (box_edge_groups(5, 3, 2), (1.65, -1.05, 1.1)),
        "vijfhoekig prisma genummerd": (numbered(prism(5, 1.0, 2.0)), (1.1, -1.6, 0.75)),
        "zeshoekige piramide genummerd": (numbered(pyramid(6, 1.2, 1.8)), (1.6, -1.0, 0.9)),
        "piramide genummerd": (numbered(pyramid(4, 1.4, 1.8)), (1.6, -0.8, 1.0)),
    }


def main() -> None:
    for name, ((traces, labels), eye) in all_figures().items():
        save(make_figure(traces, eye, labels), name)


if __name__ == "__main__":
    main()
