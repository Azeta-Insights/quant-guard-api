from fastapi import FastAPI, Query
import numpy as np

app = FastAPI(title="QuantGuard FinOps & Risk Engine")

@app.get("/")
def root():
    return {
        "service": "QuantGuard FinOps & Risk Engine",
        "interactive_docs": "/docs",
        "endpoints": ["/health", "/calculate-var"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "quant-guard-api"}

@app.get("/calculate-var")
def calculate_var(
    portfolio_value: float = Query(100000.0, description="Total portfolio value in CAD"),
    volatility: float = Query(0.02, description="Daily volatility (e.g., 0.02 for 2%)"),
    confidence_level: float = Query(0.95, description="Confidence level (e.g., 0.95 for 95%)"),
    days: int = Query(1, description="Time horizon in days")
):
    # Parametric Value at Risk (VaR) formula: Portfolio * Volatility * sqrt(Days) * Z-Score
    z_score = 1.645 if confidence_level == 0.95 else 2.326
    var_amount = portfolio_value * volatility * np.sqrt(days) * z_score

    return {
        "portfolio_value_cad": portfolio_value,
        "confidence_level": confidence_level,
        "time_horizon_days": days,
        "value_at_risk_cad": round(float(var_amount), 2),
        "finops_tier": "scale-to-zero-consumption"
    }