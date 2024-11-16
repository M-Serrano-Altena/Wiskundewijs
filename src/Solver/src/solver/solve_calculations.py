"""
Module for symbolic and numerical equation solving.

The `solve_calculations` module provides tools for parsing, solving, and analyzing mathematical equations
symbolically and numerically, utilizing libraries like SymPy and SciPy. It includes the `Solve` class, which
supports initialization with an equation string and optional angle mode selection (degrees or radians).

Key functionalities:
- Equation parsing and transformation using custom mathematical parsing tools.
- Symbolic manipulations and simplifications powered by SymPy.
- Numerical solutions for equations using methods like `fsolve`, `bisect`, and `newton`.
- Customizable LaTeX rendering for symbolic outputs.

Dependencies:
- SymPy, SciPy, NumPy, and other custom helper functions.

"""

import numpy as np
import sympy as sp
from sympy.simplify.fu import TR2, TR111
import sympy.vector as sp_vector
import regex as re
from scipy.optimize import fsolve, bisect, newton
from warnings import filterwarnings
from src.Solver.src.solver.math_parser import *
from src.Solver.src.solver.helper import *
from src.Solver.src.solver.sympy_custom_funcs import *
import src.Solver.src.solver.sympy_custom_funcs as sp_custom
import traceback
import typing
from types import FunctionType
from collections.abc import Iterable
from numbers import Number
from copy import deepcopy
import itertools

filterwarnings("ignore", category=RuntimeWarning)

class VectorFieldError(TypeError):
    """Custom error raised when an invalid field type is used for vector operations."""
    def __init__(self, message="Operation requires a vector field, not a scalar function"):
        super().__init__(message)

class ScalarFieldError(TypeError):
    """Custom error raised when an invalid field type is used for scalar operations."""
    def __init__(self, message="Operation requires a scalar field, not a vector function"):
        super().__init__(message)


class Solve:
    def __init__(self, input_string: str, use_degrees: typing.Optional[bool]) -> None:
        """
        Initializes the Solve class with the input equation string.

        Args:
            input_string (str): A string representing the equation to solve.
        """

        self.symbol = None
        self.use_degrees = use_degrees
        self.use_degrees_reciprocal = True if use_degrees is None else use_degrees
        self.locals = LOCALS.copy()
        self.equation_type = "="
        self.equation_is_inequality = False
        self.equation_type_sp = sp.Eq
        self.solution_set = None
        self.solution_inequality = None
        self.has_any_solutions = False
        self.interval_solutions = None
        self.vert_asympt = None
        self.vert_asympt_eq = None

        self.eq_string = math_interpreter(input_string)
        if any(degree_symbol in self.eq_string for degree_symbol in ["°", "∘"]):
            self.use_degrees = True
            self.eq_string = re.sub(r"\^?[°∘]", "", self.eq_string)
            self.eq_string = re.sub(r"\^?\(\)", "", self.eq_string)

        if self.use_degrees_reciprocal:
            self.locals.update(DEG_ARC_GONIO_LOCALS)

        self.output = []
        self.equation_interpret = self.eq_string
        self.plot = False
        self.intersect = False
        self.numerical = False
        self.multivariate = False
        self.derivative = False
        self.integral = False
        self.real_root = False

        self.is_vector = False
        self.vect_dim = sp_custom.vect_dim

        self.is_system_of_eq = ";" in self.eq_string


    @staticmethod
    def get_lambdas(expr: typing.Union[sp.Expr, typing.Iterable[sp.Expr]], symbol: sp.Symbol, numeric: bool = False) -> typing.Union[FunctionType, typing.Iterable[FunctionType]]:
        def get_lambda_numeric(single_expr, modules = ["numpy", "scipy", "sympy"]):
            for module in modules:
                try:
                    single_expr = sp_custom.get_real_root(single_expr)
                    func = sp.lambdify(symbol, single_expr, module)
                    try:
                        func(0)
                    except ZeroDivisionError:
                        func(1)
                    return func
                except NameError:
                    continue
        
        if not isinstance(expr, Iterable):
            if numeric:
                return get_lambda_numeric(single_expr=expr)
            return sp.lambdify(symbol, expr, "sympy")
    
        lambdas = []
        if numeric:
            for single_expr in expr:
                lambdas.append(get_lambda_numeric(single_expr=single_expr))
        else:
            for single_expr in expr:
                lambdas.append(sp.lambdify(symbol, single_expr, "sympy"))

        return lambdas
    
    @staticmethod
    def apply_func_to_array(func: FunctionType, array: typing.Union[np.ndarray, Number]) -> np.ndarray:
        try:
            obj = func(array)
        except ZeroDivisionError:
            obj = func(array + 1e-10)


        if np.isscalar(obj):
            return np.full(array.shape, obj).astype(float)
            
        return obj.astype(float)
            

    def numerical_roots(
        self,
        eq_sp: sp.Expr,
        eq_lambda_np: FunctionType,
        a: float = -10000,
        b: float = 10000,
        dx: float = 1e-6,
        solve_method: str = "newton",
        tolerance: float = 0.01,
        default_func: bool = True
    ) -> np.ndarray:
        
        """
        Finds numerical roots of the equation within a specified interval using various methods.

        Args:
            eq (sp.Expr): The equation to solve.
            a (float, optional): The lower bound of the interval. Defaults to -10000.
            b (float, optional): The upper bound of the interval. Defaults to 10000.
            dx (float, optional): The step size for root finding. Defaults to 0.01.
            solve_method (str, optional): The root finding method ("newton", "bisect", "fsolve"). Defaults to "newton".
            dy (float, optional): The tolerance for considering a value as zero. Defaults to 0.1.
            use_scale_factor (bool, optional): Whether to use a scaling factor for the y-values. Defaults to False.
            default_func (bool, optional): Whether the function is a default (internal) function. Defaults to True.

        Returns:
            np.ndarray: The array of found roots.
        """

        if solve_method == "newton":
            eq_diff_sp = sp.diff(eq_sp, self.symbol).doit().simplify()
            eq_diff_lambda_np = self.get_lambdas(eq_diff_sp, self.symbol, numeric=True)

        x_vals = get_smooth_x_coords((a, b), dx, self.vert_asympt)
        y_vals = eq_lambda_np(x_vals)
        xy = np.vstack((x_vals, y_vals)).T
        xy = xy[~np.isnan(xy[:,1]) & ~np.isinf(xy[:,1])]

        if xy.size == 0:
            if default_func:
                self.intersect = False
                self.numerical = False
            return np.array([])

        min_values = xy[np.argmin(np.abs(xy[:,1]))]
        y_value_shift = eq_lambda_np(min_values[0] + tolerance)
        y_value_shift = tolerance if np.isnan(y_value_shift) or np.isinf(y_value_shift) else y_value_shift
        tolerance = 3*abs(y_value_shift - min_values[1])

        condition = np.abs(xy[:, 1]) < tolerance
        indices = np.where(condition)[0]

        # Find discontinuities in indices
        discontinuities = np.where(np.diff(indices) != 1)[0] + 1
        split_indices = np.split(indices, discontinuities)

        if indices.size == 0:
            if default_func:
                self.intersect = False
                self.numerical = False
            return np.array([])
            
        roots = []
        for indices in split_indices:

            if indices.size == 0:
                continue

            min_index = np.argmin(np.abs(xy[indices]), axis=0)[1]
            guess = xy[indices][min_index, 0]

            try:
                if solve_method == "newton":
                    root = newton(eq_lambda_np, guess, fprime=eq_diff_lambda_np)

                elif solve_method == "bisect":
                    a_bisect = np.min(xy[indices])
                    b_bisect = np.max(xy[indices])

                    try:
                        if eq_lambda_np(a_bisect) * eq_lambda_np(b_bisect) < 0:
                            root = bisect(eq_lambda_np, a_bisect, b_bisect)
                        else:
                            root = None
                    except ValueError:
                        root = None

                elif solve_method == "fsolve":
                    root = float(fsolve(eq_lambda_np, guess))

            except RuntimeError:
                root = None

            if root is not None and not np.isnan(root):
                roots.append(root)
            
        # Ensure roots are within bounds and remove duplicates
        roots = np.array(roots)
        roots = np.unique(roots[(roots >= a) & (roots <= b)])

        # Boundary check
        if a in roots and eq_lambda_np(a -1) * eq_lambda_np(a + 1) >= 0:
            roots = np.delete(roots, np.where(roots == a))
        if b in roots and eq_lambda_np(b - 1) * eq_lambda_np(b + 1) >= 0:
            roots = np.delete(roots, np.where(roots == b))

        roots = roots[(np.isfinite(eq_lambda_np(roots + 0.01))) | (np.isfinite(eq_lambda_np(roots - 0.01)))]

        if default_func:
            self.intersect = True
            self.numerical = True

        return roots


    def solve_numerically(self, eq_sp: typing.Optional[sp.Expr] = None, eq_lambda_np: typing.Optional[FunctionType] = None) -> sp.FiniteSet:
        """
        Solves the equation numerically and returns the roots as a finite set.

        Args:
            sp_func_lambda (Optional[sp.Expr], optional): The equation to solve. If None, the class equation is used. Defaults to None.

        Returns:
            sp.FiniteSet: A set of the found numerical solutions.
        """

        if eq_sp is None or eq_lambda_np is None:
            default_func = True
            eq_sp = self.eq12 if not self.multivariate else self.eq2
            eq_lambda_np = self.eq12_lambda_np if not self.multivariate else self.eq2_lambda_np
            self.numerical = True
        else:
            default_func = False

        methods = ["newton", "fsolve", "bisect"]

        # checks between -10 000 and 10 000 with all methods if the previous returns nothing
        for method in methods:
            self.roots_numeric = self.numerical_roots(eq_sp, eq_lambda_np, -10000, 10000, solve_method=method, default_func=default_func)
            if self.roots_numeric.size != 0:
                break

        solutions = sp.FiniteSet(*self.roots_numeric)
        self.intersect = not solutions.is_empty

        # handle inequality
        if self.equation_is_inequality and not isinstance(self.solution_inequality, (sp.logic.boolalg.BooleanFalse, sp.logic.boolalg.BooleanTrue, list)) and self.intersect:
            abs_sorted_roots = self.roots_numeric[np.argsort(np.abs(self.roots_numeric))]
            solution_inequality_list = list(np.append(abs_sorted_roots[abs_sorted_roots >=0], abs_sorted_roots[abs_sorted_roots < 0]))

            test_dx = 0.1 if self.equation_type in ">=" else -0.1
            self.equation_type_opposite = sp_custom.flip_inequality_sign(self.equation_type)
            self.equation_type_opposite_sp = map_equation_type_to_sp(self.equation_type_opposite)

            if len(solution_inequality_list) == 1:
                solution = sp.nsimplify(solution_inequality_list[0], [sp.pi, sp.E], rational=False)
                if apply_opperator(self.eq12_lambda_np(solution + test_dx), self.equation_type, 0):
                    self.solution_inequality = self.equation_type_sp(self.symbol, solution)
                else:
                    self.solution_inequality = self.equation_type_opposite_sp(self.symbol, solution)

            elif len(solution_inequality_list) > 1:
                index_limited_items = 4 if len(solution_inequality_list) >= 4 else len(solution_inequality_list)
                solution_inequality_list = solution_inequality_list[:index_limited_items]
                solution_inequality_list = [sp.nsimplify(solution, [sp.pi, sp.E], rational=False) for solution in solution_inequality_list]
                solution_inequality_list = [(int(round(sol, 3)) if int(round(sol, 3)) == round(sol, 3) else round(sol, 3) ) if sp.N(sol) == sol else sol for sol in solution_inequality_list]

                for i, solution in enumerate(solution_inequality_list):
                    if apply_opperator(self.eq12_lambda_np(float(solution) + test_dx), self.equation_type, 0):
                        solution_inequality_list[i] = self.equation_type_sp(self.symbol, solution)
                    else:
                        solution_inequality_list[i] = self.equation_type_opposite_sp(self.symbol, solution)

                def combine_expressions(expr1, expr2):
                    if isinstance(sp.simplify(expr1 & expr2), (sp.logic.boolalg.BooleanFalse, sp.logic.boolalg.BooleanTrue)) and len(solution_inequality_list) < 4:
                        return expr1 | expr2
                    
                    if isinstance(sp.simplify(expr1 | expr2), (sp.logic.boolalg.BooleanFalse, sp.logic.boolalg.BooleanTrue)):
                        return expr1 & expr2
                    
                    if expr1 == solution_inequality_list[0] and len(solution_inequality_list) >= 4:
                        return expr2
                    
                    return expr1

                combined_expr = solution_inequality_list[0]
                for i in range(1, len(solution_inequality_list)):
                    combined_expr = combine_expressions(combined_expr, solution_inequality_list[i])

                self.solution_inequality = combined_expr
        
        return solutions


    def check_solve_numerically(self, solution_set) -> typing.Optional[sp.FiniteSet]:
        """
        Checks if the equation's solutions need to be solved numerically, and does so if necessary.

        Returns:
            Optional[sp.FiniteSet]: A set of the numerical solutions, or None if not applicable.
        """

        if isinstance(solution_set, sp.ConditionSet) and solution_set.condition.simplify() == sp.Eq(self.eq12, 0).simplify():
            return self.solve_numerically()
        

    def process_equation(self, eq_string: str) -> str:
        equation_symbols = ["!=", ">=", "<=", "==", "=", ">", "<"]
        eq_split = split_equation(eq_string)
        eq_split = [string for string in eq_split if string not in equation_symbols]

        for equation_type in equation_symbols:
            if equation_type in eq_string:
                self.equation_type = equation_type
                self.equation_type_sp = map_equation_type_to_sp(equation_type)
                return self.set_eqs(eq_split)
        
        return self.set_eqs(eq_split)

    def set_eqs(self, eq_split, use_self=True):
        eq_split[0], eq1 = self.sympify_equation(eq_split[0])

        if len(eq_split) == 1:
            eq2 = 0
        elif len(eq_split) == 2:
            eq_split[1], eq2 = self.sympify_equation(eq_split[1])
        elif use_self:
            self.output.append(("Error: Meer dan 1 relatieteken (=, ≥, ≤, etc.)", {"latex": False}))
            return None
        
        eq1 = self.gonio_degree_check(eq1, eq_split[0], use_degree=self.use_degrees)
        if len(eq_split) == 2:
            eq2 = self.gonio_degree_check(eq2, eq_split[1], use_degree=self.use_degrees)
            eq12 = eq1 - eq2
        else:
            eq12 = eq1

        vector_classes = (sp_vector.Vector, sp.MatrixBase, sp.MatrixExpr)
        if isinstance(eq1, vector_classes) or isinstance(eq2, vector_classes):
            self.is_vector = True
            self.vect_dim = sp_custom.vect_dim

        elif any("grad" in eq_split_part for eq_split_part in eq_split):
            self.is_vector = True
            self.vect_dim = sp_custom.vect_dim


        eq = self.get_self_eq(eq1, eq2)

        if any(sub_str in self.eq_string for sub_str in ["vect", "laplacian", "matrix"]):
            self.is_vector = True
            self.vect_dim = sp_custom.vect_dim

        if not use_self:
            return eq1, eq2, eq12, eq
        
        self.eq1_unsimplified, self.eq2_unsimplified, self.eq12_unsimplified = self.eq1, self.eq2, self.eq12 = eq1, eq2, eq12
        self.eq = eq


        if self.equation_type == "==":
            self.output.append(f"\\text{{{self.eq}}}")
            return None

        if len(eq_split) == 2:
            self.eq_string = str(self.eq)

        return eq_split

    def sympify_equation(self, eq_str: str) -> sp.Basic:
        if any(sub_str in eq_str for sub_str in ["div", "curl"]) and not any(sub_str in eq_str for sub_str in ["vect", "grad"]):
            raise VectorFieldError("Argument must be a vector (use 'vect' function)")

        try:
            return eq_str, TR111(sp.sympify(eq_str, locals=self.locals)).doit()
        except ValueError:
            eq_str = add_args_to_func(eq_str, func_name="integrate", replace_with="x").replace(".integrate()", ".integrate(x)")
            return eq_str, TR111(sp.sympify(eq_str, locals=self.locals)).doit()

    def gonio_degree_condition(self, inner_arg: str) -> bool:
        try:
            if not isinstance(sp.sympify(inner_arg), sp.Expr):
                return False
        except Exception:
            return False
        
        return sp.nsimplify(sp.sympify(inner_arg, self.locals).subs(degree, 1)).is_Rational
    
    def convert_gonio_to_degree(self, eq_str: str, gonio_set: set[str], use_degree_condition=True) -> str:
        for gonio_func in gonio_set:
            if gonio_func in eq_str:
                if use_degree_condition:
                    eq_str = apply_inner_func_to_func(eq_str, func_name=gonio_func, inner_func_name="rad", inner_arg_condition_func=self.gonio_degree_condition)
                else:
                    eq_str = apply_inner_func_to_func(eq_str, func_name=gonio_func, inner_func_name="rad")

        return eq_str

    def gonio_degree_check(self, eq: sp.Expr, eq_str: str, use_degree: typing.Optional[bool]=None):
        gonio_set = set(["sin", "cos", "tan", "sec", "csc", "cot"])
        relevant_gonio_set = set()
        for gonio_func in gonio_set:
            if bool(re.findall(rf"(?<!a){gonio_func}\b", eq_str)):
                relevant_gonio_set.add(gonio_func)

        # if the equation doesn't contain a gonio function, then just return
        if use_degree is False or len(relevant_gonio_set) == 0:
            return eq
        
        # only use the condition if use_degree is set to None and not when it's set to True
        use_degree_condition = not bool(use_degree)
        eq_str_new = self.convert_gonio_to_degree(eq_str, relevant_gonio_set, use_degree_condition=use_degree_condition)
        if eq_str_new != eq_str:
            self.equation_interpret = add_degree_symbol(self.equation_interpret, gonio_set=relevant_gonio_set)
            if any(arc_gonio for arc_gonio in ["asin", "acos", "atan", "asec", "acsc", "acot"] if arc_gonio in eq_str_new):
                self.equation_interpret = self.equation_interpret.replace("°", r"")
                self.eq_string = self.equation_interpret
            else:
                self.eq_string = self.equation_interpret.replace("°", r"^(circ)")

        # get rid of the degree symbol
        sp_eq = sp.sympify(eq_str_new, locals=self.locals).subs(degree, 1)
        return sp_eq


    def get_self_eq(self, eq1, eq2):
        try:
            return sp.nsimplify(self.equation_type_sp(eq1, eq2), tolerance=1e-7)
        except AttributeError:
            return self.equation_type_sp(eq1, eq2)
                    


    def solve_equation(self) -> typing.Tuple[str, typing.List[typing.Tuple[str, dict]], bool]:
        """Solve the equation, analyze it, and display the results.

        Returns:
            A tuple containing:
            - The interpreted equation string.
            - A list of output messages.
            - A boolean indicating whether to plot the results.
        """

        def handle_multivariate(eq12: sp.Basic, y_symbol: sp.Symbol) -> typing.Tuple[sp.Basic, sp.Basic]:
            free_y_equation = reversed([sol for sol in sp.solve(eq12, y_symbol) if "I" not in str(sol)])
            abs_solutions = []
            new_solutions = []
            for sol in free_y_equation:
                if sp.Abs(sol) not in abs_solutions:
                    new_solutions.append(sol)
                    abs_solutions.append(sp.Abs(sol))

            return y_symbol, new_solutions[0]
        
        def check_multivariate():
            if len(free_symbols) == 2:
                y_symbol = sp.symbols("y")
                
                if y_symbol in free_symbols:
                    self.multivariate = True
                    self.eq1, self.eq2 = handle_multivariate(eq12=self.eq12, y_symbol=y_symbol)
                    self.eq12 = - self.eq2
                    self.eq = self.get_self_eq(0, self.eq2)
                    free_symbols.remove(y_symbol)
                    eq_split = (str(y_symbol), str(self.eq2))

                    return eq_split
        
        def set_real_symbol():
            self.symbol = free_symbols.pop()
            symbol_new = sp.symbols(str(self.symbol), real=True)
            self.eq = self.eq.subs(self.symbol, symbol_new)
            self.eq1 = sp.sympify(self.eq1).subs(self.symbol, symbol_new)
            self.eq2 = sp.sympify(self.eq2).subs(self.symbol, symbol_new)
            self.eq12 = self.eq1 - self.eq2 if not self.multivariate else self.eq2
            self.symbol = symbol_new

        def no_solutions_inequality_output():
            if self.equation_is_inequality:
                try:
                    extrema_func = [self.eq12_lambda_np(float(sol)) for sol in sp.solve(sp.diff(self.eq12))]
                    extrema_func = min(extrema_func) if ">" in self.equation_type else max(extrema_func)
                except Exception:
                    values = sorted([num for num in range(-100, 100)], key=abs)
                    for num in values:
                        try:
                            extrema_func = self.eq12_lambda_np(num)
                        except Exception:
                            pass

                if apply_opperator(extrema_func, self.equation_type, 0):
                    self.output.append(("Deze vergelijking is waar voor alle x", {"latex": False}))
                else:
                    self.output.append(("Deze vergelijking klopt voor geen enkele x", {"latex": False}))
        
        def no_solutions_output():
            self.plot = True
            self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
            self.output.append(f"{custom_latex(self.eq1)} {sp_custom.equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2)}")

            if self.equation_is_inequality:
                no_solutions_inequality_output()
                return self.equation_interpret, self.output, self.plot

            if self.multivariate:
                self.output.append((f"Geen snijpunt met de x-as gevonden", {"latex":False}))
            else:
                self.output.append(("Geen oplossing gevonden", {"latex": False}))
            return self.equation_interpret, self.output, self.plot
        

        def set_inequatity_solution_output():
            if not isinstance(self.solution_inequality, (sp.logic.boolalg.BooleanFalse, sp.logic.boolalg.BooleanTrue, list)):
                self.output.append((f"De oplossing is:", {"latex":False}))
                self.output.append(custom_latex(self.solution_inequality))
                return

            no_solutions_inequality_output()
        

        def set_count_solutions():
            is_numerical = lambda solution: solution.equals(sp.N(solution))
            has_many_decimals = lambda solution: sp.N(solution, 9).equals(sp.N(solution, 10))
            equals_sign = lambda solution: "=" if not is_numerical(solution) or has_many_decimals(solution) else "\\approx"
            
            interval_solutions = [sp.nsimplify(solution, [sp.pi, sp.E], rational=False) for solution in self.interval_solutions]
            if len(self.interval_solutions) == 1:
                solution = interval_solutions[0]
                solution_display = solution
                if is_numerical(solution):
                    solution_display = sp.N(solution, 7)
                    try:
                        if int(solution_display) == float(solution_display):
                            solution_display = int(solution)
                    except Exception:
                        pass

                self.output.append(f"{custom_latex(self.symbol)} {equals_sign(solution)} {custom_latex(solution_display, symbol=self.symbol)}")
                if not is_numerical(solution):
                    self.output[-1] += f" \\approx {sp.N(solution, 5)}"
                return
            
            counter = 0
            for solution in interval_solutions:
                counter += 1

                solution_display = solution
                if is_numerical(solution):
                    solution_display = sp.N(solution, 7)
                    try:
                        if int(solution_display) == float(solution_display):
                            solution_display = int(solution)
                    except Exception:
                        pass

                self.output.append(f"{counter}) \\quad {custom_latex(self.symbol)} {equals_sign(solution)} {custom_latex(solution_display, symbol=self.symbol)}")
                if not is_numerical(solution):
                    self.output[-1] += f" \\approx {sp.N(solution, 5)}"


        def set_numerical_text():
            if self.numerical:
                if len(self.roots_numeric) == 1:
                    self.output.append(("(Oplossing is numeriek bepaald)", {"latex":False, "new_line":2}))
                else:
                    self.output.append(("(Oplossingen zijn numeriek bepaald)", {"latex":False, "new_line":2}))


        def get_uneval_derivative_integral(eq_split_index: int=0, is_integral: bool=False) -> sp.Basic:
            symbol = self.symbol or sp.symbols("x", real=True)
            extra_index = 0
            if eq_split_index == 0:
                eq = self.eq1
            else:
                eq = self.eq2

            if is_integral:
                if eq.is_number:
                    extra_index = 1

            str_func = np.array(([f"f'({symbol})", f"g'({symbol})"], [f"F({symbol})", f"G({symbol})"], ["I", "II"]))[int(is_integral) + extra_index][eq_split_index]
            if is_integral:
                derivative_integral = self.integral[eq_split_index]
            else:
                derivative_integral = self.derivative[eq_split_index]

            derivative_integral = get_uneval_sp_objs(eq_split[eq_split_index])
            if derivative_integral == eq:
                derivative_integral = get_uneval_sp_objs(add_args_to_func(eq_split[eq_split_index], func_name="diff", replace_with=symbol))

            if len(derivative_integral.free_symbols) >= 1:
                derivative_integral = derivative_integral.subs(derivative_integral.free_symbols.pop(), symbol)
            
            return str_func, derivative_integral, eq
        
        def set_combined_derivative_integral_text(is_derivative_integral, specific_text: str="afgeleide"):
            if self.derivative.any() and self.integral.any():
                if self.integral[0] and self.derivative.any():
                    if len(eq_split) == 2 and self.derivative[1]:
                        self.output[0] = ("De primitieve en afgeleide van de functies zijn:", {"latex": False})
                    elif self.derivative[0]:
                        self.output[0] = ("De primitieve en afgeleide van de functie is:", {"latex": False})

                if len(eq_split) == 2 and self.integral[1] and self.derivative.any():
                    if self.integral[0] or self.derivative[0]:
                        self.output[0] = ("De primitieve en afgeleide van de functies zijn:", {"latex": False})
                    elif self.derivative[1]:
                        self.output[0] = ("De primitieve en afgeleide van de functie is:", {"latex": False})

            else:
                if len(eq_split) == 2 and is_derivative_integral.all():
                    self.output.append((f"De {specific_text}n van de functies zijn:", {"latex": False}))
                else:
                    self.output.append((f"De {specific_text} van de functie is:", {"latex": False}))


        def set_derivative_integral_output(is_integral: bool=False):
            if is_integral:
                specific_text = "primitieve"
                is_derivative_integral = self.integral
            else:
                specific_text = "afgeleide"
                is_derivative_integral = self.derivative

            if is_integral:
                set_combined_derivative_integral_text(is_derivative_integral, specific_text)

            if is_derivative_integral[0]:
                str_func, derivative_integral, eq = get_uneval_derivative_integral(eq_split_index=0, is_integral=is_integral)
                output = f"{str_func} = {custom_latex(derivative_integral)} = {custom_latex(eq)}"
                if "F" in str_func or "G" in str_func:
                    output += " + C"
                self.output.append(output)

            if len(eq_split) == 2 and is_derivative_integral[1]:
                str_func, derivative_integral, eq = get_uneval_derivative_integral(eq_split_index=1, is_integral=is_integral)
                output = f"{str_func} = {custom_latex(derivative_integral)} = {custom_latex(eq)}"
                if "F" in str_func or "G" in str_func:
                    output += " + C"
                self.output.append(output)

        try:
            if self.is_system_of_eq:
                return self.solve_system_of_eq()

            eq_split = self.process_equation(self.eq_string)

            if eq_split is None:
                return self.equation_interpret, self.output, self.plot
            
            if self.is_vector:
                return self.solve_vector(eq_split=eq_split)
            
            free_symbols = [symbol for symbol in self.eq12.free_symbols if symbol.name != "circ"]
            if free_symbols:
                new_eq_spit = check_multivariate()
                if new_eq_spit:
                    eq_split = new_eq_spit

                if len(free_symbols) >= 2:
                    self.output.append(("Error: Meer dan 1 variabele", {"latex": False}))
                    return self.equation_interpret, self.output, self.plot
                
                set_real_symbol()
                
                eqs = [self.eq1, self.eq2, self.eq12]
                self.eq1_unsimplified, self.eq2_unsimplified, self.eq12_unsimplified = eqs
                eqs = [custom_simplify(eq) for eq in eqs]
                self.eq1, self.eq2, self.eq12 = eqs
                self.eq1_lambda, self.eq2_lambda, self.eq12_lambda = self.get_lambdas(eqs, symbol=self.symbol)
                self.eq1_lambda_np, self.eq2_lambda_np, self.eq12_lambda_np = self.get_lambdas(eqs, symbol=self.symbol, numeric=True)
                if self.multivariate:
                    self.eq1_lambda = self.eq1_lambda_np = lambda _: 0

                if len(eq_split) == 1 and not sp.sympify(self.eq1).is_number:
                    self.equation_interpret = f"{self.eq_string} = 0"            

            self.derivative = np.array(["diff" in string for string in eq_split])
            self.integral = np.array(["integrate" in string for string in eq_split])
            if self.derivative.any():
                set_derivative_integral_output(is_integral=False)

            if self.integral.any():
                set_derivative_integral_output(is_integral=True)

            if self.derivative.any() or self.integral.any():
                self.output.append(("", {"latex": False}))

            if self.symbol:
                try:
                    self.domain = sp.calculus.util.continuous_domain(self.eq12, self.symbol, domain=sp.S.Reals)
                except NotImplementedError:
                    self.domain = sp.S.Reals
                self.domain_is_reals = bool(self.domain is sp.S.Reals)

            self.equation_is_inequality = self.equation_type != '=' and not self.multivariate

            if not isinstance(self.eq12, sp.AccumBounds) and self.symbol is not None:
                self.solution_set = sp.solveset(self.eq12, domain=sp.S.Reals)
            else:
                self.solution_set = sp.EmptySet

            if self.equation_is_inequality:
                self.solution_inequality = sp.solve(self.eq)

            if self.symbol:
                self.vert_asympt_eq = write_as_sin_and_cos(self.eq12).as_numer_denom()[1]
                if self.vert_asympt_eq.is_number:
                    self.vert_asympt_eq = None
                
                elif not self.domain_is_reals and (self.domain.is_Interval or self.domain.is_Union):
                    amt_intervals = len(self.domain.args) if self.domain.is_Union else 1
                    asympt_check = []
                    asympt_values = []
                    for i in range(amt_intervals):
                        sub_domain = self.domain.args[i] if self.domain.is_Union else self.domain
                        asympt_check.extend([self.eq12_lambda(sub_domain.args[j]).is_finite for j in range(2) if sub_domain.args[j].is_finite])
                        asympt_values.extend([sub_domain.args[j] for j in range(2) if sub_domain.args[j].is_finite])

                    if False in asympt_check:
                        self.vert_asympt_eq = list(set([asympt_values[i] for i in range(len(asympt_values)) if not asympt_check[i]]))
                        if not self.vert_asympt_eq:
                            self.vert_asympt_eq = None

            check_numerical = self.check_solve_numerically(self.solution_set)
            if check_numerical is not None and not self.intersect:
                return no_solutions_output()

            elif check_numerical is not None:
                self.solution_set = check_numerical 
                self.has_any_solutions = not self.solution_set.is_empty

            elif self.symbol:
                try:
                    complex_symbol = sp.symbols("x")
                    self.solutions_complex = sp.solve(TR2(sp.Eq(self.eq1_lambda(complex_symbol), self.eq2_lambda(complex_symbol))))
                    self.solutions = [sol for sol in self.solutions_complex if sol.is_real and sp.N(self.eq1_lambda(sol)).is_real]
                except Exception:
                    self.solutions_complex = []
                    try:
                        self.solutions = sp.solve(TR2(self.eq12))
                    except Exception:
                        self.solutions = []

                self.has_any_solutions = bool(self.solutions_complex or self.solutions or (self.solution_set.is_FiniteSet and not self.solution_set.is_empty))


            if not self.has_any_solutions and not self.numerical:
                self.eq_string = add_args_to_func(self.eq_string, func_name="root", replace_with="evaluate=False", amt_commas=2)

                try:
                    self.eq_string = sp.sympify(self.eq_string, evaluate=False)
                except AttributeError:
                    self.eq_string = sp.sympify(self.eq_string)

                if len(eq_split) == 1:
                    if not self.symbol:
                        solution = sp.nsimplify(self.eq1, [sp.pi])
                        equals_sign = '='
                        if solution.is_number:
                            if solution.equals(sp.N(solution)) or self.eq1.equals(sp.N(solution)):
                                equals_sign = '='
                            else:
                                equals_sign = '\\approx'

                            solution = sp.N(solution)
                            try:
                                complex_num = False
                                if solution.is_finite and int(solution) == float(solution) and len(str(round(solution))) < 10:
                                    solution = int(solution)

                            except TypeError:
                                complex_num = True
                                real_part, imag_part = solution.as_real_imag()

                                if sp.Integer(real_part) == real_part and sp.Integer(imag_part) == imag_part:
                                    solution = sp.Add(sp.Integer(real_part), sp.Mul(sp.Integer(imag_part), sp.I))

                                if real_part == sp.nsimplify(self.eq1, [sp.pi]).as_real_imag()[0] and imag_part == sp.nsimplify(self.eq1, [sp.pi]).as_real_imag()[1]:
                                    equals_sign = '='

                            except ValueError:
                                equals_sign = '='

                        try:
                            str(self.eq1)
                        except ValueError:
                            equals_sign = '='

                        if self.eq1 != self.eq_string and equals_sign != "=" and "circ" not in str(self.eq_string):
                            if not complex_num and sp.N(solution, 9).equals(sp.N(solution, 10)):
                                equals_sign = '='  
                            self.output.append(f"{custom_latex(self.eq_string)} = {custom_latex(self.eq1)} {equals_sign} {custom_latex(solution, symbol=self.symbol)}")

                        elif self.eq_string == solution:
                            if eq_split[0] != str(solution):
                                has_dot_function = any(dot_func in eq_split[0] for dot_func in [".subs", ".diff", ".integrate", "limit"])
                                if self.derivative.any() or self.integral.any():
                                    self.output.pop()
                                elif has_dot_function:
                                    self.eq_string = get_uneval_sp_objs(eq_split[0])
                                    self.output.append(f"{custom_latex(self.eq_string)} {equals_sign} {custom_latex(solution, symbol=self.symbol)}")
                                else:
                                    self.output.append(f"\\textrm{{{eq_split[0]}}} {equals_sign} {custom_latex(solution, symbol=self.symbol)}")
                            
                            else:
                                self.output.append(f"\\textrm{{Yep dat is }} {custom_latex(solution, symbol=self.symbol)}")

                        else:
                            if equals_sign == '=' and not sp.N(solution, 9).equals(sp.N(solution, 10)):
                                equals_sign = '\\approx'

                            self.output.append(f"{custom_latex(self.eq_string)} {equals_sign} {custom_latex(solution, symbol=self.symbol)}")

                    elif sp.nsimplify(self.eq1, [sp.pi]).is_number:
                        solution = custom_simplify(self.eq1)
                        if solution != sp.N(solution):
                            self.output.append(f"{custom_latex(self.eq_string)} = {custom_latex(solution)} \\approx {custom_latex(sp.N(solution, 5))}")
                        
                        else:
                            self.output.append(f"{custom_latex(self.eq_string)} = {custom_latex(solution)}")
                        

                    else:
                        self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                        self.output.append(f"{custom_latex(custom_simplify(self.eq1))} = 0")

                        if self.multivariate:
                            self.output.append((f"Geen snijpunt met de x-as gevonden", {"latex":False}))
                        elif self.has_any_solutions:
                            self.output.append(("Geen reële oplossing gevonden", {"latex": False}))
                        else:
                            self.output.append(("Geen oplossing gevonden", {"latex": False}))

                        self.plot = True


                elif len(eq_split) == 2:
                    lhs = sp.nsimplify(self.eq1, [sp.pi, sp.E], rational=False)
                    rhs = sp.nsimplify(self.eq2, [sp.pi, sp.E], rational=False)

                    has_equal_sides = apply_opperator(lhs, self.equation_type, rhs)
                    sides_are_numbers = (lhs.is_number and rhs.is_number)
                    has_solution = has_equal_sides or sides_are_numbers

                    if has_solution:
                        self.output.append((f"Vergelijking:", {"latex": False}))

                    simplify = self.eq1_unsimplified != lhs or self.eq2_unsimplified != rhs
                    if simplify:
                        self.output.append(f"{custom_latex(self.eq1_unsimplified)} {sp_custom.equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2_unsimplified)}")
                        self.output.append((f"Versimpelingen:", {"latex": False}))

                        if self.eq1_unsimplified != lhs:
                            self.output.append(f"\\bullet \\quad {custom_latex(self.eq1_unsimplified)} \\Longrightarrow {custom_latex(lhs)}")
                        if self.eq2_unsimplified != rhs:
                            self.output.append(f"\\bullet \\quad {custom_latex(self.eq2_unsimplified)} \\Longrightarrow {custom_latex(rhs)}")
                    
                    if has_solution:
                        if simplify:
                            self.output.append(("Onze vergelijking wordt dus:", {"latex": False}))

                        self.output.append((f"{custom_latex(lhs)} {sp_custom.equation_type_to_latex(self.equation_type)} {custom_latex(rhs)}"))

                        if has_equal_sides:
                            self.output.append(("Dit is waar, dus deze vergelijking klopt", {"latex": False}))
                        elif sides_are_numbers:
                            self.output.append(("Dit is niet waar, dus deze vergelijking klopt niet", {"latex": False}))

                    else:
                        self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                        self.output.append(f"{custom_latex(self.eq1)} {sp_custom.equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2)}")

                        if self.multivariate:
                            self.output.append((f"Geen snijpunt met de x-as gevonden", {"latex":False}))
                        elif self.has_any_solutions:
                            self.output.append(("Geen reële oplossing gevonden", {"latex": False}))
                        else:
                            self.output.append(("Geen oplossing gevonden", {"latex": False}))

                        self.plot = True

                return self.equation_interpret, self.output, self.plot
            
            if self.solution_set.is_empty:
                return no_solutions_output()
            
        except VectorFieldError:
            vector_operator = "div" if "div" in self.eq_string else "curl"
            self.output.append((f"Error: Argument van `{vector_operator}` moet een vector zijn", {"latex": False}))
            return self.equation_interpret, self.output, self.plot
        
        except ArcReciprocalInvalidDomainError:
            self.output.append((f"Error: Argument van de arc functie mag niet tussen -1 en 1 zijn", {"latex": False}))
            return self.equation_interpret, self.output, self.plot

        except ArcGonioInvalidDomainError:
            self.output.append((f"Error: Argument van de arc functie moet een getal tussen -1 en 1 zijn", {"latex": False}))
            return self.equation_interpret, self.output, self.plot
        except VectorShapeError:
            self.output.append((f"Error: De matrix kan niet omgezet worden naar een vector", {"latex": False}))
            return self.equation_interpret, self.output, self.plot
        except sp.ShapeError:
            self.output.append((f"Error: De dimensies van de matrices komen niet overeen", {"latex": False}))
            return self.equation_interpret, self.output, self.plot


        except (NotImplementedError, TypeError):
            # TypeError from interpretation
            try:
                self.eq12
            except Exception:
                self.output.append((f"ERROR", {"latex":False}))
                traceback.print_exc()
                return self.equation_interpret, self.output, self.plot

            try:
                check_numerical = self.check_solve_numerically(self.solution_set)

                if check_numerical is not None and not self.intersect:
                    return no_solutions_output()
                
                elif check_numerical is not None:
                    self.interval_solutions = self.solution_set = check_numerical

            except Exception:
                self.output.append((f"ERROR", {"latex":False}))
                traceback.print_exc()
                return self.equation_interpret, self.output, self.plot


        except sp.SympifyError:
            self.output.append((f"Error: De ingevoerde functie klopt niet", {"latex":False}))
            traceback.print_exc()
            return self.equation_interpret, self.output, self.plot

        except Exception:
            self.output.append((f"ERROR", {"latex":False}))
            traceback.print_exc()
            return self.equation_interpret, self.output, self.plot

        try:
            self.plot = True
            self.intersect = True
            self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
            self.output.append(f"{custom_latex(self.eq1)} {sp_custom.equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2)}")

            if self.solution_set.is_FiniteSet:
                set_numerical_text()

                if len(self.solution_set) == 1:
                    if self.equation_is_inequality:
                        set_inequatity_solution_output()
                    else:
                        self.output.append((f"De oplossing is:", {"latex":False}) if not self.multivariate else (f"Het snijpunt met de $x$-as is:", {"latex":False}))
                        self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solution_set.args[0])}")
                    
                    if not self.solution_set.args[0].equals(sp.N(self.solution_set.args[0])):
                        self.output[-1] += f" \\approx {sp.N(self.solution_set.args[0], 5)}"
                    
                else:
                    if len(self.solution_set) > 5:
                        solution_array = np.array(list(self.solution_set))
                        self.interval_solutions = solution_array[np.argsort(np.abs(solution_array))][:5]
                    else:
                        self.interval_solutions = self.solution_set
                       
                    if self.equation_is_inequality:
                        set_inequatity_solution_output()
                    else:
                        self.output.append((f"De oplossingen zijn:", {"latex":False}) if not self.multivariate else (f"De snijpunten met de $x$-as zijn:", {"latex":False}))
                        if len(self.solution_set) > 5:
                            self.output[-1] = (f"De eerste 5 oplossingen zijn:", {"latex":False}) if not self.multivariate else (f"De eerste 5 snijpunten met de $x$-as zijn:", {"latex":False})
                            
                        set_count_solutions()
                            
                if not self.domain_is_reals:
                    self.output.append((f"Het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(custom_latex(self.domain))
            
            else:
                if self.equation_is_inequality:
                    set_inequatity_solution_output()
                else:
                    self.output.append((f"De oplossingen zijn:", {"latex":False}) if not self.multivariate else (f"De snijpunten met de $x$-as zijn:", {"latex":False}))
                    self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solution_set, symbol=self.symbol)}")         

                if not self.domain_is_reals:
                    self.output.append((f"Het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(custom_latex(self.domain))

                if not self.equation_is_inequality:
                    self.output.append(("Oplossingen in het domein $[0, 2\\pi]$:", {"latex":False, "new_line":2}) if not self.multivariate else ("Snijpunten in het domein $[0, 2\\pi]$:", {"latex":False, "new_line":2}))

                counter = 0
                self.interval_solutions = []

                if self.solution_set.is_iterable:
                    for solution in self.solution_set:

                        if not solution.is_real:
                            continue
                        
                        if 0 <= sp.N(solution) <= 2 * np.pi:
                            self.interval_solutions.append(solution)
                            continue
                        else:
                            counter += 1

                        if counter > 10:
                            break
                else:
                    self.solution_set = self.solve_numerically()
                    self.interval_solutions = list(self.solution_set)

                    if self.numerical and len(self.roots_numeric) > 5:
                        self.interval_solutions = self.interval_solutions[:5]

                    if not self.equation_is_inequality:
                        self.output = self.output[:-2]
                        if len(self.roots_numeric) == 1:
                            self.output[-1] = (f"Het snijpunt met de $x$-as is:", {"latex":False}) if self.multivariate else (f"De oplossing is:", {"latex":False})
                        set_numerical_text()
                
                self.interval_solutions = sp.FiniteSet(*self.interval_solutions)

                if not self.equation_is_inequality:
                    if self.interval_solutions.is_empty:
                        self.intersect = False
                        self.output = self.output[:-6]
                        self.output.append(("Geen oplossing gevonden", {"latex":False, "new_line":2}) if not self.multivariate else ("Geen snijpunten met de $x$-as gevonden", {"latex":False}))
                        
                        return self.equation_interpret, self.output, self.plot

                    set_count_solutions()

        except Exception:
            self.output.append((f"ERROR", {"latex":False}))
            traceback.print_exc()

        return self.equation_interpret, self.output, self.plot
    

    def get_range(self):
        def no_intersect():
            self.intersect = False
            self.x_range = np.array([-10, 10])
            self.y_range = np.array([-10, 10])
            return self.x_range, self.y_range


        if not self.intersect:
            return no_intersect()

        if self.solution_set.is_FiniteSet and not (self.numerical and len(self.roots_numeric) > 5):
            self.interval_solutions = self.solution_set

        self.interval_solutions = list(self.interval_solutions)
        
        self.x_intersect = np.sort(np.array(sp.Matrix(self.interval_solutions).evalf(), dtype=np.float64))
        self.y_intersect = self.apply_func_to_array(self.eq1_lambda_np, self.x_intersect)

        self.x_intersect = self.x_intersect[np.isreal(self.y_intersect) & np.isfinite(self.y_intersect)]
        self.y_intersect = self.y_intersect[np.isreal(self.y_intersect) & np.isfinite(self.y_intersect)].astype(np.float64)

        self.y_intersect[np.abs(self.y_intersect) < 1e-6] = 0

        if self.x_intersect.size == 0:
            return no_intersect()

        intersect_xrange = np.ptp(self.x_intersect)
        intersect_yrange = np.ptp(self.y_intersect)

        self.x_range_og = np.array((min(self.x_intersect) - (intersect_xrange/3 + 2), max(self.x_intersect) + (intersect_xrange/3 + 2)))
        self.y_range_og = np.array((min(self.y_intersect) - (intersect_yrange/3 + 2), max(self.y_intersect) + (intersect_yrange/3 + 2)))
        
        self.x_range = self.x_range_og
        self.y_range = self.y_range_og

        return self.x_range, self.y_range


    def get_plot_data(self, x_range, dx=0.01):
        if self.multivariate:
            self.eq1 = sp.sympify(0)

        def get_plottable_coords(x_coords, domain_eq1, domain_eq2):

            def get_plottable_xy(np_lambda_func, domain):
                y_coords = np_lambda_func(x_coords_np)
                plottable_x_coords = x_coords_np[np.isreal(y_coords) & np.isfinite(y_coords)].ravel()
                plottable_x_coords = add_important_points(list(plottable_x_coords), np_lambda_func, domain).ravel()

                if plottable_x_coords.size != 0:
                    plottable_x_coords_diff = plottable_x_coords[np.where(np.diff(plottable_x_coords) < 1)]
                    plottable_x_coords = np.append(plottable_x_coords_diff, plottable_x_coords[-1])

                y_coords = self.apply_func_to_array(np_lambda_func, plottable_x_coords)

                return plottable_x_coords, y_coords
            
            def add_important_points(plottable_x_coords, lambda_func, domain):
                if self.intersect:
                    min_plottable_x = min(plottable_x_coords)
                    max_plottable_x = max(plottable_x_coords)
                    for x_intersect in self.x_intersect:
                        if min_plottable_x <= x_intersect <= max_plottable_x:
                            plottable_x_coords.append(x_intersect)
                    
                    plottable_x_coords = sorted(plottable_x_coords)

                return add_endpoint(plottable_x_coords, lambda_func, domain)
            
            def add_endpoint(plottable_x_coords, lambda_func, domain):
                try:    
                    if domain is sp.S.Reals or not domain.is_Interval:
                        return np.array(plottable_x_coords)

                    amt_intervals = len(domain.args) if domain.is_Union else 1
                    for _ in range(amt_intervals):
                        for j in range(2):
                            end_point = domain.args[j].evalf()
                            if end_point.is_finite and np.isfinite(lambda_func(float(end_point))):
                                max_plottable_x_coords = max(plottable_x_coords)
                                min_plottable_x_coords = min(plottable_x_coords)
                                end_point = float(end_point)
            
                                if end_point > max_plottable_x_coords:
                                    plottable_x_coords.extend(list(np.linspace(max_plottable_x_coords - 0.1, end_point, 50)))
                                elif end_point < min_plottable_x_coords:
                                    plottable_x_coords.extend(list(np.linspace(end_point, min_plottable_x_coords + 0.1, 50)))
                    
                    plottable_x_coords = np.sort(plottable_x_coords)
                    plottable_x_coords = plottable_x_coords[(domain.args[0] <= plottable_x_coords) & (plottable_x_coords <= domain.args[1])]

                except Exception:
                    plottable_x_coords = np.sort(plottable_x_coords)

                return plottable_x_coords


            x_coords_np = np.array(x_coords)
            plottable_x1_coords, y1_coords = get_plottable_xy(self.eq1_lambda_np, domain_eq1)
            plottable_x2_coords, y2_coords = get_plottable_xy(self.eq2_lambda_np, domain_eq2)

            return plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords


        if self.vert_asympt_eq is None:
            self.x_coords = get_smooth_x_coords(x_range, dx, self.vert_asympt_eq)

        else:
            if isinstance(self.vert_asympt_eq, list):
                self.vert_asympt = np.array(self.vert_asympt_eq, dtype=np.float64)
            else:
                self.vert_asympt_set = sp.solveset(self.vert_asympt_eq, domain=sp.Interval(*x_range)).evalf()
                if isinstance(self.vert_asympt_set, sp.ConditionSet) and self.vert_asympt_set.condition == self.vert_asympt_eq:
                    self.vert_asympt = np.array(self.solve_numerically(self.vert_asympt_eq, self.get_lambdas(self.vert_asympt_eq, self.symbol, numeric=True)), dtype=np.float64)
                else:
                    self.vert_asympt = np.array(list(self.vert_asympt_set), dtype=np.float64)

            self.vert_asympt = self.vert_asympt[np.isreal(self.vert_asympt)]
            self.x_coords = get_smooth_x_coords(x_range, dx, self.vert_asympt)


        if self.vert_asympt_eq is None:
            if not self.domain_is_reals:
                if not self.multivariate:
                    domain_eq1 = sp.calculus.util.continuous_domain(sp.sympify(self.eq1), self.symbol, domain=sp.S.Reals)
                    domain_eq2 = sp.calculus.util.continuous_domain(sp.sympify(self.eq2), self.symbol, domain=sp.S.Reals)
                else:
                    domain_eq1 = sp.S.Reals
                    domain_eq2 = self.domain

            else:
                domain_eq1 = domain_eq2 = sp.S.Reals

            plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = get_plottable_coords(self.x_coords, domain_eq1, domain_eq2)
            plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = plottable_x1_coords.astype(float), y1_coords.astype(float), plottable_x2_coords.astype(float), y2_coords.astype(float)

        else:
            plottable_x1_coords = []
            plottable_x2_coords = []
            y1_coords = []
            y2_coords = []

            if not self.domain_is_reals:
                domain_eq1 = sp.calculus.util.continuous_domain(sp.N(self.eq1), self.symbol, domain=sp.S.Reals)
                domain_eq2 = sp.calculus.util.continuous_domain(sp.N(self.eq2), self.symbol, domain=sp.S.Reals)
            else:
                domain_eq1 = domain_eq2 = sp.S.Reals

            for x_coord in self.x_coords:
                plottable_x1_coords_i, y1_coords_i, plottable_x2_coords_i, y2_coords_i = get_plottable_coords(x_coord, domain_eq1, domain_eq2)

                plottable_x1_coords.append(plottable_x1_coords_i)
                plottable_x2_coords.append(plottable_x2_coords_i)
                y1_coords.append(y1_coords_i)
                y2_coords.append(y2_coords_i)

        return list(plottable_x1_coords), list(y1_coords), list(plottable_x2_coords), list(y2_coords)


    def solve_vector(self, eq_split):
        if len(eq_split) == 1:
            try:
                eq_string_sp = self.eq_string
                try:
                    eq_string_sp = get_uneval_sp_objs(self.eq_string)
                except AttributeError:
                    eq_string_sp = sp.sympify(self.eq_string, locals=self.locals)

                if eq_string_sp == self.eq1:
                    eq_string_sp = sp.sympify(self.eq_string, locals=self.locals, evaluate=False)
            except Exception:
                traceback.print_exc()

            self.eq1 = self.eq1.doit()

            self.output.append((f"{custom_latex(eq_string_sp, vect_dim=self.vect_dim)} = {custom_latex(self.eq1, vect_dim=self.vect_dim)}"))
            return self.equation_interpret, self.output, self.plot
        

        lhs = self.eq1.simplify()
        rhs = self.eq2.simplify()

        if not isinstance(lhs, (CustomVector, sp_vector.Vector)):
            lhs = convert_symbols_for_vector(lhs)
        if not isinstance(rhs, (CustomVector, sp_vector.Vector)):
            rhs = convert_symbols_for_vector(rhs)

        has_equal_sides = apply_opperator(lhs, self.equation_type, rhs)
        
        if isinstance(lhs, CustomVector) and isinstance(rhs, CustomVector):
            sides_are_numbers = (lhs.contain_only_numbers and rhs.contain_only_numbers)
        else:
            sides_are_numbers = (lhs.is_number and rhs.is_number)

        different_types = (isinstance(lhs, CustomVector)) ^ (isinstance(rhs, CustomVector))

        try:
            has_solution = has_equal_sides or sides_are_numbers or different_types
        except TypeError:
            has_solution = False

        if self.eq1_unsimplified == self.eq1:
            self.eq1_unsimplified = get_uneval_sp_objs(eq_split[0])
            
        if self.eq2_unsimplified != rhs:
            self.eq2_unsimplified = get_uneval_sp_objs(eq_split[1])

        if has_solution:
            self.output.append((f"Vergelijking:", {"latex": False}))

        simplify = self.eq1_unsimplified != lhs or self.eq2_unsimplified != rhs
        if simplify:
            self.output.append(f"{custom_latex(self.eq1_unsimplified)} {sp_custom.equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2_unsimplified)}")
            self.output.append((f"Versimpelingen:", {"latex": False}))

            if self.eq1_unsimplified != lhs:
                self.output.append(f"\\bullet \\quad {custom_latex(self.eq1_unsimplified)} \\Longrightarrow {custom_latex(lhs)}")
            if self.eq2_unsimplified != rhs:
                self.output.append(f"\\bullet \\quad {custom_latex(self.eq2_unsimplified)} \\Longrightarrow {custom_latex(rhs)}")
        
        if has_solution:
            if simplify:
                self.output.append(("Onze vergelijking wordt dus:", {"latex": False}))

            self.output.append((f"{custom_latex(lhs)} {sp_custom.equation_type_to_latex(self.equation_type)} {custom_latex(rhs)}"))

            if has_equal_sides:
                self.output.append(("Dit is waar, dus deze vergelijking klopt", {"latex": False}))
            elif sides_are_numbers:
                self.output.append(("Dit is niet waar, dus deze vergelijking klopt niet", {"latex": False}))
            elif different_types:
                self.output.append(("Dit is niet waar: de een is een vector, de ander is een getal", {"latex": False}))

        else:
            self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
            self.output.append(f"{custom_latex(lhs)} {sp_custom.equation_type_to_latex(self.equation_type)} {custom_latex(rhs)}")
            self.output.append(("Geen oplossing gevonden", {"latex": False}))

        return self.equation_interpret, self.output, self.plot
    
    def process_system_of_eq(self, eq_strings):
        equation_symbols = ["!=", ">=", "<=", "==", "=", ">", "<"]
        eq_strings = self.eq_string.split(";")
        eq_strings = [eq_string for eq_string in eq_strings if eq_string.strip()]
        eqs = []
        for eq_string in eq_strings:
            eq_split = split_equation(eq_string)
            eq_split = [string for string in eq_split if string not in equation_symbols]
            eqs.append(self.set_eqs(eq_split, use_self=False))

        return eqs
    
    def make_symbols_real(self, eq):
        symbols = eq.free_symbols
        for symbol in symbols:
            if symbol.name != "circ":
                eq = eq.subs(symbol, sp.symbols(symbol.name, real=True))

        return eq
    
    def make_eqs_real(self, eqs):
        for i in range(len(eqs)):
            for j in range(len(eqs[i])):
                eqs[i][j] = self.make_symbols_real(eqs[i][j])

        return eqs

    @staticmethod
    def convert_sol_list_to_dict(solution: list[dict]) -> dict:
        new_solution_dict = {}
        for solution_dict in solution:
            for key, value in solution_dict.items():
                if key in new_solution_dict:
                    if isinstance(new_solution_dict[key], list) and value not in new_solution_dict[key]:
                        new_solution_dict[key].append(value)

                    elif new_solution_dict[key] != value:
                        new_solution_dict[key] = [new_solution_dict[key]] + [value]
                else:
                    new_solution_dict[key] = value

        return new_solution_dict

    
    @staticmethod
    def order_equations_by_complexity(sp_equations: list[sp.Expr]) -> list[sp.Expr]:
        def get_amt_symbols(equation: sp.Expr) -> int:
            return len(equation.free_symbols)
        
        def get_function_compexity(equation: sp.Expr) -> int:
            return sp.count_ops(equation)
        
        def quantize_function_order(equation: sp.Expr) -> float:
            return get_amt_symbols(equation) + get_function_compexity(equation)/10

        return sorted(sp_equations, key=quantize_function_order)
    
    @staticmethod
    def get_least_used_symbol(equation: sp.Expr) -> sp.Symbol:
        equation_str = str(equation)
        least_used_symbol = None
        least_used_amt = float("inf")
        for symbol in equation.free_symbols:
            amt_symbol = equation_str.count(symbol.name)
            if amt_symbol < least_used_amt:
                least_used_amt = amt_symbol
                least_used_symbol = symbol

        return least_used_symbol

    @staticmethod
    def get_least_complex_substitution(equation: sp.Expr) -> tuple[sp.Symbol, list[sp.Expr]]:
        substitution_eqs_dict: dict[tuple[sp.Expr], sp.Symbol] = {}
        for symbol in equation.free_symbols:
            try:
                substitution = tuple(sp.solve(equation, symbol))
                substitution_eqs_dict[substitution] = symbol
            except NotImplementedError:
                continue

        def count_combined_ops(substitution: sp.Expr) -> int:
            return sum(sp.count_ops(eq) for eq in substitution)

        substitution_eqs_all_symbols: list[list[sp.Expr]] = [list(eq) for eq in substitution_eqs_dict]
        substitution_eqs_all_symbols = [eq for eq in substitution_eqs_all_symbols if eq != []]
        substitution_eqs_all_symbols = sorted(substitution_eqs_all_symbols, key=len)
        substitution_eqs_all_symbols = [eq for eq in substitution_eqs_all_symbols if len(eq) == len(substitution_eqs_all_symbols[0])]
        substitution_eqs_all_symbols = sorted(substitution_eqs_all_symbols, key=count_combined_ops)

        if len(substitution_eqs_all_symbols) > 1:
            # sorted by name to remove random aspect
            substitution_eqs_all_symbols = sorted(substitution_eqs_all_symbols, key=lambda x: substitution_eqs_dict[tuple(x)].name, reverse=True)
            substitution_eqs_symbol = substitution_eqs_all_symbols[0]

        else:
            substitution_eqs_symbol = substitution_eqs_all_symbols[0]
        symbol = substitution_eqs_dict[tuple(substitution_eqs_symbol)]
        return symbol, substitution_eqs_symbol
    
    @staticmethod
    def substitute_symbol_equation(rewritten_eqs: dict[sp.Symbol, sp.Expr], sp_equations: list[sp.Expr], current_equation: sp.Expr) -> list[sp.Expr]:
        for symbol, equations in rewritten_eqs.items():
            for i, sp_equation in enumerate(sp_equations.copy()):
                for j, substitution in enumerate(equations):
                    # don't substitute the equation with itself
                    new_sp_equation = sp.simplify(sp_equation.subs(symbol, substitution), inverse=True)
                    if new_sp_equation in SYMPY_BOOLEANS + (sp.true, sp.false):
                        continue
                    
                    # add any extra versions as an equation. For example:
                    # x^2 + y^2 = 1 --> y = -sqrt(1 - x^2) AND y = sqrt(1 - x^2)
                    if j == 0:
                        sp_equations[i] = new_sp_equation
                    else:
                        new_sp_equation = new_sp_equation
                        if any(equivalent_eq(new_sp_equation, eq) for eq in sp_equations):
                            continue

                        sp_equations.append(new_sp_equation)

        sp_equations = unique_equivalent_eqs(sp_equations)
        return sp_equations
    
    @staticmethod
    def substitute_symbol_value(sp_equations: list[sp.Expr], symbol: sp.Symbol, value: float) -> list[sp.Expr]:
        og_sp_equations = sp_equations.copy()
        for i, equation in enumerate(og_sp_equations):
            sp_equations[i] = equation.subs(symbol, value)

        sp_equations = [eq for eq in sp_equations if not isinstance(eq, SYMPY_BOOLEANS)]
        return sp_equations

    def rewrite_system_into_single_variable_eqs(self, sp_equations: list[sp.Expr], recursion_count: int=0) -> list[sp.Expr]:
        sp_equations = self.order_equations_by_complexity(sp_equations)
        prev_sp_equations = sp_equations.copy()
        rewritten_eqs = {}
        for equation in sp_equations.copy():
            if len(equation.free_symbols) == 1:
                continue
            try:
                symbol, substitutions = self.get_least_complex_substitution(equation)
                if symbol not in rewritten_eqs:
                    rewritten_eqs[symbol] = substitutions
                else:
                    substitutions = [sub for sub in substitutions if sub not in rewritten_eqs[symbol]]
                    rewritten_eqs[symbol] += substitutions
            except NotImplementedError:
                    continue

            sp_equations = self.substitute_symbol_equation(rewritten_eqs, sp_equations, equation)

        if len(sp_equations) != 0 and any(len(eq.free_symbols) > 1 for eq in sp_equations) and recursion_count < 10 and prev_sp_equations != sp_equations:
            return self.rewrite_system_into_single_variable_eqs(sp_equations, recursion_count + 1)
        
        sp_equations = unique_equivalent_eqs(sp_equations)

        return sp_equations
    

    def solve_system_of_eq_numerically(self, sp_equations, solutions: dict[sp.Symbol, list[float]]|None=None) -> dict[sp.Symbol, list[float]]:
        sp_equations = self.rewrite_system_into_single_variable_eqs(sp_equations)
        if solutions is None:
            solutions = {}
        
        for equation in sp_equations:
            if len(equation.free_symbols) == 1:
                symbol = list(equation.free_symbols)[0]
                prior_symbol_solution = solutions.get(symbol, [])

                try:
                    solutions[symbol] = prior_symbol_solution + [sol for sol in sp.solve(equation) if sol not in prior_symbol_solution]
                    if not solutions[symbol]:
                        raise NotImplementedError
                
                except NotImplementedError:
                    self.symbol = symbol # necessary for solve_numerically
                    equation = equation.lhs - equation.rhs
                    solutions[symbol] = prior_symbol_solution + [sol for sol in self.solve_numerically(equation, self.get_lambdas(equation, symbol, numeric=True)) if sol not in prior_symbol_solution]
        
        og_solutions = solutions.copy()
        for symbol, values in og_solutions.items():
            og_sp_equations = sp_equations.copy()
            for value in values:
                sp_equations = og_sp_equations.copy()

                if sp_equations == []:
                    return solutions
                
                sp_equations = self.substitute_symbol_value(sp_equations, symbol, value)
                if og_sp_equations == sp_equations:
                    continue

                solutions = self.solve_system_of_eq_numerically(sp_equations, solutions)

        return solutions
    
    @staticmethod
    def remove_extra_solutions(solutions: dict[sp.Symbol, list[float]]) -> dict[sp.Symbol, list[float]]:
        if not solutions:
            return solutions
        
        solutions_count = [len(solutions[symbol]) for symbol in solutions]
        min_solutions = min(solutions_count)
        if min_solutions == 0:
            min_solutions = 1
        
        solutions = {symbol: solutions[symbol][:min_solutions] for symbol in solutions}
        return solutions
    
    def add_missing_solutions(self, solutions: dict[sp.Symbol, list[float]]) -> dict[sp.Symbol, list[float]]:
        solution_pairs: list[dict[sp.Symbol, float]] = transform_dict_list_to_list_dict(solutions)
        for solution_pair in solution_pairs:
            sp_equations = self.og_sp_equations.copy()

            for symbol, value in solution_pair.items():
                sp_equations = self.substitute_symbol_value(sp_equations, symbol, value)

            sp_equations = [eq for eq in sp_equations if not isinstance(eq, SYMPY_BOOLEANS)]
            if not sp_equations:
                continue

            new_symbol = self.get_least_used_symbol(sp_equations[0])
            new_symbol_solutions: list[list[sp.Number]] = [
                set(round_list_val_with_symbolic(sp.solve(equation, new_symbol))) for equation in sp_equations
            ]
            new_symbol_solutions = [sol for sol in new_symbol_solutions if sol] # remove empty solutions
            if not new_symbol_solutions:
                continue
            
            new_symbol_valid_solutions = new_symbol_solutions[0]
            for sol_set in new_symbol_solutions:
                if all(sp.N(sol).is_number for sol in sol_set):
                    new_symbol_solutions = new_symbol_valid_solutions.intersection(sol_set)
            
            if not new_symbol_solutions:
                continue

            new_symbol_solutions = list(new_symbol_solutions)
            if new_symbol in solutions:
                solutions[new_symbol] += new_symbol_solutions
            else:
                solutions[new_symbol] = new_symbol_solutions
        
        return solutions


    def check_solution(self, symbol: sp.Symbol, solution: float, other_solution_dict: dict[sp.Symbol, float]) -> bool:
        """
        Checks if a symbol value with a given combination of other symbol values
        satisfies all equations. True if all equations give True, False otherwise

        Args:
            symbol (sp.Symbol): Symbol to check
            solution (float): Found solution value for the given symbol
            other_solution_dict (dict[sp.Symbol, float]): A given combination of other symbols and their values

        Returns:
            bool: True if all equations are satisfied with the given combination, false otherwise
        """
        for equation in self.og_sp_equations:
            equation = equation.lhs - equation.rhs
            equation = equation.subs(symbol, solution)
            for other_symbol, other_solution in other_solution_dict.items():
                if symbol == other_symbol:
                    continue

                equation = equation.subs(other_symbol, other_solution)

            if sp.Abs(sp.N(equation)) > 1e-5:
                return False

        return True

    @staticmethod
    def get_all_combinations_of_solutions(solutions: dict[sp.Symbol, list[float]]) -> list[dict[sp.Symbol, float]]:
        all_combinations = [
            {key: value for key, value in zip(solutions.keys(), values)}
            for values in itertools.product(*solutions.values())
        ]
        return all_combinations

    def remove_invalid_solutions(self, solutions: dict[sp.Symbol, list[float]]) -> dict[sp.Symbol, list[sp.Number]]:
        solutions_copy = deepcopy(solutions)
        for symbol, symbol_solutions in solutions_copy.items():
            other_solution_copy = deepcopy(solutions_copy)
            other_solution_copy.pop(symbol, None)
            remove_symbol_sol = True
            for symbol_sol in symbol_solutions:
                for other_solution_dict in self.get_all_combinations_of_solutions(other_solution_copy):
                    if self.check_solution(symbol, symbol_sol, other_solution_dict):
                        remove_symbol_sol = False
                
                if remove_symbol_sol:
                    solutions[symbol].remove(symbol_sol)

        return solutions
    
    @staticmethod
    def remove_duplicate_solutions(solutions: dict[sp.Symbol, list[float]]) -> dict[sp.Symbol, list[sp.Number]]:
        for symbol in solutions:
            solutions[symbol] = round_list_val_with_symbolic(solutions[symbol])
            solutions[symbol] = unique_preserve_order(solutions[symbol])
        return solutions
    

    def validate_numeric_solutions(self, solutions: dict[sp.Symbol, list[float]]) -> dict[sp.Symbol, list[sp.Number]]:
        solutions = self.remove_extra_solutions(solutions)

        all_symbols = set(symbol for equation in self.og_sp_equations for symbol in equation.free_symbols)
        for _ in range(len(all_symbols) - len(solutions)):
            solutions = self.add_missing_solutions(solutions)

        solutions = self.remove_invalid_solutions(solutions)
        solutions = self.remove_duplicate_solutions(solutions)
        return solutions

    def solve_system_of_eq(self):
        self.processed_eqs = self.process_system_of_eq(eq_strings=self.eq_string)
        self.processed_eqs = [list(eqs) for eqs in self.processed_eqs]
        self.processed_eqs = self.make_eqs_real(self.processed_eqs)

        sp_equations = [eq[3] for eq in self.processed_eqs]
        self.output.append((f"Stelsel van Vergelijkingen:", {"latex": False}))
        eq_strings = [f"{custom_latex(eq[0])} = {custom_latex(eq[1])}" for eq in self.processed_eqs]
        system_eq_string = r"\begin{cases} " + r" \\[4pt] ".join(eq_strings) + r" \end{cases}"
        self.output.append(system_eq_string)

        try:
            solutions = sp.solve(sp_equations)
            if not solutions:
                raise NotImplementedError
            
            self.numerical = False
        except NotImplementedError:
            self.og_sp_equations = sp_equations 
            solutions = self.solve_system_of_eq_numerically(sp_equations)
            solutions = self.validate_numeric_solutions(solutions)
            self.numerical = True
        
        if not solutions or (isinstance(solutions, dict) and all(sol == [] for sol in solutions.values())):
            self.output.append((f"Geen oplossing gevonden", {"latex": False}))
            return self.equation_interpret, self.output, self.plot
        
        if isinstance(solutions, list):
            solutions = self.convert_sol_list_to_dict(solutions)

        # sort solutions alphabetically
        solutions = {symbol: solutions[symbol] for symbol in sorted(solutions, key=lambda symbol: symbol.name)}

        solution_strings = []
        for key, value in solutions.items():
            solution_string_parts = []
            if isinstance(value, list):
                for val in value:
                    solution_string_parts.append(f"{custom_latex(key)} = {custom_latex(val)}")
            else:
                solution_string_parts.append(f"{custom_latex(key)} = {custom_latex(value)}")
            
            solution_string = f' \\ \\vee \\ '.join(solution_string_parts)
            solution_strings.append(solution_string)

        if len(solution_strings) == 1:
            if self.numerical:
                self.output.append((f"(Oplossing is numeriek bepaald)", {"latex": False}))

            self.output.append((f"Oplossing:", {"latex": False}))
            solution_str = solution_strings[0]
        else:
            if self.numerical:
                self.output.append((f"(Oplossingen zijn numeriek bepaald)", {"latex": False}))

            self.output.append((f"Oplossingen:", {"latex": False}))
            solution_str = r"\begin{cases} " + r" \\[4pt]".join(solution_strings) + r" \end{cases}"

        self.output.append(solution_str)

        return self.equation_interpret, self.output, self.plot