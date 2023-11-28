from django.urls import path

from .views import *


urlpatterns = [
    # http://127.0.0.1:8000/py-terminals/pyterm-list/
    path('pyterms-list/', get_pyterminals_list, name='get pyterminals list'),

    # http://127.0.0.1:8000/py-terminals/add-pyterm/
    path('add-pyterm/', add_pyterminal, name='add pyterminal'),

    # http://127.0.0.1:8000/py-terminals/show-pyterm/1/
    path('show-pyterm/<str:identifier>/', show_pyterminal, name='show pyterminal'),

    # http://127.0.0.1:8000/py-terminals/edit-pyterm/1/
    path('edit-pyterm/<str:identifier>/', edit_pyterminal, name='edit pyterminal'),

    # http://127.0.0.1:8000/py-terminals/delete-pyterm/1/
    path('delete-pyterm/<str:identifier>/', delete_pyterminal, name='delete pyterminal'),
]
