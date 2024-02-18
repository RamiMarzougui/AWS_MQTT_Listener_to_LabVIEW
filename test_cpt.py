import time
compteur_header_prev = -1
compteur_header = 0
while True:
    compteur_header = (compteur_header+1)%256
    # Conditions initilaes
    if compteur_header_prev == -1 or compteur_header == compteur_header_prev + 1 or (compteur_header == 0 and compteur_header_prev==255):
        print("OK ✅")
        compteur_header_prev = compteur_header
    else:
        #breakpoint()
        if compteur_header_prev == 255:
            compteur_header_prev = 0
        else:
            print("ERROR ❌")
            print(" PREV : " + str(compteur_header_prev) + "   NEW : " + str(compteur_header))
            compteur_header_prev +=1
    time.sleep(0.1)