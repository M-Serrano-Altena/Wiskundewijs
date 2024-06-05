from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.http import url_has_allowed_host_and_scheme
from django.template.loader import render_to_string
import sympy as sp
from django.conf import settings
import os
import json
from src.Solver.src.solver.solve_calculations import Solve
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
            updated_text = f"{solution_text}<br>\[\\boxed{{{new_text}}}\]"

        elif not new_line:
            updated_text = f"{solution_text}\[\\boxed{{{new_text}}}\]"

        elif type(new_line) is int:
            amt_new_line = new_line * "<br>"
            updated_text = f"{solution_text}{amt_new_line}\[\\boxed{{{new_text}}}\]"
    
    else:
        if new_line and type(new_line) is not int:
            updated_text = f"{solution_text}<br>{new_text}"

        elif not new_line:
            updated_text = f"{solution_text}{new_text}"

        elif type(new_line) is int:
            amt_new_line = new_line * "<br>"
            updated_text = f"{solution_text}{amt_new_line}{new_text}"

    solution_text = updated_text
    return solution_text


def solve_equation_view(request):
    if request.method == 'POST':
        form = EquationForm(request.POST)
        if form.is_valid():
            equation_text = form.cleaned_data['equation_text']
            solver = Solve(input_string=equation_text)
            equation_interpret, outputs, plot = solver.solve_equation()
            plot_data = []
            
            solution_text = ""
            for output in outputs:
                if type(output) is tuple:
                    if '$' in output[0]:
                        output = list(output)
                        output[0] = output[0].replace('$', '\(', 1)
                        output[0] = output[0].replace('$', '\)', 1)
                        output = tuple(output)

                    solution_text = add_solution_text(solution_text=solution_text, new_text=output[0], options=output[1])
                
                else:
                    solution_text = add_solution_text(solution_text=solution_text, new_text=output)

            if plot:
                plot_data = generate_plot_data(solver)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('oplosser/equation_result.html', {
                    'equation_text': equation_text,
                    'equation_interpret': equation_interpret,
                    'solutions': solution_text,
                    'plot_data': json.dumps(plot_data),
                    'title': 'Vergelijking Oplosser'
                })
                return JsonResponse({'result': html})

            return render(request, 'oplosser/equation_detail.html', {
                'equation_text': equation_text,
                'equation_interpret': equation_interpret,
                'solutions': solution_text,
                'plot_data': json.dumps(plot_data),
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
    x_range, y_range = solver.get_range()
    plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = solver.get_plot_data(x_range)
    
    plot_data = []
    
    if solver.vert_asympt is None:
        plot_data.append({'x': list(plottable_x1_coords), 'y': list(y1_coords), 'type': 'scatter', 'mode': 'lines', 'name': f'f(x) = {solver.eq1(solver.symbol)}'})
        plot_data.append({'x': list(plottable_x2_coords), 'y': list(y2_coords), 'type': 'scatter', 'mode': 'lines', 'name': f'g(x) = {solver.eq2(solver.symbol)}'})
    else:
        for i in range(len(plottable_x1_coords)):
            plot_data.append({'x': list(plottable_x1_coords[i]), 'y': list(y1_coords[i]), 'type': 'scatter', 'mode': 'lines', 'name': f'f(x) = {str(solver.eq1(solver.symbol)).replace('log', 'ln')}'})
            plot_data.append({'x': list(plottable_x2_coords[i]), 'y': list(y2_coords[i]), 'type': 'scatter', 'mode': 'lines', 'name': f'g(x) = {solver.eq2(solver.symbol)}' if i == 0 else '', 'showlegend': i == 0})
    

    if not solver.solutions.is_FiniteSet:
        solver.x_intersect = [sol for sol in sp.solveset(solver.eq, domain=sp.Interval(0, 2*sp.pi))]
        solver.y_intersect = [solver.eq1(sol) for sol in solver.x_intersect]
        
    else:
        solver.x_intersect = [float(sol) for sol in solver.solutions]
        solver.y_intersect = [float(solver.eq1(sol)) for sol in solver.solutions]

    counter = 0
    for x, y in zip(solver.x_intersect, solver.y_intersect):
        counter += 1 
        plot_data.append({'x': [float(x)], 'y': [float(y)], 'type': 'scatter', 'mode': 'markers', 'name': f"Snijpunt {counter} = ({no_frac(sp.nsimplify(round(x,13), [sp.pi]))}, {no_frac(sp.nsimplify(round(y,13), [sp.pi]))})", 'marker': {'color': 'black', 'size': 10}})

    return plot_data