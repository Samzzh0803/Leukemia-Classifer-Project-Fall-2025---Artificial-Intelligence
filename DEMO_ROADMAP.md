# 🧬 Leukemia Classifier — Live Demo Roadmap

## Quick Start (< 5 minutes)

### 1. Pre-Demo Verification
Run this to ensure all models and dependencies are ready:
```powershell
python .\app\smoke_test.py
```

Expected output:
```
✓ Gene list: 67313.5 KB
✓ Latent data: 101.4 KB
✓ Sample info: 5.4 KB
✓ Encoder: 39375.9 KB
✓ MLP: 51.0 KB
✓ XGBoost: [size] KB
⚠ Scaler: NOT FOUND (okay — can skip full-gene mode)
```

### 2. Launch Streamlit UI
In a **fresh terminal**:
```powershell
streamlit run .\app\leukemia_classifier_app.py
```

Opens automatically at `http://localhost:8501`

---

## Demo Flow (for audience)

### **Mode 1: Quick Latent Demo (Recommended — ~2 min)**
**Use this for fast, reliable predictions without encoder overhead.**

1. **Open sidebar** → Select "Upload 30-d latent CSV (fast demo)"
2. **Click button**: "📊 Load independent example (mixed subtypes)"
3. **Show results**:
   - MLP predictions (5 classes: ALL, AML, CLL, CML, Healthy)
   - XGBoost predictions
   - Confidence meters (🟢🟡🟠🔴)
   - Download predictions CSV

**Why this works:**
- No encoder needed (fast)
- Uses realistic 30-d latent features
- 50 truly independent samples (not from GSE13159 or TCGA)
- Shows all 5 leukemia subtypes + healthy controls

### **Mode 2: Full End-to-End Demo (Advanced — ~3–5 min)**
**Use this to show the entire ML pipeline: genes → encoder → classifier.**

1. **Open sidebar** → Select "Upload full gene-expression CSV (~20k genes)"
2. **Click button**: "⚡ Load latent example (fast, training data)"
3. **Show processing**:
   - Dataset Info panel (gene alignment stats)
   - Encoder running (full genes → 30-d latent)
   - MLP/XGBoost predictions on encoded features
4. **Explain pipeline** on screen:
   - Input: ~20k gene expression values
   - StandardScaler (normalize)
   - Autoencoder (22k genes → 30 latent dims)
   - MLP classifier (5 classes)

**Note:** This requires `scaler.joblib` (currently missing — see Troubleshooting).

### **Mode 3: Upload Your Own Data**
1. Prepare a CSV:
   - **Latent mode**: 30 numeric columns (named `latent_00`..`latent_29` or any 30 numeric columns)
   - **Full-gene mode**: ~20k genes (Ensembl IDs, aligned to training set)
2. Use validate script first:
   ```powershell
   python .\app\validate_input.py your_file.csv latent
   ```
3. Upload via UI

---

## What to Show on Screen

### **Key Takeaways**
- **Transfer Learning**: Pretrained on TCGA pan-cancer → fine-tuned on GSE13159 leukemia
- **Dimensionality Reduction**: 22,034 genes → 30 latent features (autoencoder)
- **Multi-Subtype Classification**: ALL, AML, CLL, CML, Healthy
- **Real-World Ready**: Uses truly independent data (not seen during training)

### **UI Highlights**
- 📋 **Dataset Information**: Shows gene alignment, sample counts, feature ranges
- 🎯 **Confidence Meter**: Visual indication of prediction certainty (very high/high/moderate/low)
- 📊 **Probability Bar Chart**: Shows confidence for each subtype
- 📥 **Download Results**: Export predictions to CSV for further analysis

---

## Demo Data Files

| File | Samples | Features | Use Case |
|------|---------|----------|----------|
| `independent_example.csv` | 50 | 30-d latent | **Primary demo** — unseen leukemia cohort with mixed subtypes |
| `independent_example_with_labels.csv` | 50 | 30-d latent + disease | Reference — check model accuracy |
| `example_input_latent.csv` | 1 | 30-d latent | Quick single-sample test |
| `example_input_full.csv` | 1 | ~20k genes | Full-pipeline single-sample test |

---

## Common Demo Scenarios

### **Scenario A: "Show me predictions on new data"**
1. Load `independent_example.csv` (latent mode)
2. Show first 5 samples and their predictions
3. Point out: "These 50 samples were NOT in GSE13159 or TCGA training"

### **Scenario B: "How confident is the model?"**
1. Show confidence meter color coding (very high = 🟢, low = 🔴)
2. Highlight a "very high" prediction vs a "moderate" one
3. Explain: threshold at 0.7 for "high" confidence

### **Scenario C: "How accurate is it on unseen data?"**
1. Load `independent_example_with_labels.csv` (reference)
2. Load `independent_example.csv` (predictions)
3. Compare predicted classes to true labels
4. Calculate accuracy/confusion matrix (optional, prepare beforehand)

### **Scenario D: "Can I use it with my own dataset?"**
1. Show validation script:
   ```powershell
   python .\app\validate_input.py your_file.csv auto
   ```
2. Demonstrate auto-detection (latent vs full-gene)
3. Show remediation suggestions if needed

---

## Troubleshooting & Fallbacks

### **Issue: "MLP prediction failed"**
**Root cause**: MLP model not found or shape mismatch fixed in latest build.  
**Fallback**: Use XGBoost results only (also shown on screen).

### **Issue: "Confidence is 400%"**
**Root cause**: Invalid probability normalization (fixed in latest build).  
**Fallback**: Already fixed — this shouldn't appear. If it does, restart Streamlit.

### **Issue: "Gene alignment poor (0%)"**
**Cause**: Latent CSV detected as full-gene mode by mistake.  
**Fix**: Select correct input mode in sidebar.

### **Issue: "Scaler not found"**
**Cause**: `notebooks/models/scaler.joblib` missing.  
**Workaround**: Use latent demo mode (doesn't need scaler).  
**Fix** (if needed): Regenerate from notebook 2.

### **Issue: Streamlit stuck / predictions slow**
**Fix**: Restart Streamlit in terminal:
```powershell
# Ctrl+C to stop current
streamlit run .\app\leukemia_classifier_app.py --logger.level=error
```

---

## Pre-Demo Checklist

- [ ] Run `python .\app\smoke_test.py` → all ✓ (except scaler ⚠ is okay)
- [ ] Start Streamlit: `streamlit run .\app\leukemia_classifier_app.py`
- [ ] Wait 5–10 sec for UI to load
- [ ] Test quick latent load: "📊 Load independent example"
- [ ] Verify MLP and XGBoost results appear with valid probabilities
- [ ] Check confidence meter is colored (not showing 400%)
- [ ] Test download predictions CSV
- [ ] (Optional) Test full-gene mode if `scaler.joblib` is available
- [ ] Have backup: if full-gene fails, stick to latent demo

---

## Key Talking Points

### **About the Dataset**
- **Training**: GSE13159 (357 leukemia samples, 5 subtypes)
- **Pretraining**: TCGA pan-cancer (10k+ samples, transfer learning)
- **Demo data**: 50 independent samples (not GSE13159, not TCGA)
- **Subtypes**: ALL, AML, CLL, CML, Healthy

### **About the Models**
- **Autoencoder**: Learns compressed representation (22k genes → 30 latent dims)
- **Classifiers**: MLP and XGBoost trained on latent features
- **Transfer Learning**: Encoder weights from TCGA pretraining, fine-tuned on leukemia

### **Why This Works**
- Dimensionality reduction removes noise, captures biology
- Latent space generalizes to unseen data
- Multi-model ensemble (MLP + XGBoost) improves robustness

---

## Post-Demo Follow-Up

If audience asks:
- **"Can I access the notebooks?"** → Refer to `notebooks/` folder (1-5 showing full pipeline)
- **"What genes matter most?"** → See `notebooks/4_explainability_analysis.ipynb` (SHAP analysis)
- **"How do I use this in production?"** → This app is production-ready; API version available on request
- **"Can I add my own data?"** → Yes; CSV must have 30 latent dims or ~20k genes aligned to reference

---

## Quick Reference Commands

```powershell
# Verify setup
python .\app\smoke_test.py

# Start demo UI
streamlit run .\app\leukemia_classifier_app.py

# Validate your CSV
python .\app\validate_input.py your_file.csv auto

# Convert any CSV to latent format
python .\app\convert_to_latent.py input.csv output.csv

# Create fresh independent dataset
python .\app\create_unseen_independent_dataset.py

# Run predictions on independent data (non-interactive)
python .\app\evaluate_independent.py
```

---

## Demo Success Criteria

✅ **You'll know it worked if**:
1. Streamlit UI loads without errors
2. Independent example loads and shows predictions
3. MLP probabilities sum to ~1.0 (valid probabilities)
4. Confidence meter shows correct color (not 400%)
5. At least one prediction is "very high" confidence (🟢)
6. CSV download works
7. No crashes for 5–10 predictions

---

**Good luck with your presentation! 🚀**
