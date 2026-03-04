# PredictiveForge

**Enterprise-Grade AI-Powered Predictive Analytics Platform**

> Proprietary platform — source code is confidential.
> This repository is a portfolio reference.

---

## What is PredictiveForge?

PredictiveForge is a full-stack machine learning platform built to accelerate
end-to-end AI consulting engagements. It reduces a typical ML pipeline project
to hours — from raw data ingestion through to submission-ready predictions —
while enforcing enterprise AI governance standards throughout.

Designed and built as a solo engineering effort, the platform spans 28,000+
lines of production Python across modular, independently testable components.

---

## Platform Capabilities

### AI Model Engine
- 25+ algorithms across classification, regression, and time-series tasks
  (XGBoost, LightGBM, CatBoost, Random Forest, ElasticNet, and more)
- Automated hyperparameter optimisation via Bayesian search
- Population-Based Training (PBT) and LightGBM Incremental Training
- Ensemble stacking with Sharpe-ratio-based weight optimisation
- Overfitting / underfitting detection with automated remediation suggestions

### Dual AI Backend
- **Cloud mode**: Gemini 1.5 Flash / Gemini 2.5 Pro + OpenAI GPT-4
- **Local/private mode**: Ollama  — no data leaves
  the client network. Suitable for regulated industries.

### Master Prompt Architecture
- "Principal ML Architect" prompt template that pre-scans datasets
  (column names, dtypes, sample rows, image shapes) before generating code
- HARD CONSTRAINTS enforced: sklearn/numpy/pandas-only fallback paths,
  mandatory self_check() verification, deterministic seeding
- Post-generation quality gate: validates self_check presence,
  seeding strategy, and validation methodology before code is executed

### AI Governance & Compliance
- Notebook compliance scanner aligned to **NIST AI Risk Management
  Framework (AI RMF)** and **EU AI Act** control categories
- Generates downloadable HTML compliance reports with risk ratings,
  findings, and remediation recommendations
- Two-tier audit logging: per-session JSONL files + master archive
- OWASP LLM Top 10 control mapping (LLM01–LLM10)
- PII masking (emails, SSNs, phone numbers, credit cards, IP addresses)
  applied automatically before data enters any pipeline or log

### Streaming Data Pipeline
- Real-time ingestion from CSV polling, REST APIs, WebSockets,
  and direct database queries
- Feature engineering: rolling statistics, lag features, time features,
  interaction terms — all leakage-safe
- Pipeline stages: PII mask → feature engineer → leakage check → train
- Integrated with Modal cloud GPU for scale-out training

### Cloud GPU Training (Modal)
- Enterprise patterns: zero cold-start lifecycle hooks, decoupled CPU
  preprocessing, distributed Modal Volumes, fault tolerance (retries=3,
  timeout=3600), warm pools
- Universal data ingest scripts: download from any source (APIs,
  databases, AWS S3) into persistent cloud volumes

### Feature Engineering & Leakage Prevention
- AdvancedFeatureEngineer: market features with leakage-safe groupby
- FeaturePruner: importance-based dimensionality reduction
- LeakagePreventionPipeline: ordered column dropping before preprocessing
- Adversarial validation: AUC-based train/test distribution shift detection

### Specialist Pipelines
- **ECG Digitisation**: LAB colour-space grid removal, morphological text
  suppression, power-weighted centroid signal extraction, clinical
  validation metrics (Kurtosis, Einthoven Coherence, aVR Axis Alignment)
- **Pasture Biomass Multimodal**: ResNet50 feature extraction,
  LeakageSafePCA, physics consistency constraints, seed averaging ensemble
- **Quantitative Finance**: threshold-aware allocation, exponential ramp,
  Sharpe optimisation, Max Drawdown / Calmar / Sortino risk metrics

### Integrations
| Service | Purpose |
|---------|---------|
| Gemini AI | Code generation, image analysis, strategy recommendations |
| OpenAI GPT-4 | Dual-model ensemble, auto-fix pipeline |
| Hugging Face Hub | Model/dataset push-pull, model cards, Space deployment |
| Weights & Biases | Experiment tracking, metric logging, model versioning |
| Modal | Cloud GPU training, distributed volumes |
| Ollama | Local privacy-first inference |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     PredictiveForge UI                      │
│              (Streamlit · Dark Navy Theme)                   │
└──────────┬──────────────────────────────────────────────────┘
           │
    ┌──────▼──────────────────────────────────────────┐
    │              Core Orchestration Layer            │
    │  MaxAutoML · Algorithm Registry · Feature Eng.  │
    └──────┬──────────────┬──────────────┬────────────┘
           │              │              │
    ┌──────▼──────┐ ┌─────▼──────┐ ┌───▼──────────────┐
    │  AI Backend  │ │  Streaming │ │  Governance &    │
    │  Gemini/GPT  │ │  Pipeline  │ │  Compliance      │
    │  Ollama      │ │  + Modal   │ │  NIST · EU AI    │
    └─────────────┘ └────────────┘ └──────────────────┘
```

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.x-189DDD?style=flat)
![LightGBM](https://img.shields.io/badge/LightGBM-4.x-02a651?style=flat)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_AI-2.5_Pro-4285F4?style=flat&logo=google&logoColor=white)
![NIST](https://img.shields.io/badge/NIST_AI_RMF-Compliant-005A9C?style=flat)
![EU AI Act](https://img.shields.io/badge/EU_AI_Act-Aligned-003399?style=flat)
![OWASP](https://img.shields.io/badge/OWASP_LLM_Top_10-Mapped-000000?style=flat)

---

## Commercial Application

PredictiveForge is used as an accelerator for AI consulting engagements
across the following domains:

- **Enterprise ML Delivery** — rapid prototyping to production pipeline
- **Regulated Industry AI** — local inference mode for GDPR/data-residency
  requirements; built-in NIST AI RMF and EU AI Act compliance reporting
- **Quantitative Finance** — end-to-end strategy building, risk evaluation,
  and submission generation
- **Medical AI** — ECG digitisation and clinical signal validation pipeline
- **Environmental Science** — multimodal biomass prediction with
  physics-informed constraints

Consulting rate: ** depending on engagement scope **.

---

## Intellectual Property Notice

This repository contains no source code. All implementation details,
algorithms, prompt architectures, and system designs are proprietary and
confidential.

© 2026 — All rights reserved.
Unauthorised reproduction, reverse engineering, or distribution of any
part of this platform is strictly prohibited.

For professional enquiries: singh.arjun312@gmail.com
