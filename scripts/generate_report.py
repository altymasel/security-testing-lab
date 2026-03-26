from pathlib import Path
import re

SCAN_FILE = Path("scans/nmap_scan.txt")
REPORT_FILE = Path("reports/final_report.md")


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


def build_report(scan_text, findings, risk_level):
    findings_text = "\n".join(f"- {item}" for item in findings)

    return f"""# Security Testing Report

## Target
http://localhost:8080

## Purpose
This report summarizes the results of an Nmap service discovery scan.

## Raw Scan Output
{scan_text}

## Findings
{findings_text}

## Risk Level
{risk_level}

## Interpretation
The scan confirms that port 8080 is open and serving an HTTP application using Apache.

## Recommendations
- Review Apache version for known vulnerabilities
- Limit exposed services
- Add web vulnerability scanning in the next phase
"""


def main():
    scan_text = read_scan()
    findings, risk_level = analyze_scan(scan_text)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        build_report(scan_text, findings, risk_level),
        encoding="utf-8"
    )

    print("Report generated at:", REPORT_FILE)


if __name__ == "__main__":
    main()
