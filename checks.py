import os
import psutil
print("📁 Current dir:", os.getcwd())
print("💾 RAM available:", f"{psutil.virtual_memory().available / 1e9:.1f} GB")
print("📊 Files in notebooks/models/:", os.listdir('notebooks/models') if os.path.exists('notebooks/models') else "No models dir")