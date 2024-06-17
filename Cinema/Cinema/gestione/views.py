from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *

# Create your views here.

def gestione_home(request):
    return render(request,template_name="gestione/home.html")

class FilmListView(ListView):
    titolo = "Il nostro cinema offre attualmente i seguenti film: "
    model = Film
    template_name = "gestione/lista_film.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Recupera i parametri di filtro dalla richiesta GET
        filter_category = self.request.GET.get('filter_category', None)
        filter_value = self.request.GET.get('filter_value', None)

        if filter_category and filter_value:
            if filter_category == 'genere':
                queryset = queryset.filter(genere__icontains=filter_value)
            elif filter_category == 'extra':
                if filter_value == 'in_3D':
                    queryset = queryset.filter(in_3D=True)
                elif filter_value == 'in_inglese':
                    queryset = queryset.filter(in_inglese=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_category'] = self.request.GET.get('filter_category', '')
        context['filter_value'] = self.request.GET.get('filter_value', '')
        return context


def search(request):
    pass

class FilmDetailView(DetailView):
    model = Film
    template_name = 'gestione/dettagli_film.html'

class FilmProjectionsView(DetailView):
    model = Film
    template_name = 'gestione/proiezioni_film.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggiungi qui le logiche per ottenere le proiezioni del film
        return context