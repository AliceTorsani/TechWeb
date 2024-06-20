from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

class CreaUtenteCliente(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit) #ottengo un riferimento all'utente
        g = Group.objects.get(name="Clienti") #cerco il gruppo che mi interessa
        g.user_set.add(user) #aggiungo l'utente al gruppo
        return user #restituisco quello che il metodo padre di questo metodo avrebbe restituito.

class CreaUtenteGestore(UserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit) 
        g = Group.objects.get(name="Gestori") 
        g.user_set.add(user) 
        return user 


