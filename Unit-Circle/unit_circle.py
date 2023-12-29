from manim import *
import numpy as np
import sympy as sp

class UnitCircle(Scene):
    def construct(self):
            global circle_scale_factor
            circle_scale_factor = 1

            plane = NumberPlane(x_range=[-1, 1, 1], x_length=8, y_range=[-1, 1, 1], y_length=8).add_coordinates()
            x_label = plane.get_x_axis_label(label='x')
            y_label = plane.get_y_axis_label(label='y').shift(UP + 0.5*LEFT)

            labels = VGroup(x_label, y_label)

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
            self.play(Create(VGroup(labels, geometry)), run_time=2)

            self.play(theta.animate.set_value(1/6 * np.pi), run_time=2)
            line1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/4 * np.pi), run_time=1)
            line2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/3 * np.pi), run_time=1)
            line3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/2 * np.pi), run_time=2)
            self.wait()

            

            whole_unit_circle = VGroup(plane, labels, geometry, line1, line2, line3)
            circle_scale_factor=0.6
            self.play(whole_unit_circle.animate.scale(circle_scale_factor).to_edge(DR))
            self.wait()

            values_angles_text = Tex("All you need to remember: \\\\ The values: $\\frac{1}{2} < \\frac{\sqrt{2}}{2} < \\frac{\sqrt{3}}{2}.$ \\\\ And corresponding angles: $ \\frac{1}{6} \pi < \\frac{1}{4} \pi < \\frac{1}{3} \pi. $ \\\\ This is because:").scale(0.5).to_edge(UL)

            self.play(Create(values_angles_text), run_time=7)

            quadrants_text = Tex("In the first quadrant,\\\\ we go from the point (1, 0) to the point (0,1). \\\\ Which corresponds to $\\frac{1}{2} \pi$.").scale(0.5).next_to(values_angles_text, DOWN)

            print(circle.get_center())
            quarter_circle = FunctionGraph(lambda x: circle.get_center()[1] + np.sqrt((circle_scale_factor * radius)**2 - (x - circle.get_center()[0])**2), x_range= [circle.get_center()[0] + circle_scale_factor * radius, circle.get_center()[0], -0.01], color=RED)
            # dot1 = Dot([circle.get_center()[0], quarter_circle.underlying_function(circle.get_center()[0]), 0])
            # dot2 = Dot([circle.get_center()[0] + circle_scale_factor * radius, quarter_circle.underlying_function(circle.get_center()[0] + circle_scale_factor * radius), 0])
            quadrant_1 = MathTex("1").move_to(circle.get_center() + UR).scale(1.5)

            self.play(Create(quadrants_text), run_time=3)
            self.play(Create(VGroup(quadrant_1, quarter_circle)), run_time=5)
            self.wait()


