import sympy as sp
from sympy.simplify.fu import TR2, TR1
import numpy as np
import re
import matplotlib.pyplot as plt

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

def math_interpreter(eq_string):
    function_names = [name for name in dir(sp.functions) if not name.startswith('_')]
    abs_pattern = re.compile(r"\|([^|]+)\|")
    eq_string = re.sub(abs_pattern, r"Abs(\1)", eq_string)
    relevant_functions = [func for func in function_names if func in eq_string and func not in ["And", "Or", "Not", "Xor", "Implies", "Equivalent"]]

    # relevant_functions = [relevant_functions[i] for i in range(len(relevant_functions)) if relevant_functions[i] not in func for func in relevant_functions[:i] + relevant_functions[i+1:]]

    print(relevant_functions[1] in relevant_functions[0], relevant_functions[0] in relevant_functions[1])

    for _ in range(10):
        
        eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
        eq_string = re.sub(r'([a-zA-Z])(\d)', r'\1^\2', eq_string)
        eq_string = re.sub(r'\)(\d)', r')*\1', eq_string)
        eq_string = re.sub(r'(\d)\(', r'\1*(', eq_string)

        eq_string = re.sub(r'\)([a-zA-Z])', r')*\1', eq_string)
        eq_string = re.sub(r'([a-zA-Z])\(', r'\1*(', eq_string)
        eq_string = re.sub(r'\)\(', r')*(', eq_string)

        print(relevant_functions)
        for function_name1 in relevant_functions:
            eq_string = re.sub(r'\b' + function_name1 + r'\*(\d|[a-zA-Z])', function_name1 + r'(x)*\1', eq_string)
            eq_string = re.sub(r'\b' + function_name1 + r'(\d|[a-zA-Z])', function_name1 + r'(\1)', eq_string)
            eq_string = re.sub(r'\b' + r'(\d|[a-zA-Z])' + function_name1, r'\1*' + function_name1, eq_string)
            eq_string = re.sub(r'\b' + function_name1 + r'\*\(', function_name1 + '(', eq_string)
            eq_string = re.sub(function_name1 + r'\*\(', function_name1 + '(', eq_string)

            for function_name2 in relevant_functions:
                eq_string = re.sub(function_name1 + function_name2 + r'\((\d|[a-zA-Z])\)', rf"{function_name1}({function_name2}\1)", eq_string)
                eq_string = re.sub(function_name1 + function_name2 + r'\((\d|[a-zA-Z])\)', rf"{function_name2}({function_name1}\1)", eq_string)

    return eq_string


# superscript_mapping = {'²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁺': '+', '⁻': '-', '⁼': '=', '⁽': '(', '⁾': ')', 'ⁿ': 'n', '⁰': '0'}

# text = "This is a sample text with superscripted numbers like 2² and 3³, x²."
# result = re.sub(r'(\w+)([²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ⁰]+)', r"\1" + superscript_mapping[str(r'\2')], text)

l = 1

l = np.full()

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
