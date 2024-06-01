from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.http import url_has_allowed_host_and_scheme
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
    return render(request, "solverapp/solver.html")


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
    

def solve_equation_view(request):
    if request.method == 'POST':
        form = EquationForm(request.POST)
        if form.is_valid():
            equation_text = form.cleaned_data['equation_text']
            solver = Solve(input_string=equation_text)
            equation_interpret, outputs, plot = solver.solve_equation()
            
            solutions = "\n".join([str(output) for output in outputs])
            if plot:
                plot_data = generate_plot_data(solver)

            return render(request, 'solverapp/equation_detail.html', {
                'equation_text': equation_text,
                'equation_interpret': equation_interpret,
                'solutions': solutions,
                'plot_data': json.dumps(plot_data),
            })
    else:
        form = EquationForm()

    return render(request, 'solverapp/solve_equation.html', {'form': form})


def generate_plot_data(solver):
    x_range, y_range = solver.get_range()
    plottable_x1_coords, y1_coords, plottable_x2_coords, y2_coords = solver.get_plot_data(x_range)
    
    plot_data = [
        {'x': list(plottable_x1_coords), 'y': list(y1_coords), 'type': 'scatter', 'mode': 'lines', 'name': f'f(x) = {solver.eq1}'},
        {'x': list(plottable_x2_coords), 'y': list(y2_coords), 'type': 'scatter', 'mode': 'lines', 'name': f'g(x) = {solver.eq2}'},
    ]
    
    return plot_data