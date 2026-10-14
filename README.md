# 🚗⚡ EV Battery Digital Twin & Range Optimization System
### Advanced Machine Learning Lab (19MAM56) – CAT II Project Work
**Department of Computing – AI & ML**  
**Coimbatore Institute of Technology, Coimbatore – 641 014**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ev-battery-predictor.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)](http://localhost:8000/docs)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](Dockerfile)

* **🌐 Live Cloud Application:** [https://ev-battery-predictor.streamlit.app/](https://ev-battery-predictor.streamlit.app/)
* **💻 GitHub Source Code:** [https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor](https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor)
* **📄 Academic Project Report:** [`IEEE_PROJECT_REPORT.pdf`](IEEE_PROJECT_REPORT.pdf)

---

## 📌 1. Project Overview & Research Objectives
Accurate driving range forecasting and battery health prognostics are vital for sustainable electric vehicle (EV) operation. Traditional on-board estimation algorithms fail under fluctuating real-world variables, while battery degradation is non-linear and sensitive to thermal cycling.

This project implements an end-to-end **Physics-Informed Digital Twin and Advanced Ensemble Machine Learning Pipeline** that:
1. **Models Battery Electro-Chemical Aging**: Implements Arrhenius thermal degradation, calendar fade, and cycle stress equations to calculate State of Health (SOH) and Remaining Useful Life (RUL).
2. **Predicts Real-World Driving Range**: Deploys an advanced regression ensemble (**XGBoost + Gradient Boosting + Random Forest + Linear Baseline**) evaluated against multi-factor telemetry.
3. **Applies Dimensionality Reduction & Model Explainability**: Conducts **Principal Component Analysis (PCA)** and **SHAP (SHapley Additive exPlanations)** to interpret non-linear feature attributions.
4. **Delivers Production-Grade Deployment**: Exposes a real-time **FastAPI** inference service with Pydantic validation schemas, containerized with **Docker** and hosted via an interactive **Streamlit** dashboard.

---

## 🏗️ 2. System Architecture

```
                                  [ Raw Fleet Telemetry / CSV Data ]
                                                   │
                                     ┌─────────────┴─────────────┐
                                     ▼                           ▼
                        [ Physics Digital Twin ]     [ Data Processing Pipeline ]
                        • Arrhenius Thermal Stress   • 1.5x IQR Outlier Detection
                        • Calendar & Cycle Aging     • 40+ Domain Engineered Features
                        • SOH & RUL Prognostics      • PCA Dimensionality Reduction
                                     │                           │
                                     └─────────────┬─────────────┘
                                                   ▼
                                    [ Advanced ML Range Models ]
                                    • Random Forest Regressor
                                    • Gradient Boosting Regressor
                                    • XGBoost (Optuna Tuned)
                                    • Linear Baseline
                                                   │
                                                   ▼
                                    [ Weighted Blending Ensemble ]
                                                   │
                                     ┌─────────────┴─────────────┐
                                     ▼                           ▼
                        [ Production FastAPI API ]    [ Interactive Streamlit UI ]
                        (Pydantic Validation / Swagger) (Docker / Hugging Face Spaces)
```

---

## 🔬 3. Mathematical Formulations

### A. Physics-Informed Battery Degradation Model
Battery State of Health (SOH) is formulated by combining calendar aging, cycle fatigue, and thermal stress:
$$\text{Degradation}_{\text{total}} = \Big(k_{\text{calendar}} \cdot t_{\text{days}} + k_{\text{cycle}} \cdot N_{\text{cycles}}\Big) \cdot \exp\left(k_{\text{temp}} \cdot \frac{T - 25}{25}\right) \cdot \Big(1 + k_{\text{DoD}} \cdot \text{DoD}\Big)$$
$$\text{SOH}(t) = \max\Big(0.70, \; 1.0 - \text{Degradation}_{\text{total}}\Big)$$

Remaining Useful Life (RUL) until automotive retirement ($80\%$ SOH threshold):
$$\text{RUL}_{\text{days}} = \frac{\text{SOH}_{\text{current}} - 0.80}{k_{\text{calendar}} + k_{\text{cycle}} \cdot n_{\text{daily\_cycles}}}$$

### B. Weighted Blending Regression Ensemble
The final driving range prediction $\hat{y}_{\text{ensemble}}$ blends decision-tree variance reduction, boosting residual minimization, and linear regularization:
$$\hat{y}_{\text{ensemble}} = 0.35 \cdot \hat{y}_{\text{RF}} + 0.35 \cdot \hat{y}_{\text{GBDT}} + 0.20 \cdot \hat{y}_{\text{XGBoost}} + 0.10 \cdot \hat{y}_{\text{Linear}}$$

---

## 📊 4. Experimental Benchmarks & Results

Evaluated on an independent $20\%$ hold-out test dataset across 5,000 driving instances:

| Model Architecture | MAE (km) ↓ | RMSE (km) ↓ | $R^2$ Score ↑ | Relative Inference Latency |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression Baseline** | 22.144 | 29.774 | 0.8112 | $< 1\text{ ms}$ |
| **Random Forest Regressor** | 17.642 | 24.201 | 0.8752 | $12\text{ ms}$ |
| **Gradient Boosting (GBDT)** | 11.875 | 17.026 | 0.9383 | $4\text{ ms}$ |
| **XGBoost (Optuna Tuned)** | **9.685** | **13.887** | **0.9589** | **$2\text{ ms}$** |
| **Weighted Blending Ensemble** | **12.962** | **18.488** | **0.9272** | **$18\text{ ms}$** |

*Optuna automated hyperparameter optimization minimized XGBoost MAE to sub-10 km error across varied weather and driving styles.*

---

## 📈 5. Advanced Analytical Visualizations
The project generates 5 comprehensive analytical figures saved under `visualizations/`:

1. **`fig1_model_benchmarking.png`**: Side-by-side bar comparison of MAE and $R^2$ goodness-of-fit across all candidate models.
2. **`fig2_actual_vs_predicted_parity.png`**: Parity calibration plot with $\pm 10\%$ error tolerance boundaries.
3. **`fig3_residual_analysis.png`**: Residual error histogram, kernel density estimation, and homoscedasticity scatter.
4. **`fig4_pca_dimensionality_reduction.png`**: 2D Principal Component projections with explained variance ratio ($> 65\%$ captured in first 2 components).
5. **`fig5_shap_feature_importance.png`**: TreeExplainer SHAP attribution ranking top range predictors (Usable Battery Capacity, State of Charge, Speed, and Temperature).

---

## 🚀 6. Installation & Execution

### Prerequisites
* Python 3.10+
* Windows / Linux / macOS

```bash
# 1. Clone repository & navigate to directory
git clone <repository_url>
cd ev-battery-predictor

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate   # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt
```

---

### Option A: Run Interactive Web Dashboard (Local / Hugging Face Spaces)
```bash
streamlit run app.py
```
*Access UI at:* `http://localhost:8501`

---

### Option B: Run Production FastAPI REST Service (Rubric Component 4)
```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
*Interactive Swagger Documentation:* `http://localhost:8000/docs`

**Sample Inference Request (`POST /predict/range`):**
```json
{
  "battery_capacity_kwh": 75.0,
  "battery_soh": 0.92,
  "battery_soc_start": 0.85,
  "vehicle_efficiency_km_kwh": 4.5,
  "temperature_c": 22.0,
  "humidity_percent": 60.0,
  "wind_speed_kmh": 10.0,
  "precipitation": 0,
  "avg_speed_kmh": 55.0,
  "traffic_density": "medium",
  "route_type": "city",
  "elevation_change_m": 0.0,
  "driving_style": "normal",
  "ac_usage": 1
}
```

---

### Option C: Re-generate Visualizations & Benchmark Table
```bash
python generate_benchmarks_and_visualizations.py
```

---

## 🐳 7. Docker & Container Deployment
The application is fully containerized for deployment on **Hugging Face Spaces** or cloud instances:

```bash
# Build Docker image
docker build -t ev-battery-predictor .

# Run Docker container locally
docker run -p 7860:7860 ev-battery-predictor
```
*Access containerized UI at:* `http://localhost:7860`

---

## 📂 8. Repository Organization

```
ev-battery-predictor/
├── Dockerfile                                      # Containerization specification (HF Spaces / Cloud)
├── requirements.txt                                # Production Python dependencies
├── api.py                                          # Production FastAPI service with Pydantic validation
├── app.py                                          # Interactive Streamlit dashboard
├── demo.py                                         # CLI terminal demonstration script
├── generate_benchmarks_and_visualizations.py        # Automated benchmarking & 5 analytical plots generator
├── Part1(1).csv.zip                                # Real EV fleet telemetry archive (81K+ records)
│
├── visualizations/                                 # 300 DPI exported analytical figures for IEEE report
│   ├── fig1_model_benchmarking.png
│   ├── fig2_actual_vs_predicted_parity.png
│   ├── fig3_residual_analysis.png
│   ├── fig4_pca_dimensionality_reduction.png
│   ├── fig5_shap_feature_importance.png
│   └── model_benchmarks.csv
│
├── src/                                            # Modular backend packages
│   ├── digital_twin/
│   │   └── battery_twin.py                         # Arrhenius SOH & RUL physics degradation engine
│   ├── data_processing/
│   │   └── data_pipeline.py                        # Preprocessing, PCA, and 40+ engineered features
│   ├── models/
│   │   └── range_predictor.py                      # Multi-model ensemble, Optuna tuner & SHAP explainer
│   └── utils/
│       └── visualization.py                        # Plotly and metric visualizers
│
└── notebooks/
    ├── battery_digital_twin_analysis.ipynb         # Physics simulation notebook
    └── range_prediction_analysis.ipynb             # ML model analysis notebook
```

---

## 👥 Authors & Academic Affiliation
* **Course:** 19MAM56 – Advanced Machine Learning Lab
* **Program:** III M.Sc. AI & ML (V Semester)
* **Institution:** Department of Computing – AI & ML, Coimbatore Institute of Technology
