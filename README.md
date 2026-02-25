# MechaPulse

<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/></a>
<a href="https://isocpp.org/"><img src="https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white"/></a>
<a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white"/></a>
<a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white"/></a>
<a href="https://www.raspberrypi.org/"><img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat&logo=raspberry-pi&logoColor=white"/></a>
<a href="https://www.espressif.com/en/products/socs/esp32"><img src="https://img.shields.io/badge/ESP32-000000?style=flat&logo=espressif&logoColor=white"/></a>
<a href="https://code.visualstudio.com/"><img src="https://img.shields.io/badge/VS%20Code-007ACC?style=flat&logo=visual-studio-code&logoColor=white"/></a>
<a href="https://jupyter.org/"><img src="https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white"/></a>

> **Industrial IoT platform for sound-based machine fault detection using TinyML.**

---

## Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Components](#components)
- [Documentation](#documentation)
- [License](#license)

---

## Project Overview

MechaPulse is an Industrial IoT system that uses acoustic (sound) analysis to detect faults in rotating machinery in real time. An array of ESP32 embedded devices is deployed across industrial machines; each device continuously monitors machine sound and applies a TinyML inference model to predict potential faults. Alerts and sensor data are forwarded to a central dashboard for fleet-wide monitoring.

### Current Prototype

The current prototype demonstrates the full end-to-end pipeline:

1. An **ESP32** module records audio from a machine and publishes sensor data over **MQTT**.
2. A **Raspberry Pi** (gateway) receives the data, runs the ML inference model, and exposes results via a **FastAPI** REST API.
3. A **Streamlit** desktop application provides a graphical interface for model training, testing, validation, and live prediction.

### Roadmap

The next stage of the prototype will move ML inference directly onto the ESP32 (TinyML), with the Raspberry Pi serving only as a protocol gateway to a cloud-based dashboard.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Industrial Floor                         │
│                                                                 │
│  ┌──────────┐   Audio    ┌──────────────┐   MQTT   ┌─────────┐ │
│  │ Machine  │──────────▶│    ESP32     │─────────▶│  MQTT   │ │
│  │(Rotating │           │  (Firmware)  │          │ Broker  │ │
│  │Machinery)│           │  WiFi + Mic  │          └────┬────┘ │
│  └──────────┘           └──────────────┘               │      │
└───────────────────────────────────────────────────────────────-┘
                                                          │ MQTT
                                               ┌──────────▼──────────┐
                                               │    Raspberry Pi      │
                                               │  (Gateway / Server)  │
                                               │  FastAPI  |  ML Model│
                                               └──────────┬──────────┘
                                                          │ REST API
                                               ┌──────────▼──────────┐
                                               │  Desktop Application │
                                               │  Streamlit Frontend  │
                                               └─────────────────────┘
```

For detailed architecture documentation see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## Repository Structure

```
MechaPulse/
├── desktop-app/                  # Desktop monitoring & ML application
│   ├── backend/                  # FastAPI inference server
│   │   ├── api/app.py            # Full API with audio recording + ML inference
│   │   └── main.py               # Lightweight prediction-only API
│   ├── frontend/                 # Streamlit multi-page web UI
│   │   ├── main.py               # App entry point & navigation
│   │   └── pages/                # Individual workflow pages
│   │       ├── 1_Train.py        # Model training interface
│   │       ├── 2_Test.py         # Model testing interface
│   │       ├── 3_Validate.py     # Model validation interface
│   │       └── 4_Predict.py      # Live prediction interface
│   └── trained_models/           # Serialised scikit-learn models (.pkl)
├── device-firmware/              # ESP32 embedded firmware (PlatformIO)
│   ├── src/main.cpp              # Main firmware source
│   ├── include/                  # Project header files
│   ├── lib/                      # Private project libraries
│   ├── legacy-sketches/          # Earlier Arduino prototype sketches
│   │   ├── mqtt/                 # Basic MQTT publish sketch
│   │   └── mqttjson/             # MQTT + JSON publish sketch
│   └── platformio.ini            # PlatformIO build configuration
├── notebooks/                    # Jupyter notebooks for ML development
│   ├── anomaly_detection.ipynb          # Unsupervised anomaly detection
│   ├── data_collection.ipynb            # Raw data capture & labelling
│   ├── failure_classification.ipynb     # Multi-class fault classification
│   ├── machine_failure_prediction.ipynb # Binary failure prediction
│   ├── assets/                          # Images & audio samples
│   └── data/                            # Training & validation CSV datasets
├── docs/                         # Detailed technical documentation
│   ├── ARCHITECTURE.md           # System architecture
│   ├── API_REFERENCE.md          # REST API reference
│   ├── SETUP_GUIDE.md            # Installation & configuration
│   ├── DATA_PIPELINE.md          # Data & ML pipeline
│   └── CONTRIBUTING.md           # Contribution guidelines
└── README.md                     # This file
```

---

## Quick Start

### Prerequisites

| Component | Requirement |
|-----------|-------------|
| Python    | ≥ 3.9       |
| PlatformIO CLI | latest |
| MQTT Broker (Mosquitto) | any version |
| ESP32 DevKit | any variant |

### 1 — Clone the repository

```bash
git clone https://github.com/AkinduID/MechaPulse.git
cd MechaPulse
```

### 2 — Set up the Desktop Application

```bash
cd desktop-app

# Install Python dependencies
pip install fastapi uvicorn pydantic numpy pandas scikit-learn \
            streamlit sounddevice soundfile scipy

# Start the backend API server
python backend/main.py          # runs on http://localhost:8000

# In a separate terminal, start the Streamlit frontend
streamlit run frontend/main.py  # runs on http://localhost:8501
```

### 3 — Flash the ESP32 Firmware

```bash
cd device-firmware

# Edit WiFi & MQTT credentials in src/main.cpp, then build & upload
pio run --target upload
```

### 4 — Run the ML Notebooks

```bash
cd notebooks
pip install jupyter scikit-learn pandas numpy matplotlib scipy
jupyter notebook
```

See [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md) for full environment setup and configuration options.

---

## Components

| Component | Technology | Description |
|-----------|-----------|-------------|
| [Desktop App](desktop-app/README.md) | FastAPI · Streamlit | Backend inference API and ML management UI |
| [Device Firmware](device-firmware/README.md) | C++ · Arduino · PlatformIO | ESP32 audio capture and MQTT telemetry |
| [ML Notebooks](notebooks/README.md) | Python · Jupyter · scikit-learn | Model development, training and evaluation |

---

## Documentation

| Document | Description |
|----------|-------------|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | End-to-end system architecture |
| [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) | REST API endpoint reference |
| [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md) | Installation & configuration guide |
| [`docs/DATA_PIPELINE.md`](docs/DATA_PIPELINE.md) | Data collection & ML pipeline |
| [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) | How to contribute |

---

## License

This project is maintained by the MechaPulse team. See repository settings for license details.
