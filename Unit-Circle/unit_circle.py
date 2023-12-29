from manim import *
import numpy as np
import sympy as sp

class UnitCircle(Scene):
    def construct(self):
            global circle_scale_factor
            circle_scale_factor = 1

            plane = NumberPlane(x_range=[-1, 1, 1], x_length=8, y_range=[-1, 1, 1], y_length=8).add_coordinates()

            theta = ValueTracker(0.001)
            radius = 4
            circle = Circle(radius=radius, color=WHITE)

            def set_points(radius, theta, circle_center):
                global circle_scale_factor

                point_1 = circle_center + [0, 0, 0]
                point_2 = circle_center + [circle_scale_factor * radius * np.cos(theta), 0, 0]
                point_3 = circle_center + [circle_scale_factor * radius * np.cos(theta), circle_scale_factor * radius * np.sin(theta), 0]
                return point_1, point_2, point_3
                            
            def draw_triangle(radius, theta, circle_center):
                point_1, point_2, point_3 = set_points(radius=radius, theta=theta, circle_center=circle_center)
                triangle = Polygon(point_1, point_2, point_3).set_color(BLUE)
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
                pass

            theta_symbol = always_redraw(lambda : MathTex("\\theta").move_to(circle.get_center() + [circle_scale_factor * 0.75 * np.cos(theta.get_value()/2), circle_scale_factor * 0.75 * np.sin(theta.get_value()/2), 0]).scale(scale_factor=circle_scale_factor))

            def draw_line(radius, theta):
                line = Line(start=[0, 0, 0], end=[radius * np.cos(theta), radius * np.sin(theta), 0]).set_color(GREEN)
                angle_split1, angle_split2 = str(sp.nsimplify(theta/np.pi)).split('/')
                angle_text = MathTex(f"\\theta = \\frac{{{angle_split1}}}{{{angle_split2}}} \\pi").next_to(line.get_end(), RIGHT).set_color(GREEN).scale(0.75)

                x_pos_split1, x_pos_split2 = str(sp.nsimplify(np.cos(theta))).split('/')
                y_pos_split1, y_pos_split2 = str(sp.nsimplify(np.sin(theta))).split('/')

                try:
                    x_pos_text = MathTex(f"\\frac{{{int(x_pos_split1)}}}{{{x_pos_split2}}}").move_to([radius * np.cos(theta), 0, 0]).shift(0.5 * DOWN).scale(0.5)
                except ValueError:
                    x_pos_text = MathTex(f"\\frac{{\\{(x_pos_split1)}}}{{{x_pos_split2}}}").move_to([radius * np.cos(theta), 0, 0]).shift(0.5 * DOWN).scale(0.5)
                
                try:
                    y_pos_text = MathTex(f"\\frac{{{int(y_pos_split1)}}}{{{y_pos_split2}}}").move_to([0, radius * np.sin(theta), 0]).shift(0.5 * RIGHT).scale(0.5)
                except ValueError:
                    y_pos_text = MathTex(f"\\frac{{\\{y_pos_split1}}}{{{y_pos_split2}}}").move_to([0, radius * np.sin(theta), 0]).shift(0.5 * RIGHT).scale(0.5)

                x_line = Line(start=[radius * np.cos(theta), -0.1, 0], end=[radius * np.cos(theta), 0.1, 0]).set_color(WHITE)
                y_line = Line(start=[-0.1, radius * np.sin(theta), 0], end=[0.1, radius * np.sin(theta), 0]).set_color(WHITE)

                whole_line = VGroup(line, angle_text, x_line, x_pos_text, y_line, y_pos_text)
                self.play(Create(whole_line), run_time=2)

                return whole_line

            geometry = VGroup(circle, triangle, angle, theta_symbol)

            self.play(DrawBorderThenFill(plane))
            self.play(Create(geometry), run_time=2)

            self.play(theta.animate.set_value(1/6 * np.pi), run_time=2)
            line1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/4 * np.pi), run_time=1)
            line2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/3 * np.pi), run_time=1)
            line3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/2 * np.pi), run_time=2)
            self.wait()

            

            whole_unit_circle = VGroup(plane, geometry, line1, line2, line3)
            circle_scale_factor=0.5
            self.play(whole_unit_circle.animate.scale(0.5).to_edge(DR))
            self.wait()


            explanation_text1 = Tex("All you need to remember: ").scale(0.5).to_edge(UL)
            explanation_text2 = Tex("The values: $ \\frac{1}{2} < \\frac{\sqrt{2}}{2} < \\frac{\sqrt{3}}{2} $").scale(0.5).next_to(explanation_text1, DOWN)
            explanation_text3 = Tex("With the corresponding angles: $ \\frac{1}{6} \pi < \\frac{1}{4} \pi < \\frac{1}{3} \pi $").scale(0.5).next_to(explanation_text2, DOWN)

            self.play(Create(VGroup(explanation_text1, explanation_text2, explanation_text3)), run_time=7)
            self.wait()