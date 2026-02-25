# System Architecture

## Table of Contents

- [Overview](#overview)
- [High-Level Architecture](#high-level-architecture)
- [Component Details](#component-details)
  - [ESP32 Device Firmware](#esp32-device-firmware)
  - [MQTT Broker](#mqtt-broker)
  - [Raspberry Pi Gateway & Backend](#raspberry-pi-gateway--backend)
  - [Desktop Application Frontend](#desktop-application-frontend)
- [Data Flow](#data-flow)
- [Communication Protocols](#communication-protocols)
- [ML Inference Pipeline](#ml-inference-pipeline)
- [Future Architecture (TinyML on Device)](#future-architecture-tinyml-on-device)

---

## Overview

MechaPulse is structured as a layered Industrial IoT (IIoT) system with three physical tiers:

| Tier | Hardware | Role |
|------|----------|------|
| Edge  | ESP32 DevKit | Audio capture, pre-processing, MQTT publish |
| Gateway | Raspberry Pi | MQTT subscriber, ML inference, REST API host |
| Application | PC / Server | Streamlit dashboard, model management |

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          INDUSTRIAL FLOOR                            │
│                                                                      │
│  ┌────────────┐  PCM Audio   ┌──────────────────────────────────┐   │
│  │  Machine   │─────────────▶│           ESP32 Node             │   │
│  │ (Rotating  │              │  ┌────────────────────────────┐  │   │
│  │ Machinery) │              │  │  Microphone / I2S Input    │  │   │
│  └────────────┘              │  ├────────────────────────────┤  │   │
│                              │  │  Feature Extraction (FFT)  │  │   │
│                              │  ├────────────────────────────┤  │   │
│                              │  │  WiFi + MQTT Client        │  │   │
│                              │  └────────────────┬───────────┘  │   │
│                              └───────────────────┼──────────────┘   │
└──────────────────────────────────────────────────┼──────────────────┘
                                                    │ MQTT (TCP/IP)
                                         ┌──────────▼──────────┐
                                         │    MQTT Broker       │
                                         │  (Mosquitto / any)   │
                                         └──────────┬──────────┘
                                                    │ MQTT Subscribe
                                         ┌──────────▼──────────────────┐
                                         │       Raspberry Pi           │
                                         │  ┌─────────────────────────┐ │
                                         │  │   MQTT Subscriber       │ │
                                         │  ├─────────────────────────┤ │
                                         │  │   ML Model (scikit-     │ │
                                         │  │   learn .pkl)           │ │
                                         │  ├─────────────────────────┤ │
                                         │  │   FastAPI REST Server   │ │
                                         │  └──────────┬──────────────┘ │
                                         └─────────────┼────────────────┘
                                                        │ HTTP / REST
                                         ┌─────────────▼───────────────┐
                                         │    Desktop Application       │
                                         │  ┌─────────────────────────┐ │
                                         │  │  Streamlit Frontend     │ │
                                         │  │  Train | Test | Predict │ │
                                         │  └─────────────────────────┘ │
                                         └─────────────────────────────┘
```

---

## Component Details

### ESP32 Device Firmware

**Location:** `device-firmware/`  
**Language:** C++ (Arduino framework, PlatformIO)  
**Key Libraries:** `WiFi`, `PubSubClient`, `ArduinoJson`

Responsibilities:
- Establish a WiFi connection to the local network.
- Connect to the MQTT broker using credentials.
- Continuously capture sensor readings (audio features or raw sensor values).
- Serialize data as a JSON payload and publish to an MQTT topic (e.g., `esp/test`).
- Handle reconnection logic on network or broker failure.

Key configuration (in `src/main.cpp`):

| Parameter | Description |
|-----------|-------------|
| `ssid` | WiFi network name |
| `password` | WiFi network password |
| `mqttServer` | IP address of the MQTT broker |
| `mqttPort` | MQTT broker port (default `1883`) |
| `mqttUser` / `mqttPassword` | MQTT broker credentials |

---

### MQTT Broker

**Protocol:** MQTT v3.1.1  
**Default Port:** 1883  
**Recommended Implementation:** Eclipse Mosquitto

The broker acts as the message hub, decoupling the edge devices from the backend processing layer. Each ESP32 node publishes telemetry to a dedicated topic. The Raspberry Pi subscribes to these topics.

Recommended topic convention:

```
mechapulse/<device_id>/telemetry      # sensor data payload
mechapulse/<device_id>/status         # heartbeat / connection status
```

---

### Raspberry Pi Gateway & Backend

**Location:** `desktop-app/backend/`  
**Language:** Python 3  
**Framework:** FastAPI + Uvicorn  
**Port:** 8000

Two server variants are provided:

| File | Description |
|------|-------------|
| `backend/main.py` | Lightweight server – accepts pre-computed feature vectors via HTTP POST and returns predictions. |
| `backend/api/app.py` | Full-featured server – also provides `/start-recording` and `/stop-recording` endpoints that capture audio locally, extract features, and run inference. |

Both servers load the trained scikit-learn model from `trained_models/machine_failure_detection_model3.pkl` at startup.

**Input feature vector:**

| Feature | Type | Description |
|---------|------|-------------|
| `RMS` | float | Root Mean Square of the audio signal |
| `Mean` | float | Mean absolute amplitude |
| `MA1` | float | Highest FFT magnitude |
| `MA2` | float | Second highest FFT magnitude |
| `MA3` | float | Third highest FFT magnitude |
| `F1` | float | Frequency of MA1 (Hz) |
| `F2` | float | Frequency of MA2 (Hz) |
| `F3` | float | Frequency of MA3 (Hz) |

---

### Desktop Application Frontend

**Location:** `desktop-app/frontend/`  
**Language:** Python 3  
**Framework:** Streamlit  
**Port:** 8501

Multi-page Streamlit application:

| Page | File | Description |
|------|------|-------------|
| Home | `main.py` | Navigation hub |
| Train | `pages/1_Train.py` | Upload CSV data and select a model type to train |
| Test | `pages/2_Test.py` | Upload test data and evaluate a trained model |
| Validate | `pages/3_Validate.py` | Upload validation data and measure model accuracy |
| Predict | `pages/4_Predict.py` | Upload CSV or WAV file for live fault prediction |

---

## Data Flow

```
1. ESP32 captures audio samples from the machine microphone.
2. ESP32 performs basic feature extraction (RMS, Mean, FFT peaks, peak frequencies).
3. Feature vector is serialized to JSON and published to MQTT topic.
4. MQTT Broker relays message to all subscribers.
5. Raspberry Pi (MQTT subscriber) receives the feature vector.
6. Raspberry Pi passes features to the FastAPI /predict endpoint.
7. Loaded scikit-learn model performs binary classification (fault / no-fault).
8. Prediction result is returned as JSON to the calling client.
9. Streamlit dashboard displays the result and history.
```

---

## Communication Protocols

| Link | Protocol | Transport | Notes |
|------|----------|-----------|-------|
| ESP32 → MQTT Broker | MQTT v3.1.1 | TCP/IP (WiFi) | QoS 0, JSON payload |
| MQTT Broker → Raspberry Pi | MQTT v3.1.1 | TCP/IP (LAN) | Subscribe |
| Raspberry Pi → Desktop App | HTTP REST | TCP/IP (LAN) | FastAPI / JSON |
| Desktop App → Backend | HTTP REST | localhost | Streamlit → FastAPI |

---

## ML Inference Pipeline

```
Raw Audio (WAV, 48 kHz, mono)
        │
        ▼
┌───────────────────┐
│  Signal Analysis  │
│  - RMS            │
│  - Mean Amplitude │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  FFT Analysis     │
│  - Compute FFT    │
│  - Top 3 peaks    │
│  - Peak freqs     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Feature Vector   │
│  [RMS, Mean,      │
│   MA1, MA2, MA3,  │
│   F1, F2, F3]     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  scikit-learn     │
│  Classifier       │
│  (.pkl model)     │
└────────┬──────────┘
         │
         ▼
  Prediction Label
  (0 = Normal, 1 = Fault)
```

---

## Future Architecture (TinyML on Device)

In the next development phase, the ML inference model will be converted to TensorFlow Lite and deployed directly onto the ESP32. The Raspberry Pi will act purely as a protocol gateway, forwarding predictions (rather than raw features) to a cloud-based dashboard.

```
ESP32 (TinyML inference)  →  MQTT  →  Raspberry Pi (gateway)  →  Cloud Dashboard
```

Benefits:
- Reduced latency (inference at the edge).
- Lower bandwidth usage (predictions sent, not raw audio).
- Works without constant internet connectivity.
