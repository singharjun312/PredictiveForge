"""
ISO/IEC 42001:2023 AI Management System Compliance Validator
Validates Jupyter notebooks against ISO 42001 clauses 4–10.
Generates structured compliance reports with risk ratings.
"""

import re
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ISOCheck:
    clause: str
    title: str
    requirement: str
    status: str      # "pass", "warn", "fail"
    severity: str    # "low", "medium", "high", "critical"
    finding: str
    recommendation: str


@dataclass
class ISO42001Report:
    timestamp: str
    notebook_name: str
    overall_score: float
    risk_level: str
    clause_scores: Dict[str, float]
    checks: List[ISOCheck] = field(default_factory=list)


ISO42001_CHECKS = [
    # Clause 4 — Context of the Organisation
    {
        "clause": "4.1",
        "title": "Understanding the Organisation",
        "requirement": "AI system purpose and context are documented",
        "check_fn": "_check_purpose_documentation",
        "severity": "high",
    },
    {
        "clause": "4.2",
        "title": "Interested Parties",
        "requirement": "Stakeholders and their requirements are identified",
        "check_fn": "_check_stakeholder_identification",
        "severity": "medium",
    },
    # Clause 6 — Planning
    {
        "clause": "6.1",
        "title": "Risk & Opportunity Assessment",
        "requirement": "AI-specific risks and opportunities are assessed",
        "check_fn": "_check_risk_assessment",
        "severity": "high",
    },
    {
        "clause": "6.2",
        "title": "AI Objectives",
        "requirement": "Measurable AI system objectives are defined",
        "check_fn": "_check_objectives_defined",
        "severity": "medium",
    },
    # Clause 7 — Support
    {
        "clause": "7.1",
        "title": "Resources",
        "requirement": "Adequate resources for AI system are identified",
        "check_fn": "_check_resources_identified",
        "severity": "low",
    },
    {
        "clause": "7.4",
        "title": "Communication",
        "requirement": "AI system documentation and communication controls exist",
        "check_fn": "_check_documentation_quality",
        "severity": "medium",
    },
    # Clause 8 — Operation
    {
        "clause": "8.1",
        "title": "Operational Planning",
        "requirement": "Data governance and preprocessing controls are implemented",
        "check_fn": "_check_data_governance",
        "severity": "high",
    },
    {
        "clause": "8.2",
        "title": "AI System Impact Assessment",
        "requirement": "Potential negative impacts of AI outputs are assessed",
        "check_fn": "_check_impact_assessment",
        "severity": "critical",
    },
    {
        "clause": "8.4",
        "title": "Data for AI Systems",
        "requirement": "Training data quality, lineage, and validation are controlled",
        "check_fn": "_check_data_quality",
        "severity": "high",
    },
    {
        "clause": "8.5",
        "title": "AI System Development",
        "requirement": "Model validation, testing, and reproducibility controls are present",
        "check_fn": "_check_model_validation",
        "severity": "high",
    },
    {
        "clause": "8.6",
        "title": "AI System in Production",
        "requirement": "Monitoring and performance tracking controls are implemented",
        "check_fn": "_check_monitoring",
        "severity": "high",
    },
    # Clause 9 — Performance Evaluation
    {
        "clause": "9.1",
        "title": "Monitoring & Measurement",
        "requirement": "AI system performance metrics are tracked and reported",
        "check_fn": "_check_performance_metrics",
        "severity": "medium",
    },
    {
        "clause": "9.2",
        "title": "Internal Audit",
        "requirement": "Audit trails and logging mechanisms are present",
        "check_fn": "_check_audit_trail",
        "severity": "high",
    },
    # Clause 10 — Improvement
    {
        "clause": "10.1",
        "title": "Nonconformity & Corrective Action",
        "requirement": "Error handling and corrective mechanisms are implemented",
        "check_fn": "_check_error_handling",
        "severity": "medium",
    },
    {
        "clause": "10.2",
        "title": "Continual Improvement",
        "requirement": "Model retraining and improvement processes are defined",
        "check_fn": "_check_improvement_process",
        "severity": "low",
    },
]

SEVERITY_WEIGHTS = {"critical": 4, "high": 3, "medium": 2, "low": 1}
STATUS_SCORES = {"pass": 1.0, "warn": 0.5, "fail": 0.0}


class ISO42001Validator:

    def validate_notebook(self, notebook_content: dict, notebook_name: str = "notebook.ipynb") -> ISO42001Report:
        parsed = self._parse_notebook(notebook_content)
        checks = []

        for chk in ISO42001_CHECKS:
            fn = getattr(self, chk["check_fn"], None)
            if fn:
                status, finding, recommendation = fn(parsed)
            else:
                status, finding, recommendation = "warn", "Check not implemented.", "Manual review required."

            checks.append(ISOCheck(
                clause=chk["clause"],
                title=chk["title"],
                requirement=chk["requirement"],
                status=status,
                severity=chk["severity"],
                finding=finding,
                recommendation=recommendation,
            ))

        overall_score, risk_level, clause_scores = self._compute_scores(checks)

        return ISO42001Report(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            notebook_name=notebook_name,
            overall_score=overall_score,
            risk_level=risk_level,
            clause_scores=clause_scores,
            checks=checks,
        )

    def _parse_notebook(self, notebook_content: dict) -> dict:
        code_cells, markdown_cells, all_imports = [], [], []
        all_code, all_markdown = "", ""

        for cell in notebook_content.get("cells", []):
            source = "".join(cell.get("source", []))
            if cell.get("cell_type") == "code":
                code_cells.append(source)
                all_code += source + "\n"
                imports = re.findall(r"^(?:import|from)\s+[\w.]+", source, re.MULTILINE)
                all_imports.extend(imports)
            elif cell.get("cell_type") == "markdown":
                markdown_cells.append(source)
                all_markdown += source + "\n"

        return {
            "code_cells": code_cells,
            "markdown_cells": markdown_cells,
            "all_imports": all_imports,
            "all_code": all_code,
            "all_markdown": all_markdown,
            "cell_count": len(notebook_content.get("cells", [])),
        }

    def _compute_scores(self, checks: List[ISOCheck]):
        clause_groups = {}
        for c in checks:
            clause_num = c.clause.split(".")[0]
            clause_groups.setdefault(clause_num, []).append(c)

        clause_scores = {}
        for clause_num, clause_checks in clause_groups.items():
            total_weight = sum(SEVERITY_WEIGHTS.get(c.severity, 1) for c in clause_checks)
            earned = sum(SEVERITY_WEIGHTS.get(c.severity, 1) * STATUS_SCORES.get(c.status, 0)
                         for c in clause_checks)
            clause_scores[f"Clause {clause_num}"] = round((earned / total_weight) * 100, 1) if total_weight else 100.0

        total_weight = sum(SEVERITY_WEIGHTS.get(c.severity, 1) for c in checks)
        earned = sum(SEVERITY_WEIGHTS.get(c.severity, 1) * STATUS_SCORES.get(c.status, 0) for c in checks)
        overall_score = round((earned / total_weight) * 100, 1) if total_weight else 100.0

        critical_fails = sum(1 for c in checks if c.status == "fail" and c.severity == "critical")
        high_fails = sum(1 for c in checks if c.status == "fail" and c.severity == "high")

        if critical_fails > 0 or overall_score < 40:
            risk_level = "Critical"
        elif high_fails > 1 or overall_score < 60:
            risk_level = "High"
        elif overall_score < 80:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return overall_score, risk_level, clause_scores

    # --- Check Functions ---

    def _check_purpose_documentation(self, p):
        kw = ["purpose", "objective", "goal", "intended use", "use case", "overview", "introduction"]
        if any(k in p["all_markdown"].lower() for k in kw):
            return "pass", "AI system purpose is documented in notebook markdown.", ""
        if any(k in p["all_code"].lower() for k in ["#purpose", "#objective", "#goal"]):
            return "warn", "Partial purpose documentation found in code comments.", "Move purpose documentation to a dedicated markdown cell."
        return "fail", "No documentation of AI system purpose or intended use found.", "Add a markdown cell describing the AI system's purpose, intended use, and scope."

    def _check_stakeholder_identification(self, p):
        kw = ["stakeholder", "user", "client", "customer", "end user", "beneficiary"]
        if any(k in p["all_markdown"].lower() for k in kw):
            return "pass", "Stakeholder references found in documentation.", ""
        return "warn", "No explicit stakeholder identification found.", "Document who the intended users and affected parties are."

    def _check_risk_assessment(self, p):
        kw = ["risk", "threat", "vulnerability", "bias", "fairness", "limitation"]
        found = [k for k in kw if k in p["all_markdown"].lower() or k in p["all_code"].lower()]
        if len(found) >= 3:
            return "pass", f"Risk assessment indicators found: {', '.join(found[:3])}.", ""
        if found:
            return "warn", f"Partial risk assessment: {', '.join(found)}.", "Expand risk assessment to cover bias, limitations, and failure modes."
        return "fail", "No risk assessment or threat identification found.", "Add a dedicated section assessing AI-specific risks including bias, data quality, and model failure modes."

    def _check_objectives_defined(self, p):
        kw = ["accuracy", "f1", "auc", "rmse", "mae", "r2", "metric", "target", "threshold"]
        found = [k for k in kw if k in p["all_code"].lower()]
        if len(found) >= 2:
            return "pass", f"Measurable objectives defined via metrics: {', '.join(found[:3])}.", ""
        return "warn", "Measurable AI objectives not clearly defined.", "Define specific, measurable performance targets (e.g., accuracy > 0.90, AUC > 0.85)."

    def _check_resources_identified(self, p):
        if p["all_imports"]:
            return "pass", f"{len(p['all_imports'])} library imports identified as computational resources.", ""
        return "warn", "Resource identification not explicit.", "Document computational and data requirements."

    def _check_documentation_quality(self, p):
        md_count = len(p["markdown_cells"])
        code_count = len(p["code_cells"])
        ratio = md_count / max(code_count, 1)
        if ratio >= 0.4:
            return "pass", f"Documentation ratio adequate: {md_count} markdown cells vs {code_count} code cells.", ""
        if md_count > 0:
            return "warn", f"Documentation sparse: {md_count} markdown cells for {code_count} code cells.", "Add more markdown documentation explaining each section."
        return "fail", "No markdown documentation found.", "Add markdown cells to document methodology, decisions, and findings."

    def _check_data_governance(self, p):
        kw = ["dropna", "fillna", "impute", "clean", "preprocess", "validate", "dtype", "schema"]
        found = [k for k in kw if k in p["all_code"].lower()]
        if len(found) >= 3:
            return "pass", f"Data governance controls found: {', '.join(found[:4])}.", ""
        if found:
            return "warn", f"Partial data governance: {', '.join(found)}.", "Implement comprehensive data validation and preprocessing controls."
        return "fail", "No data preprocessing or validation controls found.", "Add data validation, missing value handling, and schema checks before model training."

    def _check_impact_assessment(self, p):
        kw = ["impact", "consequence", "harm", "fairness", "discrimination", "bias", "false positive", "false negative"]
        found = [k for k in kw if k in p["all_markdown"].lower()]
        if len(found) >= 2:
            return "pass", f"Impact assessment indicators found: {', '.join(found[:3])}.", ""
        if found:
            return "warn", "Partial impact assessment found.", "Expand assessment to cover potential harms, bias, and fairness implications."
        return "fail", "No AI impact assessment found.", "Add a mandatory impact assessment section covering potential harms, affected groups, and mitigation strategies."

    def _check_data_quality(self, p):
        kw = ["train_test_split", "cross_val", "validation", "train_size", "test_size", "stratif"]
        found = [k for k in kw if k in p["all_code"].lower()]
        if found:
            return "pass", f"Data quality controls found: {', '.join(found[:3])}.", ""
        if "random_state" in p["all_code"].lower() or "seed" in p["all_code"].lower():
            return "warn", "Partial data quality: reproducibility seed found but no validation split.", "Add train/test split and validation strategy."
        return "fail", "No data quality or validation controls found.", "Implement train/test split, cross-validation, and data lineage documentation."

    def _check_model_validation(self, p):
        kw = ["random_state", "seed", "set_seed", "np.random.seed", "torch.manual_seed"]
        reproducible = any(k in p["all_code"].lower() for k in kw)
        tested = any(k in p["all_code"].lower() for k in ["predict", "score", "evaluate", "test"])
        if reproducible and tested:
            return "pass", "Model validation with reproducibility controls found.", ""
        if tested:
            return "warn", "Model testing found but no reproducibility seed set.", "Add random_state/seed for deterministic, reproducible results."
        return "fail", "No model validation or testing found.", "Add model evaluation code with reproducibility seeds and performance metrics."

    def _check_monitoring(self, p):
        kw = ["monitor", "drift", "alert", "log", "track", "wandb", "mlflow", "callback"]
        found = [k for k in kw if k in p["all_code"].lower()]
        if len(found) >= 2:
            return "pass", f"Monitoring controls found: {', '.join(found[:3])}.", ""
        if found:
            return "warn", f"Partial monitoring: {', '.join(found)}.", "Implement comprehensive monitoring including data drift detection."
        return "fail", "No monitoring or production tracking controls found.", "Add performance monitoring, data drift detection, and alerting mechanisms."

    def _check_performance_metrics(self, p):
        kw = ["accuracy", "f1_score", "roc_auc", "classification_report", "confusion_matrix",
              "mean_squared_error", "r2_score", "precision", "recall"]
        found = [k for k in kw if k in p["all_code"].lower()]
        if len(found) >= 2:
            return "pass", f"Performance metrics tracked: {', '.join(found[:3])}.", ""
        if found:
            return "warn", f"Limited metrics: only {', '.join(found)} found.", "Add comprehensive evaluation metrics suite."
        return "fail", "No performance measurement found.", "Implement quantitative performance metrics and reporting."

    def _check_audit_trail(self, p):
        kw = ["logging", "log.", "audit", "print(", "timestamp", "datetime", "record"]
        found = [k for k in kw if k in p["all_code"].lower()]
        if len(found) >= 3:
            return "pass", f"Audit trail mechanisms found: {', '.join(found[:3])}.", ""
        if found:
            return "warn", f"Partial audit trail: {', '.join(found)}.", "Implement structured logging with timestamps for full auditability."
        return "fail", "No audit trail or logging found.", "Add structured logging with timestamps to track all model decisions and data operations."

    def _check_error_handling(self, p):
        try_count = p["all_code"].lower().count("try:")
        except_count = p["all_code"].lower().count("except")
        if try_count >= 2 and except_count >= 2:
            return "pass", f"Error handling present: {try_count} try/except blocks.", ""
        if try_count >= 1:
            return "warn", "Minimal error handling found.", "Add comprehensive error handling across all critical operations."
        return "fail", "No error handling found.", "Implement try/except blocks for all data loading, model training, and prediction operations."

    def _check_improvement_process(self, p):
        kw = ["retrain", "update", "improve", "iteration", "version", "v2", "next steps", "future"]
        if any(k in p["all_markdown"].lower() for k in kw):
            return "pass", "Improvement process and future iterations documented.", ""
        return "warn", "No continual improvement process documented.", "Add a section describing model update schedule, retraining triggers, and version control strategy."


def generate_iso42001_html(report: ISO42001Report) -> str:
    risk_colors = {"Low": "#006600", "Medium": "#cc8800", "High": "#cc4400", "Critical": "#8b0000"}
    ov_color = risk_colors.get(report.risk_level, "#333")

    clause_rows = ""
    for clause_name, score in report.clause_scores.items():
        bar_color = "#006600" if score >= 80 else "#cc8800" if score >= 60 else "#cc4400"
        clause_rows += f"""
        <tr>
            <td>{clause_name}</td>
            <td>
                <div style="background:#eee;border-radius:4px;height:16px;width:200px;display:inline-block">
                    <div style="background:{bar_color};height:16px;width:{score*2}px;border-radius:4px"></div>
                </div>
                &nbsp;{score}%
            </td>
        </tr>"""

    check_rows = ""
    for c in report.checks:
        icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}.get(c.status, "?")
        sev_color = {"critical": "#8b0000", "high": "#cc4400", "medium": "#cc8800", "low": "#006600"}.get(c.severity, "#333")
        check_rows += f"""
        <tr>
            <td>{icon}</td>
            <td><strong>{c.clause}</strong> {c.title}</td>
            <td><span style="color:{sev_color};font-weight:bold">{c.severity.upper()}</span></td>
            <td>{c.finding}</td>
            <td>{c.recommendation or '—'}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ISO/IEC 42001:2023 Compliance Report — PredictiveForge</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 30px; color: #222; max-width: 1000px; }}
  h1 {{ color: #003366; border-bottom: 2px solid #003366; }}
  h2 {{ color: #005599; margin-top: 25px; }}
  .metric {{ display: inline-block; padding: 12px 20px; margin: 6px; border-radius: 8px; text-align: center; min-width: 110px; }}
  .metric .num {{ font-size: 26px; font-weight: bold; }}
  .metric .lbl {{ font-size: 12px; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 10px; font-size: 13px; }}
  th {{ background: #003366; color: white; padding: 8px 12px; text-align: left; }}
  td {{ padding: 7px 12px; border-bottom: 1px solid #ddd; vertical-align: top; }}
  tr:nth-child(even) {{ background: #f4f8ff; }}
  @media print {{ body {{ margin: 15px; }} }}
</style>
</head>
<body>
<h1>ISO/IEC 42001:2023 AI Management System Compliance Report</h1>
<p><strong>Platform:</strong> PredictiveForge &nbsp;|&nbsp;
<strong>Notebook:</strong> {report.notebook_name} &nbsp;|&nbsp;
<strong>Generated:</strong> {report.timestamp}</p>

<div>
  <div class="metric" style="background:#e8f0fe">
    <div class="num" style="color:#003366">{report.overall_score}%</div>
    <div class="lbl">Overall Score</div>
  </div>
  <div class="metric" style="background:{ov_color};color:white">
    <div class="num">{report.risk_level}</div>
    <div class="lbl">Risk Level</div>
  </div>
  <div class="metric" style="background:#f0fff0">
    <div class="num" style="color:#006600">{sum(1 for c in report.checks if c.status=='pass')}</div>
    <div class="lbl">Passed</div>
  </div>
  <div class="metric" style="background:#fff8cc">
    <div class="num" style="color:#cc8800">{sum(1 for c in report.checks if c.status=='warn')}</div>
    <div class="lbl">Warnings</div>
  </div>
  <div class="metric" style="background:#ffdddd">
    <div class="num" style="color:#8b0000">{sum(1 for c in report.checks if c.status=='fail')}</div>
    <div class="lbl">Failed</div>
  </div>
</div>

<h2>Clause Scores</h2>
<table>
<tr><th>Clause</th><th>Score</th></tr>
{clause_rows}
</table>

<h2>Detailed Findings</h2>
<table>
<tr><th>Status</th><th>Clause</th><th>Severity</th><th>Finding</th><th>Recommendation</th></tr>
{check_rows}
</table>

<hr>
<p style="font-size:11px;color:#888;">ISO/IEC 42001:2023 AI Management System compliance report generated by PredictiveForge.
Standard reference: ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management system.
Generated: {report.timestamp}</p>
</body>
</html>"""
