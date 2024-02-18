from can_nwt import CanNwt 
import time

# create the CAN handler
h_can = CanNwt()

while True:
    msg = {"id":1,
           "data":[1,2,3,4,5,6,7]}
    h_can.WriteMessage()
    time.sleep(1)
    pass