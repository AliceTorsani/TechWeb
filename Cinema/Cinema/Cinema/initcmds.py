from gestione.models import Utente, Film, Proiezione, Prenotazione
import os
from django.core.files import File
from django.utils import timezone
from datetime import timedelta, datetime, time
import random

def erase_db():
    print("Cancello il DB")
    Film.objects.all().delete()
    Proiezione.objects.all().delete()
    Prenotazione.objects.all().delete()


def init_db():

    #se ci sono già dei film nel database non faccio nulla
    if len(Film.objects.all()) != 0:
        return
    
    filmdict = {
        "titoli": ["Il Signore degli Anelli: La Compagnia dell'Anello", "Harry Potter e la Pietra Filosofale", "La Bussola d'Oro", "Le Cronache di Narnia: Il Leone, la Strega e l'Armadio",
                    "Blade Runner", "Matrix", "Inception", "Interstellar", 
                    "Toy Story", "Il Re Leone", "Alla Ricerca di Nemo", "Shrek", 
                    "Titanic","Orgoglio e Pregiudizio", "Le pagine della nostra vita", "La La Land", 
                    "Il Sesto Senso", "Chinatown", "Seven", "Assassinio sull'Orient Express", 
                    ], 
        "generi": ["Fantasy", "Fantasy", "Fantasy", "Fantasy", 
                    "Fantascienza", "Fantascienza", "Fantascienza", "Fantascienza", 
                    "Animazione", "Animazione", "Animazione", "Animazione",
                    "Romantico", "Romantico", "Romantico", "Romantico",
                    "Giallo", "Giallo", "Giallo", "Giallo", 
                    ], 
        "descrizioni": ["Un giovane hobbit, Frodo, intraprende un pericoloso viaggio per distruggere l'Unico Anello e salvare la Terra di Mezzo dal potere oscuro di Sauron.", 
                        "Harry Potter scopre di essere un mago nel giorno del suo undicesimo compleanno e viene portato alla scuola di magia di Hogwarts, dove comincia la sua avventura.",
                        "Lyra Belacqua, una giovane orfana, si imbarca in un'avventura attraverso mondi paralleli per salvare il suo migliore amico e altri bambini rapiti.", 
                        "Quattro fratelli scoprono un armadio magico che li trasporta nel mondo incantato di Narnia, dove devono unire le forze con Aslan, un leone parlante, per sconfiggere la Strega Bianca.", 
                        "In un futuro distopico, un ex poliziotto deve dare la caccia a un gruppo di replicanti fuggitivi che cercano di prolungare la loro vita.", 
                        "Un hacker scopre la verità sulla sua realtà e il suo ruolo nella guerra contro i controllori di essa, le macchine intelligenti.", 
                        "Un ladro che ruba segreti attraverso l'uso della tecnologia di condivisione dei sogni riceve l'incarico di impiantare un'idea nella mente di un CEO.", 
                        "Un gruppo di esploratori spaziali viaggia attraverso un wormhole alla ricerca di una nuova casa per l'umanità, mentre la Terra è in pericolo di estinzione.", 
                        "Quando un nuovo giocattolo, Buzz Lightyear, arriva nella stanza di Andy, il cowboy Woody si sente minacciato e inizia una serie di avventure che portano a una preziosa amicizia.", 
                        "Il giovane leone Simba deve affrontare la sua eredità e prendere il suo posto come re della savana dopo la morte del padre, Mufasa.", 
                        "Un pesce pagliaccio, Marlin, parte in un'avventura per ritrovare suo figlio Nemo, rapito da un subacqueo e finito in un acquario.", 
                        "Un orco solitario di nome Shrek si allea con un asino chiacchierone per salvare una principessa incantata da un malvagio signore, Lord Farquaad.", 
                        "Una giovane aristocratica si innamora di un artista povero a bordo del lussuoso, ma sfortunato, RMS Titanic.", 
                        "Nella campagna inglese del XIX secolo, Elizabeth Bennet deve confrontarsi con le questioni dell'orgoglio, del pregiudizio e dell'amore mentre si innamora del misterioso Mr. Darcy.", 
                        "Una giovane coppia degli anni '40 si innamora profondamente, ma viene separata dalle circostanze e dalle differenze sociali. Anni dopo, si ritrovano e riscoprono il loro amore.", 
                        "Un musicista jazz e un'aspirante attrice si incontrano e si innamorano a Los Angeles, cercando di conciliare l'amore con le loro ambizioni e carriere.", 
                        "Un bambino di otto anni, Cole Sear, è perseguitato da visioni di spiriti. Il psicologo infantile Dr. Malcolm Crowe cerca di aiutarlo a svelare il mistero di questi incontri inquietanti.", 
                        "Un investigatore privato di Los Angeles degli anni '30 viene coinvolto in una rete di inganni, corruzione e omicidi mentre indaga su una semplice questione di adulterio.", 
                        "Due detective sono sulle tracce di un serial killer che commette omicidi seguendo i sette peccati capitali.", 
                        "Durante un viaggio in treno, il famoso detective Hercule Poirot indaga sull'omicidio di un ricco uomo d'affari, con molti passeggeri che diventano sospettati.", 
                        ],
        "prezzi": [10.0, 10.0, 13.0, 13.0, 10.0, 13.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 13.0, 13.0, ], 
        "immagini": ["immagini_film/Signore_anelli.jpeg", "immagini_film/Harry_Potter.jpeg", "immagini_film/Bussola_oro.jpeg", "immagini_film/Narnia.jpeg",
                    "immagini_film/Blade_Runner.jpeg", "immagini_film/Matrix.jpeg", "immagini_film/Inception.jpeg", "immagini_film/Interstellar.jpeg",  
                    "immagini_film/Toy Story.jpeg", "immagini_film/Re_leone.jpeg", "immagini_film/Nemo.jpeg", "immagini_film/Shrek.jpeg", 
                    "immagini_film/Titanic.jpeg", "immagini_film/Orgoglio_pregiudizio.jpeg", "immagini_film/Pagine.jpeg", "immagini_film/LaLaLand.jpeg", 
                    "immagini_film/Sesto.jpeg", "immagini_film/Chinatown.jpeg", "immagini_film/Seven.jpeg", "immagini_film/Express.jpeg", 
                    ],
        "in_3D": [False, False, True, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, True, ], 
        "in_inglese": [False, True, False, True, False, False, True, False, False, False, False, False, True, False, False, False, True, False, False, True, ], 
    }

    for i in range(len(filmdict['titoli'])):
        # Crea un'istanza del film
        film = Film(
            titolo=filmdict['titoli'][i],
            genere=filmdict['generi'][i],
            descrizione=filmdict['descrizioni'][i],
            prezzo=filmdict['prezzi'][i],
            in_3D=filmdict['in_3D'][i],
            in_inglese=filmdict['in_inglese'][i]
        )

        # Ottieni il percorso dell'immagine e il nome base dell'immagine
        image_path = filmdict['immagini'][i]
        image_name = os.path.basename(image_path)

        # Apri il file immagine e assegnalo al campo immagine
        with open(image_path, 'rb') as img_file:
            film.immagine.save(image_name, File(img_file), save=True)

        # Salva il film nel database
        film.save()
    
    # Definizione delle liste condivise per le sale
    num_sale = 8 # Numero totale di sale
    #Creare un dizionario per tracciare le proiezioni per sala:
    proiezioni_per_sala = {sala: [] for sala in range(1, num_sale + 1)}
    film_list = Film.objects.all()
    # Loop sui film
    for film in film_list:
        # Crea le proiezioni per il film
        # Numero randomico di proiezioni per il film
        num_proiezioni = random.randint(2, 4) #Per ogni film, scegliamo un numero casuale di proiezioni tra 2 e 4
        proiezioni_aggiunte = 0
        giorni_possibili = list(range(7, 10)) #distribuisco le proiezioni in un intervallo da 7 a 9 giorni.
        random.shuffle(giorni_possibili)
        today = timezone.now().date() #Calcolare la data di proiezione partendo da oggi.

        while proiezioni_aggiunte < num_proiezioni:
            for days_ahead in giorni_possibili:
                if proiezioni_aggiunte >= num_proiezioni:
                    break
                proiezioni_per_giorno = random.randint(1, 3)  # Da 1 a 3 proiezioni per giorno
                orari_possibili = [time(14 + i*2, 0) for i in range(3)] # Proiezioni alle 14:00, 16:00, ecc.
                random.shuffle(orari_possibili)

                for proiezione_time in orari_possibili:
                    if proiezioni_aggiunte >= num_proiezioni:
                        break
                    proiezione_date = today + timedelta(days=days_ahead) #Calcolare la data di proiezione partendo da oggi.

                    # Mescola le sale disponibili
                    sale_disponibili = list(proiezioni_per_sala.keys())
                    random.shuffle(sale_disponibili)

                    # Trova una sala disponibile
                    sala_disponibile = None
                    for sala in sale_disponibili:
                        sala_occupata = False
                        for p in proiezioni_per_sala[sala]:
                            if p['data'] == proiezione_date and p['ora_inizio'] == proiezione_time:
                                sala_occupata = True
                                break
                        if sala_occupata == False:
                        #allora è libera per questa proiezione e la assegno
                            sala_disponibile = sala
                            break #esco dal for sulle sale perchè ho trovato una sala libera
                    
                    if sala_disponibile is None:
                        continue  # Nessuna sala disponibile per questo slot di tempo, salta questa proiezione
                    
                    sala_name = f"Sala {sala_disponibile}"
                    proiezione = Proiezione(
                        film=film,
                        data=proiezione_date,
                        ora_inizio=proiezione_time,
                        sala=sala_name
                    )
                    proiezione.save()

                     # Aggiungi la proiezione alla lista delle proiezioni per quella sala
                    proiezioni_per_sala[sala_disponibile].append({
                        'data': proiezione_date,
                        'ora_inizio': proiezione_time
                    })
                    proiezioni_aggiunte += 1


    # Debugging output: verifico che siano state create le proiezioni correttamente
    for sala, proiezioni in proiezioni_per_sala.items():
        print(f"Proiezioni in Sala {sala}: {proiezioni}")


