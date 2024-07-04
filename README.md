Progetto di Tecnologie Web di Alice Torsani, matricola 164915

Gestione sistema di prenotazioni di un cinema

Il sistema permette di utilizzare un servizio di prenotazioni e visualizzazione di titoli e proiezioni di un cinema; inoltre permette di avere utenti anonimi e registrati.
Gli utenti registrati si dividono in gestori e clienti. 
Il sistema offre diverse funzionalità in base alla tipologia di utente come indicato nel file Traccia Progetto.docx nel quale sono indicate tutte le funzionalità del progetto nel dettaglio. 
Nella cartella Documentazione si può trovare tutta la documentazione allegata al progetto, in particolare il file Tesina.pdf espone una panoramica degli aspetti principali legati alla documentazione del sistema.
La cartella Cinema contiene tutto l'applicativo.

Prerequisiti

Per utilizzare l'applicativo è necessario eseguire i seguenti passaggi.
I comandi si riferiscono ad un sistema operativo Linux.

1. Installare Python (Versione 3.10)
	apt install python3.10

2. Installare pip (se non è già presente)
	sudo apt install python3-pip

3. Installare pipenv
	pip install pipenv

4. Creare una nuova cartella e accedere alla cartella appena creata
	mkdir Cinema
	cd Cinema/

5. Accertarsi di avere pipenv installato
	pipenv --version

6. Installare Django nel virtual environment
	pipenv install django

7. Attivare il virtual environment
	pipenv shell

8. Il prompt riporterà tra parentesi il nome del virtual environment utilizzato
	(Cinema)$

9. Installare le dipendenze del file requirements.txt
	pip install -r requirements.txt

10. Per avviare il server eseguire il comando
	python manage.py runserver

Nota su alcune librerie usate 

Di seguito sono riportate delle indicazioni su alcune librerie installate

1.Pillow-10.3.0
Pillow è una libreria di Python su cui Django fa affidamento per gestire i file immagine ed è necessario per utilizzare ImageField in Django. 
MEDIA_URL e MEDIA_ROOT sono stati configurati in settings.py per gestire i file media caricati dagli utenti (MEDIA_URL = '/media/' e MEDIA_ROOT = os.path.join(BASE_DIR, 'media')) 
e sono stati utilizzati in urls.py del progetto per gestire i file media durante lo sviluppo (urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)).
ImageField nel modello Film utilizza Pillow per gestire i file immagine; quindi, per gestire correttamente le immagini caricate dagli utenti (immagine = models.ImageField(upload_to='film_immagini/')).
Installata con: pip install Pillow.

2.django-crispy-forms-2.2
django-crispy-forms è una libreria di terze parti per Django che fornisce un modo semplice e potente per gestire la visualizzazione e la stilizzazione dei form.
Ho scelto di utilizzarla per dare un aspetto più elegante e ben strutturato alla parte di presentazione del mio progetto dal punto di vista grafico.
Ho configurato alcune impostazioni nel file settings.py: django-crispy-forms è stato aggiunto alle app installate (aggiunto ad INSTALLED_APPS: 'crispy_forms') 
e ho Impostato il template pack di default (CRISPY_TEMPLATE_PACK = 'bootstrap4').
Installata con: pip install django-crispy-forms.

3.crispy-bootstrap4-2024.1
crispy-bootstrap4 è un pacchetto per Django che integra il framework di form django-crispy-forms con Bootstrap 4.
Questo pacchetto rende facile la creazione di form ben strutturati e stilizzati utilizzando le classi di Bootstrap 4, senza dover scrivere manualmente il codice HTML per ciascun form.
Ho scelto di utilizzarlo per dare un aspetto più elegante e ben strutturato alla parte di presentazione del mio progetto dal punto di vista grafico.
Ho configurato alcune impostazioni nel file settings.py: crispy_bootstrap4 è stato aggiunto alle app installate (aggiunto ad INSTALLED_APPS: 'crispy_bootstrap4') 
e ho Impostato il template pack di default (CRISPY_TEMPLATE_PACK = 'bootstrap4', CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4").
Installato con: pip install crispy-bootstrap4.

4.django-braces-1.15.0
django-braces è una libreria di terze parti per Django che fornisce una serie di mixins riutilizzabili, progettati per semplificare le operazioni comuni nelle view class-based di Django (CBV).
La ho utilizzata per le view per i soli utenti gestori per verificare che gli utenti che tentavano di eseguire le operazioni associate a quelle view appartenessero al gruppo dei gestori e per negare tali funzionalità agli utenti che non fanno parte di tale gruppo.
Le funzionalità principali che ho utilizzato sono state due mixins appartenenti agli Access Mixins: 
LoginRequiredMixin, che garantisce che l'utente sia autenticato prima di poter accedere alla view, e UserPassesTestMixin, che permette di definire una funzione di test personalizzata che deve restituire True affinché l'utente possa accedere alla view.
Ho incluso la libreria con 'from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin' 
e ho usato le sue funzionalità con 'class CreateFilmView(LoginRequiredMixin, UserPassesTestMixin, CreateView)' nelle view interessate.
Installato con: pip install django-braces.

