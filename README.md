# Security Testing Lab

## Overview
This project demonstrates a basic penetration testing workflow using a local vulnerable web application.

## What I Built
- Set up a vulnerable web application (DVWA) using Docker
- Performed service discovery with Nmap
- Built a Python script to parse scan results and generate a structured report
- Ran OWASP ZAP baseline scans to identify web security misconfigurations
- Stored both summary and full scan reports in the project repository

## Tech Stack
- Docker
- DVWA
- Nmap
- Python
- OWASP ZAP

## Workflow
1. Run DVWA locally in Docker
2. Perform service discovery using Nmap
3. Save raw scan results
4. Generate a structured report with Python
5. Run OWASP ZAP baseline scan
6. Review vulnerability findings in the HTML report

## Findings Observed
- Open port 8080 detected
- Apache web server identified (version 2.4.25)
- Missing security headers
- Cookie without HttpOnly flag
- Content Security Policy not set
- Server version information disclosure

## Reports
- `reports/final_report.md` — Python-generated summary report
- `reports/zap_report.html` — OWASP ZAP vulnerability scan report
- `reports/zap.yaml` — ZAP automation configuration

## How to Run

```bash
docker start dvwa
nmap -sV localhost -p 8080 -oN scans/nmap_scan.txt
python3 scripts/generate_report.py
docker run -v "$(pwd):/zap/wrk" -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:8080 -r zap_report.html
