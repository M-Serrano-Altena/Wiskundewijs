import sys
from PySide6 import QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np
import sympy as sp
import re

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

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
        eq_string = self.equation_input.text()
        self.plot_widget.clear()
        self.textedit.clear()

        try:
            eq_string = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_string)
            eq_string = re.sub(r'\)(\d)', r')*\1', eq_string)
            eq_string = re.sub(r'(\d)\(', r'\1*(', eq_string)
            self.eq_string = re.sub(r'\)\(', r')*(', eq_string)

            eq_split = eq_string.split("=")

            if len(eq_split) == 1:
                eq1 = sp.sympify(eq_split[0])
                eq2 = 0
                self.eq = sp.Eq(eq1, eq2)
                self.symbol = None

                if eq1.free_symbols:
                    self.symbol = eq1.free_symbols.pop()
                    self.eq1 = sp.lambdify(self.symbol, eq1)
                    self.eq2 = sp.lambdify(self.symbol, eq2)
                    self.equation_output.setText(f"{eq_string} = 0")

                else:
                    self.equation_output.setText(eq_string)

            elif len(eq_split) == 2:
                eq1 = sp.sympify(eq_split[0])
                eq2 = sp.sympify(eq_split[1])
                self.eq = sp.Eq(eq1, eq2)
                self.symbol = None

                if eq1.free_symbols:
                    self.symbol = self.eq.free_symbols.pop()
                    self.eq1 = sp.lambdify(self.symbol, eq1)
                    self.eq2 = sp.lambdify(self.symbol, eq2)

                self.equation_output.setText(eq_string)

            else:
                self.textedit.setTextColor('red')
                self.textedit.append("Ongeldige vergelijking")
                self.textedit.append("")
                self.textedit.setTextColor('black')
                return
            
            
            self.solutions = [sol for sol in sp.solve(self.eq) if sol.is_real]
            
            if not self.solutions:
                try:
                    if not sp.solve(self.eq):
                        solution = sp.nsimplify(eq_string)
                        self.textedit.append(f"{eq_string} = {solution}")
                        
                    else:
                        raise Exception

                except Exception:
                    self.textedit.append("Geen oplossing gevonden")

                self.textedit.append("")
                self.equation_input.setFocus()
                self.equation_input.selectAll()

                return
            
            

            if len(self.solutions) == 1:
                self.textedit.append("De oplossing is:")
                self.textedit.append(f"{self.symbol} = {self.solutions[0]}")

            else:
                self.textedit.append("De oplossingen zijn:")
                counter = 0
                for solution in self.solutions:
                    counter +=1
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


    def plot(self):
        x_coords = np.linspace(*self.x_range, 100)

        y1_coords = [float(self.eq1(x)) for x in x_coords]
        y2_coords = [float(self.eq2(x)) for x in x_coords]

        self.plot_widget.plot(x_coords, y1_coords, symbol=None, pen={'color': 'darkturquoise', 'width': 3})
        self.plot_widget.plot(x_coords, y2_coords, symbol=None, pen={'color': 'springgreen', 'width': 3})
        self.plot_widget.plot(self.x_intersect, self.y_intersect, symbol='o', symbolSize=8, pen=None, symbolBrush='black')


    def set_range(self):
        self.x_intersect = [float(sol) for sol in self.solutions]
        self.y_intersect = [float(self.eq1(sol)) for sol in self.solutions]
        intersect_range = float(max(self.x_intersect)) - float(min(self.x_intersect))
        self.x_range = (float(min(self.x_intersect)) - (intersect_range/3 + 2), float(max(self.x_intersect)) + (intersect_range/3 + 2))
        self.plot_widget.setXRange(*self.x_range)


    def update_range(self):
        self.plot_widget.clear()
        self.x_range = self.plot_widget.getViewBox().viewRange()[0]
        self.plot()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.setWindowTitle("Vergelijking Oplosser") 
    ui.setWindowIcon(QtGui.QIcon("calculator-variant-outline.png"))
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
