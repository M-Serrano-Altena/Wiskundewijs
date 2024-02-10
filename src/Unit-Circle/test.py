import numpy as np
import sympy as sp
import time
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
circ = plt.Circle((0, 0), radius=1, edgecolor='teal', facecolor='None')
ax.add_patch(circ)
ax.set_aspect('equal')

plt.xlim(-1.1,1.1)
plt.ylim(-1.1,1.1)
plt.show()