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


def get_geolocation():
    import requests
    url = 'https://ipinfo.io/loc'
    res = requests.get(url=url)
    if res.status_code == 200:
        return list(map(float, res.text.split(',')))
    return [10.878064, 106.806755]


def main():
    client = mqttclient.Client("Gateway_Thingsboard")

    client.on_connect = connected
    client.on_subscribe = subscribed
    client.on_message = recv_message

    client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)
    client.connect(BROKER_ADDRESS, PORT)
    client.loop_start()

    temperature = 25
    humidity = 25
    light_intensity = 300
    latitude, longitude = get_geolocation()

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
        time.sleep(10)


if __name__ == '__main__':
    main()


