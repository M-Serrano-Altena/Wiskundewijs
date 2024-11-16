import regex as re
import sympy as sp
import numpy as np
import scipy.optimize
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
import time
from pylatexenc.latex2text import LatexNodes2Text
from types import FunctionType
from collections.abc import Iterable
from src.Solver.src.solver.math_parser import *
from src.Solver.src.solver.sympy_custom_funcs import *


def main():
    
    from sympy import symbols, Eq, simplify, gcd_terms

    # Define symbols
    x, y, z, t = symbols('x y z t')
    l = [Eq(t, 1), Eq(t, 1), Eq(t, 1), Eq(t, 1), Eq(t, 1), Eq(t + 5, 6), Eq(3 - t, 2), Eq(3 - t, 2), Eq(3 - t, 2), Eq(3 - t, 2), Eq(3*t - 3, 0), Eq(3*t - 3, 0), Eq(3*t - 3, 0)]
    
    for _ in range(400000):
        list(set(l))






if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("It took ", end - start, "seconds")
    plt.show()