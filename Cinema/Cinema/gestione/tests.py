from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .forms import CreateProiezioneForm 

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
        #self.assertEqual(form.clean_data(), date.today())

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
        #self.assertEqual(form.clean_data(), date.today() + timedelta(days=1))
        
