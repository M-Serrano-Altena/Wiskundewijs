import scipy.optimize
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
import numpy as np
import regex as re
import matplotlib.pyplot as plt
from sympy.printing.latex import LatexPrinter
import ast
from src.Solver.src.solver.math_parser import math_interpreter, get_uneval_sp_objs, latex_to_plain_text
from types import FunctionType
from collections.abc import Iterable
import typing

x, y = sp.symbols("x,y", real=True)

string = r"cbrt(x)"
string = re.sub(r"\bcbrt\b", "jhan", string)
# string = math_interpreter(string)
print(string)