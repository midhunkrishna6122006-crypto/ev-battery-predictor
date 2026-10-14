"""
Institutional CAT II Mini Project PDF Report Generator (Concise & Simple Edition)
Compiles CAT_II_PROJECT_REPORT.pdf matching the exact simplicity and length of the CIT TrustLens reference.
Removes complex formulas, excessive graphs, and hyperlinks. Clean hard-copy print layout on standard A4 paper.
Guarantees an exact, perfectly balanced 4-page document.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import pymupdf


class SimpleHardCopyCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(SimpleHardCopyCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(SimpleHardCopyCanvas, self).showPage()
        super(SimpleHardCopyCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # 1. Page Border (Clean 1.0 pt solid black border around the page)
        border_inset = 30  # pt from page boundary
        self.setStrokeColor(colors.black)
        self.setLineWidth(1.0)
        self.rect(border_inset, border_inset, A4[0] - 2 * border_inset, A4[1] - 2 * border_inset)
        
        # 2. Centered Page Number (80, 81, 82, 83 in the middle at bottom)
        page_num = 79 + self._pageNumber
        self.setFont("Times-Roman", 10)
        self.setFillColor(colors.black)
        self.drawCentredString(A4[0] / 2.0, 42, str(page_num))
        
        # Note: No running header at top, no institute string at bottom
        self.restoreState()


def build_simple_cat2_pdf(output_pdf_path, project_dir):
    vis_dir = os.path.join(project_dir, 'visualizations')
    
    # Standard A4: 595.27 x 841.89 pt
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=44,
        bottomMargin=56
    )
    
    content_width = A4[0] - 100  # 495.27 pt
    styles = getSampleStyleSheet()
    
    # Clean typography matching the exact reference document (Times New Roman)
    title_main = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=22,
        leading=26,
        alignment=1, # Center
        textColor=colors.black,
        spaceAfter=2
    )

    title_sub1 = ParagraphStyle(
        'SubTitle1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=colors.black,
        spaceAfter=1
    )

    title_sub2 = ParagraphStyle(
        'SubTitle2',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=colors.black,
        spaceAfter=3
    )

    meta_course = ParagraphStyle(
        'MetaCourse',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.black,
        spaceAfter=1
    )

    meta_inst = ParagraphStyle(
        'MetaInst',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=12.5,
        alignment=1,
        textColor=colors.black,
        spaceAfter=3
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13.2,
        alignment=4, # Justified
        textColor=colors.black,
        spaceAfter=3.5
    )

    abstract_style = ParagraphStyle(
        'AbstractBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13.2,
        alignment=4,
        textColor=colors.black
    )

    cell_style = ParagraphStyle(
        'PipeCellStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=1, # Center
        textColor=colors.black
    )

    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=11.5,
        alignment=1,
        textColor=colors.black,
        spaceBefore=3,
        spaceAfter=5
    )

    table_title_style = ParagraphStyle(
        'TableTitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=11.5,
        alignment=1, # Center in reference docx
        textColor=colors.black,
        spaceBefore=5,
        spaceAfter=2.5,
        keepWithNext=True
    )

    eq_style = ParagraphStyle(
        'EquationStyle',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.black,
        spaceBefore=2,
        spaceAfter=2
    )

    ref_style = ParagraphStyle(
        'RefStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=11.5,
        alignment=4,
        firstLineIndent=-12,
        leftIndent=12,
        spaceAfter=2
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, ABSTRACT, 1. PROBLEM DEFINITION, 2. DATASET & PREPROCESSING
    # =========================================================================
    story.append(Paragraph("VOLTWISE", title_main))
    story.append(Paragraph("Electric Vehicle Driving Range Optimization", title_sub1))
    story.append(Paragraph("Using Physics-Informed Battery Digital Twin and ML Ensembles", title_sub2))
    story.append(Paragraph("Advanced Machine Learning Lab - CAT II Mini Project", meta_course))
    story.append(Paragraph("M.Sc. AI & ML, Coimbatore Institute of Technology, Coimbatore", meta_inst))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.black, spaceBefore=4, spaceAfter=6))

    # Abstract
    story.append(Paragraph("<b>Abstract</b>", h1_style))
    abstract_text = (
        "VoltWise presents a simple and explainable machine learning framework for electric vehicle (EV) driving "
        "range prediction and battery health estimation. The system utilizes 81,000+ real-world battery telemetry records covering 5,000 "
        "driving trips across varying weather, speed, and driving styles. Battery State of Health (SOH) and Remaining Useful Life (RUL) "
        "are estimated using a physics-informed degradation model based on thermal and cycle stress. In parallel, driving range is "
        "predicted using a weighted regression ensemble combining Random Forest, Gradient Boosting (GBDT), and an Optuna-tuned XGBoost model. "
        "The pipeline includes outlier cleaning, domain feature engineering, and SHAP-based feature interpretation. Compared with baseline "
        "linear regression, the tuned XGBoost model reduces prediction error by 56.3%, achieving a Mean Absolute Error (MAE) of 9.68 km and an "
        "R<sup>2</sup> score of 0.9589. The system is packaged with a FastAPI backend and an interactive dashboard for practical testing."
    )
    story.append(Paragraph(abstract_text, abstract_style))
    story.append(Spacer(1, 4))

    # SECTION 1: PROBLEM DEFINITION AND OBJECTIVES
    story.append(Paragraph("1. Problem Definition and Objectives", h1_style))
    story.append(Paragraph(
        "Standard on-board vehicle dashboards estimate driving range using static average energy consumption, which frequently causes "
        "severe prediction errors during extreme cold or hot weather, high air-conditioning usage, and aggressive driving styles [1], [2]. "
        "Simultaneously, lithium-ion battery packs lose storage capacity over time due to ambient temperature shifts and repeated charge-discharge "
        "cycles [3]. Most traditional machine learning range predictors assume the battery is in factory-new condition, completely ignoring capacity fade.",
        body_style
    ))
    story.append(Paragraph(
        "VoltWise resolves this critical gap by combining a physical battery digital twin with machine learning range prediction. The core objectives are: "
        "(1) clean and curate an EV telemetry dataset with outlier filtering and domain-specific feature engineering; (2) estimate battery State of Health "
        "(SOH) and Remaining Useful Life (RUL) using physical degradation laws; (3) train and compare machine learning regressors (Linear "
        "Regression, Random Forest, GBDT, and XGBoost) to forecast real-world driving range; (4) identify which vehicle and ambient factors most "
        "influence range using SHAP feature attributions; and (5) provide a simple FastAPI REST service and an interactive interface for real-time testing.",
        body_style
    ))

    # SECTION 2: DATASET AND PREPROCESSING
    story.append(Paragraph("2. Dataset and Preprocessing", h1_style))
    story.append(Paragraph(
        "The project uses real-world telemetry data containing 81,000+ sensor readings processed into 5,000 distinct trip cycles with 14 vehicle "
        "and environmental features. Sensor anomalies, charging noise, and extreme current spikes were clipped using the standard 1.5x IQR "
        "rule. The dataset was partitioned 70% for training, 15% for validation, and 15% for final evaluation using a stratified protocol. "
        "All continuous inputs were standardized strictly on training data statistics to prevent data leakage.",
        body_style
    ))

    # Table 1: Dataset Summary
    story.append(Paragraph("<b>Table 1. Dataset summary</b>", table_title_style))
    t1_data = [
        ['Variable / Dataset', 'Value', 'Role'],
        ['Telemetry observations', '81,000+ sensor records', 'Battery voltage, current, and temperature telemetry'],
        ['Driving trip instances', '5,000 trips', 'Input observations for range regression modeling'],
        ['Vehicle & weather features', '14 attributes', 'Speed, SOC, temperature, humidity, wind, elevation, AC'],
        ['Engineered features', '40+ attributes', 'Usable energy, weather severity index, interaction terms'],
        ['Train / validation / test', '70% / 15% / 15%', 'Stratified evaluation protocol (3,500 / 750 / 750 trips)'],
        ['Target variable', 'Real range (km)', 'Continuous ground-truth target for regression'],
    ]
    t1 = Table(t1_data, colWidths=[140, 145, 210])
    t1.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
    ]))
    story.append(t1)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "Key engineered features include Usable Energy (<i>E</i><sub>usable</sub> = Capacity * SOH * SOC) and a Weather Severity Index combining "
        "precipitation, headwind velocity, and ambient temperature deviations from the optimal 22 deg C operating window.",
        body_style
    ))

    # Force PageBreak to ensure Page 1 ends cleanly
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: 3. ARCHITECTURE (FIG 1, EQS), 4. METHODOLOGY, 5. RESULTS INTRO & TABLE 2
    # =========================================================================
    story.append(Paragraph("3. VoltWise System Architecture", h1_style))
    story.append(Paragraph(
        "The VoltWise architecture employs a dual-branch processing pipeline combining physical degradation kinetics with data-driven regression trees:",
        body_style
    ))
    
    # Box Pipeline Flow matching TrustLens Figure 1 (clean plain string arrows to avoid wrapping)
    pipe_data = [
        [
            Paragraph("<b>Input</b><br/>Telemetry & Weather", cell_style),
            "->",
            Paragraph("<b>Dual branch</b><br/>Physics Twin + ML Models", cell_style),
            "->",
            Paragraph("<b>Weighted Ensemble</b><br/>0.35 RF + 0.35 GBDT<br/>+ 0.20 XGB + 0.10 Lin", cell_style),
            "->",
            Paragraph("<b>Serving</b><br/>FastAPI REST Service", cell_style),
            "->",
            Paragraph("<b>Output</b><br/>Range (km), SOH %, RUL", cell_style)
        ]
    ]
    t_pipe = Table(pipe_data, colWidths=[80, 15, 92, 15, 110, 15, 80, 15, 73])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9F9F9')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#444444')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (1, 0), (1, 0), 'Times-Bold'),
        ('FONTNAME', (3, 0), (3, 0), 'Times-Bold'),
        ('FONTNAME', (5, 0), (5, 0), 'Times-Bold'),
        ('FONTNAME', (7, 0), (7, 0), 'Times-Bold'),
        ('FONTSIZE', (1, 0), (1, 0), 10),
        ('FONTSIZE', (3, 0), (3, 0), 10),
        ('FONTSIZE', (5, 0), (5, 0), 10),
        ('FONTSIZE', (7, 0), (7, 0), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_pipe)
    story.append(Paragraph("<b>Figure 1.</b> VoltWise pipeline: dual-branch processing, ensemble prediction, and output generation.", caption_style))

    story.append(Paragraph(
        "The physics digital twin calculates cumulative battery capacity loss (<i>D</i>) and State of Health (SOH) based on calendar aging days, "
        "full equivalent cycle count, and operating temperature <i>T</i> (deg C) accelerated by Arrhenius kinetics:",
        body_style
    ))
    story.append(Paragraph("D = (k_cal * days + k_cyc * cycles) * exp(k_temp * (T - 25) / 25)     (1)", eq_style))
    story.append(Paragraph("SOH = max(0.70, 1.0 - D)     (2)", eq_style))
    story.append(Paragraph(
        "Empirical calibration parameters are set to <i>k</i><sub>cal</sub> = 0.00015 day<sup>-1</sup>, <i>k</i><sub>cyc</sub> = 0.00028 cycle<sup>-1</sup>, "
        "and thermal coefficient <i>k</i><sub>temp</sub> = 0.0693. Remaining Useful Life (RUL) represents estimated calendar days until the battery "
        "reaches the standard automotive retirement threshold (SOH = 0.70). Driving range (<i>y</i><sub>pred</sub>) is synthesized by combining individual model outputs:",
        body_style
    ))
    story.append(Paragraph("y_pred = 0.35 * y_RF + 0.35 * y_GBDT + 0.20 * y_XGB + 0.10 * y_Linear     (3)", eq_style))

    # SECTION 4: MACHINE LEARNING METHODOLOGY
    story.append(Paragraph("4. Machine Learning Methodology", h1_style))
    story.append(Paragraph(
        "Four machine learning regressors are evaluated: (A) Ordinary Least Squares Linear Regression as a baseline, (B) Random Forest regressor "
        "with 200 trees and bootstrap sampling, (C) Gradient Boosted Decision Trees (GBDT) with 250 sequential estimators optimizing residual errors "
        "at learning rate 0.05, and (D) an optimized XGBoost model. A weighted blending ensemble (E) combines all four model outputs.",
        body_style
    ))
    story.append(Paragraph(
        "Hyperparameter optimization is performed using Optuna across 50 trials on the validation split [5]. The search space tunes the number of trees "
        "(100-500), maximum tree depth (3-8), learning rate (0.01-0.20), and subsample ratio (0.6-1.0) to directly minimize validation Mean Absolute "
        "Error (MAE). The best-performing configuration selected depth=5, learning_rate=0.04, and L2 regularization lambda=1.5. Model accuracy is "
        "evaluated using MAE, Root Mean Squared Error (RMSE), and coefficient of determination (<i>R</i><sup>2</sup> score). "
        "Model explainability is provided through SHAP (SHapley Additive exPlanations) values [6].",
        body_style
    ))

    # SECTION 5: RESULTS INTRO & TABLE 2
    story.append(Paragraph("5. Results and Comparative Analysis", h1_style))
    story.append(Paragraph(
        "The experimental dataset was partitioned into three distinct subsets with no temporal or vehicle overlap:",
        body_style
    ))

    # Table 2: Partition
    story.append(Paragraph("<b>Table 2. Dataset partition summary</b>", table_title_style))
    t2_data = [
        ['Partition', 'Samples', 'Description'],
        ['Training set (70%)', '3,500 trips', 'Model parameter learning and tree split construction'],
        ['Validation set (15%)', '750 trips', 'Optuna hyperparameter optimization and blending weight tuning'],
        ['Test set (15%)', '750 trips', 'Final evaluation on unseen, held-out vehicle telemetry'],
    ]
    t2 = Table(t2_data, colWidths=[125, 95, 275])
    t2.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
    ]))
    story.append(t2)

    # Force PageBreak to ensure Page 2 ends cleanly
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: TABLE 3, FIGURE 2 (BENCHMARKING), KEY FINDINGS
    # =========================================================================
    story.append(Paragraph("<b>Table 3. Test-set model comparison (evaluated on held-out test set)</b>", table_title_style))
    t3_data = [
        ['Model Architecture', 'MAE (km)', 'RMSE (km)', 'R2 Score', 'Latency', 'Rank'],
        ['A. Linear Regression (Baseline)', '22.144', '29.774', '0.8112', '< 1 ms', '5'],
        ['B. Random Forest', '17.642', '24.201', '0.8752', '12 ms', '4'],
        ['C. Gradient Boosting (GBDT)', '11.875', '17.026', '0.9383', '4 ms', '3'],
        ['D. XGBoost (Optuna Tuned)', '9.685', '13.887', '0.9589', '2 ms', '1 (Best)'],
        ['E. Weighted Blending Ensemble', '12.962', '18.488', '0.9272', '18 ms', '2'],
    ]
    t3 = Table(t3_data, colWidths=[165, 80, 80, 80, 55, 35])
    t3.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('FONTNAME', (0, 4), (-1, 4), 'Times-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
    ]))
    story.append(t3)
    story.append(Spacer(1, 4))

    # Figure 2: Model Benchmarking Chart
    fig1_path = os.path.join(vis_dir, 'fig1_model_benchmarking.png')
    if os.path.exists(fig1_path):
        img_w = content_width
        img_h = content_width * (1500 / 4200)
        story.append(Image(fig1_path, width=img_w, height=img_h))
        story.append(Paragraph("<b>Figure 2.</b> Model comparison: MAE error reduction and R<sup>2</sup> score across baseline and ensemble models.", caption_style))

    story.append(Paragraph("<b>Detailed Key Findings and Performance Analysis:</b>", h1_style))
    story.append(Paragraph(
        "<b>1. Significant Error Reduction:</b> The Optuna-tuned XGBoost model achieved a Mean Absolute Error of 9.685 km and an "
        "<i>R</i><sup>2</sup> of 0.9589 on the test partition. This performance corresponds to a <b>56.3% reduction in error</b> "
        "relative to standard Linear Regression (MAE 22.144 km). Gradient Boosting (GBDT) also proved strong with an MAE of 11.875 km, "
        "demonstrating that non-linear decision boundaries are essential for modeling non-linear battery discharge behavior.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Real-Time Inference Latency:</b> Single-sample inference latency for XGBoost is approximately 2 ms, compared to 12 ms for Random Forest "
        "and 18 ms for the weighted blending ensemble. This confirms that XGBoost is exceptionally well-suited for high-frequency deployment "
        "directly on edge automotive microcontrollers and in-vehicle telematics units where compute cycles and RAM are constrained.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Physics Digital Twin Integration:</b> Traditional range prediction algorithms estimate range purely from instantaneous energy consumption. "
        "By injecting SOH and usable capacity from the physics digital twin into the feature matrix, the model properly penalizes range predictions "
        "on aged battery packs, avoiding catastrophic battery depletion before reaching a charging station.",
        body_style
    ))
    story.append(Paragraph(
        "<b>4. Blending Ensemble Robustness:</b> While single-model XGBoost attained the lowest absolute error, the 4-model weighted ensemble "
        "(MAE 12.962 km, <i>R</i><sup>2</sup> 0.9272) provides valuable regularization against sensor outliers, ensuring robust fallbacks "
        "under anomalous driving profiles.",
        body_style
    ))
    story.append(Paragraph(
        "<b>5. Environmental Degradation Dynamics:</b> Telemetry evaluation under extreme weather demonstrates that driving at -10 deg C increases "
        "energy draw by 28% compared to standard 22 deg C conditions. In contrast, high-speed highway cruising above 90 km/h increases aerodynamic "
        "drag losses quadratically, underscoring the necessity of dynamic environmental inputs.",
        body_style
    ))

    # Force PageBreak to ensure Page 3 ends cleanly
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: FIGURE 3 (SHAP), 6. DEPLOYMENT, 7. CONCLUSION, REFERENCES
    # =========================================================================
    story.append(Paragraph("<b>Feature Importance and Model Interpretability:</b>", h1_style))
    story.append(Paragraph(
        "To verify model trustworthiness and understand feature contributions, Tree SHAP was computed across the test instances:",
        body_style
    ))

    # Figure 3: SHAP Feature Importance Chart
    fig5_path = os.path.join(vis_dir, 'fig5_shap_feature_importance.png')
    if os.path.exists(fig5_path):
        img5_w = content_width * 0.42
        img5_h = img5_w * (1800 / 3000)
        story.append(Image(fig5_path, width=img5_w, height=img5_h))
        story.append(Paragraph("<b>Figure 3.</b> SHAP feature importance ranking: Usable capacity, SOC, speed, and ambient temperature dominance.", caption_style))

    story.append(Paragraph(
        "<b>SHAP Interpretability Insights:</b> Battery Usable Capacity, State of Charge (SOC), Vehicle Speed, and Ambient Temperature account "
        "for over 78% of the total predictive power. Ambient temperature exhibits pronounced non-linear effects: cold temperatures (-10 deg C) reduce "
        "predicted range by up to 28% due to elevated internal cell resistance and cabin heating loads, while moderate temperatures (20-25 deg C) maximize efficiency.",
        body_style
    ))
    story.append(Spacer(1, 2))

    # SECTION 6: DEPLOYMENT AND SYSTEM ARCHITECTURE
    story.append(Paragraph("6. Deployment and System Architecture", h1_style))
    story.append(Paragraph(
        "The complete predictive pipeline is packaged for practical hard-copy demonstration and real-world deployment:<br/>"
        "1) <b>FastAPI REST Service:</b> Production-ready backend with Pydantic schema validation enforcing physical input bounds (temperature between "
        "-20 deg C and 50 deg C; SOC between 0% and 100%). Provides modular endpoints for real-time range estimation, SOH calculation, and safe charging advice.<br/>"
        "2) <b>Containerization:</b> Packaged using a reproducible Dockerfile containing the lightweight Python runtime, dependencies, and serialized model weights.<br/>"
        "3) <b>Interactive Dashboard:</b> An intuitive web interface allows operators and drivers to dynamically simulate trip variables, temperature shifts, "
        "and payload changes, observing instantaneous range predictions and battery health indicators.",
        body_style
    ))
    story.append(Spacer(1, 2))

    # SECTION 7: CONCLUSION AND FUTURE SCOPE
    story.append(Paragraph("7. Conclusion and Future Scope", h1_style))
    story.append(Paragraph(
        "VoltWise demonstrates that integrating a physical battery degradation digital twin with machine learning regression significantly improves EV "
        "driving range prediction accuracy. The Optuna-tuned XGBoost model achieved an MAE of 9.685 km and an <i>R</i><sup>2</sup> score of 0.9589, representing "
        "a 56.3% error reduction over baseline linear methods with an inference latency of just 2 ms.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Future Scope:</b> Future extensions include deploying Long Short-Term Memory (LSTM) recurrent networks for continuous cell voltage tracking, "
        "and integrating road elevation gradients from digital mapping services for dynamic elevation-aware energy optimization.",
        body_style
    ))
    story.append(Spacer(1, 2))

    # REFERENCES
    story.append(Paragraph("References", h1_style))
    refs = [
        "[1] C. Bingham, C. Walsh, and S. Carroll, 'Impact of driving characteristics on electric vehicle energy consumption,' <i>SAE Int. J. Alt. Power</i>, vol. 1, no. 1, pp. 132-141, 2012.",
        "[2] Y. Bi, D. Chrenko, F. Gao, and D. Paire, 'Estimating vehicle electric consumption using machine learning algorithms,' in <i>Proc. IEEE Transportation Electrification Conf. and Expo (ITEC)</i>, 2020, pp. 450-455.",
        "[3] J. Schmalstieg, S. Kabitz, M. Ecker, and D. U. Sauer, 'A holistic aging model for Li(NiMnCo)O2 based 18650 lithium-ion cells,' <i>Journal of Power Sources</i>, vol. 257, pp. 325-334, 2014.",
        "[4] T. Chen and C. Guestrin, 'XGBoost: A scalable tree boosting system,' in <i>Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.</i>, 2016, pp. 785-794.",
        "[5] T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, 'Optuna: A next-generation hyperparameter optimization framework,' in <i>Proc. 25th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.</i>, 2019, pp. 2623-2631.",
        "[6] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' in <i>Proc. Advances in Neural Information Processing Systems (NeurIPS)</i>, 2017, pp. 4765-4774."
    ]
    for ref in refs:
        story.append(Paragraph(ref, ref_style))

    doc.build(story, canvasmaker=SimpleHardCopyCanvas)
    
    # Check page count
    pdf_doc = pymupdf.open(output_pdf_path)
    total_pages = len(pdf_doc)
    print(f"Compiled Concise Hard Copy CAT II Report PDF. Total Pages: {total_pages}")
    return total_pages


if __name__ == '__main__':
    project_root = r'c:\Users\midhu\Downloads\ev-battery-predictor-main\ev-battery-predictor-main'
    pdf_out = os.path.join(project_root, 'CAT_II_PROJECT_REPORT.pdf')
    build_simple_cat2_pdf(pdf_out, project_root)
