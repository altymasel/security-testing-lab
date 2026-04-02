# Security Testing Report

## Target
http://localhost:8080

## Findings (Nmap)
- Port 8080 is open.
- HTTP service detected.
- Apache server detected.
- Apache version 2.4.25 detected.

## Risk Level
Medium

## ZAP Scan
Status: Available

## ZAP Findings
- Cookies missing HttpOnly flag.
- Missing Content Security Policy header.
- Missing X-Content-Type-Options header.
- Server version information exposed.
- Missing clickjacking protection.

## Summary
The system exposes an HTTP service on port 8080. ZAP analysis shows several security weaknesses such as missing headers and insecure cookie settings.

## Recommendations
- Review server configuration
- Add security headers
- Secure cookies
- Investigate ZAP findings
