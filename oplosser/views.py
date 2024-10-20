from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.http import url_has_allowed_host_and_scheme
from django.template.loader import render_to_string
import sympy as sp
import numpy as np
import regex as re
from django.conf import settings
import os
import json
import multiprocessing
from src.Solver.src.solver.solve_calculations import Solve, math_interpreter, custom_latex, custom_simplify
from src.Solver.src.solver.openai_api import ChatGPT
from .forms import EquationForm, QuestionForm
import ast
import html
import time
import traceback
import mistune

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


def get_view_attributes(equation_text, angle_mode, queue):
    angle_mode_map = {"automatic": None,  "degrees": True, "radians": False}

    solver = Solve(input_string=equation_text, use_degrees=angle_mode_map.get(angle_mode, None))
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
        except Exception:
            traceback.print_exc()
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
        start_time = time.time()
        form = EquationForm(request.POST)
        angle_mode = request.POST["angle_mode"]
        if form.is_valid():
            equation_text = form.cleaned_data['equation_text']

            manager = multiprocessing.Manager()
            queue = manager.Queue()

            process = multiprocessing.Process(target=get_view_attributes, args=(equation_text, angle_mode, queue))
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
                
            print(f"Solving - Time taken: {time.time() - start_time}")
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
    view_x_range, view_y_range = solver.get_range()

    extended_range = 50*abs(np.ptp(view_x_range))*np.array([-1, 1])
    dx = 0.0001

    if solver.vert_asympt_eq is not None and not isinstance(solver.vert_asympt_eq, list):
        dx = 0.02

    x_range = view_x_range + extended_range

    plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = solver.get_plot_data(x_range, dx=dx)

    # swap the values
    if solver.multivariate:
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

    output_legend1 = f"${f"{function_f_type}({solver.symbol})" if not solver.multivariate else 'y'} = {custom_latex(solver.eq1)}$"
    output_legend2 = f"${f"{function_g_type}({solver.symbol})" if not solver.multivariate else 'y'} = {custom_latex(solver.eq2)}$"

    hoverinfo1_func = str(solver.eq1).replace('**', '^').replace('log', 'ln')
    hoverinfo2_func = str(solver.eq2).replace('**', '^').replace('log', 'ln')

    if solver.real_root:
        if sp.sympify(solver.eq1).is_Piecewise:
            eq1 = solver.eq1.args[1][0]
            hoverinfo1_func = str(sp.sympify(re.sub(r"\bAbs\b", "", str(eq1))))
        if sp.sympify(solver.eq2).is_Piecewise:
            eq2 = solver.eq1.args[1][0]
            hoverinfo2_func = str(sp.sympify(re.sub(r"\bAbs\b", "", str(eq2))))

    hoverinfo1 = f"{f'{function_f_type}({solver.symbol})' if not solver.multivariate else 'y'} = {hoverinfo1_func}"
    hoverinfo2 = f"{f'{function_g_type}({solver.symbol})' if not solver.multivariate else 'y'} = {hoverinfo2_func}"
    get_hover_template = lambda hoverinfo: '(%{x:.4f}, %{y:.4f})' + f'<extra>{hoverinfo}</extra>'

    if len(hoverinfo1) > len(hoverinfo2):
        output_legend1 = output_legend1[:-1] + "\\qquad .$"
    else:
        output_legend2 = output_legend2[:-1] + "\\qquad .$"


    empty_plot_data = {'x': [None], 'y': [None], 'type': 'scatter', 'mode': 'lines', 'name': '', 'showlegend': True, 'line': {'color': 'rgba(0,0,0,0)'}, 'hoverinfo': 'skip'}

    if solver.vert_asympt is None:
        plot_data.append({
            'x': plottable_x1_coords,
            'y': y1_coords,
            'type': 'scatter',
            'mode': 'lines',
            'name': output_legend1,
            'line': {'color': 'darkturquoise'},
            'hovertemplate': get_hover_template(hoverinfo1),
        })
        # plot_data.append(empty_plot_data)
        plot_data.append({
            'x': plottable_x2_coords,
            'y': y2_coords,
            'type': 'scatter',
            'mode': 'lines',
            'name': output_legend2,
            'line': {'color': 'springgreen'},
            'hovertemplate': get_hover_template(hoverinfo2),
        })
    
    else:
        skip1 = 0
        skip2 = 0
        plot_data_f = []
        plot_data_g = []

        for i in range(len(plottable_x1_coords)):
            x1_coords_list = list(plottable_x1_coords[i].astype(float))
            x2_coords_list = list(plottable_x2_coords[i].astype(float))
            y1_coords_list = list(y1_coords[i].astype(float))
            y2_coords_list = list(y2_coords[i].astype(float))

            if x1_coords_list and y1_coords_list:
                plot_data_f.append({
                    'x': x1_coords_list,
                    'y': y1_coords_list,
                    'type': 'scatter',
                    'mode': 'lines',
                    'name': output_legend1,
                    'showlegend': i == skip1,
                    'line': {'color': 'darkturquoise'},
                    'hovertemplate': get_hover_template(hoverinfo1),
                })
            
            else:
                skip1 += 1

            if x2_coords_list and y2_coords_list:
                plot_data_g.append({
                    'x': x2_coords_list,
                    'y': y2_coords_list,
                    'type': 'scatter',
                    'mode': 'lines',
                    'name': output_legend2,
                    'showlegend': i == skip2,
                    'line': {'color': 'springgreen'},
                    'hovertemplate': get_hover_template(hoverinfo2),
                })

            else:
                skip2 += 1

        plot_data = plot_data_f + plot_data_g
        plot_data_f, plot_data_g = [], []

    if not solver.intersect:
        return plot_data, list(view_x_range), list(view_y_range)
    
    if not solver.solution_set.is_FiniteSet and not solver.numerical:
        solver.x_intersect = []
        counter = 0
        for solution in solver.solution_set.evalf():
            if x_range[0] <= solution <= x_range[1]:
                solver.x_intersect.append(solution)
                continue
            else:
                counter += 1
            if counter > 10:
                break

        solver.x_intersect = np.array(solver.x_intersect).astype(float)
        solver.y_intersect = solver.apply_func_to_array(solver.eq1_lambda_np, solver.x_intersect)

    elif solver.numerical:
        solver.x_intersect = solver.roots_numeric[(x_range[0] <= solver.roots_numeric) & (solver.roots_numeric <= x_range[1])]
        solver.y_intersect = solver.apply_func_to_array(solver.eq1_lambda_np, solver.x_intersect)

    solver.x_intersect = np.round(solver.x_intersect, decimals=8)
    solver.y_intersect = np.round(solver.y_intersect, decimals=8)    

    plot_data.append({
        'x': list(solver.x_intersect),
        'y': list(solver.y_intersect),
        'type': 'scatter',
        'mode': 'markers',
        'name': f"Snijpunt",
        'showlegend': False,
        'marker': {'color': 'black', 'size': 10},
    })

    return plot_data, list(view_x_range), list(view_y_range)


chatgpt = ChatGPT()

def check_display_math(string, final=False):
    condition = not ((not (r"\[" in string and r"\]" in string)) ^ (not (r"\\[" in string and r"\\]" in string)))
    if condition and string != '':
        if final and "boxed" not in string:
            string = rf"\\boxed{{{string}}}"

        string = rf"\\[{string}\\]"

    elif final and "boxed" not in string:
        string = string.split(r"\[")
        if len(string) > 1:
            string = string[1]

        string = string.split(r"\]")[0]
        string = rf"\\[\boxed{{{string}}}\\]"

    string = check_forward_slash(string)
    
    return string

def check_forward_slash(string: str) -> str:
    string_list = list(string)
    for i in range(len(string_list)):
        if string_list[i] == '\t':
            string_list[i] = "t"
            string_list.insert(i, "\\")

        elif string_list[i] == '\f':
            string_list[i] = "f"
            string_list.insert(i, "\\")

    string = ''.join(string_list)
    return string 

def explain_equation_base(request, use_chatgpt=False):
    start_time = time.time()
    generation_success = False
    if request.method == 'GET':
        if use_chatgpt:
            data_chatgpt = request.GET.get("data_chatgpt", None)
            data_chatgpt = html.unescape(data_chatgpt)

            if data_chatgpt is None or data_chatgpt == "Geen uitleg beschikbaar" or data_chatgpt == "error":
                return JsonResponse({'explanation': "Geen uitleg beschikbaar", 'generation_success': generation_success})
            
            elif data_chatgpt == "numeriek":
                return JsonResponse({'explanation': 'Voor numerieke oplossingen is er geen uitleg mogelijk <span style="arithmatex">\\( \\phantom{.} \\)</span><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc.--><path d="M256 512a256 256 0 1 0 0-512 256 256 0 1 0 0 512zm-96.7-123.3c-2.6 8.4-11.6 13.2-20 10.5s-13.2-11.6-10.5-20C145.2 326.1 196.3 288 256 288s110.8 38.1 127.3 91.3c2.6 8.4-2.1 17.4-10.5 20s-17.4-2.1-20-10.5C340.5 349.4 302.1 320 256 320s-84.5 29.4-96.7 68.7zM144.4 208a32 32 0 1 1 64 0 32 32 0 1 1-64 0zm192-32a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg></span>', 'generation_success': generation_success})
            
            chatgpt_response = chatgpt.get_explanation(data_chatgpt)
            chatgpt_response_text = check_forward_slash(chatgpt_response)
            explanation_raw = ast.literal_eval(chatgpt_response_text)
            generation_success = True

        else:
            explanation_raw = {"steps": [{"explanation": "We beginnen met de volgende vergelijking:", "output": "\\[\\sin(x) = \\dfrac{1}{2} \\sqrt{3}\\]"}, {"explanation": "Om dit op te lossen, moeten we eerst aan beide kanten een sinus hebben. Op de eenheidscirkel kunnen we aflezen dat we \\(\\frac{1}{2} \\sqrt{3}\\) kunnen schrijven als de sinus van \\(x = \\frac{1}{3} \\pi\\):", "output": "\\[\\sin(x) = \\sin \\left( \\dfrac{1}{3}\\pi \\right) \\]"}, {"explanation": "Nu kunnen we dit oplossen met de algemene oplossing voor een sinus:", "output": "\\[x = \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\, \\vee \\, x = \\pi - \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\]"}, {"explanation": "Hierbij is \\(n\\) een geheel getal (dit geven we ook aan als \\(n \\in \\mathbb{Z}\\) ). We kunnen de vergelijking nog verder versimpelen tot:", "output": "\\[x = \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\, \\vee \\, x = \\dfrac{2}{3}\\pi + n \\cdot 2\\pi \\]"}, {"explanation": "Dit is de formule voor alle oplossingen, maar we kunnen ook nog de oplossingen in het domein \\( \\left[ 0, 2\\pi \\right] \\) bepalen. We vullen dan alle gehele getallen in voor \\(n\\) die ons een uitkomst tussen \\(0\\) en \\(2\\pi\\) geven. <br> In dit geval is dat alleen voor \\( n=1 \\), dus we vinden als oplossingen:", "output": "\\[ x = \\dfrac{1}{3} \\pi \\, \\vee \\, x = \\dfrac{2}{3} \\pi \\]"}], "final_answer": "\\[\\boxed{1) \\quad x = \\frac{\\pi}{3} \\approx 1.04720}\\]<br>\\[\\boxed{2) \\quad x = \\frac{2 \\pi}{3} \\approx 2.09440}\\]"}
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

    print(f"Explanation - Time taken: {time.time() - start_time}")
    return JsonResponse({'explanation': explanation, 'generation_success': generation_success})


def explain_equation_dummy(request):
    return explain_equation_base(request, use_chatgpt=False)

def explain_equation(request):
    return explain_equation_base(request, use_chatgpt=True)

def format_answer(answer_question: str) -> str:
    markdown = mistune.create_markdown()

    answer_question = check_forward_slash(answer_question)
    answer_question = answer_question.replace("\\", r"\\")
    answer_question = markdown(answer_question)
    return answer_question

def answer_question(request):
    if request.method == "POST":
        start_time = time.time()
        form = QuestionForm(request.POST)
        if form.is_valid():
            explanation = request.POST.get("explanation")
            question = form.cleaned_data.get("question")

            if explanation is None or question is None:
                return JsonResponse({'explanation': "Er is iets mis gegaan. Probeer het anders opnieuw."})
            
            if chatgpt.amt_questions_asked() == 0:
                chatgpt.add_user_input(explanation)

            chatgpt_response = chatgpt.reply_to_question(question)
            answer_question = ast.literal_eval(chatgpt_response)["response"]
            answer_question = format_answer(answer_question)
            
        else:
            answer_question = "Geen uitleg beschikbaar"

        print(f"Answer Question - Time taken: {time.time() - start_time}")

        return JsonResponse({'answer': answer_question})

    else:
        form = QuestionForm()

    return render(request, 'equation_result.html', {'form': form})

