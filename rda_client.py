import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

# MQTT Broker info
broker_address = "192.168.219.177"
broker_port = 1883

#Topic
rda_response = "rda/iot/response" 
rda_request = "rda/iot/query" 
rda_id = 0

def rda_set(): # set database access info
    rv = {"db_host":"localhost", "db_port":"3306", "db_name":"nplt", "db_user":"root", "db_password":"P@ssw0rd"}
    return rv

def get_ID(): # generating unique id
    ctm = int(datetime.timestamp(datetime.now()) * 1000)
    return ctm

# Callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(rda_response)

def on_message(client, userdata, msg):
    m = msg.payload.decode('utf-8')
    print(f"\nReceived message on topic {msg.topic}: {m}")

client = mqtt.Client()  # Create MQTT client instance

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, broker_port, 60) # Connect to the broker
client.loop_start()  # Start the loop

try:
    while True:
        # Publish a message
        message = str(input("Input Query: "))
        if message.lower()=="end":
            break
        rda_id = get_ID()
        rda_head=rda_set()
        rda_body={"id":rda_id, "sql":message}
        rda_message = json.dumps({"head":rda_head, "body":rda_body})
        client.publish(rda_request, rda_message)
        # Wait for a while before publishing the next message
        time.sleep(3)
except KeyboardInterrupt: # Disconnect on keyboard interrupt
    client.disconnect()
    client.loop_stop()
    print("Disconnected.")
