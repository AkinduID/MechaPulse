# Setup Guide

This guide walks you through setting up every component of MechaPulse from scratch.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Repository Setup](#repository-setup)
- [Desktop Application Setup](#desktop-application-setup)
  - [Python Environment](#python-environment)
  - [Backend API Server](#backend-api-server)
  - [Frontend Streamlit App](#frontend-streamlit-app)
- [Device Firmware Setup](#device-firmware-setup)
  - [PlatformIO Installation](#platformio-installation)
  - [Configure Credentials](#configure-credentials)
  - [Build and Flash](#build-and-flash)
- [MQTT Broker Setup](#mqtt-broker-setup)
- [ML Notebooks Setup](#ml-notebooks-setup)
- [Configuration Reference](#configuration-reference)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | ≥ 3.9 | Backend API, Streamlit frontend, notebooks |
| pip | latest | Python package management |
| PlatformIO Core (CLI) | latest | ESP32 firmware build & flash |
| Mosquitto (or any MQTT broker) | any | Message broker for device telemetry |
| Git | any | Cloning the repository |

Optional but recommended:
- **VS Code** with the PlatformIO and Python extensions for firmware and backend development.
- **Jupyter** for running the ML development notebooks.

---

## Repository Setup

```bash
git clone https://github.com/AkinduID/MechaPulse.git
cd MechaPulse
```

---

## Desktop Application Setup

### Python Environment

It is strongly recommended to use a virtual environment to isolate dependencies.

```bash
cd desktop-app

python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate.bat     # Windows (cmd)
# .venv\Scripts\Activate.ps1     # Windows (PowerShell)
```

Install all required packages:

```bash
pip install fastapi uvicorn pydantic \
            numpy pandas scikit-learn \
            streamlit \
            sounddevice soundfile scipy
```

| Package | Purpose |
|---------|---------|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server for FastAPI |
| `pydantic` | Request body validation |
| `numpy` | Numerical computing |
| `pandas` | Data manipulation |
| `scikit-learn` | ML model loading and inference |
| `streamlit` | Frontend dashboard |
| `sounddevice` | Audio capture (full-featured server) |
| `soundfile` | WAV file I/O |
| `scipy` | FFT computation |

### Backend API Server

The lightweight server (`backend/main.py`) accepts pre-computed feature vectors:

```bash
# From the desktop-app directory
python backend/main.py
# API available at http://localhost:8000
```

The full-featured server (`backend/api/app.py`) additionally supports local audio recording:

```bash
python -m uvicorn backend.api.app:app --reload --port 8000
```

Verify the server is running:

```bash
curl http://localhost:8000/
# Expected: {"msg":"Machine Failure Predictor"}
```

### Frontend Streamlit App

```bash
# From the desktop-app directory
streamlit run frontend/main.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`.

---

## Device Firmware Setup

### PlatformIO Installation

Install PlatformIO Core:

```bash
pip install platformio
```

Or install the [PlatformIO VS Code extension](https://platformio.org/install/ide?install=vscode).

### Configure Credentials

Open `device-firmware/src/main.cpp` and update the following constants with your environment values:

```cpp
const char* ssid       = "YOUR_WIFI_SSID";
const char* password   = "YOUR_WIFI_PASSWORD";
const char* mqttServer = "192.168.x.x";     // IP of your MQTT broker
const int   mqttPort   = 1883;
const char* mqttUser   = "your_mqtt_user";
const char* mqttPassword = "your_mqtt_pass";
```

> **Security note:** Do not commit real credentials to version control. Consider using a configuration header file excluded from Git, or environment-based injection for production deployments.

### Build and Flash

Connect the ESP32 via USB, then:

```bash
cd device-firmware

# Build only
pio run

# Build and upload to the connected board
pio run --target upload

# Open serial monitor (115200 baud)
pio device monitor --baud 115200
```

Expected serial output once connected:

```
Connected to the WiFi network
Connecting to MQTT...
connected
Sending message to MQTT topic..
{"device":"ESP32","sensorType":"Temperature","values":[20,21,23]}
Success sending message
```

---

## MQTT Broker Setup

### Mosquitto (recommended)

**Linux (Debian/Ubuntu):**

```bash
sudo apt-get update && sudo apt-get install -y mosquitto mosquitto-clients

# Create a password file
sudo mosquitto_passwd -c /etc/mosquitto/passwd <username>

# Edit /etc/mosquitto/mosquitto.conf and add:
# listener 1883
# allow_anonymous false
# password_file /etc/mosquitto/passwd

sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

**Verify the broker:**

```bash
# Subscribe in one terminal
mosquitto_sub -h localhost -t "esp/test" -u <username> -P <password>

# Publish a test message in another
mosquitto_pub -h localhost -t "esp/test" -m "hello" -u <username> -P <password>
```

---

## ML Notebooks Setup

```bash
cd notebooks

python -m venv .venv
source .venv/bin/activate

pip install jupyter notebook \
            scikit-learn pandas numpy \
            matplotlib seaborn scipy

jupyter notebook
```

Open any of the following notebooks in the Jupyter interface:

| Notebook | Description |
|----------|-------------|
| `data_collection.ipynb` | Record or import raw audio, label samples |
| `anomaly_detection.ipynb` | Train and evaluate an unsupervised anomaly detector |
| `failure_classification.ipynb` | Multi-class fault classification model development |
| `machine_failure_prediction.ipynb` | Binary failure prediction model (exported to `.pkl`) |

---

## Configuration Reference

### Backend (`backend/main.py` / `backend/api/app.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| Port | `8000` | Uvicorn listen port |
| Model path | `../trained_models/machine_failure_detection_model3.pkl` | Path to the serialized model |
| Sample rate | `48000` Hz | Audio recording sample rate (full server only) |
| Duration | `5` seconds | Recording window length (full server only) |

### Firmware (`device-firmware/src/main.cpp`)

| Constant | Default | Description |
|----------|---------|-------------|
| `mqttPort` | `1883` | MQTT broker port |
| `delay(10000)` | 10 000 ms | Interval between telemetry publishes |

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| `ModuleNotFoundError: sounddevice` | Package not installed | `pip install sounddevice soundfile` |
| Model file not found | Wrong working directory | Run from the `desktop-app` directory |
| ESP32 not connecting to WiFi | Incorrect credentials | Double-check `ssid` / `password` in `main.cpp` |
| MQTT connection refused | Broker not running or wrong IP | Start the broker; verify `mqttServer` IP |
| Streamlit page not loading | Frontend not started | Run `streamlit run frontend/main.py` |
| `422 Unprocessable Entity` from API | Missing or wrong-type fields | Ensure all 8 float fields are present in the request body |
