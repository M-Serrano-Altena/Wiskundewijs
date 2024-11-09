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
from src.Solver.src.solver.sympy_custom_funcs import LOCALS, DEG_ARC_GONIO_LOCALS, custom_latex, r, vect, matrix, CustomMatAdd, CustomMatMul, inverse
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
eq = sp.sympify(string, locals=local_funcs, evaluate=False)
print(custom_latex(eq))

# matrix_ = vect(1,1) * vect(1,1).T
# print(matrix_)
# print(matrix_ * vect(1,1))
# print(custom_latex(vect(1,1) * vect(1,1).T * vect(1,1)))

print()
print(CustomMatAdd(CustomMatMul(3,sp.Matrix([[1,1], [1,1]])), sp.Matrix([[1,1], [1,1]])))

sub_expr = CustomMatMul(3,sp.Matrix([[1,1], [1,1]]))
expr =  sub_expr + matrix([1,1], [1,1])
print(expr)

# eq1 = sp.Eq(2*x + 3*y, 5)
# eq2 = sp.Eq(3*x + 2*y, 4)
# sol = sp.solve([eq1, eq2], (x, y))
# print(sol)

print(inverse(sp.sin(x)))
print(inverse(matrix([1,0], [1,1])))
print(inverse(sp.asin(x)))


print(sp.Determinant(matrix([1,2], [2,1])).doit())