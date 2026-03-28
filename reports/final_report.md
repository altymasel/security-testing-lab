# Security Testing Report

## Target
http://localhost:8080

## Purpose
This report summarizes the results of Nmap service discovery and confirms whether an OWASP ZAP report is available.

## Raw Scan Output
# Nmap 7.98 scan initiated Wed Mar 25 13:55:19 2026 as: nmap -sV -p 8080 -oN scans/nmap_scan.txt localhost
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000037s latency).
Other addresses for localhost (not scanned): ::1

PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache httpd 2.4.25 ((Debian))

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Mar 25 13:55:26 2026 -- 1 IP address (1 host up) scanned in 6.30 seconds


## Findings
- Port 8080 is open and accessible on localhost.
- An HTTP service was detected on the target.
- Apache web server was identified.
- Apache web server version 2.4.25 was detected.
- Older Apache versions may contain known vulnerabilities if not patched.

## Risk Level
Medium

## ZAP Scan
ZAP scan report available: reports/zap_report.html

## Interpretation
The scan confirms that port 8080 is open and serving an HTTP application using Apache. This indicates an exposed service that may be vulnerable depending on configuration and version. The ZAP section shows whether a web vulnerability report is also available.

## Recommendations
- Review Apache version for known vulnerabilities
- Limit exposed services
- Review the OWASP ZAP HTML report for web security issues
- Add deeper web vulnerability analysis in the next phase
