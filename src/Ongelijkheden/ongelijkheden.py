import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def draw_funcs(func, func2, title, x_range, y_range, intersect):
    x = np.arange(x_range[0], x_range[1], 0.01)
    f = [func(num) for num in x]
    g = [func2(num) for num in x]


    fig = plt.figure()
    

    ax = fig.add_subplot(111)

    ax.set_xlabel('X-as')
    ax.set_ylabel('Y-as')

    ax.spines['bottom'].set_color('#D3D3D3')
    ax.spines['top'].set_color('#D3D3D3')
    ax.spines['left'].set_color('#D3D3D3')
    ax.spines['right'].set_color('#D3D3D3')
    ax.xaxis.label.set_color('#D3D3D3')
    ax.yaxis.label.set_color('#D3D3D3')
    ax.tick_params(axis='both', colors='#D3D3D3')
    ax.set_facecolor("#FF0000")
    

    ax.set_title(title, loc='center', color='#D3D3D3')


    plt.xlim(x_range)
    plt.ylim(y_range)

    plt.plot(x, f, 'darkturquoise', label='f(x)')
    plt.plot(x, g, 'springgreen', label='g(x)')
    plt.hlines(xmin=x_range[0], xmax=x_range[1], y=0, colors='#D3D3D3')
    plt.vlines(ymin=y_range[0], ymax=y_range[1], x=0, colors='#D3D3D3')
    plt.scatter([intersect[0]], [intersect[1]], c='aquamarine')
    plt.legend(loc="upper right")

    plt.savefig(f"{title}.svg")
    plt.show()


draw_funcs(lambda x: x -1, lambda x: -x + 2, "f(x) = x - 1; g(x) = -x + 2", (-1, 4), (-2, 6), (1.5, 0.5))

draw_funcs(lambda x: 3*x + 2, lambda x: 8, "f(x) = 3x + 2; g(x) = 8", (0, 4), (6, 10), (2, 8))
draw_funcs(lambda x: -8*x - 7, lambda x: 33, "f(x) = -8x - 7; g(x) = 33", (-7, -3), (25, 41), (-5, 33))
draw_funcs(lambda x: x - 4, lambda x: 2*x + 9, "f(x) = x - 4; g(x) = 2x + 9", (-15, -11), (-20, -14), (-13, -17))

