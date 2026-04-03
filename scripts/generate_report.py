from pathlib import Path
import re
import os

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

    if not findings:
        findings.append("No obvious Nmap findings detected.")

    return findings


def calculate_risk(scan_text, zap_findings):
    score = 0

    if "8080/tcp open" in scan_text:
        score += 1

    if zap_findings:
        score += len([z for z in zap_findings if "No ZAP findings" not in z])

    if score >= 5:
        return "High"
    if score >= 2:
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
        findings.append("No major ZAP issues detected.")

    return findings


def explain_findings_with_ai(nmap_findings, zap_findings):
    fallback = """Executive Summary:
The application exposes a web service with several security weaknesses.

Top Risks:
- Insecure cookie handling
- Missing security headers
- Information disclosure

Recommendations:
- Add security headers such as CSP, X-Frame-Options, and X-Content-Type-Options
- Secure cookies with HttpOnly and Secure flags
- Limit server version disclosure in HTTP responses
"""

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return fallback + "\n(AI not configured)"

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        combined = "\n".join(
            [f"- {item}" for item in (nmap_findings + zap_findings)]
        )

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "You are a security analyst.\n\n"
                        "Given these findings, write:\n"
                        "1. A short executive summary\n"
                        "2. The top 3 most important risks\n"
                        "3. Practical recommendations\n\n"
                        "Keep the language simple and concise.\n\n"
                        f"Findings:\n{combined}"
                    ),
                }
            ],
        )

        parts = []
        for block in response.content:
            text = getattr(block, "text", None)
            if text:
                parts.append(text)

        ai_text = "\n".join(parts).strip()
        return ai_text if ai_text else fallback + "\n(AI returned no text)"

    except Exception:
        return fallback + "\n(AI generated explanation unavailable; fallback summary used)"


def build_report(scan_text, nmap_findings, risk_level, zap_exists, zap_findings, ai_summary):
    nmap_text = "\n".join(f"- {item}" for item in nmap_findings)
    zap_text = "\n".join(f"- {item}" for item in zap_findings)
    zap_status = "Available" if zap_exists else "Not found"

    return f"""# Security Testing Report

## Target
http://localhost:8080

## Service Discovery (Nmap)
{nmap_text}

## Risk Level
{risk_level}

## ZAP Scan
Status: {zap_status}

## ZAP Findings
{zap_text}

## AI Analysis
{ai_summary}

## Raw Scan Output
{scan_text}

## Summary
The application exposes an HTTP service on port 8080. Security analysis identified multiple weaknesses related to headers, cookies, and information disclosure.

## Recommendations
- Update Apache to a secure supported version
- Add missing security headers
- Secure cookies with HttpOnly and Secure flags
- Reduce server information disclosure
- Review the ZAP HTML report for additional detail
"""


def main():
    scan_text = read_scan()
    nmap_findings = analyze_scan(scan_text)
    zap_exists = check_zap()
    zap_findings = parse_zap()
    risk_level = calculate_risk(scan_text, zap_findings)
    ai_summary = explain_findings_with_ai(nmap_findings, zap_findings)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        build_report(
            scan_text,
            nmap_findings,
            risk_level,
            zap_exists,
            zap_findings,
            ai_summary,
        ),
        encoding="utf-8",
    )

    print("Report generated:", REPORT_FILE)


if __name__ == "__main__":
    main()
