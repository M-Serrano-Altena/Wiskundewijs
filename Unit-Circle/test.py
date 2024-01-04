import numpy as np
import sympy as sp

num = sp.nsimplify(1/3)
div, mod = divmod(num, 1)
mod = sp.nsimplify(mod)
print(f"{div} {mod}")