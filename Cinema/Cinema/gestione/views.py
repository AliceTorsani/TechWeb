from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

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
        filter_date = self.request.GET.get('filter_date', None)

        #if filter_category:
        if filter_category == 'genere' and filter_value:
            queryset = queryset.filter(genere=filter_value)
        elif filter_category == 'extra' and filter_value:
            if filter_value == 'in_3D':
                queryset = queryset.filter(in_3D=True)
            elif filter_value == 'in_inglese':
                queryset = queryset.filter(in_inglese=True)
        elif filter_category == 'data' and filter_date:
            try:
                # Filtraggio dei film con proiezioni per la data selezionata
                date = datetime.strptime(filter_date, "%Y-%m-%d")
                # Filtriamo i film in base alle proiezioni con data uguale alla data selezionata
                # Otteniamo tutti gli ID dei film con proiezioni nella data selezionata
                film_ids_with_projections = Proiezione.objects.filter(data=date).values_list('film_id', flat=True)
                # Filtriamo i film per includere solo quelli con proiezioni nella data selezionata
                queryset = queryset.filter(id__in=film_ids_with_projections)
            except ValueError:
                #queryset = queryset.none()
                print("Problemi nel filtraggio per data")
        return queryset        
        '''
        if filter_category and filter_value:
            if filter_category == 'genere':
                queryset = queryset.filter(genere__icontains=filter_value)
            elif filter_category == 'extra':
                if filter_value == 'in_3D':
                    queryset = queryset.filter(in_3D=True)
                elif filter_value == 'in_inglese':
                    queryset = queryset.filter(in_inglese=True)

        return queryset
        '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_category'] = self.request.GET.get('filter_category', '')
        context['filter_value'] = self.request.GET.get('filter_value', '')
        context['filter_date'] = self.request.GET.get('filter_date', '')
        return context


def search(request):
    query = request.GET.get('search_title')
    context = {'search_title': query}
    
    if query:
        films = Film.objects.filter(titolo__icontains=query)
        if films.exists():
            film = films.first()
            proiezioni_dates = Proiezione.objects.filter(film=film).values('data').distinct()
            context.update({
                'film': film,
                'proiezioni_dates': proiezioni_dates,
            })
        else:
            context['film_not_found'] = True
    
    return render(request, 'gestione/cerca_film.html', context)

class FilmDetailView(DetailView):
    model = Film
    template_name = 'gestione/dettagli_film.html'

class FilmProjectionsView(ListView):
    model = Proiezione
    template_name = 'gestione/proiezioni_film.html'
    context_object_name = 'proiezioni'

    def get_queryset(self):
        film_id = self.kwargs['pk']
        today = timezone.now()
        return Proiezione.objects.filter(film_id=film_id, data__gte=today)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['film'] = Film.objects.get(pk=self.kwargs['pk'])
        return context

class FilmProjectionsByDateView(TemplateView):
    template_name = "gestione/lista_proiezioni_per_data.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = get_object_or_404(Film, pk=self.kwargs['pk'])
        filter_date = self.request.GET.get('filter_date')

        try:
            date = datetime.strptime(filter_date, "%Y-%m-%d")
            # Ottieni le proiezioni per il film e la data specificata
            proiezioni = Proiezione.objects.filter(film=film, data=date)
        except (ValueError, TypeError):
            proiezioni = Proiezione.objects.none()

        context['film'] = film
        context['filter_date'] = filter_date
        context['proiezioni'] = proiezioni
        return context

    '''
    def get_queryset(self):
        film_id = self.kwargs['pk']
        filter_date = self.request.GET.get('filter_date')
        
        if filter_date:
            filter_date_dt = datetime.strptime(filter_date, '%Y-%m-%d')
            return Proiezione.objects.filter(film_id=film_id, data__date=filter_date_dt)
        else:
            return Proiezione.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['film'] = Film.objects.get(pk=self.kwargs['pk'])
        context['filter_date'] = self.request.GET.get('filter_date', '')
        return context
    '''
class FilmProjectionsDatesView(DetailView):
    model = Film
    template_name = 'gestione/proiezioni_date.html'
    context_object_name = 'film'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = self.get_object()
        proiezioni_dates = Proiezione.objects.filter(film=film).values('data').distinct()
        context['proiezioni_dates'] = proiezioni_dates
        return context

class FilmProiezioniPerDataView(ListView):
    template_name = 'gestione/proiezioni_per_data.html'
    context_object_name = 'proiezioni'

    def get_queryset(self):
        film_id = self.kwargs['film_id']
        data = self.kwargs['data']
        return Proiezione.objects.filter(film_id=film_id, data=data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = get_object_or_404(Film, pk=self.kwargs['film_id'])
        context['film'] = film
        context['data'] = self.kwargs['data']
        return context
        