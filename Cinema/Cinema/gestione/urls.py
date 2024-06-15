from django.urls import path
from .views import *

app_name = "gestione"

urlpatterns = [
    path("", gestione_home, name="home"),
    path("listafilm/", FilmListView.as_view(),name="listafilm"),
    path("ricerca/", search, name="cercafilm"),
]