# Security Testing Lab

## Overview
This project demonstrates a basic penetration testing workflow using a local vulnerable application.

## What I Built
- Set up a vulnerable web application (DVWA) using Docker
- Performed service discovery using Nmap
- Parsed scan results using Python
- Generated a structured security report with risk classification

## Tech Stack
- Docker
- Nmap
- Python

## How It Works
1. Run a vulnerable application locally
2. Scan the target using Nmap
3. Save scan results to a file
4. Process results with a Python script
5. Generate a security report

## Example Findings
- Open port 8080 detected
- HTTP service identified
- Apache web server detected (version 2.4.25)
- Risk level classified as Medium

## How to Run

```bash
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa
nmap -sV localhost -p 8080 -oN scans/nmap_scan.txt
python3 scripts/generate_report.py
