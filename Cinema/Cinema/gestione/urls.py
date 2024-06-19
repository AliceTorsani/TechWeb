from django.urls import path
from .views import *

app_name = "gestione"

urlpatterns = [
    path("", gestione_home, name="home"),
    path("listafilm/", FilmListView.as_view(),name="listafilm"),
    path('listafilm/<int:pk>/', FilmDetailView.as_view(), name='dettagli_film'),
    path('listafilm/<int:pk>/proiezioni/', FilmProjectionsView.as_view(), name='proiezioni_film'),
    path('film/<int:pk>/proiezioni_per_data/', FilmProjectionsByDateView.as_view(), name='lista_proiezioni_per_data'),
    path('film/<int:pk>/proiezioni/', FilmProjectionsDatesView.as_view(), name='film_proiezioni_date'),
    path('film/<int:film_id>/proiezioni_per_data/<str:data>/', FilmProiezioniPerDataView.as_view(), name='film_proiezioni_per_data'),
    path("ricerca/", search, name="cercafilm"),
    path('my_situation/', my_situation, name='my_situation'),
]