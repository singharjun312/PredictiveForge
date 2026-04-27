# PredictiveForge - AI-Powered Predictive Analytics Platform

## Overview
PredictiveForge is an AI-powered predictive analytics platform designed to automate the machine learning workflow from data analysis to model deployment. It offers an intuitive interface, enterprise-level ML capabilities with over 25 algorithms, automated model building, hyperparameter optimization, and comprehensive performance evaluation. The platform aims to be a complete and accessible solution for predictive modeling, supporting advanced feature engineering, robust handling of large datasets, and achieving high success rates in diverse tasks such as Program Synthesis, Quantitative Finance, and Multimodal ML.

## User Preferences
Preferred communication style: Simple, everyday language.
Competition setup preference: Simplified interface with only competition title input - AI should automatically parse and determine all competition details including target labels, competition type (classification/regression), and submission format.
Kaggle API setup preference: Single, simplified credentials prompt in connections tab only - avoid duplicate credential inputs across different pages.

## System Architecture

### UI/UX Decisions
- **Frontend Framework**: Streamlit, utilizing a multi-page interface with sidebar navigation.
- **Theme**: Professional dark navy (#0F2232) with complementary teal and light blue-white text, optimized for data science.

### Technical Implementations
- **Core Engine**: Modular Python components, supporting Replit and Local environments.
- **AI-Powered Solvers**: Integrates Gemini AI for Program Synthesis, Computer Vision, and Game AI.
- **Master Prompt Architecture**: Production-grade code generation using a "Principal ML Architect" prompt template, enforcing hard constraints and post-generation quality checks.
- **Local AI Integration (Ollama)**: Privacy-first mode using local Ollama models for clients requiring no data to leave their network.
- **AI Compliance Validators**: Validates Jupyter notebooks against NIST AI RMF, EU AI Act, and ISO/IEC 42001:2023 frameworks, generating downloadable HTML compliance reports.
- **Supply Chain Security Scanner & SBOM Generator**: Scans Python packages for CVEs and generates an SPDX-inspired Software Bill of Materials.
- **Streaming Data Pipeline**: Real-time data ingestion, configurable feature engineering, PII masking, and Modal GPU training integration.
- **Streaming-to-Modal Training Pipeline**: Dual-mode architecture supporting local and cloud GPU training (via Modal) for streaming data.
- **PII Masking / Data Governance**: `PIIMasker` class detects and masks sensitive information before data ingestion.
- **Modal Cloud GPU Integration (Enterprise)**: Offloads heavy training jobs to Modal with enterprise patterns for efficiency and fault tolerance.
- **Universal Data Ingest (Modal)**: Generates production-grade Modal scripts for data download from various sources into distributed volumes.
- **Hugging Face Hub Integration**: Enables push/pull of models and datasets, model card generation, and deployment to Spaces.
- **Weights & Biases Integration (with System Observability)**: Experiment tracking, metric logging, model versioning, and system health monitoring.
- **Unified Connections Tab**: Centralized configuration for Kaggle, Modal, Hugging Face, and W&B API credentials.
- **MaxAutoML Unified Engine**: Provides unified configuration, task detection, intelligent preprocessing, model building, and training across multiple frameworks with time-series awareness.
- **Algorithm Registry & Recommendations**: Centralized registry for 25+ ML algorithms with automatic recommendations.
- **Adaptive Hyperparameter Tuning**: Utilizes Bayesian optimization, adaptive learning rate scheduling, and adaptive training control.
- **Advanced Training Modes**: Supports LightGBM Incremental Training, Population-Based Training (PBT), and SGD Online Learning.
- **Feature Engineering**: `AdvancedFeatureEngineer` for generating sophisticated market features with leakage-safe operations.
- **Feature Pruning**: `FeaturePruner` for dimensionality reduction based on importance-based ranking.
- **Class Imbalance Handling**: Correct `scale_pos_weight`, `class_weight='balanced'`, and UI warnings for extreme imbalance.
- **Pasture Biomass Multimodal Pipeline**: End-to-end pipeline including ResNet50 feature extraction, LeakageSafePCA, data pivoting, and physical consistency constraints.
- **Gold-Medal Post-Processing**: Implements mean-smoothing, percentile clipping, conservation snap, and proper cross-validation.
- **Reference Models**: Includes CSIRO Biomass Gold-Medal Notebook.
- **Hull Tactical Market Strategy**: Integrated Gold-Medal Financial Strategy for market analysis.

### Feature Specifications
- **Competition Management**: UI for selection, analysis, and dataset management; Universal Competition Framework.
- **Advanced Model Development**: 25+ algorithms, automated hyperparameter tuning, cross-validation, overfitting/underfitting detection.
- **Kaggle Competition Readiness**: Addresses distribution shift, data leakage, adversarial validation, time-based validation, and feature stability.
- **ECG Digitization Gold-Medal Pipeline v6.0**: Advanced ECG signal processing including LAB Color Space Grid Removal, Morphological Text Suppression, Power-Weighted Centroid, Baseline Correction, and Clinical Validation Metrics.
- **Pasture Biomass Gold-Medal Workflow**: Professional competition pipeline featuring held-out test sets, seed averaging ensembles, Gold-Medal Enhancements, adversarial validation, and pseudo-labeling.
- **Hull Tactical Market Workflow**: Professional Quantitative Finance pipeline with financial feature engineering, threshold-aware allocation, ensemble optimization, and financial risk metrics.
- **Performance Optimization**: Lazy-loading, button-triggered execution, data sampling, and caching.
- **AI-Powered Code Compression**: Gemini AI engine compresses generated code.
- **Automatic Code Quality Refinement**: Iteratively improves generated code.
- **Intermediate Transparency Logging**: Detailed logging and UI display of AI synthesis stages.
- **Semantic Task Clustering**: Knowledge base for reusing solutions.
- **Explicit Backtracking Controller**: Systematic multi-level decision tree exploration.
- **Comprehensive Data Leakage Prevention**: `LeakagePreventionPipeline` for multi-strategy column filtering and advanced detection.
- **Time Series Best Practices**: Incorporates correct feature engineering order, imputation, conditional scaling, and chronological validation splits.
- **Extreme Regularization Presets**: Pre-tuned hyperparameters for shallow, highly regularized trees including a "Finance-Optimized Preset".
- **Improved Forecasting Pipeline**: Modules for enhanced stock forecasting, including Target Mode Transformation, Calendar Features, Rolling Normalization, Enhanced Metrics, and a Universal Ensemble.
- **Strategy Builder Module**: Competition-specific module for S&P 500 Kaggle competition.
- **External Assets Manager**: Integrates external datasets, pre-trained model weights, and Python-based feature extraction logic.

### System Design Choices
- **Adaptive Strategies & Pattern Learning**: Implements template injection, self-healing code, AST reconstruction, and pre-prompt validation with a dual model ensemble and hybrid multi-strategy approach.
- **Validator-Aligned Prompt Engineering**: Enhanced synthesis prompts with comprehensive validator rules.
- **Flexible Gemini Model Selection**: Allows switching between Gemini 1.5 Flash and Gemini 2.5 Pro.
- **Automatic Syntax Error Repair**: Four-layer auto-fix system and extended retries.
- **Robust Code Extraction & Validation**: Five-strategy fallback for code extraction and pre-generation syntax validation.
- **ARC Determinism Learning**: Incorporates pre-execution validation to prevent non-deterministic code patterns.
- **Code Generation Flexibility**: Dual-mode generation supporting Python Standard Library only for ARC/Program Synthesis, and full library access for other competitions.

## External Dependencies
- **Streamlit**: Web application framework.
- **scikit-learn**: Traditional machine learning algorithms.
- **pandas/numpy**: Data manipulation and numerical computing.
- **requests**: HTTP client for API interactions.
- **TensorFlow**: Deep learning models.
- **PyTorch**: Deep learning framework.
- **spaCy**: Advanced NLP processing.
- **NLTK**: Natural Language Toolkit for text processing.
- **XGBoost**: Gradient boosting algorithm.
- **LightGBM**: Gradient boosting algorithm.
- **scikit-optimize**: Bayesian optimization.
- **SQLite**: Local database persistence.
- **Kaggle API**: Competition data access and submission.
- **Plotly**: Charting and visualization.
- **Gemini AI**: For AI-powered features.