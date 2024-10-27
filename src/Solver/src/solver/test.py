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
from src.Solver.src.solver.sympy_custom_funcs import LOCALS, custom_latex, r
import src.Solver.src.solver.sympy_custom_funcs as sp_custom
from types import FunctionType
from collections.abc import Iterable
import typing
import operator
import mistune
import sympy.vector as sp_vector

x, y = sp.symbols("x,y", real=True)

string = "magnitude(vect(2,3,4))"
string = math_interpreter(string)
print(string)
print(sp.sympify(string, locals=LOCALS))


angle = (sp_custom.vect(4, 3), sp_custom.vect(3, -4))
print(angle)
print(angle.doit())
print(custom_latex(angle))
