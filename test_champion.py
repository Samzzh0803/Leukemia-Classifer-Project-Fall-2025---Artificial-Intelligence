#!/usr/bin/env python
"""Quick test of champion MLP on independent data."""

import pandas as pd
import numpy as np
from tensorflow import keras
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load champion model
mlp_champion = keras.models.load_model('notebooks/models/final_champion_model.h5')
print('[OK] Champion MLP loaded')

# Load independent data
df = pd.read_csv('app/independent_example.csv', index_col=0)
df_labels = pd.read_csv('app/independent_example_with_labels.csv', index_col=0)
classes = ['ALL', 'AML', 'CLL', 'CML', 'Healthy']

print(f'[INFO] Testing on {df.shape[0]} independent samples')

# Predict with champion
probs = mlp_champion.predict(df.values, verbose=0)
probs = np.clip(probs, 0, 1)
probs = probs / (probs.sum(axis=1, keepdims=True) + 1e-10)

n_classes = probs.shape[1]
class_names = classes[:n_classes]
top_preds = [class_names[np.argmax(p)] for p in probs]
top_confs = [np.max(p) for p in probs]

df_results = pd.DataFrame({
    'Prediction': top_preds,
    'Confidence': top_confs
}, index=df.index)

print(f'\n[RESULTS] Champion MLP Predictions:')
print(df_results.head(15))
print(f'\n[STATS] Unique predictions: {df_results["Prediction"].value_counts().to_dict()}')
print(f'[STATS] Avg confidence: {df_results["Confidence"].mean():.2%}')
print(f'\n[TRUTH] Ground Truth Distribution:')
print(df_labels['disease'].value_counts().to_dict())
