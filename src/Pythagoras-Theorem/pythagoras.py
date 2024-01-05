# Credit to https://www.youtube.com/watch?v=yfGtbNgcrQ8 for the proof

import math
from manim import *

class Pythagoras(Scene):
    def construct(self):
        a_line = Line(start=[0,0,0], end=[3,0,0]).set_color(BLUE)
        a_label = MathTex("a").move_to(a_line.get_center() + 0.5*DOWN).set_color(BLUE)
        a = VGroup(a_line, a_label)

        b_line = Line(start=[3,0,0], end=[3,4,0]).set_color(GREEN)
        b_label = MathTex("b").next_to(b_line.get_center() + 0.05*RIGHT).set_color(GREEN)
        b = VGroup(b_line, b_label)

        c_line = Line(start=[0,0,0], end=[3,4,0]).set_color(RED)
        c_label = MathTex("c").move_to(c_line.get_center() + LEFT*0.5).set_color(RED)
        c = VGroup(c_line, c_label)

        right_triangle_labeled = VGroup(a, b, c).scale(0.5)

        def square_1(a_line, b_line):
            a_sqr = a_line.copy()
            b_sqr = b_line.copy()
            self.play(Rotate(b_sqr, 1/2 * math.pi))
            self.play(a_sqr.animate.move_to([-0.75,0,0]), b_sqr.animate.move_to([1,0,0]))

            a_text = MathTex("a").move_to(a_sqr.get_center() + 0.25*UP).set_color(BLUE)
            b_text = MathTex("b").move_to(b_sqr.get_center() + 0.25*UP).set_color(GREEN)

            ab1 = VGroup(a_sqr, b_sqr)

            ab2 = ab1.copy()
            self.play(Rotate(ab2, - 1/2 * math.pi))
            self.play(ab2.animate.move_to([2, -1.75, 0]))

            ab3 = ab2.copy()
            self.play(Rotate(ab3, 1/2 * math.pi))
            self.play(ab3.animate.move_to([0.25, -3.5, 0]))

            ab4 = ab3.copy()
            self.play(Rotate(ab4, - 1/2 * math.pi))
            self.play(ab4.animate.move_to([-1.5, -1.75, 0]))

            text = VGroup(a_text, b_text)
            self.play(Create(text))

            return VGroup(ab1, ab2, ab3, ab4, text)


        def insert_triangles1(right_triangle):
            right_triangle1 = right_triangle.copy()
            self.play(Rotate(right_triangle1, 1/2 * math.pi))
            self.play(right_triangle1.animate.move_to([1, -0.75,0]))

            right_triangle2 = right_triangle.copy()
            self.play(Rotate(right_triangle2, -1/2 * math.pi))
            self.play(right_triangle2.animate.move_to([1,-0.75,0]))

            right_triangle3 = right_triangle.copy()
            self.play(right_triangle3.animate.move_to([-0.75,-2.5,0]))

            right_triangle4 = right_triangle.copy()
            self.play(Rotate(right_triangle4, math.pi))
            self.play(right_triangle4.animate.move_to([-0.75,-2.5,0]))

            a_sqr_text = MathTex("a^2").move_to(right_triangle1.get_center() + 1.75*LEFT).set_color(BLUE)
            b_sqr_text = MathTex("b^2").move_to(right_triangle3.get_center() + 1.75*RIGHT).set_color(GREEN)

            A_text1 = MathTex("A").move_to(right_triangle1.get_center() + 0.25*UR).set_color(WHITE)
            A_text2 = MathTex("A").move_to(right_triangle1.get_center() + 0.25*DL).set_color(WHITE)
            A_text3 = MathTex("A").move_to(right_triangle3.get_center() + 0.25*DR).set_color(WHITE)
            A_text4 = MathTex("A").move_to(right_triangle3.get_center() + 0.25*UL).set_color(WHITE)

            text_labels = VGroup(A_text1, A_text2, A_text3, A_text4)
            self.play(Create(text_labels))

            unshaded_area1 = Square(stroke_color=BLUE, fill_color=WHITE, fill_opacity=1, side_length=1.5).move_to(a_sqr_text)
            unshaded_area2 = Square(stroke_color=GREEN, fill_color=WHITE, fill_opacity=1, side_length=2).move_to(b_sqr_text)
            unshaded_area = VGroup(unshaded_area1, unshaded_area2)

            self.play(Create(unshaded_area), run_time=2)
            self.wait()
            self.play(Create(VGroup(a_sqr_text, b_sqr_text)))
            
            text_labels = VGroup(text_labels, a_sqr_text, b_sqr_text)

            return VGroup(right_triangle1, right_triangle2, right_triangle3, right_triangle4, unshaded_area, text_labels)


        def square_2(a_line, b_line):
            a_sqr = a_line.copy()
            b_sqr = b_line.copy()
            self.play(Rotate(b_sqr, 1/2 * math.pi))
            self.play(a_sqr.animate.move_to([-0.75,0,0]), b_sqr.animate.move_to([1,0,0]))

            a_text = MathTex("a").move_to(a_sqr.get_center() + 0.25*UP).set_color(BLUE)
            b_text = MathTex("b").move_to(b_sqr.get_center() + 0.25*UP).set_color(GREEN)

            ab1 = VGroup(a_sqr, b_sqr)

            ab2 = ab1.copy()
            self.play(Rotate(ab2, -1/2 * math.pi))
            self.play(ab2.animate.move_to([2, -1.75, 0]))

            ab3 = ab2.copy()
            self.play(Rotate(ab3, -1/2 * math.pi))
            self.play(ab3.animate.move_to([0.25, -3.5, 0]))

            ab4 = ab3.copy()
            self.play(Rotate(ab4, -1/2 * math.pi))
            self.play(ab4.animate.move_to([-1.5, -1.75, 0]))

            text = VGroup(a_text, b_text)
            self.play(Create(text))

            return VGroup(ab1, ab2, ab3, ab4, text)

        def insert_triangles2(right_triangle):
            right_triangle1 = right_triangle.copy()
            self.play(Rotate(right_triangle1, 1/2 * math.pi))
            self.play(right_triangle1.animate.move_to([1, -0.75,0]))

            right_triangle2 = right_triangle.copy()
            self.play(right_triangle2.animate.move_to([1.25,-2.5,0]))

            right_triangle3 = right_triangle.copy()
            self.play(Rotate(right_triangle3, -1/2 * math.pi))
            self.play(right_triangle3.animate.move_to([-0.5,-2.75,0]))

            right_triangle4 = right_triangle.copy()
            self.play(Rotate(right_triangle4, math.pi))
            self.play(right_triangle4.animate.move_to([-0.75,-1,0]))

            filled_square2 = VGroup(right_triangle1, right_triangle2, right_triangle3, right_triangle4)
            c_sqr_text = MathTex("c^2").move_to(filled_square2.get_center()).set_color(RED)

            A_text1 = MathTex("A").move_to(right_triangle1.get_center() + 0.25*UR).set_color(WHITE)
            A_text2 = MathTex("A").move_to(right_triangle2.get_center() + 0.25*DR).set_color(WHITE)
            A_text3 = MathTex("A").move_to(right_triangle3.get_center() + 0.25*DL).set_color(WHITE)
            A_text4 = MathTex("A").move_to(right_triangle4.get_center() + 0.25*UL).set_color(WHITE)

            unshaded_area = Square(stroke_color=RED, fill_color=WHITE, fill_opacity=1, side_length=2.5).move_to(c_sqr_text).rotate(37/DEGREES)

            text_labels = VGroup(A_text1, A_text2, A_text3, A_text4)

            self.play(Create(text_labels))
            self.play(Create(unshaded_area))
            self.wait()
            self.play(Create(c_sqr_text))

            return VGroup(filled_square2, text_labels, unshaded_area, c_sqr_text)


        # play animations
        self.play(Create(right_triangle_labeled))
        self.wait()
        self.play(right_triangle_labeled.animate.to_edge(UL))

        right_triangle = VGroup(a_line, b_line, c_line)
        A_text = MathTex('A').move_to(right_triangle.get_center() + 0.25*DR).set_color(WHITE)
        self.play(Create(A_text))

        square1 = square_1(a_line, b_line)
        self.wait()

        triangles1 = insert_triangles1(right_triangle)
        self.wait()

        filled_square = VGroup(triangles1, square1)
        self.play(filled_square.animate.to_edge(DL))
        self.wait()

        square2 = square_2(a_line, b_line)
        self.wait()

        triangles2 = insert_triangles2(right_triangle)
        self.wait()

        filled_square_2 = VGroup(square2, triangles2)
        self.play(filled_square_2.animate.to_edge(DR))

        text = Tex("Het witte gebied in beide vierkanten moet gelijk zijn, omdat er bij beide 4 dezelfde driehoeken in zijn gegaan. En dus moet er gelden dat:").scale(0.5).to_edge(UP)
        # text_long = Tex("Hier zien we dat het linker vierkant een oppervlakte heeft van de 4 driehoeken met oppervlakte $A^2$, 1 vierkant met oppervlakte $a^2$ en een ander vierkant met oppervlakte $b^2$. \\\\ Maar we kunnen de vier driehoeken ook indelen zoals bij het rechter vierkant. Dezelfde oppervlakte als net bestaat nu uit de vier driehoeken met oppervlakte $A^2$ en 1 vierkant met oppervlakte $c^2$. Dit vierkant met oppervlakte $c^2$ is dus in plaats van de twee oppervlaktes $a^2$ en $b^2$ in het linker vierkant. \\\\ Maar omdat het linker vierkant even groot moet zijn als het rechter vierkant, moet er gelden dat:").scale(0.5).to_edge(UP)
        formula = MathTex("a^2 + b^2 = c^2").scale(0.75).next_to(text, DOWN)
        rectangle = Rectangle(color=WHITE, height=1).surround(formula)
        self.play(Create(text), run_time=5)
        self.play(Create(VGroup(formula, rectangle)))
        self.wait(duration=5)