import regex as re
import sympy as sp
import numpy as np
import scipy.optimize
import time
from pylatexenc.latex2text import LatexNodes2Text
from types import FunctionType
from collections.abc import Iterable

def main():
    iterate = 100
    x = sp.symbols("x", real=True)
    # solutions = sp.solveset(sp.sin(x), x).evalf()

    for _ in range(iterate):
        domain_eq1 = sp.calculus.util.continuous_domain(sp.N(sp.tan(x)), x, domain=sp.S.Reals)

    # # interval_solutions = sp.solveset(sp.sin(x), x, domain=sp.Interval(-10000, 10000))

    # print(interval_solutions)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("It took ", end - start, "seconds")