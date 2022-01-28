import paho.mqtt.client as mqttclient
import time
import json
from random import randint

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "eh89C3FhVCdHy3N2HMt1"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")

def main():
    client = mqttclient.Client("Gateway_Thingsboard")

    client.on_connect = connected
    client.on_subscribe = subscribed
    client.on_message = recv_message

    client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)
    client.connect(BROKER_ADDRESS, PORT)
    client.loop_start()

    temperature = 25
    humidity = 30
    light_intensity = 100
    longitude = 106.706819
    latitude = 11.678461
    while 1:
        data = {
            'temperature': temperature,
            'humidity': humidity,
            'light': light_intensity,
            'longitude': longitude,
            'latitude': latitude
        }
        client.publish('v1/devices/me/telemetry', json.dumps(data), 1)

        temperature += randint(-1, 1)
        humidity += randint(-1, 1)
        light_intensity += randint(-1, 1)
        time.sleep(3)


if __name__ == '__main__':
    main()

