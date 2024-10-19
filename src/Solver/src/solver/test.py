import scipy.optimize
from scipy.interpolate import UnivariateSpline
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
import numpy as np
import regex as re
import matplotlib.pyplot as plt
from sympy.printing.latex import LatexPrinter
import ast
from src.Solver.src.solver.math_parser import math_interpreter, get_uneval_sp_objs, latex_to_plain_text, apply_inner_func_to_func
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

string = r"d/dx x^2 = 34 2/15 pi"
string = math_interpreter(string)
print(string)
# print(sp.sympify(string).doit())

string = r"3/2"
string = math_interpreter(string)
print(string)
string = sp.sympify(string)
print(custom_latex(string), type(string))

t = sp.symbols("t")

string = "sin(90)"
string = apply_inner_func_to_func(string, "sin", "rad")
print(string)

print(sp.nsimplify(69.4).is_Rational)
print(custom_latex(sp.sympify("sin(90^(circ))")))

print(sp.Mul(sp.pi, sp.Rational(1,2)).as_coeff_Mul())

string = "sin(90^{\\circ})"
string = math_interpreter(string)
string = re.sub(r"\^?[°∘]", "", string)
string = re.sub(r"\^?\(\)", "", string)
print(string)