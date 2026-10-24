"""The functions available in the solver's input, and some SymPy helpers.

LOCALS maps the names users can type (vect, grad, matrix, ...) to their implementation.
The implementations live in linear_algebra.py, degree_functions.py and latex_printer.py;
they're re-exported here so existing imports keep working.
"""

from __future__ import annotations

from typing import Any

import regex as re
import sympy as sp
import sympy.vector as sp_vector
from sympy.logic.boolalg import BooleanFalse, BooleanTrue

from src.Solver.src.solver.degree_functions import (
    DEG_ARC_GONIO_LOCALS,
    ArcGonioInvalidDomainError,
    ArcReciprocalInvalidDomainError,
    acos_deg,
    angle_deg,
)
from src.Solver.src.solver.helper import equation_type_to_latex, flip_inequality_sign
from src.Solver.src.solver.latex_printer import CustomLatexPrinter, custom_latex
from src.Solver.src.solver.linear_algebra import (
    Abs,
    Angle,
    Cross,
    Curl,
    CustomMatAdd,
    CustomMatMul,
    CustomMatrix,
    CustomVector,
    CustomVectorAdd,
    CustomVectorMul,
    Dot,
    Magnitude,
    VectorShapeError,
    angle,
    convert_symbols_for_vector,
    cross,
    curl,
    det,
    dot,
    grad,
    inverse,
    laplacian,
    matrix,
    r,
    to_custom_matrix,
    to_custom_vector,
    unit,
    vect,
)
from src.Solver.src.solver.safe_parsing import safe_sympify

__all__ = [
    "LOCALS", "DEG_ARC_GONIO_LOCALS", "SYMPY_BOOLEANS", "custom_simplify", "get_real_root",
    "custom_latex", "CustomLatexPrinter", "equation_type_to_latex", "flip_inequality_sign",
    "ArcGonioInvalidDomainError", "ArcReciprocalInvalidDomainError", "acos_deg", "angle_deg",
    "CustomVector", "CustomVectorAdd", "CustomVectorMul", "CustomMatrix", "CustomMatAdd", "CustomMatMul",
    "VectorShapeError", "Magnitude", "Angle", "convert_symbols_for_vector", "to_custom_vector",
    "to_custom_matrix", "r", "vect", "matrix", "inverse", "det", "Abs", "unit", "grad", "laplacian",
    "angle", "dot", "Dot", "cross", "Cross", "curl", "Curl",
]

SYMPY_BOOLEANS = (BooleanTrue, BooleanFalse)

LOCALS: dict[str, Any] = {
    "vect": vect,
    "Abs": Abs,
    "r": r,
    "dot": dot,
    "Dot": Dot,
    "cross": cross,
    "Cross": Cross,
    "div": sp_vector.divergence,
    "Divergence": sp_vector.Divergence,
    "curl": curl,
    "Curl": Curl,
    "grad": grad,
    "Gradient": sp_vector.Gradient,
    "laplacian": laplacian,
    "Laplacian": sp_vector.Laplacian,
    "magnitude": Abs,
    "Magnitude": Magnitude,
    "unit": unit,
    "norm": unit,
    "normalize": unit,
    "angle": angle,
    "Angle": Angle,
    "matrix": matrix,
    "inverse": inverse,
    "det": det,
}


def custom_simplify(expr: Any) -> Any:
    """Simplify an expression, and expand logarithms. Returns expr unchanged if that fails."""
    if not isinstance(expr, sp.Basic):
        return expr

    if expr.is_number:
        return sp.nsimplify(expr)

    try:
        simplified = sp.simplify(expr)
    except Exception:
        return expr

    try:
        return sp.expand_log(simplified)
    except Exception:
        return simplified


def get_real_root(expr: Any) -> Any:
    """Replace x**(1/3) by sign(x)*|x|**(1/3), so odd roots of negative numbers are real (for plotting)."""

    def replace_root(match: re.Match[str]) -> str:
        base, power = match.group(1), match.group(2)
        power_sp: Any = safe_sympify(power)
        if power_sp.q % 2 == 0 or power_sp.p % 2 == 0:
            return f"Abs({base})**({power})"
        return f"sign({base})*Abs({base})**({power})"

    str_expr = str(expr)
    str_expr = re.sub(r"(\w*\(.*\))\*\*\((-*\d+/\d+)\)", replace_root, str_expr)
    str_expr = re.sub(r"(\w+)\*\*\((-*\d+/\d+)\)", replace_root, str_expr)
    return safe_sympify(str_expr)
