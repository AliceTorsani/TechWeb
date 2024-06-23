from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from datetime import date, time
import re
from .models import *

class CreateFilmForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addfilm_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Film"))

    class Meta:
        model = Film
        fields = ["titolo","genere","descrizione", "prezzo", "immagine", "in_3D", "in_inglese"]

class CreateProiezioneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addproiezione_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Proiezione"))

    class Meta:
        model = Proiezione
        fields = ["data", "ora_inizio", "film", "sala", "posti_disponibili"]

    def clean_data(self):
        data = self.cleaned_data.get("data")
        if data < date.today():
            raise ValidationError("La data della proiezione deve essere futura.")
        return data
    
    def clean_posti_disponibili(self):
        posti_disponibili = self.cleaned_data.get("posti_disponibili")
        if posti_disponibili > 100:  # Suppongo che il massimo dei posti sia 100
            raise ValidationError("Il numero di posti disponibili non può superare 100.")
        elif posti_disponibili == 0:
            raise ValidationError("Inserire almeno un posto disponibile")
        elif posti_disponibili < 0:
            raise ValidationError("Formato non valido. Inserire un numero positivo di posti")
        return posti_disponibili

    def clean_ora_inizio(self):
        ora_inizio = self.cleaned_data.get("ora_inizio")
        start_time = time(14, 0)  # 14:00
        end_time = time(22, 0)    # 22:00
        if ora_inizio < start_time or ora_inizio > end_time:
            raise ValidationError("L'ora di inizio deve essere compresa tra le 14:00 e le 22:00")
        return ora_inizio

    def clean_sala(self):
        sala = self.cleaned_data.get("sala")
        pattern = r"^Sala ([1-8])$"
        match = re.match(pattern, sala)
        if not match:
            raise ValidationError("La sala deve essere compresa tra Sala 1 e Sala 8 nel formato 'Sala X'.")
        return sala
    



