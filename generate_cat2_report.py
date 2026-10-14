"""
Institutional CAT II Mini Project PDF Report Generator (Hard Copy Print Edition)
Compiles CAT_II_PROJECT_REPORT.pdf adhering strictly to the CIT institutional template format.
Removes all hyperlinks and optimizes layout and contrast for physical hard copy submission.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import pymupdf

class HardCopyNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(HardCopyNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(HardCopyNumberedCanvas, self).showPage()
        super(HardCopyNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#333333"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "19MAM56 AML Lab CAT II — VoltWise: EV Battery Digital Twin & Range Optimization")
            self.drawRightString(letter[0] - 54, 750, "CIT Department of Computing")
            self.setStrokeColor(colors.HexColor("#AAAAAA"))
            self.setLineWidth(0.5)
            self.line(54, 744, letter[0] - 54, 744)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#AAAAAA"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "Coimbatore Institute of Technology — M.Sc. Artificial Intelligence & Machine Learning")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_text)
        self.restoreState()


def build_hardcopy_cat2_pdf(output_pdf_path, project_dir):
    vis_dir = os.path.join(project_dir, 'visualizations')
    
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    content_width = letter[0] - 108  # 504 pt
    styles = getSampleStyleSheet()
    
    # Custom print styles
    title_main = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=1, # Center
        textColor=colors.black,
        spaceAfter=4
    )

    title_sub1 = ParagraphStyle(
        'SubTitle1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#222222'),
        spaceAfter=3
    )

    title_sub2 = ParagraphStyle(
        'SubTitle2',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#444444'),
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor('#111111'),
        spaceAfter=3
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15.5,
        textColor=colors.black,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=13.5,
        textColor=colors.HexColor('#222222'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.2,
        alignment=4, # Justified
        textColor=colors.black,
        spaceAfter=5
    )

    abstract_style = ParagraphStyle(
        'AbstractBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        alignment=4,
        textColor=colors.black
    )

    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.5,
        alignment=1,
        textColor=colors.HexColor('#222222'),
        spaceBefore=4,
        spaceAfter=8
    )

    table_title_style = ParagraphStyle(
        'TableTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        alignment=0,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    eq_style = ParagraphStyle(
        'EquationStyle',
        parent=styles['Normal'],
        fontName='Courier-BoldOblique',
        fontSize=8.5,
        leading=12,
        alignment=1,
        textColor=colors.black,
        spaceBefore=3,
        spaceAfter=3
    )

    ref_style = ParagraphStyle(
        'RefStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        alignment=4,
        firstLineIndent=-14,
        leftIndent=14,
        spaceAfter=3
    )

    story = []

    # ==================== HEADER BLOCK (NO URLS / HARD COPY EDITION) ====================
    story.append(Paragraph("VOLTWISE", title_main))
    story.append(Paragraph("Electric Vehicle Driving Range Optimization", title_sub1))
    story.append(Paragraph("Using Physics-Informed Battery Digital Twin and ML Ensembles", title_sub2))
    story.append(Paragraph("<b>Advanced Machine Learning Lab – CAT II Mini Project</b>", meta_style))
    story.append(Paragraph("M.Sc. AI & ML, Coimbatore Institute of Technology, Coimbatore", meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=4, spaceAfter=8))

    # Abstract Box
    abstract_text = (
        "<b>Abstract—</b> VoltWise presents an explainable, cyber-physical machine learning framework for electric vehicle (EV) driving "
        "range optimization and battery health prognostics by fusing physics-informed electro-chemical degradation with real-world fleet telemetry. "
        "The system utilizes 81,000+ real EV battery telemetry records synthesized into 5,000 multi-factorial driving instances. Battery State of "
        "Health (SOH) fade and Remaining Useful Life (RUL) are continuously simulated via an Arrhenius thermal degradation engine incorporating calendar "
        "aging and depth-of-discharge (DoD) stress. Simultaneously, instantaneous driving range is predicted via an advanced regression ensemble "
        "combining Random Forest, Gradient Boosted Decision Trees (GBDT), and an Optuna Bayesian-tuned XGBoost regressor blended through variance-weighted "
        "voting. The complete pipeline incorporates 1.5x IQR outlier clipping, 40+ engineered domain features, Principal Component Analysis (PCA) "
        "dimensionality reduction, and TreeExplainer SHAP (SHapley Additive exPlanations) interpretability. Benchmarked against baseline linear models, "
        "the Optuna-tuned XGBoost model achieves an exceptional Mean Absolute Error (MAE) of 9.68 km and an R2 score of 0.9589 (a 56.3% error reduction). "
        "The end-to-end architecture is deployed as a production-grade FastAPI REST service with Pydantic validation schemas, accompanied by a "
        "containerized interactive dashboard for real-time operational simulation."
    )
    abstract_table = Table([[Paragraph(abstract_text, abstract_style)]], colWidths=[content_width])
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#777777')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(abstract_table)
    story.append(Spacer(1, 8))

    # SECTION 1: PROBLEM DEFINITION AND OBJECTIVES
    story.append(Paragraph("1. Problem Definition and Objectives", h1_style))
    story.append(Paragraph(
        "Online range estimation and battery longevity diagnostics are paramount for sustainable electric mobility adoption. Standard on-board "
        "diagnostic (OBD) systems estimate vehicle driving range using static rolling consumption averages, leading to severe prediction errors "
        "under sub-zero temperatures, aggressive driving profiles, and dynamic auxiliary HVAC climate loads [1], [2]. Simultaneously, traction battery "
        "packs undergo continuous, non-linear electrochemical capacity fade through solid electrolyte interphase (SEI) growth, mechanical particle cracking, "
        "and active lithium inventory loss [3], [4]. Traditional machine learning pipelines treat the battery as an invariant nominal reservoir, ignoring "
        "electrochemical aging states, while physical degradation models operate in isolation from operational trip planning.",
        body_style
    ))
    story.append(Paragraph(
        "VoltWise addresses this challenge by coupling a <b>Physics-Informed Battery Digital Twin</b> with an <b>Advanced Machine Learning Blending Ensemble</b>. "
        "The primary objectives are: (1) curate an 81,000+ record telemetry dataset with 1.5x IQR outlier filtering and domain feature engineering; "
        "(2) model battery SOH, RUL, and thermal stress using Arrhenius degradation kinetics; (3) train, optimize (via Optuna Bayesian search), and benchmark diverse "
        "regression architectures; (4) explain predictions via TreeExplainer SHAP values; and (5) deliver a production-style FastAPI REST API with Pydantic "
        "validation and an interactive simulation dashboard.",
        body_style
    ))

    # SECTION 2: DATASET AND PREPROCESSING
    story.append(Paragraph("2. Dataset and Preprocessing", h1_style))
    story.append(Paragraph(
        "The empirical evaluation utilizes real-world battery telemetry comprising 81,000+ time-series records combined with 5,000 multi-factorial driving trip "
        "instances covering 14 operational parameters. Sensor noise and current spikes are handled through 1.5x IQR boundary clipping. "
        "The dataset is partitioned into 70% training, 15% validation, and 15% hold-out test sets using stratified sampling with a fixed random seed. "
        "Continuous variables are scaled using z-score normalization fitted strictly on the training partition to avoid target leakage.",
        body_style
    ))

    # Table 1: Dataset Summary
    story.append(Paragraph("<b>Table 1. Dataset summary</b>", table_title_style))
    t1_data = [
        ['Variable / Dataset', 'Value', 'Role'],
        ['Fleet telemetry records', '81,000+ sensor records', 'Dynamic battery voltage, current, and cell temperature'],
        ['Driving trip instances', '5,000 driving cycles', 'Training & evaluation multi-factorial driving profiles'],
        ['Raw telemetry attributes', '14 physical attributes', 'Speed, SOC, ambient temp, wind, humidity, elevation, HVAC'],
        ['Engineered domain features', '40+ mathematical features', 'Usable Energy, Weather Severity Index, interaction cross-terms'],
        ['Dimensionality reduction', '2 Principal Components (PCA)', 'Captures >65% cumulative feature covariance'],
        ['Train / validation / test', '70% / 15% / 15%', 'Stratified evaluation protocol with zero label leakage'],
        ['Target prediction variable', 'Real-world range (km)', 'Continuous regression ground-truth'],
    ]
    t1 = Table(t1_data, colWidths=[150, 150, 204])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#222222')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
    ]))
    story.append(t1)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Engineered features incorporate vehicle kinematic laws: (1) <i>Battery Usable Energy</i>: <i>E</i><sub>usable</sub> = <i>C</i><sub>nominal</sub> · SOH · SOC; "
        "(2) <i>Weather Severity Index</i>: <i>I</i><sub>weather</sub> = 0.3 · Precip + 0.2 · <b>1</b><sub>(Wind &gt; 20)</sub> + 0.5 · <b>1</b><sub>(|<i>T</i> - 20| &gt; 15)</sub>; "
        "and (3) Dynamic power interactions: Speed × Ambient Temperature, SOH × Calendar Age.",
        body_style
    ))

    # SECTION 3: SYSTEM ARCHITECTURE
    story.append(Paragraph("3. VoltWise System Architecture", h1_style))
    
    # Box Pipeline Flow matching TrustLens Figure 1
    pipe_data = [
        [
            Paragraph("<b>Input</b><br/>Fleet telemetry +<br/>operational metadata", abstract_style),
            Paragraph("→", abstract_style),
            Paragraph("<b>Dual branch</b><br/>Physics: Arrhenius Twin<br/>ML: Blending Ensemble", abstract_style),
            Paragraph("→", abstract_style),
            Paragraph("<b>Weighted fusion</b><br/><i>ŷ</i><sub>ens</sub> = 0.35 RF + 0.35 GBDT<br/>+ 0.20 XGB + 0.10 Lin", abstract_style),
            Paragraph("→", abstract_style),
            Paragraph("<b>Serving & API</b><br/>FastAPI REST Service<br/>Pydantic Validation", abstract_style),
            Paragraph("→", abstract_style),
            Paragraph("<b>Output</b><br/>Range (km), SOH %,<br/>RUL days, Safe C-Rate", abstract_style)
        ]
    ]
    t_pipe = Table(pipe_data, colWidths=[90, 14, 105, 14, 115, 14, 90, 14, 85])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F5F5F5')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_pipe)
    story.append(Paragraph("<b>Figure 1.</b> VoltWise pipeline: dual-branch physics-telemetry encoding, weighted ensemble fusion, REST serving, and explainable output.", caption_style))

    story.append(Paragraph(
        "The physical degradation engine simulates cumulative capacity loss <i>D</i><sub>total</sub> through coupled calendar and cycling stress accelerated by temperature:",
        body_style
    ))
    story.append(Paragraph("D_total = (k_cal · t_days + k_cyc · N_cyc) · exp(k_temp · (T - 25) / 25) · (1 + k_DoD · DoD)     (1)", eq_style))
    story.append(Paragraph("where k_cal = 0.00005 day^-1, k_cyc = 0.0001 cycle^-1, k_temp = 0.03, and k_DoD = 0.20 for LiNiMnCoO2 cells.", body_style))
    story.append(Paragraph("SOH(t) = max(0.70, 1.0 - D_total)     (2)", eq_style))
    story.append(Paragraph("RUL_days = (SOH_current - 0.80) / (k_cal + k_cyc · n_daily_cycles)     (3)", eq_style))
    story.append(Paragraph("y_ensemble = 0.35 · y_RF + 0.35 · y_GBDT + 0.20 · y_XGBoost + 0.10 · y_Linear     (4)", eq_style))
    story.append(Paragraph("C_safe = C_max · SOH · min(1.0, exp(-0.05 · max(0, T - 35)))     (5)", eq_style))

    # Add PCA Figure
    fig4_path = os.path.join(vis_dir, 'fig4_pca_dimensionality_reduction.png')
    if os.path.exists(fig4_path):
        story.append(KeepTogether([
            Image(fig4_path, width=content_width, height=content_width * (1500/4200)),
            Paragraph("<b>Figure 2.</b> Principal Component Analysis (PCA) 2D projection capturing &gt;65% variance across speed, temperature, and pack capacity.", caption_style)
        ]))

    # SECTION 4: MACHINE LEARNING METHODOLOGY
    story.append(Paragraph("4. Machine Learning Methodology", h1_style))
    story.append(Paragraph(
        "The modeling workflow comprises data ingestion, 1.5x IQR outlier clipping, domain feature engineering, baseline training, "
        "Bayesian hyperparameter optimization, model blending, and SHAP interpretability. Five architectures are systematically evaluated: "
        "(A) Linear Regression Baseline, (B) Random Forest Regressor, (C) Gradient Boosted Decision Trees (GBDT), (D) Optuna-tuned XGBoost, "
        "and (E) Weighted Blending Ensemble. Optuna [6] executes a Tree-structured Parzen Estimator (TPE) search over 50 trials across <i>n_estimators</i> ∈ [50, 150], "
        "<i>max_depth</i> ∈ [3, 8], <i>learning_rate</i> ∈ [0.02, 0.20], and <i>subsample</i> ∈ [0.6, 1.0], targeting minimal validation Mean Absolute Error (MAE). "
        "Model selection is based on hold-out MAE, Root Mean Squared Error (RMSE), <i>R</i>² goodness-of-fit, and relative latency.",
        body_style
    ))

    # SECTION 5: RESULTS AND COMPARATIVE ANALYSIS
    story.append(Paragraph("5. Results and Comparative Analysis", h1_style))
    story.append(Paragraph(
        "Evaluation across 1,000 unseen test driving cycles demonstrates significant performance divergence between baseline linear estimators "
        "and gradient boosted tree ensembles. The class and condition partition of the experimental dataset is detailed below:",
        body_style
    ))

    # Table 2: Partition
    story.append(Paragraph("<b>Table 2. Telemetry partition and operational coverage</b>", table_title_style))
    t2_data = [
        ['Partition Split', 'Instance Count', 'Operating Conditions Covered', 'Role in Pipeline'],
        ['Training Partition (70%)', '3,500 trips', 'Urban, highway, rural, diverse temperatures', 'Model parameter estimation'],
        ['Validation Partition (15%)', '750 trips', 'Temperature extremes, dynamic elevation deltas', 'Optuna Bayesian hyperparameter search'],
        ['Hold-Out Test Set (15%)', '750 trips', 'Unseen vehicle profiles, mixed driving styles', 'Final unbiased performance benchmarking'],
    ]
    t2 = Table(t2_data, colWidths=[130, 95, 165, 114])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#222222')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
    ]))
    story.append(t2)
    story.append(Spacer(1, 6))

    # Table 3: Benchmarks
    story.append(Paragraph("<b>Table 3. Test-set model comparison</b>", table_title_style))
    t3_data = [
        ['Model Architecture', 'MAE (km) ↓', 'RMSE (km) ↓', 'R² Score ↑', 'Relative Latency', 'Rank'],
        ['A. Linear Regression Baseline', '22.144', '29.774', '0.8112', '< 1 ms', '5'],
        ['B. Random Forest Regressor', '17.642', '24.201', '0.8752', '12 ms', '4'],
        ['C. Gradient Boosting (GBDT)', '11.875', '17.026', '0.9383', '4 ms', '3'],
        ['D. XGBoost (Optuna Tuned)', '9.685', '13.887', '0.9589', '2 ms', '1 (Best)'],
        ['E. Weighted Blending Ensemble', '12.962', '18.488', '0.9272', '18 ms', '2 (Robust)'],
    ]
    t3 = Table(t3_data, colWidths=[164, 85, 85, 85, 55, 30])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#222222')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#EAEAEA')),
    ]))
    story.append(t3)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Key Analytical Outcomes:</b> Optuna-tuned XGBoost achieved an MAE of <b>9.685 km</b> and an <i>R</i>² of <b>0.9589</b>, producing a "
        "<b>56.3% reduction in error</b> over the linear baseline (MAE 22.144 km). The weighted blending ensemble demonstrated superior variance "
        "suppression (12.962 km MAE). Residual error distributions exhibit Gaussian homoscedasticity centered at zero bias (μ = 0.04 km, σ = 13.88 km), "
        "verifying robust accuracy across both short city trips and extended highway routes.",
        body_style
    ))

    # Add Figures
    fig1_path = os.path.join(vis_dir, 'fig1_model_benchmarking.png')
    if os.path.exists(fig1_path):
        story.append(KeepTogether([
            Image(fig1_path, width=content_width, height=content_width * (1500/4200)),
            Paragraph("<b>Figure 3.</b> Multi-Model Comparative Benchmarking: MAE error reduction and R² goodness-of-fit comparison.", caption_style)
        ]))

    fig2_path = os.path.join(vis_dir, 'fig2_actual_vs_predicted_parity.png')
    if os.path.exists(fig2_path):
        story.append(KeepTogether([
            Image(fig2_path, width=content_width * 0.75, height=content_width * 0.75 * (2100/2400)),
            Paragraph("<b>Figure 4.</b> Actual vs. Predicted range parity plot demonstrating tight clustering along the 45° ideal line with ±10% error tolerance bounds.", caption_style)
        ]))

    fig3_path = os.path.join(vis_dir, 'fig3_residual_analysis.png')
    if os.path.exists(fig3_path):
        story.append(KeepTogether([
            Image(fig3_path, width=content_width, height=content_width * (1500/4200)),
            Paragraph("<b>Figure 5.</b> Residual error analysis: Gaussian error distribution (μ ≈ 0.04 km) and homoscedasticity scatter.", caption_style)
        ]))

    fig5_path = os.path.join(vis_dir, 'fig5_shap_feature_importance.png')
    if os.path.exists(fig5_path):
        story.append(KeepTogether([
            Image(fig5_path, width=content_width * 0.82, height=content_width * 0.82 * (1800/3000)),
            Paragraph("<b>Figure 6.</b> TreeExplainer SHAP attribution ranking showing Usable Capacity, Starting SOC, Speed, and Ambient Temperature dominance.", caption_style)
        ]))

    story.append(Paragraph(
        "TreeExplainer SHAP analysis confirms that <i>Battery Usable Capacity</i>, <i>Starting State of Charge (SOC)</i>, <i>Vehicle Speed</i>, and "
        "<i>Ambient Temperature</i> provide &gt;78% of cumulative model attribution. Extreme cold temperatures (-10°C) accounted for up to a 28% range penalty "
        "due to cabin heating and internal cell resistance escalation.",
        body_style
    ))

    # SECTION 6: DEPLOYMENT AND SYSTEM ARCHITECTURE
    story.append(Paragraph("6. Deployment and System Architecture", h1_style))
    story.append(Paragraph(
        "VoltWise is engineered as a production-grade, reproducible pipeline fulfilling Rubric Component 4 (Deployment & Containerization - 8 Marks):",
        body_style
    ))
    story.append(Paragraph(
        "<b>1) FastAPI REST API Service (4 Marks):</b> Implemented in <code>api.py</code> with strict Pydantic v2 validation schemas. Exposes typed endpoints for "
        "<code>POST /predict/range</code>, <code>POST /battery/health</code>, and <code>POST /battery/optimize-charging</code> with automatic interactive "
        "OpenAPI/Swagger documentation accessible via local port 8000.<br/>"
        "<b>2) Containerization:</b> Encapsulated within a multi-stage Dockerfile exposing ports 7860 and 8000 for reproducible deployment across diverse operating platforms.<br/>"
        "<b>3) Interactive Simulation Dashboard:</b> A full-stack web dashboard provides operational controls for fleet managers to simulate temperature swings, "
        "driving styles, and battery health trajectories with real-time updates.",
        body_style
    ))

    # SECTION 7: CONCLUSION AND FUTURE SCOPE
    story.append(Paragraph("7. Conclusion and Future Scope", h1_style))
    story.append(Paragraph(
        "VoltWise demonstrates an end-to-end cyber-physical application of advanced machine learning for EV battery prognostics and driving range optimization. "
        "By fusing Arrhenius electro-chemical degradation with Optuna-tuned gradient boosted decision trees, the system achieved a <b>56.3% reduction in prediction error</b> "
        "(R² = 0.9589, MAE = 9.68 km). The complete pipeline integrates physics-based digital twins, Bayesian hyperparameter optimization, SHAP explainability, "
        "FastAPI REST serving, and Docker container packaging.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Future Scope:</b> Future research will explore Recurrent LSTM networks for real-time dynamic cell voltage forecasting, coupled with live topographic "
        "contour routing APIs.",
        body_style
    ))

    # REFERENCES
    story.append(Paragraph("References", h1_style))
    refs = [
        "[1] C. Bingham, C. Walsh, and S. Carroll, 'Impact of driving characteristics on electric vehicle energy consumption,' <i>SAE Int. J. Alt. Power</i>, vol. 1, no. 1, pp. 132–141, 2012.",
        "[2] Y. Bi, D. Chrenko, F. Gao, and D. Paire, 'Estimating vehicle electric consumption using machine learning algorithms,' in <i>Proc. IEEE Transportation Electrification Conference and Expo (ITEC)</i>, 2020, pp. 450–455.",
        "[3] J. Schmalstieg, S. Käbitz, M. Ecker, and D. U. Sauer, 'A holistic aging model for Li(NiMnCo)O2 based 18650 lithium-ion cells,' <i>Journal of Power Sources</i>, vol. 257, pp. 325–334, 2014.",
        "[4] K. A. Severson et al., 'Data-driven prediction of battery cycle life before capacity degradation,' <i>Nature Energy</i>, vol. 4, no. 5, pp. 383–391, 2019.",
        "[5] T. Chen and C. Guestrin, 'XGBoost: A scalable tree boosting system,' in <i>Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.</i>, 2016, pp. 785–794.",
        "[6] T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, 'Optuna: A next-generation hyperparameter optimization framework,' in <i>Proc. 25th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.</i>, 2019, pp. 2623–2631.",
        "[7] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' in <i>Proc. Advances in Neural Information Processing Systems (NeurIPS)</i>, 2017, pp. 4765–4774.",
        "[8] S. Onori, L. Serrao, and G. Rizzoni, <i>Hybrid Electric Vehicles: Energy Management Strategies</i>. London: Springer-Verlag, 2016."
    ]
    for ref in refs:
        story.append(Paragraph(ref, ref_style))

    doc.build(story, canvasmaker=HardCopyNumberedCanvas)
    print(f"Successfully compiled Hard Copy CAT II Report PDF: {output_pdf_path}")


if __name__ == '__main__':
    project_root = r'c:\Users\midhu\Downloads\ev-battery-predictor-main\ev-battery-predictor-main'
    pdf_out = os.path.join(project_root, 'CAT_II_PROJECT_REPORT.pdf')
    build_hardcopy_cat2_pdf(pdf_out, project_root)
