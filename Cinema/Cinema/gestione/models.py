from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Q
from collections import defaultdict

# Create your models here.

class Utente(AbstractUser):
    #metodo che ritorna tutte le prenotazioni associate all'utente
    def get_prenotazioni(self):
        return Prenotazione.objects.filter(utente=self)

    def get_film_consigliati(self):
        prenotazioni = list(self.prenotazioni.all())
        prenotazioni.reverse()  # Inverti l'ordine delle prenotazioni
        film_consigliati = []

        film_acquistati_ids = [prenotazione.proiezione.film.id for prenotazione in prenotazioni]

        caratteristiche_films = defaultdict(list)
        for prenotazione in prenotazioni:
            film = prenotazione.proiezione.film
            caratteristiche_films[film.genere].append(film)
            if film.in_3D:
                caratteristiche_films['3D'].append(film)
            if film.in_inglese:
                caratteristiche_films['inglese'].append(film)

        def get_similar_films(query, exclude_ids, limit):
            return Film.objects.filter(query).exclude(id__in=exclude_ids).distinct()[:limit]

        num_films_to_recommend = 10  # Numero totale di film da consigliare
        max_weight = 5  # Numero massimo di film da consigliare per il film più recente

        # Calcola la riduzione di film consigliati per ogni prenotazione più vecchia
        total_prenotazioni = len(prenotazioni)
        if total_prenotazioni > 1:
            step = (max_weight - 1) / (total_prenotazioni - 1)
        else:
            step = 0

        for idx, prenotazione in enumerate(prenotazioni):
            film = prenotazione.proiezione.film
            query = Q(genere=film.genere)
            if film.in_3D:
                query |= Q(in_3D=True)
            if film.in_inglese:
                query |= Q(in_inglese=True)

            # Decrementa gradualmente il numero di film consigliati per prenotazioni meno recenti
            limit = max(max_weight - int(idx * step), 1)
            similar_films = get_similar_films(query, film_acquistati_ids, limit)
            film_consigliati.extend(similar_films)#Aggiungi in coda alla lista
            film_acquistati_ids.extend([f.id for f in similar_films])

        # Limita il numero totale di film consigliati
        return film_consigliati[:num_films_to_recommend]


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
