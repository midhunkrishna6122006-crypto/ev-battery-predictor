# VOLTWISE
## Electric Vehicle Driving Range Optimization
### Using Physics-Informed Battery Digital Twin and ML Ensembles
**Advanced Machine Learning Lab – CAT II Mini Project**  
**M.Sc. AI & ML, Coimbatore Institute of Technology, Coimbatore**

---

### Abstract
VoltWise presents a simple and explainable machine learning framework for electric vehicle (EV) driving range prediction and battery health estimation. The system utilizes 81,000+ real-world battery telemetry records covering 5,000 driving trips across varying weather, speed, and driving styles. Battery State of Health (SOH) and Remaining Useful Life (RUL) are estimated using a physics-informed degradation model based on thermal and cycle stress. In parallel, driving range is predicted using a weighted regression ensemble combining Random Forest, Gradient Boosting (GBDT), and an Optuna-tuned XGBoost model. The pipeline includes outlier cleaning, domain feature engineering, and SHAP-based feature interpretation. Compared with baseline linear regression, the tuned XGBoost model reduces prediction error by 56.3%, achieving a Mean Absolute Error (MAE) of 9.68 km and an R2 score of 0.9589. The system is packaged with a FastAPI backend and an interactive dashboard for practical testing.

---

### 1. Problem Definition and Objectives
Standard on-board vehicle dashboards estimate driving range using static average energy consumption, which frequently causes severe prediction errors during extreme cold or hot weather, high air-conditioning usage, and aggressive driving styles [1], [2]. Simultaneously, lithium-ion battery packs lose storage capacity over time due to ambient temperature shifts and repeated charge-discharge cycles [3]. Most traditional machine learning range predictors assume the battery is in factory-new condition, completely ignoring capacity fade.

VoltWise resolves this critical gap by combining a physical battery digital twin with machine learning range prediction. The core objectives are:
1. Clean and curate an EV telemetry dataset with outlier filtering and domain-specific feature engineering.
2. Estimate battery State of Health (SOH) and Remaining Useful Life (RUL) using physical degradation laws.
3. Train and compare machine learning regressors (Linear Regression, Random Forest, GBDT, and XGBoost) to forecast real-world driving range.
4. Identify which vehicle and ambient factors most influence range using SHAP feature attributions.
5. Provide a simple FastAPI REST service and an interactive interface for real-time testing.

---

### 2. Dataset and Preprocessing
The project uses real-world telemetry data containing 81,000+ sensor readings processed into 5,000 distinct trip cycles with 14 vehicle and environmental features. Sensor anomalies, charging noise, and extreme current spikes were clipped using the standard 1.5x IQR rule. The dataset was partitioned 70% for training, 15% for validation, and 15% for final evaluation using a stratified protocol. All continuous inputs were standardized strictly on training data statistics to prevent data leakage.

#### Table 1. Dataset summary
| Variable / Dataset | Value | Role |
| :--- | :--- | :--- |
| Telemetry observations | 81,000+ sensor records | Battery voltage, current, and temperature telemetry |
| Driving trip instances | 5,000 trips | Input observations for range regression modeling |
| Vehicle & weather features | 14 attributes | Speed, SOC, temperature, humidity, wind, elevation, AC |
| Engineered features | 40+ attributes | Usable energy, weather severity index, interaction terms |
| Train / validation / test | 70% / 15% / 15% | Stratified evaluation protocol (3,500 / 750 / 750 trips) |
| Target variable | Real range (km) | Continuous ground-truth target for regression |

Key engineered features include Usable Energy ($E_{\text{usable}} = \text{Capacity} \times \text{SOH} \times \text{SOC}$) and a Weather Severity Index combining precipitation, headwind velocity, and ambient temperature deviations from the optimal 22°C operating window.

---

### 3. VoltWise System Architecture
```
[Input: Telemetry & Weather] 
       -> [Dual branch: Physics Twin + ML Models] 
       -> [Weighted Ensemble: 0.35 RF + 0.35 GBDT + 0.20 XGB + 0.10 Lin] 
       -> [Serving: FastAPI REST Service] 
       -> [Output: Range (km), SOH %, RUL]
```
*Figure 1. VoltWise pipeline: dual-branch processing, ensemble prediction, and output generation.*

The physics digital twin calculates cumulative battery capacity loss ($D$) and State of Health (SOH) based on calendar aging days, full equivalent cycle count, and operating temperature $T$ (°C) accelerated by Arrhenius kinetics:

$$D = (k_{\text{cal}} \times \text{days} + k_{\text{cyc}} \times \text{cycles}) \times \exp\left(k_{\text{temp}} \times \frac{T - 25}{25}\right) \quad (1)$$

$$\text{SOH} = \max(0.70, 1.0 - D) \quad (2)$$

Empirical calibration parameters are set to $k_{\text{cal}} = 0.00015\text{ day}^{-1}$, $k_{\text{cyc}} = 0.00028\text{ cycle}^{-1}$, and thermal coefficient $k_{\text{temp}} = 0.0693$. Remaining Useful Life (RUL) represents estimated calendar days until the battery reaches the standard automotive retirement threshold ($\text{SOH} = 0.70$). Driving range ($y_{\text{pred}}$) is synthesized by combining individual model outputs:

$$y_{\text{pred}} = 0.35 \times y_{\text{RF}} + 0.35 \times y_{\text{GBDT}} + 0.20 \times y_{\text{XGB}} + 0.10 \times y_{\text{Linear}} \quad (3)$$

---

### 4. Machine Learning Methodology
Four machine learning regressors are evaluated:
- **A. Linear Regression (Baseline):** Ordinary Least Squares baseline reference.
- **B. Random Forest:** 200 unpruned trees with bootstrap sampling and random feature subspacing.
- **C. Gradient Boosted Decision Trees (GBDT):** 250 sequential estimators optimizing residual errors at learning rate 0.05.
- **D. XGBoost (Optuna Tuned):** Second-order Taylor loss approximation with L2 regularization ($\lambda = 1.5$), maximum tree depth of 5, and learning rate of 0.04 tuned over 50 Optuna trials to minimize validation MAE [5].
- **E. Blending Ensemble:** Weighted combination of all four models (0.35 RF + 0.35 GBDT + 0.20 XGB + 0.10 Linear).

Model accuracy is evaluated using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and coefficient of determination ($R^2$ score). Model explainability is quantified using SHAP (SHapley Additive exPlanations) values [6].

---

### 5. Results and Comparative Analysis
The experimental dataset was partitioned into three distinct subsets with no temporal or vehicle overlap:

#### Table 2. Dataset partition summary
| Partition | Samples | Description |
| :--- | :---: | :--- |
| Training set (70%) | 3,500 trips | Model parameter learning and tree split construction |
| Validation set (15%) | 750 trips | Optuna hyperparameter optimization and blending weight tuning |
| Test set (15%) | 750 trips | Final evaluation on unseen, held-out vehicle telemetry |

#### Table 3. Test-set model comparison (evaluated on held-out test set)
| Model Architecture | MAE (km) | RMSE (km) | R2 Score | Latency | Rank |
| :--- | :---: | :---: | :---: | :---: | :---: |
| A. Linear Regression (Baseline) | 22.144 | 29.774 | 0.8112 | < 1 ms | 5 |
| B. Random Forest | 17.642 | 24.201 | 0.8752 | 12 ms | 4 |
| C. Gradient Boosting (GBDT) | 11.875 | 17.026 | 0.9383 | 4 ms | 3 |
| D. XGBoost (Optuna Tuned) | 9.685 | 13.887 | 0.9589 | 2 ms | 1 (Best) |
| E. Weighted Blending Ensemble | 12.962 | 18.488 | 0.9272 | 18 ms | 2 |

*Figure 2. Model comparison: MAE error reduction and R2 score across baseline and ensemble models.*

#### Detailed Key Findings and Performance Analysis:
1. **Significant Error Reduction:** The Optuna-tuned XGBoost model achieved a Mean Absolute Error of 9.685 km and an $R^2$ of 0.9589 on the test partition. This performance corresponds to a **56.3% reduction in error** relative to standard Linear Regression (MAE 22.144 km). Gradient Boosting (GBDT) also proved strong with an MAE of 11.875 km, demonstrating that non-linear decision boundaries are essential for modeling non-linear battery discharge behavior.
2. **Real-Time Inference Latency:** Single-sample inference latency for XGBoost is approximately 2 ms, compared to 12 ms for Random Forest and 18 ms for the weighted blending ensemble. This confirms that XGBoost is exceptionally well-suited for high-frequency deployment directly on edge automotive microcontrollers and in-vehicle telematics units where compute cycles and RAM are constrained.
3. **Physics Digital Twin Integration:** Traditional range prediction algorithms estimate range purely from instantaneous energy consumption. By injecting SOH and usable capacity from the physics digital twin into the feature matrix, the model properly penalizes range predictions on aged battery packs, avoiding catastrophic battery depletion before reaching a charging station.
4. **Blending Ensemble Robustness:** While single-model XGBoost attained the lowest absolute error, the 4-model weighted ensemble (MAE 12.962 km, $R^2$ 0.9272) provides valuable regularization against sensor outliers, ensuring robust fallbacks under anomalous driving profiles.
5. **Environmental Degradation Dynamics:** Telemetry evaluation under extreme weather demonstrates that driving at -10°C increases energy draw by 28% compared to standard 22°C conditions. In contrast, high-speed highway cruising above 90 km/h increases aerodynamic drag losses quadratically, underscoring the necessity of dynamic environmental inputs.

---

### Feature Importance and Model Interpretability
To verify model trustworthiness and understand feature contributions, Tree SHAP was computed across the test instances:

*Figure 3. SHAP feature importance ranking: Usable capacity, SOC, speed, and ambient temperature dominance.*

**SHAP Interpretability Insights:** Battery Usable Capacity, State of Charge (SOC), Vehicle Speed, and Ambient Temperature account for over 78% of the total predictive power. Ambient temperature exhibits pronounced non-linear effects: cold temperatures (-10°C) reduce predicted range by up to 28% due to elevated internal cell resistance and cabin heating loads, while moderate temperatures (20–25°C) maximize efficiency.

---

### 6. Deployment and System Architecture
The complete predictive pipeline is packaged for practical hard-copy demonstration and real-world deployment:
1. **FastAPI REST Service:** Production-ready backend with Pydantic schema validation enforcing physical input bounds (temperature between -20°C and 50°C; SOC between 0% and 100%). Provides modular endpoints for real-time range estimation, SOH calculation, and safe charging advice with automatic documentation.
2. **Containerization:** Packaged using a reproducible Dockerfile containing the lightweight Python runtime, dependencies, and serialized model weights for cross-platform portability.
3. **Interactive Dashboard:** An intuitive web interface allows operators and drivers to dynamically simulate trip variables, temperature shifts, and payload changes, observing instantaneous range predictions and battery health indicators.

---

### 7. Conclusion and Future Scope
VoltWise demonstrates that integrating a physical battery degradation digital twin with machine learning regression significantly improves EV driving range prediction accuracy. The Optuna-tuned XGBoost model achieved an MAE of 9.685 km and an $R^2$ score of 0.9589, representing a 56.3% error reduction over baseline linear methods with an inference latency of just 2 ms.

**Future Scope:** Future extensions include deploying Long Short-Term Memory (LSTM) recurrent networks for continuous cell voltage tracking, and integrating road elevation gradients from digital mapping services for dynamic elevation-aware energy optimization.

---

### References
[1] C. Bingham, C. Walsh, and S. Carroll, "Impact of driving characteristics on electric vehicle energy consumption," *SAE Int. J. Alt. Power*, vol. 1, no. 1, pp. 132–141, 2012.  
[2] Y. Bi, D. Chrenko, F. Gao, and D. Paire, "Estimating vehicle electric consumption using machine learning algorithms," in *Proc. IEEE Transportation Electrification Conf. and Expo (ITEC)*, 2020, pp. 450–455.  
[3] J. Schmalstieg, S. Kabitz, M. Ecker, and D. U. Sauer, "A holistic aging model for Li(NiMnCo)O2 based 18650 lithium-ion cells," *Journal of Power Sources*, vol. 257, pp. 325–334, 2014.  
[4] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.*, 2016, pp. 785–794.  
[5] T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, "Optuna: A next-generation hyperparameter optimization framework," in *Proc. 25th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.*, 2019, pp. 2623–2631.  
[6] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Proc. Advances in Neural Information Processing Systems (NeurIPS)*, 2017, pp. 4765–4774.
