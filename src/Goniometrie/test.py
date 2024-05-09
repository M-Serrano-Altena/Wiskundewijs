from sympy import Rational, latex

def mixed_fraction_latex(expr):
    whole, frac = divmod(expr, 1)
    if frac != 0 and whole != 0:
        return f"{int(whole)} {latex(frac)}"
    else:
        return latex(expr)

# Example usage:
from sympy import *

frac1 = nsimplify(3/2)
frac2 = nsimplify(5/2 * pi)

print(type(E))

print(mixed_fraction_latex(frac1))  # Output: 1 \frac{1}{2}
print(nsimplify(frac2))  # Output: (5*pi, 2
print(mixed_fraction_latex(frac2))  # Output: 2 \frac{1}{2} \pi