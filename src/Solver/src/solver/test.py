import scipy.optimize
import sympy as sp
from sympy.simplify.fu import TR2, TR1, TR111
import numpy as np
import regex as re
import matplotlib.pyplot as plt
from sympy.printing.latex import LatexPrinter
import ast
from src.Solver.src.solver.math_parser import math_interpreter, get_uneval_sp_objs
from types import FunctionType
from collections.abc import Iterable
import typing


def get_lambdas(expr: typing.Union[sp.Expr, typing.Iterable[sp.Expr]], symbol: sp.Symbol, numeric: bool = False) -> typing.Union[FunctionType, typing.Iterable[FunctionType]]:
        def get_lambda_numeric(single_expr, modules = ["numpy", "scipy", "sympy"]):
            for module in modules:
                try:
                    return sp.lambdify(symbol, single_expr, module)
                except NameError:
                    continue
        
        if not isinstance(expr, Iterable):
            if numeric:
                return get_lambda_numeric(single_expr=expr)
            return sp.lambdify(symbol, expr, "sympy")
        
        lambdas = []
        if numeric:
            for single_expr in expr:
                lambdas.append(get_lambda_numeric(single_expr=single_expr))
        else:
            for single_expr in expr:
                lambdas.append(sp.lambdify(symbol, single_expr, "sympy"))

        return lambdas

x, y = sp.symbols("x,y", real=True)

string = "(5 * x).integrate() + (sin(x) + cos(x).integrate((x, 2, 3)) + tan(x).diff()).subs(2) + diff(4x, x) + subs(x^5, 2) + integrate(sinh(x), (1, 2))"
string = math_interpreter(string)
print(string)
string = get_uneval_sp_objs(string)
print()
print(string)

string = "pii"
string = math_interpreter(string)
print(string)
# string = replace_dot_funcs(string)
# print(string)

func = sp.sin(x)
func_lambda = get_lambdas(func, x, numeric=True)
print(func_lambda(0))
array = np.array([1])
print(func_lambda(array))

func1, func2 = sp.sin(x), sp.cos(x)
func1_lambda, func2_lambda = get_lambdas([func1, func2], x, numeric=True)
print(func1_lambda(0))
print(func2_lambda(0))
print(func1_lambda(array))
print(func2_lambda(array))