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
    expr = sp.sympify(re.sub(r"\bAbs\b", "", "x/Abs(x**(2/3))"))
    print(sp.powsimp(expr, force=True))






if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("It took ", end - start, "seconds")