import scipy.optimize
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
import numpy as np
import regex as re
import matplotlib.pyplot as plt
from sympy.printing.latex import LatexPrinter
import ast
from src.Solver.src.solver.math_parser import math_interpreter, replace_dot_funcs


x, y = sp.symbols("x,y", real=True)

# string = "integrate(x**2 + diff(x, 3).diff(sqrt(4)) + diff(log(x, 4), 2), (1, 2)).integrate((sqrt(4), sqrt(16)))"
# string = math_interpreter(string)
# # string = add_args_to_func(string, func_name="diff", replace_with='x', amt_commas=1, nested_level=1, position_type="before")
# # # string = add_args_to_func(string, func_name="integrate", replace_with='x', amt_commas=1, nested_level=2, position_type="before")
# # # string = add_args_to_func(string, func_name='log', replace_with='10')
# print(string)


string = "(5 * x).integrate() + (sin(x) + cos(x).integrate((x, 1, 2)) + tan(x).diff()).subs(2) + diff(4x, x) + subs(x^5, 2) + integrate(sinh(x), (1, 2))"
string = math_interpreter(string)
print(string)
string = replace_dot_funcs(string)
print()
print(string)


print("\n\n")
string = r"sinsinsinsin"
string = math_interpreter(string)
print(string)
# print()
# string =  replace_dot_funcs(string)
# print(string)

