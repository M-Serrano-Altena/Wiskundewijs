from src.Solver.src.solver.solve_calculations import Solve

import sys
from PySide6 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
from sympy import nsimplify, pi, Rational
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

def no_frac(num):
    if isinstance(num, Rational) and (abs(num.p) > 100 or abs(num.q) > 100):
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
        self.plot_widget.showGrid(x=True, y=True, alpha=0.5)
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
        self.equation_input.returnPressed.connect(self.show_solutions)
        self.equation_input.setFocus()

        self.equation_input.setStyleSheet("QLineEdit { background-color: white }")
        self.equation_input.setStyleSheet("QLineEdit { color: black }")
        self.equation_input.setStyleSheet("QLineEdit { border: 2px solid black }")

        self.solve_button = QtWidgets.QPushButton("Vergelijking Oplossen")
        self.vbox1.addWidget(self.solve_button)

        self.equation_interpretation_label = QtWidgets.QLabel("Interpretatie:")
        self.vbox1.addWidget(self.equation_interpretation_label)

        self.equation_interpretation = QtWidgets.QLineEdit()
        self.equation_interpretation.setReadOnly(True)
        self.vbox1.addWidget(self.equation_interpretation)

        answer_label = QtWidgets.QLabel("Antwoord:")
        self.vbox1.addWidget(answer_label)

        self.create_fig()        

        self.solve_button.clicked.connect(self.show_solutions)

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

    def add_solution_text(self, new_text, new_line=True, latex=True, options=None):
        if type(options) is dict:
            if "new_line" in options:
                new_line = options["new_line"]

            if "latex" in options:
                latex = options["latex"]

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


    def show_solutions(self):
        self.create_fig()

        self.plot_widget.sigXRangeChanged.disconnect(self.update_range)
        self.plot_widget.sigYRangeChanged.disconnect(self.update_range)

        self.plot_widget.setXRange(-10, 10)
        self.plot_widget.setYRange(-10, 10)

        self.plot_widget.clear()
        self.legend.setBrush('white')
        self.legend.setPen("white")

        self.solve = Solve(input_string=self.equation_input.text())
        equation_interpret, outputs, plot = self.solve.solve_equation()
        self.start = True

        self.equation_input.setFocus()
        self.equation_input.selectAll()

        self.plot_widget.sigXRangeChanged.connect(self.update_range)
        self.plot_widget.sigYRangeChanged.connect(self.update_range)

        if equation_interpret is None:
            return
        
        self.equation_interpretation.setText(equation_interpret)

        if outputs is None:
            return
        
        for output in outputs:
            if type(output) is tuple:
                self.add_solution_text(output[0], options=output[1])
            
            else:
                self.add_solution_text(output)

        if plot:
            self.set_range()
            self.legend.setBrush('lightgrey')
            self.legend.setPen("black")
            self.plot()

    
    def set_range(self):
        self.x_range, self.y_range = self.solve.get_range()
        self.plot_widget.setRange(xRange=self.x_range, yRange=self.y_range)
        self.plot_widget.getViewBox().setDefaultPadding(-0.1)


    def plot(self):
        self.plot_widget.clear()
        
        plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = self.solve.get_plot_data(self.x_range)

        counter = 0

        if self.solve.vert_asympt is None:
            self.plot_widget.plot(plottable_x1_coords, y1_coords, symbol=None, pen={'color': 'darkturquoise', 'width': 3}, name=f"f(x) = {self.solve.eq1(self.solve.symbol)}")
            self.plot_widget.plot(plottable_x2_coords, y2_coords, symbol=None, pen={'color': 'springgreen', 'width': 3}, name=f"g(x) = {self.solve.eq2(self.solve.symbol)}")

        else:
            for i in range(len(self.solve.x_coords)):
                counter += 1
                self.plot_widget.plot(plottable_x1_coords[i], y1_coords[i], symbol=None, pen={'color': 'darkturquoise', 'width': 3}, name=f"f(x) = {self.solve.eq1(self.solve.symbol)}" if counter == 1 else None)
                self.plot_widget.plot(plottable_x2_coords[i], y2_coords[i], symbol=None, pen={'color': 'springgreen', 'width': 3}, name=f"g(x) = {self.solve.eq2(self.solve.symbol)}" if counter == 1 else None)

            counter = 0

            if len(self.solve.vert_asympt) < 9:
                for vert_asympt in self.solve.vert_asympt:
                    counter += 1
                    self.plot_widget.plot([vert_asympt, vert_asympt], self.y_range, symbol=None, pen=pg.mkPen('black', width=3, style=QtCore.Qt.DashLine), name=f"Verticale Asymptoot" if counter == 1 else None)

        if len(self.solve.x_intersect) > 5:
            return
        
        counter = 0
        for x,y in zip(self.solve.x_intersect, self.solve.y_intersect):
            if self.x_range[0] <= x <= self.x_range[1]:
                counter += 1
                self.plot_widget.plot([float(x)], [float(y)], symbol='o', symbolSize=8, pen=None, symbolBrush='black', name=f"Snijpunt {counter} = ({no_frac(nsimplify(round(x,13), [pi]))}, {no_frac(nsimplify(round(y,13), [pi]))})")


    def update_range(self):
        if not self.start:
            return

        self.plot_widget.sigXRangeChanged.disconnect(self.update_range)
        self.plot_widget.sigYRangeChanged.disconnect(self.update_range)

        self.x_range, self.y_range = self.plot_widget.getViewBox().viewRange()
        self.plot()

        self.plot_widget.sigXRangeChanged.connect(self.update_range)
        self.plot_widget.sigYRangeChanged.connect(self.update_range)
        


def solve_application():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.setWindowTitle("Vergelijking Oplosser") 
    ui.setWindowIcon(QtGui.QIcon("calculator-variant-outline.png"))
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    solve_application()
