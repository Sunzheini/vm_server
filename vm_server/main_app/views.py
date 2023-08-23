from django.shortcuts import render


"""
can upload .py scripts which will be executed on the server
"""


def index(request):
    return render(request, 'core/index.html')


def test(request):
    return render(request, 'main_app/test.html')
