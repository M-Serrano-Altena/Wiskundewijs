"""Which page of the site explains how to solve an equation like the one typed into the oplosser.

The solver already knows the structure of the equation (polynomial of degree 2, inequality,
system of equations, ...), so the topic is chosen with rules on that structure, most specific
first. When no rule fits, there's no link: there's no page about solving x = cos(x)
numerically or about matrices, and a link to something unrelated wouldn't help.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import regex as re
import sympy as sp

if TYPE_CHECKING:
    from src.Solver.src.solver.solve_calculations import Solve


@dataclass(frozen=True)
class Topic:
    title: str
    # path of the page on the site, with the anchor of the section
    url: str


STELSELS = Topic("Stelsels van vergelijkingen", "/stelsels_van_vergelijkingen/")
AFGELEIDE = Topic("De afgeleide: afgeleides bepalen", "/afgeleide/#afgeleides-bepalen")
EXTREME_WAARDES = Topic("De afgeleide: extreme waardes bepalen", "/afgeleide/#extreme-waardes-bepalen")
PRIMITIEVE = Topic("De primitieve functie", "/primitieve/#introductie-primitieven")
INTEGRAAL = Topic("Integralen", "/primitieve/#introductie-integralen")
LINEAIRE_ONGELIJKHEID = Topic("Lineaire ongelijkheden", "/ongelijkheden/#lineaire-ongelijkheden")
KWADRATISCHE_ONGELIJKHEID = Topic("Kwadratische ongelijkheden", "/ongelijkheden/#kwadratische-ongelijkheden")
GONIOMETRISCHE_VERGELIJKING = Topic("Goniometrische vergelijkingen", "/goniometrie/#goniometrische-vergelijkingen")
KWADRATISCH_X2_C = Topic("Kwadratische vergelijkingen van de vorm x² = c", "/kwadratische_vergelijkingen/#oplossen-vorm-x2-c")
KWADRATISCH_X2_BX = Topic("Kwadratische vergelijkingen van de vorm x² + bx = 0", "/kwadratische_vergelijkingen/#oplossen-vorm-x2-bx-0")
KWADRATISCH_X2_BX_C = Topic("Kwadratische vergelijkingen van de vorm x² + bx + c = 0", "/kwadratische_vergelijkingen/#oplossen-vorm-x2-bx-c-0")
SNIJPUNTEN_X_AS = Topic("Snijpunten van een parabool met de x-as", "/kwadratische_vergelijkingen/#snijpunten-met-de-x-as")
FORMULES_OMSCHRIJVEN = Topic("Formules omschrijven", "/basisvaardigheden/#formules-omschrijven")
LINEAIRE_VERGELIJKING = Topic("Vergelijkingen omschrijven", "/basisvaardigheden/#vergelijkingen-omschrijven")
LOGARITMES = Topic("Logaritmes", "/basisvaardigheden/#logaritmes")

ALL_TOPICS = [
    STELSELS, AFGELEIDE, EXTREME_WAARDES, PRIMITIEVE, INTEGRAAL, LINEAIRE_ONGELIJKHEID, KWADRATISCHE_ONGELIJKHEID,
    GONIOMETRISCHE_VERGELIJKING, KWADRATISCH_X2_C, KWADRATISCH_X2_BX, KWADRATISCH_X2_BX_C, SNIJPUNTEN_X_AS,
    FORMULES_OMSCHRIJVEN, LINEAIRE_VERGELIJKING, LOGARITMES,
]

_TRIG_FUNCTIONS = (sp.sin, sp.cos, sp.tan, sp.sec, sp.csc, sp.cot)
# exact forms that aren't taught at school, so the page wouldn't explain the answer
_UNREADABLE = (sp.CRootOf, sp.LambertW)


def find_topic(solver: Solve, has_error: bool = False) -> Topic | None:
    """The page that explains how to solve the solver's input by hand, if there is one."""
    if has_error or solver.is_vector or solver.numerical:
        return None

    if solver.is_system_of_eq:
        return _system_topic(solver)

    if not _has_variable_or_calculus(solver):
        # a calculation without a variable: only logarithms have their own section
        # (the calculation is already worked out, so look at the input)
        return LOGARITMES if re.search(r"\b(log|ln)\(", solver.equation_interpret) else None

    solution_set = solver.solution_set
    if isinstance(solution_set, sp.Basic) and solution_set.has(*_UNREADABLE):
        return None

    return _calculus_topic(solver) or _single_equation_topic(solver)


def _has_variable_or_calculus(solver: Solve) -> bool:
    return solver.symbol is not None or bool(_any(solver.derivative)) or bool(_any(solver.integral))


def _any(flags: Any) -> bool:
    return bool(getattr(flags, "any", lambda: flags)())


def _has_log(expr: Any) -> bool:
    return isinstance(expr, sp.Basic) and expr.has(sp.log)


def _system_topic(solver: Solve) -> Topic | None:
    equations = solver.system_equations
    if not equations:
        return None
    for equation in equations:
        expr = equation.lhs - equation.rhs
        symbols = list(expr.free_symbols)
        if not symbols or not expr.is_polynomial(*symbols) or _polynomial(expr, *symbols).total_degree() != 1:
            # only linear systems are explained on the site
            return None
    return STELSELS


def _calculus_topic(solver: Solve) -> Topic | None:
    if _any(solver.integral):
        # a definite integral is a number, an indefinite one (a primitive) a function
        integral_sides = [solver.eq1, solver.eq2] if _any(solver.integral[1:]) else [solver.eq1]
        if all(sp.sympify(side).is_number for side in integral_sides):
            return INTEGRAAL
        return PRIMITIEVE
    if _any(solver.derivative):
        # f'(x) = 0 is how extremes are found
        is_derivative_equation = len(solver.derivative) == 2 or "=" in solver.equation_interpret
        if is_derivative_equation and sp.sympify(solver.eq2) == 0:
            return EXTREME_WAARDES
        return AFGELEIDE
    return None


def _single_equation_topic(solver: Solve) -> Topic | None:
    symbol = solver.symbol
    expr = sp.sympify(solver.eq12)
    if symbol is None:
        return None

    if expr.has(*_TRIG_FUNCTIONS):
        return GONIOMETRISCHE_VERGELIJKING

    degree = _polynomial_degree(expr, symbol)
    if solver.multivariate:
        if degree == 2:
            return SNIJPUNTEN_X_AS
        if degree == 1 and not re.match(r"\s*y\s*=", solver.equation_interpret):
            # like 2y - 4x = 8: the y is made free
            return FORMULES_OMSCHRIJVEN
        return None

    if solver.equation_is_inequality and solver.equation_type != "!=":
        return {1: LINEAIRE_ONGELIJKHEID, 2: KWADRATISCHE_ONGELIJKHEID}.get(degree or 0)

    if degree == 1:
        return LINEAIRE_VERGELIJKING
    if degree == 2:
        return _quadratic_topic(expr, symbol)
    if _has_log(expr) or _has_exponential(expr, symbol):
        return LOGARITMES
    return None


def _polynomial(expr: Any, *symbols: Any) -> Any:
    # sympy's type hints for creating a Poly differ between versions, so it's called untyped
    make_polynomial: Any = sp.Poly
    return make_polynomial(sp.expand(expr), *symbols)


def _polynomial_degree(expr: Any, symbol: Any) -> int | None:
    if not expr.is_polynomial(symbol):
        return None
    degree = _polynomial(expr, symbol).degree()
    if degree == -sp.oo:
        # the degree of the polynomial 0
        return None
    return int(degree)


def _quadratic_topic(expr: Any, symbol: Any) -> Topic:
    """x² = c, x² + bx = 0 and x² + bx + c = 0 each have their own section."""
    _, b, c = _polynomial(expr, symbol).all_coeffs()
    if b == 0:
        return KWADRATISCH_X2_C
    if c == 0:
        return KWADRATISCH_X2_BX
    return KWADRATISCH_X2_BX_C


def _has_exponential(expr: Any, symbol: Any) -> bool:
    """Whether the variable is in an exponent, like 2^x = 8 (solved with logarithms)."""
    return any(power.exp.has(symbol) for power in expr.atoms(sp.Pow)) or expr.has(sp.exp)
