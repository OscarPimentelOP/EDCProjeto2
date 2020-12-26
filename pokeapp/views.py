from django.shortcuts import render

# Create your views here.


def index(request):

    return render(request, 'index.html')

def pokemon(request):

    return render(request, 'pokemon.html')