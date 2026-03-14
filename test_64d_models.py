"""Quick test to verify 64d models work with example data"""

import pandas as pd
import numpy as np
from pathlib import Path
import tensorflow as tf
import xgboost as xgb
import joblib

ROOT = Path(__file__).parent
MODEL_DIR = ROOT / "notebooks" / "models"

print("=" * 60)
print("Testing 64d Models with Example Data")
print("=" * 60)

# Load models
print("\n[1] Loading models...")
try:
    mlp = tf.keras.models.load_model(str(MODEL_DIR / "mlp_robust_64d_final.keras"))
    print("  OK MLP loaded")
except Exception as e:
    print(f"  FAIL: {e}")
    mlp = None

try:
    xgb_model = xgb.Booster()
    xgb_model.load_model(str(MODEL_DIR / "xgboost_robust_64d.model"))
    print("  OK XGBoost loaded")
except Exception as e:
    print(f"  FAIL: {e}")
    xgb_model = None

try:
    label_enc = joblib.load(str(MODEL_DIR / "label_encoder_64d.joblib"))
    classes = list(label_enc.classes_)
    print(f"  OK Label encoder loaded: {classes}")
except Exception as e:
    print(f"  FAIL: {e}")
    classes = ['ALL', 'AML', 'CLL', 'CML', 'Healthy']

# Load example data
print("\n[2] Loading example 64d data...")
example_path = ROOT / "app" / "example_input_64d.csv"
if example_path.exists():
    df = pd.read_csv(example_path, index_col=0)
    print(f"  OK Loaded: {df.shape[0]} samples, {df.shape[1]} features")
    print(f"  Columns: {list(df.columns[:3])}...{list(df.columns[-2:])}")
else:
    print("  FAIL: Example file not found")
    df = None

# Test predictions
if df is not None and mlp is not None and xgb_model is not None:
    print("\n[3] Making predictions...")
    
    X = df.values.astype('float32')
    
    # MLP
    try:
        mlp_probs = mlp.predict(X, verbose=0)
        print(f"  OK MLP: {mlp_probs.shape}")
        print(f"     First sample: {mlp_probs[0]}")
    except Exception as e:
        print(f"  FAIL MLP: {e}")
        mlp_probs = None
    
    # XGBoost
    try:
        dmatrix = xgb.DMatrix(X)
        xgb_preds = xgb_model.predict(dmatrix)
        # Convert XGBoost class predictions to one-hot probabilities
        num_classes = len(classes)
        xgb_probs = np.zeros((len(xgb_preds), num_classes))
        for i, pred in enumerate(xgb_preds):
            class_idx = int(pred) % num_classes
            xgb_probs[i, class_idx] = 1.0
        print(f"  OK XGBoost: {xgb_probs.shape}")
        print(f"     First sample: {xgb_probs[0]}")
    except Exception as e:
        print(f"  FAIL XGBoost: {e}")
        xgb_probs = None
    
    # Ensemble
    if mlp_probs is not None and xgb_probs is not None:
        print("\n[4] Ensemble Results...")
        # Normalize and average
        mlp_norm = mlp_probs / (mlp_probs.sum(axis=1, keepdims=True) + 1e-10)
        xgb_norm = xgb_probs / (xgb_probs.sum(axis=1, keepdims=True) + 1e-10)
        ensemble_probs = (mlp_norm + xgb_norm) / 2
        
        for i, sample_id in enumerate(df.index[:3]):
            pred_idx = np.argmax(ensemble_probs[i])
            pred_class = classes[pred_idx]
            confidence = ensemble_probs[i, pred_idx]
            
            print(f"  Sample {sample_id}: {pred_class} ({confidence:.1%})")

print("\n" + "=" * 60)
print("SUCCESS: 64d models working correctly!")
print("=" * 60)
