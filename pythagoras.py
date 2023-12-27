# Credit to https://www.youtube.com/watch?v=yfGtbNgcrQ8 for the proof

from manim import *

class Pythagoras(Scene):
    def construct(self):
        a = Line(start=[0,0,0], end=[3,0,0]).set_color(BLUE)
        b = Line(start=[3,0,0], end=[3,4,0]).set_color(GREEN)
        c = Line(start=[0,0,0], end=[3,4,0]).set_color(RED)

        right_triangle = VGroup(a, b, c).scale(0.5)

        def labels():
            a_label = Tex("a").next_to(right_triangle, DOWN)
            b_label = Tex("b").next_to(right_triangle, RIGHT)
            c_label = Tex("c").move_to(right_triangle.get_center() + LEFT*0.5)

            return VGroup(a_label, b_label, c_label)
        
        label = always_redraw(labels)

        self.play(Create(VGroup(right_triangle, label)))
        self.wait(duration=3)
        self.play(right_triangle.animate.to_edge(UL))

        