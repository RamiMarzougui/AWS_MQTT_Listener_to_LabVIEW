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
t = 0
while flag:
    try : 
        if t==0:
            t=int(time.time())
        else:
            t+=1
        t_conv = int(str(t)[-4:])
        t_byte = t_conv.to_bytes(4,"big")
        #id = bytes([110+i,120+i,130+i,140+i])
        # data = bytes([0+i,10+i,20+i,30+i,40+i,50+i,60+i,70+i])
        # data_hex = hex(int.from_bytes(data, byteorder='big'))
        data = i
        message = data.to_bytes(8,"big")
        data_hex = hex(int.from_bytes(message, byteorder='big'))
        print("time : "+str(t_conv)+"  /  data : "+str(data))
        client_socket.sendall(t_byte)
        client_socket.sendall(message)
        i = (i+1)%10
        #client_socket.sendall(message.encode('utf-8'))
        #time.sleep(0.001)
        time.sleep(1)
    except:
        print("le client est déconnecté")
        raise
        break

# Fermer les sockets
client_socket.close()
serveur_socket.close()

