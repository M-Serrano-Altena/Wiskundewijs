"""The simplified graphs must look the same as the full graphs."""

import numpy as np
import pytest

from src.Solver.src.solver.plotting import SIMPLIFY_TOLERANCE, generate_plot_data, simplify_line
from src.Solver.src.solver.solve_calculations import Solve


def max_distance_to_simplified(x: np.ndarray, y: np.ndarray, simple_x: np.ndarray, simple_y: np.ndarray) -> float:
    """The largest distance from a point of the full line to the simplified line."""
    largest = 0.0
    segment = 0
    for px, py in zip(x, y):
        # the simplified points are a subset of the full points, in the same order
        while segment < len(simple_x) - 2 and px > simple_x[segment + 1]:
            segment += 1
        ax, ay, bx, by = simple_x[segment], simple_y[segment], simple_x[segment + 1], simple_y[segment + 1]
        length = np.hypot(bx - ax, by - ay)
        if length == 0:
            distance = np.hypot(px - ax, py - ay)
        else:
            distance = abs((by - ay) * (px - ax) - (bx - ax) * (py - ay)) / length
        largest = max(largest, float(distance))
    return largest


def test_straight_line_keeps_only_end_points() -> None:
    x = np.linspace(-10, 10, 1000)
    assert simplify_line(x, 2 * x + 1, 1e-6).sum() == 2


def test_simplified_sine_stays_close() -> None:
    x = np.linspace(0, 20, 20000)
    y = np.sin(x)
    keep = simplify_line(x, y, 1e-3)
    assert keep.sum() < 1000
    assert max_distance_to_simplified(x, y, x[keep], y[keep]) <= 1e-3


@pytest.mark.parametrize("equation", ["x^2 - 5x + 6 = 0", "1/x = 2", "y = sin(x)", "e^x = 3x", "sqrt(4 - x^2) = 1"])
def test_simplified_graph_matches_full_graph(equation: str) -> None:
    full_solver = Solve(equation, None)
    full_solver.solve_equation()
    full, view_x, view_y = generate_plot_data(full_solver, simplify=False)

    simple_solver = Solve(equation, None)
    simple_solver.solve_equation()
    simple, _, _ = generate_plot_data(simple_solver, simplify=True)

    assert len(full) == len(simple)
    x_scale, y_scale = np.ptp(view_x), np.ptp(view_y)
    for full_trace, simple_trace in zip(full, simple):
        if full_trace["mode"] != "lines":
            assert full_trace == simple_trace
            continue
        distance = max_distance_to_simplified(
            np.asarray(full_trace["x"], dtype=float) / x_scale,
            np.asarray(full_trace["y"], dtype=float) / y_scale,
            np.asarray(simple_trace["x"], dtype=float) / x_scale,
            np.asarray(simple_trace["y"], dtype=float) / y_scale,
        )
        # a little extra room for rounding the coordinates
        assert distance <= 1.5 * SIMPLIFY_TOLERANCE, f"{full_trace['name']}: {distance}"
