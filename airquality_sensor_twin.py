import paho.mqtt.client as mqtt
import random
import time
import json

# Digital twin info
namespace = "airquality"
sensor_name = "mysensor"

# MQTT info
broker = "192.168.49.2"  # Replace with your MQTT broker address
port = 30511  # Replace with your MQTT broker port
topic = "telemetry/"  # Topic where data will be published

# Authentication info (replace with actual username and password)
username = ""
password = ""

# MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successful connection")
    else:
        print(f"Connection failed with code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(username, password)
client.connect(broker, port, 60)

def generate_air_data():
    temperature = random.uniform(15, 45)
    humidity = random.uniform(0, 100)
    co2 = random.uniform(0, 5)
    return temperature, humidity, co2

def get_ditto_protocol_value_air(time, temperature, humidity, co2):
    return {
        "temperature": {
            "properties": {
                "value": temperature,
                "time": time
            }
        },
        "humidity": {
            "properties": {
                "value": humidity,
                "time": time
            }
        },
        "co2": {
            "properties": {
                "value": co2,
                "time": time
            }
        }
    }

def get_ditto_protocol_msg(name, value):
    return {
        "topic": f"{namespace}/{name}/things/twin/commands/merge",
        "headers": {
            "content-type": "application/merge-patch+json"
        },
        "path": "/features",
        "value": value
    }

# Send data
try:
    client.loop_start()  # Start the MQTT loop

    while True:
        t = round(time.time() * 1000)  # Unix time in ms

        # Sensor twin
        temperature, humidity, co2 = generate_air_data()
        msg = get_ditto_protocol_msg(sensor_name, get_ditto_protocol_value_air(t, temperature, humidity, co2))
        client.publish(topic + namespace + "/" + sensor_name, json.dumps(msg))
        print(t, temperature, humidity, co2, f"{sensor_name} data published", sep="|")

        time.sleep(5)

except KeyboardInterrupt:
    client.loop_stop()  # Stop the MQTT loop
    client.disconnect()
