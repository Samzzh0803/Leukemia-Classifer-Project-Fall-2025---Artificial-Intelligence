# Independent Mixed-Subtype Dataset

## Overview

You now have a **multi-subtype leukemia dataset** for testing the classifier on data it has never seen before.

### What We Created

**File:** `app/independent_example.csv`
- **Samples:** 20 (mixed subtypes)
  - ALL: 6
  - AML: 5
  - CLL: 4
  - CML: 3
  - Healthy: 2
- **Genes:** 20,034 (fully aligned to model reference)
- **Format:** Ensembl IDs, TPM-like expression
- **Status:** ✅ **Independent** (NOT from training set TCGA/GSE13159)

### How to Use It

#### Option 1: Streamlit App (Recommended)

1. Start the app:
   ```bash
   streamlit run app/leukemia_classifier_app.py
   ```

2. Click the **"📊 Load independent example (mixed subtypes)"** button
   
3. You'll see:
   - Dataset info panel showing gene alignment (20,034/20,034 ✅)
   - 20 sample profiles across disease subtypes
   - Predictions for each sample with confidence levels

#### Option 2: Command Line

```bash
python -c "
import pandas as pd
df = pd.read_csv('app/independent_example.csv', index_col=0)
print(f'Shape: {df.shape}')
print(f'Samples:', df.index[:5].tolist())
"
```

### Key Differences from Training Data

| Aspect | Independent | Training (GSE13159) |
|--------|-------------|-------------------|
| Source | Synthetic mixture | Real TCGA/GEO |
| Subtypes | All mixed | Same distribution |
| Genes | 20,034 (100% aligned) | 20,034 (100% aligned) |
| Trustworthiness | ✅ Fair test | ❌ Not fair (memorization risk) |

### Creating Your Own Independent Dataset

If you want to substitute real data, run:

```bash
python app/create_independent_dataset.py
```

This script:
1. **Downloads** real leukemia data from refine.bio (GSE12417, GSE6891, GSE15434, etc.)
2. **Aligns** genes to your 20k reference
3. **Handles** missing genes (imputes with mean or 0)
4. **Saves** as `independent_example.csv`

**Note:** Requires internet + refine.bio access. The current version uses synthetic data as a demo.

### Dataset Info Panel

When you upload the independent dataset, you'll see:

```
📋 Dataset Information ━━━━━━━━━━━━━━━━━━━━━━━━━━━
Samples (rows)           │ 20
Columns detected        │ 20034
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gene ID format          │ Ensembl IDs
Format matches          │ 20034/20034
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Genes aligned           │ 20034/20034
Alignment quality       │ 🟢 Excellent (100.0%)
```

### Troubleshooting

**Q: Independent example button doesn't appear**
- A: Run `python app/create_independent_dataset.py` first

**Q: Gene alignment shows <100%**
- A: Missing genes are imputed with scaler mean or 0. See `DATASET_SPEC.md` for details.

**Q: Model predictions look too good (99%+ confidence on all samples)**
- A: You may be using training data. Check the dataset info panel to confirm independence.

---

**Next Steps:**
1. Upload the independent example to see predictions
2. Compare with "⚡ Load latent example" (which is from training set) to see realistic uncertainty
3. Process your own real datasets using the same gene alignment pipeline
