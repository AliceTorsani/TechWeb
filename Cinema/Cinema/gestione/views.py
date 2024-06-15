from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.

def gestione_home(request):
    return render(request,template_name="gestione/home.html")

class FilmListView(ListView):
    pass

def search(request):
    pass
