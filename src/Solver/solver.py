import sys
from PySide6 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import sympy as sp
from sympy.simplify.fu import TR2
import re
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

def no_frac(num):
    if isinstance(num, sp.Rational) and (abs(num.p) > 100 or abs(num.q) > 100):
        return round(num.evalf(), 4)
    return num

def math_interpreter(eq_string):
    function_names = [name for name in dir(sp.functions) if not name.startswith('_')]
    function_regex = '|'.join(r'\b' + name + r'\b' for name in function_names)

    
    eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
    eq_string = re.sub(r'\)(\d)', r')*\1', eq_string)
    eq_string = re.sub(r'(\d)\(', r'\1*(', eq_string)

    eq_string = re.sub(r'\)([a-zA-Z])', r')*\1', eq_string)
    eq_string = re.sub(r'([a-zA-Z])\(', r'\1*(', eq_string)
    eq_string = re.sub(r'\)\(', r')*(', eq_string)

    for function_name in function_names:
        eq_string = re.sub(r'\b' + function_name + r'\*\(', function_name + '(', eq_string)

    return eq_string

def segmented_linspace(start, end, breakpoints, num=10, dx=0.01):
    breakpoints = list(breakpoints)
    all_points = sorted([start] + breakpoints + [end])
    lists_with_breaks = [np.linspace(all_points[i] + dx, all_points[i+1] - dx, num) for i in range(len(all_points)-1)]
    return lists_with_breaks


class UserInterface(QtWidgets.QMainWindow):
    """Graphical User interface
    """

    def __init__(self):
        """initialise values and create widgets"""
        super().__init__()
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("bottom", "x-as")
        self.plot_widget.setLabel("left", "y-as")
        self.plot_widget.setTitle("Vergelijkingen Plot")
        self.legend = self.plot_widget.addLegend(offset=(7, 5))
        self.plot_widget.hideButtons()

        self.start = False

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        hbox = QtWidgets.QHBoxLayout(central_widget)
        self.vbox1 = QtWidgets.QVBoxLayout()
        hbox.addLayout(self.vbox1)

        hbox.addWidget(self.plot_widget)

        equation_label = QtWidgets.QLabel("Voer vergelijking in:")
        self.vbox1.addWidget(equation_label)

        self.equation_input = QtWidgets.QLineEdit()
        self.vbox1.addWidget(self.equation_input)

        self.equation_input.setPlaceholderText("bijv. 2x^2 + 1 = 9")
        self.equation_input.returnPressed.connect(self.solve_equation)
        self.equation_input.setFocus()

        self.equation_input.setStyleSheet("QLineEdit { background-color: white }")
        self.equation_input.setStyleSheet("QLineEdit { color: black }")
        self.equation_input.setStyleSheet("QLineEdit { border: 2px solid black }")

        self.solve_button = QtWidgets.QPushButton("Vergelijking Oplossen")
        self.vbox1.addWidget(self.solve_button)

        self.equation_output_label = QtWidgets.QLabel("Interpretatie:")
        self.vbox1.addWidget(self.equation_output_label)

        self.equation_output = QtWidgets.QLineEdit()
        self.equation_output.setReadOnly(True)
        self.vbox1.addWidget(self.equation_output)

        answer_label = QtWidgets.QLabel("Antwoord:")
        self.vbox1.addWidget(answer_label)

        self.create_fig()        

        self.solve_button.clicked.connect(self.solve_equation)

        self.plot_widget.sigXRangeChanged.connect(self.update_range)
        self.plot_widget.sigYRangeChanged.connect(self.update_range)



    def create_fig(self, text="", fig_size=(5, 4)):
        try:
            self.vbox1.removeWidget(self.canvas_answer)
            self.canvas_answer.deleteLater()

        except AttributeError:
            pass

        fig_answer = Figure(figsize=fig_size)
        ax_answer = fig_answer.add_subplot(111)
        ax_answer.axis("off")
        self.solution_text = ax_answer.text(-0.14/5 * fig_size[0], 1.18, text, fontsize=11, ha="left", va="top", wrap=False)
        self.canvas_answer = FigureCanvas(fig_answer)
        self.vbox1.addWidget(self.canvas_answer)

    def add_solution_text(self, new_text, new_line=True, latex=True):
        if (type(new_line) is not bool) and (type(new_line) is not int):
            raise TypeError("new_line must be a boolean or an integer")
        
        if type(latex) is not bool:
            raise TypeError("latex must be a boolean")

        if latex:
            if new_line and type(new_line) is not int:
                updated_text = f"{self.solution_text.get_text()}\n${new_text}$"

            elif not new_line:
                updated_text = f"{self.solution_text.get_text()}${new_text}$"

            elif type(new_line) is int:
                amt_new_line = new_line * "\n"
                updated_text = f"{self.solution_text.get_text()}{amt_new_line}${new_text}$"
        
        else:
            if new_line and type(new_line) is not int:
                updated_text = f"{self.solution_text.get_text()}\n{new_text}"

            elif not new_line:
                updated_text = f"{self.solution_text.get_text()}{new_text}"

            elif type(new_line) is int:
                amt_new_line = new_line * "\n"
                updated_text = f"{self.solution_text.get_text()}{amt_new_line}{new_text}"

        self.solution_text.set_text(updated_text)
        return updated_text

    def clear_solution_text(self):
        self.solution_text.set_text("")


    def solve_equation(self):
        """Solve the equation and display the results
        """
        self.vert_asympt = None
        self.vert_asympt_eq = None
        self.start = True

        self.plot_widget.sigXRangeChanged.disconnect(self.update_range)
        self.plot_widget.sigYRangeChanged.disconnect(self.update_range)

        self.plot_widget.setXRange(-10, 10)
        self.plot_widget.setYRange(-10, 10)

        self.plot_widget.clear()
        self.legend.setBrush('white')
        self.legend.setPen("white")
        eq_string = self.equation_input.text()
        
        self.create_fig()

        try:
            eq_string = math_interpreter(eq_string)
            self.eq_string = eq_string

            eq_split = eq_string.split("=")

            if len(eq_split) == 1:
                eq1 = sp.sympify(eq_split[0])
                eq2 = 0
                self.symbol = None

                try:
                    self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                except AttributeError:
                    self.eq = eq1


                if eq1.free_symbols:
                    self.symbol = eq1.free_symbols.pop()
                    if not sp.solveset(self.eq, domain=sp.S.Reals).is_empty:
                        self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")
                        self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")
                        self.equation_output.setText(f"{eq_string} = 0")

                    else:
                        self.equation_output.setText(eq_string)

                else:
                    self.equation_output.setText(eq_string)

            elif len(eq_split) == 2:
                eq1 = sp.sympify(eq_split[0])
                eq2 = sp.sympify(eq_split[1])
                self.symbol = None

                try:
                    self.eq = sp.nsimplify(sp.Eq(eq1, eq2), tolerance=10**-7)
                except AttributeError:
                    self.eq = sp.Eq(eq1, eq2)
  

                if eq1.free_symbols:
                    self.symbol = self.eq.free_symbols.pop()
                    self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")
                    self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")

                self.equation_output.setText(eq_string)

            else:
                self.solution_text.set_color("red")
                self.add_solution_text("Ongeldige vergelijking", latex=False)

                self.equation_input.setFocus()
                self.equation_input.selectAll()

                self.plot_widget.sigXRangeChanged.connect(self.update_range)
                self.plot_widget.sigYRangeChanged.connect(self.update_range)
                return
            
            self.eq = sp.simplify(self.eq)
            self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)
            domain = sp.calculus.util.continuous_domain(self.eq, self.symbol, domain=sp.S.Reals)
            domain_string = sp.pretty(domain)


            eq12 = sp.simplify(eq1 - eq2)
            if self.symbol:
                if len(eq_split) == 1 and TR2(eq1) != eq1:
                    self.vert_asympt_eq = TR2(eq1).as_numer_denom()[1]

            elif len(eq_split) == 2 and TR2(eq12) != eq12:
                self.vert_asympt_eq = TR2(eq12).as_numer_denom()[1]


            if isinstance(self.solutions, sp.ConditionSet):
                self.eq = sp.simplify(self.solutions.condition)
                self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)



            if not [sol for sol in sp.solve(self.eq) if sol.is_real]:
                try:
                    if not sp.solve(self.eq):
                        if len(eq_split) == 1:

                            if not self.symbol:
                                solution = sp.nsimplify(eq1, [sp.pi])
                                self.add_solution_text(f"{sp.latex(eq_string)} = {sp.latex(solution)}")


                            else:
                                solution = sp.simplify(eq1)
                                self.add_solution_text(f"{sp.latex(eq_string)} = {sp.latex(solution)}")

                        elif len(eq_split) == 2:
                            lhs = sp.nsimplify(eq1, [sp.pi])
                            rhs = sp.nsimplify(eq2, [sp.pi])
                            
                            if lhs == rhs:
                                self.add_solution_text(f"{sp.latex(lhs)} = {sp.latex(rhs)}")
                                self.add_solution_text("Deze vergelijking klopt", latex=False)

                            elif sp.simplify(lhs) == sp.simplify(rhs):
                                lhs = sp.simplify(lhs)
                                rhs = sp.simplify(rhs)
                                self.add_solution_text(f"{sp.latex(lhs)} = {sp.latex(rhs)}")
                                self.add_solution_text("Deze vergelijking klopt", latex=False)

                            else:
                                self.add_solution_text(f"{sp.latex(lhs)} \\neq {sp.latex(rhs)}")
                                self.add_solution_text("Deze vergelijking klopt niet", latex=False)
   
                    else:
                        raise Exception

                except Exception:
                    self.add_solution_text("Geen oplossing gevonden", latex=False)

                self.equation_input.setFocus()
                self.equation_input.selectAll()

                self.plot_widget.sigXRangeChanged.connect(self.update_range)
                self.plot_widget.sigYRangeChanged.connect(self.update_range)

                return
            

            if len(eq_split) == 1:
                self.add_solution_text(f"Vereenvoudigde Vergelijking:", latex=False)
                self.add_solution_text(f"{sp.latex(sp.simplify(eq1))} = 0")

            elif len(eq_split) == 2:
                self.add_solution_text(f"Vereenvoudigde Vergelijking:", latex=False)
                self.add_solution_text(f"{sp.latex(sp.simplify(eq1))} = {sp.latex(sp.simplify(eq2))}")


            if self.solutions.is_FiniteSet:
                if len(self.solutions) == 1:
                    self.add_solution_text(f"De oplossing is:", latex=False, new_line=3)
                    self.add_solution_text(f"{sp.latex(self.symbol)} = {sp.latex(self.solutions.args[0])}")

                else:
                    self.add_solution_text(f"De oplossingen zijn:", latex=False, new_line=2)
                    counter = 0
                    for solution in self.solutions:
                        counter +=1
                        self.add_solution_text(f"{counter}) \quad {sp.latex(self.symbol)} = {sp.latex(solution)}")
            
            else:
                if isinstance(self.solutions, sp.ConditionSet):
                    self.solutions = self.solutions.base_set

                self.add_solution_text("De oplossingen zijn:", latex=False, new_line=2)
                self.add_solution_text(f"{sp.latex(self.symbol)} = {sp.latex(self.solutions)}")

                if domain_string != "ℝ":
                    self.add_solution_text(f"Met de voorwaarde dat het domein van ${self.symbol}$ is:", latex=False, new_line=2)
                    self.add_solution_text(sp.latex(domain))


                self.add_solution_text("In het domein $[0, 2\pi]$: ", latex=False, new_line=2)
                self.interval_solutions = sp.solveset(self.eq, domain=sp.Interval(0, 2*sp.pi))
                counter = 0
                for solution in self.interval_solutions:
                    counter += 1
                    self.add_solution_text(f"{counter}) \quad {sp.latex(self.symbol)} = {sp.latex(solution)}")
 
            self.set_range()
            self.plot()

       
        
        except Exception as e:
            self.solution_text.set_color("red")
            self.add_solution_text(f"Fout: {str(e)}", latex=False)
            print(e)

        self.equation_input.setFocus()
        self.equation_input.selectAll()

        self.plot_widget.sigXRangeChanged.connect(self.update_range)
        self.plot_widget.sigYRangeChanged.connect(self.update_range)

    
    def set_range(self):
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

        self.plot_widget.setXRange(*self.x_range)
        self.plot_widget.setYRange(*self.y_range)

        self.plot_widget.getViewBox().setDefaultPadding(-0.1)


    def get_plottable(self, x_coords):
        plottable_x1_coords = [x for x in x_coords if sp.N(self.eq1(x)).is_real]
        plottable_x2_coords = [x for x in x_coords if sp.N(self.eq2(x)).is_real]      

        def add_endpoint(plottable_x_coords, eq):
            domain = sp.calculus.util.continuous_domain(eq, self.symbol, domain=sp.S.Reals)

            if (not domain.is_Interval) or (type(domain) is type(sp.Reals)):
                return plottable_x_coords
    
            for i in range(2):
                if domain.args[i].is_finite and not (min(plottable_x_coords) <= domain.args[i] <= max(plottable_x_coords)):
                    plottable_x_coords.append(float(domain.args[i]))
                    plottable_x_coords = sorted(plottable_x_coords)

            plottable_x_coords = [x for x in plottable_x_coords if domain.args[0] <= x <= domain.args[1]]   

            return plottable_x_coords

        plottable_x1_coords = add_endpoint(plottable_x1_coords, sp.sympify(self.eq1(self.symbol)))
        plottable_x2_coords = add_endpoint(plottable_x2_coords, sp.sympify(self.eq2(self.symbol)))

        y1_coords = [float(self.eq1(x)) for x in plottable_x1_coords]
        y2_coords = [float(self.eq2(x)) for x in plottable_x2_coords]

        return plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords


    def plot(self):
        self.plot_widget.clear()

        if self.solutions.is_iterable:
            self.x_intersect = sorted([float(sol) for sol in sp.solveset(self.eq, domain=sp.Interval(*self.x_range)) if (sp.N(self.eq1(float(sol))).is_real and sp.N(self.eq2(float(sol))).is_real)])
            self.y_intersect = [float(self.eq1(sol)) for sol in self.x_intersect]

        if self.vert_asympt_eq is None:
            x_coords = np.linspace(self.x_range[0] - 1, self.x_range[1] + 1, 100)

        else:
            self.vert_asympt = sp.solveset(self.vert_asympt_eq, domain=sp.Interval(*self.x_range))
            self.vert_asympt = [float(sol) for sol in self.vert_asympt if sp.N(sol).is_real]
            x_coords = segmented_linspace(self.x_range[0] - 1, self.x_range[1] + 1, self.vert_asympt, num=10, dx=0.00001)

        plottable_x1_coords = []
        y1_coords = []
        plottable_x2_coords = []
        y2_coords = []

        if self.vert_asympt_eq is None:
            plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = self.get_plottable(x_coords)

        else:
            for i in range(len(x_coords)):
                plottable_x1_coords_i, y1_coords_i, plottable_x2_coords_i, y2_coords_i = self.get_plottable(x_coords[i])

                plottable_x1_coords.append(plottable_x1_coords_i)
                y1_coords.append(y1_coords_i)
                plottable_x2_coords.append(plottable_x2_coords_i)
                y2_coords.append(y2_coords_i)


        self.legend.setBrush('lightgrey')
        self.legend.setPen("black")

        counter = 0

        if self.vert_asympt is None:
            self.plot_widget.plot(plottable_x1_coords, y1_coords, symbol=None, pen={'color': 'darkturquoise', 'width': 3}, name=f"f(x) = {self.eq1(self.symbol)}")
            self.plot_widget.plot(plottable_x2_coords, y2_coords, symbol=None, pen={'color': 'springgreen', 'width': 3}, name=f"g(x) = {self.eq2(self.symbol)}")

        else:
            for i in range(len(x_coords)):
                counter += 1
                self.plot_widget.plot(plottable_x1_coords[i], y1_coords[i], symbol=None, pen={'color': 'darkturquoise', 'width': 3}, name=f"f(x) = {self.eq1(self.symbol)}" if counter == 1 else None)
                self.plot_widget.plot(plottable_x2_coords[i], y2_coords[i], symbol=None, pen={'color': 'springgreen', 'width': 3}, name=f"g(x) = {self.eq2(self.symbol)}" if counter == 1 else None)

            counter = 0
            if len(self.vert_asympt) >= 10 and len(self.x_intersect) >= 7:
                return

            for vert_asympt in self.vert_asympt:
                counter += 1
                self.plot_widget.plot([vert_asympt, vert_asympt], self.y_range, symbol=None, pen=pg.mkPen('black', width=3, style=QtCore.Qt.DashLine), name=f"Verticale Asymptoot" if counter == 1 else None)

        if len(self.x_intersect) >= 7:
            return
        
        counter = 0
        for x,y in zip(self.x_intersect, self.y_intersect):
            if self.x_range[0] <= x <= self.x_range[1]:
                counter += 1
                self.plot_widget.plot([float(x)], [float(y)], symbol='o', symbolSize=8, pen=None, symbolBrush='black', name=f"Snijpunt {counter} = ({no_frac(sp.nsimplify(round(x,13), [sp.pi]))}, {no_frac(sp.nsimplify(round(y,13), [sp.pi]))})")


    def update_range(self):
        if not self.start:
            return

        self.plot_widget.sigXRangeChanged.disconnect(self.update_range)
        self.plot_widget.sigYRangeChanged.disconnect(self.update_range)

        self.plot_widget.clear()

        self.x_range = self.plot_widget.getViewBox().viewRange()[0]
        self.y_range = self.plot_widget.getViewBox().viewRange()[1]
        self.plot()

        self.plot_widget.sigXRangeChanged.connect(self.update_range)
        self.plot_widget.sigYRangeChanged.connect(self.update_range)
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.setWindowTitle("Vergelijking Oplosser") 
    ui.setWindowIcon(QtGui.QIcon("calculator-variant-outline.png"))
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
