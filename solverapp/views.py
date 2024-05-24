from django.shortcuts import render
from django.http import HttpResponse
import sympy as sp


# Create your views here.
def test(request):
    x = sp.symbols('x', real=True)
    solution = sp.solve(x**2 - 4, x)
    # return HttpResponse(str(solution))
    return render(request, "solverapp/solver.html")