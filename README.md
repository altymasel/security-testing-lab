# 🔐 Security Testing Lab

## Overview
This project demonstrates an end-to-end security testing workflow using a vulnerable web application.

It combines service discovery, vulnerability scanning, automated reporting, and an AI-assisted analysis layer to simulate a real-world application security pipeline.

---

## 🚀 What This Project Does

- Runs a vulnerable web application using Docker (DVWA)
- Performs service discovery using Nmap
- Scans for vulnerabilities using OWASP ZAP
- Parses scan results using Python
- Generates a structured security report
- Adds an AI-assisted analysis layer for explanations and recommendations (with fallback support)

---

## 🧠 Architecture

DVWA (Docker)
↓
Nmap (Service Discovery)
↓
OWASP ZAP (Vulnerability Scanning)
↓
Python Script (Parsing + Reporting)
↓
AI Layer (Analysis & Recommendations)


---

## 🛠 Tech Stack

- Docker  
- DVWA  
- Nmap  
- OWASP ZAP  
- Python  

---

## 📊 Example Findings

- Open port 8080 detected  
- Apache web server identified  
- Missing security headers (CSP, X-Content-Type-Options)  
- Cookies without HttpOnly flag  
- Server version information disclosure  

---

## 🤖 AI-Assisted Analysis

This project includes an AI-assisted layer that enhances the report by:

- Generating executive summaries  
- Highlighting key risks  
- Providing actionable recommendations  

If the AI service is unavailable, the system gracefully falls back to a predefined summary to ensure consistent output.

---

## 📁 Project Structure

security-testing-lab/
├── reports/
│ ├── final_report.md
│ ├── zap_report.html
│ └── zap.yaml
├── scans/
│ └── nmap_scan.txt
├── scripts/
│ └── generate_report.py
└── README.md


---

## ▶️ How to Run

1. Start DVWA

```bash
docker start dvwa

2. Run Nmap scan

nmap -sV localhost -p 8080 -oN scans/nmap_scan.txt

3. Run OWASP ZAP scan

docker run -v "$(pwd):/zap/wrk" -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:8080 -r zap_report.html

4. Generate report

python3 scripts/generate_report.py

5. View report

open reports/final_report.md

📸 Screenshots
<img width="1791" height="1032" alt="Screenshot 2026-04-03 at 3 08 53 PM" src="https://github.com/user-attachments/assets/02183daa-6963-48b3-abc7-548a7f3c578d" />

