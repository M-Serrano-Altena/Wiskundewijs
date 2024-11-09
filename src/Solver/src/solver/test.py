import scipy.optimize
from scipy.interpolate import UnivariateSpline
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
import numpy as np
import regex as re
import matplotlib.pyplot as plt
from sympy.printing.latex import LatexPrinter
import ast
from src.Solver.src.solver.math_parser import *
from src.Solver.src.solver.sympy_custom_funcs import LOCALS, DEG_ARC_GONIO_LOCALS, custom_latex, r, vect
import src.Solver.src.solver.sympy_custom_funcs as sp_custom
from types import FunctionType
from collections.abc import Iterable
import typing
import operator
import mistune
import sympy.vector as sp_vector

x, y = sp.symbols("x,y", real=True)

local_funcs = {**LOCALS, **DEG_ARC_GONIO_LOCALS}

string = "div(vect(x,2,0)) + vect(1,1,1)"
# string = math_interpreter(string)
print(string)
eq = sp.sympify(string, locals=local_funcs)
print(custom_latex(eq))

string = "matrix([1,0], [0,1]) @ matrix([[1],[0]])"
string = math_interpreter(string)
print(string)
matrix = sp.sympify(string, locals=local_funcs)
# matrix = sp.Matrix([[1,0], [0,1]]) @ sp.Matrix([[1],[0]])
print(matrix)
print(custom_latex(matrix))

# eq1 = sp.Eq(2*x + 3*y, 5)
# eq2 = sp.Eq(3*x + 2*y, 4)
# sol = sp.solve([eq1, eq2], (x, y))
# print(sol)
