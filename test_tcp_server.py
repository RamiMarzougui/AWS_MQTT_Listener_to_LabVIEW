import socket
import random
import time


# Créer un socket TCP/IP pour le serveur
serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Lier le socket à une adresse et un port
adresse_serveur = ('localhost', 12345)
serveur_socket.bind(adresse_serveur)
# Mettre le socket en mode écoute
serveur_socket.listen(1)
print(f"Le serveur écoute sur {adresse_serveur[0]}:{adresse_serveur[1]}")

# Attendre une connexion
client_socket, client_address = serveur_socket.accept()

print("Le client est connecté")

# Flag while
flag = True
i= 0
while flag:
    try : 
        id = 820
        id = id.to_bytes(4,"big")
        #id = bytes([110+i,120+i,130+i,140+i])
        data = bytes([0+i,10+i,20+i,30+i,40+i,50+i,60+i,70+i])
        data_hex = hex(int.from_bytes(data, byteorder='big'))
        message = data
        print(data_hex)
        client_socket.sendall(id)
        client_socket.sendall(message)
        i = (i+1)%10
        #client_socket.sendall(message.encode('utf-8'))
        time.sleep(1)
    except:
        print("le client est déconnecté")
        break

# Fermer les sockets
client_socket.close()
serveur_socket.close()

