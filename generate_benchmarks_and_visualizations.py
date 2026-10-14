"""
Automated Benchmarking and Advanced Visualizations Generator
CIT Coimbatore - 19MAM56 Advanced Machine Learning Lab
Generates the 5 required advanced analytical visualizations and benchmarking comparisons.
"""

import sys
import os

if sys.platform.startswith('win') and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from models.range_predictor import RangePredictionModel
from data_processing.data_pipeline import EVDataProcessor
from digital_twin.battery_twin import BatteryDigitalTwin, BatteryState

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'visualizations')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set aesthetic styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Arial', 'font.size': 11})

print("=" * 70)
print("[CIT 19MAM56 AML LAB] BENCHMARKING & ADVANCED VISUALIZATIONS GENERATOR")
print("=" * 70)

# Step 1: Initialize Models and Data Pipeline
processor = EVDataProcessor()
range_model = RangePredictionModel(model_type="ensemble")

print("\n[1/5] Generating dataset & training models (Random Forest, GBDT, XGBoost, Linear)...")
data = range_model.generate_synthetic_data(n_samples=5000)
training_results = range_model.train(data)

# Preprocess for test set
processed_data = range_model.preprocess_data(data, is_training=False)
feature_cols = range_model.feature_columns
X = processed_data[feature_cols]
y = processed_data['range_km']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Benchmark Table
print("\n" + "=" * 65)
print("📊 MODEL BENCHMARK PERFORMANCE COMPARISON (TEST SET)")
print("=" * 65)
benchmark_records = []
for name, model in range_model.models.items():
    if name == 'linear':
        X_test_scaled = range_model.scalers['numerical'].transform(X_test)
        y_pred = model.predict(X_test_scaled)
    else:
        y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    benchmark_records.append({
        'Model Architecture': name.replace('_', ' ').title(),
        'MAE (km)': round(mae, 3),
        'RMSE (km)': round(rmse, 3),
        'R² Score': round(r2, 4)
    })

# Add Ensemble
preds_rf = range_model.models['random_forest'].predict(X_test)
preds_gb = range_model.models['gradient_boost'].predict(X_test)
preds_xgb = range_model.models['xgboost'].predict(X_test)
X_test_scaled = range_model.scalers['numerical'].transform(X_test)
preds_lr = range_model.models['linear'].predict(X_test_scaled)

ensemble_preds = 0.35 * preds_rf + 0.35 * preds_gb + 0.20 * preds_xgb + 0.10 * preds_lr

mae_ens = mean_absolute_error(y_test, ensemble_preds)
rmse_ens = np.sqrt(mean_squared_error(y_test, ensemble_preds))
r2_ens = r2_score(y_test, ensemble_preds)
benchmark_records.append({
    'Model Architecture': 'Ensemble (Weighted Blending)',
    'MAE (km)': round(mae_ens, 3),
    'RMSE (km)': round(rmse_ens, 3),
    'R² Score': round(r2_ens, 4)
})

benchmark_df = pd.DataFrame(benchmark_records)
print(benchmark_df.to_string(index=False))
benchmark_df.to_csv(os.path.join(OUTPUT_DIR, 'model_benchmarks.csv'), index=False)
print(f" Saved benchmark table to: {os.path.join(OUTPUT_DIR, 'model_benchmarks.csv')}")

# =====================================================================
# VISUALIZATION 1: Multi-Model Comparative Benchmarking Bar Chart
# =====================================================================
print("\n[2/5] Creating Visualization 1: Model Benchmarking Comparison...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# MAE Plot
bars1 = ax1.bar(benchmark_df['Model Architecture'], benchmark_df['MAE (km)'], color=['#3498db', '#2ecc71', '#e67e22', '#e74c3c', '#9b59b6'])
ax1.set_title('Mean Absolute Error (MAE in km) - Lower is Better', fontsize=12, fontweight='bold')
ax1.set_ylabel('MAE (km)')
ax1.tick_params(axis='x', rotation=25)
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f"{yval:.2f}", ha='center', va='bottom', fontsize=9)

# R² Plot
bars2 = ax2.bar(benchmark_df['Model Architecture'], benchmark_df['R² Score'], color=['#3498db', '#2ecc71', '#e67e22', '#e74c3c', '#9b59b6'])
ax2.set_title('R² Goodness of Fit - Higher is Better', fontsize=12, fontweight='bold')
ax2.set_ylabel('R² Score')
ax2.set_ylim(0.85, 1.02)
ax2.tick_params(axis='x', rotation=25)
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.005, f"{yval:.3f}", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
fig_path1 = os.path.join(OUTPUT_DIR, 'fig1_model_benchmarking.png')
plt.savefig(fig_path1, dpi=300)
plt.close()
print(f" Saved: {fig_path1}")

# =====================================================================
# VISUALIZATION 2: Actual vs Predicted Regression Parity Plot with Error Bands
# =====================================================================
print("\n[3/5] Creating Visualization 2: Regression Parity & Calibration Curve...")
plt.figure(figsize=(8, 7))
plt.scatter(y_test, ensemble_preds, alpha=0.4, color='#2980b9', edgecolors='none', s=25, label='Ensemble Predictions')

min_val = min(y_test.min(), ensemble_preds.min())
max_val = max(y_test.max(), ensemble_preds.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Parity (y = x)')

# 10% error margin bands
x_line = np.linspace(min_val, max_val, 100)
plt.fill_between(x_line, x_line * 0.9, x_line * 1.1, color='gray', alpha=0.15, label='±10% Error Tolerance Band')

plt.title('Actual vs. Predicted EV Driving Range (Test Set)', fontsize=13, fontweight='bold')
plt.xlabel('Actual Range (km)', fontsize=11)
plt.ylabel('Predicted Range (km)', fontsize=11)
plt.legend(loc='upper left', frameon=True)
plt.tight_layout()
fig_path2 = os.path.join(OUTPUT_DIR, 'fig2_actual_vs_predicted_parity.png')
plt.savefig(fig_path2, dpi=300)
plt.close()
print(f" Saved: {fig_path2}")

# =====================================================================
# VISUALIZATION 3: Residual Error Distribution & Statistical Density
# =====================================================================
print("\n[4/5] Creating Visualization 3: Residual Error Analysis...")
residuals = ensemble_preds - y_test
fig, (ax_res1, ax_res2) = plt.subplots(1, 2, figsize=(14, 5))

# Residual Histogram & KDE
sns.histplot(residuals, kde=True, ax=ax_res1, color='#27ae60', bins=35)
ax_res1.axvline(x=0, color='red', linestyle='--', lw=1.5, label='Zero Error')
ax_res1.set_title('Residual Error Distribution (e = y_pred - y_true)', fontsize=12, fontweight='bold')
ax_res1.set_xlabel('Residual Error (km)')
ax_res1.legend()

# Residuals vs Predicted (Homoscedasticity Check)
ax_res2.scatter(ensemble_preds, residuals, alpha=0.35, color='#8e44ad', s=20)
ax_res2.axhline(y=0, color='red', linestyle='--', lw=1.5)
ax_res2.set_title('Residuals vs Predicted Range (Homoscedasticity Analysis)', fontsize=12, fontweight='bold')
ax_res2.set_xlabel('Predicted Range (km)')
ax_res2.set_ylabel('Residual Error (km)')

plt.tight_layout()
fig_path3 = os.path.join(OUTPUT_DIR, 'fig3_residual_analysis.png')
plt.savefig(fig_path3, dpi=300)
plt.close()
print(f" Saved: {fig_path3}")

# =====================================================================
# VISUALIZATION 4: PCA 2D Dimensionality Reduction & Variance Ratio
# =====================================================================
print("\n[5/5] Creating Visualization 4: PCA Dimensionality Reduction...")
pca_df, pca_obj, exp_var = processor.apply_pca(data, n_components=2)
fig, (ax_pca1, ax_pca2) = plt.subplots(1, 2, figsize=(14, 5))

# 2D PCA Projection colored by Range
range_col = 'range_km' if 'range_km' in data.columns else 'predicted_range_km'
scatter = ax_pca1.scatter(pca_df['PC1'], pca_df['PC2'], c=data.loc[pca_df.index, range_col], cmap='plasma', alpha=0.5, s=20)
cbar = plt.colorbar(scatter, ax=ax_pca1)
cbar.set_label('Range (km)', fontsize=10)
ax_pca1.set_title('2D PCA Projection of EV Feature Space', fontsize=12, fontweight='bold')
ax_pca1.set_xlabel(f'Principal Component 1 ({exp_var[0]*100:.1f}% Variance)')
ax_pca1.set_ylabel(f'Principal Component 2 ({exp_var[1]*100:.1f}% Variance)')

# Explained Variance Ratio Bar Chart
ax_pca2.bar(['PC1', 'PC2'], exp_var * 100, color=['#2980b9', '#16a085'], width=0.5)
ax_pca2.set_title('Principal Components Explained Variance Ratio', fontsize=12, fontweight='bold')
ax_pca2.set_ylabel('Explained Variance (%)')
ax_pca2.set_ylim(0, 100)
for i, v in enumerate(exp_var * 100):
    ax_pca2.text(i, v + 2, f"{v:.1f}%", ha='center', fontweight='bold')

plt.tight_layout()
fig_path4 = os.path.join(OUTPUT_DIR, 'fig4_pca_dimensionality_reduction.png')
plt.savefig(fig_path4, dpi=300)
plt.close()
print(f" Saved: {fig_path4}")

# =====================================================================
# VISUALIZATION 5: SHAP Feature Importance & Attribution Plot
# =====================================================================
print("\n[Bonus] Creating Visualization 5: SHAP Model Explainability...")
shap_results = range_model.compute_shap_explanations(data, max_samples=80)
shap_imp = shap_results['mean_shap_values']

top_features = dict(list(shap_imp.items())[:10])
plt.figure(figsize=(10, 6))
y_pos = np.arange(len(top_features))
plt.barh(y_pos, list(top_features.values()), color='#d35400', align='center')
plt.yticks(y_pos, [f.replace('_', ' ').title() for f in top_features.keys()])
plt.gca().invert_yaxis()  # Top feature on top
plt.title('SHAP Feature Importance (Mean Absolute Attribution)', fontsize=13, fontweight='bold')
plt.xlabel('Mean |SHAP Value| (Impact on Driving Range Prediction)')
plt.tight_layout()
fig_path5 = os.path.join(OUTPUT_DIR, 'fig5_shap_feature_importance.png')
plt.savefig(fig_path5, dpi=300)
plt.close()
print(f" Saved: {fig_path5}")

print("\n" + "=" * 70)
print(f"[OK] SUCCESS: All 5 Advanced Analytical Visualizations saved in: {OUTPUT_DIR}")
print("=" * 70)
