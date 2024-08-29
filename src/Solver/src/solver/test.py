import scipy.optimize
from scipy.interpolate import UnivariateSpline
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
import numpy as np
import regex as re
import matplotlib.pyplot as plt
from sympy.printing.latex import LatexPrinter
import ast
from src.Solver.src.solver.math_parser import math_interpreter, get_uneval_sp_objs, latex_to_plain_text
from src.Solver.src.solver.solve_calculations import custom_latex
from types import FunctionType
from collections.abc import Iterable
import typing
import operator



x, y = sp.symbols("x,y", real=True)

# string = r"\int d/dx (\frac{1}{x}) dx + \int \frac{log_100 (x^2) - log(x)}{4 + 1} dt - \int_{∜(16)}^{\sqrt[9](2^9)} \int_{-\infty}^{\infty} e^{-x^2} dx dt"
# string = r"d/dx \sqrt[4]{x^2} != 0"
# string = math_interpreter(string)
# print(string)
# print(sp.sympify(string))

string = "integrate(log(x, 4), x, root(4, 2), log(100)) + integrate(log(x^2, 100) - integrate(1/(x log(100))), 4 + 1, 7) - integrate(e^(-x^2), (-oo, oo))"
string = r"\int_{0}^{2pi} \dfrac{d^2}{dx^2} (sinx + cosx) + 4 dx"
string = r"\cfrac{1}{2}"
string = math_interpreter(string)
print(string)
# print(sp.sympify(string).doit())
