import sys
from PySide6 import QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np
import sympy as sp
import re

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

def no_frac(num):
    if isinstance(num, sp.Rational) and (abs(num.p) > 100 or abs(num.q) > 100):
        return round(num.evalf(), 4)
    return num

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
        vbox1 = QtWidgets.QVBoxLayout()
        hbox.addLayout(vbox1)

        hbox.addWidget(self.plot_widget)

        equation_label = QtWidgets.QLabel("Voer vergelijking in:")
        vbox1.addWidget(equation_label)

        self.equation_input = QtWidgets.QLineEdit()
        vbox1.addWidget(self.equation_input)

        self.equation_input.setPlaceholderText("bijv. 2x^2 + 1 = 9")
        self.equation_input.returnPressed.connect(self.solve_equation)
        self.equation_input.setFocus()

        self.equation_input.setStyleSheet("QLineEdit { background-color: white }")
        self.equation_input.setStyleSheet("QLineEdit { color: black }")
        self.equation_input.setStyleSheet("QLineEdit { border: 2px solid black }")

        self.solve_button = QtWidgets.QPushButton("Vergelijking Oplossen")
        vbox1.addWidget(self.solve_button)

        self.equation_output_label = QtWidgets.QLabel("Interpretatie:")
        vbox1.addWidget(self.equation_output_label)

        self.equation_output = QtWidgets.QLineEdit()
        self.equation_output.setReadOnly(True)
        vbox1.addWidget(self.equation_output)

        answer_label = QtWidgets.QLabel("Antwoord:")
        vbox1.addWidget(answer_label)

        self.textedit = QtWidgets.QTextEdit()
        self.textedit.setReadOnly(True)
        vbox1.addWidget(self.textedit)
        self.textedit.setTextColor('black')

        self.solve_button.clicked.connect(self.solve_equation)


        self.plot_widget.sigXRangeChanged.connect(self.update_range)
        self.plot_widget.sigYRangeChanged.connect(self.update_range)


    def solve_equation(self):
        """Solve the equation and display the results
        """
        self.start = True

        self.plot_widget.sigXRangeChanged.disconnect(self.update_range)
        self.plot_widget.sigYRangeChanged.disconnect(self.update_range)

        self.plot_widget.setXRange(-10, 10)
        self.plot_widget.setYRange(-10, 10)

        self.plot_widget.clear()
        self.legend.setBrush('white')
        self.legend.setPen("white")
        eq_string = self.equation_input.text()
        self.textedit.clear()

        try:
            eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
            eq_string = re.sub(r'\)(\d)', r')*\1', eq_string)
            eq_string = re.sub(r'(\d)\(', r'\1*(', eq_string)
            eq_string = re.sub(r'(\d)\)\((\d)', r'\1)*(\2', eq_string)
            eq_string = re.sub(r'([a-zA-Z])\)\((\d)', r'\1)*(\2', eq_string)
            eq_string = re.sub(r'(\d)\)\(([a-zA-Z])', r'\1)*(\2', eq_string)
            eq_string = re.sub(r'([a-zA-Z])\)\(([a-zA-Z])', r'\1)*(\2', eq_string)

            self.eq_string = eq_string

            eq_split = eq_string.split("=")

            if len(eq_split) == 1:
                eq1 = sp.sympify(eq_split[0])
                eq2 = 0
                self.eq = sp.Eq(eq1, eq2)
                self.symbol = None

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
                self.eq = sp.Eq(eq1, eq2)
                self.symbol = None

                if eq1.free_symbols:
                    self.symbol = self.eq.free_symbols.pop()
                    self.eq1 = sp.lambdify(self.symbol, eq1, "sympy")
                    self.eq2 = sp.lambdify(self.symbol, eq2, "sympy")

                self.equation_output.setText(eq_string)

            else:
                self.textedit.setTextColor('red')
                self.textedit.append("Ongeldige vergelijking")
                self.textedit.append("")
                self.textedit.setTextColor('black')
                self.equation_input.setFocus()
                self.equation_input.selectAll()

                self.plot_widget.sigXRangeChanged.connect(self.update_range)
                self.plot_widget.sigYRangeChanged.connect(self.update_range)
                return
            
            self.eq = sp.simplify(self.eq)
            self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)

            if isinstance(self.solutions, sp.ConditionSet):
                self.eq = sp.simplify(self.solutions.condition)
                self.solutions = sp.solveset(self.eq, domain=sp.S.Reals)


            # if self.solutions.is_FiniteSet:
            #     self.solutions = list(self.solutions)

            if not [sol for sol in sp.solve(self.eq) if sol.is_real]:
                try:
                    if not sp.solve(self.eq):
                        if len(eq_split) == 1:

                            if not self.symbol:
                                solution = sp.nsimplify(eq1, [sp.pi])
                                self.textedit.append(f"{eq_string} = {solution}")

                            else:
                                solution = sp.simplify(eq1)
                                self.textedit.append(f"{eq_string} = {solution}")

                        elif len(eq_split) == 2:
                            lhs = sp.nsimplify(eq1, [sp.pi])
                            rhs = sp.nsimplify(eq2, [sp.pi])
                            
                            if lhs == rhs:
                                self.textedit.append(f"{lhs} = {rhs}:")
                                self.textedit.append(f"Deze vergelijking klopt")

                            elif sp.simplify(lhs) == sp.simplify(rhs):
                                self.textedit.append(f"{sp.simplify(lhs)} = {sp.simplify(rhs)}:")
                                self.textedit.append(f"Deze vergelijking klopt")

                            else:
                                self.textedit.append(f"{lhs} ≠ {rhs}:")
                                self.textedit.append(f"Deze vergelijking klopt niet")
   
                    else:
                        raise Exception

                except Exception:
                    self.textedit.append("Geen oplossing gevonden")

                self.textedit.append("")
                self.equation_input.setFocus()
                self.equation_input.selectAll()

                self.plot_widget.sigXRangeChanged.connect(self.update_range)
                self.plot_widget.sigYRangeChanged.connect(self.update_range)

                return
            
            
            if self.solutions.is_FiniteSet:
                if len(eq_split) == 1:
                    self.textedit.append(f"Vereenvoudigde Vergelijking: \n {sp.simplify(eq1)} = 0 \n")

                elif len(eq_split) == 2:
                    self.textedit.append(f"Vereenvoudigde Vergelijking: \n {sp.simplify(eq1)} = {sp.simplify(eq2)} \n")


                if len(self.solutions) == 1:
                    self.textedit.append("De oplossing is:")
                    self.textedit.append(f"{self.symbol} = {self.solutions.args[0]}")

                else:
                    self.textedit.append("De oplossingen zijn:")
                    counter = 0
                    for solution in self.solutions:
                        counter +=1
                        self.textedit.append(f"{counter})   {self.symbol} = {solution}")
            
            else:
                if isinstance(self.solutions, sp.ConditionSet):
                    self.solutions = self.solutions.base_set

                self.textedit.append("De oplossing is de set:")
                self.textedit.append(f"{self.symbol} = ")
                pretty_solution = sp.pretty(self.solutions)
                self.textedit.append(pretty_solution)

                self.textedit.append("")
                self.textedit.append("In het domein [0, 2pi]:")
                self.interval_solutions = sp.solveset(self.eq, domain=sp.Interval(0, 2*sp.pi))
                counter = 0
                for solution in self.interval_solutions:
                    counter += 1
                    self.textedit.append(f"{counter})   {self.symbol} = {solution}")

                
            self.set_range()
            self.plot()     
       
        
        except Exception as e:
            self.textedit.setTextColor('red')
            self.textedit.append(f"Fout: {str(e)}")
            self.textedit.setTextColor('black')

        self.textedit.append("")
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

    
    def plot(self):
        self.plot_widget.clear()

        if self.solutions.is_iterable:
            self.x_intersect = sorted([float(sol) for sol in sp.solveset(self.eq, domain=sp.Interval(*self.x_range))])
            self.y_intersect = [float(self.eq1(sol)) for sol in self.x_intersect]


        x_coords = np.linspace(self.x_range[0] - 1, self.x_range[1] + 1, 100)

        y1_coords = [float(self.eq1(x)) for x in x_coords]
        y2_coords = [float(self.eq2(x)) for x in x_coords]

        self.legend.setBrush('lightgrey')
        self.legend.setPen("black")

        self.plot_widget.plot(x_coords, y1_coords, symbol=None, pen={'color': 'darkturquoise', 'width': 3}, name=f"f(x) = {self.eq1(self.symbol)}")
        self.plot_widget.plot(x_coords, y2_coords, symbol=None, pen={'color': 'springgreen', 'width': 3}, name=f"g(x) = {self.eq2(self.symbol)}")

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
