import numpy as np
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
from sympy.printing.latex import LatexPrinter
import regex as re
from scipy.optimize import fsolve, bisect, newton
from warnings import filterwarnings
from src.Solver.src.solver.math_parser import add_args_to_func, math_interpreter, get_uneval_sp_objs, split_equation
import traceback
import typing
from types import FunctionType
from collections.abc import Iterable
from numbers import Number
import operator

filterwarnings("ignore", category=RuntimeWarning)

def apply_opperator(x, selected_operator, y):
    # Dictionary to map operator strings to functions
    operators = {
        "==": operator.eq,  # Equality
        "=": operator.eq,   # Equality
        "!=": operator.ne,  # Not equal
        ">": operator.gt,   # Greater than
        "<": operator.lt,   # Less than
        ">=": operator.ge,  # Greater than or equal to
        "<=": operator.le,  # Less than or equal to
    }
    try:
        return operators[selected_operator](x, y)
    except KeyError:
        raise ValueError("Invalid operator")

def segmented_linspace(start: float, end: float, breakpoints: typing.Iterable[float], num: int=10, breakpoint_offset: float=0.01) -> typing.List[np.ndarray]:
    """
    Generate a list of linearly spaced segments between `start` and `end`, divided by `breakpoints`.

    Args:
        start (float): The starting point of the range.
        end (float): The ending point of the range.
        breakpoints (Iterable[float]): Points at which the range is divided into segments.
        num (int): Number of points in each segment (default is 10).
        breakpoint_offset (float): Small offset added to the start and end of each segment (default is 0.01).

    Returns:
        List[np.ndarray]: A list of numpy arrays, each containing a segment of linearly spaced points.
    """

    all_points = sorted([start] + list(breakpoints) + [end])
    return [np.linspace(all_points[i] + breakpoint_offset, all_points[i+1] - breakpoint_offset, num) for i in range(len(all_points)-1)]


def get_smooth_x_coords(x_range, dx, vert_asympt=None):
    if vert_asympt is None:
        x_coords = np.linspace(x_range[0] - 1, x_range[1] + 1, int(1/dx))
        for i in range(1, 10):
            x_coords = np.sort(np.append(x_coords, np.linspace(x_range[0]/(10**i), x_range[1]/(10**i), max(10, int(10/(dx*10**i))))))

    else:
        x_coords = segmented_linspace(x_range[0] - 1, x_range[1] + 1, vert_asympt, num=int(1/dx), breakpoint_offset=0.00001)
        if len(x_coords) > 3:
            return x_coords

        for i in range(1, 5):
            new_x_coords = segmented_linspace(x_range[0]/(10**i), x_range[1]/(10**i), vert_asympt, num=max(10, int(10/(dx*10**i))), breakpoint_offset=0.00001)
            for i in range(len(x_coords)):
                array = x_coords[i]
                min_array = min(array)
                max_array = max(array)
                for array_new in new_x_coords:
                    if min_array <= np.mean(array_new) <= max_array:
                        x_coords[i] = np.sort(np.append(array, array_new))

    return x_coords


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


def equation_type_to_latex(equation_symbol):
    equation_type_latex_map = {"!=": "\\neq", ">=": "\\geq", "<=": "\\leq"}
    return equation_type_latex_map.get(equation_symbol, equation_symbol)

def flip_inequality_sign(inequality_sign):
    """
    Flip the sign of an inequality.

    Args:
        inequality_sign (str): The inequality sign to flip.

    Returns:
        str: The flipped inequality sign.
    """
    inequality_flip_replacements = {">": "<", "<": ">", ">=": "\\leq", "<=": "\\geq", "!=": "=", "=": "\\neq"}
    return inequality_flip_replacements.get(inequality_sign, inequality_sign)

class CustomLatexPrinter(LatexPrinter):
    """
    A custom LaTeX printer that provides customized formatting for SymPy expressions.
    """

     
    def _print_Relational(self, expr, **kwargs):
        """
        Customize the printing of relational expressions (e.g., inequalities).

        Args:
            expr (sp.Relational): The relational expression to print.

        Returns:
            str: The LaTeX representation of the relational expression.
        """

        lhs = expr.lhs
        rhs = expr.rhs

        # If the relation is flipped, reverse the relation and swap lhs and rhs
        if lhs.is_Symbol:
            return super()._print_Relational(expr, **kwargs)
        else:
            flipped_relation = flip_inequality_sign(expr.rel_op)
            return f"{self._print(rhs)} {flipped_relation} {self._print(lhs)}"
        
    def _print_Or(self, expr, **kwargs):
        """
        Customize the printing of Or expressions by controlling the order of arguments.

        Args:
            expr (sp.Or): The Or expression to print.

        Returns:
            str: The LaTeX representation of the Or expression.
        """

        if len(expr.args) != 2:
            return super()._print_Or(expr, **kwargs)

        ordered_args = [expr.args[1], expr.args[0]]

        # Convert the ordered arguments to LaTeX
        latex_args = [self._print(arg) for arg in ordered_args]

        # Join the LaTeX strings with the \vee symbol
        return ' \\ \\vee \\ '.join(latex_args)
    

    def _print_And(self, expr, **kwargs):
        """
        Customize the printing of And expressions by combining inequalities.

        Args:
            expr (sp.And): The And expression to print.

        Returns:
            str: The LaTeX representation of the And expression.
        """

        if len(expr.args) != 2:
            return super()._print_And(expr, **kwargs)
        
        expr_left = expr.args[0]
        expr_right = expr.args[1]

        symbol_left = expr_left.args[1]
        symbol_right = expr_right.args[0]
        lower_bound = expr_left.args[0]
        upper_bound = expr_right.args[1]

        if not symbol_left.is_Symbol or not symbol_right.is_Symbol:
            symbol_left = expr_left.args[0]
            symbol_right = expr_right.args[1]
            lower_bound = expr_left.args[1]
            upper_bound = expr_right.args[0]

        if symbol_left != symbol_right or not symbol_left.is_Symbol:
            return super()._print_And(expr, **kwargs)
        
        if lower_bound.evalf() > upper_bound.evalf():
            lower_bound, upper_bound = upper_bound, lower_bound

        left_inequality = equation_type_to_latex(expr_left.rel_op)
        right_inequality = equation_type_to_latex(expr_right.rel_op)

        return f"{self._print(lower_bound)} {left_inequality} {self._print(symbol_left)} {right_inequality} {self._print(upper_bound)}"
    

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
                arg = self._print(arg)
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
    

def custom_latex(expr: sp.Basic, **kwargs) -> str:
    """
    Convert a SymPy expression to a custom LaTeX representation.

    Args:
        expr (sp.Basic): The SymPy expression to convert.

    Returns:
        str: The LaTeX representation of the expression.
    """

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
    
def get_real_root(expr: sp.Expr):
    def replace_root(matched_expr):
        base = matched_expr.group(1)
        power = matched_expr.group(2)
        power_sp = sp.sympify(power)
        if power_sp.q % 2 == 0 or power_sp.p % 2 == 0:
            return f"Abs({base})**({power})"
        return f"sign({base})*Abs({base})**({power})"
        

    str_expr = str(expr)

    str_expr = re.sub(r"(\w*\(.*\))\*\*\((-*\d+/\d+)\)", replace_root, str_expr)
    str_expr = re.sub(r"(\w+)\*\*\((-*\d+/\d+)\)", replace_root, str_expr)

    expr = sp.sympify(str_expr)
    return expr


class Solve:
    def __init__(self, input_string: str) -> None:
        """
        Initializes the Solve class with the input equation string.

        Args:
            input_string (str): A string representing the equation to solve.
        """

        self.symbol = None
        self.equation_type = "="
        self.equation_type_sp = sp.Eq
        self.solution_set = None
        self.solution_inequality = None
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
                    single_expr = get_real_root(single_expr)
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

        def apply_double_equals_operator(lhs, rhs):
            return apply_opperator(lhs, "==", rhs)

        def process_equation(eq_string: str) -> str:
            equation_symbol_map = {"!=": sp.Ne, ">=": sp.Ge, "<=": sp.Le, "==": apply_double_equals_operator, "=": sp.Eq, ">": sp.Gt, "<": sp.Lt}
            eq_split = split_equation(eq_string)
            eq_split = [string for string in eq_split if string not in equation_symbol_map.keys()]

            for symbol, equation_type in equation_symbol_map.items():
                if symbol in eq_string:
                    self.equation_type = symbol
                    self.equation_type_sp = equation_type
                    return set_eqs(eq_split)
                
            return set_eqs(eq_split)


        def sympify_equation(eq_str: str) -> sp.Basic:
            try:
                return eq_str, TR111(sp.sympify(eq_str)).doit()
            except ValueError:
                eq_str = add_args_to_func(eq_str, func_name="integrate", replace_with="x").replace(".integrate()", ".integrate(x)")
                return eq_str, TR111(sp.sympify(eq_str)).doit()


        def get_self_eq(eq1, eq2):
            try:
                return sp.nsimplify(self.equation_type_sp(eq1, eq2), tolerance=1e-7)
            except AttributeError:
                return self.equation_type_sp(eq1, eq2)
            

        def set_eqs(eq_split, use_self=True):
            eq_split[0], eq1 = sympify_equation(eq_split[0])

            if len(eq_split) == 1:
                eq2 = 0
            elif len(eq_split) == 2:
                eq_split[1], eq2 = sympify_equation(eq_split[1])
            elif use_self:
                self.output.append(("Error: Meer dan 1 relatieteken (=, ≥, ≤, etc.)", {"latex": False}))
                return None
            
            eq12 = eq1 - eq2
            eq = get_self_eq(eq1, eq2)

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
            self.eq1 = sp.sympify(self.eq1).subs(self.symbol, symbol_new)
            self.eq2 = sp.sympify(self.eq2).subs(self.symbol, symbol_new)
            self.eq12 = self.eq1 - self.eq2
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
            eq_split = process_equation(self.eq_string)
            if eq_split is None:
                return self.equation_interpret, self.output, self.plot

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
                self.domain = sp.calculus.util.continuous_domain(self.eq12, self.symbol, domain=sp.S.Reals)
                self.domain_is_reals = bool(self.domain is sp.S.Reals)

            self.equation_is_inequality = self.equation_type != '='

            if not isinstance(self.eq12, sp.AccumBounds):
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
                                has_dot_function = np.array([dot_func in eq_split[0] for dot_func in [".subs", ".diff", ".integrate", "limit"]]).any()
                                if self.derivative.any() or self.integral.any():
                                    self.output.pop()
                                elif has_dot_function:
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
                    
                    has_equal_sides = apply_opperator(lhs, self.equation_type, rhs)
                    sides_are_numbers = (lhs.is_number and rhs.is_number)
                    has_solution = has_equal_sides or sides_are_numbers

                    if has_solution:
                        self.output.append((f"Vergelijking:", {"latex": False}))

                    simplify = self.eq1_unsimplified != lhs or self.eq2_unsimplified != rhs
                    if simplify:
                        self.output.append(f"{custom_latex(self.eq1_unsimplified)} {equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2_unsimplified)}")
                        self.output.append((f"Versimpelingen:", {"latex": False}))

                        if self.eq1_unsimplified != lhs:
                            self.output.append(f"\\bullet \\quad {custom_latex(self.eq1_unsimplified)} \\Longrightarrow {custom_latex(lhs)}")
                        if self.eq2_unsimplified != rhs:
                            self.output.append(f"\\bullet \\quad {custom_latex(self.eq2_unsimplified)} \\Longrightarrow {custom_latex(rhs)}")
                    
                    if has_solution:
                        if simplify:
                            self.output.append(("Onze vergelijking wordt dus:", {"latex": False}))

                        self.output.append((f"{custom_latex(lhs)} {equation_type_to_latex(self.equation_type)} {custom_latex(rhs)}"))

                        if has_equal_sides:
                            self.output.append(("Dit is waar, dus deze vergelijking klopt", {"latex": False}))
                        elif sides_are_numbers:
                            self.output.append(("Dit is niet waar, dus deze vergelijking klopt niet", {"latex": False}))

                    else:                        
                        self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                        self.output.append(f"{custom_latex(self.eq1)} {equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2)}")

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
            self.output.append(f"{custom_latex(self.eq1)} {equation_type_to_latex(self.equation_type)} {custom_latex(self.eq2)}")

            if self.solution_set.is_FiniteSet:
                set_numerical_text()

                if len(self.solution_set) == 1:
                    if self.equation_is_inequality:
                        self.output.append((f"De oplossing is:", {"latex":False}))
                        self.output.append(custom_latex(self.solution_inequality))
                    else:
                        self.output.append((f"De oplossing is:", {"latex":False}) if not self.multivariate else (f"Het snijpunt met de $x$-as is:", {"latex":False}))
                        self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solution_set.args[0])}")
                    
                    if self.solution_set.args[0] != sp.N(self.solution_set.args[0]):
                        self.output[-1] += f" \\approx {round(sp.N(self.solution_set.args[0]), 5)}"
                    
                else:
                    if self.equation_is_inequality:
                        self.output.append((f"De oplossing is:", {"latex":False}))
                        self.output.append(custom_latex(self.solution_inequality))
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
                if self.equation_is_inequality:
                    self.output.append((f"De (eerste) oplossing is:", {"latex":False}))
                    self.output.append(custom_latex(self.solution_inequality))
                else:
                    self.output.append((f"De oplossingen zijn:", {"latex":False}) if not self.multivariate else (f"De snijpunten met de $x$-as zijn:", {"latex":False}))
                    self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solution_set)}")         

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