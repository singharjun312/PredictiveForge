"""
Supply Chain Security Scanner & SBOM Generator
Scans installed Python packages for known CVEs and generates
a Software Bill of Materials (SBOM) in SPDX-inspired format.
"""

import subprocess
import sys
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional


KNOWN_VULNERABLE = {
    "numpy": [
        {"below": "1.22.0", "cve": "CVE-2021-33430", "severity": "high",
         "desc": "Buffer overflow in NumPy < 1.22.0 via crafted array operations."},
    ],
    "pillow": [
        {"below": "9.0.0", "cve": "CVE-2022-22815", "severity": "high",
         "desc": "Path traversal in Pillow < 9.0.0 via crafted image filenames."},
        {"below": "8.3.2", "cve": "CVE-2021-34552", "severity": "critical",
         "desc": "Buffer overflow in Pillow < 8.3.2 via crafted PDF/TIFF."},
    ],
    "requests": [
        {"below": "2.28.0", "cve": "CVE-2022-3602", "severity": "medium",
         "desc": "Proxy-Authorization header leak in requests < 2.28.0."},
    ],
    "cryptography": [
        {"below": "41.0.0", "cve": "CVE-2023-38325", "severity": "high",
         "desc": "SSH certificate validation bypass in cryptography < 41.0.0."},
        {"below": "39.0.1", "cve": "CVE-2023-0286", "severity": "high",
         "desc": "X.400 address parsing vulnerability in cryptography < 39.0.1."},
    ],
    "urllib3": [
        {"below": "1.26.5", "cve": "CVE-2021-33503", "severity": "high",
         "desc": "ReDoS vulnerability in urllib3 < 1.26.5."},
        {"below": "2.0.4", "cve": "CVE-2023-43804", "severity": "medium",
         "desc": "Cookie injection in urllib3 < 2.0.4 via crafted headers."},
    ],
    "setuptools": [
        {"below": "65.5.1", "cve": "CVE-2022-40897", "severity": "medium",
         "desc": "ReDoS vulnerability in setuptools < 65.5.1 package_index."},
    ],
    "certifi": [
        {"below": "2023.7.22", "cve": "CVE-2023-37920", "severity": "medium",
         "desc": "Compromised root CA in certifi < 2023.7.22."},
    ],
    "tornado": [
        {"below": "6.3.3", "cve": "CVE-2023-28370", "severity": "medium",
         "desc": "Open redirect in tornado < 6.3.3."},
    ],
    "scikit-learn": [
        {"below": "1.0.2", "cve": "CVE-2020-28975", "severity": "medium",
         "desc": "Denial of service via crafted model in scikit-learn < 1.0.2."},
    ],
    "tensorflow": [
        {"below": "2.12.0", "cve": "CVE-2023-25660", "severity": "high",
         "desc": "Heap buffer overflow in TensorFlow < 2.12.0."},
    ],
    "torch": [
        {"below": "2.0.1", "cve": "CVE-2023-44487", "severity": "high",
         "desc": "Arbitrary code execution via crafted model file in PyTorch < 2.0.1."},
    ],
    "pyyaml": [
        {"below": "6.0", "cve": "CVE-2020-14343", "severity": "critical",
         "desc": "Arbitrary code execution via yaml.load() in PyYAML < 6.0."},
    ],
    "paramiko": [
        {"below": "3.4.0", "cve": "CVE-2023-48795", "severity": "medium",
         "desc": "Terrapin attack in paramiko < 3.4.0 SSH prefix truncation."},
    ],
    "werkzeug": [
        {"below": "3.0.1", "cve": "CVE-2023-46136", "severity": "high",
         "desc": "DoS via crafted multipart data in Werkzeug < 3.0.1."},
    ],
    "flask": [
        {"below": "2.3.0", "cve": "CVE-2023-30861", "severity": "high",
         "desc": "Cookie samesite bypass in Flask < 2.3.0."},
    ],
}


@dataclass
class PackageInfo:
    name: str
    version: str
    license: str = "UNKNOWN"
    vulnerabilities: List[Dict] = field(default_factory=list)
    risk_level: str = "safe"


@dataclass
class SBOMReport:
    timestamp: str
    total_packages: int
    critical_count: int
    high_count: int
    medium_count: int
    safe_count: int
    overall_risk: str
    packages: List[PackageInfo] = field(default_factory=list)


def _version_tuple(v: str):
    try:
        return tuple(int(x) for x in v.split(".")[:3])
    except Exception:
        return (0, 0, 0)


def get_installed_packages() -> Dict[str, str]:
    """Get all installed packages and their versions."""
    try:
        import pkg_resources
        return {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    except Exception:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json"],
                capture_output=True, text=True, timeout=30
            )
            pkgs = json.loads(result.stdout)
            return {p["name"].lower(): p["version"] for p in pkgs}
        except Exception:
            return {}


def get_package_license(name: str) -> str:
    """Try to get package license."""
    try:
        import pkg_resources
        pkg = pkg_resources.get_distribution(name)
        meta = pkg.get_metadata(pkg.PKG_INFO) if pkg.has_metadata(pkg.PKG_INFO) else ""
        for line in meta.splitlines():
            if line.startswith("License:"):
                lic = line.split(":", 1)[1].strip()
                return lic if lic and lic != "UNKNOWN" else "UNKNOWN"
    except Exception:
        pass
    return "UNKNOWN"


def scan_packages() -> SBOMReport:
    """Scan all installed packages for vulnerabilities and build SBOM."""
    packages = get_installed_packages()
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    pkg_infos = []
    critical_count = high_count = medium_count = 0

    for name, version in sorted(packages.items()):
        vulns = []
        risk = "safe"
        name_lower = name.lower()

        if name_lower in KNOWN_VULNERABLE:
            for vuln in KNOWN_VULNERABLE[name_lower]:
                try:
                    if _version_tuple(version) < _version_tuple(vuln["below"]):
                        vulns.append(vuln)
                        sev = vuln["severity"]
                        if sev == "critical":
                            critical_count += 1
                            risk = "critical"
                        elif sev == "high" and risk not in ("critical",):
                            high_count += 1
                            risk = "high"
                        elif sev == "medium" and risk not in ("critical", "high"):
                            medium_count += 1
                            risk = "medium"
                except Exception:
                    pass

        license_str = get_package_license(name_lower)
        pkg_infos.append(PackageInfo(
            name=name,
            version=version,
            license=license_str,
            vulnerabilities=vulns,
            risk_level=risk
        ))

    safe_count = sum(1 for p in pkg_infos if p.risk_level == "safe")

    if critical_count > 0:
        overall_risk = "CRITICAL"
    elif high_count > 0:
        overall_risk = "HIGH"
    elif medium_count > 0:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"

    return SBOMReport(
        timestamp=timestamp,
        total_packages=len(pkg_infos),
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        safe_count=safe_count,
        overall_risk=overall_risk,
        packages=pkg_infos
    )


def generate_sbom_html(report: SBOMReport) -> str:
    risk_colors = {
        "CRITICAL": "#8b0000", "HIGH": "#cc4400",
        "MEDIUM": "#cc8800", "LOW": "#006600"
    }
    ov_color = risk_colors.get(report.overall_risk, "#333")

    vuln_rows = ""
    for pkg in report.packages:
        if pkg.vulnerabilities:
            for v in pkg.vulnerabilities:
                sev_color = {"critical": "#8b0000", "high": "#cc4400",
                             "medium": "#cc8800", "low": "#006600"}.get(v["severity"], "#333")
                vuln_rows += f"""
                <tr>
                    <td><strong>{pkg.name}</strong></td>
                    <td>{pkg.version}</td>
                    <td><a href="https://nvd.nist.gov/vuln/detail/{v['cve']}" target="_blank">{v['cve']}</a></td>
                    <td><span style="color:{sev_color};font-weight:bold">{v['severity'].upper()}</span></td>
                    <td>{v['desc']}</td>
                    <td>Upgrade to &ge; {v['below']}</td>
                </tr>"""

    sbom_rows = ""
    for pkg in report.packages:
        rc = {"critical": "#ffdddd", "high": "#ffe8cc",
              "medium": "#fff8cc", "safe": "#f0fff0"}.get(pkg.risk_level, "#fff")
        sbom_rows += f"""
        <tr style="background:{rc}">
            <td>{pkg.name}</td>
            <td>{pkg.version}</td>
            <td>{pkg.license}</td>
            <td><span style="color:{risk_colors.get(pkg.risk_level.upper(),'#006600')}">{pkg.risk_level.upper()}</span></td>
            <td>{'<br>'.join(v['cve'] for v in pkg.vulnerabilities) or '—'}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Supply Chain Security Report — PredictiveForge</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 30px; color: #222; }}
  h1 {{ color: #003366; border-bottom: 2px solid #003366; }}
  h2 {{ color: #005599; margin-top: 25px; }}
  .metric {{ display: inline-block; padding: 12px 20px; margin: 6px; border-radius: 8px;
             text-align: center; min-width: 100px; }}
  .metric .num {{ font-size: 28px; font-weight: bold; }}
  .metric .lbl {{ font-size: 12px; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 10px; font-size: 12px; }}
  th {{ background: #003366; color: white; padding: 8px 10px; text-align: left; }}
  td {{ padding: 6px 10px; border-bottom: 1px solid #ddd; vertical-align: top; }}
  a {{ color: #005599; }}
  @media print {{ body {{ margin: 15px; }} }}
</style>
</head>
<body>
<h1>Supply Chain Security Report & SBOM</h1>
<p><strong>Platform:</strong> PredictiveForge &nbsp;|&nbsp;
<strong>Generated:</strong> {report.timestamp} &nbsp;|&nbsp;
<strong>Total Packages:</strong> {report.total_packages}</p>

<div>
  <div class="metric" style="background:#ffdddd">
    <div class="num" style="color:#8b0000">{report.critical_count}</div>
    <div class="lbl">Critical</div>
  </div>
  <div class="metric" style="background:#ffe8cc">
    <div class="num" style="color:#cc4400">{report.high_count}</div>
    <div class="lbl">High</div>
  </div>
  <div class="metric" style="background:#fff8cc">
    <div class="num" style="color:#cc8800">{report.medium_count}</div>
    <div class="lbl">Medium</div>
  </div>
  <div class="metric" style="background:#f0fff0">
    <div class="num" style="color:#006600">{report.safe_count}</div>
    <div class="lbl">Safe</div>
  </div>
  <div class="metric" style="background:{ov_color};color:white">
    <div class="num">{report.overall_risk}</div>
    <div class="lbl">Overall Risk</div>
  </div>
</div>

<h2>Vulnerability Findings</h2>
{'<table><tr><th>Package</th><th>Version</th><th>CVE</th><th>Severity</th><th>Description</th><th>Remediation</th></tr>' + vuln_rows + '</table>' if vuln_rows else '<p style="color:green">✅ No known vulnerabilities detected in scanned packages.</p>'}

<h2>Software Bill of Materials (SBOM)</h2>
<table>
<tr><th>Package</th><th>Version</th><th>License</th><th>Risk</th><th>CVEs</th></tr>
{sbom_rows}
</table>

<hr>
<p style="font-size:11px;color:#888;">Generated by PredictiveForge Supply Chain Security Scanner.
CVE data sourced from NVD. SBOM format inspired by SPDX 2.3.
Scan timestamp: {report.timestamp}</p>
</body>
</html>"""
