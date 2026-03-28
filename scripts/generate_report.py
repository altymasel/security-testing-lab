from pathlib import Path
import re

SCAN_FILE = Path("scans/nmap_scan.txt")
REPORT_FILE = Path("reports/final_report.md")
ZAP_FILE = Path("reports/zap_report.html")


def read_scan():
    if not SCAN_FILE.exists():
        return "Scan file not found."
    return SCAN_FILE.read_text(encoding="utf-8", errors="ignore")


def extract_apache_version(scan_text):
    match = re.search(r"Apache httpd ([0-9.]+)", scan_text)
    if match:
        return match.group(1)
    return None


def calculate_risk(scan_text, apache_version):
    if "8080/tcp open" in scan_text and apache_version:
        return "Medium"
    if "8080/tcp open" in scan_text:
        return "Low"
    return "Informational"


def analyze_scan(scan_text):
    findings = []

    if "8080/tcp open" in scan_text:
        findings.append("Port 8080 is open and accessible on localhost.")

    if "http" in scan_text.lower():
        findings.append("An HTTP service was detected on the target.")

    if "apache" in scan_text.lower():
        findings.append("Apache web server was identified.")

    apache_version = extract_apache_version(scan_text)
    if apache_version:
        findings.append(f"Apache web server version {apache_version} was detected.")
        findings.append("Older Apache versions may contain known vulnerabilities if not patched.")

    if not findings:
        findings.append("No obvious findings were detected from the scan output.")

    risk_level = calculate_risk(scan_text, apache_version)
    return findings, risk_level


def check_zap_report():
    if ZAP_FILE.exists():
        return "ZAP scan report available: reports/zap_report.html"
    return "ZAP scan not found."


def build_report(scan_text, findings, risk_level, zap_summary):
    findings_text = "\n".join(f"- {item}" for item in findings)

    return f"""# Security Testing Report

## Target
http://localhost:8080

## Purpose
This report summarizes the results of Nmap service discovery and confirms whether an OWASP ZAP report is available.

## Raw Scan Output
{scan_text}

## Findings
{findings_text}

## Risk Level
{risk_level}

## ZAP Scan
{zap_summary}

## Interpretation
The scan confirms that port 8080 is open and serving an HTTP application using Apache. This indicates an exposed service that may be vulnerable depending on configuration and version. The ZAP section shows whether a web vulnerability report is also available.

## Recommendations
- Review Apache version for known vulnerabilities
- Limit exposed services
- Review the OWASP ZAP HTML report for web security issues
- Add deeper web vulnerability analysis in the next phase
"""


def main():
    scan_text = read_scan()
    findings, risk_level = analyze_scan(scan_text)
    zap_summary = check_zap_report()

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        build_report(scan_text, findings, risk_level, zap_summary),
        encoding="utf-8"
    )

    print("Report generated at:", REPORT_FILE)


if __name__ == "__main__":
    main()
