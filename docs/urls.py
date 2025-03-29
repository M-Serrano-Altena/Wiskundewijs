from django.urls import path
from . import views 

urlpatterns = [
    path('load-external-html/<path:path>', views.load_external_html, name='load-external-html'),
    path('<path:path>', views.serve_docs),
    path('', views.serve_home),
]