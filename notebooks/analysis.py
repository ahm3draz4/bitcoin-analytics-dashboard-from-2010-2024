# notebooks/analysis.ipynb  (save as .ipynb via Jupyter, or run as .py)
# ─────────────────────────────────────────────────────
# Bitcoin History — Exploratory Data Analysis (EDA)
# ─────────────────────────────────────────────────────

import sys
sys.path.insert(0, "..")          # allow imports from project root

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from filters import load_data

df = load_data("../data/Bitcoin_History.csv")

# ── 1. Basic Info ────────────────────────────────────────────────────────────
print("Shape:", df.shape)
print("\nColumn types:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())

# ── 2. Descriptive Statistics ────────────────────────────────────────────────
print("\nDescriptive Stats:")
print(df[["Price", "Open", "High", "Low", "Vol.", "Change %"]].describe().round(2))

# ── 3. Sample rows ───────────────────────────────────────────────────────────
print("\nFirst 5 rows:")
print(df.head())
