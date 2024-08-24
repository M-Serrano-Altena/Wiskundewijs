import regex as re
import sympy as sp
import numpy as np
import scipy.optimize
import time
from pylatexenc.latex2text import LatexNodes2Text
from types import FunctionType
from collections.abc import Iterable


def main():
    iterate = 1000000
    x = sp.symbols("x", real=True)
    # solutions = sp.solveset(sp.sin(x), x).evalf()

    # for _ in range(iterate):
    #     sp.sympify(sp.sin(x))
    func = sp.Piecewise((0, sp.Eq(x, 0)), (1/(3*sp.Abs(x**(2/3))), True))
    func_lambda = sp.lambdify(x, func, "numpy")
    print(func_lambda(1))







if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("It took ", end - start, "seconds")