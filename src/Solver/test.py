import sympy as sp
from sympy.simplify.fu import TR2
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



if __name__ == "__main__":
    x = sp.symbols('x')
    f = sp.sin(x)/sp.cos(x)#*sp.sqrt(x)
    g = sp.tan(x) - 1
    eq = sp.nsimplify(sp.Eq(g, 0), tolerance=10**-5)
    domain = sp.calculus.util.continuous_domain(f, x, domain=sp.S.Reals)
    # sp.pprint(domain)
    # print(domain.is_Interval)
    print(f.rewrite((sp.cos, sp.sin)))
    print(TR2(g))
    print(TR2(g).as_numer_denom())

    start, end = 1, 100
    breakpoints = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    num = 10
    print(segmented_linspace(start, end, breakpoints, num=num))

    print([sp.N(x) for x in (sp.solve(sp.sin(x)))])

    l = []
    l.append([1,2])
    l.append([3,4])
    print(l)


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
