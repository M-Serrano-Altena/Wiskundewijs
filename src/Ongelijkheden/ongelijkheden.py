import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def draw_funcs(
    func, func2, title, x_range, y_range, intersect1=None, intersect2=None, no_ax=False
):
    x = np.arange(x_range[0], x_range[1], 0.01)
    f = [func(num) for num in x]
    g = [func2(num) for num in x]

    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.set_xlabel("X-as")
    ax.set_ylabel("Y-as")

    ax.spines["bottom"].set_color("#D3D3D3")
    ax.spines["top"].set_color("#D3D3D3")
    ax.spines["left"].set_color("#D3D3D3")
    ax.spines["right"].set_color("#D3D3D3")
    ax.xaxis.label.set_color("#D3D3D3")
    ax.yaxis.label.set_color("#D3D3D3")
    ax.tick_params(axis="both", colors="#D3D3D3")
    ax.set_facecolor("#FF0000")

    ax.set_title(title, loc="center", color="#D3D3D3")

    if no_ax:
        ax.set_yticks([])
        ax.set_xticks([])
        plt.text(s=r"$a$", x=1, y=0.1, color="#D3D3D3")
        plt.text(s=r"$b$", x=2, y=0.1, color="#D3D3D3")

    plt.xlim(x_range)
    plt.ylim(y_range)

    # x and y axes
    plt.hlines(xmin=x_range[0], xmax=x_range[1], y=0, colors="#D3D3D3")
    plt.vlines(ymin=y_range[0], ymax=y_range[1], x=0, colors="#D3D3D3")

    # graphs
    plt.plot(x, f, "darkturquoise", label="f(x)")
    plt.plot(x, g, "springgreen", label="g(x)")

    # intersect points
    if intersect1 != None:
        plt.scatter([intersect1[0]], [intersect1[1]], c="aquamarine")

        if intersect2 != None:
            plt.scatter(intersect2[0], intersect2[1], c="aquamarine")

    plt.legend(loc="upper right")

    plt.savefig(f"{title}.svg")
    plt.show()


# draw_funcs(lambda x: x -1, lambda x: -x + 2, "f(x) = x - 1; g(x) = -x + 2", (-1, 4), (-2, 6), intersect1=(1.5, 0.5))

# draw_funcs(lambda x: 3*x + 2, lambda x: 8, "f(x) = 3x + 2; g(x) = 8", (0, 4), (6, 10), intersect1=(2, 8))
# draw_funcs(lambda x: -8*x - 7, lambda x: 33, "f(x) = -8x - 7; g(x) = 33", (-7, -3), (25, 41), intersect1=(-5, 33))
# draw_funcs(lambda x: x - 4, lambda x: 2*x + 9, "f(x) = x - 4; g(x) = 2x + 9", (-15, -11), (-20, -14), intersect1=(-13, -17))
    
# draw_funcs(
#     lambda x: (x - 1) * (x - 2),
#     lambda x: 0,
#     "f(x) = (x - 1)(x - 2); g(x) = 0",
#     (-1, 4),
#     (-2, 8),
#     intersect1=(1, 0),
#     intersect2=(2, 0),
# )
# draw_funcs(lambda x: x**2, lambda x: 1, "f(x) = x²; g(x) = 1", (-3, 3), (-1, 8), intersect1=(-1, 1), intersect2=(1, 1))

# draw_funcs(
#     lambda x: (x - 1) * (x - 2),
#     lambda x: 0,
#     "f(x) = (x - a)(x - b); g(x) = 0",
#     (0, 3),
#     (-1, 2),
#     intersect1=(1, 0),
#     intersect2=(2, 0),
#     no_ax=True,
# )
    
# draw_funcs(lambda x: x**2 + 10*x + 4, lambda x: 15, title="f(x) = x² + 10x + 4; g(x) = 15",  x_range=(-13, 3), y_range=(-25, 25), intersect1=(-11, 15), intersect2=(1, 15))
# draw_funcs(lambda x: x**2 + 25, lambda x: 16, title="f(x) = x² + 25; g(x) = 16",  x_range=(-10, 10), y_range=(-5, 125))
draw_funcs(lambda x: -x**2 + 9*x - 12, lambda x: x**2 - 15/8, title="f(x) = - x² + 9x - 12; g(x) = x² - 1.875",  x_range=(-3, 6), y_range=(-3, 11), intersect1=(2.25, 3.1875))
