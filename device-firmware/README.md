# Device Firmware

The MechaPulse device firmware runs on an **ESP32** microcontroller using the **Arduino framework** and is built with **PlatformIO**. It connects to a WiFi network, publishes sensor telemetry to an MQTT broker, and is the foundation for future TinyML on-device inference.

---

## Table of Contents

- [Directory Structure](#directory-structure)
- [Hardware Requirements](#hardware-requirements)
- [Firmware Overview](#firmware-overview)
- [Configuration](#configuration)
- [Building and Flashing](#building-and-flashing)
- [MQTT Telemetry Format](#mqtt-telemetry-format)
- [Legacy Sketches](#legacy-sketches)
- [Dependencies](#dependencies)
- [Roadmap](#roadmap)

---

## Directory Structure

```
device-firmware/
├── src/
│   └── main.cpp              # Main firmware source
├── include/                  # Project header files
├── lib/                      # Private project libraries
├── legacy-sketches/
│   ├── mqtt/
│   │   └── mqtt.ino          # Basic MQTT publish sketch
│   └── mqttjson/
│       └── mqttjson.ino      # MQTT + JSON publish sketch
├── test/                     # PlatformIO unit tests
└── platformio.ini            # Build configuration
```

---

## Hardware Requirements

| Component | Specification |
|-----------|---------------|
| Microcontroller | ESP32 DevKit (any variant) |
| WiFi | 2.4 GHz 802.11 b/g/n (built-in to ESP32) |
| Microphone | I2S MEMS microphone (for audio capture) |
| Power | 5 V via USB or 3.3 V regulated supply |

---

## Firmware Overview

`src/main.cpp` implements the following behaviour:

1. **`setup()`**  
   - Initialize serial port at 115 200 baud.  
   - Connect to WiFi using the configured SSID and password.  
   - Connect to the MQTT broker with username/password authentication.

2. **`loop()`**  
   - Build a JSON payload containing device ID, sensor type, and sensor values.  
   - Publish the payload to the MQTT topic `esp/test`.  
   - Wait 10 seconds and repeat.

---

## Configuration

Edit the constants at the top of `src/main.cpp` before building:

```cpp
const char* ssid         = "YOUR_WIFI_SSID";
const char* password     = "YOUR_WIFI_PASSWORD";
const char* mqttServer   = "192.168.x.x";      // MQTT broker IP
const int   mqttPort     = 1883;
const char* mqttUser     = "your_mqtt_user";
const char* mqttPassword = "your_mqtt_password";
```

> **Security note:** Never commit real credentials to version control. Use a separate, Git-ignored configuration header in production.

---

## Building and Flashing

### Prerequisites

Install PlatformIO Core:

```bash
uv tool install platformio
```

Or use the [PlatformIO IDE extension for VS Code](https://platformio.org/install/ide?install=vscode).

### Commands

```bash
cd device-firmware

# Compile the firmware
pio run

# Compile and upload to the connected ESP32
pio run --target upload

# Open the serial monitor (115200 baud)
pio device monitor --baud 115200
```

### Expected Serial Output

```
Connected to the WiFi network
Connecting to MQTT...
connected
Sending message to MQTT topic..
{"device":"ESP32","sensorType":"Temperature","values":[20,21,23]}
Success sending message
-------------
```

---

## MQTT Telemetry Format

The firmware publishes JSON messages to the topic `esp/test`:

```json
{
  "device": "ESP32",
  "sensorType": "Temperature",
  "values": [20, 21, 23]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `device` | string | Device identifier |
| `sensorType` | string | Type of sensor data |
| `values` | array of numbers | Sensor readings |

Future firmware versions will replace `values` with the 8-element audio feature vector (`RMS`, `Mean`, `MA1–3`, `F1–3`) used by the ML model.

---

## Legacy Sketches

The `legacy-sketches/` directory contains earlier Arduino `.ino` prototypes used during initial development:

| Sketch | Description |
|--------|-------------|
| `mqtt/mqtt.ino` | Connects to WiFi and MQTT, then continuously publishes temperature and humidity readings. |
| `mqttjson/mqttjson.ino` | Same as above but serializes data as a JSON object using ArduinoJson. |

These sketches are retained for historical reference and are not part of the active build.

---

## Dependencies

Declared in `platformio.ini` and resolved automatically by PlatformIO:

| Library | Purpose |
|---------|---------|
| `WiFi` (built-in ESP32) | WiFi connectivity |
| `PubSubClient` | MQTT client |
| `ArduinoJson` | JSON serialization/deserialization |

---

## Roadmap

| Feature | Status |
|---------|--------|
| WiFi + MQTT telemetry | ✅ Complete |
| Audio capture (I2S microphone) | 🔄 In progress |
| On-device FFT feature extraction | 🔄 In progress |
| TinyML inference (TensorFlow Lite) | 📋 Planned |
| SD card logging | 📋 Planned |
| OTA firmware updates | 📋 Planned |
