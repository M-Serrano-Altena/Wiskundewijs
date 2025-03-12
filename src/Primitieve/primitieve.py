from manim import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
import plotly.io as pio
from bs4 import BeautifulSoup
import sympy as sp
import numpy as np
import re
from src.Solver.src.solver.solve_calculations import custom_latex
import os
from pathlib import Path
import typing
from numbers import Number
from types import FunctionType

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


base_path = os.path.dirname(__file__)
base_path = os.path.dirname(base_path)
base_path = os.path.dirname(base_path)
asset_path = os.path.join(base_path, "mkdocs", "assets")


def replace_superscript(eq_string):
    def replace_superscript_logic(match):
        matched_super = match.group(1)
        matched_super_list = list(matched_super)
        index_list = [list_superscript.index(matched_super_list[i]) for i in range(len(matched_super_list))]
        letter_list = [list_corresp_letters[i] for i in index_list]
        letters_string = ''.join(letter_list)

        replace = "^" + f"{letters_string}"
        return replace


    string_superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻ"
    string_corresp_letters = "0123456789abcdefghijklmnopqrstuvwxyz"
    list_superscript = list(string_superscripts)
    list_corresp_letters = list(string_corresp_letters)

    
    eq_string = re.sub(f'([{string_superscripts}]+)', replace_superscript_logic, eq_string)

    return eq_string


def draw_func(
    func, title, x_range, y_range, func2=None, line=None, **kwargs
):
    global asset_path
    images_primitieve_path = os.path.join(asset_path, "images", "primitieven")
    os.chdir(images_primitieve_path)

    x = np.arange(x_range[0], x_range[1], 0.01)

    x1 = [num for num in x if sp.sympify(func(num)).is_real]
    f = [float(func(num)) for num in x1 if sp.sympify(func(num)).is_real]

    surface_type = kwargs.get("surface_type", "func1")

    if line is not None:
        x_line = x
        f_line = [float(line(num)) for num in x]

    if func2 is not None:
        x2 = [num for num in x if sp.sympify(func2(num)).is_real]
        f2 = [float(func2(num)) for num in x2 if sp.sympify(func2(num)).is_real]


    if func2 is not None:
        f_fill = [float(func(num)) for num in x1 if sp.sympify(func(num)).is_real and sp.sympify(func2(num)).is_real]
        f2_fill = [float(func2(num)) for num in x2 if sp.sympify(func(num)).is_real and sp.sympify(func2(num)).is_real]

        if len(x1) < len(x2):
            x = x1
        elif len(x2) < len(x1):
            x = x2
        elif len(x1) < len(x):
            x = x1
    
    else:
        f_fill = f
        if len(x1) < len(x):
            x = x1


    if line is not None:
        if func2 is not None:
            f_line_fill = [float(line(num)) for num in x if sp.sympify(func(num)).is_real and sp.sympify(func2(num)).is_real]

        else:
            f_line_fill = [float(line(num)) for num in x if sp.sympify(func(num)).is_real]
        


    fig = plt.figure(facecolor="none")

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
    ax.set_facecolor("none")

    ax.set_title(title, loc="center", color="#D3D3D3")

    if kwargs.get('no_ax', False):
        ax.set_yticks([])
        ax.set_xticks([])

        if kwargs.get('ab_loc', False) is not False:
            ab_loc = kwargs['ab_loc']
            plt.text(s=r"$a$", x=ab_loc[0,0] - 0.075, y=ab_loc[0,1], color="#D3D3D3", fontsize='x-large')
            plt.vlines(x=ab_loc[0,0], ymin=-0.35, ymax=0.35, color="#D3D3D3", zorder=4)

            plt.text(s=r"$b$", x=ab_loc[1,0] - 0.06, y=ab_loc[1,1], color="#D3D3D3", fontsize='x-large')
            plt.vlines(x=ab_loc[1,0], ymin=-0.35, ymax=0.35, color="#D3D3D3", zorder=4)


        if kwargs.get("use_c", False):
            x_symbol = sp.symbols('x', real=True)
            x_roots = [x1 for x1 in sp.solve(func(x_symbol)) if x.is_real]

            if kwargs.get('integral_range', False):
                integral_range = kwargs["integral_range"]
                c_xcoord = [x for x in x_roots if integral_range[0] + 0.001 < x < integral_range[1] - 0.001][0]

            else:
                c_xcoord = x_roots[0]

            plt.text(s=r"$c$", x=c_xcoord - 0.06, y=0.5, color="#D3D3D3", fontsize='x-large')
            plt.vlines(x=c_xcoord, ymin=-0.35, ymax=0.35, color="#D3D3D3", zorder=4)

    plt.xlim([float(x) for x in x_range])
    plt.ylim([float(y) for y in y_range])

    # x and y axes
    plt.hlines(xmin=x_range[0], xmax=x_range[1], y=0, colors="#D3D3D3", zorder=1)
    plt.vlines(ymin=y_range[0], ymax=y_range[1], x=0, colors="#D3D3D3", zorder=1)

    x_symbol = sp.Symbol('x', real=True)

    if type(kwargs.get("func_label", False)) is bool:
        func_label = kwargs.get("func_label", False)
        if func2 is not None:
            func_label_f = rf"$f(x) = {custom_latex(func(x_symbol))}$" if func_label else r"$f(x)$"
            func_label_g = rf"$g(x) = {custom_latex(func2(x_symbol))}$" if func_label else r"$g(x)$"
        else:
            func_label_f = rf"$f(x) = {custom_latex(func(x_symbol))}$" if func_label else r"$f(x)$"
    
    else:
        func_label = kwargs["func_label"]
        if func2 is not None:
            func_label_f = func_label[0]
            func_label_g = func_label[1]

        else:
            func_label_f = func_label

    # graph(s)
    plt.plot(x1, f, "darkturquoise", zorder=2, label=func_label_f)
    if func2 is not None:
        plt.plot(x2, f2, "crimson", zorder=2, label=func_label_g)
    
    if line is not None:
        plt.plot(x_line, f_line, "springgreen", zorder=2, label=kwargs.get("line_label", "Lijn"))


    # calculate and plot integral
    def plot_integral(main_color="springgreen", letter="V"):
        if kwargs.get('integral_range', False) is not False:

            if kwargs['integral_range'] == 'roots' or kwargs['integral_range'] == 'roots1':
                integral_range = sp.solve(func(x_symbol), real=True)
                integral_range = [float(x_root) for x_root in integral_range if x_root.is_real]
                integral_range = [integral_range[0], integral_range[-1]]

            elif kwargs['integral_range'] == 'roots2' and func2 is not None:
                integral_range = sp.solve(func2(x_symbol), real=True)
                integral_range = [float(x_root) for x_root in integral_range if x_root.is_real]
                integral_range = [integral_range[0], integral_range[-1]]

            elif kwargs['integral_range'] == 'intersect' and func2 is not None:
                integral_range = sp.solve(func(x_symbol) - func2(x_symbol), real=True)
                integral_range = [float(x_root) for x_root in integral_range if x_root.is_real]
                integral_range = [integral_range[0], integral_range[-1]]

            else:
                integral_range = kwargs['integral_range']

            
            if surface_type == 'func2' and func2 is not None:
                integral_func = func2(x_symbol)

            elif surface_type == 'between' and func2 is not None:
                integral_func = func(x_symbol) - func2(x_symbol)

            elif surface_type == "line" and line is not None:
                integral_func = line(x_symbol)

            else:
                integral_func = func(x_symbol)


            integral_area = sp.Abs(sp.integrate(integral_func, (x_symbol, integral_range[0], integral_range[1])))
            print(f"Area of {letter} = {integral_area}")

            if kwargs.get("split_factor", False) is not False or kwargs.get("x_split", False) is not False:
                if kwargs.get("x_split", False) is not False and kwargs["x_split"] == "root":
                    x_split = sp.nsolve(func(x_symbol), sp.N(np.mean(integral_range)))

                elif kwargs.get("x_split", False) is not False:
                    x_split = kwargs["x_split"]

                else:
                    integral = sp.integrate(integral_func)
                    x_split = sp.nsolve(integral - integral_area/kwargs["split_factor"], sp.N(np.mean(integral_range)))

                print(f"split at x = {x_split}")


                if surface_type == "between" and func2 is not None:
                    plt.fill_between(x, f_fill, f2_fill, where=[(x >= integral_range[0]) and (x <= x_split) for x in x], color="darkviolet", zorder=3, alpha=0.7)
                    plt.fill_between(x, f_fill, f2_fill, where=[(x > x_split) and (x <= integral_range[1]) for x in x], color="darkorchid", zorder=3, alpha=0.7)
                
                elif surface_type == "line" and line is not None:
                    plt.fill_between(x, f_line_fill, where=[(x >= integral_range[0]) and (x <= x_split) for x in x], color="darkviolet", zorder=3, alpha=0.7)
                    plt.fill_between(x, f_line_fill, where=[(x > x_split) and (x <= integral_range[1]) for x in x], color="darkorchid", zorder=3, alpha=0.7)

                else:
                    plt.fill_between(x, f_fill, where=[(x >= integral_range[0]) and (x <= x_split) for x in x], color=main_color, zorder=3, alpha=0.7)
                    plt.fill_between(x, f_fill, where=[(x > x_split) and (x <= integral_range[1]) for x in x], color="mediumspringgreen", zorder=3, alpha=0.7)


                if func2 is not None:
                    p_line_color = "springgreen"
                else:
                    p_line_color = "firebrick"

                if kwargs.get("split_line", True):
                    plt.vlines(x=x_split, ymin=y_range[0], ymax=y_range[1], color=p_line_color, zorder=4, linestyle="--", label=r"$x=p$")


                if kwargs.get("split_numbered", False):
                    if kwargs.get("split_loc", False) is not False:
                        split_loc = kwargs["split_loc"]
                        print(split_loc)
                        plt.text(s=r"$I$", x=split_loc[0, 0], y=split_loc[0, 1], color="white", fontsize='xx-large', zorder=4)
                        plt.text(s=r"$II$", x=split_loc[1, 0], y=split_loc[1, 1], color="white", fontsize='xx-large', zorder=4)

                    elif kwargs.get('V_loc_label', False) is not False:
                        V_loc_label = kwargs['V_loc_label']
                        plt.text(s=r"$I$", x=x_split - 0.5, y=V_loc_label[1], color="white", fontsize='xx-large', zorder=4)
                        plt.text(s=r"$II$", x=x_split + 0.5, y=V_loc_label[1], color="white", fontsize='xx-large', zorder=4)
                    else:
                        plt.text(s=r"$I$", x=x_split - 0.5, y=1, color="white", fontsize='xx-large', zorder=4)
                        plt.text(s=r"$II$", x=x_split + 0.5, y=1, color="white", fontsize='xx-large', zorder=4)       


            elif kwargs.get("riemann_amt", False):
                plt.fill_between(x, f_fill, where=[(x >= integral_range[0]) and (x <= integral_range[1]) for x in x], color=main_color, zorder=3, alpha=0.7)

                n = kwargs["riemann_amt"]
                if type(n) == bool:
                    n = 10
                elif type(n) == float:
                    n = int(n)
                
                dx = (integral_range[1] - integral_range[0]) / n
                x_riemann = np.arange(integral_range[0], integral_range[1], dx)
                f_riemann = [float(func(num)) for num in x_riemann]

                for xi, yi in zip(x_riemann, f_riemann):
                    ax.add_patch(plt.Rectangle((xi, 0), dx, yi, edgecolor='blue', facecolor='navy', alpha=0.5, zorder=4))

                if kwargs.get("arrow_riemann_h", False):
                    head_width = 0.2
                    head_length = head_width * 2/5
                    plt.arrow(x_riemann[0], -0.5, dx, 0, head_length=head_length, head_width=head_width, length_includes_head=True, color="white", zorder=4)
                    plt.arrow(x_riemann[0] + dx, -0.5, -dx, 0, head_length=head_length, head_width=head_width, length_includes_head=True, color="white", zorder=4)
                    plt.text(s=r"$\Delta x$", x=x_riemann[0] + head_length, y=-1, color="white", zorder=4)

                if kwargs.get("arrow_riemann_v", False):
                    head_width = 0.2
                    head_length = head_width * 4/5
                    plt.arrow(integral_range[0] -0.2, 0, 0, f_riemann[0], head_length=head_length, head_width=head_width, length_includes_head=True, color="white", zorder=4)
                    plt.arrow(integral_range[0] -0.2, f_riemann[0], 0, -f_riemann[0], head_length=head_length, head_width=head_width, length_includes_head=True, color="white", zorder=4)
                    plt.text(s=r"$f(x_1)$", x=integral_range[0] - 0.7, y=f_riemann[0]/2.2, color="white", zorder=4)

            else:
                if surface_type == "func2":
                    plt.fill_between(x, f2_fill, where=[(x >= integral_range[0]) and (x <= integral_range[1]) for x in x], color="lightcoral", zorder=3, alpha=0.7)
                    
                elif surface_type == "between":
                    plt.fill_between(x, f_fill, f2_fill, where=[(x >= integral_range[0]) and (x <= integral_range[1]) for x in x], color="darkviolet", zorder=3, alpha=0.7)
                
                elif surface_type == "line":
                    plt.fill_between(x, f_line_fill, where=[(x >= integral_range[0]) and (x <= integral_range[1]) for x in x], color="chocolate", zorder=3, alpha=0.7)
                
                elif surface_type == "line, func2":
                    plt.fill_between(x, f_line_fill, f2_fill, where=[(x >= integral_range[0]) and (x <= integral_range[1]) for x in x], color="goldenrod", zorder=3, alpha=0.7)

                else:
                    plt.fill_between(x, f_fill, where=[(x >= integral_range[0]) and (x <= integral_range[1]) for x in x], color=main_color, zorder=3, alpha=0.7)

                if kwargs.get('V_loc_label', False) is not False:
                    V_loc_label = kwargs['V_loc_label']
                    if type(V_loc_label) is np.ndarray:
                        for i in range(len(V_loc_label)):
                            plt.text(s=rf"${letter}$", x=V_loc_label[i][0], y=V_loc_label[i][1], color="white", fontsize='xx-large', zorder=3)
                    
                    else:
                        plt.text(s=rf"${letter}$", x=V_loc_label[0], y=V_loc_label[1], color="white", fontsize='xx-large', zorder=3)

    if kwargs.get("double_integral", False):
        if kwargs.get("integral_range", False) is not False:
            integral_range = kwargs["integral_range"]
            V_loc_label = kwargs.get("V_loc_label", False)
            print(V_loc_label)
            colors = ["springgreen", "mediumspringgreen"]
            letters = ["V", "W"]
            for i in range(len(integral_range)):
                kwargs["integral_range"] = integral_range[i]
                
                if V_loc_label is not False:
                    kwargs["V_loc_label"] = V_loc_label[i]

                plot_integral(main_color=colors[i], letter=letters[i])
    
    else:
        plot_integral(letter=kwargs.get("letter", "V"))


    # calculate and plot the roots
    if kwargs.get("root", False) or kwargs.get("root_values", False):

        if kwargs.get("root_values", False):
            x_roots = kwargs["root_values"]

        else:
            x_roots = sp.solve(func(x_symbol), real=True)
            x_roots_set = sp.solveset(func(x_symbol), domain=sp.S.Reals)
            if not x_roots_set.is_FiniteSet:
                x_roots = []
                counter = 0
                for x_root in x_roots_set:
                    if not x_root.is_real:
                        continue

                    if 0 < x_root < 2*np.pi:
                        x_roots.append(x_root)
                    else:
                        counter += 1

                    if counter > 10:
                        break 

            else:
                x_roots = [float(x_root) for x_root in x_roots if x_root.is_real]

        y_roots = [func(x_root) for x_root in x_roots]
        plt.scatter(x_roots, y_roots, c="aquamarine", zorder=4)


    # calculate and plot extrema
    if kwargs.get('diff') is not None and kwargs['diff']:
        diff = sp.diff(func(x))
        x_extrm = [float(num) for num in sp.solveset(diff, domain=sp.Interval(x_range[0], x_range[1]))]
        y_extrm = [func(x) for x in x_extrm]

        plt.scatter(x_extrm, y_extrm, c="springgreen", zorder=4)


    # calculate and plot intercepts
    if kwargs.get("intersect", False) is not False:
        if type(kwargs.get("intersect")) is bool:
            x_intersects = sp.solve(func(x_symbol) - func2(x_symbol), real=True)
            x_intersects_set = sp.solveset(func(x_symbol) - func2(x_symbol), domain=sp.S.Reals)
            if not x_intersects_set.is_FiniteSet:
                x_intersects = []
                counter = 0
                for x_intersect in x_intersects_set:
                    if not x_intersect.is_real:
                        continue

                    if 0 < x_intersect < 2*np.pi:
                        x_intersects.append(x_intersect)
                    else:
                        counter += 1

                    if counter > 10:
                        break 

            else:
                x_intersects = [float(x_intersect) for x_intersect in x_intersects if x_intersect.is_real]

        else:
            x_intersects = kwargs["integral_range"]
        
        print("intersection points: x = ", sorted(x_intersects))

        y_intersects = [func(x_intersect) for x_intersect in x_intersects]
        plt.scatter(x_intersects, y_intersects, c="aquamarine", zorder=5)


    if kwargs.get('p_xline', False):
        if func2 is not None:
            p_line_color = "springgreen"
        else:
            p_line_color = "firebrick"

        
        plt.vlines(x=kwargs["p_xline"], ymin=y_range[0], ymax=y_range[1], color=p_line_color, zorder=4, linestyle="--", label=r"$x=p$")



    plt.legend(loc="upper right")

    save_name = replace_superscript(title).replace('÷', '!divide!')
    plt.savefig(f"{save_name}.svg", dpi=300)
    plt.show()

    os.chdir(asset_path)


# draw_func(lambda x: 6*x**2, "f(x) = 6x²", x_range=(-2, 2), y_range=(-2, 8), root=False, integral_range=(0, 1), V_loc_label=(0.72, 1.75), func_label=True)
# draw_func(lambda x: -6*x**2, "f(x) = -6x²", x_range=(-2, 2), y_range=(-8, 2), root=False, integral_range=(0, 1), V_loc_label=(0.72, -1.75), func_label=True)
# draw_func(lambda x: sp.sin(x), "f(x) = sin(x)", x_range=(-4, 4), y_range=(-2, 2), root=False, integral_range=(-sp.pi, sp.pi), func_label=True, x_split=0, split_numbered=True, split_loc=np.array(([-np.pi/2 -0.025, -0.5], [np.pi/2 - 0.1, 0.4])).astype(float), split_line=False)

# draw_func(lambda x: sp.cos(0.5*x) + 3, "Oppervlakte onder de grafiek", x_range=(8, 14), y_range=(-2, 8), root=False, integral_range=(9, 13), V_loc_label=(11, 1.5), func_label=False)
# draw_func(lambda x: sp.cos(0.5*x) + 3, "Oppervlakte onder de grafiek (met 10 rechthoeken)", x_range=(8, 14), y_range=(-2, 8), root=False, integral_range=(9, 13), riemann_amt=10, func_label=False, arrow_riemann_h=True, arrow_riemann_v=True)
# draw_func(lambda x: sp.cos(0.5*x) + 3, "Oppervlakte onder de grafiek (met 100 rechthoeken)", x_range=(8, 14), y_range=(-2, 8), root=False, integral_range=(9, 13), riemann_amt=100, func_label=False)

# draw_func(lambda x: -x**2 + 2*x + 3 , "f(x) = -x² + 2x + 3", x_range=(-2, 4), y_range=(-2, 6), root=True, integral_range=(0, 3), V_loc_label=(1, 1.5), func_label=True, no_ax=True)
# draw_func(lambda x: -x**2 + 2*x + 3 , "f(x) = -x² + 2x + 3 (gesplitst)", x_range=(-2, 4), y_range=(-2, 6), root=True, integral_range=(0, 3), V_loc_label=(1, 1.5), func_label=True, no_ax=True, split_factor=2, split_numbered=True)

# draw_func(lambda x: sp.cos(x), "f(x) = cos(x)", x_range=(0, sp.pi), y_range=(-2, 2), root=False, integral_range=(sp.pi/6, 2/3 * sp.pi), func_label=True, no_ax=False, V_loc_label=(0.77, 0.23))
# draw_func(lambda x: sp.cos(x), "f(x) = cos(x) (gesplitst)", x_range=(0, sp.pi), y_range=(-2, 2), root=False, integral_range=(sp.pi/6, 2/3 * sp.pi), func_label=True, no_ax=False, V_loc_label=False, x_split='root', split_numbered=True, split_loc=np.array(([0.85, 0.25], [1.9, -0.26])).astype(float), split_line=False)
# draw_func(lambda x: sp.cos(x), "f(x) = cos(x) (p onbekend)", x_range=(0, sp.pi), y_range=(-2, 2), root=False, integral_range=(sp.pi/6, 5/6 * sp.pi), func_label=True, no_ax=False, V_loc_label=False, x_split='root', split_numbered=True, split_loc=np.array(([0.85, 0.25], [2.25, -0.4])).astype(float), split_line=False, p_xline=5/6*np.pi)

# draw_func(lambda x: 2/x, "f(x) = 2 ÷ x", x_range=(-10, 10), y_range=(-5, 5), root=False, integral_range=(-1000, -1), func_label=True, no_ax=False, V_loc_label=(-2.1, -0.8))

# draw_func(lambda x: sp.sqrt(x), "f(x) = sqrt(x)", x_range=(-1, 5), y_range=(-1, 3), root=False, double_integral=True, integral_range=np.array(([0, sp.cbrt(4)], [2, 2*sp.cbrt(4)])), func_label=True, no_ax=False, V_loc_label=np.array(([0.8, 0.35], [2.45, 0.6])))

# draw_func(lambda x: (4*x-7)**3 -10*x + 18, "f(x) = (4x-7)³ -10x + 18", x_range=(1, 2.5), y_range=(-2, 3), root=True, root_values=(1.33175, 1.80084, 2.1174), integral_range=(1.33175, 2.1174), func_label=True, no_ax=True, V_loc_label=(1.5, 0.75))
# draw_func(lambda x: (4*x-7)**3 -10*x + 18, "f(x) = (4x-7)³ -10x + 18 (gesplitst)", x_range=(1, 2.5), y_range=(-2, 3), root=True, root_values=(1.33175, 1.80084, 2.1174), integral_range=(1.33175, 2.1174), func_label=True, no_ax=False, V_loc_label=False,  x_split='root', split_numbered=True, split_loc=np.array(([1.54, 0.93], [1.95, -0.5])).astype(float), split_line=False)

# draw_func(func=lambda x: 6 - x**2, func2=lambda x: x + 4, title="f(x) = 6 - x²; g(x) = x + 4", x_range=(-4, 4), y_range=(-2, 8), root=False, intersect=True, integral_range='intersect', V_loc_label=(-0.65, 4.25), func_label=True, surface_type='between', letter='V')
# draw_func(func=lambda x: 6 - x**2, func2=lambda x: x + 4, title="f(x) = 6 - x²; g(x) = x + 4 (Opp I)", x_range=(-4, 4), y_range=(-2, 8), root=False, intersect=True, integral_range='intersect', V_loc_label=(-0.5, 3), func_label=True, surface_type='func1', letter='I')
# draw_func(func=lambda x: 6 - x**2, func2=lambda x: x + 4, title="f(x) = 6 - x²; g(x) = x + 4 (Opp II)", x_range=(-4, 4), y_range=(-2, 8), root=False, intersect=True, integral_range='intersect', V_loc_label=(-0.6, 1.65), func_label=True, surface_type='func2', letter='II')

# draw_func(func=lambda x: x**2 - 4*x + 6, func2=lambda x: -x**2 + 4*x, title="f(x) = x² - 4x + 6; g(x) = -x² + 4x", x_range=(-1, 5), y_range=(-1, 6), root=False, intersect=True, integral_range='intersect', V_loc_label=(1.8, 2.8), func_label=True, surface_type='between', letter='V', no_ax=True)
# draw_func(func=lambda x: x**2 - 4*x + 6, func2=lambda x: -x**2 + 4*x, title="f(x) = x² - 4x + 6; g(x) = -x² + 4x (gesplitst)", x_range=(-1, 5), y_range=(-1, 6), root=False, intersect=True, integral_range='intersect', V_loc_label=(1.8, 2.8), func_label=True, surface_type='between', letter='V', no_ax=True, split_factor=3, split_numbered=True, split_loc=np.array(([1.65, 2.9], [2.45, 2.9])).astype(float))


# draw_func(func=lambda x: -(x-2)**3, title="Functie met deel boven en deel onder de x-as", x_range=(-0.5, 4), y_range=(-8, 8), root=False, integral_range=(0.5, 3.5), ab_loc=np.array(([0.5 - 0.01, -1], [3.5 + 0.01, 0.5])), use_c=True, V_loc_label=False, func_label=False, letter='V', no_ax=True)

# draw_func(func=lambda x: 3*x - x**2, func2=lambda x: x**2 - 2.5*x + 1, title="Oppervlakte tussen twee functies onder de x-as", x_range=(-1, 4), y_range=(-1, 5), root=False, intersect=True, integral_range='intersect', V_loc_label=(1.3, 0.8), func_label=False, surface_type='between', letter='V', no_ax=True)
# draw_func(func=lambda x: 3*x - x**2 + 2, func2=lambda x: x**2 - 2.5*x + 3, title="Oppervlakte tussen twee functies onder de x-as (verschoven)", x_range=(-1, 4), y_range=(-1, 5), root=False, intersect=True, integral_range='intersect', V_loc_label=(1.3, 2.8), func_label=(r"$f(x) + c$", r"$g(x) + c$"), surface_type='between', letter='V', no_ax=True)

# draw_func(func=lambda x: sp.sqrt(x), func2=lambda x: x**2, title="f(x) = sqrt(x); g(x) = x²", x_range=(-0.5, 1.5), y_range=(-0.5, 1.5), root=False, intersect=True, integral_range='intersect', V_loc_label=(0.4, 0.4), func_label=True, surface_type='between', letter='V', no_ax=True)
# draw_func(func=lambda x: sp.sqrt(x), func2=lambda x: x**2, title="f(x) = sqrt(x); g(x) = x² (met lijn k; opp I)", x_range=(-0.5, 2), y_range=(-0.5, 2), root=False, intersect=True, integral_range='intersect', V_loc_label=(0.475, 0.3), func_label=True, surface_type='line, func2', letter='I', no_ax=False, line=lambda x: x, line_label=r"$k \! : y = x$")
# draw_func(func=lambda x: sp.sqrt(x), func2=lambda x: x**2, title="f(x) = sqrt(x); g(x) = x² (met lijn k; opp W)", x_range=(-0.5, 2), y_range=(-0.5, 2), root=False, intersect=True, integral_range='intersect', V_loc_label=(0.7, 0.4), func_label=True, surface_type='line', letter='W', no_ax=True, line=lambda x: x, line_label=r"$k \! : y = x$")

# draw_func(func=lambda x: sp.sin(3*x) + 2, func2=lambda x: sp.cos(3*x) + 2, title="f(x) = sin(3x) + 2; g(x) = cos(3x) + 2", x_range=(-1, 3), y_range=(-1, 5), root=False, intersect=True, integral_range=(1/12 * sp.pi, 2/3 * sp.pi), V_loc_label=np.array(([0.675, 2], [1.8, 2])), func_label=True, surface_type='between', letter='V', no_ax=False, p_xline=2/3*np.pi)

# draw_func(func=lambda x: sp.exp(x-4) - 2, func2=lambda x: sp.log(x), title="f(x) = e^(x - 4) - 2; g(x) = ln(x)", x_range=(-1, 6), y_range=(-4, 4), root=False, intersect=(0.13821, 5.29954), integral_range=(0.13821, 5.29954), V_loc_label=(2.6, -0.4), func_label=True, surface_type='between', letter='V', no_ax=False)
# draw_func(func=lambda x: sp.exp(x-4) - 2, func2=lambda x: sp.log(x), title="f(x) = e^(x - 4) - 2; g(x) = ln(x) (met lijn k)", x_range=(-1, 6), y_range=(-4, 4), root=False, intersect=(0.13821, 5.29954), integral_range=(0.13821, 5.29954), V_loc_label=(2, -0.1), func_label=True, surface_type='line, func2', letter='W', no_ax=False, line=lambda x: 0.706523519268244 * x - 2.07663, line_label=r"Lijn $k$")

def apply_func_to_array(func: FunctionType, array: typing.Union[np.ndarray, Number]) -> np.ndarray:
    try:
        obj = func(array)
    except ZeroDivisionError:
        obj = func(array + 1e-10)


    if np.isscalar(obj):
        return np.full(array.shape, obj).astype(float)
        
    return obj.astype(float)

def draw_func_3d(save_file: str, func: sp.Expr, x_range: tuple[int], y_range: tuple[int], integral_range: tuple[int]|str, func_label=False, add_caps=True, riemann=False, func2=None, rot_x_axis_line=0, surface_type: str="func1", **kwargs) -> None:
    """
    Generates a 3D plot of a function rotated around the x-axis and saves it as an HTML file.
    
    Parameters:
        save_file (str): Path to save the output HTML file.
        func (sympy expression): The function to be plotted.
        x_range (tuple): The range of x-values for the plot (min, max).
        y_range (tuple): The range of y-values for the plot (min, max).
        integral_range (tuple): The range of x-values for volume integration.
        func_label (bool, optional): Whether to display the function label in the plot. Defaults to False.
        add_caps (bool, optional): Whether to add caps at the ends of the rotated shape. Defaults to True.
        riemann (bool or int, optional): If True, creates a Riemann sum approximation. If an integer, sets the number of subdivisions. Defaults to False.
        func2 (sympy expression, optional): An optional second function defining the lower boundary for volume generation. Defaults to None.
        rot_x_axis_line (float, optional): Defines the rotation axis shift along the y-axis. Defaults to 0.
        **kwargs: Additional keyword arguments.
    
    Returns:
        None. The function saves the plot as an HTML file.
    """
    
    global asset_path

    def create_plot(save_file, colour_rotation_surface="springgreen", colour_2D_surface="green", letter="L"):
        """Creates and configures the 3D plot."""

        def create_caps(surface_combined, x_start, x_end, colorscale=[[0, colour_rotation_surface], [1, colour_rotation_surface]], hoverinfo='none'):
            """Creates the caps at the ends of the rotated shape."""

            def create_filled_disk(radius, height, theta, radius_inner=0):
                """Creates a filled disk at a given height."""
                r = np.linspace(radius_inner, radius, 100)
                R, Theta = np.meshgrid(r, theta)

                X_disk = np.full_like(R, height)
                Y_disk = R * np.cos(Theta)
                Z_disk = R * np.sin(Theta) + rot_x_axis_line

                return X_disk, Y_disk, Z_disk
            
            def compare_func_with_value(func: FunctionType, n2: Number) -> bool:
                """
                Checks if a function only returns a specific value (n2).
                """
                try:
                    result = func(None)  # Try calling the function with None
                except Exception:
                    return False  # If the function cannot handle None, we return False
                
                # Now compare the result with n2
                return result == n2
            
            radius_inner_lower = 0
            radius_inner_upper = 0

            if func2 is not None and not compare_func_with_value(func2_np, rot_x_axis_line) and surface_type == "between":
                radius_inner_lower = func2_np(x_start)
                radius_inner_upper = func2_np(x_end)

            X_lower_bound, Y_lower_bound, Z_lower_bound = create_filled_disk(
                func_np_shifted(x_start), x_start, theta, 
                radius_inner=radius_inner_lower
            )
            X_upper_bound, Y_upper_bound, Z_upper_bound = create_filled_disk(
                func_np_shifted(x_end), x_end, theta, 
                radius_inner=radius_inner_upper
            )

            surface_lower_bound = go.Surface(
                x=X_lower_bound, y=Y_lower_bound, z=Z_lower_bound, 
                colorscale=colorscale, opacity=0.5, showscale=False, 
                contours=dict(x=dict(highlight=True), y=dict(highlight=False), z=dict(highlight=False)), 
                hoverinfo=hoverinfo
            ) 
            surface_upper_bound = go.Surface(
                x=X_upper_bound, y=Y_upper_bound, z=Z_upper_bound, 
                colorscale=colorscale, opacity=0.5, showscale=False, 
                contours=dict(x=dict(highlight=True), y=dict(highlight=False), z=dict(highlight=False)), 
                hoverinfo=hoverinfo
            )

            surface_combined.extend([surface_lower_bound, surface_upper_bound])
            return surface_combined
        
        def create_filled_cylinder(surface_combined, r, x_start, x_end, theta, colorscale, name=None):
            """
            Creates a cylindrical volume element between two x values for Riemann sum visualization.
            """
            r = np.array([r, r])
            Theta, R = np.meshgrid(theta, r)

            X_cylinder = np.array([[x_start, x_end]]).T
            X_cylinder = np.repeat(X_cylinder, len(theta), axis=1)

            Y_cylinder = R * np.cos(Theta)
            Z_cylinder = R * np.sin(Theta)

            surface_cylinder = go.Surface(x=X_cylinder, y=Y_cylinder, z=Z_cylinder, colorscale=colorscale, opacity=0.6, showscale=False, contours=dict(x=dict(highlight=True), y=dict(highlight=False), z=dict(highlight=False)), hovertemplate=f"{name}<extra></extra>")
            surface_combined.append(surface_cylinder)

            return surface_combined

        x_symbol = sp.Symbol('x', real=True)
        func_np = sp.lambdify(x_symbol, func(x_symbol))

        # Create a shifted version of the function (relative to the rotation axis)
        func_np_shifted = sp.lambdify(x_symbol, func(x_symbol) - rot_x_axis_line)

        # Generate x values for plotting and integration
        x = np.linspace(*x_range, 100)
        x_volume = np.linspace(*integral_range, 100)
        x = np.sort(np.append(x, x_volume))

        # Compute function values and initialize y2 for a possible second function
        y = apply_func_to_array(func_np, x)

        # Create a meshgrid for 3D rotation (x along the volume and theta for the circular sweep)
        theta = np.linspace(0, 2 * np.pi, 100)
        X, Theta = np.meshgrid(x_volume, theta)

        # Convert the function into cylindrical coordinates for 3D plotting
        R_shifted = apply_func_to_array(func_np_shifted, X)
        Y = R_shifted * np.cos(Theta)
        Z = R_shifted * np.sin(Theta)

        R = apply_func_to_array(func_np, X)

        if surface_type == "func1":
            Z_diff = np.abs(R * np.sin(Theta))

        # If a second function is provided, compute its rotated values
        if func2 is not None:
            func2_np = sp.lambdify(x_symbol, func2(x_symbol))

            # Compute cylindrical coordinates for func2
            y2 = apply_func_to_array(func2_np, x)
            y2_volume = apply_func_to_array(func2_np, x_volume)

            R2 = apply_func_to_array(func2_np, X)
            Y2 = R2 * np.cos(Theta)
            Z2 = R2 * np.sin(Theta)

            # Compute the surface between the two functions
            if surface_type == "between":
                Z_diff = np.abs(apply_func_to_array(func_np, X) * np.sin(Theta) - Z2) + y2_volume
            
            # Compute the surface below the second function
            elif surface_type == "func2":
                Z_diff = Z2

        # Create the base surface plot of the original function
        surface_2D = go.Surface(
            x=X, 
            y=np.full_like(X, 0), 
            z=Z_diff, 
            colorscale=[[0, colour_2D_surface], [1, colour_2D_surface]], 
            opacity=0.6, 
            showscale=False, 
            contours=dict(x=dict(highlight=False), y=dict(highlight=False), z=dict(highlight=False)), 
            hoverinfo='skip'
        )

        # Create the 3D surface of the function after rotation
        surface_rotation = go.Surface(
            x=X, 
            y=Y, 
            z=Z + rot_x_axis_line, 
            colorscale=[[0, colour_rotation_surface], [1, colour_rotation_surface]], 
            opacity=0.6, 
            showscale=False, 
            contours=dict(x=dict(highlight=not riemann), y=dict(highlight=False), z=dict(highlight=False)), 
            hovertemplate=f"Lichaam {letter}<extra></extra>" if not riemann else None, 
            hoverinfo=None if not riemann else 'none'
        )

        # Combine the surfaces for visualization
        surface_combined = [surface_2D, surface_rotation]
        
        # If a second function (func2) is provided and the rotation axis is at y=0,
        # create a separate surface plot for func2's rotation.
        if func2 is not None and rot_x_axis_line == 0:
            surface_rotation2 = go.Surface(
                x=X, 
                y=Y2, # Radial component for func2 along Y-axis
                z=Z2, # Radial component for func2 along Z-axis
                colorscale=[[0, colour_rotation_surface], [1, colour_rotation_surface]], 
                opacity=0.6, 
                showscale=False, 
                contours=dict(x=dict(highlight=not riemann), y=dict(highlight=False), z=dict(highlight=False)), 
                hovertemplate=f"Lichaam {letter}<extra></extra>" if not riemann else None, 
                hoverinfo=None if not riemann else 'none'
            )
            surface_combined.append(surface_rotation2) # Add to the visualization

        # Remove the surfaces of the function you don't want to display
        if len(surface_combined) == 3:
            if surface_type == "func1":
                surface_combined.pop()
            elif surface_type == "func2":
                surface_combined.pop(1)

        if add_caps and not riemann:
            surface_combined = create_caps(surface_combined, x_start=x_volume[0], x_end=x_volume[-1])

        # Default camera position for the 3D visualization
        camera_eye = dict(x=0.9, y=-1.68, z=0.6)

        # If Riemann sum visualization is enabled, create the volume elements
        if riemann:
            surface_combined.pop(0) # Remove the original surface since Riemann sums replace it

             # Determine the number of Riemann slices
            if isinstance(riemann, bool):
                n = 10 # Default to 10 subdivisions if `riemann=True`
            elif isinstance(riemann, int):
                n = riemann # Use the provided number of subdivisions

            colorscale = [[0, 'blue'], [1, 'blue']]
            camera_eye = dict(x=0.13, y=-2, z=0.5)

            if n <= 50:
                # Generate subdivision points for the Riemann sum
                x_volume = np.linspace(*integral_range, n+1)
                y_volume = func_np(x_volume)

                # Create `n` filled cylinders to approximate the volume
                for i in range(n):
                    surface_combined = create_filled_cylinder(surface_combined, y_volume[i], x_volume[i], x_volume[i+1], theta, colorscale, name=f"Cilinder {i+1}")

                    # Optionally add caps to each cylinder
                    if add_caps:
                        surface_combined = create_caps(surface_combined, x_start=x_volume[i], x_end=x_volume[i+1], colorscale=colorscale, hoverinfo='skip')

            else:
                # For a large number of subdivisions, adjust the first surface instead of adding many cylinders
                print(len(surface_combined))
                surface_combined[0].contours.x.show = True
                for i in range(len(surface_combined)):
                    surface_combined[i].colorscale = colorscale

        # Define hover text for function line plot
        hover_template1 = '(%{x:.4f}, %{z:.4f})'+ f'<extra>f(x) = {func(x_symbol)}</extra>' if func_label else '(%{x:.4f}, %{z:.4f})' + f'<extra></extra>'

        line_functions = []

        # Create the function's curve in 3D space
        line_function = go.Scatter3d(
            x=x, 
            y=np.zeros_like(x), 
            z=y, 
            mode='lines', 
            line=dict(color="darkturquoise", width=5), 
            name=rf'$f(x) = {custom_latex(func(x_symbol))}$' if func_label else '$f(x)$', 
            hovertemplate=hover_template1
        )

        line_functions.append(line_function)

        if func2 is not None:
            hover_template2 = '(%{x:.4f}, %{z:.4f})'+ f'<extra>g(x) = {func2(x_symbol)}</extra>' if func_label else '(%{x:.4f}, %{z:.4f})' + f'<extra></extra>'

            line_function_2 = go.Scatter3d(
                x=x, 
                y=np.zeros_like(x), 
                z=y2, 
                mode='lines', 
                line=dict(color="firebrick", width=5), 
                name=rf'$g(x) = {custom_latex(func2(x_symbol))}$' if func_label else '$g(x)$', 
                hovertemplate=hover_template2
            )
            line_functions.append(line_function_2)
        
        # Create horizontal and vertical reference lines
        line_x_axis = go.Scatter3d(
            x=x_range, 
            y=[0, 0], 
            z=[0, 0], 
            mode='lines', 
            line=dict(color='#2e2e2e', width=5), 
            showlegend=False, 
            hoverinfo='skip'
        )
        
        line_y_axis = go.Scatter3d(
            x=[0, 0], 
            y=[0, 0], 
            z=y_range, 
            mode='lines', 
            line=dict(color='#2e2e2e', width=5), 
            showlegend=False, 
            hoverinfo='skip'
        )

        # Create the final 3D figure with all elements
        fig = go.Figure(data=[*surface_combined, *line_functions, line_x_axis, line_y_axis])

        fig.update_layout(
            scene=dict(
                xaxis=dict(title='X-as', range=x_range, titlefont=dict(color='#D3D3D3'), tickfont=dict(color='#D3D3D3'), showspikes=False),
                yaxis=dict(title='', showticklabels=False, range=y_range, titlefont=dict(color='#D3D3D3'), showspikes=False),
                zaxis=dict(title='Y-as', range=y_range, titlefont=dict(color='#D3D3D3'), tickfont=dict(color='#D3D3D3'), showspikes=False),
                aspectmode='cube',  # Set equal aspect ratio
                camera=dict(
                    eye=camera_eye,  # Adjust the camera position
                    center=dict(x=-0.25, y=-0, z=-0.25),
                    up=dict(x=0, y=0, z=1),  # Up the camera view
                ),
            ),
            paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background to transparent
            plot_bgcolor='rgba(0,0,0,0)',    # Set the plot background to transparent
            margin=dict(l=0, r=0, t=0, b=0),  # Reduce padding around the plot
            legend=dict(
                x=0.98,
                y=0.93,
                xanchor='right',
                yanchor='top',
                bgcolor='rgba(211,211,211,0.75)',
                font=dict(color='black'),
            ),
            hovermode='closest',
        )

        config = {
            'modeBarButtonsToRemove': ['orbitRotation', 'resetCameraDefault'],
            'displaylogo': False,
            'scrollZoom': True,
        }

        if save_file.endswith('.html'):
            save_file_html = save_file
            save_file_png = str(Path(save_file_png).stem + '.png')
        elif save_file.endswith('.png'):
            save_file_png = save_file
            save_file_html = str(Path(save_file_png).stem + '.html')
        else:
            save_file_html = save_file + '.html'
            save_file_png = save_file + '.png'

        interactive_image_path = os.path.join(asset_path, "interactive_images")
        os.chdir(interactive_image_path)
        pio.write_html(fig, file=save_file_html, config=config, auto_open=kwargs.get("auto_open", False)) # Save the figure as an interactive HTML file

        images_primitieve_path = os.path.join(asset_path, "images", "primitieven")
        os.chdir(images_primitieve_path)

        fig.write_image(save_file_png, scale=3)  # Save the figure as a PNG file

        

        interactive_image_path = os.path.join(asset_path, "interactive_images")
        os.chdir(interactive_image_path)

        return save_file_html

    def add_meta_tag(save_file):
        with open(save_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        if soup.head is None:
            soup.head = soup.new_tag('head')
            soup.html.insert(0, soup.head)

        meta_tag = soup.new_tag('meta', attrs={'name': 'color-scheme', 'content': 'light dark'})
        soup.head.append(meta_tag)

        script_tag1 = soup.new_tag('script', attrs={'src': "../javascripts/bundle.6c14ae12.min.js"})
        script_tag2 = soup.new_tag('script', attrs={'src': "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_HTMLorMML"})

        soup.head.extend([script_tag1, script_tag2])

        # Save the modified HTML back to the file
        with open(save_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))


    x_symbol = sp.Symbol('x', real=True)
    if integral_range == 'root':
        roots = sp.solve(func(x_symbol), x_symbol)
        if len(roots) >= 2:
            integral_range = (float(roots[0]), float(roots[-1]))
        else:
            raise ValueError("Not enough roots found to calculate integral range")
        
    elif integral_range == 'intersect':
        intersections = sp.solve(func(x_symbol) - func2(x_symbol), x_symbol)
        if len(intersections) >= 2:
            integral_range = (float(intersections[0]), float(intersections[-1]))
        else:
            raise ValueError("Not enough intersections found to calculate integral range")
    
    colour_matches_surface_type = kwargs.get("colour_matches_surface_type", False)

    surface_types = ['func1', 'func2', 'between']
    if surface_type not in surface_types and colour_matches_surface_type and colour_matches_surface_type in surface_types:
        raise ValueError(f"Invalid surface type. Expected one of: {', '.join(surface_types)}")
    elif surface_type in ['func2', 'between'] and func2 is None:
        raise ValueError("A second function must be provided for the selected surface type")

    surface_type_colour_map = {
        "func1": {"rotation": "springgreen", "2D": "green"},
        "func2": {"rotation": "lightcoral", "2D": "red"},
        "between": {"rotation": "violet", "2D": "indigo"}
    }

    colour_rotation_surface = kwargs.get("colour_rotation_surface") 
    colour_2D_surface = kwargs.get("colour_2D_surface")

    def get_colour(colour, surface_version):
        """Returns the colour if it is a valid surface type, otherwise returns None."""
        assert surface_version in ["rotation", "2D"]
        
        # if rotation type is given as colour, use the corresponding colour
        if colour in surface_types:
            return surface_type_colour_map[colour][surface_version]
        
        if colour_matches_surface_type in surface_types:
            return surface_type_colour_map[colour_matches_surface_type][surface_version]
        
        # if colour not given, use default colours
        if colour is None:
            return surface_type_colour_map[surface_type][surface_version]

        return colour

    colour_rotation_surface = get_colour(colour_rotation_surface, "rotation")
    colour_2D_surface = get_colour(colour_2D_surface, "2D")
    letter = kwargs.get("letter", "L")

    save_file_html = create_plot(save_file, colour_rotation_surface=colour_rotation_surface, colour_2D_surface=colour_2D_surface, letter=letter)
    add_meta_tag(save_file_html)

    os.chdir(asset_path)


# draw_func(lambda x: sp.cos(x) + 3, "Oppervlakte onder de grafiek - herhaling", x_range=(8, 14), y_range=(-2, 8), root=False, integral_range=(9, 13), V_loc_label=(11, 1.5), func_label=False)
# draw_func(lambda x: sp.cos(x) + 3, "Oppervlakte onder de grafiek - herhaling (met 100 rechthoeken)", x_range=(8, 14), y_range=(-2, 8), root=False, integral_range=(9, 13), riemann_amt=100, func_label=False)

# draw_func_3d("Grafiek wentelen om de x-as", lambda x: sp.cos(x) + 3, x_range=(8, 14), y_range=(-6, 6), root=False, integral_range=(9, 13), func_label=False, add_caps=True)
# draw_func_3d("Grafiek wentelen om de x-as (10 cilinders)", lambda x: sp.cos(x) + 3, x_range=(8, 14), y_range=(-6, 6), integral_range=(9, 13), func_label=False, add_caps=True, riemann=10)
# draw_func_3d("Grafiek wentelen om de x-as (50 cilinders)", lambda x: sp.cos(x) + 3, x_range=(8, 14), y_range=(-6, 6), integral_range=(9, 13), func_label=False, add_caps=True, riemann=50)

# draw_func_3d("f(x) = 2x^2 (3D)", lambda x: 2*x**2, x_range=(-1, 3), y_range=(-20, 20), integral_range=(0, 2), func_label=True, add_caps=True)
# draw_func_3d("f(x) = 4 - x^2 (3D)", lambda x: 4 - x**2, x_range=(-3, 3), y_range=(-5, 5), integral_range='root', func_label=True, add_caps=True)
# draw_func_3d("f(x) = sin(x) + cos(x) (3D)", lambda x: sp.sin(x) + sp.cos(x), x_range=(-1, 3), y_range=(-2, 2), integral_range=(0, 3*np.pi/4), func_label=True, add_caps=True)
# draw_func_3d("f(x) = sqrt(2x - 8) (3D)", lambda x: sp.sqrt(2*x - 8), x_range=(-1, 12), y_range=(-4, 4), integral_range=(4, 10), func_label=True, add_caps=True)

draw_func_3d(r"f(x) = (x+1) !divide! x (3D)", lambda x: (x+1)/x, func2=lambda x: 1, x_range=(0.01, 6), y_range=(-3, 3), integral_range=(1, 4), func_label=True, add_caps=True, surface_type="between", colour_matches_surface_type="func1", auto_open=True)
draw_func_3d(r"f(x) = (x+1) !divide! x (3D - om y=1)", lambda x: (x+1)/x, func2=lambda x: 1, x_range=(0.01, 6), y_range=(-3, 3), integral_range=(1, 4), func_label=True, add_caps=True, rot_x_axis_line=1, surface_type="between", letter="L₂", auto_open=True)
draw_func_3d(r"f(x) = 1 !divide! x (3D)", lambda x: 1/x, x_range=(0.01, 6), y_range=(-3, 3), integral_range=(1, 4), func_label=True, add_caps=True, letter="L₂", colour_matches_surface_type="between", auto_open=True)

# draw_func_3d("Opp tussen twee functies wentelen om x-as", lambda x: sp.sin(x) + 3, func2=lambda x: -sp.sin(x) + 3, x_range=(-0.5, np.pi), y_range=(-6, 6), integral_range="intersect", func_label=True, auto_open=True, surface_type='between')
# draw_func_3d("Opp tussen twee functies wentelen om x-as (Inhoud 1)", lambda x: sp.sin(x) + 3, func2=lambda x: -sp.sin(x) + 3, x_range=(-0.5, np.pi), y_range=(-6, 6), integral_range="intersect", func_label=True, auto_open=True, surface_type='func1', letter="I")
# draw_func_3d("Opp tussen twee functies wentelen om x-as (Inhoud 2)", lambda x: sp.sin(x) + 3, func2=lambda x: -sp.sin(x) + 3, x_range=(-0.5, np.pi), y_range=(-6, 6), integral_range="intersect", func_label=True, auto_open=True, surface_type='func2', letter="II")
