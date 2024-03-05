import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def draw_func(
    func, title, x_range, y_range, **kwargs
):
    x = np.arange(x_range[0], x_range[1], 0.01)
    f = [func(num) for num in x]

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

    if kwargs.get('no_ax') is not None and kwargs['no_ax']:
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

    if kwargs.get('points') is not None:
        for point in kwargs['points']:
            plt.scatter([point[0]], [point[1]], c="aquamarine", label="Extreme waarde")


    plt.legend(loc="upper right")

    plt.savefig(f"{title}.svg")
    plt.show()