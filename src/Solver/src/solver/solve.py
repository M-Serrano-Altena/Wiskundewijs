import numpy as np
import sympy as sp
from sympy.simplify.fu import TR2, TR1
import re

def math_interpreter(eq_string):
    function_names = [name for name in dir(sp.functions) if not name.startswith('_')]
    abs_pattern = re.compile(r"\|([^|]+)\|")
    eq_string = re.sub(abs_pattern, r"Abs(\1)", eq_string)
    eq_string = re.sub(r'\b' + r'abs', r'Abs', eq_string)
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
                    
                    if not sp.solveset(self.eq, domain=sp.S.Reals).is_empty:
                        self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")
                        self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")
                        self.equation_interpret = f"{self.eq_string} = 0"
                    
                    elif not sp.simplify(self.eq).is_number:
                        self.equation_interpret = f"{self.eq_string} = 0"

            elif len(eq_split) == 2:
                eq1 = sp.sympify(eq_split[0])
                eq2 = sp.sympify(eq_split[1])

                try:
                    self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                except AttributeError:
                    self.eq = sp.Eq(eq1, eq2)

                self.equation_interpret = self.eq_string
                self.eq_string = str(self.eq)
                
                if self.eq.free_symbols:
                    self.symbol = self.eq.free_symbols.pop()
                    symbol_new = sp.symbols(str(self.symbol), real=True)
                    self.eq = self.eq.subs(self.symbol, symbol_new)
                    eq1 = eq1.subs(self.symbol, symbol_new)
                    eq2 = eq2.subs(self.symbol, symbol_new)
                    self.symbol = symbol_new

                    self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")
                    self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")
                

            else:
                self.output.append("Ongeldige Vergelijking")
                return self.equation_interpret, self.output, self.plot
            
            self.eq = sp.simplify(self.eq)
            self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)
            domain = sp.calculus.util.continuous_domain(self.eq, self.symbol, domain=sp.S.Reals)
            domain_string = sp.pretty(domain)

            if self.symbol and (sp.solve(self.eq)):
                eq12 = sp.simplify(eq1 - eq2)
                self.eq12 = sp.lambdify(self.symbol, eq12, "sympy")
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
                            

            if isinstance(self.solutions, sp.ConditionSet):
                self.eq = sp.simplify(self.solutions.condition)
                self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)


            if not sp.solve(self.eq):
                
                if sp.sympify(self.eq_string) == sp.nsimplify(sp.simplify(eq1), [sp.pi]):
                    self.eq_string = sp.sympify(self.eq_string, evaluate=False)
                else:
                    self.eq_string = sp.sympify(self.eq_string)

                
                if len(eq_split) == 1:

                    if not self.symbol:
                        solution = sp.nsimplify(eq1, [sp.pi])
                        if solution.is_number:
                            solution = sp.N(solution)
                            if int(solution) == solution:
                                solution = int(solution)

                        self.output.append(f"{sp.latex(self.eq_string)} = {sp.latex(solution)}")

                    elif sp.nsimplify(sp.simplify(eq1), [sp.pi]).is_number:
                        solution = sp.simplify(eq1)
                        self.output.append(f"{sp.latex(self.eq_string)} = {sp.latex(solution)}")
                    
                    else:
                        self.output.append(("Geen oplossing gevonden", {"latex": False}))

                elif len(eq_split) == 2:
                    lhs = sp.nsimplify(sp.simplify(eq1), [sp.pi])
                    rhs = sp.nsimplify(sp.simplify(eq2), [sp.pi])

                    if eq1 != lhs or eq2 != rhs:
                        self.output.append((f"Versimpelingen:", {"latex": False}))

                        if eq1 != lhs:
                            self.output.append(f"\\bullet \quad {sp.latex(eq1)} = {sp.latex(lhs)}")
                        if eq2 != rhs:
                            self.output.append(f"\\bullet \quad {sp.latex(eq2)} = {sp.latex(rhs)}")
                    
                    if lhs == rhs:
                        self.output.append((f"{sp.latex(lhs)} = {sp.latex(rhs)}", {"new_line":2}))
                        self.output.append(("Deze vergelijking klopt", {"latex": False}))

                    elif lhs.is_number and rhs.is_number:
                        self.output.append((f"{sp.latex(lhs)} \\neq {sp.latex(rhs)}", {"new_line":2}))
                        self.output.append(("Deze vergelijking klopt niet", {"latex": False}))

                    else:
                        self.output.append(("Geen oplossing gevonden", {"latex": False}))

                return self.equation_interpret, self.output, self.plot
            
            self.plot = True

            if len(eq_split) == 1:
                self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                self.output.append(f"{sp.latex(sp.simplify(eq1)).replace('log', 'ln')} = 0")

            elif len(eq_split) == 2:
                self.output.append((f"Vereenvoudigde Vergelijking:", {"latex": False}))
                self.output.append(f"{sp.latex(sp.simplify(eq1)).replace('log', 'ln')} = {sp.latex(sp.simplify(eq2)).replace('log', 'ln')}")


            if self.solutions.is_FiniteSet:
                if len(self.solutions) == 1:
                    self.output.append((f"De oplossing is:", {"latex":False, "new_line":2}))
                    self.output.append(f"{sp.latex(self.symbol)} = {sp.latex(self.solutions.args[0]).replace('log', 'ln')}")

                else:
                    self.output.append((f"De oplossingen zijn:", {"latex":False, "new_line":2}))
                    counter = 0
                    for solution in self.solutions:
                        counter +=1
                        self.output.append(f"{counter}) \quad {sp.latex(self.symbol)} = {sp.latex(solution).replace('log', 'ln')}")

                if domain_string != "ℝ":
                    self.output.append((f"Het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(sp.latex(domain))
            
            else:
                self.output.append((f"De oplossingen zijn:", {"latex":False, "new_line":2}))
                self.output.append(f"{sp.latex(self.symbol)} = {sp.latex(self.solutions)}")

                if isinstance(self.solutions, sp.ConditionSet):
                    self.solutions = self.solutions.base_set                

                if domain_string != "ℝ":
                    self.output.append((f"Met de voorwaarde dat het domein van ${self.symbol}$ is:", {"latex":False, "new_line":2}))
                    self.output.append(sp.latex(domain))


                self.output.append(("Oplossingen in het domein $[0, 2\pi]$: ", {"latex":False, "new_line":2}))
                self.interval_solutions = sp.solveset(self.eq, domain=sp.Interval(0, 2*sp.pi))
                counter = 0
                for solution in self.interval_solutions:
                    counter += 1
                    self.output.append(f"{counter}) \quad {sp.latex(self.symbol)} = {sp.latex(solution)}")        
        
        except Exception as e:
            self.output.append((f"Error: {str(e)}", {"latex":False}))
            print(e)
    
        return self.equation_interpret, self.output, self.plot
    

    def get_range(self):
        if not self.solutions.is_FiniteSet:
            self.x_intersect = [sol for sol in sp.solveset(self.eq, domain=sp.Interval(0, 2*sp.pi))]
            self.y_intersect = [self.eq1(sol) for sol in self.x_intersect]
        
        else:
            self.x_intersect = [float(sol) for sol in self.solutions]
            self.y_intersect = [float(self.eq1(sol)) for sol in self.solutions]


        intersect_xrange = float(max(self.x_intersect)) - float(min(self.x_intersect))
        intersect_yrange = float(max(self.y_intersect)) - float(min(self.y_intersect))
        self.x_range_og = (float(min(self.x_intersect)) - (intersect_xrange/3 + 2), float(max(self.x_intersect)) + (intersect_xrange/3 + 2))
        self.x_range = self.x_range_og

        self.y_range_og = (float(min(self.y_intersect)) - (intersect_yrange/3 + 2), float(max(self.y_intersect)) + (intersect_yrange/3 + 2))
        self.y_range = self.y_range_og

        return self.x_range, self.y_range


    def get_plot_data(self, x_range):

        def get_plottable_coords(x_coords):
            plottable_x1_coords = [x for x in x_coords if sp.N(self.eq1(x)).is_real]
            plottable_x2_coords = [x for x in x_coords if sp.N(self.eq2(x)).is_real]      

            def add_endpoint(plottable_x_coords, eq):
                domain = sp.calculus.util.continuous_domain(eq, self.symbol, domain=sp.S.Reals)
                

                if (not domain.is_Interval) or (type(domain) is type(sp.Reals)):
                    return plottable_x_coords

                input_eq = sp.lambdify(self.symbol, eq, "sympy")
                amt_intervals = len(domain.args) if domain.is_Union else 1
                for i in range(amt_intervals):
                    sub_domain = domain.args[i] if domain.is_Union else domain
                    for j in range(2):
                        if domain.args[j].is_finite and input_eq(float(domain.args[j])).is_finite and not (min(plottable_x_coords) <= domain.args[j] <= max(plottable_x_coords)):
                                plottable_x_coords.append(float(domain.args[j]))
                                plottable_x_coords = sorted(plottable_x_coords)

                plottable_x_coords = [x for x in plottable_x_coords if domain.args[0] <= x <= domain.args[1]]   

                return plottable_x_coords

            plottable_x1_coords = add_endpoint(plottable_x1_coords, sp.sympify(self.eq1(self.symbol)))
            plottable_x2_coords = add_endpoint(plottable_x2_coords, sp.sympify(self.eq2(self.symbol)))

            y1_coords = [float(self.eq1(x)) for x in plottable_x1_coords]
            y2_coords = [float(self.eq2(x)) for x in plottable_x2_coords]

            return plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords


        if self.solutions.is_iterable:
            self.x_intersect = sorted([float(sol) for sol in sp.solveset(self.eq, domain=sp.Interval(*x_range)) if (sp.N(self.eq1(float(sol))).is_real and sp.N(self.eq2(float(sol))).is_real)])
            self.y_intersect = [float(self.eq1(sol)) for sol in self.x_intersect]

        if self.vert_asympt_eq is None:
            self.x_coords = np.linspace(x_range[0] - 1, x_range[1] + 1, 100)

        else:
            if isinstance(self.vert_asympt_eq, list):
                self.vert_asympt = self.vert_asympt_eq
            else:
                self.vert_asympt = sp.solveset(self.vert_asympt_eq, domain=sp.Interval(*x_range))

            self.vert_asympt = [float(sol) for sol in self.vert_asympt if sp.N(sol).is_real]
            num = int(round(50/len(self.vert_asympt))) if 0 < len(self.vert_asympt) < 5 else 10
            self.x_coords = segmented_linspace(x_range[0] - 1, x_range[1] + 1, self.vert_asympt, num=num, dx=0.00001)

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

        return plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords