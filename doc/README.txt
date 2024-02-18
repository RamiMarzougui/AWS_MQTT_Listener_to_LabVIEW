################################################################## 14/12/23 ##############################################################
VERSION STABLE : mqtt_reader_compressed_RT_v2-4-3.py

COMPATIBILITE : 
	- Labview : LBV_Lutece_V1
	- Publisher : mqtt_loader_compr_CAN_v1-1-4
	- Comparateur : realTime_compare_V3 (aucune différence avec la V2)

CONDITIONS :
Un trc avec des datas pseudo aléatoire (généré par python) et envoyé sur le CAN.
Le CAN est lue par le simulateur du VCU (mqtt_loader_compr_CAN_v1-1-4.py) qui renvoie les msgs échantillonés sur MQTT.
Les msgs sont récupérés et transféré à Labview via TCP (mqtt_reader_compressed_RT_v2-4-3.py)

	
TEST : 
	- Comparaison data : 
		- Comparaison tableau debug Labview avec debug_history de python : Avec notepad ++, ok, aucune perte, tout dans l'ordre
		- fichier test : test_error_final

##########################################################################################################################################

################################################################## 15/12/23 ##############################################################
VERSION STABLE : mqtt_reader_compressed_RT_v2-4-4.py, ajout de la gestion des erreurs

COMPATIBILITE : 
	- Labview : LBV_Lutece_V1
	- Publisher : mqtt_loader_compr_CAN_v1-1-5, ajout du compteur par temps de cycle
	- Comparateur : realTime_compare_V3 (aucune différence avec la V2)

CONDITIONS :
Un trc avec des datas pseudo aléatoire (généré par python) et envoyé sur le CAN.
Le CAN est lue par le simulateur du VCU (mqtt_loader_compr_CAN_v1-1-5.py) qui renvoie les msgs échantillonés sur MQTT.
Les msgs sont récupérés et transféré à Labview via TCP (mqtt_reader_compressed_RT_v2-4-4.py)

NOTE : 
Avec le détection d'erreurs, on remarque que mqtt_loader_compr_CAN_v1-1-5 envoi des trames qui, sont parfois coupées par la tempo à 100ms.
Par exemple, envoi deux paquets de 6trames au lieu d'un seul de 12 trames.

TEST : 
	- Comparaison data : 
		- Comparaison tableau debug Labview avec debug_history de python : Avec notepad ++, ok, les pertes sont gérées, tout dans l'ordre
		- fichier test : test_error_final2
##########################################################################################################################################