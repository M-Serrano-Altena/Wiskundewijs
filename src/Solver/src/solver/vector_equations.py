"""Output for input with vectors or matrices: calculating them, or checking whether two sides are equal."""

from __future__ import annotations

import traceback
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import sympy as sp
import sympy.vector as sp_vector

from src.Solver.src.solver.helper import apply_operator, equation_type_to_latex
from src.Solver.src.solver.latex_printer import custom_latex
from src.Solver.src.solver.linear_algebra import (
    CustomMatrix,
    CustomVector,
    CustomVectorAdd,
    CustomVectorMul,
    convert_symbols_for_vector,
    to_custom_matrix,
)
from src.Solver.src.solver.math_parser import get_uneval_sp_objs
from src.Solver.src.solver.output import SolveOutput, text
from src.Solver.src.solver.safe_parsing import safe_sympify

if TYPE_CHECKING:
    from src.Solver.src.solver.solve_calculations import Solve


def solve_vector(solver: Solve, eq_split: Sequence[str]) -> SolveOutput:
    if len(eq_split) == 1:
        return _output_calculation(solver)

    lhs = _as_vector_side(solver.eq1.simplify())
    rhs = _as_vector_side(solver.eq2.simplify())

    has_equal_sides = apply_operator(lhs, solver.equation_type, rhs)

    if any(isinstance(side, (CustomVector, CustomMatrix, sp.MatrixBase, sp.MatrixExpr)) for side in [lhs, rhs]):
        sides_are_numbers = lhs.contains_only_numbers() and rhs.contains_only_numbers()
    else:
        sides_are_numbers = lhs.is_number and rhs.is_number

    different_types = isinstance(lhs, CustomVector) ^ isinstance(rhs, CustomVector)

    try:
        has_solution = bool(has_equal_sides or sides_are_numbers or different_types)
    except TypeError:
        # the truth value of a symbolic relation is unknown
        has_solution = False

    if solver.eq1_unsimplified == solver.eq1:
        solver.eq1_unsimplified = get_uneval_sp_objs(eq_split[0])
    if solver.eq2_unsimplified != rhs:
        solver.eq2_unsimplified = get_uneval_sp_objs(eq_split[1])

    output = solver.output
    relation = equation_type_to_latex(solver.equation_type)

    if has_solution:
        output.append(text("Vergelijking:"))

    simplify = solver.eq1_unsimplified != lhs or solver.eq2_unsimplified != rhs
    if simplify:
        output.append(f"{custom_latex(solver.eq1_unsimplified)} {relation} {custom_latex(solver.eq2_unsimplified)}")
        output.append(text("Versimpelingen:"))
        if solver.eq1_unsimplified != lhs:
            output.append(f"\\bullet \\quad {custom_latex(solver.eq1_unsimplified)} \\Longrightarrow {custom_latex(lhs)}")
        if solver.eq2_unsimplified != rhs:
            output.append(f"\\bullet \\quad {custom_latex(solver.eq2_unsimplified)} \\Longrightarrow {custom_latex(rhs)}")

    if not has_solution:
        output.append(text("Vereenvoudigde Vergelijking:"))
        output.append(f"{custom_latex(lhs)} {relation} {custom_latex(rhs)}")
        output.append(text("Geen oplossing gevonden"))
        return solver.result()

    if simplify:
        output.append(text("Onze vergelijking wordt dus:"))
    output.append(f"{custom_latex(lhs)} {relation} {custom_latex(rhs)}")

    if has_equal_sides:
        output.append(text("Dit is waar, dus deze vergelijking klopt"))
    elif sides_are_numbers:
        output.append(text("Dit is niet waar, dus deze vergelijking klopt niet"))
    elif different_types:
        output.append(text("Dit is niet waar: de een is een vector, de ander is een getal"))

    return solver.result()


def _output_calculation(solver: Solve) -> SolveOutput:
    """Output for a calculation with vectors or matrices, like vect(1, 2) + vect(3, 4)."""
    eq_string_sp: Any = solver.eq_string
    try:
        try:
            eq_string_sp = get_uneval_sp_objs(solver.eq_string)
        except AttributeError:
            eq_string_sp = safe_sympify(solver.eq_string, solver.locals)

        if eq_string_sp == solver.eq1:
            eq_string_sp = safe_sympify(solver.eq_string, {**solver.locals, **_UNEVALUATED_VECTOR_OPERATIONS}, evaluate=False)
    except Exception:
        traceback.print_exc()

    solver.eq1 = solver.eq1.doit()
    solver.output.append(
        f"{custom_latex(eq_string_sp, vect_dim=solver.vect_dim)} = {custom_latex(solver.eq1, vect_dim=solver.vect_dim)}"
    )
    return solver.result()


def _has_vector(args: tuple[Any, ...]) -> bool:
    return any(isinstance(arg, sp_vector.Vector) for arg in args)


def _unevaluated_add(*args: Any, evaluate: bool = True) -> Any:
    # Since sympy 1.14, sp.Add adds vectors together even with evaluate=False. CustomVectorAdd
    # keeps them apart, so the input can be shown as typed (vect(1, 2) + vect(3, 4) = ...).
    if _has_vector(args):
        return CustomVectorAdd(*args)
    return sp.Add(*args, evaluate=evaluate)


def _unevaluated_mul(*args: Any, evaluate: bool = True) -> Any:
    if _has_vector(args):
        return CustomVectorMul(*args, evaluate=False)
    return sp.Mul(*args, evaluate=evaluate)


# Parsing with evaluate=False builds the expression with calls to Add and Mul, which these replace.
_UNEVALUATED_VECTOR_OPERATIONS = {"Add": _unevaluated_add, "Mul": _unevaluated_mul}


def _as_vector_side(side: Any) -> Any:
    if not isinstance(side, sp_vector.Vector):
        side = convert_symbols_for_vector(side)
    if isinstance(side, sp.MatrixBase):
        side = to_custom_matrix(side)
    return side
