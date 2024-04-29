from django.urls import path
from . import views 

urlpatterns = [
    path('<path:path>', views.serve_docs),
    path('', views.serve_home),
]