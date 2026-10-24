"""Numerical tools: turning expressions into numpy functions and finding roots numerically."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

import numpy as np
import sympy as sp
from scipy.optimize import bisect, fsolve, newton

from src.Solver.src.solver.helper import FloatArray, segmented_smooth_x_coords, smooth_x_coords
from src.Solver.src.solver.sympy_custom_funcs import get_real_root

NumericFunction = Callable[..., Any]
RootMethod = Literal["newton", "fsolve", "bisect"]


def _no_numeric_function(*args: Any) -> Any:
    # Stands in for an expression that couldn't be turned into a numeric function. Calling it
    # raises the TypeError the solver relies on to switch to its fallback for such expressions.
    raise TypeError("expression could not be converted to a numeric function")


def sympy_function(expr: Any, symbol: Any) -> NumericFunction:
    """expr as a Python function of symbol, evaluated with sympy (exact)."""
    return sp.lambdify(symbol, expr, "sympy")


def numpy_function(expr: Any, symbol: Any) -> NumericFunction:
    """expr as a fast numeric function of symbol, using numpy if possible (then scipy, then sympy)."""
    return numpy_function_or_none(expr, symbol) or _no_numeric_function


def numpy_function_or_none(expr: Any, symbol: Any) -> NumericFunction | None:
    """Like numpy_function, but None if expr can't be turned into a numeric function."""
    for module in ["numpy", "scipy", "sympy"]:
        try:
            expr = get_real_root(expr)
            func = sp.lambdify(symbol, expr, module)
            try:
                func(0)
            except ZeroDivisionError:
                func(1)
            return func
        except NameError:
            # a function in expr doesn't exist in this module
            continue

    return None


def apply_func_to_array(func: NumericFunction, array: FloatArray) -> FloatArray:
    """func(array) as a float array, also when func is constant."""
    try:
        values = func(array)
    except ZeroDivisionError:
        values = func(array + 1e-10)

    if np.isscalar(values):
        return np.full(array.shape, values).astype(float)
    return values.astype(float)


def find_roots(
    eq_sp: Any,
    eq_lambda_np: NumericFunction,
    symbol: Any,
    a: float = -10000,
    b: float = 10000,
    dx: float = 1e-6,
    solve_method: RootMethod = "newton",
    tolerance: float = 0.01,
    vert_asympt: FloatArray | None = None,
) -> tuple[FloatArray, bool]:
    """Find the roots of eq_sp between a and b.

    The function is evaluated on a fine grid, and every stretch where it's close to 0 gives a
    starting point for the root finding method. Returns the roots, and whether there were any
    points close to 0 to start from.
    """
    eq_diff_lambda_np: NumericFunction | None = None
    if solve_method == "newton":
        eq_diff_sp = sp.diff(eq_sp, symbol).doit().simplify()
        eq_diff_lambda_np = numpy_function(eq_diff_sp, symbol)

    if vert_asympt is None:
        x_vals: Any = smooth_x_coords((a, b), dx)
    else:
        x_vals = segmented_smooth_x_coords((a, b), dx, vert_asympt)
    y_vals = eq_lambda_np(x_vals)
    xy = np.vstack((x_vals, y_vals)).T
    xy = xy[~np.isnan(xy[:, 1]) & ~np.isinf(xy[:, 1])]

    if xy.size == 0:
        return np.array([]), False

    closest_to_zero = xy[np.argmin(np.abs(xy[:, 1]))]
    y_value_shift = eq_lambda_np(closest_to_zero[0] + tolerance)
    y_value_shift = tolerance if np.isnan(y_value_shift) or np.isinf(y_value_shift) else y_value_shift
    tolerance = 3 * abs(y_value_shift - closest_to_zero[1])

    near_zero_indices = np.where(np.abs(xy[:, 1]) < tolerance)[0]
    if near_zero_indices.size == 0:
        return np.array([]), False

    # split the indices into stretches of consecutive points
    discontinuities = np.where(np.diff(near_zero_indices) != 1)[0] + 1
    roots: list[float] = []
    for indices in np.split(near_zero_indices, discontinuities):
        if indices.size == 0:
            continue

        root = _find_root_near(eq_lambda_np, eq_diff_lambda_np, xy[indices], solve_method)
        if root is not None and not np.isnan(root):
            roots.append(root)

    return _clean_roots(np.array(roots), eq_lambda_np, a, b), True


def _find_root_near(
    eq_lambda_np: NumericFunction, eq_diff_lambda_np: NumericFunction | None, xy: FloatArray, solve_method: RootMethod
) -> float | None:
    min_index = np.argmin(np.abs(xy), axis=0)[1]
    guess = xy[min_index, 0]

    try:
        if solve_method == "newton":
            root: Any = newton(eq_lambda_np, guess, fprime=eq_diff_lambda_np)
            return float(root)

        if solve_method == "bisect":
            a_bisect, b_bisect = np.min(xy), np.max(xy)
            try:
                if eq_lambda_np(a_bisect) * eq_lambda_np(b_bisect) < 0:
                    bisect_root: Any = bisect(eq_lambda_np, a_bisect, b_bisect)
                    return float(bisect_root)
            except ValueError:
                pass
            return None

        return float(np.asarray(fsolve(eq_lambda_np, guess)).ravel()[0])
    except RuntimeError:
        # the method didn't converge
        return None


def _clean_roots(roots: FloatArray, eq_lambda_np: NumericFunction, a: float, b: float) -> FloatArray:
    """Remove duplicates, roots outside [a, b], and roots at a or b where the graph only touches 0."""
    roots = np.unique(roots[(roots >= a) & (roots <= b)])

    if a in roots and eq_lambda_np(a - 1) * eq_lambda_np(a + 1) >= 0:
        roots = np.delete(roots, np.where(roots == a))
    if b in roots and eq_lambda_np(b - 1) * eq_lambda_np(b + 1) >= 0:
        roots = np.delete(roots, np.where(roots == b))

    return roots[(np.isfinite(eq_lambda_np(roots + 0.01))) | (np.isfinite(eq_lambda_np(roots - 0.01)))]
