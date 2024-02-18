import time
from queue import Queue

tab_receive = []
# Init Var
#P1_header  = {"ts_s":1, "compteur":1}
P1_trame_1 = {"id":"A","ms_ts":1,"data":[1,2,3]}
P1_trame_2 = {"id":"B","ms_ts":2,"data":[1,2,3]}
P1_trame_3 = {"id":"C","ms_ts":3,"data":[1,2,3]}
P1_trame_4 = {"id":"D","ms_ts":4,"data":[1,2,3]}
P1_trame_5 = {"id":"E","ms_ts":5,"data":[1,2,3]}
tab_receive.append(P1_trame_1)

P1_trame_1 = {"id":"A","ms_ts":1,"data":[1,2,3]}
P1_trame_2 = {"id":"B","ms_ts":2,"data":[1,2,3]}
P1_trame_3 = {"id":"C","ms_ts":3,"data":[1,2,3]}
P1_trame_4 = {"id":"D","ms_ts":4,"data":[1,2,3]}
P1_trame_5 = {"id":"E","ms_ts":5,"data":[1,2,3]}
