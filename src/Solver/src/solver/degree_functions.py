"""Inverse trigonometric functions that give their answer in degrees, used in degree mode."""

from __future__ import annotations

from typing import Any

import sympy as sp
from sympy.physics.units import degree


class ArcGonioInvalidDomainError(ValueError):
    """Raised when arcsin, arccos, ... get a value for which the answer isn't real."""

    def __init__(self, message: str = "Operation requires a valid input that yields a real result for arc-goniometric functions") -> None:
        super().__init__(message)


class ArcReciprocalInvalidDomainError(ArcGonioInvalidDomainError):
    """Raised when arcsec or arccsc get a value between -1 and 1."""


# 180/π: multiplying an angle in radians by this gives degrees
DEGREES_PER_RADIAN = 180 / sp.pi


def _without_degree(arg: Any) -> Any:
    return sp.nsimplify(sp.sympify(arg).subs(degree, 1), rational=True)


def _in_degrees(radians: Any) -> Any:
    """An angle in degrees: exact (30) when possible, otherwise a decimal."""
    degrees = sp.deg(radians)
    if not degrees.is_Rational:
        degrees = sp.N(degrees, 10)
    return degrees * degree


def _arc_function(function: Any, arg: Any, invalid_domain: Any, variable_in_degrees: bool) -> Any:
    arg = _without_degree(arg)
    if arg.has(sp.Symbol):
        # in degree mode, arcsin(x) = 30 is solved in degrees too; otherwise arcsin(x) is in radians
        return DEGREES_PER_RADIAN * function(arg) if variable_in_degrees else function(arg)
    if invalid_domain is not None and invalid_domain(arg):
        raise ArcReciprocalInvalidDomainError() if function in (sp.asec, sp.acsc) else ArcGonioInvalidDomainError()
    return _in_degrees(function(arg))


def _outside_minus_one_to_one(value: Any) -> bool:
    return not -1 <= value <= 1


def _between_minus_one_and_one(value: Any) -> bool:
    return -1 < value < 1


_ARC_FUNCTIONS: dict[str, tuple[Any, Any]] = {
    "asin": (sp.asin, _outside_minus_one_to_one),
    "acos": (sp.acos, _outside_minus_one_to_one),
    "atan": (sp.atan, None),
    "asec": (sp.asec, _between_minus_one_and_one),
    "acsc": (sp.acsc, _between_minus_one_and_one),
    "acot": (sp.acot, None),
}


def degree_arc_locals(variable_in_degrees: bool) -> dict[str, Any]:
    """arcsin, arccos, ... that give degrees, and angle() between vectors in degrees.

    variable_in_degrees: whether arcsin(x) with a variable is in degrees as well (degree mode).
    """
    functions: dict[str, Any] = {
        name: (lambda arg, function=function, invalid=invalid: _arc_function(function, arg, invalid, variable_in_degrees))
        for name, (function, invalid) in _ARC_FUNCTIONS.items()
    }
    functions["angle"] = angle_deg
    return functions


def acos_deg(arg: Any) -> Any:
    return _arc_function(sp.acos, arg, _outside_minus_one_to_one, variable_in_degrees=False)


def angle_deg(v1: Any, v2: Any) -> Any:
    """The angle between two vectors, in degrees."""
    return acos_deg(v1.dot(v2) / (v1.magnitude() * v2.magnitude()))


DEG_ARC_GONIO_LOCALS = degree_arc_locals(variable_in_degrees=False)
