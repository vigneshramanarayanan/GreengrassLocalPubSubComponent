# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 1
device_end = 6

#Path to the dataset, modify this
data_path = "vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "./Vehicles/vehicle{}/cert.pem"
key_formatter = "./Vehicles/vehicle{}/private.key"
topic_formatter = "vehicle{}/emission/data"
vehicle_counter = 0 

class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("a3j70qh1ex6gf3-ats.iot.us-east-1.amazonaws.com", 8883)
        self.client.configureCredentials("./Vehicles/AmazonRootCA1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO 3: fill in the function to show your received message
        #print("client {} received payload {} from topic {}".format(self.device_id, , ))
        pass


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass

    
    def publish(self, topic,vehicle_counter):
    # Load the vehicle's emission data
        
        df = pd.read_csv(data_path.format(vehicle_counter)) 
        df = df.sort_values(by='timestep_time')       
        for index, row in df.iterrows():
            # Create a JSON payload from the row data
            payload = json.dumps(row.to_dict())
            
            #time.sleep(1)
            # Publish the payload to the specified topic
            print(f"Publishing: {payload} to {topic}")
            self.client.publishAsync(topic, payload, 0, ackCallback=self.customPubackCallback)
            
            # Sleep to simulate real-time data publishing
            



print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):    
    try:
        client = MQTTClient(device_id,certificate_formatter.format(device_id) ,key_formatter.format(device_id))
        client.client.connect()
        clients.append(client)
        print("Connected so far {} MQTTClients ...".format(device_id))
    except:
        print("device {} failed to connect moving on..".format(device_id))
 

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            c.publish(topic_formatter.format(i+1),vehicle_counter)
            time.sleep(1)
            vehicle_counter = vehicle_counter + 1
            if vehicle_counter > 4:
                vehicle_counter = 0
            
                

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)





