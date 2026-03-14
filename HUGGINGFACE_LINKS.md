# HuggingFace Resources

All large files (models and datasets) for this project are hosted on HuggingFace due to GitHub file size limits.

---

## Models

**Repository**: https://huggingface.co/Samzzh/leukemia_classifier_project_models/tree/main

| File | Description |
|------|-------------|
| `encoder.h5` | Autoencoder encoder — compresses ~22k genes to 64-d latent space |
| `mlp_lightweight_final.h5` | MLP neural network classifier (64-d latent → 5 subtypes) |
| `xgboost_optimized.model` | XGBoost classifier (64-d latent → 5 subtypes) |
| `scaler.joblib` | StandardScaler fitted on GSE13159 training data |
| `autoencoder_full.h5` | Full autoencoder (encoder + decoder) |
| `decoder.h5` | Decoder only |

### Download models
```bash
python app/download_models.py
```
Or manually download from the link above and place files in `notebooks/models/`.

---

## Datasets

**Repository**: https://huggingface.co/datasets/Samzzh/leukemia_classifier_project_datasets

### Raw Data (`data/raw/`)
| File | Description |
|------|-------------|
| `GSE13159.txt` | Raw GSE13159 leukemia gene expression data |
| `GSE13159_refinebio_expression.tsv` | Normalized expression matrix (samples × genes) |
| `GSE13159_refinebio_metadata.json` | Sample metadata and disease labels |
| `probeMap_gencode.v23.annotation.gene.probemap` | Gene annotation mapping |
| `tcga_RSEM_gene_tpm.gz` | TCGA pan-cancer TPM expression data (~10k samples) |

### Processed Data (`data/processed/`)
| File | Description |
|------|-------------|
| `leukemia_filtered.csv` | GSE13159 filtered to overlapping genes with TCGA |
| `leukemia_sample_info.csv` | Sample metadata with disease labels |
| `leukemia_latent_features.csv` | 64-d latent features for all GSE13159 samples |
| `leukemia_latent_features_collab.csv` | Latent features (collaborative version) |
| `tcga_filtered.csv` | TCGA data filtered to overlapping genes |
| `final_predictions.csv` | Final model predictions on test set |
| `phase3_predictions_64d.csv` | Phase 3 predictions using 64-d features |
| `phase3_performance_summary.csv` | Performance metrics summary |
| `gene_latent_correlations.csv` | Gene-to-latent dimension correlation analysis |

### Download datasets
```python
from huggingface_hub import snapshot_download

# Download all processed data
snapshot_download(
    repo_id="Samzzh/leukemia_classifier_project_datasets",
    repo_type="dataset",
    local_dir="data/"
)
```

---

## Notes

- The `data/` folder is excluded from this GitHub repo via `.gitignore`
- The `notebooks/models/` folder is excluded from this GitHub repo via `.gitignore`
- All model files use Git LFS on HuggingFace for efficient storage
