# -*- coding: utf-8 -*-
"""
DorkHunter Config & Constants Module
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
]

SEARCH_ENGINE_DOMAINS = frozenset([
    "google.com", "bing.com", "duckduckgo.com", "yahoo.com", "search.yahoo.com",
    "microsoft.com", "googleapis.com", "gstatic.com", "googleusercontent.com",
    "yimg.com", "yahoo.net"
])

CATEGORY_INFO = {
    "actuator_endpoints":     ("OWASP A05",  "Spring Boot Actuator Endpoints Exposure"),
    "api":                    ("OWASP API",  "API Endpoint Discovery"),
    "api_bola":               ("API Top 1",  "Broken Object Level Authorization"),
    "api_broken_auth":        ("API Top 2",  "Broken Authentication (API)"),
    "api_broken_func_auth":   ("API Top 5",  "Broken Function Level Authorization"),
    "api_inventory":          ("API Top 9",  "Improper Inventory Management"),
    "api_misconfig":          ("API Top 8",  "API Security Misconfiguration"),
    "api_ssrf":               ("API Top 7",  "SSRF in APIs"),
    "auth_failures":          ("OWASP A07",  "Authentication Failures"),
    "backup_databases":       ("OWASP A05",  "Exposed Database Backup Files"),
    "business_logic":         ("OWASP A04",  "Business Logic"),
    "cameras":                ("IoT",        "Exposed Cameras"),
    "cloud":                  ("OWASP A05",  "Cloud/Infrastructure Exposure"),
    "cloud_buckets":          ("Cloud",      "Exposed AWS S3 / Azure / GCP Buckets"),
    "cmdi":                   ("OWASP A03",  "Command Injection"),
    "cms":                    ("OWASP A06",  "CMS Vulnerabilities"),
    "cors":                   ("CWE-942",    "CORS Misconfiguration"),
    "crypto_failures":        ("OWASP A02",  "Cryptographic Failures"),
    "database_exposed":       ("OWASP A05",  "Exposed Databases"),
    "deserialization":        ("OWASP A08",  "Insecure Deserialization"),
    "docker_registry":        ("DevOps",     "Exposed Docker Registry / Catalog"),
    "env_files":              ("OWASP A05",  "Exposed Environment Credentials (.env)"),
    "exposed":                ("OWASP A05",  "Exposed Sensitive Files"),
    "file_upload":            ("OWASP A04",  "Insecure File Upload"),
    "git_exposure":           ("DevOps",     "Exposed Git Repositories (.git)"),
    "graphql":                ("API",        "GraphQL Exposure"),
    "idor":                   ("OWASP A01",  "Insecure Direct Object Reference"),
    "info_disclosure":        ("OWASP A09",  "Information Disclosure"),
    "iot":                    ("IoT",        "Routers, Printers & IoT Devices"),
    "jwt":                    ("OWASP A07",  "JWT Vulnerabilities"),
    "lfi":                    ("OWASP A03",  "Local File Inclusion"),
    "login":                  ("OWASP A07",  "Login / Admin Panels"),
    "mass_assignment":        ("OWASP A01",  "Mass Assignment"),
    "oauth_tokens":           ("OWASP A07",  "OAuth Secrets & Token Exposure"),
    "open_redirect":          ("CWE-601",    "Open Redirect"),
    "path_traversal":         ("OWASP A01",  "Path Traversal"),
    "phpinfo":                ("OWASP A05",  "Exposed PHPInfo Pages"),
    "rfi":                    ("OWASP A03",  "Remote File Inclusion"),
    "security_misconfig":     ("OWASP A05",  "Security Misconfiguration"),
    "sensitive_docs":         ("PII",        "Sensitive Documents & Data"),
    "sqli":                   ("OWASP A03",  "SQL Injection"),
    "ssrf":                   ("OWASP A10",  "Server-Side Request Forgery"),
    "ssti":                   ("OWASP A03",  "Server-Side Template Injection"),
    "subdomain_takeover":     ("Recon",      "Subdomain Takeover Dangling Records"),
    "subdomains":             ("Recon",      "Subdomain Enumeration"),
    "vulnerable_components":  ("OWASP A06",  "Vulnerable Components"),
    "wp_plugins":             ("CMS",        "Vulnerable WordPress Plugins"),
    "xss":                    ("OWASP A03",  "Cross-Site Scripting"),
    "xxe":                    ("OWASP A03",  "XML External Entity"),
}
