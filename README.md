# PMS5003 MQTT Sender

This project reads air quality data from a PMS5003 sensor and publishes it to AWS IoT Core using MQTT.

## Project Structure

- `cert/`: Contains AWS certificates and `send_pms_mqtt.py` (not pushed to GitHub).
- `mqtt-env/`: Local Python virtual environment (ignored).
- `.gitignore`: Ensures sensitive files and folders are not pushed.
- `send_pms_mqtt.py`: Main script to read sensor data and publish to MQTT.

## Requirements

- Raspberry Pi with UART enabled
- PMS5003 sensor
- AWS IoT Core certificates

## Setup
Create a virtual environment:
   ```bash
   python3 -m venv mqtt-env
   source mqtt-env/bin/activate
  ```
Install the required libraries
  ```bash
   pip install paho-mqtt pyserial
```

