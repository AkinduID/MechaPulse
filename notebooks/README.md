# ML Notebooks

The `notebooks/` directory contains Jupyter notebooks that cover the full machine learning development lifecycle for MechaPulse — from raw data collection through model training, evaluation, and export.

---

## Table of Contents

- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Notebooks](#notebooks)
  - [data_collection.ipynb](#data_collectionipynb)
  - [anomaly_detection.ipynb](#anomaly_detectionipynb)
  - [failure_classification.ipynb](#failure_classificationipynb)
  - [machine_failure_prediction.ipynb](#machine_failure_predictionipynb)
- [Datasets](#datasets)
- [Feature Schema](#feature-schema)
- [Running the Notebooks](#running-the-notebooks)

---

## Directory Structure

```
notebooks/
├── data_collection.ipynb             # Record audio and build labelled CSV datasets
├── anomaly_detection.ipynb           # Unsupervised anomaly detection
├── failure_classification.ipynb      # Multi-class fault classification
├── machine_failure_prediction.ipynb  # Binary failure prediction (production model)
├── assets/
│   ├── images/                       # Result plots and diagrams
│   │   ├── good_.png
│   │   ├── mfault1_.png
│   │   ├── mfault2.png
│   │   └── off.png
│   └── audio-samples/                # Reference audio samples
└── data/
    ├── anomaly_detection_training.csv
    ├── failure_classification_training.csv
    ├── failure_classification_training_v2.csv
    └── sdcard_failure_classification.csv
```

---

## Prerequisites

```bash
pip install jupyter notebook \
            scikit-learn pandas numpy \
            matplotlib seaborn scipy
```

---

## Notebooks

### `data_collection.ipynb`

**Purpose:** Record audio samples from machines and build labelled CSV training datasets.

**Workflow:**
1. Set the machine state label (e.g., `0` = normal, `1` = fault).
2. Execute the recording cell — a 5-second audio window is captured from the local microphone.
3. Statistical (`RMS`, `Mean`) and spectral (`MA1–3`, `F1–3`) features are extracted using FFT.
4. A new row is appended to the target CSV file.
5. Repeat for each machine state to accumulate a balanced dataset.

**Output:** Rows appended to one of the CSV files in `data/`.

---

### `anomaly_detection.ipynb`

**Purpose:** Train and evaluate an unsupervised anomaly detection model. Only normal-state data is used for training; any sample that deviates significantly from the learnt distribution is flagged as anomalous.

**Workflow:**
1. Load `data/anomaly_detection_training.csv`.
2. Normalize features.
3. Fit an anomaly detector (e.g., Isolation Forest or One-Class SVM).
4. Evaluate detection performance on a held-out set containing both normal and fault samples.
5. Visualise decision boundary and anomaly scores.

**Use case:** Useful when labelled fault data is scarce or unavailable.

---

### `failure_classification.ipynb`

**Purpose:** Train a multi-class classifier to distinguish between different fault types (e.g., bearing failure, shaft imbalance, looseness).

**Workflow:**
1. Load `data/failure_classification_training.csv` (or `_v2`).
2. Explore class distributions and feature correlations.
3. Train and compare candidate classifiers (Random Forest, SVM, Logistic Regression).
4. Evaluate with confusion matrix, precision, recall, and F1-score per class.
5. Export the best model.

**Output:** Serialized `.pkl` model for multi-class fault identification.

---

### `machine_failure_prediction.ipynb`

**Purpose:** Develop the **binary failure prediction** model deployed in the FastAPI production server.

**Workflow:**
1. Load and merge labelled datasets.
2. Perform feature selection and engineering.
3. Stratified train/test split.
4. Hyperparameter tuning via cross-validation.
5. Final evaluation: accuracy, ROC-AUC, F1-score.
6. Serialize the best model to `desktop-app/trained_models/machine_failure_detection_model3.pkl`.

**Output:** `desktop-app/trained_models/machine_failure_detection_model3.pkl` — loaded by the FastAPI server at startup.

---

## Datasets

All datasets in `data/` use the following CSV format:

```
RMS,Mean,MA1,MA2,MA3,F1,F2,F3,label
```

| File | Rows (approx.) | Labels | Notes |
|------|----------------|--------|-------|
| `anomaly_detection_training.csv` | varies | None | Normal-state samples only |
| `failure_classification_training.csv` | varies | Multi-class | Original collection |
| `failure_classification_training_v2.csv` | varies | Multi-class | Expanded / re-labelled |
| `sdcard_failure_classification.csv` | varies | Multi-class | Collected via ESP32 SD card |

---

## Feature Schema

Each row in a dataset corresponds to one 5-second audio window:

| Column | Type | Description |
|--------|------|-------------|
| `RMS` | float | Root Mean Square amplitude |
| `Mean` | float | Mean absolute amplitude |
| `MA1` | float | Dominant FFT magnitude |
| `MA2` | float | 2nd dominant FFT magnitude |
| `MA3` | float | 3rd dominant FFT magnitude |
| `F1` | float | Frequency of MA1 (Hz) |
| `F2` | float | Frequency of MA2 (Hz) |
| `F3` | float | Frequency of MA3 (Hz) |
| `label` | int | `0` = normal · `1` = fault (binary) or fault-type index (multi-class) |

---

## Running the Notebooks

```bash
cd notebooks
jupyter notebook
```

Open any notebook in the Jupyter interface and run all cells from top to bottom (`Kernel → Restart & Run All`).

For batch execution (CI / automated validation):

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```
