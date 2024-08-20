import numpy as np
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
from sympy.printing.latex import LatexPrinter
import regex as re
from scipy.optimize import fsolve, bisect, newton
from warnings import filterwarnings
from src.Solver.src.solver.math_parser import add_args_to_func, math_interpreter, get_uneval_sp_objs
import traceback
import typing
from types import FunctionType
from collections.abc import Iterable
from numbers import Number

filterwarnings("ignore", category=RuntimeWarning)

def segmented_linspace(start: float, end: float, breakpoints: typing.Iterable[float], num: int=10, dx: float=0.01) -> typing.List[np.ndarray]:
    """
    Generate a list of linearly spaced segments between `start` and `end`, divided by `breakpoints`.

    Args:
        start (float): The starting point of the range.
        end (float): The ending point of the range.
        breakpoints (Iterable[float]): Points at which the range is divided into segments.
        num (int): Number of points in each segment (default is 10).
        dx (float): Small offset added to the start and end of each segment (default is 0.01).

    Returns:
        List[np.ndarray]: A list of numpy arrays, each containing a segment of linearly spaced points.
    """

    all_points = sorted([start] + list(breakpoints) + [end])
    return [np.linspace(all_points[i] + dx, all_points[i+1] - dx, num) for i in range(len(all_points)-1)]

def write_as_sin_and_cos(x):
    """
    Write sec-csc and tan-cot in terms of cos-sin.

    Args:
        expr (sp.Basic): The SymPy expression to simplify.

    Returns:
        sp.Basic: The simplified SymPy expression.
    """

    return TR1(TR2(x))

def pop_iterable(pop_list: list, index_list: typing.Iterable[int]) -> list:
    """
    Remove elements from `pop_list` at the specified indices.

    Args:
        pop_list (list): The list from which elements will be removed.
        index_list (Iterable[int]): List of indices to remove from `pop_list`.

    Returns:
        list: The list after the specified elements have been removed.
    """

    for index in sorted(index_list, reverse=True):
        pop_list.pop(index)
    return pop_list


class CustomLatexPrinter(LatexPrinter):
    """
    A custom LaTeX printer that provides customized formatting for SymPy expressions.
    """
    real_root = False
    eq1 = eq2 = eq12 = eq = None

    def _print_Mul(self, expr: sp.Mul, **kwargs) -> str:

        """
        Customize the printing of multiplication expressions, especially for logarithmic functions.

        Args:
            expr (sp.Mul): The multiplication expression to print.

        Returns:
            str: The LaTeX representation of the multiplication expression.
        """

        numer, denom = expr.as_numer_denom()

        # Custom handling for logarithms
        if isinstance(numer, sp.log) and isinstance(denom, sp.log):
            arg = numer.args[0]
            base = denom.args[0]

            if isinstance(base, sp.Number):
                arg = self._print(numer)
                base = self._print(base)

                return f' \\ ^{{{base}}} \\! \\log\\left({arg} \\right)'

        # Default handling with custom modifications
        result = super()._print_Mul(expr).replace("1 \\cdot", " ")
        result = re.sub(r"\\left\(-(\d+)\\right\) ", r"- \1 \\cdot", result)
        return result
    

    def _print_Pow(self, expr: sp.Pow, **kwargs) -> str:
        """
        Customize the printing of power expressions.

        Args:
            expr (sp.Pow): The power expression to print.

        Returns:
            str: The LaTeX representation of the power expression.
        """

        base, exp = expr.as_base_exp()

        if expr.is_Rational and exp.q != 1 and expr != sp.root(base, 1/exp, evaluate=False):
            base = self._print(base)
            exp = self._print(sp.simplify(exp))
            return f"{base}^{{{exp}}}"

        elif expr.as_numer_denom()[1] != 1:
            expr = sp.nsimplify(expr)
            return sp.latex(expr)
        

        return sp.latex(expr).replace("log", "ln")

    def _print_log(self, expr: sp.log, **kwargs) -> str:
        """
        Customize the printing of logarithmic expressions.

        Args:
            expr (sp.log): The logarithmic expression to print.

        Returns:
            str: The LaTeX representation of the logarithmic expression.
        """

        arg = self._print(expr.args[0])

        # Natural logarithm
        if len(expr.args) == 1:
            return f'\\ln \\left({arg} \\right)'
        
        # Logarithm with a specific base
        elif len(expr.args) == 2:
            base = self._print(expr.args[1])
            return f' \\ ^{{{base}}} \\! \\log\\left({arg} \\right)'
            
        # Fallback for unexpected cases
        return super()._print_log(expr)
        

    def _print_Limit(self, expr: sp.Limit, **kwargs) -> str:
        """
        Customize the printing of limit expressions.

        Args:
            expr (sp.Limit): The limit expression to print.

        Returns:
            str: The LaTeX representation of the limit expression.
        """

        func, var, point, direction = expr.args
        limit_expr = str(expr)
        limit_value = sp.simplify(expr)

        if str(direction) == "+":
            limit_expr_opposite = limit_expr.replace("dir='+'", "dir='-'")
        else:
            limit_expr_opposite = limit_expr.replace("dir='-'", "dir='+'")
        
        limit_value_opposite = sp.simplify(limit_expr_opposite)


        if limit_value == limit_value_opposite:
            return f"\\lim_{{{self._print(var)} \\, \\to \\, {self._print(point)}}} {self._print(func)}"
        
        elif str(direction) == "+":
            return f"\\lim_{{{self._print(var)} \\, \\downarrow \\, {self._print(point)}}} {self._print(func)}"
        
        elif str(direction) == "-":
            return f"\\lim_{{{self._print(var)} \\, \\uparrow \\, {self._print(point)}}} {self._print(func)}"

        # Fallback just in case
        return super()._print_Limit(expr)
    
    
    def _print_Function(self, expr: sp.Function, **kwargs) -> str:
        """
        Customize the printing of specific mathematical functions.

        Args:
            expr (sp.Function): The function expression to print.

        Returns:
            str: The LaTeX representation of the function expression.
        """

        func_name = expr.func.__name__
        func_map = {
            'asin': '\\arcsin',
            'acos': '\\arccos',
            'atan': '\\arctan',
            'asec': '\\arcsec',
            'acsc': '\\arccsc',
            'acot': '\\arccot',
        }

        if func_name in func_map:
            return rf'{func_map[func_name]}{{\left({self._print(expr.args[0])}\right)}}'
        
        return super()._print_Function(expr, **kwargs)
    
    @classmethod
    def set_real_root(cls, real_root: bool):
        cls.real_root = real_root


def custom_latex(expr: sp.Basic, **kwargs) -> str:
    """
    Convert a SymPy expression to a custom LaTeX representation.

    Args:
        expr (sp.Basic): The SymPy expression to convert.

    Returns:
        str: The LaTeX representation of the expression.
    """
    if CustomLatexPrinter.real_root and sp.sympify(expr).is_Piecewise:
        expr = expr.args[1][0]
        expr = sp.sympify(re.sub(r"\bAbs\b", "", str(expr)))

    return CustomLatexPrinter(**kwargs).doprint(expr)

def custom_simplify(expr: typing.Union[sp.Basic, Number]) -> typing.Union[sp.Basic, Number]:
    """
    Simplify a SymPy expression with custom logic.

    Args:
        expr: The expression to simplify.

    Returns:
        sp.Basic: The simplified expression, or the original expression if simplification fails.
    """
    if not isinstance(expr, sp.Basic):
        return expr

    if expr.is_number:
        return sp.nsimplify(expr)

    try:
        symp_expr = sp.simplify(expr)
        return sp.expand_log(symp_expr)
    except Exception:
        pass

    try:
        return symp_expr
    except UnboundLocalError:
        return expr


class Solve:
    def __init__(self, input_string: str) -> None:
        """
        Initializes the Solve class with the input equation string.

        Args:
            input_string (str): A string representing the equation to solve.
        """

        self.symbol = None
        self.solution_set = None
        self.has_any_solutions = False
        self.interval_solutions = None
        self.vert_asympt = None
        self.vert_asympt_eq = None
        self.eq_string = math_interpreter(input_string)
        self.output = []
        self.equation_interpret = self.eq_string
        self.plot = False
        self.intersect = False
        self.numerical = False
        self.multivariate = False
        self.derivative = False
        self.integral = False
        self.real_root = False

    @staticmethod
    def get_lambdas(expr: typing.Union[sp.Expr, typing.Iterable[sp.Expr]], symbol: sp.Symbol, numeric: bool = False) -> typing.Union[FunctionType, typing.Iterable[FunctionType]]:
        def get_lambda_numeric(single_expr, modules = ["numpy", "scipy", "sympy"]):
            for module in modules:
                try:
                    return sp.lambdify(symbol, single_expr, module)
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
        obj = func(array)
        if np.isscalar(obj):
            return np.full(array.shape, obj).astype(float)
        return obj.astype(float)
            

    def numerical_roots(
        self,
        eq_sp: sp.Expr,
        eq_lambda_np: FunctionType,
        a: float = -10000,
        b: float = 10000,
        dx: float = 0.01,
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
            eq_diff_lambda_np = self.get_lambdas(sp.diff(eq_sp, self.symbol), self.symbol, numeric=True)
        
        x_vals = np.linspace(a, b, (b-a) * int(1/dx))
        y_vals = eq_lambda_np(x_vals)
        xy = np.vstack((x_vals, y_vals)).T
        xy = xy[~np.isnan(xy[:,1]) & ~np.isinf(xy[:,1])]

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
        
        return sp.FiniteSet(*self.roots_numeric)


    def check_solve_numerically(self, solution_set) -> typing.Optional[sp.FiniteSet]:
        """
        Checks if the equation's solutions need to be solved numerically, and does so if necessary.

        Returns:
            Optional[sp.FiniteSet]: A set of the numerical solutions, or None if not applicable.
        """

        if isinstance(solution_set, sp.ConditionSet) and solution_set.condition == self.eq:
            return self.solve_numerically()
                    


    def solve_equation(self) -> typing.Tuple[str, typing.List[typing.Tuple[str, dict]], bool]:
        """Solve the equation, analyze it, and display the results.

        Returns:
            A tuple containing:
            - The interpreted equation string.
            - A list of output messages.
            - A boolean indicating whether to plot the results.
        """
        def make_froot_real(string):
            if "root" not in string and "cbrt" not in string:
                return string
            
            CustomLatexPrinter.set_real_root(True)
            self.real_root = True

            string = re.sub(r"\broot\b", "real_root", string)
            string = re.sub(r"\bcbrt\b", "real_root", string)
            string = add_args_to_func(string, func_name='real_root', replace_with='3')

            return string


        def process_equation(eq_str: str) -> sp.Basic:
            try:
                return TR111(sp.sympify(eq_str)).doit()
            except ValueError:
                eq_str = add_args_to_func(eq_str, func_name="integrate", replace_with="x").replace(".integrate()", ".integrate(x)")
                return TR111(sp.sympify(eq_str)).doit()

        def get_self_eq(eq1, eq2):
            try:
                return sp.nsimplify(sp.Eq(eq1, eq2), tolerance=1e-7)
            except AttributeError:
                return sp.Eq(eq1, eq2)
            
        def set_eqs(eq_split, use_self=True):
            eq1 = process_equation(eq_split[0])

            if len(eq_split) == 1:
                eq2 = 0
            elif len(eq_split) == 2:
                eq2 = process_equation(eq_split[1])
            elif use_self:
                self.output.append(("Error: Meer dan 1 '='-teken ", {"latex": False}))
                return self.equation_interpret, self.output, self.plot 
            
            eq12 = eq1 - eq2
            eq = get_self_eq(eq1, eq2)

            if not use_self:
                return eq1, eq2, eq12, eq
            
            self.eq1, self.eq2, self.eq12, self.eq = eq1, eq2, eq12, eq

            if len(eq_split) == 2:
                self.eq_string = str(self.eq)

            

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
                    self.eq = get_self_eq(0, self.eq2)
                    free_symbols.remove(y_symbol)
                    eq_split = (str(y_symbol), str(self.eq2))

                return eq_split
        
        def set_real_symbol():
            self.symbol = free_symbols.pop()
            symbol_new = sp.symbols(str(self.symbol), real=True)
            self.eq = self.eq.subs(self.symbol, symbol_new)
            self.eq1 = self.eq1.subs(self.symbol, symbol_new)
            self.symbol = symbol_new
        
        def no_solutions_output():
            self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
            self.output.append(f"{custom_latex(self.eq1)} = {custom_latex(self.eq2)}")

            self.plot = True
            if self.multivariate:
                self.output.append((f"Geen snijpunt met de x-as gevonden", {"latex":False}))
            else:
                self.output.append(("Geen oplossing gevonden", {"latex": False}))
            return self.equation_interpret, self.output, self.plot
        
        def set_count_solutions():
            is_numerical = lambda solution: solution == sp.N(solution)
            has_many_decimals = lambda solution: round(sp.N(solution), 9) == round(sp.N(solution), 10)
            equals_sign = lambda solution: "=" if not is_numerical(solution) or has_many_decimals(solution) else "\\approx"
            
            interval_solutions = [sp.nsimplify(solution, [sp.pi, sp.E], rational=False) for solution in self.interval_solutions]
            if len(self.interval_solutions) == 1:
                solution = interval_solutions[0]
                self.output.append(f"{custom_latex(self.symbol)} {equals_sign(solution)} {custom_latex(solution)}")
                if not is_numerical(solution):
                    self.output[-1] += f" \\approx {round(sp.N(solution), 5)}"
                return
            
            counter = 0
            for solution in interval_solutions:
                counter += 1

                self.output.append(f"{counter}) \\quad {custom_latex(self.symbol)} {equals_sign(solution)} {custom_latex(solution)}")
                if not is_numerical(solution):
                    self.output[-1] += f" \\approx {round(sp.N(solution), 5)}"


        def set_numerical_text():
            if self.numerical:
                if len(self.roots_numeric) == 1:
                    self.output.append(("(Oplossing is numeriek bepaald)", {"latex":False, "new_line":2}))
                else:
                    self.output.append(("(Oplossingen zijn numeriek bepaald)", {"latex":False, "new_line":2}))

        try:
            eq_split = make_froot_real(self.eq_string).split("=")
            
            set_eqs(eq_split=eq_split)

            free_symbols = list(self.eq12.free_symbols)
            if free_symbols:
                new_eq_spit = check_multivariate()
                if new_eq_spit:
                    eq_split = new_eq_spit

                if len(free_symbols) >= 2:
                    self.output.append(("Error: Meer dan 1 variabele", {"latex": False}))
                    return self.equation_interpret, self.output, self.plot
                
                set_real_symbol()

                eqs = [self.eq1, self.eq2, self.eq12]
                self.eq1, self.eq2, self.eq12 = [custom_simplify(eq) for eq in eqs]
                self.eq1_lambda, self.eq2_lambda, self.eq12_lambda = self.get_lambdas(eqs, symbol=self.symbol)
                self.eq1_lambda_np, self.eq2_lambda_np, self.eq12_lambda_np = self.get_lambdas(eqs, symbol=self.symbol, numeric=True)
                if self.multivariate:
                    self.eq1_lambda = self.eq1_lambda_np = lambda _: 0


                if len(eq_split) == 1 and not (isinstance(self.eq1, Number) or self.eq1.is_number):
                    self.equation_interpret = f"{self.eq_string} = 0"            

            self.derivative = np.array(["diff" in string for string in eq_split])
            if self.derivative.any():
                symbol = self.symbol or "x"

                if len(eq_split) == 2 and self.derivative.all():
                    self.output.append(("De afgeleide van de functies zijn:", {"latex": False}))
                else:
                    self.output.append(("De afgeleide van de functie is:", {"latex": False}))

                if self.derivative[0]:
                    derivative = get_uneval_sp_objs(eq_split[0])
                    self.output.append(f"f'({symbol}) = {custom_latex(derivative)} = {custom_latex(self.eq1)}")

                if len(eq_split) == 2 and self.derivative[1]:
                    derivative = get_uneval_sp_objs(eq_split[1])
                    self.output.append(f"g'({symbol}) = {custom_latex(derivative)} = {custom_latex(self.eq2)}")


            self.integral = np.array(["integrate" in string for string in eq_split])
            if self.integral.any():
                symbol = self.symbol or "x"

                if len(eq_split) == 2 and self.integral[0] and self.integral[1]:
                    self.output.append(("De primitieven van de functies zijn:", {"latex": False}))
                else:
                    self.output.append(("De primitieve van de functie is:", {"latex": False}))

                if self.integral[0]:
                    if self.derivative[0] and len(eq_split) == 2 and self.derivative[1]:
                        self.output[0] = ("De primitieve en afgeleide van de functies zijn:", {"latex": False})
                        self.output = pop_iterable(self.output, (1,3))
                    elif self.derivative[0]:
                        self.output[0] = ("De primitieve en afgeleide van de functie is:", {"latex": False})
                        pop_iterable(self.output, (1,2))


                    if self.eq1.is_number:
                        integral = get_uneval_sp_objs(eq_split[0])
                        self.output.append(f"I = {custom_latex(integral)} = {custom_latex(self.eq1)}")
                    
                    else:
                        self.output.append(f"F({symbol}) = {custom_latex(self.eq1)} + C")

                if len(eq_split) == 2 and self.integral[1]:
                    if self.integral[0]:
                        if self.derivative[1] and self.derivative[0]:
                            self.output[0] = ("De primitieve en afgeleide van de functies zijn:", {"latex": False})
                        elif self.derivative[1]:
                            self.output[0] = ("De primitieve en afgeleide van de functies zijn:", {"latex": False})
                            self.output = pop_iterable(self.output, (1,2))

                    else:
                        if self.derivative[1] and self.derivative[0]:
                            self.output[0] = ("De primitieve en afgeleide van de functies zijn:", {"latex": False})
                            self.output = pop_iterable(self.output, (2,3))
                        elif self.derivative[1]:
                            self.output[0] = ("De primitieve en afgeleide van de functie is:", {"latex": False})
                            self.output = pop_iterable(self.output, (1,2))

                    if self.eq2.is_number:
                        integral = get_uneval_sp_objs(eq_split[1])
                        self.output.append(f"II = {custom_latex(integral)} = {custom_latex(self.eq2)}")
                    
                    else:
                        self.output.append(f"G({symbol}) = {custom_latex(self.eq2)} + C")

            if self.derivative.any() or self.integral.any():
                self.output.append(("", {"latex": False}))


            if self.symbol:
                self.domain = sp.calculus.util.continuous_domain(self.eq, self.symbol, domain=sp.S.Reals)
                self.domain_is_reals = bool(self.domain is sp.S.Reals)


            if not isinstance(self.eq, sp.AccumBounds):
                self.solution_set = sp.solveset(self.eq, domain=sp.S.Reals)
            else:
                self.solution_set = sp.EmptySet


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
                        self.vert_asympt_eq = [asympt_values[i] for i in range(len(asympt_values)) if not asympt_check[i]]
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
                except NotImplementedError:
                    self.solutions_complex = sp.EmptySet
                    self.solutions = sp.solve(TR2(self.eq))

                self.has_any_solutions = bool(self.solutions_complex or self.solutions or self.solution_set.is_FiniteSet)


            if not self.has_any_solutions and not self.numerical:
                self.eq_string = add_args_to_func(self.eq_string, func_name="root", replace_with="evaluate=False", amt_commas=2)
                self.eq_string = self.eq_string.replace("limit", "Limit")

                try:
                    self.eq_string = sp.sympify(self.eq_string, evaluate=False)
                except AttributeError:
                    self.eq_string = sp.sympify(self.eq_string)

                if len(eq_split) == 1:
                    if not self.symbol:
                        solution = sp.nsimplify(self.eq1, [sp.pi])
                        equals_sign = '='
                        if solution.is_number:
                            if solution == sp.N(solution) or self.eq1 == sp.N(solution):
                                equals_sign = '='
                            else:
                                equals_sign = '\\approx'

                            solution = sp.N(solution)
                            try:
                                complex_num = False
                                if solution.is_finite and int(solution) == solution and len(str(round(solution))) < 10:
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


                        if self.eq1 != self.eq_string and equals_sign != "=":
                            if not complex_num and round(float(solution), 9) == round(float(solution), 10):
                                equals_sign = '='  

                            self.output.append(f"{custom_latex(self.eq_string)} = {custom_latex(self.eq1)} {equals_sign} {custom_latex(solution)}")

                        elif self.eq_string == solution:
                            if eq_split[0] != str(solution):
                                if self.derivative.any() or self.integral.any():
                                    self.output.pop()
                                elif ".subs" in eq_split[0] or ".diff" in eq_split[0] or ".integrate" in eq_split[0]:
                                    self.eq_string = get_uneval_sp_objs(eq_split[0])
                                    self.output.append(f"{custom_latex(self.eq_string)} {equals_sign} {custom_latex(solution)}")
                                else:
                                    self.output.append(f"\\textrm{{{eq_split[0]}}} {equals_sign} {custom_latex(solution)}")
                            
                            else:
                                self.output.append(f"\\textrm{{Yep dat is }} {custom_latex(solution)}")

                        else:
                            if equals_sign == '=' and round(solution, 9) != round(solution, 10):
                                equals_sign = '\\approx'

                            self.output.append(f"{custom_latex(self.eq_string)} {equals_sign} {custom_latex(solution)}")

                    elif sp.nsimplify(self.eq1, [sp.pi]).is_number:
                        solution = custom_simplify(self.eq1)
                        if solution != sp.N(solution):
                            self.output.append(f"{custom_latex(self.eq_string)} = {custom_latex(solution)} \\approx {custom_latex(round(sp.N(solution), 5))}")
                        
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

                    if self.eq1 != lhs or self.eq2 != rhs:
                        self.output.append((f"Versimpelingen:", {"latex": False}))

                        if self.eq1 != lhs:
                            self.output.append(f"\\bullet \\quad {custom_latex(self.eq1)} = {custom_latex(lhs)}")
                        if self.eq2 != rhs:
                            self.output.append(f"\\bullet \\quad {custom_latex(self.eq2)} = {custom_latex(rhs)}")
                    
                    if lhs == rhs:
                        if self.derivative.any() or self.integral.any():
                            self.output.append(("De vergelijking wordt dus:", {"latex": False}))
                        
                        self.output.append((f"{custom_latex(lhs)} = {custom_latex(rhs)}", {"new_line":2}))
                        self.output.append(("Deze vergelijking klopt", {"latex": False}))

                    elif lhs.is_number and rhs.is_number:
                        if self.derivative.any() or self.integral.any():
                            self.output.append(("De vergelijking wordt dus:", {"latex": False}))

                        self.output.append((f"{custom_latex(lhs)} \\neq {custom_latex(rhs)}", {"new_line":2}))
                        self.output.append(("Deze vergelijking klopt niet", {"latex": False}))

                    else:                        
                        self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                        self.output.append(f"{custom_latex(self.eq1)} = {custom_latex(self.eq2)}")

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
            
        except (NotImplementedError, TypeError):
            # TypeError from interpretation
            try:
                self.eq12
            except UnboundLocalError:
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
            self.output.append(f"{custom_latex(self.eq1)} = {custom_latex(self.eq2)}")

            if self.solution_set.is_FiniteSet:
                set_numerical_text()

                if len(self.solution_set) == 1:
                    self.output.append((f"De oplossing is:", {"latex":False}) if not self.multivariate else (f"Het snijpunt met de $x$-as is:", {"latex":False}))
                    self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solution_set.args[0])}")
                    if self.solution_set.args[0] != sp.N(self.solution_set.args[0]):
                        self.output[-1] += f" \\approx {round(sp.N(self.solution_set.args[0]), 5)}"
                    
                else:
                    self.output.append((f"De oplossingen zijn:", {"latex":False}) if not self.multivariate else (f"De snijpunten met de $x$-as zijn:", {"latex":False}))
                    if len(self.solution_set) > 5:
                        solution_array = np.array(list(self.solution_set))
                        self.interval_solutions = solution_array[np.argsort(np.abs(solution_array))][:5]
                        self.output[-1] = (f"De eerste 5 oplossingen zijn:", {"latex":False}) if not self.multivariate else (f"De eerste 5 snijpunten met de $x$-as zijn:", {"latex":False})
                    else:
                        self.interval_solutions = self.solution_set

                    set_count_solutions()
                            
                if not self.domain_is_reals:
                    self.output.append((f"Het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(custom_latex(self.domain))
            
            else:
                self.output.append((f"De oplossingen zijn:", {"latex":False}) if not self.multivariate else (f"De snijpunten met de $x$-as zijn:", {"latex":False}))
                self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solution_set)}")         

                if not self.domain_is_reals:
                    self.output.append((f"Het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(custom_latex(self.domain))


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


                    self.output = self.output[:-2]
                    if len(self.roots_numeric) == 1:
                        self.output[-1] = (f"Het snijpunt met de $x$-as is:", {"latex":False}) if self.multivariate else (f"De oplossing is:", {"latex":False})
                    set_numerical_text()
                
                self.interval_solutions = sp.FiniteSet(*self.interval_solutions)

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
                plottable_x_coords = x_coords_np[np.isreal(y_coords) & np.isfinite(y_coords)]
                plottable_x_coords = add_endpoint(list(plottable_x_coords), np_lambda_func, domain).ravel()
                y_coords = self.apply_func_to_array(np_lambda_func, plottable_x_coords)

                return plottable_x_coords, y_coords
            
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
            self.x_coords = np.linspace(x_range[0] - 1, x_range[1] + 1, int(1/dx))

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
            self.x_coords = segmented_linspace(x_range[0] - 1, x_range[1] + 1, self.vert_asympt, num=int(1/dx), dx=0.00001)


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