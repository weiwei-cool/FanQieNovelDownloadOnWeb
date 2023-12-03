from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def history(request):
    return render(request, 'history/index.html')

def eula(request):
    return render(request, 'eula/index.html')
