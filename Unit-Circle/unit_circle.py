from manim import *
import numpy as np
import sympy as sp

class UnitCircle(Scene):
    def construct(self):
            global circle_scale_factor
            circle_scale_factor = 1

            theta = ValueTracker(0.001)
            radius = 3

            plane = NumberPlane(x_range=[-1, 1, 1], x_length=2*radius, y_range=[-1, 1, 1], y_length=2*radius).add_coordinates()
            x_label = plane.get_x_axis_label(label='x')
            y_label = plane.get_y_axis_label(label='y').shift(radius/4 * 0.5*UP + radius/4 * 0.5*LEFT)

            labels = VGroup(x_label, y_label)


            circle = Circle(radius=radius, color=WHITE)


            def set_points(radius, theta, circle_center):
                global circle_scale_factor

                point_1 = circle_center
                point_2 = circle_center + [circle_scale_factor * radius * np.cos(theta), 0, 0]
                point_3 = circle_center + [circle_scale_factor * radius * np.cos(theta), circle_scale_factor * radius * np.sin(theta), 0] 
                return point_1, point_2, point_3


            def draw_triangle(radius, theta, circle_center):
                point_1, point_2, point_3 = set_points(radius=radius, theta=theta, circle_center=circle_center)

                if theta < 2 * np.pi:
                    triangle = Polygon(point_1, point_2, point_3).set_color(BLUE)

                else:
                    triangle = Dot(fill_opacity=0)

                return triangle
            

            def draw_angle(radius, theta, circle_center):
                point_1, _, point_3 = set_points(radius=radius, theta=theta, circle_center=circle_center)
                point_2 = circle_center + [circle_scale_factor * radius, 0, 0]

                angle = Angle.from_three_points(point_2, point_1, point_3, radius=0.5*circle_scale_factor)

                return angle
            
            triangle = always_redraw(lambda : draw_triangle(radius=radius, theta=theta.get_value(), circle_center=circle.get_center()))

            try:
                angle = always_redraw(lambda : draw_angle(radius=radius, theta=theta.get_value(), circle_center=circle.get_center()))

            except ValueError:
                angle = always_redraw(lambda : draw_angle(radius=radius, theta=theta.get_value() - 0.000001, circle_center=circle.get_center()))

            def draw_theta_symbol():
                if theta.get_value() < 2 * np.pi:
                    theta_symbol = MathTex("\\theta").move_to(circle.get_center() + [circle_scale_factor * 0.75 * np.cos(theta.get_value()/2), circle_scale_factor * 0.75 * np.sin(theta.get_value()/2), 0]).scale(scale_factor=circle_scale_factor)
                
                else:
                    theta_symbol = Dot(fill_opacity=0)

                return theta_symbol
            
            theta_symbol = always_redraw(draw_theta_symbol)

            def draw_line(radius, theta):
                line = Line(start=[0, 0, 0], end=[radius * np.cos(theta), radius * np.sin(theta), 0]).set_color(GREEN)
                integer, remainder = divmod(sp.nsimplify(theta/np.pi), 1)
                remainder = sp.nsimplify(remainder)
                angle_split1, angle_split2 = str(sp.nsimplify(remainder)).split('/')

                if integer == 0:
                    angle_text = MathTex(f"\\theta = \\frac{{{angle_split1}}}{{{angle_split2}}} \\pi").move_to(line.get_end()).shift([circle_scale_factor * 0.75 * np.cos(theta), circle_scale_factor * 0.75 * np.sin(theta), 0]).set_color(GREEN).scale(0.75 * radius/4)
                else:
                    angle_text = MathTex(f"\\theta = {integer} \\frac{{{angle_split1}}}{{{angle_split2}}} \\pi").move_to(line.get_end()).shift([circle_scale_factor * 0.75 * np.cos(theta), circle_scale_factor * 0.75 * np.sin(theta), 0]).set_color(GREEN).scale(0.75 * radius/4)
               
                x_pos_split1, x_pos_split2 = str(sp.nsimplify(np.cos(theta))).split('/')
                y_pos_split1, y_pos_split2 = str(sp.nsimplify(np.sin(theta))).split('/')

                if sp.sympify(x_pos_split1) > 0:
                    try:
                        x_pos_text = MathTex(f"\\frac{{{int((x_pos_split1))}}}{{{x_pos_split2}}}").move_to([radius * np.cos(theta), 0, 0]).shift(0.5 * DOWN).scale(0.5 * radius/4)
                    except ValueError:
                        x_pos_text = MathTex(f"\\frac{{\\{x_pos_split1.replace('(', '{').replace(')', '}')}}}{{{x_pos_split2}}}").move_to([radius * np.cos(theta), 0, 0]).shift(0.5 * DOWN).scale(0.5 * radius/4)
                
                else:
                    try:
                        x_pos_text = MathTex(f"- \\frac{{{-int(x_pos_split1)}}}{{{x_pos_split2}}}").move_to([radius * np.cos(theta), 0, 0]).shift(0.5 * DOWN).scale(0.5)
                    except ValueError:
                        x_pos_text = MathTex(f"- \\frac{{\\{str(-sp.sympify(x_pos_split1)).replace('(', '{').replace(')', '}')}}}{{{x_pos_split2}}}").move_to([radius * np.cos(theta), 0, 0]).shift(0.5 * DOWN).scale(0.5 * radius/4)
                
                # positive y value
                if sp.sympify(y_pos_split1) > 0:
                    try:
                        y_pos_text = MathTex(f"\\frac{{{int(y_pos_split1)}}}{{{y_pos_split2}}}").move_to([0, radius * np.sin(theta), 0]).shift(0.5 * RIGHT).scale(0.5 * radius/4)
                    except ValueError:
                        y_pos_text = MathTex(f"\\frac{{\\{y_pos_split1.replace('(', '{').replace(')', '}')}}}{{{y_pos_split2}}}").move_to([0, radius * np.sin(theta), 0]).shift(0.5 * RIGHT).scale(0.5 * radius/4)

                else:
                    try:
                        y_pos_text = MathTex(f"- \\frac{{{-int((y_pos_split1))}}}{{{(y_pos_split2)}}}").move_to([0, radius * np.sin(theta), 0]).shift(0.5 * RIGHT).scale(0.5 * radius/4)
                    except ValueError:
                        y_pos_text = MathTex(f"- \\frac{{\\{str(-sp.sympify(y_pos_split1)).replace('(', '{').replace(')', '}')}}}{{{y_pos_split2}}}").move_to([0, radius * np.sin(theta), 0]).shift(0.5 * RIGHT).scale(0.5 * radius/4)

                x_line = Line(start=[radius * np.cos(theta), -0.1, 0], end=[radius * np.cos(theta), 0.1, 0]).set_color(WHITE)
                y_line = Line(start=[-0.1, radius * np.sin(theta), 0], end=[0.1, radius * np.sin(theta), 0]).set_color(WHITE)

                whole_line = VGroup(line, angle_text, x_line, x_pos_text, y_line, y_pos_text)
                self.play(Create(whole_line), run_time=2)

                return whole_line

            geometry = VGroup(circle, triangle, angle, theta_symbol)

            self.play(DrawBorderThenFill(plane))
            self.play(Create(VGroup(labels, geometry)), run_time=2)

            self.play(theta.animate.set_value(1/6 * np.pi), run_time=2)
            line1_1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/4 * np.pi), run_time=1)
            line1_2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/3 * np.pi), run_time=1)
            line1_3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/2 * np.pi), run_time=2)
            self.wait()

            self.play(theta.animate.set_value(2/3 * np.pi), run_time=2)
            line2_1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(3/4 * np.pi), run_time=1)
            line2_2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(5/6 * np.pi), run_time=1)
            line2_3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1 * np.pi - 0.0001), run_time=2)
            self.wait()

            self.play(theta.animate.set_value(np.pi + 1/6 * np.pi), run_time=2)
            line3_1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 1/4 * np.pi), run_time=1)
            line3_2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 1/3 * np.pi), run_time=1)
            line3_3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 1/2 * np.pi), run_time=2)
            self.wait()

            self.play(theta.animate.set_value(np.pi + 2/3 * np.pi), run_time=2)
            line4_1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 3/4 * np.pi), run_time=1)
            line4_2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 5/6 * np.pi), run_time=1)
            line4_3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(2 * np.pi + 0.001), run_time=2)
            self.wait()


            whole_unit_circle = VGroup(plane, labels, geometry, line1_1, line1_2, line1_3, line2_1, line2_2, line2_3, line3_1, line3_2, line3_3, line4_1, line4_2, line4_3)
            circle_scale_factor=0.6
            self.play(whole_unit_circle.animate.scale(circle_scale_factor).to_edge(DR))
            self.wait()

            values_angles_text = Tex("All you need to remember: \\\\ The values: $\\frac{1}{2} < \\frac{\sqrt{2}}{2} < \\frac{\sqrt{3}}{2}$ and corresponding angles: $ \\frac{1}{6} \pi < \\frac{1}{4} \pi < \\frac{1}{3} \pi. $").scale(0.5).to_edge(UL).shift(0.25*RIGHT)

            self.play(Create(values_angles_text), run_time=7)

            quadrant1_text1 = Tex("For example: \\\\ In the first quadrant, we go from the point (1, 0) to the point (0,1). Which corresponds to $\\frac{1}{2} \pi$.").scale(0.5).next_to(values_angles_text, DOWN)


            def quarter_circle(x_range):
                return FunctionGraph(lambda x: circle.get_center()[1] + np.sqrt(round((circle_scale_factor * radius)**2 - (x - circle.get_center()[0])**2, 7)), x_range=x_range, color=RED)


            quarter_circ1 = quarter_circle(x_range=[circle.get_center()[0] + circle_scale_factor * radius, circle.get_center()[0], -0.01])
            quarter_circle_func = quarter_circ1.get_function()

            dot1 = Dot(quarter_circle_func(circle.get_center()[0] + circle_scale_factor * radius), color=RED)
            dot2 = Dot(quarter_circle_func(circle.get_center()[0]), color=RED)
            quadrant_1 = Tex("1").move_to(circle.get_center() + radius/4 * UR).scale(1.5 * circle_scale_factor/0.6)

            self.play(Create(quadrant1_text1), run_time=5)
            self.play(Create(VGroup(quadrant_1, dot1, quarter_circ1, dot2)), run_time=5)
            self.wait()

            quadrant1_text2 = Tex("This means that with the smallest angle of $\\theta = \\frac{1}{6} \pi$, the least amount of progress is made. \\\\ In other words, $x$ is closest to $x=1$ out of the 3 values, thus $x = \\frac{\sqrt{3}}{2}$. \\\\ The same is true for $y$, it is the closest value to 0 of the three values, and thus $y = \\frac{1}{2}$.").scale(0.5).next_to(quadrant1_text1, DOWN)
            quadrant1_text3 = Tex("The same applies if we look at $\\theta = \\frac{1}{3} \pi$. It is the biggest angle between $\\theta = 0 \\ \& \\ \\theta = \\frac{1}{2} \pi$ meaning that the most amount of progress is made to go from (1,0) to (0,1). This means that $x = \\frac{1}{2} \\ \& \\ y = \\frac{\sqrt{3}}{2}$.").scale(0.5).next_to(quadrant1_text2, DOWN)
            quadrant1_text4 = Tex("Finally, if we have the angle $\\theta = \\frac{1}{4} \pi$ then the progress is not the most, and not the least, but right in the middle. This means that we have $x=\\frac{\sqrt{2}}{2}$ and $y=\\frac{\sqrt{2}}{2}$.").scale(0.5).next_to(quadrant1_text3, DOWN)

            self.play(Create(VGroup(quadrant1_text2, quadrant1_text3, quadrant1_text4)), run_time=20)
            self.wait(duration=10)

            self.play(FadeOut(VGroup(quadrant1_text1, quadrant1_text2, quadrant1_text3, quadrant1_text4, quarter_circ1, dot1, dot2)), run_time=2)

            quarter_circ2 = quarter_circle(x_range=[circle.get_center()[0], circle.get_center()[0] - circle_scale_factor * radius, -0.01])
            quadrant2 = Tex("2").move_to(circle.get_center() + radius/4 * UL).scale(1.5 * circle_scale_factor/0.6)
            dot3 = Dot(quarter_circle_func(circle.get_center()[0] - circle_scale_factor * radius), color=RED)

            quadrant2_text1 = Tex("Now let's look at the second quadrant.").scale(0.5).next_to(values_angles_text, DOWN)

            self.play(Create(quadrant2_text1))
            self.play(Create(VGroup(quadrant2, dot2, quarter_circ2, dot3)), run_time=6)
            self.wait()

            quadrant2_text2 = Tex("It goes from $\\theta = \\frac{1}{2} \pi$ to $\\theta = \pi$, which is from (0,1) to (-1, 0). But we can still use the same values as before.").scale(0.5).next_to(quadrant2_text1, DOWN)
            quadrant2_text3 = Tex("First we subtract the starting angle, so in this case $\\frac{1}{2} \pi$ to our angle $\\theta$. Then we do the same as before. \\\\ For example:").scale(0.5).next_to(quadrant2_text2, DOWN)
            quadrant2_text4 = Tex("If we have the angle $\\theta = \\frac{5}{6} \pi$, then we subtract $\\frac{1}{2} \pi$ to get $\\theta = \\frac{1}{3} \pi$. This means that the most amount of progress is made to go from (0,1) to (-1, 0). From that it follows that we have $x= - \\frac{\sqrt{3}}{2}$ and $y=\\frac{1}{2}$.").scale(0.5).next_to(quadrant2_text3, DOWN)
            quadrant2_text5 = Tex("Looking at the angle $\\theta = \\frac{2}{3} \pi$, we can use the same method. First subtract the starting angle $\\frac{1}{2} \pi$ so that $\\theta = \\frac{1}{6} \pi$. This means that the least amount of progress is made to go from (0,1) to (-1, 0). ").scale(0.5).next_to(quadrant2_text4, DOWN)
            ending_text = Tex("These same principles can also be used to derive the values for the other half of the unit circle. But then you would subtract $\pi$ in the third quadrant and $1 \\frac{1}{2} \pi$ in the last quadrant, instead of the $\\frac{1}{2} \pi$ in the second quadrant or no subtraction in the first. Again, from that it follows that we have $x= - \\frac{1}{2}$ and $y=\\frac{\sqrt{3}}{2}$.").scale(0.5).next_to(quadrant2_text5, DOWN)

            quadrant3 = Tex("3").move_to(circle.get_center() + radius/4 * DL).scale(1.5 * circle_scale_factor/0.6)
            quadrant4 = Tex("4").move_to(circle.get_center() + radius/4 * DR).scale(1.5 * circle_scale_factor/0.6)

            self.play(Create(VGroup(quadrant2_text2, quadrant2_text3, quadrant2_text4)), run_time=20)
            self.play(FadeOut(VGroup(dot2, quarter_circ2, dot3)), run_time=2)
            self.play(Create(ending_text), Create(VGroup(quadrant3, quadrant4)), run_time=10)
            self.wait()
