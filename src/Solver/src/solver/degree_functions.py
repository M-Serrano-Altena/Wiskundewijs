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


def _without_degree(arg: Any) -> Any:
    return sp.sympify(arg).subs(degree, 1)


def _in_degrees(radians: Any) -> Any:
    return sp.N(sp.deg(radians), 4) * degree


def asin_deg(arg: Any) -> Any:
    arg = _without_degree(arg)
    if arg.has(sp.Symbol):
        return sp.asin(arg)
    if not -1 <= arg <= 1:
        raise ArcGonioInvalidDomainError()
    return _in_degrees(sp.asin(arg))


def acos_deg(arg: Any) -> Any:
    arg = _without_degree(arg)
    if arg.has(sp.Symbol):
        return sp.acos(arg)
    if not -1 <= arg <= 1:
        raise ArcGonioInvalidDomainError()
    return _in_degrees(sp.acos(arg))


def atan_deg(arg: Any) -> Any:
    arg = _without_degree(arg)
    if arg.has(sp.Symbol):
        return sp.atan(arg)
    return _in_degrees(sp.atan(arg))


def asec_deg(arg: Any) -> Any:
    arg = _without_degree(arg)
    if arg.has(sp.Symbol):
        return sp.asec(arg)
    if -1 <= arg <= 1:
        raise ArcReciprocalInvalidDomainError()
    return _in_degrees(sp.asec(arg))


def acsc_deg(arg: Any) -> Any:
    arg = _without_degree(arg)
    if -1 <= arg <= 1:
        raise ArcReciprocalInvalidDomainError()
    return _in_degrees(sp.acsc(arg))


def acot_deg(arg: Any) -> Any:
    return _in_degrees(sp.acot(arg))


def angle_deg(v1: Any, v2: Any) -> Any:
    """The angle between two vectors, in degrees."""
    return acos_deg(v1.dot(v2) / (v1.magnitude() * v2.magnitude()))


DEG_ARC_GONIO_LOCALS: dict[str, Any] = {
    "asin": asin_deg,
    "acos": acos_deg,
    "atan": atan_deg,
    "asec": asec_deg,
    "acsc": acsc_deg,
    "acot": acot_deg,
    "angle": angle_deg,
}
