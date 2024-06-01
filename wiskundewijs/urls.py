"""
URL configuration for wiskundewijs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from solverapp import views as solver_views
from src.Solver.src.solver.solve_application import solve_application

urlpatterns = [
    path("admin/", admin.site.urls),
    path("solverapp/", solver_views.solve_equation_view, name="solverapp"),
    path('solverapp/search/search_index.json', solver_views.serve_search_index),
    re_path(r'^solverapp/(?P<path>.*)/$', solver_views.redirect_view),
    path("", include("docs.urls")),
]
