from manim import *
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np

class Parabola(Scene):
    def construct(self):
        num = ValueTracker(-4)
        dx = 0.00001

        derivative_label = always_redraw(lambda : MathTex(f"f'(x = {round(num.get_value(), 2):.2f}) = {round(2 * num.get_value(), 2):.2f}").to_edge(UL))
        
        plane = NumberPlane(
            x_range=[-4, 4, 2], x_length=7, y_range=[0, 16, 4], y_length=4
        ).add_coordinates()

        labels = plane.get_axis_labels(x_label="x", y_label="f(x)")

        parab = plane.plot(lambda x: x**2, x_range=[-4, 4], color=GREEN)
        func_label = (
            MathTex("f(x) = x^2 \\\\ f'(x) = 2x")
            .scale(0.6)
            .next_to(parab, UR, buff=0.5)
            .set_color(GREEN)
        )

        slope = always_redraw(
            lambda: plane.get_secant_slope_group(
                x=num.get_value(),
                graph=parab,
                dx=dx,
                secant_line_color=RED,
                secant_line_length=3,
            )
        )

        point = always_redraw(
            lambda: Dot(color=GREEN).move_to(
                plane.c2p(num.get_value(), parab.underlying_function(num.get_value()))
            )
        )

        slope_label = always_redraw(lambda : MathTex(f"\\text{{helling}} = {round((parab.underlying_function(num.get_value() + dx) - parab.underlying_function(num.get_value())) / dx, 2):.2f}").next_to(derivative_label, DOWN))

        self.play(DrawBorderThenFill(plane))
        self.play(Create(VGroup(parab, labels, func_label, slope, point, derivative_label, slope_label)), run_time=6)
        self.wait()
        self.play(num.animate.set_value(0), run_time=5)
        self.wait()
        self.play(num.animate.set_value(4), run_time = 5)
        self.wait()


class Exponential(Scene):
    def construct(self):
        num = ValueTracker(-4)
        dx = 0.00001

        function_label = always_redraw(lambda : MathTex(f"f(x = {num.get_value():.2f}) = e^{{{(num.get_value()):.2f}}} = {np.exp(num.get_value()):.2f}").to_edge(UL))
        derivative_label = always_redraw(lambda : MathTex(f"f'(x = {num.get_value():.2f}) = {np.exp(num.get_value()):.2f}").next_to(function_label, DOWN))
        
        plane = NumberPlane(
            x_range=[-4, 4, 2], x_length=8, y_range=[0, 60, 10], y_length=6
        ).add_coordinates()

        labels = plane.get_axis_labels(x_label="x", y_label="f(x)")

        exp = plane.plot(lambda x: np.exp(x), x_range=[-4, 4], color=GREEN)
        func_label = (
            MathTex("f(x) = e^x \\\\ f'(x) = e^x")
            .scale(0.6)
            .next_to(exp, UR, buff=0.5)
            .set_color(GREEN)
        )

        slope = always_redraw(
            lambda: plane.get_secant_slope_group(
                x=num.get_value(),
                graph=exp,
                dx=dx,
                secant_line_color=RED,
                secant_line_length=3,
            )
        )

        point = always_redraw(
            lambda: Dot(color=GREEN).move_to(
                plane.c2p(num.get_value(), exp.underlying_function(num.get_value()))
            )
        )

        slope_label = always_redraw(lambda : MathTex(f"\\text{{helling}} = {((exp.underlying_function(num.get_value() + dx) - exp.underlying_function(num.get_value())) / dx):.2f}").next_to(derivative_label, DOWN))

        self.play(DrawBorderThenFill(plane))
        self.play(Create(VGroup(exp, labels, func_label, slope, point, function_label, derivative_label, slope_label)), run_time=7)
        self.wait()
        self.play(num.animate.set_value(4), run_time=10)
        self.wait()



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

    # graph(s)
    plt.plot(x, f, "darkturquoise")

    x = sp.Symbol('x')

    # calculate and plot extrema
    if kwargs.get('diff') is not None and kwargs['diff']:
        diff = sp.diff(func(x))
        x_extrm = [float(num) for num in sp.solve(diff)]
        y_extrm = [func(x) for x in x_extrm]

        for x_coord, y_coord in zip(x_extrm, y_extrm):
            plt.scatter([x_coord], [y_coord], c="springgreen")


    # calculate and plot intercepts
    if kwargs.get("intercept") is not None and kwargs["intercept"]:
        print(func(x))
        x_intercepts = sp.solve(func(x))
        print(x_intercepts)

        for x_intercept in x_intercepts:
            plt.scatter([x_intercept], [func(x_intercept)], c="aquamarine")

    plt.savefig(f"{title}.svg")
    plt.show()

draw_func(lambda x: -x**2 + 2, "f(x) = -x² + 2", x_range=(-3, 3), y_range=(-4, 4), diff=True, intercept=False)
# draw_func(lambda x: -x**2 + x, "f(x) = -x² + 2", x_range=(-3, 3), y_range=(-4, 4))
# draw_func(lambda x: x**3 - x, "f(x) = -x² + 2", x_range=(-3, 3), y_range=(-4, 4))