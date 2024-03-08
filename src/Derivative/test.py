import numpy as np
import sympy as sp

def f(x):
    return x**2 + 4*x + 4

x = sp.Symbol('x')


for num in sp.solveset(x**2 + 4*x + 4, domain=sp.Interval((-4, 4))):
    print(num)