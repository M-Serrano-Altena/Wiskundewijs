from manim import *
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

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
                self.play(Create(whole_line), run_time=1)

                return whole_line

            geometry = VGroup(circle, triangle, angle, theta_symbol)

            self.play(DrawBorderThenFill(plane))
            self.play(Create(VGroup(labels, geometry)), run_time=1)

            self.play(theta.animate.set_value(1/6 * np.pi), run_time=1)
            line1_1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/4 * np.pi), run_time=0.5)
            line1_2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/3 * np.pi), run_time=0.5)
            line1_3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1/2 * np.pi), run_time=1)
            self.wait()

            self.play(theta.animate.set_value(2/3 * np.pi), run_time=1)
            line2_1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(3/4 * np.pi), run_time=0.5)
            line2_2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(5/6 * np.pi), run_time=0.5)
            line2_3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(1 * np.pi - 0.0001), run_time=1)
            self.wait()

            self.play(theta.animate.set_value(np.pi + 1/6 * np.pi), run_time=1)
            line3_1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 1/4 * np.pi), run_time=0.5)
            line3_2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 1/3 * np.pi), run_time=0.5)
            line3_3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 1/2 * np.pi), run_time=1)
            self.wait()

            self.play(theta.animate.set_value(np.pi + 2/3 * np.pi), run_time=1)
            line4_1 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 3/4 * np.pi), run_time=0.5)
            line4_2 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(np.pi + 5/6 * np.pi), run_time=0.5)
            line4_3 = draw_line(radius=radius, theta=theta.get_value())

            self.play(theta.animate.set_value(2 * np.pi + 0.001), run_time=1)
            self.wait()


            whole_unit_circle = VGroup(plane, labels, geometry, line1_1, line1_2, line1_3, line2_1, line2_2, line2_3, line3_1, line3_2, line3_3, line4_1, line4_2, line4_3)
            circle_scale_factor=0.6
            self.play(whole_unit_circle.animate.scale(circle_scale_factor).to_edge(DR))
            self.wait()

            values_angles_text = Tex("Het enige wat je hoeft te onthouden zijn deze waardes en hoeken: \\\\ Waardes: $\\frac{1}{2} < \\frac{\sqrt{2}}{2} < \\frac{\sqrt{3}}{2}$ en Hoeken: $ \\frac{1}{6} \pi < \\frac{1}{4} \pi < \\frac{1}{3} \pi.$").scale(0.75).to_edge(UL).shift(0.25*RIGHT)

            self.play(Create(values_angles_text), run_time=7)

            quadrant1_text1 = Tex("Welke waarde bij welke hoek hoort kan je zelf achter halen door te kijken naar het begin- en eindpunt en dan te kijken naar de voortgang. Bij een grotere hoek gaan de $x$ en $y$ waardes meer lijken op de eindwaardes en minder op de startwaardes.").scale(0.75).next_to(values_angles_text, DOWN).shift(0.4*RIGHT)

            self.play(Create(quadrant1_text1), run_time=5)
            self.wait()


def draw_unit_circle():
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
    

    ax.set_title("De Eenheidscirkel", loc='center', color='#D3D3D3')

    circ = plt.Circle((0, 0), radius=1, edgecolor='darkturquoise', facecolor='None')
    ax.add_patch(circ)
    ax.set_aspect('equal')

    plt.xlim(-1.2,1.2)
    plt.ylim(-1.2,1.2) 

    plt.vlines(x=0, ymin=-1.1, ymax=1.1, colors='#D3D3D3')
    plt.hlines(y=0, xmin=-1.1, xmax=1.1, colors='#D3D3D3')

    angles = [1/6 * sp.pi, 1/4 * sp.pi, 1/3 * sp.pi, 2/3  * sp.pi, 3/4 * sp.pi, 5/6 * sp.pi, 7/6 * sp.pi, 5/4 * sp.pi, 4/3 * sp.pi, 5/3 * sp.pi, 7/4 * sp.pi, 11/6 * sp.pi]
    counter = 0

    for theta in angles:
        plt.plot([0, sp.cos(theta)], [0, sp.sin(theta)], 'darkturquoise')

        integer, remainder = divmod(sp.nsimplify(theta/sp.pi), 1)
        remainder = sp.nsimplify(remainder)
        angle_split1, angle_split2 = str(sp.nsimplify(remainder)).split('/')

        if theta < sp.pi/2:
            plt.text(sp.cos(theta), sp.sin(theta) + 0.04, f"$\\theta = \\frac{{{angle_split1}}}{{{angle_split2}}} \\pi$", color="darkturquoise")

        elif theta < sp.pi:
            plt.text(sp.cos(theta) - 0.275, sp.sin(theta) + 0.025, f"$\\theta = \\frac{{{angle_split1}}}{{{angle_split2}}} \\pi$", color="darkturquoise")  
        
        elif theta < 3/2*sp.pi:
            plt.text(sp.cos(theta) - 0.28, sp.sin(theta) - 0.125, f"$\\theta = {integer} \\frac{{{angle_split1}}}{{{angle_split2}}} \\pi$", color="darkturquoise")
        
        elif theta < 2*sp.pi:
            plt.text(sp.cos(theta) - 0.02, sp.sin(theta) - 0.11, f"$\\theta = {integer} \\frac{{{angle_split1}}}{{{angle_split2}}} \\pi$", color="darkturquoise")
        
        x_pos_split1, x_pos_split2 = str(sp.nsimplify(sp.cos(theta))).split('/')
        y_pos_split1, y_pos_split2 = str(sp.nsimplify(sp.sin(theta))).split('/')


        if sp.sympify(x_pos_split1) > 0:
            try:
                plt.text(sp.cos(theta) - 0.019, 0.1, f"$\\frac{{{int((x_pos_split1))}}}{{{x_pos_split2}}}$", color="#D3D3D3")
            except ValueError:
                plt.text(sp.cos(theta) - 0.05, 0.1, f"$\\frac{{\\{x_pos_split1.replace('(', '{').replace(')', '}')}}}{{{x_pos_split2}}}$", color="#D3D3D3")
        
        else:
            try:
                plt.text(sp.cos(theta) - 0.0519, 0.1, f"$- \\frac{{{-int(x_pos_split1)}}}{{{x_pos_split2}}}$", color="#D3D3D3")
            except ValueError:
                if counter < 1 or counter > 2:
                    plt.text(sp.cos(theta) - 0.09, 0.1, f"$- \\frac{{\\{str(-sp.sympify(x_pos_split1)).replace('(', '{').replace(')', '}')}}}{{{x_pos_split2}}}$", color="#D3D3D3")
                else:
                    plt.text(sp.cos(theta) - 0.125, 0.1, f"$- \\frac{{\\{str(-sp.sympify(x_pos_split1)).replace('(', '{').replace(')', '}')}}}{{{x_pos_split2}}}$", color="#D3D3D3")
                
                counter += 1

        # positive y value
        if sp.sympify(y_pos_split1) > 0:
            try:
                plt.text(0.1, sp.sin(theta) - 0.01, f"$\\frac{{{int(y_pos_split1)}}}{{{y_pos_split2}}}$", color="#D3D3D3")
            except ValueError:
                plt.text(0.1, sp.sin(theta) - 0.01, f"$\\frac{{\\{y_pos_split1.replace('(', '{').replace(')', '}')}}}{{{y_pos_split2}}}$", color="#D3D3D3")

        else:
            try:
                plt.text(0.1, sp.sin(theta) - 0.01, f"$- \\frac{{{-int((y_pos_split1))}}}{{{(y_pos_split2)}}}$", color="#D3D3D3")
            except ValueError:
                    plt.text(0.1, sp.sin(theta) - 0.01, f"$- \\frac{{\\{str(-sp.sympify(y_pos_split1)).replace('(', '{').replace(')', '}')}}}{{{y_pos_split2}}}$", color="#D3D3D3")
       
        plt.hlines(y=float(sp.sin(theta)), xmin=-0.05, xmax=0.05, color="#D3D3D3")
        plt.vlines(x=float(sp.cos(theta)), ymin=-0.05, ymax=0.05, color="#D3D3D3")

    plt.savefig("Unit_Circle.svg")
    plt.show()
    

# draw_unit_circle()