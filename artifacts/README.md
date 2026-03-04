# Artifacts — Session Traceability Note

All three files in this folder were generated during a single platform session:
**`sess_20260304_232917_dd3b5e`**

They form a traceable end-to-end audit chain across the following pipeline stages:

| Stage | File | Evidence |
|---|---|---|
| Data Ingestion & PII Masking | `audit_log_sample.jsonl` | 11 masking events — email/phone columns detected, SHA-256 hashes recorded before and after redaction |
| Model Training | `audit_log_sample.jsonl` | Training run entry linked to same session ID, confirming model was trained on masked data |
| Security Verification | `security_cert.json` | OWASP LLM01/LLM02 checks passed — AST import whitelist enforced, `self_check()` structural safety verified — session ID matches |
| Governance & Compliance | `compliance_report.html` | NIST AI RMF and EU AI Act compliance scan — open in a browser to view the full report with risk ratings and recommendations |

## How to verify the chain

1. Open `audit_log_sample.jsonl` — every entry carries `"session_id": "sess_20260304_232917_dd3b5e"`
2. Open `security_cert.json` — `session_id` field matches
3. The `audit_log_sample.jsonl` shows PII masking events followed by a `training_run` event, confirming the model was trained on governance-compliant, redacted data

*These are real platform outputs — not mock data.*
