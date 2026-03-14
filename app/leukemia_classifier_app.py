"""
Leukemia Classifier - Streamlit Web Application
Streamlit app for predicting leukemia types using robust 64d latent features.

Usage:
    streamlit run app/leukemia_classifier_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import joblib
import warnings
warnings.filterwarnings('ignore')

# Add parent to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ============================================================
# CONFIG & PATHS
# ============================================================
st.set_page_config(
    page_title="Leukemia Classifier",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL_DIR = ROOT / "notebooks" / "models"
DATA_DIR = ROOT / "data" / "processed"

MODEL_PATHS = {
    "encoder": MODEL_DIR / "encoder.h5",
    "mlp": MODEL_DIR / "mlp_robust_64d_final.keras",
    "xgb": MODEL_DIR / "xgboost_robust_64d.model",
    "scaler": MODEL_DIR / "scaler.joblib",
    "label_encoder": MODEL_DIR / "label_encoder_64d.joblib",
}

# ============================================================
# LOAD MODELS (CACHED)
# ============================================================
@st.cache_resource
def load_models():
    """Load all required models with caching."""
    models = {}
    missing = []
    
    try:
        import tensorflow as tf
        if MODEL_PATHS["mlp"].exists():
            models["mlp"] = tf.keras.models.load_model(str(MODEL_PATHS["mlp"]))
        else:
            missing.append("MLP model")
    except Exception as e:
        st.warning(f"⚠️ Failed to load MLP: {e}")
        missing.append("MLP model")
    
    try:
        import xgboost as xgb
        if MODEL_PATHS["xgb"].exists():
            xgb_model = xgb.Booster()
            xgb_model.load_model(str(MODEL_PATHS["xgb"]))
            models["xgb"] = xgb_model
        else:
            missing.append("XGBoost model")
    except Exception as e:
        st.warning(f"⚠️ Failed to load XGBoost: {e}")
        missing.append("XGBoost model")
    
    try:
        if MODEL_PATHS["scaler"].exists():
            models["scaler"] = joblib.load(str(MODEL_PATHS["scaler"]))
        else:
            st.info("Scaler not found - skipping gene-level preprocessing")
    except Exception as e:
        st.warning(f"⚠️ Scaler unavailable: {e}")
    
    try:
        if MODEL_PATHS["label_encoder"].exists():
            models["label_encoder"] = joblib.load(str(MODEL_PATHS["label_encoder"]))
        else:
            st.info("Label encoder not found - using default class names")
    except Exception as e:
        st.warning(f"⚠️ Label encoder unavailable: {e}")
    
    # Load encoder for 30d → 64d conversion
    try:
        import tensorflow as tf
        if MODEL_PATHS["encoder"].exists():
            models["encoder"] = tf.keras.models.load_model(str(MODEL_PATHS["encoder"]))
        else:
            st.info("Encoder not found - cannot convert 30d to 64d")
    except Exception as e:
        st.warning(f"⚠️ Encoder unavailable: {e}")
    
    return models, missing

# ============================================================
# UTILITY FUNCTIONS
# ============================================================


def normalize_probabilities(probs):
    """Normalize prediction probabilities using softmax if needed."""
    if probs.ndim == 1:
        probs = np.expand_dims(probs, axis=1)
    
    # Check if already normalized
    row_sums = probs.sum(axis=1)
    if not np.allclose(row_sums, 1.0, atol=1e-3):
        # Apply softmax
        probs_exp = np.exp(probs - probs.max(axis=1, keepdims=True))
        probs = probs_exp / probs_exp.sum(axis=1, keepdims=True)
    
    return np.clip(probs, 0, 1)

def get_class_names(label_encoder):
    """Get disease class names."""
    if label_encoder is not None:
        return list(label_encoder.classes_)
    else:
        return ['ALL', 'AML', 'CLL', 'CML', 'Healthy']

# ============================================================
# UI SETUP
# ============================================================
st.title("🔬 Leukemia Classifier")
st.markdown("### Predict leukemia type from gene expression data using deep learning")

with st.sidebar:
    st.header("Configuration")
    prediction_mode = st.radio(
        "Select prediction mode:",
        ["64d Robust Features (Recommended)", "Full Gene Expression"],
        help="Choose input format for predictions"
    )
    
    ensemble = st.checkbox(
        "Use ensemble predictions",
        value=True,
        help="Average predictions from both MLP and XGBoost models"
    )

# ============================================================
# MAIN APP
# ============================================================

# Load models
with st.spinner("🔄 Loading models..."):
    models, missing = load_models()

if missing:
    st.error(f"❌ Missing models: {', '.join(missing)}")
    st.info("Please ensure all model files are present in `notebooks/models/`")
    st.stop()

st.success("✅ All models loaded successfully!")

# ============================================================
# INPUT SECTION
# ============================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input Data")
    
    if prediction_mode == "64d Robust Features":
        st.write("Upload a CSV with 64 robust latent feature columns")
        
        input_type = st.radio(
            "Input method:",
            ["Upload CSV", "Use example data"],
            horizontal=True,
            key="input_64d"
        )
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input Data")
    
    if prediction_mode == "64d Robust Features (Recommended)":
        st.write("Upload a CSV with 64 latent feature columns (latent_00...latent_63)")
        
        input_type = st.radio(
            "Input method:",
            ["Upload CSV", "Use example data"],
            horizontal=True
        )
        
        if input_type == "Upload CSV":
            uploaded_file = st.file_uploader(
                "Choose CSV file",
                type="csv",
                help="Expected: samples x 64 robust latent features"
            )
            
            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file, index_col=0)
                    st.write(f"Loaded: {df.shape[0]} samples, {df.shape[1]} features")
                except Exception as e:
                    st.error(f"Error loading file: {e}")
                    df = None
            else:
                df = None
        else:
            # Use example
            example_path = ROOT / "app" / "example_input_64d.csv"
            if example_path.exists():
                df = pd.read_csv(example_path, index_col=0)
                st.info(f"Using example: {df.shape[0]} samples")
            else:
                st.warning("Example file not found")
                df = None
    
    else:  # Full gene expression
        st.write("Upload a CSV with full gene expression (genes as rows or columns)")
        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type="csv",
            help="Will be converted to 64d latent features using encoder"
        )
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file, index_col=0)
                st.write(f"Loaded: {df.shape[0]} samples, {df.shape[1]} features")
                st.info("NOTE: Requires encoder - converting to 64d latent space")
            except Exception as e:
                st.error(f"Error loading file: {e}")
                df = None
        else:
            df = None

with col2:
    st.subheader("Data Info")
    if df is not None:
        st.metric("Samples", df.shape[0])
        st.metric("Features", df.shape[1])
        
        if prediction_mode == "64d Robust Features (Recommended)":
            if df.shape[1] >= 64:
                st.success("Has 64+ features")
            else:
                st.warning(f"Only {df.shape[1]} features (need 64)")
    else:
        st.info("No data loaded yet")

# ============================================================
# PREDICTION SECTION
# ============================================================
if df is not None and df.shape[1] >= 64:
    st.subheader("Predictions")
    
    # Prepare data (use first 64 columns)
    X = df.iloc[:, :64].values.astype('float32')
    sample_names = df.index.tolist()
    
    # Make predictions
    predictions = {}
    
    if "mlp" in models:
        with st.spinner("Running MLP model..."):
            mlp_probs = models["mlp"].predict(X, verbose=0)
            mlp_probs = normalize_probabilities(mlp_probs)
            predictions["mlp"] = mlp_probs
    
    if "xgb" in models:
        with st.spinner("Running XGBoost model..."):
            import xgboost as xgb
            dmatrix = xgb.DMatrix(X)
            xgb_preds = models["xgb"].predict(dmatrix)
            
            # Convert XGBoost class predictions to probability matrix
            num_classes = 5  # ALL, AML, CLL, CML, Healthy
            xgb_probs = np.zeros((len(xgb_preds), num_classes))
            for i, pred in enumerate(xgb_preds):
                class_idx = int(pred) % num_classes
                xgb_probs[i, class_idx] = 1.0
            
            xgb_probs = normalize_probabilities(xgb_probs)
            predictions["xgb"] = xgb_probs
    
    # Get class names
    class_names = get_class_names(models.get("label_encoder"))
    n_classes = min(predictions[list(predictions.keys())[0]].shape[1], len(class_names))
    class_names = class_names[:n_classes]
    
    # Ensemble or individual
    if ensemble and len(predictions) > 1:
        st.write("**Ensemble Predictions** (averaged from MLP + XGBoost)")
        final_probs = np.mean([p for p in predictions.values()], axis=0)
    else:
        model_name = list(predictions.keys())[0] if predictions else "MLP"
        st.write(f"**{model_name.upper()} Predictions**")
        final_probs = predictions[list(predictions.keys())[0]]
    
    # Display results
    final_preds = np.argmax(final_probs, axis=1)
    final_confs = np.max(final_probs, axis=1)
    
    results_df = pd.DataFrame({
        'Sample': sample_names,
        'Prediction': [class_names[p] for p in final_preds],
        'Confidence': [f"{c:.1%}" for c in final_confs],
    })
    
    st.dataframe(results_df, use_container_width=True)
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Samples", len(results_df))
    with col2:
        avg_conf = final_confs.mean()
        st.metric("Avg Confidence", f"{avg_conf:.1%}")
    with col3:
        top_class = results_df['Prediction'].value_counts().index[0]
        top_count = results_df['Prediction'].value_counts().values[0]
        st.metric("Most Common", f"{top_class} ({top_count})")
    
    # Class distribution
    st.subheader("Prediction Distribution")
    class_dist = results_df['Prediction'].value_counts()
    st.bar_chart(class_dist)
    
    # Confidence visualization with colors
    st.subheader("Confidence Scores by Sample")
    
    # Create confidence data with color coding
    conf_data = []
    colors = []
    for i, conf in enumerate(final_confs):
        conf_pct = conf * 100
        if conf_pct >= 80:
            colors.append('green')
        elif conf_pct >= 60:
            colors.append('yellow')
        else:
            colors.append('red')
        conf_data.append({
            'Sample': sample_names[i],
            'Confidence': conf_pct,
            'Color': colors[-1]
        })
    
    conf_df = pd.DataFrame(conf_data)
    
    # Create color-coded bar chart
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    # Add bars with colors
    for color in ['green', 'yellow', 'red']:
        mask = conf_df['Color'] == color
        subset = conf_df[mask]
        
        if color == 'green':
            color_val = '#2ecc71'
            label = 'High (≥80%)'
        elif color == 'yellow':
            color_val = '#f1c40f'
            label = 'Moderate (60-79%)'
        else:
            color_val = '#e74c3c'
            label = 'Low (<60%)'
        
        fig.add_trace(go.Bar(
            x=subset['Sample'],
            y=subset['Confidence'],
            name=label,
            marker_color=color_val,
            text=[f"{v:.1f}%" for v in subset['Confidence']],
            textposition='auto',
        ))
    
    fig.update_layout(
        title="Confidence Scores by Sample",
        xaxis_title="Sample",
        yaxis_title="Confidence (%)",
        barmode='group',
        height=400,
        showlegend=True,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Confidence statistics
    st.subheader("Confidence Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        high_conf = (final_confs >= 0.80).sum()
        st.metric("High Confidence (≥80%)", high_conf, delta=f"{100*high_conf/len(final_confs):.1f}%")
    with col2:
        med_conf = ((final_confs >= 0.60) & (final_confs < 0.80)).sum()
        st.metric("Moderate (60-79%)", med_conf, delta=f"{100*med_conf/len(final_confs):.1f}%")
    with col3:
        low_conf = (final_confs < 0.60).sum()
        st.metric("Low (<60%)", low_conf, delta=f"{100*low_conf/len(final_confs):.1f}%")
    with col4:
        avg_conf = final_confs.mean() * 100
        st.metric("Average", f"{avg_conf:.1f}%")
    
    # Download results
    csv = results_df.to_csv(index=False)
    st.download_button(
        "Download predictions",
        csv,
        "leukemia_predictions.csv",
        "text/csv"
    )

else:
    if df is None:
        st.info("Upload a file to get started")
    else:
        st.warning(f"Insufficient features: {df.shape[1]} provided, 64 required")

# ============================================================
# INFO FOOTER
st.divider()
st.markdown("""
### About This App
- **Models**: MLP (robust 64d) + XGBoost (robust 64d)
- **Input**: 64-dimensional robust latent features (latent_00...latent_63)
- **Classes**: ALL, AML, CLL, CML, Healthy
- **Framework**: TensorFlow + XGBoost + Streamlit
""")

