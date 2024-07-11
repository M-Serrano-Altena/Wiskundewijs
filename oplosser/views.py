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
from src.Solver.src.solver.solve_calculations import Solve, math_interpreter
from .forms import EquationForm

# Create your views here.
def solve_html(request):
    x = sp.symbols('x', real=True)
    solution = sp.solve(x**2 - 4, x)
    # return HttpResponse(str(solution))
    return render(request, "oplosser/solver.html")


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

    if plot:
        plot_data, view_x_range, view_y_range = generate_plot_data(solver)

    data = {'equation_text': equation_text, 'equation_interpret': equation_interpret, 'solution_text': solution_text, "plot": plot, 'plot_data': plot_data, 'x_range': view_x_range, 'y_range': view_y_range}
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

            process.join(timeout=30)

            if process.is_alive():
                process.terminate()
                process.join()

                equation_interpret = math_interpreter(equation_text)
                solution_text = "<br>Error: Berekening duurt te lang"
                data = {
                    "equation_interpret": equation_interpret,
                    "solution_text": solution_text,
                    "plot_data": [],
                    "x_range": None,
                    "y_range": None,
                    "plot": False
                }

            else:
                data = queue.get()
                    
            if data["plot"]:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    html = render_to_string('oplosser/equation_result.html', {
                        'equation_text': equation_text,
                        'equation_interpret': data['equation_interpret'],
                        'solutions': data['solution_text'],
                        'plot_data': json.dumps(data['plot_data']),
                        'x_range': data['x_range'],
                        'y_range': data['y_range'],
                        'title': 'Vergelijking Oplosser'
                    })
                    return JsonResponse({'result': html})

                return render(request, 'oplosser/equation_detail.html', {
                    'equation_text': equation_text,
                    'equation_interpret': data['equation_interpret'],
                    'solutions': data['solution_text'],
                    'plot_data': json.dumps(data['plot_data']),
                    'x_range': data['x_range'],
                    'y_range': data['y_range'],
                    'title': 'Vergelijking Oplosser'
                    })
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('oplosser/equation_result.html', {
                    'equation_text': equation_text,
                    'equation_interpret': data['equation_interpret'],
                    'solutions': data['solution_text'],
                    'title': 'Vergelijking Oplosser'
                })
                return JsonResponse({'result': html})

            return render(request, 'oplosser/equation_detail.html', {
                'equation_text': equation_text,
                'equation_interpret': data['equation_interpret'],
                'solutions': data['solution_text'],
                'title': 'Vergelijking Oplosser'
            })

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
    
    if solver.vert_asympt is None:
        plot_data.append({'x': list(plottable_x1_coords), 'y': list(y1_coords), 'type': 'scatter', 'mode': 'lines', 'name': f'{f'f({solver.symbol})' if not solver.multivariate else 'y'} = {str(solver.eq1(solver.symbol)).replace('log', 'ln')}', 'line': {'color': 'darkturquoise'}})
        plot_data.append({'x': list(plottable_x2_coords), 'y': list(y2_coords), 'type': 'scatter', 'mode': 'lines', 'name': f'{f'g({solver.symbol})' if not solver.multivariate else 'y'} = {str(solver.eq2(solver.symbol)).replace('log', 'ln')}', 'line': {'color': 'springgreen'}})
    
    else:
        skip1 = 0
        skip2 = 0
        plot_data_f = []
        plot_data_g = []

        for i in range(len(plottable_x1_coords)):

            if list(plottable_x1_coords[i]) and list(y1_coords[i]):
                plot_data_f.append({'x': list(plottable_x1_coords[i]), 'y': list(y1_coords[i]), 'type': 'scatter', 'mode': 'lines', 'name': f'{f'f({solver.symbol})' if not solver.multivariate else 'y'} = {str(solver.eq1(solver.symbol)).replace('log', 'ln')}', 'showlegend': i == skip1, 'line': {'color': 'darkturquoise'}})
            
            else:
                skip1 +=1

            if list(plottable_x2_coords[i]) and list(y2_coords[i]):
                plot_data_g.append({'x': list(plottable_x2_coords[i]), 'y': list(y2_coords[i]), 'type': 'scatter', 'mode': 'lines', 'name': f'{f'g({solver.symbol})' if not solver.multivariate else 'y'} = {str(solver.eq2(solver.symbol)).replace('log', 'ln')}', 'showlegend': i == skip2, 'line': {'color': 'springgreen'}})

            else:
                skip2 += 1

        plot_data = plot_data_f + plot_data_g
        plot_data_f, plot_data_g = [], []
        
    if not solver.intersect:
        return plot_data, view_x_range, view_y_range

    plot_data.append({'x': solver.x_intersect, 'y': solver.y_intersect, 'type': 'scatter', 'mode': 'markers', 'name': f"Snijpunt", 'showlegend':False, 'marker': {'color': 'black', 'size': 10}})

    return plot_data, view_x_range, view_y_range