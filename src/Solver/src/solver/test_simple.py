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


def main():
    iterate = 1000000
    x = sp.symbols("x", real=True)
    # solutions = sp.solveset(sp.sin(x), x).evalf()

    # for _ in range(iterate):
    #     sp.sympify(sp.sin(x))
    # Sample data with steep regions
    samples = 1000
    x = np.linspace(-1000, 1000, samples)
    y = np.cbrt(x)

    # Fit spline (s = smoothing factor)
    x_dense = np.linspace(-1000, 1000, 10000*samples)
    # spline = UnivariateSpline(x, y, s=0.25)
    # y_smooth = spline(x_dense)
    y_smooth = np.cbrt(x_dense)

    # Plot
    plt.plot(x, y, 'o', label='Original data')
    plt.plot(x_dense, y_smooth, label='Spline interpolation')
    plt.xlim(-2, 2)
    plt.ylim(-1, 1)
    plt.legend()
    







if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("It took ", end - start, "seconds")
    plt.show()