import random
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "cinta"
topic2 = "pupus"
client_id = f'satu-atau-dua-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

# Define the client ID you want to listen to
target_client_id = "bintang"
target2_client_id = "kibo"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Received `{payload}` from `{msg.topic}` topic")
        
        # Assuming payload is formatted as "client_id: message"
        if payload.startswith(target_client_id):
            message = payload.split(": ", 1)[1]  # Extract the actual message
            print(f"Message from {target_client_id or target2_client_id}: {message}")
        else:
            print(f"Ignoring message not from {target_client_id}")

    client.subscribe(topic)
    client.subscribe(topic2)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
