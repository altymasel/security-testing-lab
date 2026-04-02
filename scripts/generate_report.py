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
    return match.group(1) if match else None


def analyze_scan(scan_text):
    findings = []

    if "8080/tcp open" in scan_text:
        findings.append("Port 8080 is open.")

    if "http" in scan_text.lower():
        findings.append("HTTP service detected.")

    if "apache" in scan_text.lower():
        findings.append("Apache server detected.")

    version = extract_apache_version(scan_text)
    if version:
        findings.append(f"Apache version {version} detected.")

    return findings


def calculate_risk(scan_text):
    if "8080/tcp open" in scan_text:
        return "Medium"
    return "Low"


def check_zap():
    return ZAP_FILE.exists()


def parse_zap():
    if not ZAP_FILE.exists():
        return ["No ZAP findings available."]

    content = ZAP_FILE.read_text(encoding="utf-8", errors="ignore")
    findings = []

    if "Cookie No HttpOnly Flag" in content:
        findings.append("Cookies missing HttpOnly flag.")

    if "Content Security Policy (CSP) Header Not Set" in content:
        findings.append("Missing Content Security Policy header.")

    if "X-Content-Type-Options Header Missing" in content:
        findings.append("Missing X-Content-Type-Options header.")

    if "Server Leaks Version Information" in content:
        findings.append("Server version information exposed.")

    if "Missing Anti-clickjacking Header" in content:
        findings.append("Missing clickjacking protection.")

    if not findings:
        findings.append("No major issues detected.")

    return findings


def build_report(scan, findings, risk, zap_exists, zap_findings):
    findings_text = "\n".join(f"- {f}" for f in findings)
    zap_findings_text = "\n".join(f"- {z}" for z in zap_findings)

    zap_status = "Available" if zap_exists else "Not found"

    return f"""# Security Testing Report

## Target
http://localhost:8080

## Findings (Nmap)
{findings_text}

## Risk Level
{risk}

## ZAP Scan
Status: {zap_status}

## ZAP Findings
{zap_findings_text}

## Summary
The system exposes an HTTP service on port 8080. ZAP analysis shows several security weaknesses such as missing headers and insecure cookie settings.

## Recommendations
- Review server configuration
- Add security headers
- Secure cookies
- Investigate ZAP findings
"""


def main():
    scan = read_scan()
    findings = analyze_scan(scan)
    risk = calculate_risk(scan)

    zap_exists = check_zap()
    zap_findings = parse_zap()

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        build_report(scan, findings, risk, zap_exists, zap_findings),
        encoding="utf-8"
    )

    print("Report generated:", REPORT_FILE)


if __name__ == "__main__":
    main()
