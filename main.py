from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import numpy as np

tags_metadata = [
    {
        "name": "Quantitative Risk Engine",
        "description": "Core mathematical endpoints for computing Parametric Value at Risk (VaR) across investment portfolios.",
    },
    {
        "name": "System & FinOps Telemetry",
        "description": "Health checks, container runtime verification, and Azure FinOps governance metadata.",
    },
]

app = FastAPI(
    title="QuantGuard | FinOps & Quantitative Risk Engine",
    description="""
**Enterprise Quantitative Risk & Cloud FinOps Microservice**

Engineered with **Zero-Trust DevSecOps** (non-root container runtime, automated Aqua Trivy CVE & IaC security gates) and **Cloud FinOps Governance** (Terraform scale-to-zero compute & mandatory cost-allocation tagging on Microsoft Azure).

* **Engineer:** Blessing Azeta ([GitHub](https://github.com/Azeta-Insights/quant-guard-api))
* **Cloud Region:** Azure Canada Central (`canadacentral`)
    """,
    version="1.2.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "list",
        "filter": True,
        "syntaxHighlight.theme": "monokai",
    },
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuantGuard | FinOps & Quantitative Risk Engine</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #e2e8f0; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        .glass { background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(51, 65, 85, 0.6); }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-6 md:p-12">
    <div class="max-w-6xl mx-auto w-full space-y-8">
        
        <!-- Header / Nav -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
            <div>
                <div class="flex items-center gap-3">
                    <span class="px-2.5 py-1 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        ONLINE • AZURE CANADA CENTRAL
                    </span>
                    <span class="px-2.5 py-1 text-xs font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20 rounded-full mono">
                        v1.2.0
                    </span>
                </div>
                <h1 class="text-3xl md:text-4xl font-bold text-white mt-3 tracking-tight">QuantGuard Risk & FinOps Engine</h1>
                <p class="text-slate-400 mt-1 text-sm md:text-base">Cloud-Native Parametric Value at Risk (VaR) Microservice with Automated DevSecOps Gating</p>
            </div>
            <div class="flex gap-3">
                <a href="/docs" class="px-4 py-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-sm font-medium border border-slate-700 transition">
                    Swagger UI (/docs)
                </a>
                <a href="/redoc" class="px-4 py-2.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white text-sm font-medium transition shadow-lg shadow-sky-600/20">
                    ReDoc API Specs
                </a>
            </div>
        </header>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <!-- Left: Interactive VaR Calculator -->
            <div class="lg:col-span-7 glass rounded-2xl p-6 md:p-8 space-y-6">
                <div class="flex items-center justify-between border-b border-slate-800 pb-4">
                    <div>
                        <h2 class="text-xl font-semibold text-white">Interactive Parametric VaR Simulator</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Live API execution against <code class="text-sky-400 mono">GET /calculate-var</code></p>
                    </div>
                    <span class="mono text-xs text-slate-400 bg-slate-900 px-3 py-1.5 rounded-md border border-slate-800">VaR = V × σ × √T × Zα</span>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Portfolio Value (CAD $)</label>
                        <input id="portfolio_value" type="number" value="250000" step="10000"
                            class="w-full px-4 py-2.5 rounded-lg bg-slate-900 border border-slate-700 text-white mono focus:outline-none focus:border-sky-500">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Daily Volatility (σ)</label>
                        <input id="volatility" type="number" value="0.018" step="0.001"
                            class="w-full px-4 py-2.5 rounded-lg bg-slate-900 border border-slate-700 text-white mono focus:outline-none focus:border-sky-500">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Confidence Interval</label>
                        <select id="confidence_level"
                            class="w-full px-4 py-2.5 rounded-lg bg-slate-900 border border-slate-700 text-white mono focus:outline-none focus:border-sky-500">
                            <option value="0.95" selected>95% Confidence (Z = 1.645)</option>
                            <option value="0.99">99% Confidence (Z = 2.326)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">Time Horizon (Trading Days)</label>
                        <input id="days" type="number" value="10" min="1" max="365"
                            class="w-full px-4 py-2.5 rounded-lg bg-slate-900 border border-slate-700 text-white mono focus:outline-none focus:border-sky-500">
                    </div>
                </div>

                <button onclick="runVarCalculation()"
                    class="w-full py-3 rounded-lg bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold shadow-lg shadow-sky-500/20 transition cursor-pointer">
                    Compute Parametric Value at Risk
                </button>

                <!-- Results Card -->
                <div class="bg-slate-950/90 rounded-xl p-5 border border-slate-800 space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-4">
                        <div>
                            <span class="text-xs uppercase tracking-wider text-slate-400">Estimated Maximum Potential Loss (VaR)</span>
                            <div id="var_display" class="text-3xl font-bold text-rose-400 mono mt-1">$23,408.73 CAD</div>
                        </div>
                        <div class="text-right">
                            <span class="text-xs uppercase tracking-wider text-slate-400">Portfolio Exposure</span>
                            <div id="pct_display" class="text-lg font-semibold text-amber-400 mono mt-1">9.36% of Capital</div>
                        </div>
                    </div>
                    <div>
                        <div class="text-xs text-slate-400 mb-1.5 flex justify-between">
                            <span>Raw JSON API Response:</span>
                            <span id="status_badge" class="text-emerald-400 mono">HTTP 200 OK</span>
                        </div>
                        <pre id="json_output" class="mono text-xs text-sky-300 overflow-x-auto bg-slate-900/90 p-3 rounded-lg border border-slate-800/80"></pre>
                    </div>
                </div>
            </div>

            <!-- Right: Architecture, DevSecOps & FinOps Telemetry -->
            <div class="lg:col-span-5 space-y-6">
                <div class="glass rounded-2xl p-6 space-y-4">
                    <h3 class="text-lg font-semibold text-white">Cloud & Security Architecture</h3>
                    <div class="space-y-3 text-sm">
                        <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                            <div class="font-semibold text-emerald-400 flex items-center justify-between">
                                <span>🛡️ Zero-Trust Container Hardening</span>
                                <span class="text-xs mono bg-emerald-500/10 px-2 py-0.5 rounded">PASSED</span>
                            </div>
                            <p class="text-slate-400 text-xs mt-1">Runs under non-root <code class="text-slate-200">quantuser</code> (UID 1000) on patched Debian slim layers.</p>
                        </div>

                        <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                            <div class="font-semibold text-sky-400 flex items-center justify-between">
                                <span>🔍 Shift-Left Aqua Trivy Gates</span>
                                <span class="text-xs mono bg-sky-500/10 px-2 py-0.5 rounded">ACTIVE</span>
                            </div>
                            <p class="text-slate-400 text-xs mt-1">Automated GitHub Actions CI/CD blocks CRITICAL/HIGH CVEs and Terraform IaC misconfigurations.</p>
                        </div>

                        <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                            <div class="font-semibold text-amber-400 flex items-center justify-between">
                                <span>💰 FinOps Scale-to-Zero Governance</span>
                                <span class="text-xs mono bg-amber-500/10 px-2 py-0.5 rounded">$0.00/HR IDLE</span>
                            </div>
                            <p class="text-slate-400 text-xs mt-1">Terraform-provisioned Azure Container Apps (<code class="text-slate-200">min_replicas = 0</code>) with mandatory FinOps cost-allocation tags.</p>
                        </div>
                    </div>
                </div>

                <div class="glass rounded-2xl p-6 space-y-3">
                    <h3 class="text-sm font-semibold uppercase tracking-wider text-slate-400">FinOps Resource Tags</h3>
                    <div class="grid grid-cols-2 gap-2.5 mono text-xs">
                        <div class="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
                            <span class="text-slate-500 block">CostCenter</span>
                            <span class="text-slate-200 font-semibold">FinEng-Quant-001</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
                            <span class="text-slate-500 block">Environment</span>
                            <span class="text-slate-200 font-semibold">Production</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
                            <span class="text-slate-500 block">ManagedBy</span>
                            <span class="text-slate-200 font-semibold">Terraform-FinOps</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
                            <span class="text-slate-500 block">Region</span>
                            <span class="text-slate-200 font-semibold">canadacentral</span>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Footer -->
    <footer class="max-w-6xl mx-auto w-full border-t border-slate-800/80 pt-6 mt-12 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-500 gap-4">
        <div>Engineered by <strong class="text-slate-300">Blessing Azeta</strong> • Cloud, DevSecOps & Financial Engineering</div>
        <div class="flex gap-4">
            <a href="https://github.com/Azeta-Insights/quant-guard-api" target="_blank" class="hover:text-sky-400 transition">GitHub Repository</a>
            <span>•</span>
            <a href="/health" class="hover:text-sky-400 transition">Health Telemetry (/health)</a>
        </div>
    </footer>

    <script>
        async function runVarCalculation() {
            const pv = document.getElementById('portfolio_value').value;
            const vol = document.getElementById('volatility').value;
            const conf = document.getElementById('confidence_level').value;
            const days = document.getElementById('days').value;

            const url = `/calculate-var?portfolio_value=${pv}&volatility=${vol}&confidence_level=${conf}&days=${days}`;
            try {
                const res = await fetch(url);
                const data = await res.json();
                const varVal = data.parametric_var_cad ?? data.value_at_risk_cad ?? 0;
                document.getElementById('var_display').innerText =
                    '$' + Number(varVal).toLocaleString('en-CA', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' CAD';
                const pct = ((varVal / Number(pv)) * 100).toFixed(2);
                document.getElementById('pct_display').innerText = `${pct}% of Capital`;
                document.getElementById('json_output').innerText = JSON.stringify(data, null, 2);
            } catch (err) {
                document.getElementById('json_output').innerText = "Error calling endpoint: " + err;
            }
        }
        window.onload = runVarCalculation;
    </script>
</body>
</html>
    """


@app.get(
    "/health",
    tags=["System & FinOps Telemetry"],
    summary="Container Health & FinOps Governance Check",
)
def health_check():
    """Returns real-time container health and FinOps resource governance tags."""
    return {
        "status": "healthy",
        "service": "quant-guard-api",
        "version": "1.2.0",
        "security_context": "non-root (quantuser)",
        "finops_governance": {
            "cloud_provider": "Microsoft Azure",
            "region": "canadacentral",
            "compute_tier": "Scale-to-Zero (min_replicas=0)",
            "cost_center": "FinEng-Quant-001",
        },
    }


@app.get(
    "/calculate-var",
    tags=["Quantitative Risk Engine"],
    summary="Calculate Parametric Value at Risk (VaR)",
)
def calculate_var(
    portfolio_value: float = Query(100000.0, gt=0, description="Total portfolio value in CAD"),
    volatility: float = Query(0.02, gt=0, le=1.0, description="Daily portfolio volatility (e.g., 0.02 for 2%)"),
    confidence_level: float = Query(0.95, description="Confidence interval (0.95 or 0.99)"),
    days: int = Query(1, ge=1, le=365, description="Time horizon in trading days (T)"),
):
    """
    Computes the Parametric Value at Risk (VaR) for an investment portfolio:
    **VaR = Portfolio Value × σ × √T × Z_α**
    """
    z_score = 1.645 if confidence_level <= 0.95 else 2.326
    var_value = portfolio_value * volatility * np.sqrt(days) * z_score

    return {
        "portfolio_value_cad": portfolio_value,
        "daily_volatility": volatility,
        "confidence_level": confidence_level,
        "time_horizon_days": days,
        "z_score_applied": z_score,
        "parametric_var_cad": round(float(var_value), 2),
        "risk_exposure_pct": round(float((var_value / portfolio_value) * 100), 2),
    }