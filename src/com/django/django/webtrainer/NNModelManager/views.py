from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def model_config(request):
    return render(request, 'model_config.html')
