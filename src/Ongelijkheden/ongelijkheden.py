import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def draw_funcs(
    func, func2, title, x_range=(-10,10), y_range=(-10,10), svg=True, intersect1=None, intersect2=None, no_ax=False, intersect_line=True
):
    x_coords = np.arange(x_range[0], x_range[1], 0.01)
    f = [func(num) for num in x_coords]
    g = [func2(num) for num in x_coords]

    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.set_xlabel("X-as")
    ax.set_ylabel("Y-as")

    if svg:
        ax.set_facecolor("#FF0000")
        main_color = "#D3D3D3"
        dot_color = "aquamarine"
    else:
        main_color = "#000000"
        dot_color = "black"

    ax.spines["bottom"].set_color(main_color)
    ax.spines["top"].set_color(main_color)
    ax.spines["left"].set_color(main_color)
    ax.spines["right"].set_color(main_color)
    ax.xaxis.label.set_color(main_color)
    ax.yaxis.label.set_color(main_color)
    ax.tick_params(axis="both", colors=main_color)
    

    ax.set_title(title, loc="center", color=main_color)

    x = sp.symbols("x", real=True)
    x_intersects = sp.solve(func(x) - func2(x), x)
    y_intersects = [func(num) for num in x_intersects]

    if no_ax:
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        ax.set_yticks([])
        ax.set_xticks([])

        sf = abs(x_range[1] - x_range[0]) / 8
        
        for i, (x_intersect, y_intersect) in enumerate(zip(x_intersects, y_intersects)):
            plt.text(s=rf"${alphabet[i]}$", x=x_intersect - 0.075*sf, y=y_intersect - 0.65*sf, color=main_color)
            if intersect_line:
                plt.vlines(x=x_intersect, ymin=-0.25*sf, ymax=0.25*sf, color=main_color)

    plt.xlim(x_range)
    plt.ylim(y_range)

    # x and y axes
    plt.hlines(xmin=x_range[0], xmax=x_range[1], y=0, colors=main_color, zorder=1)
    plt.vlines(ymin=y_range[0], ymax=y_range[1], x=0, colors=main_color, zorder=1)

    # graphs
    plt.plot(x_coords, f, "darkturquoise", label="f(x)", zorder=1)
    plt.plot(x_coords, g, "springgreen", label="g(x)", zorder=1)

    for x_intersect, y_intersect in zip(x_intersects, y_intersects):
        plt.scatter(x_intersect, y_intersect, c=dot_color, zorder=2)

    plt.legend(loc="upper right")

    if svg:
        plt.savefig(f"{title}.svg")
    else:
        plt.savefig(f"{title}.png")

    plt.show()


draw_funcs(lambda x: x -1, lambda x: -x + 2, "f(x) = x - 1; g(x) = -x + 2", (-1, 4), (-2, 6))

draw_funcs(lambda x: 3*x + 2, lambda x: 8, "f(x) = 3x + 2; g(x) = 8", (0, 4), (6, 10))
draw_funcs(lambda x: -8*x - 7, lambda x: 33, "f(x) = -8x - 7; g(x) = 33", (-7, -3), (25, 41))
draw_funcs(lambda x: x - 4, lambda x: 2*x + 9, "f(x) = x - 4; g(x) = 2x + 9", (-15, -11), (-20, -14))
draw_funcs(lambda x: (x - 1) * (x - 2), lambda x: 0, "f(x) = (x - 1)(x - 2); g(x) = 0", (-1, 4), (-2, 8))
draw_funcs(lambda x: x**2, lambda x: 1, "f(x) = x²; g(x) = 1", (-3, 3), (-1, 8))
    
draw_funcs(lambda x: (x - 1) * (x - 2), lambda x: 0, "f(x) = (x - a)(x - b); g(x) = 0", (0, 3), (-1, 2), no_ax=True, intersect_line=False, svg=True)
    
draw_funcs(lambda x: x**2 + 10*x + 4, lambda x: 15, title="f(x) = x² + 10x + 4; g(x) = 15",  x_range=(-13, 3), y_range=(-25, 25))
draw_funcs(lambda x: x**2 + 25, lambda x: 16, title="f(x) = x² + 25; g(x) = 16",  x_range=(-10, 10), y_range=(-5, 125))
draw_funcs(lambda x: -x**2 + 9*x - 12, lambda x: x**2 - 15/8, title="f(x) = - x² + 9x - 12; g(x) = x² - 1.875",  x_range=(-3, 6), y_range=(-3, 11))
draw_funcs(lambda x: -x + 4, lambda x: 4*x - 6, title="f(x) = -x + 2a; g(x) = 4x - 3a",  x_range=(-2, 6), y_range=(-2, 6), no_ax=True, svg=False)
