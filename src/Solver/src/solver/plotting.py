"""The Plotly graph of a solved equation: both sides as functions of x, and their intersections.

The x-coordinates cover a range much wider than what's visible at first, so users can pan and
zoom out. Around vertical asymptotes the graph is split into separate pieces, so Plotly doesn't
draw a vertical line through the asymptote.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import numpy as np
import sympy as sp
from sympy.calculus.util import continuous_domain

from src.Solver.src.solver.helper import FloatArray, XRange, segmented_smooth_x_coords, smooth_x_coords
from src.Solver.src.solver.latex_printer import custom_latex
from src.Solver.src.solver.numeric import NumericFunction, apply_func_to_array, numpy_function_or_none

if TYPE_CHECKING:
    from src.Solver.src.solver.solve_calculations import Solve

PlotTrace = dict[str, Any]
BoolArray = np.ndarray[Any, np.dtype[np.bool_]]


def get_range(solver: Solve) -> tuple[FloatArray, FloatArray]:
    """The x and y range to show at first: around the intersections, or [-10, 10] without them."""

    def no_intersect() -> tuple[FloatArray, FloatArray]:
        solver.intersect = False
        solver.x_range = np.array([-10, 10])
        solver.y_range = np.array([-10, 10])
        return solver.x_range, solver.y_range

    if not solver.intersect:
        return no_intersect()

    if solver.solution_set.is_FiniteSet and not (solver.numerical and len(solver.roots_numeric) > 5):
        solver.interval_solutions = solver.solution_set

    solver.interval_solutions = list(solver.interval_solutions)

    x_intersect = np.sort(np.array(sp.Matrix(solver.interval_solutions).evalf(), dtype=np.float64))
    y_intersect = apply_func_to_array(solver.eq1_lambda_np, x_intersect)

    plottable = np.isreal(y_intersect) & np.isfinite(y_intersect)
    solver.x_intersect = x_intersect[plottable]
    solver.y_intersect = y_intersect[plottable].astype(np.float64)
    solver.y_intersect[np.abs(solver.y_intersect) < 1e-6] = 0

    if solver.x_intersect.size == 0:
        return no_intersect()

    x_margin = np.ptp(solver.x_intersect) / 3 + 2
    y_margin = np.ptp(solver.y_intersect) / 3 + 2
    solver.x_range_og = np.array((min(solver.x_intersect) - x_margin, max(solver.x_intersect) + x_margin))
    solver.y_range_og = np.array((min(solver.y_intersect) - y_margin, max(solver.y_intersect) + y_margin))

    solver.x_range = solver.x_range_og
    solver.y_range = solver.y_range_og
    return solver.x_range, solver.y_range


def _with_important_points(solver: Solve, plottable_x_coords: list[float], lambda_func: NumericFunction, domain: Any) -> FloatArray:
    """Add the intersections and the end points of the domain to the x-coordinates."""
    if solver.intersect:
        min_plottable_x = min(plottable_x_coords)
        max_plottable_x = max(plottable_x_coords)
        for x_intersect in solver.x_intersect:
            if min_plottable_x <= x_intersect <= max_plottable_x:
                plottable_x_coords.append(x_intersect)
        plottable_x_coords = sorted(plottable_x_coords)

    return _with_endpoints(plottable_x_coords, lambda_func, domain)


def _with_endpoints(plottable_x_coords: list[float], lambda_func: NumericFunction, domain: Any) -> FloatArray:
    """For a function defined on an interval, extend the graph up to the ends of the interval."""
    try:
        if domain is sp.S.Reals or not domain.is_Interval:
            return np.array(plottable_x_coords)

        for j in range(2):
            end_point = domain.args[j].evalf()
            if end_point.is_finite and np.isfinite(lambda_func(float(end_point))):
                max_plottable_x = max(plottable_x_coords)
                min_plottable_x = min(plottable_x_coords)
                end_point = float(end_point)

                if end_point > max_plottable_x:
                    plottable_x_coords.extend(list(np.linspace(max_plottable_x - 0.1, end_point, 50)))
                elif end_point < min_plottable_x:
                    plottable_x_coords.extend(list(np.linspace(end_point, min_plottable_x + 0.1, 50)))

        x_coords = np.sort(plottable_x_coords)
        return x_coords[(domain.args[0] <= x_coords) & (x_coords <= domain.args[1])]
    except Exception:
        return np.sort(plottable_x_coords)


def _plottable_xy(solver: Solve, x_coords: FloatArray, lambda_func: NumericFunction, domain: Any) -> tuple[FloatArray, FloatArray]:
    """The points of the graph of lambda_func where it's defined and finite."""
    y_coords = lambda_func(x_coords)
    plottable_x_coords = x_coords[np.isreal(y_coords) & np.isfinite(y_coords)].ravel()
    plottable_x_coords = _with_important_points(solver, list(plottable_x_coords), lambda_func, domain).ravel()

    if plottable_x_coords.size != 0:
        # leave out points right before a gap, so separate parts of the graph aren't joined
        before_small_steps = plottable_x_coords[np.where(np.diff(plottable_x_coords) < 1)]
        plottable_x_coords = np.append(before_small_steps, plottable_x_coords[-1])

    return plottable_x_coords, apply_func_to_array(lambda_func, plottable_x_coords)


def _plottable_coords(solver: Solve, x_coords: Any, domain_eq1: Any, domain_eq2: Any) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    x_coords_np = np.array(x_coords)
    x1, y1 = _plottable_xy(solver, x_coords_np, solver.eq1_lambda_np, domain_eq1)
    x2, y2 = _plottable_xy(solver, x_coords_np, solver.eq2_lambda_np, domain_eq2)
    return x1, y1, x2, y2


def _set_vertical_asymptotes(solver: Solve, x_range: XRange) -> None:
    if isinstance(solver.vert_asympt_eq, list):
        vert_asympt = np.array(solver.vert_asympt_eq, dtype=np.float64)
    else:
        asymptote_set: Any = sp.solveset(solver.vert_asympt_eq, domain=sp.Interval(x_range[0], x_range[1])).evalf()
        solver.vert_asympt_set = asymptote_set
        if isinstance(asymptote_set, sp.ConditionSet) and asymptote_set.condition == solver.vert_asympt_eq:
            numerical_asymptotes = solver.solve_numerically(solver.vert_asympt_eq, numpy_function_or_none(solver.vert_asympt_eq, solver.symbol))
            vert_asympt = np.array(numerical_asymptotes, dtype=np.float64)
        else:
            vert_asympt = np.array(list(solver.vert_asympt_set), dtype=np.float64)

    solver.vert_asympt = vert_asympt[np.isreal(vert_asympt)]


def get_plot_data(solver: Solve, x_range: XRange, dx: float = 0.01) -> tuple[list[Any], list[Any], list[Any], list[Any]]:
    """The x and y coordinates of the graphs of both sides.

    Without vertical asymptotes these are arrays; with them, lists with an array per piece.
    """
    if solver.multivariate:
        solver.eq1 = sp.sympify(0)

    if solver.vert_asympt_eq is None:
        solver.x_coords = smooth_x_coords(x_range, dx)
        domain_eq1, domain_eq2 = _domains(solver, numeric=False)
        x1, y1, x2, y2 = _plottable_coords(solver, solver.x_coords, domain_eq1, domain_eq2)
        return list(x1.astype(float)), list(y1.astype(float)), list(x2.astype(float)), list(y2.astype(float))

    _set_vertical_asymptotes(solver, x_range)
    assert solver.vert_asympt is not None
    solver.x_coords = segmented_smooth_x_coords(x_range, dx, solver.vert_asympt)

    domain_eq1, domain_eq2 = _domains(solver, numeric=True)
    pieces = [_plottable_coords(solver, x_coord, domain_eq1, domain_eq2) for x_coord in solver.x_coords]
    return [piece[0] for piece in pieces], [piece[1] for piece in pieces], [piece[2] for piece in pieces], [piece[3] for piece in pieces]


def _domains(solver: Solve, numeric: bool) -> tuple[Any, Any]:
    """Where each side of the equation is defined."""
    if solver.domain_is_reals:
        return sp.S.Reals, sp.S.Reals

    if numeric:
        return (
            continuous_domain(sp.N(solver.eq1), solver.symbol, domain=sp.S.Reals),
            continuous_domain(sp.N(solver.eq2), solver.symbol, domain=sp.S.Reals),
        )

    if solver.multivariate:
        return sp.S.Reals, solver.domain

    return (
        continuous_domain(sp.sympify(solver.eq1), solver.symbol, domain=sp.S.Reals),
        continuous_domain(sp.sympify(solver.eq2), solver.symbol, domain=sp.S.Reals),
    )


def _function_names(solver: Solve) -> tuple[str, str]:
    """f, f' or F for the left side and g, g' or G for the right side."""
    if solver.derivative[0]:
        function_f_type = "f'"
    elif solver.integral[0]:
        function_f_type = "F"
    else:
        function_f_type = "f"

    if len(solver.derivative) == 2 and solver.derivative[1]:
        function_g_type = "g'"
    elif len(solver.integral) == 2 and solver.integral[1]:
        function_g_type = "G"
    else:
        function_g_type = "g"

    if solver.multivariate:
        return "y", "y"
    return f"{function_f_type}({solver.symbol})", f"{function_g_type}({solver.symbol})"


def _hover_template(hoverinfo: str) -> str:
    return "(%{x:.4f}, %{y:.4f})" + f"<extra>{hoverinfo}</extra>"


def _trace(x: Any, y: Any, name: str, color: str, hoverinfo: str, showlegend: bool | None = None) -> PlotTrace:
    trace: PlotTrace = {"x": x, "y": y, "type": "scatter", "mode": "lines", "name": name}
    if showlegend is not None:
        trace["showlegend"] = showlegend
    trace["line"] = {"color": color}
    trace["hovertemplate"] = _hover_template(hoverinfo)
    return trace


# How far a simplified graph may be from the exact one, as a fraction of the size of the graph
# that's visible at first. Plots are about 800 pixels wide, so this is well under a pixel, and
# still under 2 pixels when zoomed in 10 times.
SIMPLIFY_TOLERANCE = 2e-4
SIGNIFICANT_DIGITS = 7


def simplify_line(x: FloatArray, y: FloatArray, tolerance: float) -> BoolArray:
    """Which points of a line to keep so it stays within `tolerance` of the original (a bool array).

    This is the Ramer-Douglas-Peucker algorithm: between two kept points, the point farthest from
    the straight line between them is kept if it's farther than the tolerance, and then both
    halves are checked the same way. Straight stretches need only their two end points.
    """
    amount = len(x)
    keep = np.zeros(amount, dtype=bool)
    if amount == 0:
        return keep
    keep[0] = keep[-1] = True

    stack = [(0, amount - 1)]
    while stack:
        start, end = stack.pop()
        if end - start < 2:
            continue

        line_dx, line_dy = x[end] - x[start], y[end] - y[start]
        between_dx, between_dy = x[start + 1:end] - x[start], y[start + 1:end] - y[start]
        length = np.hypot(line_dx, line_dy)
        if length == 0:
            distances = np.hypot(between_dx, between_dy)
        else:
            distances = np.abs(line_dy * between_dx - line_dx * between_dy) / length

        farthest = int(np.argmax(distances))
        if distances[farthest] > tolerance:
            index = start + 1 + farthest
            keep[index] = True
            stack.append((start, index))
            stack.append((index, end))

    return keep


def _round(values: FloatArray) -> list[float]:
    return [float(f"{value:.{SIGNIFICANT_DIGITS}g}") for value in values]


def simplify_traces(plot_data: list[PlotTrace], view_x_range: XRange, view_y_range: XRange) -> None:
    """Remove the points of the graphs that make no visible difference, to send much less data."""
    x_scale = float(np.ptp(view_x_range)) or 1.0
    y_scale = float(np.ptp(view_y_range)) or 1.0

    for trace in plot_data:
        if trace.get("mode") != "lines":
            continue

        x = np.asarray(trace["x"], dtype=float)
        y = np.asarray(trace["y"], dtype=float)
        # measured relative to the visible part of the graph, so both axes count equally
        keep = simplify_line(x / x_scale, y / y_scale, SIMPLIFY_TOLERANCE)
        trace["x"] = _round(x[keep])
        trace["y"] = _round(y[keep])


def generate_plot_data(solver: Solve, simplify: bool = True) -> tuple[list[PlotTrace], list[float], list[float]]:
    """The Plotly traces for the graph, and the x and y range to show at first."""
    view_x_range, view_y_range = get_range(solver)

    extended_range = 50 * abs(np.ptp(view_x_range)) * np.array([-1, 1])
    dx = 0.02 if solver.vert_asympt_eq is not None and not isinstance(solver.vert_asympt_eq, list) else 0.0001
    x_range = view_x_range + extended_range

    x1, y1, x2, y2 = get_plot_data(solver, x_range, dx=dx)

    if solver.multivariate:
        # the function y = f(x) is the right side of the equation
        x1, y1, x2, y2 = x2, y2, x1, y1
        solver.eq1, solver.eq2 = solver.eq2, solver.eq1

    name1, name2 = _function_names(solver)
    legend1 = f"${name1} = {custom_latex(solver.eq1)}$"
    legend2 = f"${name2} = {custom_latex(solver.eq2)}$"

    hoverinfo1 = f"{name1} = {str(solver.eq1).replace('**', '^').replace('log', 'ln')}"
    hoverinfo2 = f"{name2} = {str(solver.eq2).replace('**', '^').replace('log', 'ln')}"

    # space after the longer legend entry, so it isn't cut off
    if len(hoverinfo1) > len(hoverinfo2):
        legend1 = legend1[:-1] + "\\qquad .$"
    else:
        legend2 = legend2[:-1] + "\\qquad .$"

    if solver.vert_asympt is None:
        plot_data = [
            _trace(x1, y1, legend1, "darkturquoise", hoverinfo1),
            _trace(x2, y2, legend2, "springgreen", hoverinfo2),
        ]
    else:
        plot_data = _traces_per_piece(x1, y1, legend1, "darkturquoise", hoverinfo1)
        plot_data += _traces_per_piece(x2, y2, legend2, "springgreen", hoverinfo2)

    if simplify:
        simplify_traces(plot_data, view_x_range, view_y_range)

    if solver.intersect:
        plot_data.append(_intersection_trace(solver, x_range))

    return plot_data, list(view_x_range), list(view_y_range)


def _traces_per_piece(x_pieces: list[Any], y_pieces: list[Any], name: str, color: str, hoverinfo: str) -> list[PlotTrace]:
    """A trace for every piece of a graph between asymptotes; only the first is in the legend."""
    traces: list[PlotTrace] = []
    skipped = 0
    for i, (x_piece, y_piece) in enumerate(zip(x_pieces, y_pieces)):
        x_list = list(x_piece.astype(float))
        y_list = list(y_piece.astype(float))
        if x_list and y_list:
            traces.append(_trace(x_list, y_list, name, color, hoverinfo, showlegend=i == skipped))
        else:
            skipped += 1
    return traces


def _intersection_trace(solver: Solve, x_range: XRange) -> PlotTrace:
    """The intersections as black dots."""
    if not solver.solution_set.is_FiniteSet and not solver.numerical:
        x_intersect: list[Any] = []
        outside_count = 0
        for solution in solver.solution_set.evalf():
            if x_range[0] <= solution <= x_range[1]:
                x_intersect.append(solution)
                continue
            outside_count += 1
            if outside_count > 10:
                break

        solver.x_intersect = np.array(x_intersect).astype(float)
        solver.y_intersect = apply_func_to_array(solver.eq1_lambda_np, solver.x_intersect)

    elif solver.numerical:
        roots = solver.roots_numeric
        solver.x_intersect = roots[(x_range[0] <= roots) & (roots <= x_range[1])]
        solver.y_intersect = apply_func_to_array(solver.eq1_lambda_np, solver.x_intersect)

    solver.x_intersect = np.round(solver.x_intersect, decimals=8)
    solver.y_intersect = np.round(solver.y_intersect, decimals=8)

    return {
        "x": list(solver.x_intersect),
        "y": list(solver.y_intersect),
        "type": "scatter",
        "mode": "markers",
        "name": "Snijpunt",
        "showlegend": False,
        "marker": {"color": "black", "size": 10},
    }
