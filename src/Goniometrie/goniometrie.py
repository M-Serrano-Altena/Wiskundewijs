import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from manim import *

class Sin(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-2*sp.pi, 2*sp.pi, sp.pi/2], x_length=13, y_range=[-1.25, 1.25, 0.5], y_length=6, background_line_style={"stroke_color": DARK_BLUE}
        ).add_coordinates()

        labels = plane.get_axis_labels(x_label="x", y_label="y")
        plane.get_coordinate_labels().set_color(WHITE)

        sin = plane.plot(lambda x: sp.sin(x), x_range=[-4*sp.pi - 0.4, 4*sp.pi + 0.4 ], color=GREEN)
        sin_label = (
            MathTex("f(x) = \sin(x)")
            .scale(0.6)
            .to_corner(UR, buff=0.5)
            .shift(0.4*LEFT)
            .set_color(GREEN)
        )

        sin_shift = sin.copy()
        sin_shifted = plane.plot(lambda x: sp.sin(-x), x_range=[-4*sp.pi - 0.4, 4*sp.pi + 0.4], color=RED)

        sin_shifted_label = (
            MathTex("f(x) = \sin(-x)")
            .scale(0.6)
            .to_corner(UR, buff=0.5)
            .shift(0.4*DOWN + 0.4*LEFT)
            .set_color(RED)
        )

        sin_transformed = plane.plot(lambda x: sp.sin(sp.pi - x), x_range=[-3*sp.pi - 0.4, 5*sp.pi + 0.4], color=BLUE)
        sin_transformed_label = (
            MathTex("f(x) = \sin(\pi-x)")
            .scale(0.6)
            .to_corner(UR, buff=0.5)
            .shift(0.4*DOWN + 0.4*LEFT)
            .set_color(BLUE)
        )

        self.play(DrawBorderThenFill(plane), run_time=2)
        self.play(Write(labels))
        self.play(Create(sin), run_time=4)
        self.play(Write(sin_label))
        self.wait(2)
        self.play(Transform(sin_shift, sin_shifted), run_time = 3)
        self.play(Write(sin_shifted_label))
        self.wait(2)
        self.play(Transform(sin_shift, sin_transformed), run_time = 3)
        self.play(Transform(sin_shifted_label, sin_transformed_label))
        self.wait(3)



class Cos(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-2*sp.pi, 2*sp.pi, sp.pi/2], x_length=13, y_range=[-1.25, 1.25, 0.5], y_length=6, background_line_style={"stroke_color": DARK_BLUE}
        ).add_coordinates()

        labels = plane.get_axis_labels(x_label="x", y_label="y")
        plane.get_coordinate_labels().set_color(WHITE)

        cos = plane.plot(lambda x: sp.cos(x), x_range=[-4*sp.pi - 0.4, 4*sp.pi + 0.4 ], color=GREEN)
        cos_label = (
            MathTex("f(x) = \cos(x)")
            .scale(0.6)
            .to_corner(UR, buff=0.5)
            .shift(0.65*LEFT)
            .set_color(GREEN)
        )

        cos_shift = cos.copy()
        cos_shifted = plane.plot(lambda x: sp.cos(-x), x_range=[-4*sp.pi - 0.4, 4*sp.pi + 0.4], color=GREEN)

        cos_shifted_label = (
            MathTex("f(x) = \cos(-x)")
            .scale(0.6)
            .to_corner(UR, buff=0.5)
            .shift(0.65*LEFT)
            .set_color(GREEN)
        )

        cos_transformed = plane.plot(lambda x: sp.cos(sp.pi - x), x_range=[-3*sp.pi - 0.4, 5*sp.pi + 0.4], color=BLUE)
        cos_transformed_label = (
            MathTex("f(x) = \cos(\pi-x)")
            .scale(0.6)
            .to_corner(UR, buff=0.5)
            .shift(0.65*LEFT)
            .set_color(BLUE)
        )

        cos_minus = plane.plot(lambda x: -sp.cos(x), x_range=[-4*sp.pi - 0.4, 4*sp.pi + 0.4], color=RED)
        cos_minus_label = (
            MathTex("f(x) = -\cos(x)")
            .scale(0.6)
            .to_corner(UR, buff=0.5)
            .shift(0.65*LEFT + 0.4*DOWN)
            .set_color(RED)
        )


        self.play(DrawBorderThenFill(plane), run_time=2)
        self.play(Write(labels))
        self.play(Create(cos), run_time=4)
        self.play(Write(cos_label))
        self.wait(2)
        self.play(Transform(cos_shift, cos_shifted), Transform(cos, cos_minus), run_time = 4)
        self.play(Transform(cos_label, cos_shifted_label), Write(cos_minus_label), run_time=1.5)
        self.wait(2)
        self.play(Transform(cos_shift, cos_transformed), run_time = 3)
        self.play(Transform(cos_label, cos_transformed_label))
        self.wait(3)
        # self.play(Transform(cos, cos_minus), run_time = 3)
        # self.play(Transform(cos_label, cos_minus_label))
        # self.wait(3)



def draw_func(func, title, x_range=(-10,10), y_range=(-10,10), x_intersect=False, no_ax=False, intersect_line=True, svg=True, dx = None, dy = None, large=False):
    x_coords = np.arange(x_range[0], x_range[1], 0.01)
    y_coords = [float(func(num)) for num in x_coords]

    fig = plt.figure()
    
    ax = fig.add_subplot(111)

    ax.set_xlabel('X-as')
    ax.set_ylabel('Y-as')

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

    if x_intersect:
        x = sp.symbols('x', real=True)
        x_intersects = sp.solveset(func(x), x, domain=sp.Interval(x_range[0], x_range[1]))
        y_intersects = [float(func(num)) for num in x_intersects]

        for x_intersect, y_intersect in zip(x_intersects, y_intersects):
            plt.scatter(x_intersect, y_intersect, c=dot_color, zorder = 2)

    if no_ax:
        ax.set_xticks([])
        # ax.set_yticks([])

        if dx is None:
            dx=abs(y_range[1] - y_range[0]) / 6
        if dy is None:
            dy=abs(y_range[1] - y_range[0]) / 4
        
        for i, (x_intersect, y_intersect) in enumerate(zip(x_intersects, y_intersects)):
            plt.text(s=f"${sp.latex(x_intersect)}$", x=x_intersect + 0.5*dx, y=y_intersect - 0.25*dy, color=dot_color, fontsize='x-large' if large else 'large')

            if intersect_line:
                plt.vlines(x=x_intersect, ymin=-0.25*dy, ymax=0.25*dy, color=main_color)

    plt.xlim(x_range)
    plt.ylim(y_range)

    plt.plot(x_coords, y_coords, 'darkturquoise', zorder=1)
    plt.hlines(xmin=x_range[0], xmax=x_range[1], y=0, colors=main_color, zorder=1)
    plt.vlines(ymin=y_range[0], ymax=y_range[1], x=0, colors=main_color, zorder=1)

    plt.savefig(f"{title}.svg")
    plt.show()

# draw_func(lambda x: sp.sin(x), title="Sinus", x_range=(-2.5*np.pi, 2.5*np.pi), y_range=(-1.25, 1.25), x_intersect=True, no_ax=True, intersect_line=False)
# draw_func(lambda x: sp.cos(x), title="Cosinus", x_range=(-3*np.pi, 3*np.pi), y_range=(-1.25, 1.25), x_intersect=True, no_ax=True, intersect_line=False, dx=0.6, large=True)
