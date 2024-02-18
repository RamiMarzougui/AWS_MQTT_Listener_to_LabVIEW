# AWS_MQTT_Listener_to_LabVIEW
This program receives compressed data from the AWS IoT core via MQTT, decompresses it and decodes it then sends it to a LabView VI via TCP


1. Connects to the AWS MQTT broker 
Then, in 3 threads are created:
  a. Reads MQTT messages from the topic to which it has subscribed, decodes, deconcatenates, and decompresses (according to a given dbc) everything except the data part of the frames, then stores it all in an array for part b.
  b. Retrieves the uncompressed yet data at a constant time interval with a delay (to compensate for some eventual latency in the cloud service), then decompresses and organizes them in order (FIFO) for part c.
  c. Creates and manages a TCP connection, waits for the LabView VI's connection, and sends the read data from the FIFO to Labview

Note : All functions with "save_" are debug functions for testing, they allow saving results in .trc or .json format
