import math
from manim import *

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

        self.play(DrawBorderThenFill(plane))
        self.play(Create(VGroup(labels, parab, parab_label), run_time=3))
        self.wait()

        extrema_coords = MathTex("x_{top} = -\\frac{b}{2a}").move_to(parab.get_center() + 2.5*DOWN).scale(0.6)

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
        
        self.play(Create(VGroup(parab2_label1, parab2_label2)), run_time=2)
        self.wait()

        intersect1 = (
            Tex("De snijpunten van $g(x)$ met de $x$-as: $g(x) = 0$")
            .scale(0.5)
            .next_to(parab2_label2, DOWN)
            .set_color(RED)
        )

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
            MathTex("x' = \pm \\frac{1}{2a} \sqrt{b^2 - 4ac}")
            .scale(0.5)
            .next_to(intersect3, DOWN)
            .set_color(RED)
        )

        intersect5 = (
            Tex("Nu substitueren we $x'$ weer terug naar $x$:")
            .scale(0.5)
            .next_to(intersect4, DOWN)
            .set_color(RED)
        )

        intersect6 = (
            MathTex("x + \\frac{b}{2a} = \pm \\frac{1}{2a} \sqrt{b^2 - 4ac}")
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

        self.play(Create(VGroup(intersect1, intersect2, intersect3, intersect4, intersect5, intersect6, intersect7)), run_time=15)
        self.play(Create(rectangle))
        self.wait(2)

