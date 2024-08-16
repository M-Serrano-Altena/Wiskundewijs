import regex as re
import sympy as sp

x = sp.symbols("x")

print(sp.sympify("x* (5).diff()"))
print(sp.sin(x).doit())