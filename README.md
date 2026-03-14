# Leukemia Subtype Classifier — Fall 2025 AI Project

A machine learning pipeline for classifying leukemia subtypes (ALL, AML, CLL, CML, Healthy) using transfer learning and deep autoencoders trained on gene expression data.

---

## Project Overview

This project uses a two-stage approach:
1. **Pretraining** — A deep autoencoder is pretrained on ~10,000 TCGA pan-cancer samples to learn general gene expression representations
2. **Fine-tuning** — The encoder is fine-tuned on GSE13159 leukemia data to compress ~22,000 genes into a 64-dimensional latent space
3. **Classification** — MLP and XGBoost classifiers are trained on the latent features to predict leukemia subtypes

---

## Dataset & Models (HuggingFace)

The raw and processed datasets are hosted on HuggingFace (too large for GitHub):

- **Models**: [Samzzh/leukemia_classifier_project_models](https://huggingface.co/Samzzh/leukemia_classifier_project_models/tree/main)
- **Datasets**: [Samzzh/leukemia_classifier_project_datasets](https://huggingface.co/datasets/Samzzh/leukemia_classifier_project_datasets)

See [HUGGINGFACE_LINKS.md](HUGGINGFACE_LINKS.md) for full details and download instructions.

---

## Project Structure

```
leukemia_classifier_project/
├── app/                              # Streamlit web application
│   ├── leukemia_classifier_app.py    # Main UI
│   ├── smoke_test.py                 # Pre-run model checker
│   ├── validate_input.py             # CSV format validator
│   ├── convert_to_latent.py          # Gene CSV → latent features
│   ├── download_models.py            # Download models from HuggingFace
│   └── example_input_64d.csv         # Example input file
│
├── notebooks/
│   ├── 1_data_preparation.ipynb      # Phase 1: Data loading & preprocessing
│   ├── 2_autoencoder_pretraining.ipynb  # Phase 2: TCGA pretraining
│   ├── 3_transfer_learning_classification.ipynb  # Phase 3: Fine-tuning & classification
│   └── reports/figures/              # Training plots and evaluation figures
│
├── data/                             # Hosted on HuggingFace (not in repo)
│   ├── raw/                          # GSE13159 expression data, TCGA data
│   └── processed/                    # Latent features, predictions, sample info
│
├── Phase_1___Report.pdf
├── Phase_2___Autoencoder_Pretraining_Comprehensive_Technical_Report___Analysis.pdf
├── Phase_3_Report___Classification_Models.pdf
├── Phase_4__Explainability___Gene_Importance.pdf
├── requirements.txt
└── HUGGINGFACE_LINKS.md              # Model & dataset download links
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Download models from HuggingFace
```bash
python app/download_models.py
```

### 3. Run the web app
```bash
streamlit run app/leukemia_classifier_app.py
```

Open `http://localhost:8501` in your browser.

---

## Using the App

### Fast Demo (Recommended)
1. In the sidebar, select **"Upload 64-d latent CSV"**
2. Click **"Load independent example (mixed subtypes)"**
3. View predictions and confidence meters for all 5 subtypes

### Full Gene Mode
1. In the sidebar, select **"Upload full gene expression CSV"**
2. Upload a CSV with ~22,000 gene columns
3. The app encodes it and runs predictions automatically

---

## Models

All trained models are on HuggingFace: [Samzzh/leukemia_classifier_project_models](https://huggingface.co/Samzzh/leukemia_classifier_project_models/tree/main)

| Model | Description | Input |
|-------|-------------|-------|
| `encoder.h5` | Autoencoder encoder (TCGA pretrained + fine-tuned) | ~22k genes |
| `mlp_lightweight_final.h5` | MLP classifier | 64-d latent features |
| `xgboost_optimized.model` | XGBoost classifier | 64-d latent features |
| `scaler.joblib` | Feature scaler | ~22k genes |

---

## Classification Targets

| Class | Description |
|-------|-------------|
| ALL | Acute Lymphoblastic Leukemia |
| AML | Acute Myeloid Leukemia |
| CLL | Chronic Lymphocytic Leukemia |
| CML | Chronic Myelogenous Leukemia |
| Healthy | Normal/control samples |

---

## Data Sources

| Dataset | Samples | Purpose |
|---------|---------|---------|
| GSE13159 | ~2,000 | Leukemia subtype classification (fine-tuning) |
| TCGA (RSEM TPM) | ~10,000+ | Pretraining the autoencoder |

---

## Requirements

```
numpy
pandas
scikit-learn
matplotlib
seaborn
streamlit
xgboost
lightgbm
tensorflow
keras
```

---

## Phase Reports

| Phase | Topic | File |
|-------|-------|------|
| Phase 1 | Data Preparation & EDA | `Phase_1___Report.pdf` |
| Phase 2 | Autoencoder Pretraining | `Phase_2___Autoencoder_Pretraining...pdf` |
| Phase 3 | Transfer Learning & Classification | `Phase_3_Report___Classification_Models.pdf` |
| Phase 4 | Explainability & Gene Importance | `Phase_4__Explainability___Gene_Importance.pdf` |

---

**Course**: Artificial Intelligence — Fall 2025
