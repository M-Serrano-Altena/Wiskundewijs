import math
from manim import *
import matplotlib.pyplot as plt
import numpy as np

class Kwadratisch(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 6, 2], x_length=6, y_range=[-4, 10, 2], y_length=5
        )
        labels = plane.get_axis_labels(x_label="x", y_label="y")

        parab = plane.plot(lambda x: x**2 - 5*x + 4, x_range=[-1, 6], color=GREEN)
        parab2 = plane.plot(lambda x: x**2 + 4 - 0.25*25, x_range=[-3.5, 3.5], color=RED)

        parab_label = (
            MathTex("f(x) = ax^2 + bx + c")
            .scale(0.6)
            .next_to(parab, UP + 0.5 * RIGHT, buff=0.5)
            .set_color(GREEN)
        )

        self.play(DrawBorderThenFill(VGroup(plane, labels)))
        self.play(Create(parab, run_time=2))
        self.play(Create(parab_label, run_time=2))
        self.wait()

        extrema_coords = MathTex("x_{top} = -\\frac{b}{2a}").move_to(parab.get_center() + 2.5*DOWN).shift(0.1*LEFT).scale(0.6)

        self.play(Create(extrema_coords))
        self.wait()

        text = Tex("We transleren deze functie naar links zodat de top op de $y$-as komt te liggen. \\\\ Dit doen we door de substitutie te maken $x \\rightarrow x' - \\frac{b}{2a}$").scale(0.5).to_edge(UL)
        parab2 = parab.copy()

        arrow = Arrow(start=RIGHT, end=LEFT, color=WHITE).next_to(parab, DOWN).shift(0.6*LEFT).scale(0.9)
        translation = Tex("Parabool $\\frac{b}{2a}$ naar links").next_to(arrow, DOWN).shift(0.4*UP).scale(0.5)

        arrow_translation = VGroup(arrow, translation)

        self.play(Create(VGroup(text, parab2)), run_time=4)
        self.play(FadeOut(extrema_coords))
        self.play(Create(arrow_translation))
        self.wait(2)
        self.play(parab2.animate.set_color(RED).shift(1.51*LEFT), run_time=3)
        self.play(FadeOut(arrow_translation))
        self.wait()

        graph = VGroup(plane, parab, parab2, labels)
        self.play(graph.animate.to_edge(LEFT))
        self.wait()

        parab2_label1 = (
            MathTex("g(x') = a(x' - \\frac{b}{2a})^2 + b(x' - \\frac{b}{2a}) + c")
            .scale(0.5)
            .next_to(parab_label, DOWN)
            .set_color(RED)
        )

        parab2_label2 = (
            MathTex("g(x') = ax'^2 - \\frac{b^2}{4a} + c")
            .scale(0.6)
            .next_to(parab2_label1, DOWN)
            .set_color(RED)
        )
        
        self.play(Create(VGroup(parab2_label1, parab2_label2)), run_time=5)
        self.wait()

        intersect1 = (
            Tex("De snijpunten van $g(x)$ met de $x$-as: $g(x) = 0$")
            .scale(0.5)
            .next_to(parab2_label2, DOWN)
            .set_color(RED)
        )

        dot1_1 = Dot(plane.get_origin() + [-1.5*0.6, 0, 0], color=RED)
        dot1_2 = Dot(plane.get_origin() + [1.5*0.6, 0, 0], color=RED)

        intersect2 = (
            MathTex("ax'^2 - \\frac{b^2}{4a} + c = 0")
            .scale(0.5)
            .next_to(intersect1, DOWN)
            .set_color(RED)
        )

        intersect3 = (
            Tex("Als we dit oplossen voor $x'$, vinden we:")
            .scale(0.5)
            .next_to(intersect2, DOWN)
            .set_color(RED)
        )

        intersect4 = (
            MathTex("x' = \pm \\frac{\sqrt{b^2 - 4ac}}{2a}")
            .scale(0.5)
            .next_to(intersect3, DOWN)
            .set_color(RED)
        )

        parab2_intersect1 = MathTex("- \\frac{\sqrt{b^2 - 4ac}}{2a}").scale(0.5).move_to(dot1_1).shift(0.4*DOWN + 0.55*LEFT).set_color(RED)
        parab2_intersect2 = MathTex("\\frac{\sqrt{b^2 - 4ac}}{2a}").scale(0.5).move_to(dot1_2).shift(0.35*DOWN + 0.5*RIGHT).set_color(RED)

        intersect5 = (
            Tex("Nu substitueren we $x'$ weer terug naar $x$:")
            .scale(0.5)
            .next_to(intersect4, DOWN)
            .set_color(RED)
        )

        arrow_dot1 = Arrow(start=LEFT, end=RIGHT, color=WHITE).next_to(dot1_1, RIGHT).scale(0.7).shift(0.2*LEFT).set_color(LIGHT_BROWN)
        dot2_1 = Dot(plane.get_origin() + [1*0.6, 0, 0], color=GREEN)

        arrow_dot2 = Arrow(start=LEFT, end=RIGHT, color=WHITE).next_to(dot1_2, RIGHT).scale(0.7).shift(0.2*LEFT).set_color(LIGHT_BROWN)
        dot2_2 = Dot(plane.get_origin() + [4*0.6, 0, 0], color=GREEN)

        intersect6 = (
            MathTex("x + \\frac{b}{2a} = \pm \\frac{\sqrt{b^2 - 4ac}}{2a} ")
            .scale(0.5)
            .next_to(intersect5, DOWN)
            .set_color(RED)
        )

        intersect7 = (
            MathTex("x = \\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
            .scale(0.7)
            .next_to(intersect6, DOWN)
            .set_color(RED)
        )

        rectangle = Rectangle(color=WHITE, height=1.25).surround(intersect7)

        parab1_intersect1 = MathTex("\\frac{-b - \sqrt{b^2 - 4ac}}{2a}").scale(0.5).move_to(dot2_1).shift(0.35*UP + 0.45*LEFT).set_color(GREEN)
        parab1_intersect2 = MathTex("\\frac{-b + \sqrt{b^2 - 4ac}}{2a}").scale(0.5).move_to(dot2_2).shift(0.35*UP + 0.5*RIGHT).set_color(GREEN)

        self.play(Create(intersect1), run_time=2)
        self.play(Create(VGroup(dot1_1, dot1_2)), run_time=2)
        self.wait()

        self.play(Create(VGroup(intersect2, intersect3, intersect4)), run_time=6)
        self.play(Create(VGroup(parab2_intersect1, parab2_intersect2)), run_time=3)
        self.wait()

        self.play(Create(intersect5), run_time=2)

        self.play(Create(VGroup(arrow_dot1, dot2_1)), run_time=2)
        self.wait()
        self.play(FadeOut(arrow_dot1))
        self.wait()

        self.play(Create(VGroup(arrow_dot2, dot2_2)), run_time=2)
        self.wait()
        self.play(FadeOut(arrow_dot2))
        self.wait()

        self.play(Create(VGroup(intersect6, intersect7)), run_time=4)
        self.play(Create(rectangle))
        self.wait()

        self.play(Create(VGroup(parab1_intersect1, parab1_intersect2)), run_time=3)
        self.wait(3)


def draw_func(func, title):
    x = np.arange(-3, 3, 0.01)
    y = [func(num) for num in x]

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


    plt.xlim(-3, 3)
    plt.ylim(-1, 8)

    plt.plot(x, y, 'darkturquoise')
    plt.hlines(xmin=-3, xmax=3, y=0, colors='#D3D3D3')
    plt.vlines(ymin=-2, ymax=8, x=0, colors='#D3D3D3')
    # plt.scatter([2], [0], c='darkturquoise')

    plt.savefig(f"{title}.svg")
    plt.show()

    plt.clf()

draw_func(lambda x: x**2 + 1, "f(x) = x² + 1")


def draw_funcs(func, func2, title):
    x = np.arange(-2, 6, 0.01)
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


    plt.xlim(-2, 6)
    plt.ylim(-10, 10)

    plt.plot(x, f, 'darkturquoise', label='f(x)')
    plt.plot(x, g, 'springgreen', label='g(x)')
    plt.hlines(xmin=-2, xmax=6, y=0, colors='#D3D3D3')
    plt.vlines(ymin=-10, ymax=10, x=0, colors='#D3D3D3')
    plt.scatter([2 - np.sqrt(6), 2 + np.sqrt(6)], [(2 - np.sqrt(6))**2 - 6*(2 - np.sqrt(6)) - 1, (2 + np.sqrt(6))**2 - 6*(2 + np.sqrt(6)) - 1], c='aquamarine')
    plt.legend(loc="upper right")

    plt.savefig(f"{title}.svg")
    plt.show()

    plt.clf()

# draw_funcs(lambda x: x**2 -6*x - 1, lambda x: -x**2 + 2*x + 3, "f(x) = x² - 6x - 1; g(x) = -x² + 2x + 3")