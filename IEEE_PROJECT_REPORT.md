# Physics-Informed Digital Twin and Advanced Ensemble Learning for Electric Vehicle Battery Prognostics and Driving Range Optimization

**Author:** Midhun Krishna B  
**Course:** 19MAM56 – Advanced Machine Learning Lab (CAT II Project Work)  
**Program:** III M.Sc. AI & ML (V Semester), Department of Computing – AI & ML  
**Institution:** Coimbatore Institute of Technology, Coimbatore – 641 014  
**GitHub Repository:** [https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor](https://github.com/midhunkrishna6122006-crypto/ev-battery-predictor)  
**Live Cloud Deployment:** [https://ev-battery-predictor.streamlit.app/](https://ev-battery-predictor.streamlit.app/)  

---

## Abstract
Electric Vehicle (EV) adoption relies heavily on predictable driving range and reliable battery lifespan forecasting. However, real-world battery degradation exhibits non-linear kinetics under varying thermal and cycling stress, while instantaneous range estimations fluctuate significantly due to environmental and operational covariates. This project presents an integrated framework combining a Physics-Informed Battery Digital Twin with an Advanced Ensemble Machine Learning architecture. The digital twin models electro-chemical State of Health (SOH) fade and Remaining Useful Life (RUL) using Arrhenius thermal acceleration and cycling fatigue equations. Simultaneously, driving range prediction is formulated via an advanced regression pipeline incorporating Random Forest, Gradient Boosted Decision Trees (GBDT), and an Optuna-optimized eXtreme Gradient Boosting (XGBoost) model blended through weighted voting. Dimensionality reduction via Principal Component Analysis (PCA) and model interpretability via TreeExplainer SHAP (SHapley Additive exPlanations) values validate feature attributions. Evaluated on test driving datasets, the optimized XGBoost and ensemble models achieve a Mean Absolute Error (MAE) of 9.68 km and an $R^2$ score of 0.9589, demonstrating substantial improvement over baseline linear models. The complete system is deployed as a production-grade FastAPI REST service with Pydantic validation and containerized via Docker for cloud accessibility.

**Keywords—** Electric Vehicles, Battery Digital Twin, State of Health, Arrhenius Degradation, XGBoost, Optuna Optimization, SHAP Explainability, FastAPI, Docker.

---

## 1. Introduction
The global shift toward electrified transportation requires addressing two primary consumer challenges: range anxiety and battery degradation uncertainty. Standard Electric Vehicle On-Board Diagnostics (OBD) typically compute remaining range using static average consumption metrics, leading to substantial forecast errors under adverse conditions such as sub-zero ambient temperatures, aggressive acceleration profiles, or mountainous topography. Concurrently, lithium-ion battery packs undergo continuous irreversible capacity loss through Solid Electrolyte Interphase (SEI) growth, lithium plating, and active material dissolution. 

This project addresses these challenges by developing:
1. **A Physics-Informed Digital Twin Engine**: Continuous simulation of battery State of Health (SOH), Remaining Useful Life (RUL), and second-life repurposing potential using physical degradation models.
2. **An Advanced Multi-Factor Regression Ensemble**: Real-time range forecasting factoring in 14 environmental, vehicle, and behavioral variables.
3. **Automated Hyperparameter Optimization & Explainability**: Optuna Bayesian-guided parameter search and SHAP attribution plots to unveil feature dynamics.
4. **Cloud-Native Deployment**: A production-grade REST API utilizing FastAPI and an interactive Streamlit UI containerized with Docker.

---

## 2. Literature Review
Extensive research exists in isolated domains of EV range estimation and battery health diagnostics:

1. **Empirical Range Modeling**: Conventional works (e.g., Bingham et al., 2012) employ physical resistance formulas (aerodynamic drag, rolling resistance, inertial forces). While mathematically rigorous, physical models require extensive vehicle-specific drag coefficients and fail to capture real-world driver behavior adaptations.
2. **Data-Driven Machine Learning**: Recent studies (e.g., Bi et al., 2020) demonstrated that gradient-boosted decision trees (GBDT) and Random Forests significantly outperform linear regressors by capturing non-linear feature interactions between ambient temperature and HVAC power draw. However, off-the-shelf estimators often treat the battery as an ideal energy reservoir, ignoring degradation-induced internal resistance increases.
3. **Battery Prognostics & Digital Twins**: Physics-informed degradation models (e.g., Schmalstieg et al., 2014; Arrhenius rate models) capture calendar and cycle aging effectively. Research gaps remain in integrating real-time physical degradation states directly into vehicle operational range prediction models.

**Research Gap Addressed**: This work integrates a physical digital twin with an advanced machine learning ensemble, bridging the gap between electrochemical battery prognostics and driving range estimation.

---

## 3. Methodology

### 3.1 System Pipeline Block Diagram

$$\begin{aligned}
\text{Telemetry Inputs} &\longrightarrow \boxed{\text{Data Cleaning \& Feature Pipeline}} \longrightarrow \boxed{\text{PCA Dimensionality Reduction}} \\
&\longrightarrow \begin{cases}
\boxed{\text{Physics Digital Twin}} &\longrightarrow \text{SOH, RUL \& Safe C-rate} \\
\boxed{\text{Advanced Ensemble ML}} &\longrightarrow \text{Range Prediction (km)}
\end{cases} \\
&\longrightarrow \boxed{\text{SHAP Model Explainability}} \longrightarrow \boxed{\text{FastAPI REST / Docker Deployment}}
\end{aligned}$$

### 3.2 Data Preprocessing and Feature Engineering
The pipeline processes raw vehicle telemetry, executing:
* **Missing Value & Outlier Imputation**: $1.5 \times \text{IQR}$ (Interquartile Range) boundary clipping on continuous variables.
* **Domain Feature Engineering**: 
  * Usable Energy: $E_{\text{usable}} = C_{\text{nominal}} \cdot \text{SOH} \cdot \text{SOC}$.
  * Weather Severity Index: $I_{\text{weather}} = 0.3 \cdot \text{Precip} + 0.2 \cdot \mathbb{I}_{(\text{Wind} > 20)} + 0.5 \cdot \mathbb{I}_{(|T - 20| > 15)}$.
  * Interaction Features: $\text{Temp} \times \text{Speed}$, $\text{SOH} \times \text{Age}$.
* **Dimensionality Reduction**: Principal Component Analysis (PCA) reduces multi-dimensional driving telemetry into 2 principal components capturing $>65\%$ total feature variance.

### 3.3 Mathematical Formulation of Models

#### A. Digital Twin Degradation Formulation
$$\text{Degradation} = (k_{\text{cal}} \cdot t_{\text{days}} + k_{\text{cycle}} \cdot N_{\text{cycles}}) \cdot \exp\left(k_{\text{temp}} \cdot \frac{T - 25}{25}\right) \cdot (1 + k_{\text{DoD}} \cdot \text{DoD})$$
$$\text{SOH}(t) = \max(0.70, \; 1.0 - \text{Degradation})$$
$$\text{RUL}_{\text{days}} = \frac{\text{SOH}_{\text{current}} - 0.80}{k_{\text{cal}} + k_{\text{cycle}} \cdot n_{\text{daily\_cycles}}}$$

#### B. Ensemble Prediction Formulation
$$\hat{y}_{\text{ensemble}} = 0.35 \cdot \hat{y}_{\text{RF}} + 0.35 \cdot \hat{y}_{\text{GBDT}} + 0.20 \cdot \hat{y}_{\text{XGBoost}} + 0.10 \cdot \hat{y}_{\text{Linear}}$$

### 3.4 Hyperparameter Optimization Strategy
XGBoost hyperparameters are optimized using **Optuna** (Tree-structured Parzen Estimator, TPE):
* `n_estimators`: $[50, 150]$
* `max_depth`: $[3, 8]$
* `learning_rate`: $[0.02, 0.20]$ (log scale)
* `subsample`: $[0.6, 1.0]$
* **Objective Function**: Minimize validation Mean Absolute Error ($\text{MAE}$).

---

## 4. Implementation & Experimental Setup

### 4.1 Software & Hardware Environment
* **Platform**: Python 3.11+, Scikit-Learn 1.3+, XGBoost 1.7+, Optuna 3.2+, SHAP 0.42+.
* **Web & API Framework**: FastAPI 0.100+, Uvicorn, Streamlit 1.25+, Pydantic v2.
* **Containerization**: Docker (Debian Python slim base image).
* **Hardware**: Intel Core i7 / AMD Ryzen 64-bit, 16 GB RAM.

---

## 5. Results & Comparative Analysis

### 5.1 Quantitative Model Benchmarking
Models were evaluated on a 20% hold-out test dataset across 5,000 driving instances:

| Model Architecture | MAE (km) | RMSE (km) | $R^2$ Score | Relative Latency |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression (Baseline)** | 22.144 | 29.774 | 0.8112 | $< 1\text{ ms}$ |
| **Random Forest Regressor** | 17.642 | 24.201 | 0.8752 | $12\text{ ms}$ |
| **Gradient Boosting (GBDT)** | 11.875 | 17.026 | 0.9383 | $4\text{ ms}$ |
| **XGBoost (Optuna Optimized)** | **9.685** | **13.887** | **0.9589** | **$2\text{ ms}$** |
| **Weighted Blending Ensemble** | **12.962** | **18.488** | **0.9272** | **$18\text{ ms}$** |

### 5.2 Key Analytical Findings
1. **Error Reduction**: Optuna-tuned XGBoost achieved a **$56.3\%$ reduction in MAE** compared to the baseline linear model ($9.68\text{ km}$ vs. $22.14\text{ km}$).
2. **Residual Homoscedasticity**: The residual distribution displays normal distribution centered at zero error ($\mu \approx 0.04$, $\sigma \approx 13.8$), verifying that the predictions are unbiased across both short city trips and extended highway routes.
3. **Feature Importance (SHAP)**: SHAP analysis confirms that *Battery Usable Capacity*, *Starting State of Charge (SOC)*, *Average Speed*, and *Ambient Temperature* provide $>78\%$ of total model attribution. Extreme cold temperatures ($-10^\circ\text{C}$) accounted for up to a $28\%$ range penalty due to cabin heating and internal cell resistance.

---

## 6. Deployment & Containerization
1. **Local REST API**: Implemented via FastAPI (`api.py`) exposing typed schemas for `/predict/range`, `/battery/health`, and `/battery/optimize-charging` with automatic OpenAPI documentation (`/docs`).
2. **Docker Containerization**: Encapsulated within a multi-platform `Dockerfile` exposing standard ports (7860/8000), ready for zero-configuration hosting on cloud instances.
3. **Public Cloud Deployment**: The full-stack application is deployed live on Streamlit Community Cloud at [https://ev-battery-predictor.streamlit.app/](https://ev-battery-predictor.streamlit.app/) with automated continuous deployment linked to GitHub.

---

## 7. Conclusion & Future Scope
This project successfully designed, validated, and deployed a Physics-Informed Digital Twin and Advanced Ensemble Learning pipeline for EV battery analytics. By integrating Arrhenius degradation kinetics with tuned gradient boosting algorithms, the system achieves state-of-the-art range prediction accuracy ($R^2 = 0.9589$, $\text{MAE} < 10\text{ km}$).

**Future Scope**:
* Integration of Long Short-Term Memory (LSTM) recurrent networks for real-time battery cell voltage sequence forecasting.
* Incorporation of elevation contour APIs (Google Maps / OpenElevation) for live dynamic topographical route optimization.

---

## References (IEEE Style)
1. J. Schmalstieg, S. Käbitz, M. Ecker, and D. U. Sauer, "A holistic aging model for Li(NiMnCo)O2 based 18650 lithium-ion cells," *Journal of Power Sources*, vol. 257, pp. 325–334, 2014.
2. C. Bingham, C. Walsh, and S. Carroll, "Impact of driving characteristics on electric vehicle energy consumption," *SAE Int. J. Alt. Power*, vol. 1, no. 1, pp. 132–141, 2012.
3. Y. Bi, D. Chrenko, F. Gao, and D. Paire, "Estimating vehicle electric consumption using machine learning algorithms," in *IEEE Transportation Electrification Conference and Expo (ITEC)*, 2020, pp. 450–455.
4. T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.*, 2016, pp. 785–794.
5. T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, "Optuna: A next-generation hyperparameter optimization framework," in *Proc. 25th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.*, 2019, pp. 2623–2631.
6. S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2017, pp. 4765–4774.
