from django.contrib import admin
from .models import Utente, Film, Proiezione, Prenotazione

# Register your models here.

admin.site.register(Utente)
admin.site.register(Film)
admin.site.register(Proiezione)
admin.site.register(Prenotazione)
