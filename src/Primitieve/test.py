import numpy as np
import sympy as sp

l = np.array(([-np.pi/2, -0.5], [np.pi/2, 0.5])).astype(float)

print()

print(type(l) is np.ndarray)

x = sp.symbols('x')
solutions = sp.solveset(sp.sin(3*x) - sp.cos(3*x))
counter = 0

for sol in solutions:
    if 0 < sol < 2*np.pi:
        print(sol)
    else:
        counter +=1

    if counter > 10:
        break