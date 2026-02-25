# Desktop Application

The MechaPulse desktop application is a two-tier service consisting of:

- A **FastAPI** backend that loads the trained ML model and exposes a REST API for fault prediction.
- A **Streamlit** frontend that provides a graphical interface for model training, testing, validation, and live prediction.

---

## Table of Contents

- [Directory Structure](#directory-structure)
- [Backend](#backend)
  - [Running the Backend](#running-the-backend)
  - [Endpoints Summary](#endpoints-summary)
  - [Trained Models](#trained-models)
- [Frontend](#frontend)
  - [Running the Frontend](#running-the-frontend)
  - [Pages](#pages)
- [Dependencies](#dependencies)

---

## Directory Structure

```
desktop-app/
├── backend/
│   ├── main.py          # Lightweight prediction API
│   └── api/
│       └── app.py       # Full-featured API with audio recording
├── frontend/
│   ├── main.py          # Streamlit entry point & navigation
│   └── pages/
│       ├── 1_Train.py   # Model training page
│       ├── 2_Test.py    # Model testing page
│       ├── 3_Validate.py# Model validation page
│       └── 4_Predict.py # Live prediction page
└── trained_models/
    ├── machine_failure_detection_model.pkl
    └── machine_failure_detection_model3.pkl
```

---

## Backend

### Running the Backend

**Lightweight server** (accepts pre-computed feature vectors):

```bash
cd desktop-app
python backend/main.py
```

**Full-featured server** (also supports local microphone recording):

```bash
cd desktop-app
python -m uvicorn backend.api.app:app --reload --port 8000
```

Both servers listen on port `8000` by default.

### Endpoints Summary

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/predict` | Predict machine failure from feature vector |
| `POST` | `/start-recording` | Start microphone capture loop and return prediction |
| `POST` | `/stop-recording` | Stop the recording loop |
| `POST` | `/receive-request` | Acknowledge an incoming alert from an edge device |

See [`docs/API_REFERENCE.md`](../docs/API_REFERENCE.md) for full request/response details.

### Trained Models

Serialized scikit-learn models are stored in `trained_models/`:

| File | Notes |
|------|-------|
| `machine_failure_detection_model.pkl` | Earlier prototype model |
| `machine_failure_detection_model3.pkl` | Current production model (loaded by default) |

The model path is resolved relative to the server file at startup, so the servers must be launched from the `desktop-app` directory.

---

## Frontend

### Running the Frontend

```bash
cd desktop-app
streamlit run frontend/main.py
```

The app opens automatically at `http://localhost:8501`. Use the left sidebar to navigate between pages.

### Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Welcome screen and navigation instructions |
| Train | `1_Train` | Upload a CSV training dataset and select a model type to train |
| Test | `2_Test` | Upload a CSV test dataset and evaluate a trained model |
| Validate | `3_Validate` | Upload a CSV validation dataset and measure model accuracy |
| Predict | `4_Predict` | Upload a CSV or WAV file to receive a fault prediction |

---

## Dependencies

Install all required packages from the `desktop-app` directory:

```bash
pip install fastapi uvicorn pydantic \
            numpy pandas scikit-learn \
            streamlit \
            sounddevice soundfile scipy
```

| Package | Version Constraint | Purpose |
|---------|--------------------|---------|
| `fastapi` | any | REST API framework |
| `uvicorn` | any | ASGI server |
| `pydantic` | any | Data validation |
| `numpy` | any | Numerical operations |
| `pandas` | any | DataFrame construction for inference |
| `scikit-learn` | any | Model deserialization and prediction |
| `streamlit` | any | Web-based UI |
| `sounddevice` | any | Local audio capture |
| `soundfile` | any | WAV file I/O |
| `scipy` | any | FFT computation |
