import scipy.optimize
from scipy.interpolate import UnivariateSpline
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

def get_lambdas(expr: typing.Union[sp.Expr, typing.Iterable[sp.Expr]], symbol: sp.Symbol, numeric: bool = False) -> typing.Union[FunctionType, typing.Iterable[FunctionType]]:
    def get_lambda_numeric(single_expr, modules = ["numpy", "scipy", "sympy"]):
        for module in modules:
            try:
                func = sp.lambdify(symbol, single_expr, module)
                # try:
                #     func(0)
                # except ZeroDivisionError:
                #     func(1)
                return func
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

string = r"5(x+2      =     3x -     2"
string = math_interpreter(string)
print(string)

func = sp.sympify("1/((x)**(2/3))")
print(func)


inequality = sp.sympify("Ne(5*x, 0)")
print(inequality)
print((sp.solve(inequality)))