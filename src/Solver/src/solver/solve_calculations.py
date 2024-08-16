import numpy as np
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
from sympy.printing.latex import LatexPrinter
import regex as re
import scipy.optimize
import warnings
from src.Solver.src.solver.string_parser import add_args_to_func, math_interpreter, replace_dot_funcs


warnings.filterwarnings("ignore", category=RuntimeWarning)


def segmented_linspace(start, end, breakpoints, num=10, dx=0.01):
    breakpoints = list(breakpoints)
    all_points = sorted([start] + breakpoints + [end])
    lists_with_breaks = [np.linspace(all_points[i] + dx, all_points[i+1] - dx, num) for i in range(len(all_points)-1)]
    return lists_with_breaks

def trig_simp(x):
    return TR1(TR2(x))

def pop_iterable(pop_list: list, index_list):
    index_counter = 0
    for i in index_list:
        i -= index_counter
        pop_list.pop(i)
        index_counter += 1

    return pop_list


class CustomLatexPrinter(LatexPrinter):
    def _print_Mul(self, expr, **kwargs):
        numer, denom = expr.as_numer_denom()

        if isinstance(numer, sp.log) and isinstance(denom, sp.log):
            base = denom.args[0]

            if isinstance(base, (sp.Number)):
                arg = self._print(numer.args[0])
                base = self._print(base)

                return f' \\ ^{{{base}}} \\! \\log\\left({arg} \\right)'

        result = super()._print_Mul(expr).replace("1 \\cdot", " ")
        result = re.sub(r"\\left\(-(\d+)\\right\) ", r"- \1 \\cdot", result)
        return result
    

    def _print_Pow(self, expr, **kwargs):
        if expr.exp.as_numer_denom()[1] != 1 and expr != sp.root(expr.base, 1/expr.exp, evaluate=False):
            base = self._print(expr.base)
            exp = self._print(sp.simplify(expr.exp))
            return f"{base}^{{{exp}}}"

        elif expr.as_numer_denom()[1] != 1:
            expr = sp.nsimplify(expr)
            return sp.latex(expr)

        return sp.latex(expr).replace("log", "ln")

    def _print_log(self, expr, **kwargs):
        if len(expr.args) == 1:
            # Natural logarithm
            arg = self._print(expr.args[0])
            return f'\\ln \\left({arg} \\right)'
        
        elif len(expr.args) == 2:
            # Logarithm with a specific base
            base = self._print(expr.args[1])
            arg = self._print(expr.args[0])
            return f' \\ ^{{{base}}} \\! \\log\\left({arg} \\right)'
            
        else:
            # Fallback for unexpected cases
            return super()._print_log(expr)
        

    def _print_Limit(self, expr, **kwargs):
        func = expr.args[0]
        var = self._print(expr.args[1])
        point = self._print(expr.args[2])
        direction = expr.args[3]

        limit_expr = str(expr)
        limit_value = sp.simplify(expr)

        if str(direction) == "+":
            limit_expr_opposite = limit_expr.replace("dir='+'", "dir='-'")
            limit_value_opposite = sp.simplify(limit_expr_opposite)

        elif str(direction) == "-":
            limit_expr_opposite = limit_expr.replace("dir='-'", "dir='+'")
            limit_value_opposite = sp.simplify(limit_expr_opposite)


        if limit_value == limit_value_opposite:
            return f"\\lim_{{{var} \\to {point}}} {self._print(func)}"
        
        elif str(direction) == "+":
            return f"\\lim_{{{var} \\ \\downarrow \\ {point}}} {self._print(func)}"
        
        elif str(direction) == "-":
            return f"\\lim_{{{var} \\ \\uparrow \\ {point}}} {self._print(func)}"

        return super()._print_Limit(expr)
    
    def _print_Function(self, expr, **kwargs):
        func_name = expr.func.__name__
        
        if func_name == 'asin':
            return rf'\arcsin{{\left({self._print(expr.args[0], **kwargs)}\right)}}'
        elif func_name == 'acos':
            return rf'\arccos{{\left({self._print(expr.args[0], **kwargs)}\right)}}'
        elif func_name == 'atan':
            return rf'\arctan{{\left({self._print(expr.args[0], **kwargs)}\right)}}'
        elif func_name == 'asec':
            return rf'\arcsec{{\left({self._print(expr.args[0], **kwargs)}\right)}}'
        elif func_name == 'acsc':
            return rf'\arccsc{{\left({self._print(expr.args[0], **kwargs)}\right)}}'
        elif func_name == 'acot':
            return rf'\arccot{{\left({self._print(expr.args[0], **kwargs)}\right)}}'
        else:
            return super()._print_Function(expr, **kwargs)


def custom_latex(expr, **kwargs):
    return CustomLatexPrinter(**kwargs).doprint(expr)

def custom_simplify(expr, **kwargs):
    try:
        return sp.expand_log(sp.simplify(expr))
    except Exception:
        try:
            return sp.simplify(expr)
        except Exception:
            return expr


class Solve:
    def __init__(self, input_string):
        self.symbol = None
        self.solutions = None
        self.interval_solutions = None
        self.vert_asympt = None
        self.vert_asympt_eq = None
        self.eq_string = math_interpreter(input_string)
        self.output = []
        self.equation_interpret = None
        self.plot = False
        self.intersect = False
        self.numerical = False
        self.multivariate = False
        self.derivative = False
        self.integral = False

    def numerical_roots(self, eq, a=-10000, b=10000, dx=0.01, solve_method="newton", dy=0.1, use_scale_factor:bool=False, default_func:bool=True):
        eq_lambda_sp = eq

        def use_module(module="numpy"):
            nonlocal eq
            x = sp.symbols('x')
            eq = eq_lambda_sp(x)
            eq_lambda = sp.lambdify(x, eq, module)
            diff_eq = sp.diff(eq, x)
            diff_eq_lambda = sp.lambdify(x, diff_eq, module)

            x = np.linspace(a, b, (b-a) * int(1/dx))
            xy = np.zeros((x.shape[0], 2))
            xy[:, 0] = x
            xy[:, 1] = eq_lambda(x)
            xy = xy[~np.isnan(xy[:,1]) & ~np.isinf(xy[:,1])]

            return eq_lambda, diff_eq_lambda, xy

        try:
            eq_lambda, diff_eq_lambda, xy = use_module(module="numpy")

        except NameError:
            try:
                eq_lambda, diff_eq_lambda, xy = use_module(module="scipy")
            except NameError:
                eq_lambda, diff_eq_lambda, xy = use_module(module="sympy")

        if use_scale_factor:
            test = np.abs(xy[:,1])
            min_values = xy[np.argmin(test)]
            y_value_shift = eq_lambda(min_values[0] + 0.1)
            scale_factor = abs(y_value_shift - min_values[1]/min_values[1])
        else:
            scale_factor = 1

        condition = (xy[:, 1] > -dy*scale_factor) & (xy[:, 1] < dy*scale_factor)
        indices = np.where(condition)[0]

        discontinuities = np.where(np.diff(indices) != 1)[0] + 1
        split_indices = np.split(indices, discontinuities)

        len_split = len(split_indices)
        roots = np.zeros(len_split)

        if len_split == 1 and split_indices[0].size == 0:
            if default_func:
                self.intersect = False
                self.numerical = False

            return np.array([])
            

        for i in range(len_split):
            min_index = np.argmin(np.abs(xy[split_indices[i]]), axis=0)[1]
            guess = xy[split_indices[i]][min_index, 0]

            try:
                if solve_method == "newton":
                    roots[i] = round(scipy.optimize.newton(eq_lambda, guess, fprime=diff_eq_lambda), 5)

                elif solve_method == "bisect":
                    a_bisect = np.min(xy[split_indices[i]])
                    b_bisect = np.max(xy[split_indices[i]])

                    try:
                        if eq_lambda(a_bisect) * eq_lambda(b_bisect) < 0:
                            roots[i] = round(scipy.optimize.bisect(eq_lambda, a_bisect, b_bisect), 5)
                        else:
                            roots[i] = None
                    except ValueError:
                        roots[i] = None

                elif solve_method == "fsolve":
                    roots[i] = round(float(scipy.optimize.fsolve(eq_lambda, guess)), 5)

            except RuntimeError:
                roots[i] = None

        roots = roots[roots != None]
        roots = roots[~np.isnan(roots)]

        if a in roots and eq_lambda(a -1) * eq_lambda(a + 1) >= 0:
            roots = np.delete(roots, np.where(roots == a))

        if b in roots and eq_lambda(b - 1) * eq_lambda(b + 1) >= 0:
            roots = np.delete(roots, np.where(roots == b))

        if default_func:
            self.intersect = True
            self.numerical = True

        return roots


    def solve_numerically(self, sp_func=None):
        if sp_func is None:
            default_func = True
            if self.multivariate:
                sp_func = self.eq2
            else:
                sp_func = self.eq12
            
            self.numerical = True

        else:
            default_func = False

        self.roots = self.numerical_roots(sp_func, -10000, 10000, solve_method="newton", default_func=default_func)

        if self.roots.size == 0:
            self.roots = self.numerical_roots(sp_func, -10000, 10000, solve_method="fsolve", default_func=default_func)

        if self.roots.size == 0:
            self.roots = self.numerical_roots(sp_func, -10000, 10000, solve_method="bisect", default_func=default_func)

        if self.roots.size == 0:
            self.roots = self.numerical_roots(sp_func, -100, 100, dx=0.000001, solve_method="newton", use_scale_factor=True, default_func=default_func)
        

        solutions = sp.FiniteSet(*self.roots)
        return solutions


    def check_solve_numerically(self):
        if isinstance(self.solutions, sp.ConditionSet):
            self.eq = self.solutions.condition
            self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)

            if isinstance(self.solutions, sp.ConditionSet):
                if self.eq == self.solutions.condition:
                    return self.solve_numerically()
                    


    def solve_equation(self):
        """Solve the equation and display the results
        """

        try:
            eq_split = self.eq_string.split("=")

            if len(eq_split) == 1:
                try:
                    eq1 = TR111(sp.sympify(eq_split[0])).doit()
                except ValueError:
                    eq_split[0] = add_args_to_func(eq_split[0], func_name="integrate", replace_with="x").replace(".integrate()", ".integrate(x)")
                    eq1 = TR111(sp.sympify(eq_split[0])).doit()

                eq2 = 0

                try:
                    self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                except AttributeError:
                    self.eq = eq1

                self.equation_interpret = self.eq_string
                free_symbols = list(eq1.free_symbols)
                if free_symbols:
                    if len(free_symbols) == 2:
                        y_symbol = sp.symbols("y")
                        
                        if y_symbol in free_symbols:
                            self.multivariate = True

                            free_y_equation = reversed([sol for sol in sp.solve(eq1, y_symbol) if str(sp.I) not in str(sol)])
                            abs_solutions = []
                            new_solutions = []
                            for sol in free_y_equation:
                                if sp.Abs(sol) not in abs_solutions:
                                    new_solutions.append(sol)
                                    abs_solutions.append(sp.Abs(sol))
                            
                            eq1 = y_symbol
                            eq2 = new_solutions[0]
                            eq12 = eq1 - eq2

                            try:
                                self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                            except AttributeError:
                                self.eq = sp.Eq(eq1, eq2)


                            self.eq = self.eq.subs(y_symbol, 0)
                            eq12 = eq12.subs(y_symbol, 0)
                            free_symbols.remove(y_symbol)
                            eq_split = (str(y_symbol), str(eq2))

                    if (len(free_symbols) == 2 and y_symbol not in free_symbols) or len(free_symbols) > 2:
                        self.output.append(("Error: Meer dan 1 variabele", {"latex": False}))
                        return self.equation_interpret, self.output, self.plot
                    

                    self.symbol = free_symbols[0]
                    symbol_new = sp.symbols(str(self.symbol), real=True)
                    self.eq = self.eq.subs(self.symbol, symbol_new)
                    eq1 = eq1.subs(self.symbol, symbol_new)
                    self.symbol = symbol_new

                    if self.multivariate:
                        self.eq1 = sp.lambdify(self.symbol, eq1.subs(y_symbol, 0), "sympy")
                    else:
                        self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")

                    self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")
                    
                    if not custom_simplify(self.eq).is_number:
                        self.equation_interpret = f"{self.eq_string} = 0"

            elif len(eq_split) == 2:
                try:
                    eq1 = TR111(sp.sympify(eq_split[0])).doit()
                except ValueError:
                    eq_split[0] = add_args_to_func(eq_split[0], func_name="integrate", replace_with="x").replace(".integrate()", ".integrate(x)")
                    eq1 = TR111(sp.sympify(eq_split[0])).doit()
                
                try:
                    eq2 = TR111(sp.sympify(eq_split[1])).doit()
                except ValueError:
                    eq_split[1] = add_args_to_func(eq_split[1], func_name="integrate", replace_with="x").replace(".integrate()", ".integrate(x)")                
                    eq2 = TR111(sp.sympify(eq_split[1])).doit()
                
                eq12 = eq1 - eq2

                try:
                    self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                except AttributeError:
                    self.eq = sp.Eq(eq1, eq2)

                self.equation_interpret = self.eq_string
                self.eq_string = str(self.eq)
                free_symbols = list(eq12.free_symbols)
                
                if free_symbols:
                    if len(free_symbols) == 2:
                        y_symbol = sp.symbols("y")
                        
                        if y_symbol in free_symbols:
                            self.multivariate = True
                            free_y_equation = reversed([sol for sol in sp.solve(eq12, y_symbol) if str(sp.I) not in str(sol)])
                            abs_solutions = []
                            new_solutions = []
                            for sol in free_y_equation:
                                if sp.Abs(sol) not in abs_solutions:
                                    new_solutions.append(sol)
                                    abs_solutions.append(sp.Abs(sol))
                            
                            eq1 = y_symbol
                            eq2 = new_solutions[0]
                            eq12 = eq1 - eq2

                            try:
                                self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                            except AttributeError:
                                self.eq = sp.Eq(eq1, eq2)


                            self.eq = self.eq.subs(y_symbol, 0)
                            eq12 = eq12.subs(y_symbol, 0)
                            free_symbols.remove(y_symbol)
                            

                    if (len(free_symbols) == 2 and y_symbol not in free_symbols) or len(free_symbols) > 2:
                        self.output.append(("Error: Meer dan 1 variabele", {"latex": False}))
                        return self.equation_interpret, self.output, self.plot
                    
                    self.symbol = free_symbols[0]
                    symbol_new = sp.symbols(str(self.symbol), real=True)
                    self.eq = self.eq.subs(self.symbol, symbol_new)
                    eq1 = eq1.subs(self.symbol, symbol_new)
                    eq2 = eq2.subs(self.symbol, symbol_new)
                    self.symbol = symbol_new

                    if self.multivariate:
                        self.eq1 = sp.lambdify(self.symbol, eq1.subs(y_symbol, 0), "sympy")
                        self.eq2 = sp.lambdify(self.symbol, eq2.subs(y_symbol, 0), "sympy")
                    else:
                        self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")
                        self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")
                

            else:
                self.output.append(("Error: Meer dan 1 '='-teken ", {"latex": False}))
                return self.equation_interpret, self.output, self.plot
            
            try:
                self.eq = custom_simplify(self.eq)
            except ValueError:
                pass

            self.derivative = np.array(["diff" in string for string in eq_split])
            if self.derivative.any():
                if self.symbol is None:
                    symbol = "x"
                else:
                    symbol = self.symbol

                if len(eq_split) == 2 and self.derivative[0] and self.derivative[1]:
                    self.output.append(("De afgeleide van de functies zijn:", {"latex": False}))

                else:
                    self.output.append(("De afgeleide van de functie is:", {"latex": False}))

                if self.derivative[0]:
                    derivative = replace_dot_funcs(eq_split[0])
                    self.output.append(f"{custom_latex(derivative)} = {custom_latex(custom_simplify(eq1))}")

                if len(eq_split) == 2 and self.derivative[1]:
                    derivative = replace_dot_funcs(eq_split[1])
                    self.output.append(f"{custom_latex(derivative)} = {custom_latex(custom_simplify(eq2))}")


            self.integral = np.array(["integrate" in string for string in eq_split])
            if self.integral.any():
                if self.symbol is None:
                    symbol = "x"
                else:
                    symbol = self.symbol

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


                    if eq1.is_number:
                        integral = replace_dot_funcs(eq_split[0])
                        self.output.append(f"I = {custom_latex(integral)} = {custom_latex(custom_simplify(eq1))}")
                    
                    else:
                        self.output.append(f"F({symbol}) = {custom_latex(custom_simplify(eq1))} + C")

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

                    if eq2.is_number:
                        integral = replace_dot_funcs(eq_split[1])
                        self.output.append(f"II = {custom_latex(integral)} = {custom_latex(custom_simplify(eq2))}")
                    
                    else:
                        self.output.append(f"G({symbol}) = {custom_latex(custom_simplify(eq2))} + C")

            if self.derivative.any() or self.integral.any():
                self.output.append(("", {"latex": False}))



            if not isinstance(self.eq, sp.AccumBounds):
                self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)
            else:
                self.solutions = sp.EmptySet

            
            if self.symbol:
                domain = sp.calculus.util.continuous_domain(self.eq, self.symbol, domain=sp.S.Reals)
                domain_string = str(domain)

                eq12 = custom_simplify(eq1 - eq2)
                self.eq12 = sp.lambdify(self.symbol, eq12, "sympy")


            if self.symbol:
                if not trig_simp(eq12).as_numer_denom()[1].is_number:
                    self.vert_asympt_eq = trig_simp(eq12).as_numer_denom()[1]

                elif domain != sp.S.Reals and (domain.is_Interval or domain.is_Union):
                    amt_intervals = len(domain.args) if domain.is_Union else 1
                    asympt_check = []
                    asympt_values = []
                    for i in range(amt_intervals):
                        sub_domain = domain.args[i] if domain.is_Union else domain
                        asympt_check.extend([self.eq12(sub_domain.args[j]).is_finite for j in range(2) if sub_domain.args[j].is_finite])
                        asympt_values.extend([sub_domain.args[j] for j in range(2) if sub_domain.args[j].is_finite])

                    if False in asympt_check:
                        self.vert_asympt_eq = [asympt_values[i] for i in range(len(asympt_values)) if not asympt_check[i]]
                        if not self.vert_asympt_eq:
                            self.vert_asympt_eq = None

            check_numerical = self.check_solve_numerically()

            if check_numerical is not None and not self.intersect:
                self.plot = True
                self.output.append(("Geen oplossing gevonden", {"latex": False}))
                return self.equation_interpret, self.output, self.plot

            elif check_numerical is not None:
                self.solutions = check_numerical 

            if len(sp.solve(TR2(self.eq))) == 0 and not self.numerical:
                self.eq_string = add_args_to_func(self.eq_string, func_name="root", replace_with="evaluate=False", amt_commas=2)
                self.eq_string = self.eq_string.replace("limit", "Limit")

                try:
                    self.eq_string = sp.sympify(self.eq_string, evaluate=False)
                except AttributeError:
                    self.eq_string = sp.sympify(self.eq_string)

                if len(eq_split) == 1:
                    if not self.symbol:
                        solution = sp.nsimplify(eq1, [sp.pi])
                        equals_sign = '='
                        if solution.is_number:
                            if solution == sp.N(solution) or eq1 == sp.N(solution):
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

                                if real_part == sp.nsimplify(eq1, [sp.pi]).as_real_imag()[0] and imag_part == sp.nsimplify(eq1, [sp.pi]).as_real_imag()[1]:
                                    equals_sign = '='

                            except ValueError:
                                equals_sign = '='

                        try:
                            str(eq1)
                        except ValueError:
                            equals_sign = '='


                        if eq1 != self.eq_string and equals_sign != "=":
                            if not complex_num and round(float(solution), 9) == round(float(solution), 10):
                                equals_sign = '='  

                            self.output.append(f"{custom_latex(self.eq_string)} = {custom_latex(eq1)} {equals_sign} {custom_latex(solution)}")

                        elif self.eq_string == solution:
                            if eq_split[0] != str(solution):
                                if self.derivative.any() or self.integral.any():
                                    self.output.pop()
                                elif ".subs" in eq_split[0] or ".diff" in eq_split[0] or ".integrate" in eq_split[0]:
                                    self.eq_string = replace_dot_funcs(eq_split[0])
                                    self.output.append(f"{custom_latex(self.eq_string)} {equals_sign} {custom_latex(solution)}")
                                else:
                                    self.output.append(f"\\textrm{{{eq_split[0]}}} {equals_sign} {custom_latex(solution)}")
                            
                            else:
                                self.output.append(f"\\textrm{{Yep dat is }} {custom_latex(solution)}")

                        else:
                            if equals_sign == '=' and round(solution, 9) != round(solution, 10):
                                equals_sign = '\\approx'

                            self.output.append(f"{custom_latex(self.eq_string)} {equals_sign} {custom_latex(solution)}")

                    elif sp.nsimplify(sp.simplify(eq1), [sp.pi]).is_number:
                        solution = custom_simplify(eq1)
                        if solution != sp.N(solution):
                            self.output.append(f"{custom_latex(self.eq_string)} = {custom_latex(solution)} \\approx {custom_latex(round(sp.N(solution), 5))}")
                        
                        else:
                            self.output.append(f"{custom_latex(self.eq_string)} = {custom_latex(solution)}")
                        

                    else:
                        self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                        self.output.append(f"{custom_latex(custom_simplify(eq1))} = 0")

                        complex_symbol = sp.symbols("x")

                        try:
                            check_complex_solutions = sp.solve(sp.Eq(self.eq1(complex_symbol), self.eq2(complex_symbol)))
                        except NotImplementedError:
                            check_complex_solutions = False

                        if self.multivariate:
                            self.output.append((f"Geen snijpunt met de x-as gevonden", {"latex":False}))
                        elif check_complex_solutions:
                            self.output.append(("Geen reële oplossing gevonden", {"latex": False}))
                        else:
                            self.output.append(("Geen oplossing gevonden", {"latex": False}))

                        self.plot = True


                elif len(eq_split) == 2:
                    lhs = sp.nsimplify(custom_simplify(eq1), [sp.pi])
                    rhs = sp.nsimplify(custom_simplify(eq2), [sp.pi])

                    if eq1 != lhs or eq2 != rhs:
                        self.output.append((f"Versimpelingen:", {"latex": False}))

                        if eq1 != lhs:
                            self.output.append(f"\\bullet \\quad {custom_latex(eq1)} = {custom_latex(lhs)}")
                        if eq2 != rhs:
                            self.output.append(f"\\bullet \\quad {custom_latex(eq2)} = {custom_latex(rhs)}")
                    
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
                        self.output.append(f"{custom_latex(custom_simplify(eq1))} = {custom_latex(custom_simplify(eq2))}")

                        complex_symbol = sp.symbols("x")
                        if self.multivariate:
                            self.output.append((f"Geen snijpunt met de x-as gevonden", {"latex":False}))
                        elif sp.solve(sp.Eq(self.eq1(complex_symbol), self.eq2(complex_symbol))):
                            self.output.append(("Geen reële oplossing gevonden", {"latex": False}))
                        else:
                            self.output.append(("Geen oplossing gevonden", {"latex": False}))

                        self.plot = True

                return self.equation_interpret, self.output, self.plot
            
            if self.solutions.is_empty:
                if len(eq_split) == 1:
                    self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                    self.output.append(f"{custom_latex(custom_simplify(eq1))} = 0")

                elif len(eq_split) == 2:
                    self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                    self.output.append(f"{custom_latex(custom_simplify(eq1))} = {custom_latex(custom_simplify(eq2))}")

                if self.multivariate:
                    self.output.append((f"Geen snijpunt met de x-as gevonden", {"latex":False}))
                else:
                    self.output.append(("Geen oplossing gevonden", {"latex": False}))

                self.plot = True

                return self.equation_interpret, self.output, self.plot
            
        except (NotImplementedError, TypeError):
            try:
                eq1
                if len(eq_split) == 2:
                    eq2
            except UnboundLocalError as e:
                self.output.append((f"ERROR", {"latex":False}))
                print(e)
                return self.equation_interpret, self.output, self.plot

            try:
                check_numerical = self.check_solve_numerically()

                if check_numerical is not None and not self.intersect:
                    if len(eq_split) == 1:
                        self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                        self.output.append(f"{custom_latex(custom_simplify(eq1))} = 0")

                    elif len(eq_split) == 2:
                        self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                        self.output.append(f"{custom_latex(custom_simplify(eq1))} = {custom_latex(custom_simplify(eq2))}")

                    self.plot = True
                    if self.multivariate:
                        self.output.append((f"Geen snijpunt met de x-as gevonden", {"latex":False}))
                    else:
                        self.output.append(("Geen oplossing gevonden", {"latex": False}))
                    return self.equation_interpret, self.output, self.plot
                
                elif check_numerical is not None:
                    self.solutions = check_numerical

            except Exception as e:
                self.output.append((f"ERROR", {"latex":False}))
                print(e)
                return self.equation_interpret, self.output, self.plot


        except sp.SympifyError:
            self.output.append((f"Error: De ingevoerde functie klopt niet", {"latex":False}))
            return self.equation_interpret, self.output, self.plot

        except ValueError as e:
            self.output.append((f"ERROR", {"latex":False}))
            print(e)
            return self.equation_interpret, self.output, self.plot

        try:
            self.plot = True
            self.intersect = True

            if len(eq_split) == 1:
                self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                self.output.append(f"{custom_latex(custom_simplify(eq1))} = 0")

            elif len(eq_split) == 2:
                self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                self.output.append(f"{custom_latex(custom_simplify(eq1))} = {custom_latex(custom_simplify(eq2))}")


            if self.solutions.is_FiniteSet:
                if self.numerical:
                    if len(self.roots) == 1:
                        self.output.append(("(Oplossing is numeriek bepaald)", {"latex":False, "new_line":2}))
                    else:
                        self.output.append(("(Oplossingen zijn numeriek bepaald)", {"latex":False, "new_line":2}))


                if len(self.solutions) == 1:
                    if self.multivariate:
                        self.output.append((f"Het snijpunt met de $x$-as is:", {"latex":False}))
                    else:
                        self.output.append((f"De oplossing is:", {"latex":False}))


                    if self.solutions.args[0] != sp.N(self.solutions.args[0]):
                        self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solutions.args[0])} \\approx {round(sp.N(self.solutions.args[0]), 5)}")

                    else:
                        self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solutions.args[0])}")
                    

                else:
                    if self.multivariate:
                        self.output.append((f"De snijpunten met de $x$-as zijn:", {"latex":False}))
                    else:
                        self.output.append((f"De oplossingen zijn:", {"latex":False}))

                    if len(self.solutions) > 5:
                        abs_solutions= np.abs(list(self.solutions))
                        self.interval_solutions = np.array(list(self.solutions))[np.argsort(abs_solutions)[:5]]

                        self.output.remove((f"De oplossingen zijn:", {"latex":False}))
                        self.output.insert(3, (f"De eerste 5 oplossingen zijn:", {"latex":False}))

                    else:
                        self.interval_solutions = self.solutions

                    counter = 0
                    for solution in self.interval_solutions:
                        counter += 1
                        
                        if solution != sp.N(solution):
                            self.output.append(f"{counter}) \\quad {custom_latex(self.symbol)} = {custom_latex(solution)} \\approx {round(sp.N(solution), 5)}")

                        else:
                            self.output.append(f"{counter}) \\quad {custom_latex(self.symbol)} = {custom_latex(solution)}")

                if domain_string != "Reals":
                    self.output.append((f"Het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(custom_latex(domain))
            
            else:
                self.output.append((f"De oplossingen zijn:", {"latex":False, "new_line":2}))
                self.output.append(f"{custom_latex(self.symbol)} = {custom_latex(self.solutions)}")

                if isinstance(self.solutions, sp.ConditionSet):
                    self.solutions = self.solutions.base_set                

                if domain_string != "Reals":
                    self.output.append((f"Met de voorwaarde dat het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(custom_latex(domain))


                self.output.append(("Oplossingen in het domein $[0, 2\\pi]$: ", {"latex":False, "new_line":2}))
                self.interval_solutions = sp.solveset(self.eq, domain=sp.Interval(0, 2*sp.pi))
                counter = 0

                if isinstance(self.interval_solutions, sp.Set):
                    self.interval_solutions_intersect = sp.Intersection(self.interval_solutions, sp.Interval(0, 2*sp.pi))

                    if isinstance(self.interval_solutions_intersect, sp.Set):
                        counter = 0
                        self.interval_solutions_intersect = []
                        iterable = self.interval_solutions.is_iterable

                        if iterable:
                            try:
                                for solution in self.interval_solutions:
                                    pass
                            except TypeError:
                                iterable = False

                        if iterable:
                            for solution in self.interval_solutions:
    
                                if not solution.is_real:
                                    continue
                                
                                if 0 <= float(solution) <= 2 * np.pi:
                                    self.interval_solutions_intersect.append(solution)
                                else:
                                    counter += 1

                                if counter > 10:
                                    counter = 0
                                    break
                        else:
                            self.solutions = self.solve_numerically()
                            self.interval_solutions_intersect = list(self.solutions)

                            if len(self.roots) > 5:
                                self.interval_solutions_intersect = self.interval_solutions_intersect[:4]

                            if len(self.roots) == 1:
                                self.output.append(("(Oplossing is numeriek bepaald)", {"latex":False, "new_line":2}))
                            else:
                                self.output.append(("(Oplossingen zijn numeriek bepaald)", {"latex":False, "new_line":2}))

                    
                    self.interval_solutions = sp.FiniteSet(*self.interval_solutions_intersect)
                    

                    if self.interval_solutions.is_empty:
                        self.intersect = False
                        self.output = self.output[:-6]
                        self.output.append(("Geen oplossing gevonden", {"latex":False, "new_line":2}))
                        
                        return self.equation_interpret, self.output, self.plot

                for solution in self.interval_solutions:
                    counter += 1
                    if solution != sp.N(solution):
                        self.output.append(f"{counter}) \\quad {custom_latex(self.symbol)} = {custom_latex(solution)} \\approx {round(sp.N(solution), 5)}")

                    else:
                        self.output.append(f"{counter}) \\quad {custom_latex(self.symbol)} = {custom_latex(solution)}")

        except Exception as e:
            self.output.append((f"ERROR", {"latex":False}))
            print(e)

        return self.equation_interpret, self.output, self.plot
    

    def get_range(self):
        if not self.intersect:
            self.x_range = (-10, 10)
            self.y_range = (-10, 10)
            return self.x_range, self.y_range

        if not self.solutions.is_FiniteSet:
            self.x_intersect = [float(sp.N(sol)) for sol in self.interval_solutions if sp.N(self.eq1(sol)).is_real]
        
        else:
            if self.numerical and len(self.roots) > 5:
                self.x_intersect = [float(sp.N(sol)) for sol in self.interval_solutions if sp.N(self.eq1(sol)).is_real]
            else: 
                self.x_intersect = [float(sp.N(sol)) for sol in self.solutions if sp.N(self.eq1(sol)).is_real]

        self.y_intersect = [float(sp.N(self.eq1(sol))) if sp.Abs(sp.N(self.eq1(sol))) > 10**-6 else 0 for sol in self.x_intersect]

        if len(self.x_intersect) == 0:
            self.intersect = False
            self.x_range = (-10, 10)
            self.y_range = (-10, 10)
            return self.x_range, self.y_range


        intersect_xrange = float(max(self.x_intersect)) - float(min(self.x_intersect))
        intersect_yrange = float(max(self.y_intersect)) - float(min(self.y_intersect))
        self.x_range_og = (float(min(self.x_intersect)) - (intersect_xrange/3 + 2), float(max(self.x_intersect)) + (intersect_xrange/3 + 2))
        self.x_range = self.x_range_og

        self.y_range_og = (float(min(self.y_intersect)) - (intersect_yrange/3 + 2), float(max(self.y_intersect)) + (intersect_yrange/3 + 2))
        self.y_range = self.y_range_og

        return self.x_range, self.y_range


    def get_plot_data(self, x_range, dx=0.01):

        def scalar_to_array(scalar, shape):
            if np.isscalar(scalar):
                return np.full(shape, scalar).astype(float)
            return scalar.astype(float)


        def get_plottable_coords(x_coords):
            def try_func_module(module="numpy"):
                self.eq1_np = sp.lambdify(self.symbol, TR2(TR1(self.eq1(self.symbol))), module)
                self.eq2_np = sp.lambdify(self.symbol, TR2(TR1(self.eq2(self.symbol))), module)
                x_coords_np = np.array(x_coords)
                plottable_x1_coords = x_coords_np[np.isreal(scalar_to_array(self.eq1_np(x_coords_np), shape=x_coords_np.shape))]
                plottable_x2_coords = x_coords_np[np.isreal(scalar_to_array(self.eq2_np(x_coords_np), shape=x_coords_np.shape))]

                return plottable_x1_coords, plottable_x2_coords

            try:
                plottable_x1_coords, plottable_x2_coords = try_func_module(module="numpy")
            except NameError:
                try:
                    plottable_x1_coords, plottable_x2_coords = try_func_module(module="scipy")
                except NameError:
                    plottable_x1_coords, plottable_x2_coords = try_func_module(module="sympy")


            def add_endpoint(plottable_x_coords, eq):
                try:
                    domain = sp.calculus.util.continuous_domain(eq, self.symbol, domain=sp.S.Reals)

                    if (not domain.is_Interval) or (type(domain) is type(sp.Reals)):
                        return np.array(plottable_x_coords)

                    input_eq = sp.lambdify(self.symbol, eq, "sympy")
                    amt_intervals = len(domain.args) if domain.is_Union else 1
                    for i in range(amt_intervals):
                        for j in range(2):
                            if domain.args[j].is_finite and input_eq(float(domain.args[j])).is_finite and not (min(plottable_x_coords) <= domain.args[j] <= max(plottable_x_coords)):
                                    plottable_x_coords.append(float(domain.args[j]))
                                    plottable_x_coords = sorted(plottable_x_coords)

                    plottable_x_coords = np.array([x for x in plottable_x_coords if domain.args[0] <= x <= domain.args[1]])

                except (NotImplementedError, ZeroDivisionError):
                    pass

                return plottable_x_coords

            plottable_x1_coords = add_endpoint(plottable_x1_coords, sp.sympify(self.eq1(self.symbol)))
            plottable_x2_coords = add_endpoint(plottable_x2_coords, sp.sympify(self.eq2(self.symbol)))

            y1_coords = scalar_to_array(self.eq1_np(plottable_x1_coords), shape=plottable_x1_coords.shape)
            y2_coords = scalar_to_array(self.eq2_np(plottable_x2_coords), shape=plottable_x2_coords.shape)

            return list(plottable_x1_coords), list(y1_coords), list(plottable_x2_coords), list(y2_coords)

        if self.intersect and self.solutions.is_iterable:
            if self.numerical:
                self.x_intersect = sorted([float(sol) for sol in self.solutions if x_range[0] <= sol <= x_range[1]])

            else:
                if not self.solutions.is_FiniteSet:
                    self.new_interval_solutions = sp.solveset(self.eq, domain=sp.Interval(*x_range))

                else:
                    self.new_interval_solutions = [sol for sol in self.solutions if x_range[0] <= sol <= x_range[1]]

                if isinstance(self.new_interval_solutions, sp.Union) or isinstance(self.new_interval_solutions, sp.ImageSet):
                    self.new_interval_solutions_intersect = sp.Intersection(self.new_interval_solutions, sp.Interval(*x_range))

                    if isinstance(self.new_interval_solutions_intersect, sp.Intersection)  or isinstance(self.new_interval_solutions_intersect, sp.Union):
                        counter = 0
                        self.new_interval_solutions_intersect = []
                        for solution in self.new_interval_solutions:

                            if not solution.is_real:
                                continue

                            if x_range[0] <= float(solution) <= x_range[1]:
                                self.new_interval_solutions_intersect.append(solution)
                            else:
                                counter += 1

                            if counter > 10:
                                counter = 0
                                break

                    self.new_interval_solutions = sp.FiniteSet(*self.new_interval_solutions_intersect)   

                self.x_intersect = sorted([float(sp.N(sol)) for sol in self.new_interval_solutions if (sp.N(self.eq1(float(sol))).is_real and sp.N(self.eq2(float(sol))).is_real)])
            
            self.y_intersect = [float(sp.N(self.eq1(sol))) for sol in self.x_intersect]

        if self.vert_asympt_eq is None:
            self.x_coords = np.linspace(x_range[0] - 1, x_range[1] + 1, int(1/dx))

        else:
            if isinstance(self.vert_asympt_eq, list):
                self.vert_asympt = self.vert_asympt_eq
            else:
                self.vert_asympt = sp.solveset(self.vert_asympt_eq, domain=sp.Interval(*x_range))
                if isinstance(self.vert_asympt, sp.ConditionSet):
                    self.vert_asympt = self.solve_numerically(sp.lambdify(self.symbol, self.vert_asympt_eq, "sympy"))


            self.vert_asympt = [float(sol) for sol in self.vert_asympt if sp.N(sol).is_real]
            self.x_coords = segmented_linspace(x_range[0] - 1, x_range[1] + 1, self.vert_asympt, num=int(1/dx), dx=0.00001)
            

        plottable_x1_coords = []
        y1_coords = []
        plottable_x2_coords = []
        y2_coords = []

        if self.vert_asympt_eq is None:
            plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = get_plottable_coords(self.x_coords)

        else:
            for i in range(len(self.x_coords)):
                plottable_x1_coords_i, y1_coords_i, plottable_x2_coords_i, y2_coords_i = get_plottable_coords(self.x_coords[i])

                plottable_x1_coords.append(plottable_x1_coords_i)
                y1_coords.append(y1_coords_i)
                plottable_x2_coords.append(plottable_x2_coords_i)
                y2_coords.append(y2_coords_i)

        return list(plottable_x1_coords), list(y1_coords), list(plottable_x2_coords), list(y2_coords)