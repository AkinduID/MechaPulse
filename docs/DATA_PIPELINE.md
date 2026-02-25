# Data Pipeline

This document describes how raw audio data is collected, processed, and used to train and serve the machine failure prediction models in MechaPulse.

## Table of Contents

- [Overview](#overview)
- [Data Collection](#data-collection)
  - [Audio Capture](#audio-capture)
  - [Available Datasets](#available-datasets)
- [Feature Engineering](#feature-engineering)
- [Model Development Notebooks](#model-development-notebooks)
  - [1. Data Collection](#1-data-collection)
  - [2. Anomaly Detection](#2-anomaly-detection)
  - [3. Failure Classification](#3-failure-classification)
  - [4. Machine Failure Prediction](#4-machine-failure-prediction)
- [Model Training](#model-training)
- [Model Serialization](#model-serialization)
- [Model Serving](#model-serving)
- [Dataset Schema](#dataset-schema)

---

## Overview

```
Raw Audio → Feature Extraction → Labelled Dataset → Model Training → Serialized Model → REST API
```

The pipeline follows a classical supervised learning workflow:

1. Audio samples are recorded from machines in different states (normal / fault conditions).
2. Statistical and spectral features are extracted from each sample.
3. Features and labels are saved as CSV datasets.
4. Jupyter notebooks develop and evaluate candidate models.
5. The best model is serialized to a `.pkl` file.
6. The FastAPI backend loads the `.pkl` file and serves predictions via HTTP.

---

## Data Collection

### Audio Capture

Audio is captured in two ways depending on the deployment stage:

| Method | Where | Details |
|--------|-------|---------|
| Desktop microphone | Raspberry Pi / PC | `sounddevice` library, 48 kHz, mono, 5-second windows |
| SD card logging | ESP32 (future) | Raw WAV files saved to SD card for offline labelling |

Each recording session produces a 5-second WAV file (`test.wav`) that is immediately processed for features.

### Available Datasets

All datasets are stored in `notebooks/data/`:

| File | Description | Target |
|------|-------------|--------|
| `anomaly_detection_training.csv` | Unlabelled samples for unsupervised anomaly detection | — |
| `failure_classification_training.csv` | Multi-class labelled samples (fault types) | Fault class label |
| `failure_classification_training_v2.csv` | Updated multi-class dataset | Fault class label |
| `sdcard_failure_classification.csv` | Samples collected via SD card on ESP32 | Fault class label |

---

## Feature Engineering

Each 5-second audio window is transformed into an 8-dimensional feature vector:

| Feature | Formula | Description |
|---------|---------|-------------|
| `RMS` | `√(mean(x²))` | Energy of the signal |
| `Mean` | `mean(|x|)` | Mean absolute amplitude |
| `MA1` | `max(|FFT|)` | Dominant frequency amplitude |
| `MA2` | `second_max(|FFT|)` | Second dominant frequency amplitude |
| `MA3` | `third_max(|FFT|)` | Third dominant frequency amplitude |
| `F1` | `freq[argmax(|FFT|)]` | Dominant frequency (Hz) |
| `F2` | `freq[arg_second_max(|FFT|)]` | Second dominant frequency (Hz) |
| `F3` | `freq[arg_third_max(|FFT|)]` | Third dominant frequency (Hz) |

**FFT computation:**

```python
import scipy.fftpack as fftpk
import numpy as np

FFT_full = abs(fftpk.fft(signal))
FFT = FFT_full[range(len(FFT_full) // 2)]          # one-sided spectrum
freqs = fftpk.fftfreq(len(FFT), 1.0 / s_rate)[range(len(FFT_full) // 2)]

sorted_FFT = np.sort(FFT)[::-1]
ma1, ma2, ma3 = sorted_FFT[[0, 1, 2]]
f1, f2, f3 = freqs[[np.where(FFT == ma1)[0],
                    np.where(FFT == ma2)[0],
                    np.where(FFT == ma3)[0]]]
```

---

## Model Development Notebooks

### 1. Data Collection

**File:** `notebooks/data_collection.ipynb`

Records audio samples, extracts features, assigns labels, and appends rows to a CSV training file.

Workflow:
1. Configure machine state label (e.g., `0` for normal, `1` for fault).
2. Run the recording cell to capture a 5-second window.
3. Features are extracted and a new row is appended to the target CSV.
4. Repeat for each machine state to build a balanced dataset.

### 2. Anomaly Detection

**File:** `notebooks/anomaly_detection.ipynb`

Trains an unsupervised anomaly detection model (e.g., Isolation Forest, One-Class SVM) on normal-state data only. Any sample deviating significantly from the normal distribution is flagged as an anomaly.

Workflow:
1. Load `anomaly_detection_training.csv`.
2. Normalize features.
3. Train and tune the anomaly detector.
4. Evaluate on held-out normal and fault samples.

### 3. Failure Classification

**File:** `notebooks/failure_classification.ipynb`

Trains a multi-class classifier to distinguish between different fault types (e.g., bearing failure, imbalance, looseness).

Workflow:
1. Load `failure_classification_training.csv` or `v2`.
2. Explore class distributions and feature correlations.
3. Train candidate models (Random Forest, SVM, Logistic Regression).
4. Evaluate with confusion matrix, precision, recall, F1-score.
5. Export best model to `.pkl`.

### 4. Machine Failure Prediction

**File:** `notebooks/machine_failure_prediction.ipynb`

Trains the primary **binary classifier** (normal vs. any fault) that is deployed in the production FastAPI server.

Workflow:
1. Load and merge labelled datasets.
2. Feature selection and engineering.
3. Train / test split (stratified).
4. Hyperparameter tuning.
5. Final evaluation (ROC-AUC, accuracy, F1).
6. Serialize to `desktop-app/trained_models/machine_failure_detection_model3.pkl`.

---

## Model Training

Supported model types (selectable in the Streamlit Train page and notebooks):

| Model | Library | Notes |
|-------|---------|-------|
| Random Forest | `sklearn.ensemble.RandomForestClassifier` | Default production model |
| SVM | `sklearn.svm.SVC` | Effective on small datasets |
| Logistic Regression | `sklearn.linear_model.LogisticRegression` | Baseline |

Training data format (CSV, header required):

```
RMS,Mean,MA1,MA2,MA3,F1,F2,F3,label
120.4,98.1,5430,3210,1890,440,880,1320,0
...
```

---

## Model Serialization

Trained models are serialized with Python's `pickle` module:

```python
import pickle

# Save
with open("machine_failure_detection_model3.pkl", "wb") as f:
    pickle.dump(model, f)

# Load (done by the API server at startup)
model = pickle.load(open("machine_failure_detection_model3.pkl", "rb"))
```

Serialized models are stored in `desktop-app/trained_models/`.

| File | Description |
|------|-------------|
| `machine_failure_detection_model.pkl` | Earlier iteration |
| `machine_failure_detection_model3.pkl` | Current production model |

---

## Model Serving

At FastAPI server startup, the model is loaded into memory:

```python
import pickle, os

_model_path = os.path.join(os.path.dirname(__file__),
                           "..", "trained_models",
                           "machine_failure_detection_model3.pkl")
model = pickle.load(open(_model_path, "rb"))
```

At inference time, the 8-feature vector from the request body is converted to a `pandas.DataFrame` and passed to `model.predict()`:

```python
data_df = pd.DataFrame([input.dict()])
prediction = model.predict([data_df.iloc[0]])
return {"prediction": int(prediction[0])}
```

See [`docs/API_REFERENCE.md`](API_REFERENCE.md) for the full endpoint contract.
