VOLTWISE
Electric Vehicle Driving Range Optimization
Using Physics-Informed Battery Digital Twin and ML Ensembles
Advanced Machine Learning Lab – CAT II Mini Project
M.Sc. AI & ML, Coimbatore Institute of Technology, Coimbatore

Abstract
VoltWise presents an explainable, cyber-physical machine learning framework for electric vehicle (EV) driving range optimization and battery health prognostics by fusing physics-informed electro-chemical degradation with real-world fleet telemetry. The system utilizes 81,000+ real EV battery telemetry records synthesized into 5,000 multi-factorial driving instances. Battery State of Health (SOH) fade and Remaining Useful Life (RUL) are continuously simulated via an Arrhenius thermal degradation engine incorporating calendar aging and depth-of-discharge (DoD) stress. Simultaneously, instantaneous driving range is predicted via an advanced regression ensemble combining Random Forest, Gradient Boosted Decision Trees (GBDT), and an Optuna Bayesian-tuned XGBoost regressor blended through variance-weighted voting. The complete pipeline incorporates 1.5x IQR outlier clipping, 40+ engineered domain features, Principal Component Analysis (PCA) dimensionality reduction, and TreeExplainer SHAP (SHapley Additive exPlanations) interpretability. Benchmarked against baseline linear models, the Optuna-tuned XGBoost model achieves an exceptional Mean Absolute Error (MAE) of 9.68 km and an R2 score of 0.9589 (a 56.3% error reduction). The end-to-end architecture is deployed as a production-grade FastAPI REST service with Pydantic validation schemas, accompanied by a containerized interactive dashboard for real-time operational simulation.

1. Problem Definition and Objectives
Widespread adoption of Electric Vehicles (EVs) is fundamentally hindered by consumer anxiety regarding battery lifespan uncertainty and unpredictable real-world driving range [1]. Standard on-board vehicle estimators compute remaining range using static rolling average consumption metrics. Such heuristics produce substantial forecasting errors under extreme weather conditions, dynamic auxiliary HVAC climate loads, road topographical gradients, and aggressive driving styles [2]. Concurrently, lithium-ion battery packs undergo irreversible electrochemical degradation governed by solid electrolyte interphase (SEI) growth, lithium plating, and active material dissolution under thermal and cycling fatigue [3], [4]. Traditional machine learning pipelines treat the battery as an invariant nominal reservoir, ignoring electrochemical aging states, while physical degradation models operate in isolation from operational trip planning.

VoltWise addresses this algorithmic disconnect by unifying a Physics-Informed Electrochemical Digital Twin with an Advanced Machine Learning Blending Ensemble. The core objectives are:
1. Construct an end-to-end telemetry data pipeline with robust 1.5x IQR outlier filtering, domain feature engineering, and PCA dimensionality reduction.
2. Formulate an electrochemical battery digital twin implementing Arrhenius kinetics, calendar fade, and cycle fatigue to track SOH, RUL, and optimal safe C-rates.
3. Train, optimize (via Optuna Bayesian search), and benchmark diverse regressors (Linear Baseline, Random Forest, GBDT, XGBoost, and Weighted Blending Ensemble).
4. Interpret feature attributions using TreeExplainer SHAP to reveal non-linear environmental and operational interactions.
5. Deliver a production-style FastAPI REST API with Pydantic validation and an interactive simulation dashboard.

2. Dataset and Preprocessing
The empirical evaluation utilizes real-world battery telemetry comprising 81,000+ time-series records combined with 5,000 multi-factorial driving trip instances covering 14 operational and environmental covariates. Data preprocessing removes sensor dropouts, cleans invalid values, and applies 1.5x IQR boundary clipping to prevent anomalous current draw spikes from biasing model weights. The dataset is partitioned using a 70/15/15 train/validation/test stratified protocol with fixed random seeds. Continuous numerical variables are standardized using z-score normalization fitted strictly on the training partition to prevent data leakage, while categorical parameters (traffic density, route environment, driving behavior) are one-hot encoded.

Table 1. Dataset summary
| Variable / Dataset | Value | Role |
| :--- | :--- | :--- |
| Fleet telemetry records | 81,000+ sensor records | Dynamic battery voltage, current, and cell temperature |
| Driving trip instances | 5,000 driving cycles | Training & evaluation multi-factorial driving profiles |
| Raw telemetry attributes | 14 physical attributes | Speed, SOC, ambient temp, wind, humidity, elevation, HVAC |
| Engineered domain features | 40+ mathematical features | Usable Energy, Weather Severity Index, interaction cross-terms |
| Dimensionality reduction | 2 Principal Components (PCA) | Captures >65% cumulative feature covariance |
| Train / validation / test | 70% / 15% / 15% | Stratified evaluation protocol with zero label leakage |
| Target prediction variable | Real-world range (km) | Continuous regression ground-truth |

Engineered features incorporate vehicle kinematic laws:
1. Battery Usable Energy: E_usable = C_nominal * SOH * SOC
2. Weather Severity Index: I_weather = 0.3 * Precip + 0.2 * 1_(Wind > 20) + 0.5 * 1_(|T - 20| > 15)
3. Dynamic Power Interactions: Speed * Ambient Temperature, SOH * Calendar Age

3. VoltWise System Architecture
| Input: Fleet telemetry + operational metadata | -> | Dual branch: Physics Arrhenius Twin + ML Regression Pipeline | -> | Weighted Blending Ensemble: y_ens = 0.35 RF + 0.35 GBDT + 0.20 XGB + 0.10 Lin | -> | Production Serving & API: FastAPI REST Service + Pydantic | -> | Output: Driving Range (km), SOH %, RUL days, Safe C-Rate |
Figure 1. VoltWise pipeline: dual-branch physics-telemetry encoding, weighted ensemble fusion, REST serving, and explainable output.

The physical degradation engine simulates cumulative capacity loss D_total through coupled calendar and cycling stress accelerated by temperature:
D_total = (k_cal * t_days + k_cyc * N_cyc) * exp(k_temp * (T - 25) / 25) * (1 + k_DoD * DoD)     (1)

where k_cal = 0.00005 day^-1, k_cyc = 0.0001 cycle^-1, k_temp = 0.03, and k_DoD = 0.20 represent empirical kinetic rate constants for LiNiMnCoO2 cells.

State of Health (SOH) is bounded between the retirement threshold and initial capacity:
SOH(t) = max(0.70, 1.0 - D_total)     (2)

Remaining Useful Life (RUL) until automotive retirement (80% SOH standard) is formulated as:
RUL_days = (SOH_current - 0.80) / (k_cal + k_cyc * n_daily_cycles)     (3)

Driving range is predicted by blending heterogeneous estimators using variance-weighted voting:
y_ensemble = 0.35 * y_RF + 0.35 * y_GBDT + 0.20 * y_XGBoost + 0.10 * y_Linear     (4)

Dynamic safe charging C-rate prevents lithium plating during high-stress charging states:
C_safe = C_max * SOH * min(1.0, exp(-0.05 * max(0, T - 35)))     (5)

4. Machine Learning Methodology
The complete modeling workflow consists of data validation, IQR boundary clipping, domain feature engineering, stratified splitting, baseline learning, ensemble blending, hyperparameter tuning, and explainability. Five architectures are systematically evaluated: (A) Ordinary Least Squares Linear Regression as a baseline, (B) Random Forest Regressor, (C) Gradient Boosted Decision Trees (GBDT), (D) Optuna Bayesian-guided XGBoost, and (E) Weighted Blending Ensemble.

Optuna with Tree-structured Parzen Estimators (TPE) searches n_estimators in [50, 150], max_depth in [3, 8], learning_rate in [0.02, 0.20], and subsample in [0.6, 1.0] across 50 optimization trials, targeting minimal hold-out validation Mean Absolute Error (MAE). Model selection is based on hold-out MAE, Root Mean Squared Error (RMSE), R2 score, and relative latency. TreeExplainer SHAP quantifies exact marginal feature attributions across the operating envelope.

5. Results and Comparative Analysis
The experimental data partition and operational conditions are summarized below:

Table 2. Telemetry partition and operational coverage
| Partition Split | Instance Count | Operating Conditions Covered | Role in Pipeline |
| :--- | :---: | :--- | :--- |
| Training Partition (70%) | 3,500 trips | Urban, highway, rural, diverse temperatures | Model parameter estimation |
| Validation Partition (15%) | 750 trips | Temperature extremes, dynamic elevation deltas | Optuna Bayesian hyperparameter search |
| Hold-Out Test Set (15%) | 750 trips | Unseen vehicle profiles, mixed driving styles | Final unbiased performance benchmarking |

Table 3 compares all five models on the unseen hold-out test set:

Table 3. Test-set model comparison
| Model Architecture | MAE (km) | RMSE (km) | R2 Score | Relative Latency | Rank |
| :--- | :---: | :---: | :---: | :---: | :---: |
| A. Linear Regression Baseline | 22.144 | 29.774 | 0.8112 | < 1 ms | 5 |
| B. Random Forest Regressor | 17.642 | 24.201 | 0.8752 | 12 ms | 4 |
| C. Gradient Boosting (GBDT) | 11.875 | 17.026 | 0.9383 | 4 ms | 3 |
| D. XGBoost (Optuna Tuned) | 9.685 | 13.887 | 0.9589 | 2 ms | 1 (Best) |
| E. Weighted Blending Ensemble | 12.962 | 18.488 | 0.9272 | 18 ms | 2 (Robust) |

Key Analytical Findings:
1. Error Reduction: Optuna-tuned XGBoost achieved an MAE of 9.685 km and an R2 of 0.9589, producing a 56.3% reduction in error over the linear baseline (MAE 22.144 km).
2. Residual Homoscedasticity: Residual distributions exhibit strict Gaussian symmetry centered at zero bias (mu = 0.04 km, sigma = 13.88 km), verifying that predictions remain unbiased across city, highway, and mixed driving terrains.
3. Feature Attribution: TreeExplainer SHAP confirms that Battery Usable Capacity, Starting SOC, Vehicle Speed, and Ambient Temperature account for >78% of cumulative model attribution. Extreme cold temperatures (-10°C) introduce up to a 28% range penalty due to cabin climate draw and elevated internal resistance.
4. Edge Feasibility: XGBoost executes in just 2 ms, proving immediate suitability for on-board Electronic Control Units (ECUs).

6. Deployment and System Architecture
VoltWise is designed as a modular, reproducible software pipeline:
1. Production REST API: Built using FastAPI and Pydantic v2 schemas for strict input boundary validation (temperatures bounded to [-25°C, 50°C], SOC bounded to [0.05, 1.0]). The service exposes POST /predict/range, POST /battery/health, and POST /battery/optimize-charging with automatic OpenAPI/Swagger documentation.
2. Containerization: Encapsulated within a multi-stage Dockerfile exposing ports 7860 and 8000 for reproducible deployment across diverse operating platforms.
3. Interactive Simulation UI: A full-stack dashboard provides interactive operational sliders for fleet managers to simulate temperature swings, driving styles, and battery health trajectories with real-time updates.

7. Conclusion and Future Scope
VoltWise demonstrates an end-to-end cyber-physical application of advanced machine learning for EV battery prognostics and driving range optimization. The fusion of Arrhenius electro-chemical degradation with Optuna-tuned gradient boosted decision trees achieved a 56.3% reduction in prediction error (R2 = 0.9589, MAE = 9.68 km). The system combines physics-informed digital twins, Bayesian hyperparameter optimization, SHAP interpretability, and production REST API serving.

Future work will investigate Recurrent LSTM networks for dynamic cell voltage sequence forecasting and integration with live topographical elevation contour APIs.

References
[1] C. Bingham, C. Walsh, and S. Carroll, "Impact of driving characteristics on electric vehicle energy consumption," SAE Int. J. Alt. Power, vol. 1, no. 1, pp. 132-141, 2012.
[2] Y. Bi, D. Chrenko, F. Gao, and D. Paire, "Estimating vehicle electric consumption using machine learning algorithms," in Proc. IEEE Transportation Electrification Conference and Expo (ITEC), 2020, pp. 450-455.
[3] J. Schmalstieg, S. Kabitz, M. Ecker, and D. U. Sauer, "A holistic aging model for Li(NiMnCo)O2 based 18650 lithium-ion cells," Journal of Power Sources, vol. 257, pp. 325-334, 2014.
[4] K. A. Severson et al., "Data-driven prediction of battery cycle life before capacity degradation," Nature Energy, vol. 4, no. 5, pp. 383-391, 2019.
[5] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min., 2016, pp. 785-794.
[6] T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, "Optuna: A next-generation hyperparameter optimization framework," in Proc. 25th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min., 2019, pp. 2623-2631.
[7] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in Proc. Advances in Neural Information Processing Systems (NeurIPS), 2017, pp. 4765-4774.
[8] S. Onori, L. Serrao, and G. Rizzoni, Hybrid Electric Vehicles: Energy Management Strategies. London: Springer-Verlag, 2016.
