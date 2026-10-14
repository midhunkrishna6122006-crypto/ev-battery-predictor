# VOLTWISE
## Physics-Informed Battery Digital Twin & Multi-Factor EV Range Optimization
**Using Electrochemical Degradation Kinetics and Gradient-Boosted Blending Ensembles**  
*Advanced Machine Learning Lab – CAT II Mini Project*  
**Department of Computing (M.Sc. AI & ML), Coimbatore Institute of Technology, Coimbatore – 641 014**  

**Author:** Midhun Krishna B (*Student Member, CIT / IEEE*)  
**Source Repository:** [https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor](https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor)  
**Live Cloud Web Application:** [https://ev-battery-predictor.streamlit.app/](https://ev-battery-predictor.streamlit.app/)  
**Production REST API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)  

---

### Abstract
VoltWise presents an explainable, cyber-physical machine learning framework for electric vehicle (EV) driving range optimization and battery health prognostics by fusing physics-informed electro-chemical degradation with real-world fleet telemetry. The system utilizes 81,000+ real EV battery telemetry records synthesized into 5,000 multi-factorial driving instances. Battery State of Health (SOH) fade and Remaining Useful Life (RUL) are continuously simulated via an Arrhenius thermal degradation engine incorporating calendar aging and depth-of-discharge (DoD) stress. Simultaneously, instantaneous driving range is predicted via an advanced regression ensemble combining Random Forest, Gradient Boosted Decision Trees (GBDT), and an Optuna Bayesian-tuned XGBoost regressor blended through variance-weighted voting. The complete pipeline incorporates 1.5×IQR outlier clipping, 40+ engineered domain features, Principal Component Analysis (PCA) dimensionality reduction, and TreeExplainer SHAP (SHapley Additive exPlanations) interpretability. Benchmarked against baseline linear models, the Optuna-tuned XGBoost model achieves an exceptional Mean Absolute Error (MAE) of 9.68 km and an R² score of 0.9589 (a 56.3% error reduction). The end-to-end architecture is deployed as a production-grade FastAPI REST service with Pydantic v2 validation and continuously hosted on Streamlit Community Cloud with a multi-stage Docker containerization specification.

---

### 1. Problem Definition and Objectives
Widespread adoption of Electric Vehicles (EVs) is fundamentally hindered by consumer anxiety regarding battery lifespan uncertainty and unpredictable real-world driving range [1]. Standard on-board vehicle estimators compute remaining range using simplistic rolling average energy consumption metrics. Such heuristics produce substantial forecasting errors under extreme weather conditions, dynamic auxiliary HVAC climate loads, road topographical gradients, and aggressive driving styles [2]. Concurrently, lithium-ion battery packs undergo irreversible electrochemical degradation governed by solid electrolyte interphase (SEI) growth, lithium plating, and active material dissolution under thermal and cycling fatigue [3], [4].

VoltWise addresses this algorithmic disconnect by unifying a **Physics-Informed Electrochemical Digital Twin** with an **Advanced Machine Learning Blending Ensemble**. The core objectives are:
1. Construct an end-to-end telemetry data pipeline with robust $1.5\times\text{IQR}$ outlier filtering, domain feature engineering, and PCA dimensionality reduction.
2. Formulate an electrochemical battery digital twin implementing Arrhenius kinetics, calendar fade, and cycle fatigue to track SOH, RUL, and optimal safe C-rates.
3. Train, optimize (via Optuna Bayesian search), and benchmark diverse regressors (Linear Baseline, Random Forest, GBDT, XGBoost, and Weighted Blending Ensemble).
4. Interpret feature attributions using TreeExplainer SHAP to reveal non-linear environmental and operational interactions.
5. Deploy the complete architecture as a production-grade FastAPI REST API and a live cloud-hosted Streamlit dashboard accessible via public URL.

---

### 2. Dataset and Preprocessing
The empirical evaluation utilizes real-world battery telemetry comprising 81,000+ time-series records combined with 5,000 multi-factorial driving trip instances covering 14 operational and environmental covariates. Data preprocessing removes sensor dropouts, cleans invalid values, and applies $1.5\times\text{IQR}$ boundary clipping to prevent anomalous current draw spikes from biasing model weights. The dataset is partitioned using a 70/15/15 train/validation/test stratified protocol with fixed random seeds. Continuous numerical variables are standardized using z-score normalization fitted strictly on the training partition to prevent data leakage, while categorical parameters (traffic density, route environment, driving behavior) are one-hot encoded.

#### Table 1. Dataset Summary & Feature Schema
| Variable / Component | Value / Scope | Analytical Role |
| :--- | :--- | :--- |
| **Fleet Telemetry Observations** | 81,000+ sensor records | Dynamic battery voltage, current, and temperature |
| **Simulated Driving Instances** | 5,000 multi-factorial trips | Multi-condition range prediction training observations |
| **Operational & Environmental Attributes** | 14 raw telemetry features | Speed, SOC, ambient temp, humidity, wind, elevation, HVAC |
| **Engineered Domain Features** | 40+ mathematical features | Usable Energy ($E_{\text{usable}}$), Weather Severity Index ($I_{\text{weather}}$), interaction cross-terms |
| **Dimensionality Reduction** | 2 Principal Components (PCA) | Captures $>65\%$ total feature variance |
| **Train / Validation / Test Protocol** | 70% / 15% / 15% | Stratified hold-out validation with zero label leakage |
| **Target Variable** | Real-world range ($\text{km}$) | Continuous regression ground-truth |

Engineered features incorporate vehicle kinematic laws:
1. **Battery Usable Energy:** $E_{\text{usable}} = C_{\text{nominal}} \cdot \text{SOH} \cdot \text{SOC}$
2. **Weather Severity Index:** $I_{\text{weather}} = 0.3 \cdot \text{Precipitation} + 0.2 \cdot \mathbb{I}_{(\text{Wind} > 20)} + 0.5 \cdot \mathbb{I}_{(|T - 20| > 15)}$
3. **Dynamic Power Interaction:** $\text{Speed} \times \text{Ambient Temperature}$, $\text{SOH} \times \text{Calendar Age}$

---

### 3. VoltWise Cyber-Physical Architecture

```
[ Raw Fleet Telemetry & Environmental Covariates ]
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
[ Physics Digital Twin ]       [ Data Engineering Pipeline ]
• Arrhenius Thermal Kinetics   • 1.5x IQR Outlier Detection
• Calendar Fade & Cycle Aging  • 40+ Engineered Features
• SOH & RUL Prognostics        • PCA Dimensionality Reduction
       │                               │
       └───────────────┬───────────────┘
                       ▼
       [ Advanced Regression Ensemble ]
       • Linear Baseline Model
       • Random Forest Regressor
       • Gradient Boosting Regressor (GBDT)
       • Optuna-Tuned XGBoost Regressor
                       │
                       ▼
       [ Weighted Blending Ensemble ]
       ŷ_ens = 0.35 RF + 0.35 GBDT + 0.20 XGB + 0.10 Lin
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
[ Production FastAPI REST API ] [ Interactive Streamlit Dashboard ]
(Pydantic Validation / Swagger) (Docker / Live Cloud Hosting)
```
*Figure 1. VoltWise dual-engine architecture: Physics-informed digital twin, machine learning blending ensemble, and production deployment.*

#### Mathematical Formulations:
The physical degradation engine simulates cumulative capacity loss $D_{\text{total}}$ through coupled calendar and cycling stress accelerated by temperature:
$$D_{\text{total}} = (k_{\text{cal}} \cdot t_{\text{days}} + k_{\text{cyc}} \cdot N_{\text{cyc}}) \cdot \exp\left(k_{\text{temp}} \cdot \frac{T - 25}{25}\right) \cdot (1 + k_{\text{DoD}} \cdot \text{DoD}) \tag{1}$$

$$\text{SOH}(t) = \max(0.70, \; 1.0 - D_{\text{total}}) \tag{2}$$

Remaining Useful Life (RUL) until automotive retirement (80% SOH standard) is formulated as:
$$\text{RUL}_{\text{days}} = \frac{\text{SOH}_{\text{current}} - 0.80}{k_{\text{cal}} + k_{\text{cyc}} \cdot n_{\text{daily\_cycles}}} \tag{3}$$

Driving range is predicted by blending heterogeneous estimators using variance-weighted voting:
$$\hat{y}_{\text{ensemble}} = 0.35 \cdot \hat{y}_{\text{RF}} + 0.35 \cdot \hat{y}_{\text{GBDT}} + 0.20 \cdot \hat{y}_{\text{XGBoost}} + 0.10 \cdot \hat{y}_{\text{Linear}} \tag{4}$$

Dynamic safe charging C-rate prevents lithium plating during high-stress charging states:
$$C_{\text{safe}} = C_{\text{max}} \cdot \text{SOH} \cdot \min\left(1.0, \; \exp\left(-0.05 \cdot \max(0, T - 35)\right)\right) \tag{5}$$

---

### 4. Machine Learning Methodology
The workflow encompasses data validation, IQR boundary clipping, domain feature derivation, baseline model training, hyperparameter tuning, model blending, and SHAP interpretability:

1. **Model Architectures Compared:**
   * **Model A (Baseline):** Ordinary Least Squares (OLS) Linear Regression.
   * **Model B (Bagging):** Random Forest Regressor ($n=100$ trees, max depth 12).
   * **Model C (Boosting):** Gradient Boosted Decision Trees (GBDT).
   * **Model D (Optimized):** Optuna Bayesian-guided eXtreme Gradient Boosting (XGBoost).
   * **Model E (Ensemble):** Weighted Blending Ensemble ($0.35\,\text{RF} + 0.35\,\text{GBDT} + 0.20\,\text{XGB} + 0.10\,\text{Lin}$).

2. **Optuna Bayesian Optimization:**
   Tree-structured Parzen Estimator (TPE) search across 50 trials optimizing:
   * `n_estimators`: $[50, 150]$
   * `max_depth`: $[3, 8]$
   * `learning_rate`: $[0.02, 0.20]$ (log scale)
   * `subsample`: $[0.6, 1.0]$
   * **Objective Function:** Minimize hold-out validation Mean Absolute Error (MAE).

3. **Dimensionality Reduction & Explainability:**
   * **PCA:** Decomposes multi-variable telemetry into 2 orthogonal eigenvectors capturing $>65\%$ variance.
   * **TreeExplainer SHAP:** Computes Shapley additive values to quantify exact marginal feature attributions for every trip prediction.

---

### 5. Results and Comparative Analysis
The data-engineering and model evaluation stages produced comprehensive quantitative benchmarks across 1,000 unseen hold-out test driving cycles.

#### Table 2. Dataset Partition and Operational Distribution
| Partition Split | Instance Count | Operational Conditions Covered | Role |
| :--- | :---: | :--- | :--- |
| **Training Set (70%)** | 3,500 trips | Mixed urban, highway, rural, diverse temperatures | Model parameter estimation |
| **Validation Set (15%)** | 750 trips | Temperature extremes, elevation deltas | Optuna hyperparameter optimization |
| **Hold-Out Test Set (15%)** | 750 trips | Unseen trip profiles, varied driving styles | Final unbiased metric benchmarking |

#### Table 3. Quantitative Model Benchmarking Comparison (Hold-Out Test Set)
| Model Architecture | MAE (km) $\downarrow$ | RMSE (km) $\downarrow$ | $R^2$ Score $\uparrow$ | Latency | Performance Rank |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **A. Linear Regression Baseline** | 22.144 | 29.774 | 0.8112 | $< 1\text{ ms}$ | 5 |
| **B. Random Forest Regressor** | 17.642 | 24.201 | 0.8752 | $12\text{ ms}$ | 4 |
| **C. Gradient Boosting (GBDT)** | 11.875 | 17.026 | 0.9383 | $4\text{ ms}$ | 2 |
| **D. XGBoost (Optuna Tuned)** | **9.685** | **13.887** | **0.9589** | **$2\text{ ms}$** | **1 (Best)** |
| **E. Weighted Blending Ensemble** | **12.962** | **18.488** | **0.9272** | **$18\text{ ms}$** | **2 (Robust)** |

#### Key Analytical Findings:
1. **56.3% Error Reduction:** Optuna-tuned XGBoost reduced MAE from 22.144 km (linear baseline) down to **9.685 km**, achieving a state-of-the-art $R^2$ score of **0.9589**.
2. **Residual Homoscedasticity:** Residual errors display normal distribution centered at zero bias ($\mu \approx 0.04\text{ km}$, $\sigma \approx 13.88\text{ km}$), confirming that predictions remain unbiased across both short intra-city commutes and extended highway journeys.
3. **SHAP Feature Ranking:** TreeExplainer SHAP confirms that *Battery Usable Capacity*, *Starting SOC*, *Average Speed*, and *Ambient Temperature* account for $>78\%$ of cumulative model attribution. Extreme cold temperatures ($-10^\circ\text{C}$) contribute up to a $28\%$ range penalty due to cabin heating loads and internal cell resistance escalation.
4. **Edge Feasibility:** XGBoost executes in just **$2\text{ ms}$**, proving immediate viability for deployment onto on-board vehicle Electronic Control Units (ECUs).

---

### 6. Deployment and System Architecture
VoltWise is engineered as a production-grade, reproducible software pipeline:

1. **High-Throughput FastAPI REST API (`api.py`):**
   * Employs Pydantic v2 schemas for strict input boundary validation (temperatures bounded to $[-25^\circ\text{C}, 50^\circ\text{C}]$, SOC bounded to $[0.05, 1.0]$).
   * Exposes endpoints:
     * `POST /predict/range`: Real-time ensemble range forecast with confidence bounds.
     * `POST /battery/health`: SOH, RUL, and degradation grade computation.
     * `POST /battery/optimize-charging`: Safe C-rate and charging thermal constraints.
   * Auto-generates interactive Swagger documentation at `http://localhost:8000/docs`.

2. **Docker Containerization (`Dockerfile`):**
   * Multi-stage build on `python:3.11-slim` exposing ports `7860`, `8000`, and `8501`.
   * Completely reproducible across Windows, Linux, and cloud container engines.

3. **Continuous Public Cloud Hosting (Streamlit Community Cloud):**
   * Hosted continuously at: **[https://ev-battery-predictor.streamlit.app/](https://ev-battery-predictor.streamlit.app/)**.
   * Provides non-technical stakeholders with interactive parameter sliders, real-time physics simulations, and 300 DPI analytical charts.
   * Linked directly to public GitHub repository: **[https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor](https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor)**.

---

### 7. Conclusion and Future Scope
VoltWise demonstrates an end-to-end cyber-physical application of advanced machine learning for EV battery prognostics and driving range optimization. By fusing Arrhenius electro-chemical degradation with Optuna-tuned gradient boosted decision trees, the system achieved a **56.3% reduction in prediction error** ($R^2 = 0.9589$, $\text{MAE} < 10\text{ km}$). The complete pipeline integrates physics-based digital twins, Bayesian hyperparameter optimization, SHAP explainability, FastAPI REST serving, Docker packaging, and live cloud deployment.

**Future Scope:**
* Integration of Recurrent Long Short-Term Memory (LSTM) networks for multi-step cell voltage sequence forecasting.
* Direct connection with Google Maps / OpenElevation contour APIs for live route topography optimization.
* Development of an on-board OBD-II telemetry integration module for live vehicle data streaming.

---

### References
* **[1]** C. Bingham, C. Walsh, and S. Carroll, "Impact of driving characteristics on electric vehicle energy consumption," *SAE Int. J. Alt. Power*, vol. 1, no. 1, pp. 132–141, 2012.
* **[2]** Y. Bi, D. Chrenko, F. Gao, and D. Paire, "Estimating vehicle electric consumption using machine learning algorithms," in *Proc. IEEE Transportation Electrification Conference and Expo (ITEC)*, 2020, pp. 450–455.
* **[3]** J. Schmalstieg, S. Käbitz, M. Ecker, and D. U. Sauer, "A holistic aging model for Li(NiMnCo)O2 based 18650 lithium-ion cells," *Journal of Power Sources*, vol. 257, pp. 325–334, 2014.
* **[4]** K. A. Severson et al., "Data-driven prediction of battery cycle life before capacity degradation," *Nature Energy*, vol. 4, no. 5, pp. 383–391, 2019.
* **[5]** T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.*, 2016, pp. 785–794.
* **[6]** T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, "Optuna: A next-generation hyperparameter optimization framework," in *Proc. 25th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.*, 2019, pp. 2623–2631.
* **[7]** S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Proc. Advances in Neural Information Processing Systems (NeurIPS)*, 2017, pp. 4765–4774.
* **[8]** S. Onori, L. Serrao, and G. Rizzoni, *Hybrid Electric Vehicles: Energy Management Strategies*. London: Springer-Verlag, 2016.
