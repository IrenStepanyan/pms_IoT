import paho.mqtt.client as mqtt
import time
import serial
import json
from datetime import datetime
import ssl

PORT = 8883
ENDPOINT = "d09530762c0nb5dceftxl-ats.iot.us-east-1.amazonaws.com"
TOPIC = "sensors/pms"
CLIENT_ID = "pms5003-client"

CA_PATH = "AmazonRootCA1.pem"
CERT_PATH = "e961b4f7eb09ee0432b039bf4928ea24e2e7a887a26d2cafc7e102b749b9ef75-certificate.pem.crt"
KEY_PATH = "e961b4f7eb09ee0432b039bf4928ea24e2e7a887a26d2cafc7e102b749b9ef75-private.pem.key"

ser = serial.Serial("/dev/serial0", 9600, timeout=2)

def on_connect(client, userdata, flag, rc):
    print(f"Connected to AWS IoT")

mqtt_client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311, transport="tcp")
mqtt_client.on_connect = on_connect

mqtt_client.tls_set(ca_certs=CA_PATH,
                    certfile=CERT_PATH,
                    keyfile=KEY_PATH,
                    tls_version=ssl.PROTOCOL_TLSv1_2)

mqtt_client.connect(ENDPOINT, PORT, keepalive=60)
mqtt_client.loop_start()

def read_pms5003():
    while True:
        data = ser.read(32)
        if len(data) == 32 and data[0] == 0x42 and data[1] == 0x4D:
            pm1_0 = int.from_bytes(data[10:12], byteorder='big')
            pm2_5 = int.from_bytes(data[12:14], byteorder='big')
            pm10_0 = int.from_bytes(data[14:16], byteorder='big')

            return {
                "timestamp": datetime.now().isoformat(),
                "pm1.0": pm1_0,
                "pm2.5": pm2_5,
                "pm10.0": pm10_0
            }

try:
    while True:
        sensor_data = read_pms5003()
        payload = json.dumps(sensor_data)
        print("Iren: ", payload)
        mqtt_client.publish(TOPIC, payload)
        time.sleep(60)
except KeyboardInterrupt:
    print("Stop")
finally:
    ser.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
