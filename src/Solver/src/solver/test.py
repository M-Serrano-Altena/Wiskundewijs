import scipy.optimize
import sympy as sp
from sympy.simplify.fu import TR2, TR1
import numpy as np
import re
import matplotlib.pyplot as plt
from sympy.printing.latex import LatexPrinter

def main():
    eq_string = "2x^2 + 1 = 9"
    eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
    eq_split = eq_string.split("=")
    print(eq_split)

    if len(eq_split) == 1:
        eq = sp.Eq(sp.sympify(eq_split[0]), 0)

    elif len(eq_split) == 2:
        eq = sp.Eq(sp.sympify(eq_split[0]), sp.sympify(eq_split[1]))

    else:
        print("Invalid equation")
        return
        
    solutions = sp.solve(eq)
    symbol = eq.free_symbols.pop()
    for solution in solutions:
        print(f"{symbol} = {solution}")

def no_frac(num):
    if isinstance(num, sp.Rational) and (abs(num.p) > 100 or abs(num.q) > 100):
        return num.evalf()
    return num

def segmented_linspace(start, end, breakpoints, num=10):
    breakpoints = list(breakpoints)
    breakpoints = sorted(breakpoints)
    breakpoints = [num - 0.01 for num in breakpoints]
    all_points = sorted([start] + breakpoints + [end])
    lists_with_breaks = [np.linspace(all_points[i], all_points[i+1], num=10) for i in range(len(all_points)-1)]
    return lists_with_breaks


def replace_func(eq_string, func_name: str='log', replace_with: str='10', amt_commas=1):
    index_func = [m.start() for m in re.finditer(func_name, eq_string)]
    if len(index_func) == 0:
        return eq_string
    
    string_split = [list(eq_string)[index_func[i-1]:index_func[i]] if i != len(index_func) else list(eq_string)[index_func[i - 1]:] for i in range(1, len(index_func) + 1) ]
    index_list = []
    nested = 0
    index = 0
    amt_commas_start = amt_commas
    for string in string_split:

        replace = True
        amt_commas = amt_commas_start
        nested_before = nested
        nested = 0
        
        for char in string:
        
            if char == '(':
                nested += 1
            elif char == ')':
                nested -= 1

            elif char == ',' and nested == 1:
                if amt_commas == 1:
                    replace = False
                else:
                    amt_commas -= 1

            if char == ')' and nested == 0:
                nested = nested_before
                if replace:
                    index_list.append(index)
                
                replace = True
                amt_commas = amt_commas_start

            index += 1
    
    additional_index = index_func[0]
    for index in index_list:
        eq_string = eq_string[:index + additional_index] + f', {replace_with}' + eq_string[index + additional_index:]
        additional_index += 2 + len(replace_with)
    
    return eq_string

def math_interpreter(eq_string):

    def insert_asterisks(match):
        char = match.group(1)
        count = len(match.group(0))
        pos = match.start()

        # Check if repeated letters are part of any relevant function name
        for func in relevant_functions:
            if eq_string[pos:pos+len(func)] == func:
                return char * count

        # Check if repeated letters are part of any constant name
        for const in constant_names:
            if eq_string[pos:pos+len(const)] == const:
                return char * count

        return '*'.join(char for _ in range(count))

    def replace_constant_symbols(eq_string):
        eq_string = re.sub(r'\b' + r'inf' + r'\b', r'oo', eq_string)
        eq_string = re.sub(r'\b' + r'infty' + r'\b', r'oo', eq_string)
        eq_string = re.sub(r'\b' + r'infinity' + r'\b', r'oo', eq_string)
        eq_string = re.sub(r'∞', r'oo', eq_string)

        eq_string = re.sub(r'π', r'pi', eq_string)

        list_superscript = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
        num = 0
        for superscript in list_superscript:
            eq_string = re.sub(superscript, str(num), eq_string)
            num += 1

        return eq_string

    eq_string = eq_string.casefold()
    function_names = [name for name in dir(sp.functions) if not name.startswith('_')]
    function_names.extend(("diff", "integrate", "limit"))

    constant_names_og = [name for name, obj in sp.__dict__.items() if isinstance(obj, (sp.Basic, sp.core.singleton.Singleton)) and not name.startswith('_') and sp.sympify(name).is_number]
    constant_names_og.extend(("inf", "infty", "infinity"))
    constant_names = [name.casefold() for name in constant_names_og]

    eq_string = replace_constant_symbols(eq_string)


    abs_pattern = re.compile(r"\|([^|]+)\|")
    eq_string = re.sub(abs_pattern, r"Abs(\1)", eq_string)
    eq_string = re.sub(r'\b' + r'abs', r'Abs', eq_string)
    eq_string = re.sub(r'\b' + r'i'  + r'\b', r'I', eq_string)
    eq_string = re.sub(r'\b' + r'e'  + r'\b', r'E', eq_string)


    relevant_functions = [func for func in function_names if func in eq_string]

    if "limit" in relevant_functions:
        relevant_functions.remove("li")
        relevant_functions.remove("im")

    for _ in range(10):
        eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
        eq_string = re.sub(r'([a-zA-Z])(\d)', r'\1^\2', eq_string)
        eq_string = re.sub(r'\)(\d)', r')*\1', eq_string)
        eq_string = re.sub(r'(\d)\(', r'\1*(', eq_string)

        eq_string = re.sub(r'\)([a-zA-Z])', r')*\1', eq_string)
        eq_string = re.sub(r'([a-zA-Z])\(', r'\1*(', eq_string)
        eq_string = re.sub(r'\)\(', r')*(', eq_string)

        eq_string = re.sub(r'([a-zA-Z])\1+', insert_asterisks, eq_string)
        eq_string = re.sub(r'\b' + r'([e])' + r'\b', r'E', eq_string)
        eq_string = re.sub(r'\b' + r'([i])' + r'\b', r'I', eq_string)
        

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

    if "limit" in relevant_functions:
        eq_string = re.sub("im" + r'\*\(', "im" + '(', eq_string)
        eq_string = re.sub("li" + r'\*\(', "li" + '(', eq_string)    

    eq_string = replace_func(eq_string, func_name='log', replace_with='10')

    for i in range(len(constant_names)):
        constant = constant_names[i]

        if re.search(r'\b' + str(constant) + r'\b', eq_string) is not None:
            if constant in constant_names and constant not in constant_names_og:
                eq_string = re.sub(r'\b' + str(constant) + r'\b', str(constant_names_og[i]), eq_string)
    
    return eq_string


def numerical_roots(eq, a=-10000, b=10000):
    x = sp.symbols('x')
    eq = eq(x)
    eq_lambda = sp.lambdify(x, eq, "numpy")
    diff_eq = sp.diff(eq, x)
    diff_eq_lambda = sp.lambdify(x, diff_eq, "numpy")

    x = np.linspace(a, b, (b-a) * 100)
    xy = np.zeros((x.shape[0], 2))
    xy[:, 0] = x
    xy[:, 1] = eq_lambda(x)

    condition = (xy[:, 1] > -0.1) & (xy[:, 1] < 0.1)
    indices = np.where(condition)[0]

    discontinuities = np.where(np.diff(indices) != 1)[0] + 1
    split_indices = np.split(indices, discontinuities)

    len_split = len(split_indices)
    roots = np.zeros(len_split)

    for i in range(len_split):
        min_index = np.argmin(np.abs(xy[split_indices[i]]), axis=0)[1]
        guess = xy[split_indices[i]][min_index, 0]
        roots[i] = round(scipy.optimize.newton(eq_lambda, guess, fprime=diff_eq_lambda), 5)        

    return roots

class CustomLatexPrinter(LatexPrinter):
    def _print_Mul(self, expr, **kwargs):
        numer, denom = expr.as_numer_denom()

        if isinstance(numer, sp.log) and isinstance(denom, sp.log):
            base = denom.args[0]

            if isinstance(base, (sp.Symbol, sp.Number)):
                arg = self._print(numer.args[0])
                base = self._print(base)

                return f' \\ ^{{{base}}} \\! \\log\\left({arg} \\right)'
            
        return super()._print_Mul(expr).replace("1 \\cdot", " ")
    

    def _print_Pow(self, expr, **kwargs):
        if expr.exp.as_numer_denom()[1] != 1 and expr != sp.root(expr.base, 1/expr.exp, evaluate=False):
            base = self._print(expr.base)
            exp = self._print(sp.simplify(expr.exp))
            return f"{base}^{{{exp}}}"

        elif expr.as_numer_denom()[1] != 1:
            expr = sp.nsimplify(expr)
            return sp.latex(expr)

        return super()._print_Pow(expr)

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
            return f"\\lim_{{{var} \\downarrow {point}}} {self._print(func)}"
        
        elif str(direction) == "-":
            return f"\\lim_{{{var} \\uparrow {point}}} {self._print(func)}"

        return super()._print_Limit(expr)


def custom_latex(expr, **kwargs):
    return CustomLatexPrinter(**kwargs).doprint(expr)



x = sp.symbols("x")
# print(custom_latex(sp.Limit('f(x)', x, 'a')))
string = "2⁰x¹⁰"
string = math_interpreter(string)
print(string)
print(custom_latex(sp.sympify(string)))
# print(custom_latex(sp.Limit(1/x, x, 0, "+")))
# print(sp.latex(sp.sympify("Abs(1/0)")))

exit()
if __name__ == "__main__":
    x = sp.symbols('x')
    f = (x-1)**2/(x-1)
    g = sp.tan(x) - 1
    eq = sp.nsimplify(sp.Eq(0, f), tolerance=10**-5)
    domain = sp.calculus.util.continuous_domain(f, x, domain=sp.S.Reals)
    # sp.pprint(domain)
    # print(domain.is_Interval)
    print(sp.solveset(eq, x, domain=sp.S.Reals))
    print(sp.sympify("1+1*4+x^0", evaluate=False))
    sp.pprint(sp.solveset(x*sp.sin(sp.sin(x)), domain=sp.S.Reals))
    # print(TR2(g))
    # print(TR2(g).as_numer_denom())

    start, end = 1, 100
    breakpoints = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    num = 10
    # print(segmented_linspace(start, end, breakpoints, num=num))

    # print([sp.N(x) for x in (sp.solve(sp.sin(x)))])

    # func = x**2/(x**3)
    # h = sp.sin(x)*sp.sin(x) + sp.cos(x)*sp.cos(x)
    # solution = sp.solve(func)
    # print((func.as_numer_denom()))
    # print(type(func.as_numer_denom()[1]))
    # print(func.as_numer_denom()[1].is_number)
    # print(sp.sympify(h, evaluate=False))
    # # print(func.subs(x, solution[0]))


    # print(domain.is_finite) 
    # # print(sp.is_finite(domain.args[0]))
    # sp.pprint(domain)
    # print(len(domain.args))

    # print(sp.pretty(domain) == "ℝ")
    # print(sp.solve(sp.Eq(f, 0.5), x))
    # sp.pprint(sp.solveset(eq, x, domain=sp.S.Reals))

    # new_line = 2 * "\n"

    # print(r"$\\n$")

    # print(sp.nsimplify(eq, tolerance=10**-7))
    
    # eq = sp.Eq(sp.cos(x)**2+sp.sin(x)**2 + x, 1)

    # solution_set = sp.solveset(sp.simplify(eq))
    # if isinstance(solution_set, sp.ConditionSet):
    #     print(f"Variable: {solution_set.sym}, Condition: {solution_set.condition}")
    # else:
    #     sp.pprint(solution_set)
        
    # main()


#================================================================================================

# from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from sympy import symbols, Eq, cos, solveset, latex

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("SymPy Solution Display")

#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)

#         layout = QVBoxLayout()
#         central_widget.setLayout(layout)

#         # Example SymPy solveset solution
#         x = symbols('x')
#         equation = Eq(sp.sin(x), 0)
        
#         # Solve the equation
#         solution_set = solveset(equation, x)

#         # Format the equation and solution using LaTeX
#         equation_latex = latex(equation)
#         solution_latex = f"Solution: ${latex(solution_set)}$"

#         # Render equation using Matplotlib
#         fig = Figure(figsize=(1, 4))
#         ax = fig.add_subplot(111)
#         ax.axis('off')  # Turn off axis
#         ax.text(0.5, 0.5, f"${equation_latex}$", ha='left', va='top', fontsize=14)
#         equation_canvas = FigureCanvas(fig)
#         layout.addWidget(equation_canvas)

#         # Render solution using Matplotlib
#         fig = Figure(figsize=(1, 4))
#         ax = fig.add_subplot(111)
#         ax.axis('off')  # Turn off axis
#         ax.text(0.5, 0.5, f"{solution_latex}", ha='left', va='top', fontsize=14)
#         solution_canvas = FigureCanvas(fig)
#         layout.addWidget(solution_canvas)

# def main():
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec()

# if __name__ == "__main__":
#     main()

#================================================================================================
