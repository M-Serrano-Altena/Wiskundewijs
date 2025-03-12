import numpy as np
import sympy as sp\

x = sp.symbols('x')

func = sp.lambdify(x, sp.sin(x))
print(func(None))