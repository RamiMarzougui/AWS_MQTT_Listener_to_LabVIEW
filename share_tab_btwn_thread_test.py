import threading
import time
from queue import Queue

# Fonction pour mettre à jour le tableau dans le premier thread
def update_tableau(tableau, queue):
   i = 0
   while True:
        
        i = (i+1)%1001
        # Mettre à jour le tableau
        # Par exemple, ajouter des éléments
        new_data = i
        #tableau.append(new_data)

        # Mettre à jour la file d'attente
        queue.put(new_data)
        
        # Attendre 100 ms
        time.sleep(0.00001)

# Fonction pour lire et vider le tableau dans le second thread
def read_and_clear_tableau(queue):
    while True:
        tableau_data = []
        while not queue.empty():
            tableau_data.append(queue.get())
        
        # Faire quelque chose avec le tableau
        print("Data lu:", tableau_data)

        # Vider le tableau
        #tableau_data.clear()
        # Attendre 1 seconde
        #time.sleep(0.0001)


# Créer le tableau partagé et la file d'attente
tableau_partage = []
file_attente = Queue()

# Créer un verrou
verrou = threading.Lock()

# Créer les threads
thread_mise_a_jour = threading.Thread(target=update_tableau, args=(tableau_partage, file_attente))
thread_lecture = threading.Thread(target=read_and_clear_tableau, args=(file_attente,))

# Démarrer les threads
thread_mise_a_jour.start()
thread_lecture.start()

# Attendre que les threads se terminent (vous pouvez utiliser des signaux d'arrêt pour une sortie propre)
thread_mise_a_jour.join()
thread_lecture.join()