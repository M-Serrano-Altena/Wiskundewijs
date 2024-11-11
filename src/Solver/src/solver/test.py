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

eq1 = sp.Eq(4*x - 2*y, 8)
eq2 = sp.Eq(x - y, 2)
sol = sp.solve([eq1, eq2], (x, y))
print(sol)

from sympy import symbols, Eq, latex
from sympy.matrices import Matrix

# Define variables
x, y = symbols('x y')

# Define equations
eq1 = Eq(x + y, 10)
eq2 = Eq(2*x - y, 3)

# Use latex to format as a system
latex_code = r"\begin{cases} " + latex(eq1) + r" \\ " + latex(eq2) + r" \end{cases}"
print(latex_code)