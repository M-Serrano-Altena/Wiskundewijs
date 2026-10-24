"""Solving an equation, inequality or expression typed into the oplosser.

`Solve(text, use_degrees).solve_equation()` returns the interpreted input, the output lines and
whether the result can be plotted. The steps for a single equation are:

1. parse the input into two sides (`process_equation`)
2. find the variable, simplify and make numeric versions of both sides (`_prepare_variable`)
3. show derivatives and integrals in the input (`_output_derivatives_and_integrals`)
4. find the domain, the solutions and the vertical asymptotes (`_find_solutions`)
5. write the solutions (`_output_solutions`), or explain why there are none

Systems of equations (with `;`) are handled in systems.py, and equations with vectors or
matrices in vector_equations.py. The plot is made from the solver's state in plotting.py.
"""

from __future__ import annotations

import traceback
from collections.abc import Callable, Sequence
from typing import Any
from warnings import filterwarnings

import numpy as np
import regex as re
import sympy as sp
import sympy.vector as sp_vector
from sympy.calculus.util import continuous_domain
from sympy.logic.boolalg import BooleanFalse, BooleanTrue
from sympy.physics.units import degree
from sympy.simplify.fu import TR2, TR111

from src.Solver.src.solver import linear_algebra
from src.Solver.src.solver.helper import (
    FloatArray,
    apply_operator,
    equation_type_to_latex,
    flip_inequality_sign,
    map_equation_type_to_sp,
    write_as_sin_and_cos,
)
from src.Solver.src.solver.linear_algebra import CustomMatrix, VectorShapeError
from src.Solver.src.solver.math_parser import (
    add_args_to_func,
    add_degree_symbol,
    apply_inner_func_to_func,
    get_uneval_sp_objs,
    math_interpreter,
    split_equation,
)
from src.Solver.src.solver.numeric import NumericFunction, find_roots, numpy_function, sympy_function
from src.Solver.src.solver.output import OutputLine, SolveOutput, append_to_last, text
from src.Solver.src.solver.safe_parsing import safe_sympify
from src.Solver.src.solver.sympy_custom_funcs import (
    DEG_ARC_GONIO_LOCALS,
    LOCALS,
    ArcGonioInvalidDomainError,
    ArcReciprocalInvalidDomainError,
    custom_latex,
    custom_simplify,
)

# re-exported for the oplosser view
__all__ = ["Solve", "custom_latex", "custom_simplify", "math_interpreter"]

filterwarnings("ignore", category=RuntimeWarning)

EQUATION_SYMBOLS = ["!=", ">=", "<=", "==", "=", ">", "<"]
GONIO_FUNCTIONS = {"sin", "cos", "tan", "sec", "csc", "cot"}
ARC_GONIO_FUNCTIONS = ["asin", "acos", "atan", "asec", "acsc", "acot"]
SYMPY_TRUTH_VALUES = (BooleanFalse, BooleanTrue)

# marks a variable that hasn't been given a value yet
_UNSET: Any = object()


class VectorFieldError(TypeError):
    """Raised when div or curl is applied to something that isn't a vector."""

    def __init__(self, message: str = "Operation requires a vector field, not a scalar function") -> None:
        super().__init__(message)


class ScalarFieldError(TypeError):
    """Raised when an operation for scalar fields is applied to a vector."""

    def __init__(self, message: str = "Operation requires a scalar field, not a vector function") -> None:
        super().__init__(message)


def _is_truth_value_or_list(value: Any) -> bool:
    return isinstance(value, (*SYMPY_TRUTH_VALUES, list))


class Solve:
    # These are set while solving. When solving stops early they are never set at all, and the
    # error handling in solve_equation relies on that.
    eq1: Any
    eq2: Any
    eq12: Any  # eq1 - eq2
    eq: Any  # the relation between eq1 and eq2, like sp.Eq(eq1, eq2)
    eq1_unsimplified: Any
    eq2_unsimplified: Any
    eq12_unsimplified: Any
    eq1_lambda: NumericFunction
    eq2_lambda: NumericFunction
    eq12_lambda: NumericFunction
    eq1_lambda_np: NumericFunction
    eq2_lambda_np: NumericFunction
    eq12_lambda_np: NumericFunction
    domain: Any
    domain_is_reals: bool
    solutions_complex: list[Any]
    solutions: list[Any]
    roots_numeric: FloatArray
    equation_type_opposite: str
    equation_type_opposite_sp: Callable[..., Any]
    x_intersect: FloatArray
    y_intersect: FloatArray
    x_range: FloatArray
    y_range: FloatArray
    x_range_og: FloatArray
    y_range_og: FloatArray
    x_coords: Any
    vert_asympt_set: Any
    og_sp_equations: list[Any]

    def __init__(self, input_string: str, use_degrees: bool | None) -> None:
        """input_string is the text typed by the user. use_degrees is None to decide automatically."""
        self.symbol: Any = None
        self.use_degrees = use_degrees
        self.use_degrees_reciprocal = True if use_degrees is None else use_degrees
        self.locals: dict[str, Any] = LOCALS.copy()
        self.equation_type = "="
        self.equation_is_inequality = False
        self.equation_type_sp: Callable[..., Any] = sp.Eq
        self.solution_set: Any = None
        self.solution_inequality: Any = None
        self.has_any_solutions = False
        self.interval_solutions: Any = None
        self.vert_asympt: FloatArray | None = None
        self.vert_asympt_eq: Any = None

        self.eq_string = math_interpreter(input_string)
        if any(degree_symbol in self.eq_string for degree_symbol in ["°", "∘"]):
            self.use_degrees = True
            self.eq_string = re.sub(r"\^?[°∘]", "", self.eq_string)
            self.eq_string = re.sub(r"\^?\(\)", "", self.eq_string)

        if self.use_degrees_reciprocal:
            self.locals.update(DEG_ARC_GONIO_LOCALS)

        self.output: list[OutputLine] = []
        self.equation_interpret = self.eq_string
        self.plot = False
        self.intersect = False
        self.numerical = False
        self.multivariate = False
        # numpy arrays with a bool per side of the equation, once the equation is parsed
        self.derivative: Any = False
        self.integral: Any = False
        self.real_root = False

        self.is_vector = False
        self.vect_dim = linear_algebra.vect_dim

        self.is_system_of_eq = ";" in self.eq_string

    def result(self) -> SolveOutput:
        return self.equation_interpret, self.output, self.plot

    # ---------------------------------------------------------------- numerical solving

    def numerical_roots(
        self, eq_sp: Any, eq_lambda_np: NumericFunction, a: float = -10000, b: float = 10000, solve_method: Any = "newton",
        default_func: bool = True,
    ) -> FloatArray:
        """Roots of eq_sp between a and b. default_func is True when eq_sp is the equation being solved."""
        roots, searched = find_roots(eq_sp, eq_lambda_np, self.symbol, a, b, solve_method=solve_method, vert_asympt=self.vert_asympt)
        if default_func:
            self.intersect = self.numerical = searched
        return roots

    def solve_numerically(self, eq_sp: Any = None, eq_lambda_np: NumericFunction | None = None) -> Any:
        """Solve eq_sp = 0 numerically (by default the equation being solved), as a FiniteSet."""
        if eq_sp is None or eq_lambda_np is None:
            default_func = True
            eq_sp = self.eq12 if not self.multivariate else self.eq2
            eq_lambda_np = self.eq12_lambda_np if not self.multivariate else self.eq2_lambda_np
            self.numerical = True
        else:
            default_func = False

        for method in ["newton", "fsolve", "bisect"]:
            self.roots_numeric = self.numerical_roots(eq_sp, eq_lambda_np, -10000, 10000, solve_method=method, default_func=default_func)
            if self.roots_numeric.size != 0:
                break

        solutions = sp.FiniteSet(*self.roots_numeric)
        self.intersect = not solutions.is_empty

        if self.equation_is_inequality and not _is_truth_value_or_list(self.solution_inequality) and self.intersect:
            self._set_numerical_inequality_solution()

        return solutions

    def _set_numerical_inequality_solution(self) -> None:
        """Turn the numerical roots of an inequality into intervals, like x < 1 ∨ x > 3."""
        abs_sorted_roots = self.roots_numeric[np.argsort(np.abs(self.roots_numeric))]
        boundaries = list(np.append(abs_sorted_roots[abs_sorted_roots >= 0], abs_sorted_roots[abs_sorted_roots < 0]))

        test_dx = 0.1 if self.equation_type in ">=" else -0.1
        self.equation_type_opposite = flip_inequality_sign(self.equation_type)
        self.equation_type_opposite_sp = map_equation_type_to_sp(self.equation_type_opposite)

        def relation_at(boundary: Any) -> Any:
            # which side of the boundary satisfies the inequality
            if apply_operator(self.eq12_lambda_np(float(boundary) + test_dx), self.equation_type, 0):
                return self.equation_type_sp(self.symbol, boundary)
            return self.equation_type_opposite_sp(self.symbol, boundary)

        if len(boundaries) == 1:
            solution = sp.nsimplify(boundaries[0], [sp.pi, sp.E], rational=False)
            if apply_operator(self.eq12_lambda_np(solution + test_dx), self.equation_type, 0):
                self.solution_inequality = self.equation_type_sp(self.symbol, solution)
            else:
                self.solution_inequality = self.equation_type_opposite_sp(self.symbol, solution)
            return

        if len(boundaries) > 1:
            boundaries = [sp.nsimplify(solution, [sp.pi, sp.E], rational=False) for solution in boundaries[:4]]
            boundaries = [_round_boundary(sol) if sp.N(sol) == sol else sol for sol in boundaries]
            relations = [relation_at(boundary) for boundary in boundaries]

            combined_expr = relations[0]
            for relation in relations[1:]:
                combined_expr = _combine_inequalities(combined_expr, relation, relations[0], len(relations))
            self.solution_inequality = combined_expr

    def check_solve_numerically(self, solution_set: Any) -> Any:
        """Solve numerically if sympy couldn't solve the equation itself, otherwise None."""
        if isinstance(solution_set, sp.ConditionSet) and solution_set.condition.simplify() == sp.Eq(self.eq12, 0).simplify():
            return self.solve_numerically()
        return None

    # ---------------------------------------------------------------- parsing the equation

    def process_equation(self, eq_string: str) -> Sequence[str] | None:
        """Parse the input into the two sides of the equation. None if there's nothing to solve."""
        eq_split = [string for string in split_equation(eq_string) if string not in EQUATION_SYMBOLS]

        for equation_type in EQUATION_SYMBOLS:
            if equation_type in eq_string:
                self.equation_type = equation_type
                self.equation_type_sp = map_equation_type_to_sp(equation_type)
                break

        return self.set_eqs(eq_split)

    def parse_sides(self, eq_split: list[str]) -> tuple[Any, Any, Any, Any] | None:
        """(eq1, eq2, eq1 - eq2, relation) for the sides of an equation.

        eq_split is updated in place if a side had to be rewritten to be parsed.
        """
        eq_split[0], eq1 = self.sympify_equation(eq_split[0])

        eq2: Any
        if len(eq_split) == 1:
            eq2 = 0
        elif len(eq_split) == 2:
            eq_split[1], eq2 = self.sympify_equation(eq_split[1])
        else:
            return None

        eq1 = self.gonio_degree_check(eq1, eq_split[0], use_degree=self.use_degrees)
        if len(eq_split) == 2:
            eq2 = self.gonio_degree_check(eq2, eq_split[1], use_degree=self.use_degrees)
            if any(isinstance(eq, (CustomMatrix, sp.MatrixBase, sp.MatrixExpr)) for eq in [eq1, eq2]):
                eq12 = None  # not used for matrices
            else:
                eq12 = eq1 - eq2
        else:
            eq12 = eq1

        vector_classes = (sp_vector.Vector, sp.MatrixBase, sp.MatrixExpr)
        if isinstance(eq1, vector_classes) or isinstance(eq2, vector_classes) or any("grad" in part for part in eq_split):
            self.is_vector = True
            self.vect_dim = linear_algebra.vect_dim

        eq = self.get_self_eq(eq1, eq2)

        if any(sub_str in self.eq_string for sub_str in ["vect", "laplacian", "matrix"]):
            self.is_vector = True
            self.vect_dim = linear_algebra.vect_dim

        return eq1, eq2, eq12, eq

    def set_eqs(self, eq_split: list[str]) -> list[str] | None:
        """Parse the sides of the equation and store them. None if there's nothing more to solve."""
        sides = self.parse_sides(eq_split)
        if sides is None:
            self.output.append(text("Error: Meer dan 1 relatieteken (=, ≥, ≤, etc.)"))
            return None

        eq1, eq2, eq12, eq = sides
        self.eq1_unsimplified, self.eq2_unsimplified, self.eq12_unsimplified = self.eq1, self.eq2, self.eq12 = eq1, eq2, eq12
        self.eq = eq

        if self.equation_type == "==":
            self.output.append(f"\\text{{{self.eq}}}")
            return None

        if len(eq_split) == 2:
            self.eq_string = str(self.eq)

        return eq_split

    def sympify_equation(self, eq_str: str) -> tuple[str, Any]:
        """Parse one side of the equation. Returns the (possibly rewritten) text and the expression."""
        if any(sub_str in eq_str for sub_str in ["div", "curl"]) and not any(sub_str in eq_str for sub_str in ["vect", "grad"]):
            raise VectorFieldError("Argument must be a vector (use 'vect' function)")

        try:
            return eq_str, TR111(safe_sympify(eq_str, self.locals)).doit()
        except ValueError:
            # integrate() without an integration variable
            eq_str = add_args_to_func(eq_str, func_name="integrate", replace_with="x").replace(".integrate()", ".integrate(x)")
            return eq_str, TR111(safe_sympify(eq_str, self.locals)).doit()

    def gonio_degree_condition(self, inner_arg: str) -> bool:
        """Whether the argument of a trigonometric function looks like degrees (a rational number)."""
        try:
            if not isinstance(safe_sympify(inner_arg), sp.Expr):
                return False
        except Exception:
            return False

        return bool(sp.nsimplify(safe_sympify(inner_arg, self.locals).subs(degree, 1)).is_Rational)

    def convert_gonio_to_degree(self, eq_str: str, gonio_set: set[str], use_degree_condition: bool = True) -> str:
        for gonio_func in gonio_set:
            if gonio_func in eq_str:
                if use_degree_condition:
                    eq_str = apply_inner_func_to_func(eq_str, func_name=gonio_func, inner_func_name="rad", inner_arg_condition_func=self.gonio_degree_condition)
                else:
                    eq_str = apply_inner_func_to_func(eq_str, func_name=gonio_func, inner_func_name="rad")

        return eq_str

    def gonio_degree_check(self, eq: Any, eq_str: str, use_degree: bool | None = None) -> Any:
        """Interpret the arguments of trigonometric functions as degrees, if wanted.

        With use_degree=None, only arguments that look like degrees (sin(30)) are converted.
        """
        relevant_gonio_set = {func for func in GONIO_FUNCTIONS if re.findall(rf"(?<!a){func}\b", eq_str)}
        if use_degree is False or not relevant_gonio_set:
            return eq

        use_degree_condition = not bool(use_degree)
        eq_str_new = self.convert_gonio_to_degree(eq_str, relevant_gonio_set, use_degree_condition=use_degree_condition)
        if eq_str_new != eq_str:
            self.equation_interpret = add_degree_symbol(self.equation_interpret, gonio_set=relevant_gonio_set)
            if any(arc_gonio in eq_str_new for arc_gonio in ARC_GONIO_FUNCTIONS):
                self.equation_interpret = self.equation_interpret.replace("°", "")
                self.eq_string = self.equation_interpret
            else:
                self.eq_string = self.equation_interpret.replace("°", r"^(circ)")

        return safe_sympify(eq_str_new, self.locals).subs(degree, 1)

    def get_self_eq(self, eq1: Any, eq2: Any) -> Any:
        try:
            return sp.nsimplify(self.equation_type_sp(eq1, eq2), tolerance=1e-7)
        except AttributeError:
            return self.equation_type_sp(eq1, eq2)

    # ---------------------------------------------------------------- solving

    def solve_equation(self) -> SolveOutput:
        """Solve the equation and describe the result. Returns (interpreted input, output lines, plot)."""
        try:
            result = self._solve()
            if result is not None:
                return result

        except VectorFieldError:
            vector_operator = "div" if "div" in self.eq_string else "curl"
            self.output.append(text(f"Error: Argument van `{vector_operator}` moet een vector zijn"))
            return self.result()
        except ArcReciprocalInvalidDomainError:
            self.output.append(text("Error: Argument van de arc functie mag niet tussen -1 en 1 zijn"))
            return self.result()
        except ArcGonioInvalidDomainError:
            self.output.append(text("Error: Argument van de arc functie moet een getal tussen -1 en 1 zijn"))
            return self.result()
        except VectorShapeError:
            self.output.append(text("Error: De matrix kan niet omgezet worden naar een vector"))
            return self.result()
        except sp.ShapeError:
            self.output.append(text("Error: De dimensies van de matrices komen niet overeen"))
            return self.result()

        except (NotImplementedError, TypeError):
            # sympy can't handle the equation: try to solve it numerically
            result = self._solve_numerically_after_error()
            if result is not None:
                return result

        except sp.SympifyError:
            self.output.append(text("Error: De ingevoerde functie klopt niet"))
            traceback.print_exc()
            return self.result()

        except Exception:
            self.output.append(text("ERROR"))
            traceback.print_exc()
            return self.result()

        try:
            return self._output_solutions()
        except Exception:
            self.output.append(text("ERROR"))
            traceback.print_exc()
            return self.result()

    def _solve(self) -> SolveOutput | None:
        """Solve the equation. Returns the result if it's complete, or None to write the solutions."""
        if self.is_system_of_eq:
            from src.Solver.src.solver.systems import solve_system_of_eq
            return solve_system_of_eq(self)

        eq_split = self.process_equation(self.eq_string)
        if eq_split is None:
            return self.result()

        if self.is_vector:
            from src.Solver.src.solver.vector_equations import solve_vector
            return solve_vector(self, eq_split=eq_split)

        free_symbols = [symbol for symbol in self.eq12.free_symbols if symbol.name != "circ"]
        if free_symbols:
            eq_split = self._check_multivariate(free_symbols) or eq_split
            if len(free_symbols) >= 2:
                self.output.append(text("Error: Meer dan 1 variabele"))
                return self.result()
            self._prepare_variable(free_symbols, eq_split)

        self._output_derivatives_and_integrals(eq_split)
        self._find_solutions()

        check_numerical = self.check_solve_numerically(self.solution_set)
        if check_numerical is not None and not self.intersect:
            return self._no_solutions_output()
        if check_numerical is not None:
            self.solution_set = check_numerical
            self.has_any_solutions = not self.solution_set.is_empty
        elif self.symbol:
            self._find_symbolic_solutions()

        if not self.has_any_solutions and not self.numerical:
            self._output_without_solutions(eq_split)
            return self.result()

        if self.solution_set.is_empty:
            return self._no_solutions_output()

        return None

    def _solve_numerically_after_error(self) -> SolveOutput | None:
        try:
            self.eq12
        except Exception:
            # the error happened before the equation was parsed
            self.output.append(text("ERROR"))
            traceback.print_exc()
            return self.result()

        try:
            check_numerical = self.check_solve_numerically(self.solution_set)
            if check_numerical is not None and not self.intersect:
                return self._no_solutions_output()
            if check_numerical is not None:
                self.interval_solutions = self.solution_set = check_numerical
        except Exception:
            self.output.append(text("ERROR"))
            traceback.print_exc()
            return self.result()

        return None

    def _check_multivariate(self, free_symbols: list[Any]) -> tuple[str, str] | None:
        """For an equation in x and y, solve it for y so it can be treated as y = f(x).

        Removes y from free_symbols and returns the new sides of the equation.
        """
        if len(free_symbols) != 2:
            return None

        y_symbol = sp.Symbol("y")
        if y_symbol not in free_symbols:
            return None

        self.multivariate = True
        self.eq1, self.eq2 = y_symbol, _real_solution_for(self.eq12, y_symbol)
        self.eq12 = -self.eq2
        self.eq = self.get_self_eq(0, self.eq2)
        free_symbols.remove(y_symbol)
        return str(y_symbol), str(self.eq2)

    def _prepare_variable(self, free_symbols: list[Any], eq_split: Sequence[str]) -> None:
        """Make the variable real, simplify both sides and create their numeric versions."""
        self.symbol = free_symbols.pop()
        real_symbol = sp.Symbol(str(self.symbol), real=True)
        self.eq = self.eq.subs(self.symbol, real_symbol)
        self.eq1 = sp.sympify(self.eq1).subs(self.symbol, real_symbol)
        self.eq2 = sp.sympify(self.eq2).subs(self.symbol, real_symbol)
        self.eq12 = self.eq1 - self.eq2 if not self.multivariate else self.eq2
        self.symbol = real_symbol

        eqs = [self.eq1, self.eq2, self.eq12]
        self.eq1_unsimplified, self.eq2_unsimplified, self.eq12_unsimplified = eqs
        self.eq1, self.eq2, self.eq12 = eqs = [custom_simplify(eq) for eq in eqs]

        self.eq1_lambda, self.eq2_lambda, self.eq12_lambda = (sympy_function(eq, self.symbol) for eq in eqs)
        self.eq1_lambda_np, self.eq2_lambda_np, self.eq12_lambda_np = (numpy_function(eq, self.symbol) for eq in eqs)
        if self.multivariate:
            self.eq1_lambda = self.eq1_lambda_np = lambda _: 0

        if len(eq_split) == 1 and not sp.sympify(self.eq1).is_number:
            self.equation_interpret = f"{self.eq_string} = 0"

    def _find_solutions(self) -> None:
        """Find the domain, the solution set and the vertical asymptotes."""
        if self.symbol:
            try:
                self.domain = continuous_domain(self.eq12, self.symbol, domain=sp.S.Reals)
            except NotImplementedError:
                self.domain = sp.S.Reals
            self.domain_is_reals = bool(self.domain is sp.S.Reals)

        self.equation_is_inequality = self.equation_type != "=" and not self.multivariate

        if not isinstance(self.eq12, sp.AccumBounds) and self.symbol is not None:
            self.solution_set = sp.solveset(self.eq12, domain=sp.S.Reals)
        else:
            self.solution_set = sp.EmptySet

        if self.equation_is_inequality:
            self.solution_inequality = sp.solve(self.eq)

        if self.symbol:
            self._find_vertical_asymptotes()

    def _find_vertical_asymptotes(self) -> None:
        """Set vert_asympt_eq: an expression that is 0 at the asymptotes, or a list of their x-values."""
        self.vert_asympt_eq = write_as_sin_and_cos(self.eq12).as_numer_denom()[1]
        if self.vert_asympt_eq.is_number:
            self.vert_asympt_eq = None
            return

        if self.domain_is_reals or not (self.domain.is_Interval or self.domain.is_Union):
            return

        # the domain's finite boundaries where the function isn't finite are asymptotes
        sub_domains = self.domain.args if self.domain.is_Union else [self.domain]
        is_finite_at: list[Any] = []
        boundaries: list[Any] = []
        for sub_domain in sub_domains:
            for j in range(2):
                boundary = sub_domain.args[j]
                if boundary.is_finite:
                    is_finite_at.append(self.eq12_lambda(boundary).is_finite)
                    boundaries.append(boundary)

        if False in is_finite_at:
            self.vert_asympt_eq = list({boundary for boundary, finite in zip(boundaries, is_finite_at) if not finite}) or None

    def _find_symbolic_solutions(self) -> None:
        try:
            complex_symbol = sp.Symbol("x")
            self.solutions_complex = sp.solve(TR2(sp.Eq(self.eq1_lambda(complex_symbol), self.eq2_lambda(complex_symbol))))
            self.solutions = [sol for sol in self.solutions_complex if sol.is_real and sp.N(self.eq1_lambda(sol)).is_real]
        except Exception:
            self.solutions_complex = []
            try:
                self.solutions = sp.solve(TR2(self.eq12))
            except Exception:
                self.solutions = []

        self.has_any_solutions = bool(
            self.solutions_complex or self.solutions or (self.solution_set.is_FiniteSet and not self.solution_set.is_empty)
        )

    # ---------------------------------------------------------------- derivatives and integrals

    def _output_derivatives_and_integrals(self, eq_split: Sequence[str]) -> None:
        self.derivative = np.array(["diff" in string for string in eq_split])
        self.integral = np.array(["integrate" in string for string in eq_split])
        if self.derivative.any():
            self._set_derivative_integral_output(eq_split, is_integral=False)
        if self.integral.any():
            self._set_derivative_integral_output(eq_split, is_integral=True)
        if self.derivative.any() or self.integral.any():
            self.output.append(text(""))

    def _get_uneval_derivative_integral(self, eq_split: Sequence[str], eq_split_index: int = 0, is_integral: bool = False) -> tuple[str, Any, Any]:
        """(name like f'(x), the unevaluated derivative or integral, its result) for one side."""
        symbol = self.symbol or sp.Symbol("x", real=True)
        eq = self.eq1 if eq_split_index == 0 else self.eq2

        # the integral of a number is written as I (or II), not as F(x)
        names = [[f"f'({symbol})", f"g'({symbol})"], [f"F({symbol})", f"G({symbol})"], ["I", "II"]]
        row = int(is_integral) + (1 if is_integral and eq.is_number else 0)
        str_func = names[row][eq_split_index]

        derivative_integral = get_uneval_sp_objs(eq_split[eq_split_index])
        if derivative_integral == eq:
            derivative_integral = get_uneval_sp_objs(add_args_to_func(eq_split[eq_split_index], func_name="diff", replace_with=str(symbol)))

        if len(derivative_integral.free_symbols) >= 1:
            derivative_integral = derivative_integral.subs(derivative_integral.free_symbols.pop(), symbol)

        return str_func, derivative_integral, eq

    def _set_combined_derivative_integral_text(self, eq_split: Sequence[str], is_derivative_integral: Any, specific_text: str) -> None:
        if not (self.derivative.any() and self.integral.any()):
            if len(eq_split) == 2 and is_derivative_integral.all():
                self.output.append(text(f"De {specific_text}n van de functies zijn:"))
            else:
                self.output.append(text(f"De {specific_text} van de functie is:"))
            return

        both_text = text("De primitieve en afgeleide van de functies zijn:")
        single_text = text("De primitieve en afgeleide van de functie is:")
        if self.integral[0] and self.derivative.any():
            if len(eq_split) == 2 and self.derivative[1]:
                self.output[0] = both_text
            elif self.derivative[0]:
                self.output[0] = single_text

        if len(eq_split) == 2 and self.integral[1] and self.derivative.any():
            if self.integral[0] or self.derivative[0]:
                self.output[0] = both_text
            elif self.derivative[1]:
                self.output[0] = single_text

    def _set_derivative_integral_output(self, eq_split: Sequence[str], is_integral: bool = False) -> None:
        is_derivative_integral = self.integral if is_integral else self.derivative
        if is_integral:
            self._set_combined_derivative_integral_text(eq_split, is_derivative_integral, "primitieve")

        for index in range(len(eq_split)):
            if not is_derivative_integral[index]:
                continue

            str_func, derivative_integral, eq = self._get_uneval_derivative_integral(eq_split, eq_split_index=index, is_integral=is_integral)
            line = f"{str_func} = {custom_latex(derivative_integral)} = {custom_latex(eq)}"
            if "F" in str_func or "G" in str_func:
                line += " + C"
            self.output.append(line)

    # ---------------------------------------------------------------- output without solutions

    def _no_solutions_output(self) -> SolveOutput:
        self.plot = True
        self.output.append(text("Vereenvoudigde Vergelijking:"))
        self.output.append(f"{custom_latex(self.eq1)} {equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2)}")

        if self.equation_is_inequality:
            self._no_solutions_inequality_output()
            return self.result()

        if self.multivariate:
            self.output.append(text("Geen snijpunt met de x-as gevonden"))
        else:
            self.output.append(text("Geen oplossing gevonden"))
        return self.result()

    def _no_solutions_inequality_output(self) -> None:
        """An inequality without boundaries is true for all x or for none: check one value."""
        if not self.equation_is_inequality:
            return

        extrema_func: Any = _UNSET
        try:
            extrema_func = [self.eq12_lambda_np(float(sol)) for sol in sp.solve(sp.diff(self.eq12))]
            extrema_func = min(extrema_func) if ">" in self.equation_type else max(extrema_func)
        except Exception:
            for num in sorted(range(-100, 100), key=abs):
                try:
                    extrema_func = self.eq12_lambda_np(num)
                except Exception:
                    pass

        if extrema_func is _UNSET:
            raise RuntimeError("The inequality couldn't be evaluated for any value")

        if apply_operator(extrema_func, self.equation_type, 0):
            self.output.append(text("Deze vergelijking is waar voor alle x"))
        else:
            self.output.append(text("Deze vergelijking klopt voor geen enkele x"))

    def _no_solution_text(self) -> None:
        if self.multivariate:
            self.output.append(text("Geen snijpunt met de x-as gevonden"))
        elif self.has_any_solutions:
            self.output.append(text("Geen reële oplossing gevonden"))
        else:
            self.output.append(text("Geen oplossing gevonden"))

    def _output_without_solutions(self, eq_split: Sequence[str]) -> None:
        """Output for input without solutions: a calculation, or an equation that's true or false."""
        eq_string = add_args_to_func(self.eq_string, func_name="root", replace_with="evaluate=False", amt_commas=2)
        try:
            expr_display = safe_sympify(eq_string, evaluate=False)
        except AttributeError:
            expr_display = safe_sympify(eq_string)

        if len(eq_split) == 1:
            if not self.symbol:
                self._output_calculation(eq_split, expr_display)
            elif sp.nsimplify(self.eq1, [sp.pi]).is_number:
                solution = custom_simplify(self.eq1)
                if solution != sp.N(solution):
                    self.output.append(f"{custom_latex(expr_display)} = {custom_latex(solution)} \\approx {custom_latex(sp.N(solution, 5))}")
                else:
                    self.output.append(f"{custom_latex(expr_display)} = {custom_latex(solution)}")
            else:
                self.output.append(text("Vereenvoudigde Vergelijking:"))
                self.output.append(f"{custom_latex(custom_simplify(self.eq1))} = 0")
                self._no_solution_text()
                self.plot = True

        elif len(eq_split) == 2:
            self._output_comparison()

    def _output_calculation(self, eq_split: Sequence[str], expr_display: Any) -> None:
        """Output for a calculation without variables, like 2 + 3 or sqrt(8)."""
        solution: Any = sp.nsimplify(self.eq1, [sp.pi])
        equals_sign = "="
        complex_num = False
        if solution.is_number:
            equals_sign = "=" if solution.equals(sp.N(solution)) or self.eq1.equals(sp.N(solution)) else "\\approx"
            solution = sp.N(solution)
            try:
                if solution.is_finite and int(solution) == float(solution) and len(str(round(solution))) < 10:
                    solution = int(solution)
            except TypeError:
                # complex numbers can't be converted to int
                complex_num = True
                real_part, imag_part = solution.as_real_imag()
                if sp.Integer(real_part) == real_part and sp.Integer(imag_part) == imag_part:
                    solution = sp.Add(sp.Integer(real_part), sp.Mul(sp.Integer(imag_part), sp.I))

                exact_real, exact_imag = sp.nsimplify(self.eq1, [sp.pi]).as_real_imag()
                if real_part == exact_real and imag_part == exact_imag:
                    equals_sign = "="
            except ValueError:
                equals_sign = "="

        try:
            str(self.eq1)
        except ValueError:
            equals_sign = "="

        if self.eq1 != expr_display and equals_sign != "=" and "circ" not in str(expr_display):
            if not complex_num and sp.N(solution, 9).equals(sp.N(solution, 10)):
                equals_sign = "="
            self.output.append(f"{custom_latex(expr_display)} = {custom_latex(self.eq1)} {equals_sign} {custom_latex(solution, symbol=self.symbol)}")

        elif expr_display == solution:
            if eq_split[0] == str(solution):
                self.output.append(f"\\textrm{{Yep dat is }} {custom_latex(solution, symbol=self.symbol)}")
                return

            has_dot_function = any(dot_func in eq_split[0] for dot_func in [".subs", ".diff", ".integrate", "limit"])
            if self.derivative.any() or self.integral.any():
                self.output.pop()
            elif has_dot_function:
                expr_display = get_uneval_sp_objs(eq_split[0])
                self.output.append(f"{custom_latex(expr_display)} {equals_sign} {custom_latex(solution, symbol=self.symbol)}")
            else:
                self.output.append(f"\\textrm{{{eq_split[0]}}} {equals_sign} {custom_latex(solution, symbol=self.symbol)}")

        else:
            if equals_sign == "=" and not sp.N(solution, 9).equals(sp.N(solution, 10)):
                equals_sign = "\\approx"
            self.output.append(f"{custom_latex(expr_display)} {equals_sign} {custom_latex(solution, symbol=self.symbol)}")

    def _output_comparison(self) -> None:
        """Output for an equation that is simply true or false, like 2 = 3."""
        lhs = sp.nsimplify(self.eq1, [sp.pi, sp.E], rational=False)
        rhs = sp.nsimplify(self.eq2, [sp.pi, sp.E], rational=False)

        has_equal_sides = apply_operator(lhs, self.equation_type, rhs)
        sides_are_numbers = lhs.is_number and rhs.is_number
        has_solution = has_equal_sides or sides_are_numbers
        relation = equation_type_to_latex(self.equation_type)

        if has_solution:
            self.output.append(text("Vergelijking:"))

        simplify = self.eq1_unsimplified != lhs or self.eq2_unsimplified != rhs
        if simplify:
            self.output.append(f"{custom_latex(self.eq1_unsimplified)} {relation} {custom_latex(self.eq2_unsimplified)}")
            self.output.append(text("Versimpelingen:"))
            if self.eq1_unsimplified != lhs:
                self.output.append(f"\\bullet \\quad {custom_latex(self.eq1_unsimplified)} \\Longrightarrow {custom_latex(lhs)}")
            if self.eq2_unsimplified != rhs:
                self.output.append(f"\\bullet \\quad {custom_latex(self.eq2_unsimplified)} \\Longrightarrow {custom_latex(rhs)}")

        if not has_solution:
            self.output.append(text("Vereenvoudigde Vergelijking:"))
            self.output.append(f"{custom_latex(self.eq1)} {relation} {custom_latex(self.eq2)}")
            self._no_solution_text()
            self.plot = True
            return

        if simplify:
            self.output.append(text("Onze vergelijking wordt dus:"))
        self.output.append(f"{custom_latex(lhs)} {relation} {custom_latex(rhs)}")

        if has_equal_sides:
            self.output.append(text("Dit is waar, dus deze vergelijking klopt"))
        elif sides_are_numbers:
            self.output.append(text("Dit is niet waar, dus deze vergelijking klopt niet"))

    # ---------------------------------------------------------------- output with solutions

    def _solution_header(self, plural: bool) -> tuple[str, Any]:
        if self.multivariate:
            return text("De snijpunten met de $x$-as zijn:" if plural else "Het snijpunt met de $x$-as is:")
        return text("De oplossingen zijn:" if plural else "De oplossing is:")

    def _output_solutions(self) -> SolveOutput:
        self.plot = True
        self.intersect = True
        self.output.append(text("Vereenvoudigde Vergelijking:"))
        self.output.append(f"{custom_latex(self.eq1)} {equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2)}")

        if self.solution_set.is_FiniteSet:
            self._output_finite_solutions()
        else:
            self._output_infinite_solutions()

        return self.result()

    def _output_domain(self) -> None:
        if not self.domain_is_reals:
            self.output.append(text(f"Het domein van ${self.symbol}$ is:", new_line=2))
            self.output.append(custom_latex(self.domain))

    def _output_finite_solutions(self) -> None:
        self._set_numerical_text()

        if len(self.solution_set) == 1:
            if self.equation_is_inequality:
                self._set_inequality_solution_output()
            else:
                self.output.append(self._solution_header(plural=False))
                self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solution_set.args[0])}")

            if not self.solution_set.args[0].equals(sp.N(self.solution_set.args[0])):
                append_to_last(self.output, f" \\approx {sp.N(self.solution_set.args[0], 5)}")

        else:
            if len(self.solution_set) > 5:
                solution_array = np.array(list(self.solution_set))
                self.interval_solutions = solution_array[np.argsort(np.abs(solution_array))][:5]
            else:
                self.interval_solutions = self.solution_set

            if self.equation_is_inequality:
                self._set_inequality_solution_output()
            else:
                self.output.append(self._solution_header(plural=True))
                if len(self.solution_set) > 5:
                    first_five = "De eerste 5 snijpunten met de $x$-as zijn:" if self.multivariate else "De eerste 5 oplossingen zijn:"
                    self.output[-1] = text(first_five)
                self._set_count_solutions()

        self._output_domain()

    def _output_infinite_solutions(self) -> None:
        """Output for infinitely many solutions (periodic) or solutions sympy can't list."""
        if self.equation_is_inequality:
            self._set_inequality_solution_output()
        else:
            self.output.append(self._solution_header(plural=True))
            self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solution_set, symbol=self.symbol)}")

        self._output_domain()

        if not self.equation_is_inequality:
            in_domain = "Snijpunten in het domein $[0, 2\\pi]$:" if self.multivariate else "Oplossingen in het domein $[0, 2\\pi]$:"
            self.output.append(text(in_domain, new_line=2))

        self.interval_solutions = []
        if self.solution_set.is_iterable:
            self.interval_solutions = _solutions_between_0_and_2pi(self.solution_set)
        else:
            self.solution_set = self.solve_numerically()
            self.interval_solutions = list(self.solution_set)

            if self.numerical and len(self.roots_numeric) > 5:
                self.interval_solutions = self.interval_solutions[:5]

            if not self.equation_is_inequality:
                self.output = self.output[:-2]
                if len(self.roots_numeric) == 1:
                    self.output[-1] = self._solution_header(plural=False)
                self._set_numerical_text()

        self.interval_solutions = sp.FiniteSet(*self.interval_solutions)

        if self.equation_is_inequality:
            return

        if self.interval_solutions.is_empty:
            self.intersect = False
            self.output = self.output[:-6]
            if self.multivariate:
                self.output.append(text("Geen snijpunten met de $x$-as gevonden"))
            else:
                self.output.append(text("Geen oplossing gevonden", new_line=2))
            return

        self._set_count_solutions()

    def _set_inequality_solution_output(self) -> None:
        if not _is_truth_value_or_list(self.solution_inequality):
            self.output.append(text("De oplossing is:"))
            self.output.append(custom_latex(self.solution_inequality))
            return

        self._no_solutions_inequality_output()

    def _set_numerical_text(self) -> None:
        if self.numerical:
            if len(self.roots_numeric) == 1:
                self.output.append(text("(Oplossing is numeriek bepaald)", new_line=2))
            else:
                self.output.append(text("(Oplossingen zijn numeriek bepaald)", new_line=2))

    def _set_count_solutions(self) -> None:
        """Write the solutions in interval_solutions, numbered if there are several."""
        interval_solutions = [sp.nsimplify(solution, [sp.pi, sp.E], rational=False) for solution in self.interval_solutions]
        numbered = len(self.interval_solutions) != 1
        if not numbered:
            interval_solutions = interval_solutions[:1]

        for counter, solution in enumerate(interval_solutions, start=1):
            prefix = f"{counter}) \\quad " if numbered else ""
            display = _solution_display(solution)
            self.output.append(f"{prefix}{custom_latex(self.symbol)} {_equals_sign(solution)} {custom_latex(display, symbol=self.symbol)}")
            if not _is_numerical(solution):
                append_to_last(self.output, f" \\approx {sp.N(solution, 5)}")


def _real_solution_for(eq12: Any, y_symbol: Any) -> Any:
    """The first real solution of eq12 = 0 for y, skipping solutions that only differ in sign."""
    real_solutions = [sol for sol in sp.solve(eq12, y_symbol) if "I" not in str(sol)]
    abs_solutions: list[Any] = []
    new_solutions: list[Any] = []
    for sol in reversed(real_solutions):
        if sp.Abs(sol) not in abs_solutions:
            new_solutions.append(sol)
            abs_solutions.append(sp.Abs(sol))
    return new_solutions[0]


def _round_boundary(solution: Any) -> Any:
    rounded = round(solution, 3)
    return int(rounded) if int(rounded) == rounded else rounded


def _combine_inequalities(expr1: Any, expr2: Any, first: Any, amount: int) -> Any:
    """Combine the relations at two boundaries into one solution, with ∨ or ∧."""
    if isinstance(sp.simplify(expr1 & expr2), SYMPY_TRUTH_VALUES) and amount < 4:
        return expr1 | expr2
    if isinstance(sp.simplify(expr1 | expr2), SYMPY_TRUTH_VALUES):
        return expr1 & expr2
    if expr1 == first and amount >= 4:
        return expr2
    return expr1


def _solutions_between_0_and_2pi(solution_set: Any) -> list[Any]:
    """The real solutions in [0, 2π], giving up after 10 solutions outside it."""
    solutions: list[Any] = []
    outside_count = 0
    for solution in solution_set:
        if not solution.is_real:
            continue
        if 0 <= sp.N(solution) <= 2 * np.pi:
            solutions.append(solution)
            continue
        outside_count += 1
        if outside_count > 10:
            break
    return solutions


def _is_numerical(solution: Any) -> bool:
    return bool(solution.equals(sp.N(solution)))


def _equals_sign(solution: Any) -> str:
    if not _is_numerical(solution) or sp.N(solution, 9).equals(sp.N(solution, 10)):
        return "="
    return "\\approx"


def _solution_display(solution: Any) -> Any:
    """A numerical solution rounded to 7 digits, or as an integer if it is one."""
    if not _is_numerical(solution):
        return solution

    display = sp.N(solution, 7)
    try:
        if int(display) == float(display):
            return int(solution)
    except Exception:
        pass
    return display
