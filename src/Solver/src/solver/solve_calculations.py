import numpy as np
import sympy as sp
from sympy.simplify.fu import TR2, TR1
import re
import scipy.optimize
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def math_interpreter(eq_string):
    eq_string = eq_string.casefold()
    function_names = [name for name in dir(sp.functions) if not name.startswith('_')]
    abs_pattern = re.compile(r"\|([^|]+)\|")
    eq_string = re.sub(abs_pattern, r"Abs(\1)", eq_string)
    eq_string = re.sub(r'\b' + r'abs', r'Abs', eq_string)
    eq_string = re.sub(r'\b' + r'i', r'I', eq_string)
    relevant_functions = [func for func in function_names if func in eq_string]

    for _ in range(10):
        eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
        eq_string = re.sub(r'([a-zA-Z])(\d)', r'\1^\2', eq_string)
        eq_string = re.sub(r'\)(\d)', r')*\1', eq_string)
        eq_string = re.sub(r'(\d)\(', r'\1*(', eq_string)

        eq_string = re.sub(r'\)([a-zA-Z])', r')*\1', eq_string)
        eq_string = re.sub(r'([a-zA-Z])\(', r'\1*(', eq_string)
        eq_string = re.sub(r'\)\(', r')*(', eq_string)

        eq_string = re.sub(r'\b' + r'([a-zA-Z])\1', r'\1*\1', eq_string)
        eq_string = re.sub(r'\b' + r'([e])' + r'\b', r'E', eq_string)
        

        for function_name1 in relevant_functions:
            for function_name2 in relevant_functions:
                eq_string = re.sub(function_name1 + function_name2 + r'\((.*?)\)', rf"{function_name1}({function_name2}\1)", eq_string)
                eq_string = re.sub(function_name2 + function_name1 + r'\((.*?)\)', rf"{function_name2}({function_name1}\1)", eq_string)

            eq_string = re.sub(function_name1 + r'\*' + r'(?!(?:' + '|'.join(map(re.escape, relevant_functions)) + r'))(\d|[a-zA-Z])', function_name1 + r'(x)*\1', eq_string)
            eq_string = re.sub(function_name1 + r'(?!(?:' + '|'.join(map(re.escape, relevant_functions)) + r'))(\d|[a-zA-Z])', function_name1 + r'(\1)', eq_string)
            eq_string = re.sub(r'\b' + r'(?!(?:' + '|'.join(map(re.escape, relevant_functions)) + r'))(\d|[a-zA-Z])' + function_name1, r'\1*' + function_name1, eq_string)
            eq_string = re.sub(function_name1 + r'\*\(', function_name1 + '(', eq_string)
            
            for function_name2 in relevant_functions:
                eq_string = re.sub(function_name1 + function_name2 + r'\((.*?)\)', rf"{function_name1}({function_name2}(\1))", eq_string)
                eq_string = re.sub(function_name2 + function_name1 + r'\((.*?)\)', rf"{function_name2}({function_name1}(\1))", eq_string)

    return eq_string

def segmented_linspace(start, end, breakpoints, num=10, dx=0.01):
    breakpoints = list(breakpoints)
    all_points = sorted([start] + breakpoints + [end])
    lists_with_breaks = [np.linspace(all_points[i] + dx, all_points[i+1] - dx, num) for i in range(len(all_points)-1)]
    return lists_with_breaks

def trig_simp(x):
    return TR1(TR2(x))

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

    def numerical_roots(self, eq, a=-10000, b=10000, dx=0.01, solve_method="newton", dy=0.1, use_scale_factor:bool=False, default_func:bool=True):
        x = sp.symbols('x')
        eq = eq(x)
        eq_lambda = sp.lambdify(x, eq, "numpy")
        diff_eq = sp.diff(eq, x)
        diff_eq_lambda = sp.lambdify(x, diff_eq, "numpy")

        x = np.linspace(a, b, (b-a) * int(1/dx))
        xy = np.zeros((x.shape[0], 2))
        xy[:, 0] = x
        xy[:, 1] = eq_lambda(x)
        xy = xy[~np.isnan(xy[:,1]) & ~np.isinf(xy[:,1])]

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
                eq1 = sp.sympify(eq_split[0])
                eq2 = 0

                try:
                    self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                except AttributeError:
                    self.eq = eq1

                self.equation_interpret = self.eq_string

                if eq1.free_symbols:
                    self.symbol = eq1.free_symbols.pop()
                    symbol_new = sp.symbols(str(self.symbol), real=True)
                    self.eq = self.eq.subs(self.symbol, symbol_new)
                    eq1 = eq1.subs(self.symbol, symbol_new)
                    self.symbol = symbol_new

                    self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")
                    self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")
                    
                    if not sp.solveset(self.eq, domain=sp.S.Reals).is_empty:
                        self.equation_interpret = f"{self.eq_string} = 0"
                    
                    elif not sp.simplify(self.eq).is_number:
                        self.equation_interpret = f"{self.eq_string} = 0"

            elif len(eq_split) == 2:
                eq1 = sp.sympify(eq_split[0])
                eq2 = sp.sympify(eq_split[1])
                eq12 = eq1 - eq2

                try:
                    self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                except AttributeError:
                    self.eq = sp.Eq(eq1, eq2)

                self.equation_interpret = self.eq_string
                self.eq_string = str(self.eq)
                
                if eq12.free_symbols:
                    self.symbol = eq12.free_symbols.pop()
                    symbol_new = sp.symbols(str(self.symbol), real=True)
                    self.eq = self.eq.subs(self.symbol, symbol_new)
                    eq1 = eq1.subs(self.symbol, symbol_new)
                    eq2 = eq2.subs(self.symbol, symbol_new)
                    self.symbol = symbol_new

                    self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")
                    self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")
                

            else:
                self.output.append(("Ongeldige Vergelijking", {"latex": False}))
                return self.equation_interpret, self.output, self.plot
            
            self.eq = sp.simplify(self.eq)
            self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)
            
            if self.symbol:
                domain = sp.calculus.util.continuous_domain(self.eq, self.symbol, domain=sp.S.Reals)
                domain_string = str(domain)

                eq12 = sp.simplify(eq1 - eq2)
                self.eq12 = sp.lambdify(self.symbol, eq12, "sympy")


            if self.symbol and (sp.solve(self.eq)):
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

            if not sp.solve(self.eq) and not self.numerical:
                
                if sp.sympify(self.eq_string) == sp.nsimplify(sp.simplify(eq1), [sp.pi]):
                    self.eq_string = sp.sympify(self.eq_string, evaluate=False)
                else:
                    self.eq_string = sp.sympify(self.eq_string)

                
                if len(eq_split) == 1:

                    if not self.symbol:
                        solution = sp.nsimplify(eq1, [sp.pi])
                        if solution.is_number:

                            if solution == sp.N(solution):
                                equals_sign = '='
                            else:
                                equals_sign = '\\approx'

                            solution = sp.N(solution)
                            try:
                                if int(solution) == solution:
                                    solution = int(solution)

                            except TypeError:

                                real_part, imag_part = solution.as_real_imag()

                                if sp.Integer(real_part) == real_part and sp.Integer(imag_part) == imag_part:
                                    solution = sp.Add(sp.Integer(real_part), sp.Mul(sp.Integer(imag_part), sp.I))

                                if real_part == sp.nsimplify(eq1, [sp.pi]).as_real_imag()[0] and imag_part == sp.nsimplify(eq1, [sp.pi]).as_real_imag()[1]:
                                    equals_sign = '='

                                    


                        
                        if eq1 != self.eq_string and equals_sign != "=":
                            self.output.append(f"{sp.latex(self.eq_string)} = {sp.latex(eq1)} {equals_sign} {sp.latex(solution)}")

                        else:
                            self.output.append(f"{sp.latex(self.eq_string)} {equals_sign} {sp.latex(solution)}")

                    elif sp.nsimplify(sp.simplify(eq1), [sp.pi]).is_number:
                        solution = sp.simplify(eq1)
                        if solution != sp.N(solution):
                            self.output.append(f"{sp.latex(self.eq_string)} = {sp.latex(solution)} \\approx {round(sp.N(solution), 5)}")
                        
                        else:
                            self.output.append(f"{sp.latex(self.eq_string)} = {sp.latex(solution)}")
                        

                    else:
                        self.output.append(("Geen oplossing gevonden", {"latex": False}))
                        self.plot = True


                elif len(eq_split) == 2:
                    lhs = sp.nsimplify(sp.simplify(eq1), [sp.pi])
                    rhs = sp.nsimplify(sp.simplify(eq2), [sp.pi])

                    if eq1 != lhs or eq2 != rhs:
                        self.output.append((f"Versimpelingen:", {"latex": False}))

                        if eq1 != lhs:
                            self.output.append(f"\\bullet \\quad {sp.latex(eq1)} = {sp.latex(lhs)}")
                        if eq2 != rhs:
                            self.output.append(f"\\bullet \\quad {sp.latex(eq2)} = {sp.latex(rhs)}")
                    
                    if lhs == rhs:
                        self.output.append((f"{sp.latex(lhs)} = {sp.latex(rhs)}", {"new_line":2}))
                        self.output.append(("Deze vergelijking klopt", {"latex": False}))

                    elif lhs.is_number and rhs.is_number:
                        self.output.append((f"{sp.latex(lhs)} \\neq {sp.latex(rhs)}", {"new_line":2}))
                        self.output.append(("Deze vergelijking klopt niet", {"latex": False}))

                    else:
                        self.output.append(("Geen oplossing gevonden", {"latex": False}))
                        self.plot = True

                return self.equation_interpret, self.output, self.plot
            
        except NotImplementedError:
            check_numerical = self.check_solve_numerically()

            if check_numerical is not None and not self.intersect:
                self.plot = True
                self.output.append(("Geen oplossing gevonden", {"latex": False}))
                return self.equation_interpret, self.output, self.plot
            
            elif check_numerical is not None:
                self.solutions = check_numerical

        except sp.SympifyError:
            self.output.append((f"Error: De ingevoerde functie klopt niet", {"latex":False}))
            return self.equation_interpret, self.output, self.plot

        except Exception as e:
            self.output.append((f"ERROR", {"latex":False}))
            print(e)
            return self.equation_interpret, self.output, self.plot

        try:
            self.plot = True
            self.intersect = True

            if len(eq_split) == 1:
                self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                self.output.append(f"{sp.latex(sp.simplify(eq1)).replace('log', 'ln')} = 0")

            elif len(eq_split) == 2:
                self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                self.output.append(f"{sp.latex(sp.simplify(eq1)).replace('log', 'ln')} = {sp.latex(sp.simplify(eq2)).replace('log', 'ln')}")


            if self.solutions.is_FiniteSet:
                if self.numerical:
                    if len(self.roots) == 1:
                        self.output.append(("(Oplossing is numeriek bepaald)", {"latex":False, "new_line":2}))
                    else:
                        self.output.append(("(Oplossingen zijn numeriek bepaald)", {"latex":False, "new_line":2}))


                if len(self.solutions) == 1:
                    self.output.append((f"De oplossing is:", {"latex":False}))

                    if self.solutions.args[0] != sp.N(self.solutions.args[0]):
                        self.output.append(f"{sp.latex(self.symbol)} = {sp.latex(self.solutions.args[0]).replace('log', 'ln')} \\approx {round(sp.N(self.solutions.args[0]), 5)}")

                    else:
                        self.output.append(f"{sp.latex(self.symbol)} = {sp.latex(self.solutions.args[0]).replace('log', 'ln')}")
                    

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
                            self.output.append(f"{counter}) \\quad {sp.latex(self.symbol)} = {sp.latex(solution).replace('log', 'ln')} \\approx {round(sp.N(solution), 5)}")

                        else:
                            self.output.append(f"{counter}) \\quad {sp.latex(self.symbol)} = {sp.latex(solution).replace('log', 'ln')}")

                if domain_string != "Reals":
                    self.output.append((f"Het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(sp.latex(domain))
            
            else:
                self.output.append((f"De oplossingen zijn:", {"latex":False, "new_line":2}))
                self.output.append(f"{sp.latex(self.symbol)} = {sp.latex(self.solutions).replace('log', 'ln')}")

                if isinstance(self.solutions, sp.ConditionSet):
                    self.solutions = self.solutions.base_set                

                if domain_string != "Reals":
                    self.output.append((f"Met de voorwaarde dat het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(sp.latex(domain))


                self.output.append(("Oplossingen in het domein $[0, 2\\pi]$: ", {"latex":False, "new_line":2}))
                self.interval_solutions = sp.solveset(self.eq, domain=sp.Interval(0, 2*sp.pi))
                counter = 0

                if isinstance(self.interval_solutions, sp.Union) or isinstance(self.interval_solutions, sp.ImageSet):
                    self.interval_solutions_intersect = sp.Intersection(self.interval_solutions, sp.Interval(0, 2*sp.pi))

                    if isinstance(self.interval_solutions_intersect, sp.Intersection) or isinstance(self.interval_solutions_intersect, sp.Union):
                        counter = 0
                        self.interval_solutions_intersect = []

                        if self.interval_solutions.is_iterable:
                            for solution in self.interval_solutions:
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
                        self.output = []
                        self.output.append(("Geen oplossing gevonden", {"latex": False}))
                        
                        return self.equation_interpret, self.output, self.plot

                for solution in self.interval_solutions:
                    counter += 1
                    if solution != sp.N(solution):
                        self.output.append(f"{counter}) \\quad {sp.latex(self.symbol)} = {sp.latex(solution).replace('log', 'ln')} \\approx {round(sp.N(solution), 5)}")

                    else:
                        self.output.append(f"{counter}) \\quad {sp.latex(self.symbol)} = {sp.latex(solution).replace('log', 'ln')}")

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
            self.x_intersect = [sol for sol in self.interval_solutions]
        
        else:
            if self.numerical and len(self.roots) > 5:
                self.x_intersect = [float(sol) for sol in self.interval_solutions]
            else: 
                self.x_intersect = [float(sol) for sol in self.solutions]


        self.y_intersect = [float(self.eq1(sol)) for sol in self.x_intersect]


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
            self.eq1_np = sp.lambdify(self.symbol, self.eq1(self.symbol), "numpy")
            self.eq2_np = sp.lambdify(self.symbol, self.eq2(self.symbol), "numpy")
            x_coords_np = np.array(x_coords)
            plottable_x1_coords = x_coords_np[np.isreal(scalar_to_array(self.eq1_np(x_coords_np), shape=x_coords_np.shape))]
            plottable_x2_coords = x_coords_np[np.isreal(scalar_to_array(self.eq2_np(x_coords_np), shape=x_coords_np.shape))]

            def add_endpoint(plottable_x_coords, eq):
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
                return plottable_x_coords

            plottable_x1_coords = add_endpoint(plottable_x1_coords, sp.sympify(self.eq1(self.symbol)))
            plottable_x2_coords = add_endpoint(plottable_x2_coords, sp.sympify(self.eq2(self.symbol)))

            y1_coords = scalar_to_array(self.eq1_np(plottable_x1_coords), shape=plottable_x1_coords.shape)
            y2_coords = scalar_to_array(self.eq2_np(plottable_x2_coords), shape=plottable_x2_coords.shape)

            return list(plottable_x1_coords), list(y1_coords), list(plottable_x2_coords), list(y2_coords)

        if self.intersect and self.solutions.is_iterable:
            if self.numerical:
                self.x_intersect = sorted([float(sol) for sol in self.solutions  if x_range[0] <= sol <= x_range[1]])

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
                            if x_range[0] <= float(solution) <= x_range[1]:
                                self.new_interval_solutions_intersect.append(solution)
                            else:
                                counter += 1

                            if counter > 10:
                                counter = 0
                                break

                    self.new_interval_solutions = sp.FiniteSet(*self.new_interval_solutions_intersect)   

                self.x_intersect = sorted([float(sol) for sol in self.new_interval_solutions if (sp.N(self.eq1(float(sol))).is_real and sp.N(self.eq2(float(sol))).is_real)])
            
            self.y_intersect = [float(self.eq1(sol)) for sol in self.x_intersect]

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
            self.x_coords = segmented_linspace(x_range[0] - 1, x_range[1] + 1, self.vert_asympt, num=int(30/dx), dx=0.00001)
            

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