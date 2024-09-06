"""Subscribes to the MQTT broker and listens for messages."""

# pylint: disable=W0613

import json
import os
import logging
import sys

import paho.mqtt.client as mqtt
import paho.mqtt.enums as mqtt_enums
import requests

logging.basicConfig(level=logging.INFO)

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASS = os.getenv("PASSWORD")

POST_TOKEN = os.getenv("POST_TOKEN")

if not HOST:
    logging.error("HOST environment variable not set")
    sys.exit(1)

if PORT and PORT.isdigit():
    PORT = int(PORT)
else:
    logging.error("PORT environment variable not set or not an integer")
    sys.exit(1)


def on_connect(client, userdata, flags, reason_code, properties):
    """Callback for when the client receives a CONNACK response from the server."""
    logging.info("Connected with result code %s", str(reason_code))
    client.subscribe("fixtures/info")


def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server."""
    payload = json.loads(json.loads(msg.payload.decode("utf-8")))

    matches = payload["fixtures"]
    for i, match in enumerate(matches):
        logging.info("Processing match %s of %s", str(i + 1), str(len(matches)))
        try:
            requests.post(
                "http://e0-api:8000/fixtures",
                json=match,
                headers={"Authorization": f"Bearer {POST_TOKEN}"},
                timeout=5,
            )
        except requests.exceptions.RequestException as e:
            logging.error("Error posting match: %s", str(e))
    logging.info("All matches processed")


mqttc = mqtt.Client(mqtt_enums.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set(USER, PASS)
mqttc.connect(HOST, PORT, 60)

mqttc.loop_forever()
