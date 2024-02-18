from canlib import canlib, Frame
import time
import random
from random import randint
import threading
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import cantools
import datetime
from copy import deepcopy
from operator import itemgetter
import os

#Class permettant de regrouper tous les éléments d'une trame
class TrameDBC:
    def __init__(self, name, id_dec, id_hexa, dlc, ext,
                 id_compressed, can_index):
        self.name = name
        self.id = id_dec
        self.dlc= dlc
        self.ext = ext
        self.id_compressed = id_compressed
        self.id_hexa = id_hexa
        self.can_index = can_index

#Class permettant de stocker toutes les objets de Trame
#c'est un handler 
class TramesDBC:
    def __init__(self):
        self.trames = []
    
    def add_trame(self,trame):
        self.trames.append(trame)

#Save on .TRC format
def save_trc():
    print("TRC saving ⌚") 

    #Raz 
    frames = []   
    ##--------------------DECOMPRESION-------------------------------------------------
 
    #-----------------init var----------------------------
    list_all_compressed_data_per_id = []
    list_compressed_data_per_id =[]
    list_uncompressed=[]
    list_uncompressed_sorted=[]
    data_out = []
    old_data = []
    octet = 0
    unconcatened_data =[]

    #copy pour ne pas modifier la data original
    unconcatened_data = deepcopy(frame_list) 

    #----------------Tri trame par id----------------------
    #parcours le dbc
    for signal in readed_dbc.trames:
        list_compressed_data_per_id =[]
        for data in unconcatened_data:
            #trouve l'équivalence du dbc
            if data["id"] == signal.id:
                list_compressed_data_per_id.append(data)
            #debug
            if len(data["data"]) != data["data_sorter"].count("1"):
                print("error tri par id")
        list_all_compressed_data_per_id.append(list_compressed_data_per_id)

    #----------------Test-------------------------------------------------------------
    # list_all_compressed_data_per_id = [[[],[],[]],[[],[],[]],[[],[],[]]]
    # list_all_compressed_data_per_id[0][0] = {'id': '827', 'dlc': 8, 'ext': '0', 'data_sorter': '11111111', 'data': [1,2,3,4,5,6,7,10], 'time_s': '1677752547', 'time_ms': '25.6', 'start': 1677752547, 'cpt_tri': 1, 'pack': 0, 'tri': 1677752547025.6, 'nb_trame': 5} 
    # list_all_compressed_data_per_id[0][1] = {'id': '827', 'dlc': 8, 'ext': '0', 'data_sorter': '00000001', 'data': [10], 'time_s': '1677752548', 'time_ms': '25.6', 'start': 1677752547, 'cpt_tri': 2, 'pack': 0, 'tri': 1677752548025.6, 'nb_trame': 5}
    # list_all_compressed_data_per_id[0][2] = {'id': '827', 'dlc': 8, 'ext': '0', 'data_sorter': '00000001', 'data': [10], 'time_s': '1677752549', 'time_ms': '25.6', 'start': 1677752547, 'cpt_tri': 3, 'pack': 0, 'tri': 1677752549025.6, 'nb_trame': 5}
    # list_all_compressed_data_per_id[1][0] = {'id': '825', 'dlc': 8, 'ext': '0', 'data_sorter': '11111111', 'data': [1,2,3,4,30, 31, 32, 33], 'time_s': '1677752547', 'time_ms': '76.8', 'start': 1677752547, 'cpt_tri': 1, 'pack': 0, 'tri': 1677752547076.8, 'nb_trame': 5}
    # list_all_compressed_data_per_id[1][1] = {'id': '825', 'dlc': 8, 'ext': '0', 'data_sorter': '00001111', 'data': [30, 31, 32, 33], 'time_s': '1677752548', 'time_ms': '76.8', 'start': 1677752547, 'cpt_tri': 2, 'pack': 0, 'tri': 1677752548076.8, 'nb_trame': 5}
    # list_all_compressed_data_per_id[1][2] = {'id': '825', 'dlc': 8, 'ext': '0', 'data_sorter': '00001111', 'data': [30, 31, 32, 33], 'time_s': '1677752549', 'time_ms': '76.8', 'start': 1677752547, 'cpt_tri': 3, 'pack': 0, 'tri': 1677752549076.8, 'nb_trame': 5}
    # list_all_compressed_data_per_id[2][0] = {'id': '31', 'dlc': 5, 'ext': '0', 'data_sorter': '11111', 'data': [50, 51, 52, 53, 54], 'time_s': '1677752547', 'time_ms': '128.0', 'start': 1677752547, 'cpt_tri': 1, 'pack': 0, 'tri': 1677752547128.0, 'nb_trame': 5}
    # list_all_compressed_data_per_id[2][1] = {'id': '31', 'dlc': 5, 'ext': '0', 'data_sorter': '11011', 'data': [55, 56, 57, 58], 'time_s': '1677752548', 'time_ms': '128.0', 'start': 1677752547, 'cpt_tri': 2, 'pack': 0, 'tri': 1677752548128.0, 'nb_trame': 5}
    # list_all_compressed_data_per_id[2][2] = {'id': '31', 'dlc': 5, 'ext': '0', 'data_sorter': '01110', 'data': [59, 60, 61], 'time_s': '1677752549', 'time_ms': '128.0', 'start': 1677752547, 'cpt_tri': 3, 'pack': 0, 'tri': 1677752549128.0, 'nb_trame': 5}
    #---------------------------------------------------------------------------------

    #------------Benchmark data in ---------------------------------------------------
    nb_octet_compressed = 0
    for id_data in list_all_compressed_data_per_id:
        for frame in id_data:
            nb_octet_compressed += 1 + 2  + 1  + len(frame["data"])
            #                     id +time+sort+ data
    #----------------------------------------------------------------------------------

    #--------------Décompression des trames--------------
    #Pour lire uniquement si on a reçu une trame de synchronisation
    first_data_sorter = False
    #parcour la liste de data par id
    for id_data in list_all_compressed_data_per_id:
        #traite chaque trame
        first_data_sorter = False
        old_data = None
        #parcour chaque trame dans la liste des datas pour un id
        for frame in id_data:
            try:
                #Maj le first data_sorter
                data_sorter_all_new = frame["dlc"]*"1" #Calcul le data sorter quand toutes les trames changent en focntion du dlc
                if frame["data_sorter"] == data_sorter_all_new.zfill(8) and first_data_sorter==False:
                    first_data_sorter = True
                
                #On sort de la lecture si pas de trame de syncrho et on passe
                #a la trame suivante
                if first_data_sorter == False:
                    continue

                #init data_out et octet
                data_out =[]
                octet = None
                #check si toutes les trames sont là
                if frame["dlc"] == len(frame['data']):
                    data_out = frame['data']
                else:
                    cpt_octet_data = 0 #permet de se déplacer dans les data compressées
                    #traite chaque octet de la partie data
                    # ici
                    #c'est le datasorter réel (ex: 111 au lieu de 0000 0011 si dlc=3)
                    data_sorter_real =frame["data_sorter"][-frame["dlc"]:]
                    for num_octet in range(0,frame["dlc"]):
                        if data_sorter_real[num_octet] == '0':
                            data_out.append(old_data[num_octet])
                        else:
                            octet = frame['data'][cpt_octet_data]
                            data_out.append(octet)
                            cpt_octet_data += 1
                #mise en mémoire de trame précédente
                old_data = data_out 
                #création trame de sortie
                list_uncompressed.append(frame)
                #maj de la partie data
                list_uncompressed[-1]['data'] = data_out

            except Exception as e:
                print(e)      
    print("") 
    #--------------Tri--------------
    #tri les trames dans l'odre chronologique en focntion du token
    list_uncompressed_sorted = sorted(list_uncompressed,key=itemgetter('tri'))

    
    ##---------------------------------------------------------------------------------------
    
    #ici on rend compatible la partie décompression avec le reste du programme
    frames = list_uncompressed_sorted

    #mise en forme de la start_date
    start_date = datetime.datetime.fromtimestamp(frames[0]['start'])
    start_date = start_date.strftime("%d/%m/%Y %H:%M:%S")

    #------------Benchmark data out ---------------------------------------------------
    # nb_octet_uncompressed = 0
    # for data_uncompressed in list_uncompressed_sorted:
    #         nb_octet_uncompressed += 1 + 2  + 1  + len(data_uncompressed["data"])
    #         #                     id +time+sort+ data
    # print ("facteur compression : " + str(nb_octet_uncompressed/nb_octet_compressed))
    #----------------------------------------------------------------------------------

    #ecriture fichier de sortie
    i = 0

    # création nom du fichier
    now = datetime.datetime.now()
    now_str = now.strftime("%d-%m-%Y_%H-%M-%S")
    file_name = "uncompress_" + now_str + ".trc"
    with open(file_name, 'w') as f: 
    
        #Ecriture en tête
        f.write(""";$FILEVERSION=1.3
;$STARTTIME=44956.551155115827
;
;   Start time: """ + str(start_date) +"""
;   Generated by NWT Network Bridge v1.0.0
;-------------------------------------------------------------------------------
;   Bus  Connection   Net Connection     Protocol  Bit rate
;   1    Connection1  Mqtt               Custom    Custom
;-------------------------------------------------------------------------------
;   Message   Time    Bus  Type   ID    Reserved
;   Number    Offset  |    |      [hex] |   Data Length Code
;   |         [ms]    |    |      |     |   |    Data [hex] ...
;   |         |       |    |      |     |   |    |
;---+-- ------+------ +- --+-- ---+---- +- -+-- -+ -- -- -- -- -- -- --""")
        for trame in frames:
            #Mise en forme id
            id = str(trame["id"])
            #Conversion en string hex
            id = str(hex(int(id))) 
            #Enleve le "0x"
            id = id.replace("0x","")
            #Met les lettres en majuscule
            id = id.upper()
            #les id can doivent sur 4 digit minimum pour les id classiques
            if len(id) < 4 and trame["ext"] == '0':
                id = id.zfill(4)
            #les id can doivent sur 8 digit minimum pour les id extend
            if  trame["ext"] == 1:
                id = id.zfill(8)
            #conversion time
            time_ms = trame["time_ms"].split('.')[0]
            #car pas de us dans les data reçu par le log
            if "." in trame["time_ms"]:
                us = trame["time_ms"].split('.')[1]
            else :
                us = str(0)
            time_s = trame["time_s"]#[-5:] #garde uniquement les 5 premiers caracteres car sinon trop long
            #les ms et us doivent etre sur 3 digits
            if len(us) < 3:
                us = us.ljust(3,'0')
            if len(time_ms) < 3:
                time_ms = time_ms.zfill(3)
            #Pour avoir l'offset par rapport au début de l'enregistrement
            #trame["start"] = 1768843635 #-------------test
            ms_int = int(time_s) - int(trame["start"])
            ms = str(ms_int) + time_ms #concatene le temps en s avec le temps en ms pour epochtime en ms
            
            #les data doivent être en hexa
            data = []  #data2 pour inviter interference avec autres fonctions
            for j in range (0,trame['dlc']):
                data.append(str(hex(trame["data"][j])))
                data[j] = data[j].replace("0x","")
                data[j] = data[j].upper()
                if len(data[j]) < 2:
                    data[j] = data[j].zfill(2)
            
            #Mise en forme data en fonction du DLC
            data_to_write =""
            for k in range (0,trame["dlc"]):
                data_to_write = data_to_write + data[k] + " "

            #ecriture data
            f.write("\n" + (6-len(str(i+1)))*" " + str(i+1) + ")" +(10-len(ms))*" " + ms
            + "."+ us + " " + "1" + 2*" " + "Rx" + (12-len(id)) * " " 
            + id + " " + "_" + 2*" " + str(trame["dlc"]) + 4*" " + data_to_write)
            #+ " Data_sorter: " + trame["data_sorter"])  #Only for debug
            i+=1
    print("TRC saved ✅")

def frames_received(payload):
    global readed_dbc # objet dbc
    global cpt_rank # compteur de rang (numéro paquet)
    global start_time # epoch du début de l'enregistrement
    global frame_list # datas lues
    global payload_history
    global t_last_receive
    global point_display

    # Fait varier le publish
    point_display = (point_display+1)%10
    print("Frame received" + point_display*".")

    #Get the current time when receiving data
    t_last_receive = time.time() 
    #Debug l'historique des valeurs reçues
    payload_history.append(str(payload))
    
    # -------------- Debug payload --------------------
    #payload = b'\x11eM\xffI\x00\t\x00\x14\xff\x00\x89\xc0\xb5z\xf8\x1eH\n\x00&\x1f\x041\x8aS6\x0b\x007\xff|W\xfd\x84\x9a\xd6\x1b\xf4\x0c\x00B\x7fe\xfeY(\xd5\x18\x85\x11\x00F\x7f\x1a:R]\xc0\xd6\xef\x12\x00N\x7fB\x1b~\xaa\x0bIu\x13\x00T\x7f\xef<\xbe\x9c\xdaXY\x14\x00b\xff\xc4\x8a\x99\x0fjg\xf7\x1a\x16\x00b\x7f\x00iQ\xc8\xd2t\xdf\x17\x00e\x7f\xcam\x02\xed2\x9b\xe3\x18\x00k\xff\xc1\xbd\x83\xe4\x92\x9a\xc27\x1e\x00m\xffT\x04\x1f6\xfe\xed*\xff\x1f\x00{\xff1\xa64\xa0\xaa\x91Pd \x00\x88\xff\xa3,\x1ah\xc16\x1a\xac!\x00\x90\xffIX8\x9b\xedw\xe2g"\x00\x9a\xff\xb7\x8a\x84\xa4q\x95\xbaw#\x00\xaa\xff\x01\x8aCz\xbf\x0e\xec"'

    # ----- Decode the header ------
    # nb trame
    nb_trames = payload[0]
    # epoch s
    epoch_s = payload[1] << 24 | payload[2] << 16 | payload[3] << 8 | payload[4]
    # Get the first epoch as a start time
    if start_time == 0: #if=0 the var is unitialized
        start_time = epoch_s

    # get compteur signal triangle et update graph
    compteur = payload[5]

    
    # ----- Decode the frame ------
    # init
    id_compressed = 0 # déclaration et RAZ
    # nombre de 1 dans data_sorter
    nb_un = 0 
    offset = 0
    data =[]
    
    #récupère les infos par id
    for i in range(0,nb_trames):
        #recup le data sorter
        data_sorter_int =  payload[9+offset]
        #converti en string de binaire
        data_sorter = str(bin(data_sorter_int)[2:])
        #trouverle nombre de 1 dans le data sorter
        nb_un = 0
        for num in data_sorter:
            if num == '1':
                nb_un += 1
        #recup l'id compressé
        id_compressed =  str(payload[6+offset])

        #parcour le fichier dbc pour le décoder
        for signal in readed_dbc.trames:
            #recup les infos associés à l'id compressé
            if id_compressed == signal.id_compressed:
                frame_id = signal.id
                frame_dlc = signal.dlc
                frame_ext = str(int(signal.ext))
                frame_ts_ms = payload[7+offset] << 8 | payload[8+offset]
                #init
                data =[]
                #récupère les datas de sortie
                for j in range (0,nb_un):
                    data.append(payload[10+offset+j])

                #Ajout structure
                frame = {'id': frame_id, 'dlc': frame_dlc, 'ext': frame_ext,
                            'data_sorter': data_sorter.zfill(8), 'data': data, 
                        'time_s': str(epoch_s), 'time_ms': str(frame_ts_ms/10), 
                        'start':start_time, 'tri': epoch_s*1000+frame_ts_ms/10,
                        'rank':compteur }
                frame_list.append(frame)
                break
                #breakpoint() 
        
        #maj cpt_rank 
        #cpt_rank += 1 
        
        #mise en mémoire nb_un
        offset += nb_un + 4 

    # Allow to debug inside this callback
    # Normal breakpoints doesn't work
    #breakpoint() 
    pass

# Save the payload history as json file
def save_payload_history():
    print("Json saving ⌚") 
    global payload_history
     # Récupération de la date et de l'heure actuelle pour le nom
    now = datetime.datetime.now()
    now_str = now.strftime("%d-%m-%Y_%H-%M-%S")
    # Get current directory
    current_dir = os.getcwd()
    # Set subdirectory
    sub_dir = "test"
    # Create the file name
    file_name =  os.path.join(current_dir,sub_dir,"payload_" + now_str + ".json")
    # Enregistrez la structure dans un fichier texte au format JSON
    with open(file_name, 'w') as fichier:
        json.dump(payload_history, fichier, indent=1)#, sort_keys=True)
    print("Json saved ✅")

# Callback when the subscribed topic receives a message
# Launch frames_received
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    #print("Message received : "+ str(payload))
    frames_received(payload)

# Read DBC and extract values
def read_dbc():
    #Créer l'handler pour les trames
    trames_dbc = TramesDBC()
    # Name Init
    name_dbc =  "DBC_VCU_V2.dbc"
    #handleur dbc (lis le dbc)
    database = cantools.database.load_file(name_dbc)
    #Récupération des informations du dbc et maj des objets
    for index, can_msg in enumerate(database.messages):
        name = can_msg.name
        id_can_decimal = str(can_msg.frame_id)
        id_can_hexa = hex(int(id_can_decimal))[2:].upper()
        id_can_hexa = id_can_hexa.zfill(4)
        dlc = can_msg.length
        ext = can_msg.is_extended_frame
        id_compressed = str(index)
        can_index = 1
        #maj des objets
        trame_dbc = TrameDBC(name, id_can_decimal, id_can_hexa ,dlc,ext,
                      id_compressed,can_index)
        #ajout au handler
        trames_dbc.add_trame(trame_dbc)
    return trames_dbc

# ---------------------------MAIN-------------------------------------

# Read DBC and extract values
global readed_dbc
readed_dbc = read_dbc()

global cpt_rank
cpt_rank = 0

global start_time
start_time = 0

global frame_list
frame_list = []

# List every Publiseh messga received
global payload_history
payload_history = []

# Temps de la denière récpetion d'une publication
global t_last_receive
t_last_receive = time.time()

# compteur permettnat de faire varier le print des published pour voir si on ublie toujours
global point_display 
point_display = 0

# ----------------------Init MQTT--------------------------
ENDPOINT = "a1xvyu1lci6ieh-ats.iot.eu-west-3.amazonaws.com"
CLIENT_ID = "subscribe_AwsPy"
PATH_TO_CERTIFICATE = "certificates/1334cda3fa4d4a36ea0a8a7755bdbba76db34541e9f23f89388c83d357d46527-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/1334cda3fa4d4a36ea0a8a7755bdbba76db34541e9f23f89388c83d357d46527-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"
TOPIC = "pyAws"
SAVE_ACTIVATED = False #active ou désactive la sauvegarde des datas mqtt
SAVE_TIMER = 10 #Timer pour sauvegarde data mqtt  6000 = 1 min

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

# Create the client
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting ⌚")
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected ✅")

# Subscribe to the topic
print("Subscribing ⌚")
subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=TOPIC,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        #qos=mqtt.QoS.AT_MOST_ONCE,
        callback=on_message_received)
subscribe_result = subscribe_future.result()
print("Subscribed ✅")



while True:

    # ------------Save----------
    #save data via debug
    save = False

    #save data via auto-save, 10 sec after nothing received
    t_check = time.time() # check si plus de 10sec
    if t_check - t_last_receive >= 10:
        save = True
    
    if save == True:
        
        save_trc()

        #save payload history as json
        # To test the differnce with the json generated by the publisher
        save_payload_history()
        
        break

    pass