"""Solving systems of equations, typed as equations separated by `;` (like `x + y = 10; x - y = 2`).

SymPy solves most systems exactly. If it can't, the system is solved numerically: equations are
rewritten into equations in a single variable by substitution, those are solved one by one, and
the solutions found are checked against the original equations.
"""

from __future__ import annotations

import itertools
from copy import deepcopy
from typing import TYPE_CHECKING, Any

import sympy as sp

from src.Solver.src.solver.helper import (
    equivalent_eq,
    round_list_val_with_symbolic,
    transform_dict_list_to_list_dict,
    unique_equivalent_eqs,
    unique_preserve_order,
)
from src.Solver.src.solver.latex_printer import custom_latex
from src.Solver.src.solver.math_parser import split_equation
from src.Solver.src.solver.numeric import numpy_function_or_none
from src.Solver.src.solver.output import SolveOutput, text
from src.Solver.src.solver.sympy_custom_funcs import SYMPY_BOOLEANS

if TYPE_CHECKING:
    from src.Solver.src.solver.solve_calculations import Solve

EQUATION_SYMBOLS = ["!=", ">=", "<=", "==", "=", ">", "<"]

Solutions = dict[Any, list[Any]]


def solve_system_of_eq(solver: Solve) -> SolveOutput:
    return SystemSolver(solver).solve()


class SystemSolver:
    def __init__(self, solver: Solve) -> None:
        self.solver = solver
        self.og_sp_equations: list[Any] = []

    def solve(self) -> SolveOutput:
        solver = self.solver
        processed_eqs = self.make_eqs_real([list(eqs) for eqs in self.process_system_of_eq()])

        sp_equations = [eq[3] for eq in processed_eqs]
        solver.output.append(text("Stelsel van Vergelijkingen:"))
        eq_strings = [f"{custom_latex(eq[0])} = {custom_latex(eq[1])}" for eq in processed_eqs]
        solver.output.append(r"\begin{cases} " + r" \\[4pt] ".join(eq_strings) + r" \end{cases}")

        solutions: Any
        try:
            solutions = _readable_solutions(sp.solve(sp_equations))
            if not solutions:
                raise NotImplementedError
            solver.numerical = False
        except NotImplementedError:
            self.og_sp_equations = sp_equations
            solutions = self.solve_system_of_eq_numerically(sp_equations)
            solutions = self.validate_numeric_solutions(solutions)
            solver.numerical = True

        if not solutions or (isinstance(solutions, dict) and all(sol == [] for sol in solutions.values())):
            solver.output.append(text("Geen oplossing gevonden"))
            return solver.result()

        if isinstance(solutions, list):
            solutions = convert_sol_list_to_dict(solutions)

        solver.output.extend(_solution_output(solutions, solver.numerical))
        return solver.result()

    def process_system_of_eq(self) -> list[tuple[Any, Any, Any, Any]]:
        """Parse every equation of the system into (lhs, rhs, lhs - rhs, relation)."""
        eq_strings = [eq_string for eq_string in self.solver.eq_string.split(";") if eq_string.strip()]
        eqs: list[tuple[Any, Any, Any, Any]] = []
        for eq_string in eq_strings:
            eq_split = [string for string in split_equation(eq_string) if string not in EQUATION_SYMBOLS]
            sides = self.solver.parse_sides(eq_split)
            if sides is None:
                raise ValueError(f"More than one relation sign in {eq_string!r}")
            eqs.append(sides)
        return eqs

    @staticmethod
    def make_symbols_real(eq: Any) -> Any:
        for symbol in eq.free_symbols:
            if symbol.name != "circ":
                eq = eq.subs(symbol, sp.Symbol(symbol.name, real=True))
        return eq

    def make_eqs_real(self, eqs: list[list[Any]]) -> list[list[Any]]:
        return [[self.make_symbols_real(eq) for eq in eq_parts] for eq_parts in eqs]

    # ---------------------------------------------------------------- numerical solving

    def rewrite_system_into_single_variable_eqs(self, sp_equations: list[Any], recursion_count: int = 0) -> list[Any]:
        """Substitute variables until the equations each have a single variable (if possible)."""
        sp_equations = order_equations_by_complexity(sp_equations)
        prev_sp_equations = sp_equations.copy()
        rewritten_eqs: dict[Any, list[Any]] = {}
        for equation in sp_equations.copy():
            if len(equation.free_symbols) == 1:
                continue
            try:
                symbol, substitutions = get_least_complex_substitution(equation)
                if symbol not in rewritten_eqs:
                    rewritten_eqs[symbol] = substitutions
                else:
                    rewritten_eqs[symbol] += [sub for sub in substitutions if sub not in rewritten_eqs[symbol]]
            except NotImplementedError:
                continue

            sp_equations = substitute_symbol_equation(rewritten_eqs, sp_equations)

        if (
            len(sp_equations) != 0
            and any(len(eq.free_symbols) > 1 for eq in sp_equations)
            and recursion_count < 10
            and prev_sp_equations != sp_equations
        ):
            return self.rewrite_system_into_single_variable_eqs(sp_equations, recursion_count + 1)

        return unique_equivalent_eqs(sp_equations)

    def solve_system_of_eq_numerically(self, sp_equations: list[Any], solutions: Solutions | None = None) -> Solutions:
        sp_equations = self.rewrite_system_into_single_variable_eqs(sp_equations)
        if solutions is None:
            solutions = {}

        for equation in sp_equations:
            if len(equation.free_symbols) != 1:
                continue

            symbol = list(equation.free_symbols)[0]
            prior_symbol_solution = solutions.get(symbol, [])
            try:
                solutions[symbol] = prior_symbol_solution + [sol for sol in sp.solve(equation) if sol not in prior_symbol_solution]
                if not solutions[symbol]:
                    raise NotImplementedError
            except NotImplementedError:
                self.solver.symbol = symbol  # solve_numerically works with the solver's symbol
                expr = equation.lhs - equation.rhs
                numerical_solutions = self.solver.solve_numerically(expr, numpy_function_or_none(expr, symbol))
                solutions[symbol] = prior_symbol_solution + [sol for sol in numerical_solutions if sol not in prior_symbol_solution]

        # fill in each solution found and solve the rest of the system with it
        # (each next variable starts from the equations the previous one was last substituted in)
        for symbol, values in solutions.copy().items():
            og_sp_equations = sp_equations.copy()
            for value in values:
                sp_equations = og_sp_equations.copy()
                if sp_equations == []:
                    return solutions

                sp_equations = substitute_symbol_value(sp_equations, symbol, value)
                if og_sp_equations == sp_equations:
                    continue

                solutions = self.solve_system_of_eq_numerically(sp_equations, solutions)

        return solutions

    def add_missing_solutions(self, solutions: Solutions) -> Solutions:
        """Find the values of variables that have no solutions yet, using the solutions of the others."""
        solution_pairs: list[dict[Any, Any]] = transform_dict_list_to_list_dict(solutions)
        for solution_pair in solution_pairs:
            sp_equations = self.og_sp_equations.copy()
            for symbol, value in solution_pair.items():
                sp_equations = substitute_symbol_value(sp_equations, symbol, value)

            sp_equations = [eq for eq in sp_equations if not isinstance(eq, SYMPY_BOOLEANS)]
            if not sp_equations:
                continue

            new_symbol = get_least_used_symbol(sp_equations[0])
            solution_sets = [set(round_list_val_with_symbolic(sp.solve(equation, new_symbol))) for equation in sp_equations]
            solution_sets = [sol for sol in solution_sets if sol]
            if not solution_sets:
                continue

            new_symbol_solutions: Any = solution_sets
            for sol_set in solution_sets:
                if all(sp.N(sol).is_number for sol in sol_set):
                    new_symbol_solutions = solution_sets[0].intersection(sol_set)

            if not new_symbol_solutions:
                continue

            new_symbol_solutions = list(new_symbol_solutions)
            if new_symbol in solutions:
                solutions[new_symbol] += new_symbol_solutions
            else:
                solutions[new_symbol] = new_symbol_solutions

        return solutions

    def check_solution(self, symbol: Any, solution: Any, other_solution_dict: dict[Any, Any]) -> bool:
        """Whether symbol = solution, with the values in other_solution_dict, satisfies all equations."""
        for equation in self.og_sp_equations:
            expr = (equation.lhs - equation.rhs).subs(symbol, solution)
            for other_symbol, other_solution in other_solution_dict.items():
                if symbol != other_symbol:
                    expr = expr.subs(other_symbol, other_solution)

            if abs(sp.N(expr)) > 1e-5:
                return False

        return True

    def remove_invalid_solutions(self, solutions: Solutions) -> Solutions:
        solutions_copy = deepcopy(solutions)
        for symbol, symbol_solutions in solutions_copy.items():
            other_solutions = deepcopy(solutions_copy)
            other_solutions.pop(symbol, None)
            remove_symbol_sol = True
            for symbol_sol in symbol_solutions:
                for other_solution_dict in get_all_combinations_of_solutions(other_solutions):
                    if self.check_solution(symbol, symbol_sol, other_solution_dict):
                        remove_symbol_sol = False

                if remove_symbol_sol:
                    solutions[symbol].remove(symbol_sol)

        return solutions

    def validate_numeric_solutions(self, solutions: Solutions) -> Solutions:
        solutions = remove_extra_solutions(solutions)

        all_symbols = {symbol for equation in self.og_sp_equations for symbol in equation.free_symbols}
        for _ in range(len(all_symbols) - len(solutions)):
            solutions = self.add_missing_solutions(solutions)

        solutions = self.remove_invalid_solutions(solutions)
        return remove_duplicate_solutions(solutions)


def _solution_output(solutions: dict[Any, Any], numerical: bool) -> list[Any]:
    """The solutions as a system: x = 2, y = 1 (or x = 2 ∨ x = 3 for several values)."""
    solutions = {symbol: solutions[symbol] for symbol in sorted(solutions, key=lambda symbol: symbol.name)}

    solution_strings: list[str] = []
    for symbol, value in solutions.items():
        values = value if isinstance(value, list) else [value]
        solution_strings.append(" \\ \\vee \\ ".join(f"{custom_latex(symbol)} {_equals_sign(val)} {custom_latex(val)}" for val in values))

    if len(solution_strings) == 1:
        lines: list[Any] = [text("(Oplossing is numeriek bepaald)")] if numerical else []
        return [*lines, text("Oplossing:"), solution_strings[0]]

    lines = [text("(Oplossingen zijn numeriek bepaald)")] if numerical else []
    return [*lines, text("Oplossingen:"), r"\begin{cases} " + r" \\[4pt]".join(solution_strings) + r" \end{cases}"]


def _equals_sign(value: Any) -> str:
    """≈ for decimals (approximations), = for exact values."""
    return "\\approx" if isinstance(value, sp.Basic) and value.has(sp.Float) else "="


def _readable(value: Any) -> Any:
    # Lambert W and CRootOf aren't taught at school: show those solutions as decimals
    if isinstance(value, sp.Basic) and value.has(sp.LambertW, sp.CRootOf):
        return sp.Float(sp.N(value, 5), 5)
    return value


def _readable_solutions(solutions: Any) -> Any:
    if isinstance(solutions, dict):
        return {symbol: _readable(value) for symbol, value in solutions.items()}
    if isinstance(solutions, list):
        return [_readable_solutions(solution) for solution in solutions]
    return solutions


def convert_sol_list_to_dict(solution: list[dict[Any, Any]]) -> dict[Any, Any]:
    """[{x: 1, y: 2}, {x: 3, y: 2}] -> {x: [1, 3], y: 2}"""
    new_solution_dict: dict[Any, Any] = {}
    for solution_dict in solution:
        for key, value in solution_dict.items():
            if key not in new_solution_dict:
                new_solution_dict[key] = value
            elif isinstance(new_solution_dict[key], list) and value not in new_solution_dict[key]:
                new_solution_dict[key].append(value)
            elif new_solution_dict[key] != value:
                new_solution_dict[key] = [new_solution_dict[key]] + [value]

    return new_solution_dict


def order_equations_by_complexity(sp_equations: list[Any]) -> list[Any]:
    """Equations with fewer variables and operations first."""
    return sorted(sp_equations, key=lambda equation: len(equation.free_symbols) + sp.count_ops(equation) / 10)


def get_least_used_symbol(equation: Any) -> Any:
    equation_str = str(equation)
    least_used_symbol = None
    least_used_amt = float("inf")
    for symbol in equation.free_symbols:
        amt_symbol = equation_str.count(symbol.name)
        if amt_symbol < least_used_amt:
            least_used_amt = amt_symbol
            least_used_symbol = symbol

    return least_used_symbol


def get_least_complex_substitution(equation: Any) -> tuple[Any, list[Any]]:
    """The variable that's easiest to solve the equation for, and the solutions for it."""
    substitution_eqs_dict: dict[tuple[Any, ...], Any] = {}
    for symbol in equation.free_symbols:
        try:
            substitution_eqs_dict[tuple(sp.solve(equation, symbol))] = symbol
        except NotImplementedError:
            continue

    def count_combined_ops(substitution: list[Any]) -> int:
        return sum(sp.count_ops(eq) for eq in substitution)

    candidates = [list(eq) for eq in substitution_eqs_dict]
    candidates = sorted([eq for eq in candidates if eq != []], key=len)
    candidates = [eq for eq in candidates if len(eq) == len(candidates[0])]
    candidates = sorted(candidates, key=count_combined_ops)

    if len(candidates) > 1:
        # sorted by name to remove the random order of the symbols
        candidates = sorted(candidates, key=lambda x: substitution_eqs_dict[tuple(x)].name, reverse=True)

    chosen = candidates[0]
    return substitution_eqs_dict[tuple(chosen)], chosen


def substitute_symbol_equation(rewritten_eqs: dict[Any, list[Any]], sp_equations: list[Any]) -> list[Any]:
    for symbol, equations in rewritten_eqs.items():
        for i, sp_equation in enumerate(sp_equations.copy()):
            for j, substitution in enumerate(equations):
                new_sp_equation = sp.simplify(sp_equation.subs(symbol, substitution), inverse=True)
                if new_sp_equation in SYMPY_BOOLEANS + (sp.true, sp.false):
                    continue

                # add any extra versions as an equation, for example:
                # x^2 + y^2 = 1 --> y = -sqrt(1 - x^2) AND y = sqrt(1 - x^2)
                if j == 0:
                    sp_equations[i] = new_sp_equation
                elif not any(equivalent_eq(new_sp_equation, eq) for eq in sp_equations):
                    sp_equations.append(new_sp_equation)

    return unique_equivalent_eqs(sp_equations)


def substitute_symbol_value(sp_equations: list[Any], symbol: Any, value: Any) -> list[Any]:
    substituted = [equation.subs(symbol, value) for equation in sp_equations]
    return [eq for eq in substituted if not isinstance(eq, SYMPY_BOOLEANS)]


def remove_extra_solutions(solutions: Solutions) -> Solutions:
    """Keep as many solutions for every variable as the variable with the fewest solutions has."""
    if not solutions:
        return solutions

    min_solutions = min(len(values) for values in solutions.values()) or 1
    return {symbol: values[:min_solutions] for symbol, values in solutions.items()}


def get_all_combinations_of_solutions(solutions: Solutions) -> list[dict[Any, Any]]:
    return [dict(zip(solutions.keys(), values)) for values in itertools.product(*solutions.values())]


def remove_duplicate_solutions(solutions: Solutions) -> Solutions:
    for symbol in solutions:
        solutions[symbol] = unique_preserve_order(round_list_val_with_symbolic(solutions[symbol]))
    return solutions
