"""LaTeX output for the solver, adjusted to how maths is written in Dutch secondary school.

For example: mixed fractions (1 1/2), x = a + k·2π for periodic solutions, arcsin instead of
sin^-1, ^b log(x) for logarithms and column vectors.
"""

# LatexPrinter dispatches to the _print_<Class> methods by name, so their exact signatures don't matter.
# pyright: reportIncompatibleMethodOverride=false

from __future__ import annotations

from typing import Any

import regex as re
import sympy as sp
import sympy.vector as sp_vector
from sympy.printing.latex import LatexPrinter

from src.Solver.src.solver.helper import equation_type_to_latex, flip_inequality_sign
from src.Solver.src.solver.linear_algebra import CustomVector, dot, r
from src.Solver.src.solver.safe_parsing import safe_sympify

_VECTOR_IN_BRACKETS = re.compile(
    re.escape(r"\left(") + "(" + re.escape(r"\begin{pmatrix}") + r"(.*?)" + re.escape(r"\end{pmatrix}") + ")" + re.escape(r"\right)")
)

_ARC_FUNCTIONS = {
    "asin": "\\arcsin",
    "acos": "\\arccos",
    "atan": "\\arctan",
    "asec": "\\arcsec",
    "acsc": "\\arccsc",
    "acot": "\\arccot",
}


def _remove_unit_factor(latex: str) -> str:
    latex = latex.replace("1 \\cdot", " ")
    return re.sub(r"\\left\(-(\d+)\\right\) ", r"- \1 \\cdot", latex)


class CustomLatexPrinter(LatexPrinter):
    def __init__(self, **kwargs: Any) -> None:
        self.symbol = kwargs.get("symbol", "x")
        self.vect_dim = kwargs.get("vect_dim", 3)
        super().__init__()

    def _print_periodic_solution(self, image_set: Any) -> str:
        """{2nπ + a | n ∈ Z} -> a + k·2π"""
        element_expr: Any = sp.expand(image_set.lamda.expr)
        coeff, summation = element_expr.as_coeff_add()
        if coeff != 0:
            summation = (coeff, *summation)

        terms = [
            f"k \\cdot {str(self._print(term)).replace('n', '')}" if "_n" in str(term) else self._print(term)
            for term in summation
        ]
        return " + ".join(terms).replace("n", "k")

    def _print_Union(self, expr: Any, **kwargs: Any) -> str:
        """Periodic solutions as x = a + k·2π ∨ x = b + k·2π instead of set notation."""
        parts = [self._print_periodic_solution(arg) for arg in expr.args if isinstance(arg, sp.ImageSet)]
        return f" \\ \\vee \\ {self.symbol} = ".join(parts)

    def _print_ImageSet(self, expr: Any, **kwargs: Any) -> str:
        return self._print_periodic_solution(expr)

    def _print_Relational(self, expr: Any, **kwargs: Any) -> str:
        """Always print the variable on the left: 3 < x instead of x > 3 stays x > 3, 3 > x becomes x < 3."""
        if expr.lhs.is_Symbol:
            return super()._print_Relational(expr, **kwargs)

        flipped_relation = equation_type_to_latex(flip_inequality_sign(expr.rel_op))
        return f"{self._print(expr.rhs)} {flipped_relation} {self._print(expr.lhs)}"

    def _print_Or(self, expr: Any, **kwargs: Any) -> str:
        if len(expr.args) != 2:
            return super()._print_Or(expr, **kwargs)

        return " \\ \\vee \\ ".join(self._print(arg) for arg in (expr.args[1], expr.args[0]))

    def _print_And(self, expr: Any, **kwargs: Any) -> str:
        """x > 1 ∧ x < 3 -> 1 < x < 3"""
        if len(expr.args) != 2:
            return super()._print_And(expr, **kwargs)

        expr_left, expr_right = expr.args

        def symbol_value_pair(relation: Any) -> tuple[Any, Any]:
            if relation.args[0].is_Symbol:
                return relation.args[0], relation.args[1]
            return relation.args[1], relation.args[0]

        symbol_left, value_left = symbol_value_pair(expr_left)
        symbol_right, value_right = symbol_value_pair(expr_right)

        if value_left.evalf() < value_right.evalf():
            lower_bound, upper_bound = value_left, value_right
        else:
            lower_bound, upper_bound = value_right, value_left

        if symbol_left != symbol_right or not symbol_left.is_Symbol:
            return super()._print_And(expr, **kwargs)

        def as_smaller_than(relation: str) -> str:
            return {">=": "<=", ">": "<"}.get(relation, relation)

        left_inequality = equation_type_to_latex(as_smaller_than(expr_left.rel_op))
        right_inequality = equation_type_to_latex(as_smaller_than(expr_right.rel_op))
        return f"{self._print(lower_bound)} {left_inequality} {self._print(symbol_left)} {right_inequality} {self._print(upper_bound)}"

    def _print_Rational(self, expr: Any, **kwargs: Any) -> str:
        """Fractions as mixed numbers: 3/2 -> 1 1/2."""
        numer, denom = expr.as_numer_denom()
        integer_part = numer // denom
        fractional_part = abs(numer) % abs(denom)

        if fractional_part == 0:
            return rf"{integer_part}"
        if integer_part == 0:
            return rf"\frac{{{fractional_part}}}{{{denom}}}"
        if integer_part == -1:
            return rf"- \frac{{{fractional_part}}}{{{denom}}}"
        if integer_part < -1:
            return rf"{int(numer / denom)} \frac{{{abs(fractional_part)}}}{{{denom}}}"
        return rf"{integer_part} \frac{{{fractional_part}}}{{{denom}}}"

    def _print_Mul(self, expr: Any, **kwargs: Any) -> str:
        if expr.as_numer_denom()[1] == 1:
            return self._print_Mul_without_denominator(expr)

        # a rational number times a symbol, like 3/2 x
        sym_part: Any
        numer: Any
        denom: Any
        if any(expr.has(obj) for obj in [sp.Symbol, sp.pi, sp.E]):
            coeff, sym_part = sp.nsimplify(safe_sympify(str(expr))).as_coeff_Mul()
            numer, denom = coeff.as_numer_denom()
            if denom == 1:
                numer, denom = expr.as_numer_denom()
        else:
            sym_part = 1
            numer, denom = expr.as_numer_denom()

        if isinstance(numer, sp.Integer) and isinstance(denom, sp.Integer):
            latex = self._print_Rational(sp.Rational(numer, denom), **kwargs)
            if sym_part != 1:
                latex += self._print(sym_part)
            return latex

        numer, denom = expr.as_numer_denom()

        # log(x)/log(2) -> ^2 log(x)
        if isinstance(numer, sp.log) and isinstance(denom, sp.log):
            arg, base = numer.args[0], denom.args[0]
            if isinstance(base, sp.Number):
                return f" \\ ^{{{self._print(base)}}} \\! \\log\\left({self._print(arg)} \\right)"

        if expr.has(CustomVector):
            return f"{self._print(sp.S.One / denom)} \\cdot {self._print(numer)}"

        return _remove_unit_factor(sp.latex(expr))

    def _print_Mul_without_denominator(self, expr: Any) -> str:
        if (
            len(expr.args) == 2
            and all(isinstance(arg, CustomVector) for arg in expr.args)
            and dot(expr.args[0], expr.args[1]).is_number
        ):
            return f"{self._print(expr.args[0])} \\cdot {self._print(expr.args[1])}"

        return _remove_unit_factor(super()._print_Mul(expr))

    def _print_Pow(self, expr: Any, **kwargs: Any) -> str:
        base, exp = expr.as_base_exp()

        if expr.is_Rational and exp.q != 1 and expr != sp.root(base, 1 / exp, evaluate=False):
            return f"{self._print(base)}^{{{self._print(sp.simplify(exp))}}}"

        if expr.as_numer_denom()[1] != 1:
            return sp.latex(sp.nsimplify(expr))

        vector_types = [CustomVector, sp_vector.Gradient]
        if any(base.has(class_) for class_ in vector_types) and any(exp.has(class_) for class_ in vector_types):
            # vector ^ vector is the cross product
            return f"{self._print(base)} \\times {self._print(exp)}"

        return sp.latex(expr).replace("log", "ln").replace("circ", "\\circ")

    def _print_log(self, expr: Any, **kwargs: Any) -> str:
        arg = self._print(expr.args[0])
        if len(expr.args) == 1:
            return f"\\ln \\left({arg} \\right)"
        if len(expr.args) == 2:
            return f" \\ ^{{{self._print(expr.args[1])}}} \\! \\log\\left({arg} \\right)"
        return super()._print_log(expr)

    def _print_Limit(self, expr: Any, **kwargs: Any) -> str:
        """Show a one-sided limit with ↓ or ↑, but only if the limit from the other side is different."""
        func, var, point, direction = expr.args
        limit_expr = str(expr)
        limit_value = sp.simplify(expr)

        if str(direction) == "+":
            limit_expr_opposite = limit_expr.replace("dir='+'", "dir='-'")
        else:
            limit_expr_opposite = limit_expr.replace("dir='-'", "dir='+'")

        limit_value_opposite = sp.simplify(safe_sympify(limit_expr_opposite))

        if limit_value == limit_value_opposite:
            return f"\\lim_{{{self._print(var)} \\, \\to \\, {self._print(point)}}} {self._print(func)}"
        if str(direction) == "+":
            return f"\\lim_{{{self._print(var)} \\, \\downarrow \\, {self._print(point)}}} {self._print(func)}"
        if str(direction) == "-":
            return f"\\lim_{{{self._print(var)} \\, \\uparrow \\, {self._print(point)}}} {self._print(func)}"
        return super()._print_Limit(expr)

    def _print_Function(self, expr: Any, **kwargs: Any) -> str:
        func_name = expr.func.__name__
        if func_name in _ARC_FUNCTIONS:
            return rf"{_ARC_FUNCTIONS[func_name]}{{\left({self._print(expr.args[0])}\right)}}"
        return super()._print_Function(expr, **kwargs)

    def _print_Vector(self, expr: Any, **kwargs: Any) -> str:
        """Vectors as a column."""
        unit_vects = [r.i, r.j, r.k][: self.vect_dim]
        components = [expr.dot(unit_vect) for unit_vect in unit_vects]
        return r"\begin{pmatrix}" + r"\\".join(self._print(c) for c in components) + r"\end{pmatrix}"

    def _print_Magnitude(self, expr: Any, **kwargs: Any) -> str:
        return rf"\left| {self._print(expr.args[0])} \right|"

    def _print_Angle(self, expr: Any, **kwargs: Any) -> str:
        return rf"\angle \left( {self._print(expr.args[0])}, {self._print(expr.args[1])} \right)"


def custom_latex(expr: Any, **kwargs: Any) -> str:
    """LaTeX for an expression, using CustomLatexPrinter."""

    def remove_brackets_around_vector(match: re.Match[str]) -> str:
        if r"\begin{pmatrix}" in match.group(2):
            return match.group(0)
        return match.group(1)

    latex_str = CustomLatexPrinter(**kwargs).doprint(expr)
    return _VECTOR_IN_BRACKETS.sub(remove_brackets_around_vector, latex_str)
