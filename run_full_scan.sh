#!/bin/bash

echo "Starting full security scan..."

echo ""
echo "1. Starting DVWA..."
docker start dvwa >/dev/null 2>&1 || docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa

echo ""
echo "2. Running Nmap scan..."
mkdir -p scans
nmap -sV localhost -p 8080 -oN scans/nmap_scan.txt

echo ""
echo "3. Running ZAP scan..."
docker run -v "$(pwd):/zap/wrk" -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t http://host.docker.internal:8080 \
  -r zap_report.html

echo ""
echo "4. Moving ZAP results..."
mkdir -p reports
mv -f zap_report.html reports/ 2>/dev/null
mv -f zap.yaml reports/ 2>/dev/null

echo ""
echo "5. Generating report..."
python3 scripts/generate_report.py

echo ""
echo "Done ✅"
echo "Opening reports..."

open reports/final_report.md
open reports/zap_report.html
