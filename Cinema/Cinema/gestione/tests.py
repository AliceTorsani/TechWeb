from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta, time
from .forms import CreateProiezioneForm 
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from .models import Film, Proiezione, Utente, Prenotazione

# Create your tests here.

class CreateProiezioneFormTest(TestCase):

    def setUp(self):
        # Creo i dati di esempio per i campi obbligatori
        self.data_obbligatori = {
            'ora_inizio': '14:00',
            'film': 'Blade Runner',
            'sala': 'Sala 3',
            'posti_disponibili': 20
        }

    def test_clean_data_past_date(self):
        form_data = self.data_obbligatori.copy()
        form_data['data'] = date.today() - timedelta(days=1)
        form = CreateProiezioneForm(data=form_data)
        form.cleaned_data = form_data  # Imposta cleaned_data per simulare la validazione
        with self.assertRaises(ValidationError) as context:
            form.clean_data()
        self.assertEqual(context.exception.message, "La data della proiezione deve essere futura.")

    def test_clean_data_today_date(self):
        form_data = self.data_obbligatori.copy()
        form_data['data'] = date.today()
        form = CreateProiezioneForm(data=form_data)
        form.cleaned_data = form_data  # Imposta cleaned_data per simulare la validazione
        try:
            cleaned_data = form.clean_data()
            self.assertEqual(cleaned_data, date.today())
        except ValidationError:
            self.fail("clean_data() raised ValidationError unexpectedly!")

    def test_clean_data_future_date(self):
        form_data = self.data_obbligatori.copy()
        form_data['data'] = date.today() + timedelta(days=1)
        form = CreateProiezioneForm(data=form_data)
        form.cleaned_data = form_data  # Imposta cleaned_data per simulare la validazione
        try:
            cleaned_data = form.clean_data()
            self.assertEqual(cleaned_data, date.today() + timedelta(days=1))
        except ValidationError:
            self.fail("clean_data() raised ValidationError unexpectedly!")

    def test_clean_overlapping_proiezione(self):
        # Crea un film di esempio
        film = Film.objects.create(
            titolo="Blade Runner",
            prezzo=10.0 
        )
        data = date.today()
        ora_inizio = time(14, 0)
        sala = "Sala 3"

        # Crea una proiezione che si sovrappone
        Proiezione.objects.create(
            film=film,
            data=data,
            ora_inizio=ora_inizio,
            sala=sala
        )

        form_data = self.data_obbligatori.copy()
        form_data['data'] = data
        form = CreateProiezioneForm(data=form_data)
        form.cleaned_data = form_data  # Imposta cleaned_data per simulare la validazione

        with self.assertRaises(ValidationError) as context:
            form.clean()

        self.assertEqual(
            str(context.exception),
            "['Esiste già una proiezione nella sala selezionata alla data e ora specificate.']"
        )

    def test_clean_non_overlapping_proiezione(self):
        # Crea un film di esempio
        film = Film.objects.create(
            titolo="Blade Runner",
            prezzo=10.0 
        )
        data = date.today() + timedelta(days=1)  # data diversa
        ora_inizio = time(14, 0)
        sala = "Sala 3"

        # Crea una proiezione non sovrapposta
        Proiezione.objects.create(
            film=film,
            data=date.today(),  # data diversa
            ora_inizio=ora_inizio,
            sala=sala
        )

        form_data = self.data_obbligatori.copy()
        form_data['data'] = data
        form = CreateProiezioneForm(data=form_data)
        form.cleaned_data = form_data  # Imposta cleaned_data per simulare la validazione

        try:
            cleaned_data = form.clean()
            self.assertEqual(cleaned_data['data'], data)
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")
        
class FilmProjectionsViewTest(TestCase):

    def setUp(self):
        # Creo un film di esempio
        self.film = Film.objects.create(
            titolo="Film di Test",
            prezzo=10.0 
        )
        # Data di oggi
        self.today = date.today()
        # Ora di inizio fittizia
        self.ora_inizio = time(14, 0)  # 14:00
        # Proiezione passata
        self.proiezione_passata = Proiezione.objects.create(
            film=self.film, data=self.today - timedelta(days=1), ora_inizio=self.ora_inizio
        )
        # Proiezione futura
        self.proiezione_futura = Proiezione.objects.create(
            film=self.film, data=self.today + timedelta(days=1), ora_inizio=self.ora_inizio
        )
        # Proiezione presente
        self.proiezione_presente = Proiezione.objects.create(
            film=self.film, data=self.today, ora_inizio=self.ora_inizio
        )

    def test_no_proiezioni(self):
        # Rimuovo tutte le proiezioni
        Proiezione.objects.all().delete()
        response = self.client.get(reverse('gestione:proiezioni_film', kwargs={'pk': self.film.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nessuna proiezione trovata.")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_only_past_proiezioni(self):
        # Rimuovo tutte le proiezioni future e presenti
        Proiezione.objects.filter(data__gte=self.today).delete()
        response = self.client.get(reverse('gestione:proiezioni_film', kwargs={'pk': self.film.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nessuna proiezione trovata.")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_only_future_proiezioni(self):
        # Rimuovo tutte le proiezioni passate e presenti
        Proiezione.objects.filter(data__lte=self.today).delete()
        response = self.client.get(reverse('gestione:proiezioni_film', kwargs={'pk': self.film.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.proiezione_futura.film.titolo)
        self.assertNotContains(response, "Nessuna proiezione trovata.")
        self.assertIn(self.proiezione_futura, response.context['object_list'])
        

    def test_only_present_proiezioni(self):
        # Rimuovo tutte le proiezioni passate e future
        Proiezione.objects.exclude(data=self.today).delete()
        response = self.client.get(reverse('gestione:proiezioni_film', kwargs={'pk': self.film.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.proiezione_presente.film.titolo)
        self.assertNotContains(response, "Nessuna proiezione trovata.")
        self.assertIn(self.proiezione_presente, response.context['object_list'])

    def test_mixed_proiezioni(self):
        # Controllo che vengano mostrate solo le proiezioni future e presenti
        response = self.client.get(reverse('gestione:proiezioni_film', kwargs={'pk': self.film.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.proiezione_futura.film.titolo)
        self.assertContains(response, self.proiezione_presente.film.titolo)
        self.assertIn(self.proiezione_presente, response.context['object_list'])
        self.assertIn(self.proiezione_futura, response.context['object_list'])
        self.assertNotIn(self.proiezione_passata, response.context['object_list'])


class PrenotaProiezioneViewTest(TestCase):

    def setUp(self):
        # Crea un utente di test
        self.user = Utente.objects.create_user(username='testuser', password='12345')
        
        # Crea un film di esempio
        self.film = Film.objects.create(titolo="Blade Runner", prezzo=10.0)
        
        # Crea una proiezione di esempio
        self.data = date.today() + timedelta(days=1)
        self.ora_inizio = time(14, 0)
        self.sala = "Sala 1"
        self.proiezione = Proiezione.objects.create(
            film=self.film, data=self.data, ora_inizio=self.ora_inizio, sala=self.sala, posti_disponibili=10
        )

    def test_accesso_non_autorizzato(self):
        #Eseguo una richiesta GET alla view di prenotazione di una proiezione
        response = self.client.get(reverse('gestione:prenota_proiezione', args=[self.proiezione.pk]))
        #Verifico che la risposta sia un reindirizzamento alla pagina di login con il parametro next corretto
        self.assertRedirects(response, f'/login/?auth=notok&next=/gestione/prenota_proiezione/{self.proiezione.pk}/')

    def test_proiezione_inesistente(self):
        #Login con l'utente di test
        self.client.login(username='testuser', password='12345')
        #Richiesta GET alla view di prenotazione di una proiezione con un ID inesistente 
        response = self.client.get(reverse('gestione:prenota_proiezione', args=[999999])) # ID inesistente
        self.assertEqual(response.status_code, 404)

    def test_nessun_posto_disponibile(self):
        self.proiezione.posti_disponibili = 0
        self.proiezione.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('gestione:prenota_proiezione', args=[self.proiezione.pk]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Non ci sono posti disponibili per questa proiezione.')
        #Controllo che l'utente venga reindirizzato alla homepage
        self.assertRedirects(response, reverse('gestione:home'))

    def test_prenotazione_riuscita(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('gestione:prenota_proiezione', args=[self.proiezione.pk]))
        #Verifico che l'utente venga reindirizzato correttamente alla homepage dopo aver completato la prenotazione 
        self.assertRedirects(response, reverse('gestione:home'))
        #Aggiorno la proiezione dal database per ottenere i dati aggiornati
        self.proiezione.refresh_from_db()
        self.assertEqual(self.proiezione.posti_disponibili, 9)
        #Verifico che sia stata creata correttamente una prenotazione nel database 
        self.assertTrue(Prenotazione.objects.filter(utente=self.user, proiezione=self.proiezione).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Prenotazione effettuata con successo!')

    def test_prenotazione_con_next_lista_proiezioni(self):
        self.client.login(username='testuser', password='12345')
        #Costruisco l'URL di reindirizzamento per la lista delle proiezioni di un film
        next_url = reverse('gestione:lista_proiezioni_per_data', args=[self.film.pk])
        #Eseguo una richiesta GET alla view di prenotazione di una proiezione includendo next nell'URL
        response = self.client.get(f'{reverse("gestione:prenota_proiezione", args=[self.proiezione.pk])}?next={next_url}&filter_date={self.data}')
        #Verifico che l'utente venga reindirizzato correttamente alla lista delle proiezioni di un film 
        self.assertRedirects(response, next_url)
        self.assertTrue(Prenotazione.objects.filter(utente=self.user, proiezione=self.proiezione).exists())

    def test_prenotazione_con_next_proiezioni_film(self):
        self.client.login(username='testuser', password='12345')
        #Costruisco l'URL di reindirizzamento per le proiezioni di un film
        next_url = reverse('gestione:proiezioni_film', args=[self.film.pk])
        #Eseguo una richiesta GET alla view di prenotazione di una proiezione, includendo next nell'URL
        response = self.client.get(f'{reverse("gestione:prenota_proiezione", args=[self.proiezione.pk])}?next={next_url}')
        #Verifico che l'utente venga reindirizzato correttamente alle proiezioni di un film 
        self.assertRedirects(response, next_url)
        self.assertTrue(Prenotazione.objects.filter(utente=self.user, proiezione=self.proiezione).exists())

    def test_prenotazione_multiple_per_utente(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('gestione:prenota_proiezione', args=[self.proiezione.pk]))
        #Verifico che l'utente venga reindirizzato correttamente alla homepage dopo aver completato la prima prenotazione
        self.assertRedirects(response, reverse('gestione:home'))
        response = self.client.get(reverse('gestione:prenota_proiezione', args=[self.proiezione.pk]))
        #Verifico che l'utente venga reindirizzato correttamente alla homepage dopo aver completato la seconda prenotazione
        self.assertRedirects(response, reverse('gestione:home'))
        self.assertEqual(Prenotazione.objects.filter(utente=self.user, proiezione=self.proiezione).count(), 2)

    def test_prenotazione_in_sala_differente_stessa_ora(self):
        self.client.login(username='testuser', password='12345')
        # Crea una prenotazione per una proiezione in una sala differente alla stessa ora
        proiezione2 = Proiezione.objects.create(
            film=self.film,
            data=self.proiezione.data,
            ora_inizio=self.proiezione.ora_inizio,
            sala="Sala 2",
            posti_disponibili=10
        )
        # Creazione di una prenotazione per la seconda proiezione
        Prenotazione.objects.create(
            utente=self.user,
            proiezione=proiezione2
        )
        # Tenta di prenotare la prima proiezione
        response = self.client.get(reverse('gestione:prenota_proiezione', args=[self.proiezione.pk]))
        # Verifica che l'utente riceva un messaggio di errore
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Prenotazione fallita. Hai già una prenotazione alla stessa ora per un'altra proiezione in una sala differente.")
        self.assertRedirects(response, reverse('gestione:home'))
        self.assertEqual(Prenotazione.objects.filter(utente=self.user).count(), 1)
        # Verifica che la prenotazione non sia stata creata
        self.assertFalse(Prenotazione.objects.filter(utente=self.user, proiezione=self.proiezione).exists())

    def test_prenotazione_con_film_proiezioni_per_data_con_filter_date(self):
        self.client.login(username='testuser', password='12345')
        #Costruisco l'URL di reindirizzamento per le proiezioni di un film in una data specifica
        next_url = reverse('gestione:film_proiezioni_per_data', kwargs={'film_id': self.film.pk, 'data': self.data})
        #Eseguo una richiesta GET alla view di prenotazione di una proiezione includendo next e filter_date nell'URL
        response = self.client.get(f'{reverse("gestione:prenota_proiezione", args=[self.proiezione.pk])}?next={next_url}&filter_date={self.data}')
        #Verifico che l'utente venga reindirizzato correttamente alla pagina delle proiezioni di un film in una data specifica 
        self.assertRedirects(response, next_url)
        #Verifico che sia stata creata correttamente una prenotazione nel database 
        self.assertTrue(Prenotazione.objects.filter(utente=self.user, proiezione=self.proiezione).exists())

    def test_prenotazione_senza_next_url(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('gestione:prenota_proiezione', args=[self.proiezione.pk]))
        #Verifico che l'utente venga reindirizzato correttamente alla homepage dopo aver completato con successo la prenotazione
        self.assertRedirects(response, reverse('gestione:home'))
        self.assertTrue(Prenotazione.objects.filter(utente=self.user, proiezione=self.proiezione).exists())
