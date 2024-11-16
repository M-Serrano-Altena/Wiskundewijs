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
local_funcs.update({"VectorAdd": sp_custom.CustomVectorAdd})


from sympy import symbols, Eq, simplify, gcd_terms

# Define symbols
x, y, z, t = symbols('x y z t')

l = [Eq(t, 1), Eq(t, 1), Eq(t, 1), Eq(t, 1), Eq(t, 1), Eq(t + 5, 6), Eq(3 - t, 2), Eq(3 - t, 2), Eq(3 - t, 2), Eq(3 - t, 2), Eq(3*t - 3, 0), Eq(3*t - 3, 0), Eq(3*t - 3, 0)]
print(l)

print(unique_preserve_order(l))

l = [x, z, y, t]
print(sorted(l, key=lambda x: x.name))

print(sp.trigsimp(sp.asin(sp.sin(x)), inverse=True))

from itertools import product

data = {"x": [1, 2], "y": [3, 4], "z": [5, 6]}

# Generate all combinations
combinations = [
    {key: value for key, value in zip(data.keys(), values)}
    for values in product(*data.values())
]

# Print the result
for combination in combinations:
    print(combination)

s = set([1])
print(s.pop())