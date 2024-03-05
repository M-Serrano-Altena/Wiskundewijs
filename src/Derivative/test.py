import numpy as np
import sympy as sp


def func(**kwargs):
    # for key, value in kwargs.items():
    print(kwargs.get("x") is not None)
    # print(kwargs['x'], kwargs['y'])


func(y=0, z=1)

M = np.matrix([(0, 1), (1, 2), (2, 3)])

print(M)

x = sp.Symbol('x')

def f(x):
    return x**3 - x

diff = sp.diff(f(x))

solutions = [float(num) for num in sp.solve(diff)]
print(solutions)


for solution in solutions:
    print(f"The coordinates of the extrema are: ({float(solution)}, {f(float(solution))})")

def g(x):
    return x**2

diff = sp.diff(g(x))

sol = sp.solve(diff)
print(sol)

for solution in sol:
    print("hello world")