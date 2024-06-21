from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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



     
