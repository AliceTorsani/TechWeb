from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Utente(AbstractUser):
    #metodo che ritorna tutte le prenotazioni associate all'utente
    def get_prenotazioni(self):
        return Prenotazione.objects.filter(utente=self)

    class Meta:
        verbose_name_plural = "Utenti"

class Film(models.Model):
    titolo = models.CharField(max_length=200)
    genere = models.CharField(max_length=200)
    descrizione = models.CharField(max_length=500)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    immagine = models.ImageField(upload_to='film_immagini/')
    in_3D = models.BooleanField(default=False)
    in_inglese = models.BooleanField(default=False)
    
    def get_proiezioni(self):
        return list(self.proiezioni.all())

    def __str__(self):
        return self.titolo
    
    class Meta:
        verbose_name_plural = "Film"

class Proiezione(models.Model):
    data = models.DateField()
    ora_inizio = models.TimeField()
    film = models.ForeignKey(Film, related_name='proiezioni', on_delete=models.CASCADE)
    sala = models.CharField(max_length=50)
    posti_disponibili = models.IntegerField(default=20)

    #metodo che ritorna tutte le prenotazioni associate a una proiezione
    def get_prenotazioni(self):
        return Prenotazione.objects.filter(proiezione=self)

    def get_film(self):
        return self.film

    def __str__(self):
        return f"{self.film.titolo} - {self.data} {self.ora_inizio}"

    class Meta:
        verbose_name_plural = "Proiezioni"

class Prenotazione(models.Model):
    utente = models.ForeignKey('gestione.Utente', related_name='prenotazioni', on_delete=models.CASCADE)
    proiezione = models.ForeignKey(Proiezione, related_name='prenotazioni', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.utente.username} - {self.proiezione}"

    class Meta:
        verbose_name_plural = "Prenotazioni"
