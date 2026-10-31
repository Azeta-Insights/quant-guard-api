# QuantGuard: Cloud-Native Value at Risk (VaR) & FinOps Engine

![DevSecOps & FinOps Pipeline](https://github.com/Azeta-Insights/quant-guard-api/actions/workflows/ci-devsecops.yml/badge.svg)

**QuantGuard** is a containerized financial risk microservice that calculates **Parametric Value at Risk (VaR)** for investment portfolios. Built for regulated financial and energy-trading environments, it combines **Quantitative Financial Engineering**, **DevSecOps container hardening**, and **Cloud FinOps governance** on Microsoft Azure.

## Architecture & Engineering Pillars

* **Quantitative Financial Engineering (`main.py`):** Exposes a FastAPI REST endpoint (`/calculate-var`) using NumPy to compute Parametric Value at Risk across configurable portfolio values, daily volatilities ($\sigma$), confidence intervals ($95\%$, $99\%$), and time horizons ($T$ days):
  $$\text{VaR} = \text{Portfolio Value} \times \sigma \times \sqrt{T} \times Z_{\alpha}$$
* **DevSecOps Container & IaC Hardening (`Dockerfile` & `.github/workflows/ci-devsecops.yml`):**
  * **Least-Privilege Runtime:** Runs inside a patched `python:3.11-slim` image under a restricted non-root user (`quantuser`) to prevent privilege escalation.
  * **Automated Vulnerability Gates:** Every push triggers **Aqua Security Trivy** in GitHub Actions to scan both the Docker image (`vuln-type: library`) and Terraform Infrastructure-as-Code (`./infra`) for `HIGH` and `CRITICAL` security flaws before deployment, backed by documented CVE triage in `.trivyignore`.
* **Cloud FinOps Cost Governance (`infra/main.tf`):**
  * **Scale-to-Zero Compute:** Provisioned on **Azure Container Apps** (`canadacentral`) with `min_replicas = 0` and right-sized resources (`0.25 vCPU`, `0.5Gi RAM`), eliminating 100% of idle compute waste ($0.00/hr when idle).
  * **Mandatory Cost Allocation Tags:** Enforces FinOps governance tags (`CostCenter = FinEng-Quant-001`, `Project`, `Environment`, `ManagedBy`) across all Azure resources for automated cost tracking.

## Project Structure

```text
quant-guard-api/
├── main.py                        # FastAPI Parametric VaR microservice
├── requirements.txt               # Pinned & patched Python dependencies
├── Dockerfile                     # Non-root hardened container definition
├── .trivyignore                   # Documented upstream CVE triage policy
├── infra/
│   └── main.tf                    # Terraform IaC (Azure Container Apps + FinOps tags)
└── .github/
    └── workflows/
        └── ci-devsecops.yml       # GitHub Actions CI/CD + Trivy security gates