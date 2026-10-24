"""Small helper functions used throughout the solver."""

from __future__ import annotations

import operator
from collections.abc import Callable, Hashable, Iterable, Sequence
from typing import Any, TypeVar

import numpy as np
import sympy as sp
from sympy.simplify.fu import TR1, TR2

T = TypeVar("T", bound=Hashable)
FloatArray = np.ndarray[Any, np.dtype[np.float64]]
XRange = Sequence[float] | FloatArray

_COMPARISON_OPERATORS: dict[str, Callable[[Any, Any], Any]] = {
    "==": operator.eq,
    "=": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}

_SYMPY_RELATIONS: dict[str, Callable[..., Any]] = {
    "!=": sp.Ne, ">=": sp.Ge, "<=": sp.Le, "==": operator.eq, "=": sp.Eq, ">": sp.Gt, "<": sp.Lt,
}

_RELATION_LATEX = {"!=": "\\neq", ">=": "\\geq", "<=": "\\leq"}
_FLIPPED_RELATION = {">": "<", "<": ">", ">=": "<=", "<=": ">=", "!=": "=", "=": "!="}


def unique_preserve_order(items: Iterable[T]) -> list[T]:
    """Remove duplicates, keeping the first occurrence of every item."""
    return list(dict.fromkeys(items))


def apply_operator(x: Any, relation: str, y: Any) -> Any:
    """Compare x and y with a relation like "=", ">=" or "!="."""
    try:
        return _COMPARISON_OPERATORS[relation](x, y)
    except KeyError:
        raise ValueError(f"Invalid operator: {relation}") from None


def map_equation_type_to_sp(relation: str) -> Callable[..., Any]:
    """Return the sympy class for a relation, like sp.Eq for "="."""
    return _SYMPY_RELATIONS[relation]


def equation_type_to_latex(relation: str) -> str:
    return _RELATION_LATEX.get(relation, relation)


def flip_inequality_sign(relation: str) -> str:
    return _FLIPPED_RELATION.get(relation, relation)


def segmented_linspace(
    start: float, end: float, breakpoints: Iterable[float], num: int = 10, breakpoint_offset: float = 0.01
) -> list[FloatArray]:
    """Evenly spaced points from start to end, split into segments at the breakpoints."""
    all_points = sorted([start, *breakpoints, end])
    return [
        np.linspace(all_points[i] + breakpoint_offset, all_points[i + 1] - breakpoint_offset, num)
        for i in range(len(all_points) - 1)
    ]


def smooth_x_coords(x_range: XRange, dx: float) -> FloatArray:
    """x-coordinates over x_range, with extra points close to 0 so graphs look smooth there."""
    x_coords = np.linspace(x_range[0] - 1, x_range[1] + 1, int(1 / dx))
    for i in range(1, 10):
        scale = 10**i
        extra_points = np.linspace(x_range[0] / scale, x_range[1] / scale, max(10, int(10 / (dx * scale))))
        x_coords = np.sort(np.append(x_coords, extra_points))
    return x_coords


def segmented_smooth_x_coords(x_range: XRange, dx: float, vert_asympt: Iterable[float]) -> list[FloatArray]:
    """Like smooth_x_coords, but split into separate segments at the vertical asymptotes."""
    vert_asympt = list(vert_asympt)
    x_coords = segmented_linspace(x_range[0] - 1, x_range[1] + 1, vert_asympt, num=int(1 / dx), breakpoint_offset=0.00001)
    if len(x_coords) > 3:
        return x_coords

    for i in range(1, 5):
        scale = 10**i
        new_x_coords = segmented_linspace(
            x_range[0] / scale, x_range[1] / scale, vert_asympt, num=max(10, int(10 / (dx * scale))), breakpoint_offset=0.00001
        )
        for j, array in enumerate(x_coords):
            min_array, max_array = min(array), max(array)
            for array_new in new_x_coords:
                if min_array <= np.mean(array_new) <= max_array:
                    x_coords[j] = np.sort(np.append(array, array_new))

    return x_coords


def write_as_sin_and_cos(expr: Any) -> Any:
    """Write sec, csc, tan and cot in terms of sin and cos."""
    return TR1(TR2(expr))


def round_list_val_with_symbolic(values: list[Any], amt_digits: int = 5) -> list[Any]:
    """Round the purely numeric values in the list (in place), leaving symbolic values as they are."""
    for i, value in enumerate(values):
        if sp.sympify(value).equals(sp.N(value)):
            values[i] = sp.N(value, amt_digits)
    return values


def transform_dict_list_to_list_dict(input_dict: dict[Any, list[Any]]) -> list[dict[Any, Any]]:
    """{'a': [1, 2], 'b': [3, 4]} -> [{'a': 1, 'b': 3}, {'a': 2, 'b': 4}]"""
    keys = list(input_dict)
    return [dict(zip(keys, values)) for values in zip(*input_dict.values())]


def normalize_eq(eq: Any) -> Any:
    """Move everything to one side and drop numeric factors, so equivalent equations compare equal."""
    expr: Any = sp.gcd_terms(sp.simplify(eq.lhs - eq.rhs))
    if expr.is_Mul:
        non_numeric_factors = [factor for factor in expr.args if not factor.is_number]
        if not non_numeric_factors:
            return expr
        expr = non_numeric_factors[0]
    return expr


def equivalent_eq(eq1: Any, eq2: Any) -> bool:
    if eq1.free_symbols != eq2.free_symbols:
        return False

    if eq1.is_number and eq2.is_number:
        return eq1 == eq2

    norm_eq1 = normalize_eq(eq1)
    norm_eq2 = normalize_eq(eq2)
    return bool(norm_eq1 - norm_eq2 == 0 or norm_eq1 + norm_eq2 == 0)


def unique_equivalent_eqs(equations: list[Any]) -> list[Any]:
    """Remove equations that are equivalent to an earlier one (like 2x = 2y and x = y)."""
    unique_eqs: list[Any] = []
    seen_normalized: set[Any] = set()
    for eq in unique_preserve_order(equations):
        normalized_eq = normalize_eq(eq)
        if normalized_eq not in seen_normalized:
            seen_normalized.add(normalized_eq)
            seen_normalized.add(-normalized_eq)
            unique_eqs.append(eq)
    return unique_eqs
