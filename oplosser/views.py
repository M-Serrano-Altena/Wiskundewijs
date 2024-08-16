from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.http import url_has_allowed_host_and_scheme
from django.template.loader import render_to_string
import sympy as sp
import numpy as np
from django.conf import settings
import os
import json
import multiprocessing
from src.Solver.src.solver.solve_calculations import Solve, math_interpreter, custom_latex, custom_simplify
from src.Solver.src.solver.openai_api import chatgpt_get_explanation
from .forms import EquationForm
import ast
import html
import re


def serve_search_index(request):
    with open(os.path.join(settings.STATIC_ROOT, 'search', 'search_index.json')) as f:
        data = json.load(f)
    return JsonResponse(data)

def redirect_view(request, path):
    url = '/' + path
    if url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}):
        return redirect(url)
    else:
        return HttpResponseBadRequest("Bad redirect URL")


def add_solution_text(solution_text, new_text, new_line=True, latex=True, options=None):
    if type(options) is dict:
        if "new_line" in options:
            new_line = options["new_line"]

        if "latex" in options:
            latex = options["latex"]

    if (type(new_line) is not bool) and (type(new_line) is not int):
        raise TypeError("new_line must be a boolean or an integer")
    
    if type(latex) is not bool:
        raise TypeError("latex must be a boolean")

    if latex:
        if new_line and type(new_line) is not int:
            updated_text = f"<span class='arithmatex'>{solution_text}<br>\\[\\boxed{{{new_text}}}\\]</span>"

        elif not new_line:
            updated_text = f"<span class='arithmatex'>{solution_text}\\[\\boxed{{{new_text}}}\\]</span>"

        elif type(new_line) is int:
            amt_new_line = new_line * "<br>"
            updated_text = f"<span class='arithmatex'>{solution_text}{amt_new_line}\\[\\boxed{{{new_text}}}\\]</span>"
    
    else:
        if new_line and type(new_line) is not int:
            updated_text = f"{solution_text}<br>{new_text}<br>"

        elif not new_line:
            updated_text = f"{solution_text}{new_text}<br>"

        elif type(new_line) is int:
            amt_new_line = new_line * "<br>"
            updated_text = f"{solution_text}{amt_new_line}{new_text}<br>"

    solution_text = updated_text
    return solution_text


def get_view_attributes(equation_text, queue):
    solver = Solve(input_string=equation_text)
    equation_interpret, outputs, plot = solver.solve_equation()
    numerical = solver.numerical
    data_chatgpt = {'equation_text': equation_text, 'equation_interpret': equation_interpret, 'outputs': outputs}

    solution_text = ""
    plot_data = []
    view_x_range = []
    view_y_range = []
    for output in outputs:
        if type(output) is tuple:
            if '$' in output[0]:
                output = list(output)
                output[0] = output[0].replace('$', '\\(', 1)
                output[0] = output[0].replace('$', '\\)', 1)
                output = tuple(output)

            solution_text = add_solution_text(solution_text=solution_text, new_text=output[0], options=output[1])
        
        else:
            solution_text = add_solution_text(solution_text=solution_text, new_text=output)

    solution_text = add_solution_text(solution_text, new_text="", latex=False)

    if plot:
        try:
            plot_data, view_x_range, view_y_range = generate_plot_data(solver)
        except ValueError:
            plot = False
            solution_text += "<br>Error: Plot kon niet worden gegenereerd"

    if numerical:
        data_chatgpt = "numeriek"
    elif "error" in solution_text.casefold():
        data_chatgpt = "error"

    data = {'equation_text': equation_text, 'equation_interpret': equation_interpret, 'solution_text': solution_text, "plot": plot, 'plot_data': plot_data, 'x_range': view_x_range, 'y_range': view_y_range, 'data_chatgpt': rf"{data_chatgpt}"}
    return queue.put(data)


def solve_equation_view(request):
    if request.method == 'POST':
        form = EquationForm(request.POST)
        if form.is_valid():
            equation_text = form.cleaned_data['equation_text']

            manager = multiprocessing.Manager()
            queue = manager.Queue()

            process = multiprocessing.Process(target=get_view_attributes, args=(equation_text, queue))
            process.start()

            process.join(timeout=30) # process will be terminated after 30 seconds

            if process.is_alive():
                process.terminate()
                process.join()

                equation_interpret = math_interpreter(equation_text)
                solution_text = "<br>Error: Berekening duurt te lang"
                data_chatgpt = None
                data = {
                    "equation_interpret": equation_interpret,
                    "solution_text": solution_text,
                    "plot_data": [],
                    "x_range": None,
                    "y_range": None,
                    "plot": False,
                    "data_chatgpt": data_chatgpt
                }

            else:
                data = queue.get()
                

            if data["plot"]:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    html = render_to_string('oplosser/equation_result.html', {
                        'equation_text': equation_text,
                        'equation_interpret': data['equation_interpret'],
                        'solutions': data['solution_text'],
                        'plot': data['plot'],
                        'plot_data': json.dumps(data['plot_data']),
                        'x_range': data['x_range'],
                        'y_range': data['y_range'],
                        'title': 'Vergelijking Oplosser',
                        'data_chatgpt': data['data_chatgpt']
                    })
                    return JsonResponse({'result': html})
                
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('oplosser/equation_result.html', {
                    'equation_text': equation_text,
                    'equation_interpret': data['equation_interpret'],
                    'solutions': data['solution_text'],
                    'plot': data['plot'],
                    'title': 'Vergelijking Oplosser',
                    'data_chatgpt': data['data_chatgpt']
                })
                return JsonResponse({'result': html})

    else:
        form = EquationForm()

    return render(request, 'oplosser/equation_form.html', {'form': form, 'title': "Vergelijking Oplosser"})


def no_frac(num):
    if isinstance(num, sp.Rational) and (abs(num.p) > 100 or abs(num.q) > 100):
        return round(num.evalf(), 4)
    return num

def generate_plot_data(solver):
    x_range, view_y_range = solver.get_range()
    view_x_range = list(x_range)
    view_y_range = list(view_y_range)
    extended_range = 50*abs(x_range[1] - x_range[0])*np.array([-1, 1])
    dx = 0.0001

    if solver.vert_asympt_eq is not None and type(solver.vert_asympt_eq) is not list and not sp.solveset(solver.vert_asympt_eq).is_FiniteSet:
        extended_range = 5*abs(x_range[1] - x_range[0])*np.array([-1, 1])
        dx = 0.02

    x_range = np.array(x_range) + extended_range

    plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = solver.get_plot_data(x_range, dx=dx)
    if solver.multivariate:
        # swap the values
        plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = plottable_x2_coords, y2_coords, plottable_x1_coords, y1_coords
        solver.eq1, solver.eq2 = solver.eq2, solver.eq1
    
    plot_data = []

    if solver.derivative[0]:
        function_f_type = r"f'"
    elif solver.integral[0]:
        function_f_type = r"F"
    else:
        function_f_type = r"f"

    if len(solver.derivative) == 2 and solver.derivative[1]:
        function_g_type = r"g'"
    elif len(solver.integral) == 2 and solver.integral[1]:
        function_g_type = r"G"
    else:
        function_g_type = r"g"

    output_legend1 = f"${f"{function_f_type}({solver.symbol})" if not solver.multivariate else 'y'} = {custom_latex(sp.nsimplify(custom_simplify(solver.eq1(solver.symbol))))}$"
    output_legend2 = f"${f"{function_g_type}({solver.symbol})" if not solver.multivariate else 'y'} = {custom_latex(sp.nsimplify(custom_simplify(solver.eq2(solver.symbol))))}$"

    hoverinfo1 = f"{f'{function_f_type}({solver.symbol})' if not solver.multivariate else 'y'} = {str(sp.nsimplify(solver.eq1(solver.symbol))).replace('**', '^').replace('log', 'ln')}"
    hoverinfo2 = f"{f'{function_g_type}({solver.symbol})' if not solver.multivariate else 'y'} = {str(sp.nsimplify(solver.eq2(solver.symbol))).replace('**', '^').replace('log', 'ln')}"
    

    if len(hoverinfo1) > len(hoverinfo2):
        output_legend1 = output_legend1[:-1] + "\\qquad .$"
    else:
        output_legend2 = output_legend2[:-1] + "\\qquad .$"


    if solver.vert_asympt is None:
        plot_data.append({
            'x': list(plottable_x1_coords),
            'y': list(y1_coords),
            'type': 'scatter',
            'mode': 'lines',
            'name': output_legend1,
            'line': {'color': 'darkturquoise'},
            'hovertemplate': '(%{x:.4f}, %{y:.4f})'+ f'<extra>{hoverinfo1}</extra>',
        })
        plot_data.append({
            'x': list(plottable_x2_coords),
            'y': list(y2_coords),
            'type': 'scatter',
            'mode': 'lines',
            'name': output_legend2,
            'line': {'color': 'springgreen'},
            'hovertemplate': '(%{x:.4f}, %{y:.4f})'+ f'<extra>{hoverinfo2}</extra>',
        })
    
    else:
        skip1 = 0
        skip2 = 0
        plot_data_f = []
        plot_data_g = []

        for i in range(len(plottable_x1_coords)):

            if list(plottable_x1_coords[i]) and list(y1_coords[i]):
                plot_data_f.append({
                    'x': list(plottable_x1_coords[i]),
                    'y': list(y1_coords[i]),
                    'type': 'scatter',
                    'mode': 'lines',
                    'name': output_legend1,
                    'showlegend': i == skip1,
                    'line': {'color': 'darkturquoise'},
                    'hovertemplate': '(%{x:.4f}, %{y:.4f})'+ f'<extra>{hoverinfo1}</extra>',
                })
            
            else:
                skip1 += 1

            if list(plottable_x2_coords[i]) and list(y2_coords[i]):
                plot_data_g.append({
                    'x': list(plottable_x2_coords[i]),
                    'y': list(y2_coords[i]),
                    'type': 'scatter',
                    'mode': 'lines',
                    'name': output_legend2,
                    'showlegend': i == skip2,
                    'line': {'color': 'springgreen'},
                    'hovertemplate': '(%{x:.4f}, %{y:.4f})'+ f'<extra>{hoverinfo2}</extra>',
                })

            else:
                skip2 += 1

        plot_data = plot_data_f + plot_data_g
        plot_data_f, plot_data_g = [], []
        
    if not solver.intersect:
        return plot_data, view_x_range, view_y_range

    solver.x_intersect = [round(x, 8) for x in solver.x_intersect]
    solver.y_intersect = [round(y, 8) for y in solver.y_intersect]

    plot_data.append({
        'x': solver.x_intersect,
        'y': solver.y_intersect,
        'type': 'scatter',
        'mode': 'markers',
        'name': f"Snijpunt",
        'showlegend': False,
        'marker': {'color': 'black', 'size': 10},
    })

    return plot_data, view_x_range, view_y_range




def check_display_math(string, final=False):
    condition = not ((not (r"\[" in string and r"\]" in string)) ^ (not (r"\\[" in string and r"\\]" in string)))
    if condition and string != '':
        if final and "boxed" not in string:
            string = rf"\\boxed{{{string}}}"

        string = rf"\\[{string}\\]"

    elif final and "boxed" not in string:
        string = string.split(r"\[")[1]
        string = string.split(r"\]")[0]
        string = rf"\\[\boxed{{{string}}}\\]"

    string = check_forward_slash(string)
    
    return string

def check_forward_slash(string: str):
    string_list = list(string)
    for i in range(len(string_list)):
        if string_list[i] == '\t':
            string_list[i] = "t"
            string_list.insert(i, "\\")

    string = ''.join(string_list)
    return string 


def explain_equation_base(request, use_chatgpt=False):
    if request.method == 'GET':
        if use_chatgpt:
            data_chatgpt = request.GET.get("data_chatgpt", None)
            data_chatgpt = html.unescape(data_chatgpt)

            if data_chatgpt is None or data_chatgpt == "Geen uitleg beschikbaar" or data_chatgpt == "error":
                return JsonResponse({'explanation': "Geen uitleg beschikbaar"})
            
            elif data_chatgpt == "numeriek":
                return JsonResponse({'explanation': 'Voor numerieke oplossingen is er geen uitleg mogelijk <span style="arithmatex">\\( \\phantom{.} \\)</span> <span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc.--><path d="M256 512a256 256 0 1 0 0-512 256 256 0 1 0 0 512zm-96.7-123.3c-2.6 8.4-11.6 13.2-20 10.5s-13.2-11.6-10.5-20C145.2 326.1 196.3 288 256 288s110.8 38.1 127.3 91.3c2.6 8.4-2.1 17.4-10.5 20s-17.4-2.1-20-10.5C340.5 349.4 302.1 320 256 320s-84.5 29.4-96.7 68.7zM144.4 208a32 32 0 1 1 64 0 32 32 0 1 1-64 0zm192-32a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg></span>'})
            
            chatgpt_response = chatgpt_get_explanation(data_chatgpt)
            chatgpt_response_text = check_forward_slash(chatgpt_response.content)
            explanation_raw = ast.literal_eval(chatgpt_response_text)

        else:
            explanation_raw = {'steps': [{'explanation': 'We beginnen met de uitdrukking \\( e^{i \theta} \\), waar \\( \theta = \text{pi} \\). Dit is volgens de formule van Euler.', 'output': '\\[ e^{i \text{pi}} \\]'}, {'explanation': 'Volgens de formule van Euler weten we dat \\( e^{i \theta} = \text{cos}(\theta) + i \text{sin}(\theta) \\). Nu vullen we \\( \theta = \text{pi} \\) in.', 'output': '\\[ e^{i \text{pi}} = \text{cos}(\text{pi}) + i \text{sin}(\text{pi}) \\]'}, {'explanation': 'We weten dat \\( \text{cos}(\text{pi}) = -1 \\) en \\( \text{sin}(\text{pi}) = 0 \\). Dit geeft:', 'output': '\\[ e^{i \text{pi}} = -1 + i \\cdot 0 \\]'}, {'explanation': 'Dan kunnen we dit verder vereenvoudigen, omdat de imaginaire term \\( i \\cdot 0 \\) gelijk is aan 0.', 'output': '\\[ e^{i \text{pi}} = -1 \\]'}], 'final_answer': '\\[\\boxed{e^{i \text{pi}} = -1}\\]'} 
            explanation_raw = str(explanation_raw)
            explanation_raw = check_forward_slash(explanation_raw)
            explanation_raw = ast.literal_eval(str(explanation_raw))


        steps_list = explanation_raw['steps']
        explanation = ""

        for step in steps_list:
            explanation += check_forward_slash(step["explanation"]) + "<br><br>" + check_display_math(rf"{step["output"]}") + "<br>"

        final_answer = explanation_raw['final_answer']

        explanation += "We krijgen dus als eindantwoord:" + "<br><br>" + check_display_math(final_answer, final=True)
        
    else:
        explanation = "Geen uitleg beschikbaar"


    return JsonResponse({'explanation': explanation})


def explain_equation_dummy(request):
    return explain_equation_base(request, use_chatgpt=False)

def explain_equation(request):
    return explain_equation_base(request, use_chatgpt=True)