from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import numpy as np

# 1. Initialize with professional metadata, custom titles, and descriptions
app = FastAPI(
    title="QuantGuard FinOps & Risk Engine",
    description="""
    ### Enterprise Quantitative Risk & Cloud FinOps Microservice
    
    QuantGuard combines quantitative financial risk modeling (Parametric Value at Risk) 
    with production-grade cloud-native security gates and scale-to-zero cost governance.
    
    * **Developer:** Blessing Azeta (Azeta-Insights)
    * **Architecture:** FastAPI, Docker (Non-Root), Terraform, Azure Container Apps
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 2. Custom CSS injection to give Swagger UI a polished, original dark-accented theme
CUSTOM_CSS = """
.swagger-ui .topbar { display: none; }
.swagger-ui .info { margin: 20px 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
.swagger-ui .info .title { color: #0f172a; font-weight: 700; }
.swagger-ui .scheme-container { background: #f8fafc; box-shadow: none; border-radius: 8px; }
"""

@app.get("/", include_in_schema=False)
def root():
    return HTMLResponse(content="""
    <html>
        <head><title>QuantGuard API</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #0f172a; color: #fff;">
            <h1>🚀 QuantGuard FinOps & Risk Engine is Live</h1>
            <p>Secure cloud-native parametric risk microservice.</p>
            <a href="/docs" style="color: #38bdf8; font-size: 18px; text-decoration: none;">Explore Interactive API Docs &rarr;</a>
        </body>
    </html>
    """)

@app.get("/health", tags=["System Health"], summary="Service Health Check")
def health_check():
    """Returns the operational status of the QuantGuard container."""
    return {
        "status": "healthy",
        "service": "quant-guard-api",
        "cloud_provider": "Microsoft Azure",
        "region": "canadacentral"
    }

@app.get("/calculate-var", tags=["Quantitative Risk Engine"], summary="Calculate Parametric Value at Risk (VaR)")
def calculate_var(
    portfolio_value: float = Query(100000.0, description="Total portfolio value in CAD"),
    volatility: float = Query(0.015, description="Daily portfolio volatility (standard deviation σ)"),
    confidence_level: float = Query(0.95, description="Confidence interval (e.g., 0.95 or 0.99)"),
    days: int = Query(1, description="Time horizon in trading days (T)")
):
    """
    Computes the Parametric Value at Risk (VaR) for an investment portfolio 
    using configurable volatility, confidence intervals, and time horizons.
    """
    # Z-score approximation for standard confidence levels
    z_score = 1.645 if confidence_level == 0.95 else 2.326 if confidence_level == 0.99 else 1.96
    
    var_value = portfolio_value * volatility * np.sqrt(days) * z_score
    
    return {
        "portfolio_value": portfolio_value,
        "volatility": volatility,
        "confidence_level": confidence_level,
        "time_horizon_days": days,
        "z_score_applied": z_score,
        "parametric_var_cad": round(var_value, 2)
    }