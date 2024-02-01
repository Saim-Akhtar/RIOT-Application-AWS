import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    # Subscribe to the topic of interest
    client.subscribe("local_to_cloud")  # Replace with your desired topic

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    save_to_influxdb(msg.topic, msg.payload.decode())

def save_to_influxdb(topic, payload):
    token = "jUw-Q2_5fy8xXL0toyat5b_XUY6UktKzjG-r31cbhaRYTajjiOPXJwcUHvNlrCafRsgVMSnYMws-71nM1Gz4qA=="
    org = "iot_project"
    bucket = "iot_bucket"
    url = "http://localhost:8086"

    client = InfluxDBClient(url=url, token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("mqtt_data").tag("topic", topic).field("payload", payload)
    write_api.write(bucket, org, point)

# Create an MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the Mosquitto broker (replace with your broker details)
client.connect("2a05:d016:c59:1d18:70d3:bed4:fc5a:68ac", 1883, 60)  # Replace with your broker's address and port

# Start the MQTT client loop to handle events
client.loop_forever()
