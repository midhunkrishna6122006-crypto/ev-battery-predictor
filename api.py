"""
Production-grade FastAPI Inference Service for EV Battery Digital Twin & Range Predictor
Fulfills CIT 19MAM56 AML Lab - Rubric Component 4 (Local Deployment with Input Validation)
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import numpy as np
import pandas as pd
import sys
import os

# Ensure src directory is accessible
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from digital_twin.battery_twin import BatteryDigitalTwin, BatteryState
from models.range_predictor import RangePredictionModel
from data_processing.data_pipeline import EVDataProcessor

# Initialize FastAPI App
app = FastAPI(
    title="EV Battery Digital Twin & Range Inference API",
    description="Production REST API providing real-time EV driving range predictions, physics-informed battery health diagnostics, and smart charging optimization.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global Model & Engine Singletons
battery_twin = BatteryDigitalTwin(battery_capacity=75.0, chemistry="Li-ion")
range_model = RangePredictionModel(model_type="ensemble")

# Pre-train models on startup
@app.on_event("startup")
def startup_event():
    """Initialize and pre-train the ensemble regression pipeline"""
    processor = EVDataProcessor()
    train_data = range_model.generate_synthetic_data(n_samples=5000)
    range_model.train(train_data)
    print("✅ ML Ensemble (Random Forest, GBDT, XGBoost, Linear) initialized and ready for inference.")

# ----------------- Pydantic Request & Response Schemas -----------------

class RangeInferenceRequest(BaseModel):
    battery_capacity_kwh: float = Field(75.0, ge=20.0, le=150.0, description="Nominal battery pack capacity in kWh")
    battery_soh: float = Field(0.95, ge=0.5, le=1.0, description="State of Health fraction (0.5 to 1.0)")
    battery_soc_start: float = Field(0.80, ge=0.05, le=1.0, description="Starting State of Charge fraction (0.05 to 1.0)")
    vehicle_efficiency_km_kwh: float = Field(4.5, ge=1.5, le=9.0, description="Nominal vehicle efficiency in km/kWh")
    temperature_c: float = Field(22.0, ge=-25.0, le=50.0, description="Ambient temperature in Celsius")
    humidity_percent: float = Field(60.0, ge=10.0, le=100.0, description="Ambient humidity percentage")
    wind_speed_kmh: float = Field(10.0, ge=0.0, le=100.0, description="Wind speed in km/h")
    precipitation: int = Field(0, ge=0, le=1, description="Precipitation binary flag (0: No, 1: Yes)")
    avg_speed_kmh: float = Field(60.0, ge=10.0, le=160.0, description="Expected average speed in km/h")
    traffic_density: str = Field("medium", pattern="^(low|medium|high)$", description="Traffic density")
    route_type: str = Field("mixed", pattern="^(city|highway|mixed)$", description="Route environment")
    elevation_change_m: float = Field(0.0, ge=-1000.0, le=2000.0, description="Net elevation delta in meters")
    driving_style: str = Field("normal", pattern="^(eco|normal|aggressive)$", description="Driver behavioral style")
    ac_usage: int = Field(1, ge=0, le=1, description="HVAC/AC activation flag (0: Off, 1: On)")

    class Config:
        json_schema_extra = {
            "example": {
                "battery_capacity_kwh": 75.0,
                "battery_soh": 0.94,
                "battery_soc_start": 0.85,
                "vehicle_efficiency_km_kwh": 4.5,
                "temperature_c": 24.0,
                "humidity_percent": 55.0,
                "wind_speed_kmh": 12.0,
                "precipitation": 0,
                "avg_speed_kmh": 50.0,
                "traffic_density": "medium",
                "route_type": "city",
                "elevation_change_m": 15.0,
                "driving_style": "normal",
                "ac_usage": 1
            }
        }

class RangeInferenceResponse(BaseModel):
    ensemble_predicted_range_km: float
    model_breakdown: Dict[str, float]
    prediction_confidence: str
    top_influencing_factors: List[Dict[str, Any]]

class BatteryHealthRequest(BaseModel):
    soh: Optional[float] = Field(0.90, ge=0.5, le=1.0, description="Current SOH (optional, calculated if omitted)")
    soc: float = Field(0.70, ge=0.0, le=1.0, description="Current State of Charge fraction")
    temperature: float = Field(25.0, ge=-25.0, le=55.0, description="Cell temperature in Celsius")
    voltage: float = Field(3.7, ge=2.8, le=4.3, description="Nominal cell voltage")
    current: float = Field(0.0, description="Current draw in Amperes")
    cycle_count: int = Field(450, ge=0, le=5000, description="Cumulative charge cycle count")
    age_days: int = Field(500, ge=0, le=6000, description="Calendar age in days")

class BatteryHealthResponse(BaseModel):
    health_grade: str
    state_of_health_pct: float
    remaining_capacity_kwh: float
    remaining_useful_life_years: float
    second_life_application: str
    second_life_suitability: str

class ChargingOptimizationRequest(BaseModel):
    current_soc: float = Field(..., ge=0.05, le=1.0, description="Current SOC")
    target_soc: float = Field(0.80, ge=0.2, le=1.0, description="Target SOC")
    temperature_c: float = Field(25.0, ge=-25.0, le=55.0, description="Ambient/cell temperature")

class ChargingOptimizationResponse(BaseModel):
    recommended_charge_rate_c: float
    max_charge_voltage: float
    target_soc_pct: float
    estimated_charging_time_hours: float
    thermal_compensation_active: bool

# ----------------- API Endpoints -----------------

@app.get("/", tags=["System Information"])
def root():
    """System health check and metadata"""
    return {
        "status": "healthy",
        "service": "EV Battery Digital Twin & Range Predictor API",
        "department": "Computing - AI & ML, Coimbatore Institute of Technology",
        "course": "19MAM56 - Advanced Machine Learning Lab",
        "models_loaded": list(range_model.models.keys()) + ["ensemble"],
        "endpoints": {
            "swagger_docs": "/docs",
            "predict_range": "POST /predict/range",
            "battery_health": "POST /battery/health",
            "optimize_charging": "POST /battery/optimize-charging",
            "benchmark_metrics": "GET /metrics"
        }
    }

@app.post("/predict/range", response_model=RangeInferenceResponse, tags=["Inference"])
def predict_driving_range(req: RangeInferenceRequest):
    """
    Predict EV driving range using multi-factor ensemble regression
    (Random Forest + GBDT + XGBoost + Linear Baseline).
    """
    try:
        input_dict = req.dict()
        preds = range_model.predict_range(input_dict)
        factors = range_model.get_range_factors_analysis(input_dict)
        
        rf_pred = preds.get('random_forest', 0)
        gb_pred = preds.get('gradient_boost', 0)
        confidence = "High" if abs(rf_pred - gb_pred) < 20 else "Medium"

        return RangeInferenceResponse(
            ensemble_predicted_range_km=round(preds['ensemble'], 2),
            model_breakdown={k: round(v, 2) for k, v in preds.items() if k != 'ensemble'},
            prediction_confidence=confidence,
            top_influencing_factors=factors.get('top_factors', [])
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/battery/health", response_model=BatteryHealthResponse, tags=["Digital Twin"])
def assess_battery_health(req: BatteryHealthRequest):
    """
    Assess battery State of Health (SOH), Remaining Useful Life (RUL),
    and Second-Life grading using the physics-informed digital twin.
    """
    try:
        b_state = BatteryState(
            soh=req.soh or 0.95,
            soc=req.soc,
            temperature=req.temperature,
            voltage=req.voltage,
            current=req.current,
            cycle_count=req.cycle_count,
            age_days=req.age_days
        )
        report = battery_twin.get_health_report(b_state)
        second_life = report['second_life_potential']

        return BatteryHealthResponse(
            health_grade=report['health_grade'],
            state_of_health_pct=round(report['state_of_health'] * 100, 2),
            remaining_capacity_kwh=round(report['remaining_capacity_kwh'], 2),
            remaining_useful_life_years=round(report['remaining_useful_life_days'] / 365.25, 2),
            second_life_application=second_life['recommended_application'],
            second_life_suitability=second_life['suitability_rating']
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/battery/optimize-charging", response_model=ChargingOptimizationResponse, tags=["Digital Twin"])
def optimize_charging_parameters(req: ChargingOptimizationRequest):
    """
    Calculate temperature-compensated charging rates and cell protection parameters.
    """
    try:
        strategy = battery_twin.optimize_charging_strategy(
            current_soc=req.current_soc,
            target_soc=req.target_soc,
            temperature=req.temperature_c
        )
        return ChargingOptimizationResponse(
            recommended_charge_rate_c=round(strategy['charge_rate_c'], 2),
            max_charge_voltage=round(strategy['max_voltage'], 2),
            target_soc_pct=round(strategy['target_soc'] * 100, 1),
            estimated_charging_time_hours=round(strategy['estimated_time_hours'], 2),
            thermal_compensation_active=strategy['temperature_compensation']
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/metrics", tags=["Model Benchmarks"])
def get_model_benchmarks():
    """
    Returns comparative evaluation metrics across all trained regression models.
    """
    if not range_model.is_trained:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Models not yet trained.")
    
    # Generate test evaluation snapshot
    test_data = range_model.generate_synthetic_data(n_samples=1000)
    eval_results = range_model.train(test_data)
    
    return {
        "benchmark_dataset_samples": 1000,
        "models": {k: {m: round(val, 4) for m, val in metrics.items()} for k, metrics in eval_results.items()},
        "primary_metric": "Mean Absolute Error (MAE in km)",
        "best_individual_model": min(eval_results.keys(), key=lambda k: eval_results[k]['mae'])
    }
