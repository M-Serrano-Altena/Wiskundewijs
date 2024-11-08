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
print(vect(1,2,0) ^ (3 * vect(-2,1,0)))

string = "angle(vect(1,2,0),vect(2,-1,0))"
string = math_interpreter(string)
print(string)
eq = sp.sympify(string, locals=local_funcs)
print(custom_latex(eq))

eq1 = sp.Eq(2*x + 3*y, 5)
eq2 = sp.Eq(3*x + 2*y, 4)
sol = sp.solve([eq1, eq2], (x, y))
print(sol)
