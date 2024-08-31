import numpy as np
import sympy as sp

l1 = [1, 2, 3]
l2 = [4, 5, 6]
print(*np.meshgrid(l1, l2))
print()
print(*np.meshgrid(l2, l1))