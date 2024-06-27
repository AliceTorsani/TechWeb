from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import *
from .forms import *
from django.utils import timezone
from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy

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
        context['generi'] = list(Film.objects.values_list('genere', flat=True).distinct())
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
            # Filtra le proiezioni con data presente o futura
            proiezioni_dates = Proiezione.objects.filter(film=film, data__gte=date.today()).values('data').distinct()
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
        today = date.today() 
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
            if date < date.today():
                # Se la data è nel passato non mostro nessuna proiezione
                proiezioni = Proiezione.objects.none()
            else:
                # Se la data è nel futuro o è oggi
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


class FilmProiezioniPerDataView(ListView):
    model = Proiezione
    template_name = 'gestione/proiezioni_per_data.html'
    context_object_name = 'proiezioni'

    def get_queryset(self):
        film_id = self.kwargs['film_id']
        data = self.kwargs['data']
        # Verifica che la data sia presente o futura
        if data < str(date.today()):
            return Proiezione.objects.none()  # Nessuna proiezione se la data è nel passato
        return Proiezione.objects.filter(film_id=film_id, data=data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = get_object_or_404(Film, pk=self.kwargs['film_id'])
        context['film'] = film
        context['data'] = self.kwargs['data']
        return context
        
@login_required
def my_situation(request):
    utente = get_object_or_404(Utente, pk=request.user.pk)
    prenotazioni = utente.get_prenotazioni()
    context = {
        'prenotazioni': prenotazioni
    }
    return render(request, 'gestione/my_situation.html', context)


def build_redirect_url(view_name, kwargs, filter_date):
    url = reverse(view_name, kwargs=kwargs)
    if filter_date:
        url += f"?filter_date={filter_date}"
    return url


@login_required
def prenota_proiezione(request, proiezione_id):
    proiezione = get_object_or_404(Proiezione, pk=proiezione_id)
    utente = request.user

    # Recuperiamo i parametri GET
    next_url = request.GET.get('next')
    filter_date = request.GET.get('filter_date')
    
    # Costruisci l'URL di reindirizzamento
    if next_url:
        if 'film_proiezioni_per_data' in next_url:
            film_id = proiezione.film.pk
            data = filter_date if filter_date else proiezione.data
            next_url = build_redirect_url('gestione:film_proiezioni_per_data', {'film_id': film_id, 'data': data}, filter_date)
            #next_url = f"{reverse('gestione:film_proiezioni_per_data', kwargs={'film_id': film_id, 'data': data})}?filter_date={data}"
        elif 'lista_proiezioni_per_data' in next_url:
            film_id = proiezione.film.pk
            next_url = f"{reverse('gestione:lista_proiezioni_per_data', kwargs={'pk': film_id})}?filter_date={filter_date}"
        elif 'proiezioni_film' in next_url:
            film_id = proiezione.film.pk
            next_url = reverse('gestione:proiezioni_film', kwargs={'pk': film_id})
    else:
        next_url = reverse('gestione:home')  # Default redirection to home if next is not provided

    # Controllo se ci sono posti disponibili
    if proiezione.posti_disponibili <= 0:
        messages.error(request, 'Non ci sono posti disponibili per questa proiezione.')
        return redirect(next_url)

    # Controllo se l'utente ha già una prenotazione per la stessa data e ora in una sala differente
    esiste_prenotazione = Prenotazione.objects.filter(
        utente=utente,
        proiezione__data=proiezione.data,
        proiezione__ora_inizio=proiezione.ora_inizio,
    ).exclude(proiezione__sala=proiezione.sala).exists()
    
    if esiste_prenotazione:
        messages.error(request, 'Prenotazione fallita. Hai già una prenotazione alla stessa ora per un\'altra proiezione in una sala differente.')
        return redirect(next_url)

    # Creazione della prenotazione
    Prenotazione.objects.create(utente=utente, proiezione=proiezione)
    proiezione.posti_disponibili -= 1
    proiezione.save()

    messages.success(request, 'Prenotazione effettuata con successo!')
    return redirect(next_url)

@login_required
def film_consigliati_view(request):
    utente = request.user
    film_consigliati = utente.get_film_consigliati()
    return render(request, 'gestione/film_consigliati.html', {'film_consigliati': film_consigliati})

#Views per soli Gestori
class CreateFilmView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    group_required = ["Gestori"]
    title = "Aggiungi un film al cinema"
    form_class = CreateFilmForm
    template_name = "gestione/create_entry.html"
    success_url = reverse_lazy("gestione:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Il film è stato aggiunto con successo!")
        return response
    
    def test_func(self):
        return self.request.user.groups.filter(name='Gestori').exists()

class CreateProiezioneView(CreateFilmView):
    title = "Aggiungi una Proiezione ad un film"
    form_class = CreateProiezioneForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "La proiezione è stata aggiunta con successo!")
        return response




