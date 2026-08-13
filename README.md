<div align="center">

```
  ██████╗  ██████╗ ██████╗ ██╗  ██╗    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
  ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
  ██║  ██║██║   ██║██████╔╝█████╔╝     ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
  ██║  ██║██║   ██║██╔══██╗██╔═██╗     ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
  ██████╔╝╚██████╔╝██║  ██║██║  ██╗    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

### **DorkHunter — Multi-Engine Automated Dork Scanner & Hardware Harvester**
*High-Performance Reconnaissance & Device Discovery Suite*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular-FF6F00?style=for-the-badge&logo=diagramsdotnet&logoColor=white)](#-repository-structure)
[![OWASP](https://img.shields.io/badge/OWASP-Mapped-00599C?style=for-the-badge&logo=owasp&logoColor=white)](#-vulnerability-categories)
[![Author](https://img.shields.io/badge/Author-soulless-red?style=for-the-badge&logo=github&logoColor=white)](https://github.com/soulless-sec)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

</div>

## 📌 Executive Summary

**DorkHunter** is a modular, multi-engine intelligence harvesting framework built for penetration testers, red teams, and security researchers. It automates query generation, multi-threaded search engine scraping, domain/TLD enforcement, parameter URL isolation, and raw IP hardware endpoint harvesting using Shodan.

Designed around decoupled plain-text category stores, **DorkHunter** allows security teams to organize, maintain, and execute over **1,300+ security dorks** mapped directly to **OWASP Top 10** and **CWE** standards.

---

## 🔥 Key Capabilities

- ⚡ **Multi-Engine Target Discovery**: Simultaneously queries Google, Bing, DuckDuckGo, and Yahoo to aggregate search results across multiple engines.

- 🎯 **Direct Vulnerability Endpoint Extraction**: Automatically isolates vulnerable URL structures containing parameters (`?id=`, `?page=`, `?cat=`) for SQL Injection, Local File Inclusion (LFI), and Cross-Site Scripting (XSS) auditing.

- 🌐 **Strict Scope & TLD Filtering**: Enforces strict target domain and country TLD matching (`.gov.pk`, `.edu`, `.in`) to ensure all collected endpoints remain within your target scope.

- 📡 **Standalone Surveillance & IP Hardware Harvesting**: Integrates directly with Shodan API to discover raw IP:port camera portals, NVRs, DVRs, and exposed IoT interfaces.

- 🔍 **OWASP & Vulnerability Mapping**: Scans for 43+ specialized security categories covering OWASP Top 10 Web, OWASP API Top 10, Cloud Buckets, Database Exposures, and Admin Login Panels.

- 🚀 **Live Endpoint Verification**: Conducts high-speed parallel HTTP status checks to verify active `200 OK` endpoints and identify live targets.

---

## 📁 Repository Structure

```text
DorkHunter/
├── Dorks/                # Decoupled Dork database files (sqli.txt, lfi.txt, cameras.txt, etc.)
├── README.md             # Comprehensive project documentation
├── __init__.py           # Package initialization & exports
├── config.py             # User-Agents, engine domain sets & OWASP category mappings
├── dorkhunter.py         # Main CLI application entry point
├── engines.py            # Parallel multi-engine harvesting engine (Google, Bing, DDG, Yahoo)
├── filters.py            # Strict TLD matching, parameter filtering & HTTP status check
├── loader.py             # Dynamic dork file scanner & query builder
├── requirements.txt      # Project dependencies
└── shodan_module.py      # Shodan API raw IP device harvester module
```

---

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/soulless-sec/DorkHunter.git
cd DorkHunter
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

---

## 🕹️ CLI Flag Reference

| Flag | Long Option | Category | Description | Example |
| :---: | :--- | :---: | :--- | :--- |
| `-d` | `--domain` | Target | Specify exact target domain | `-d target.com` |
| `-t` | `--tld` | Target | Strict TLD filter | `-t .gov.pk` |
| `-v` | `--vuln` | Category | Target specific dork category / categories | `-v sqli lfi xss` |
| `-W` | `--all-web-vuln` | Category | Select ALL OWASP Web Top 10 categories | `-W` |
| `-A` | `--all-api-vuln` | Category | Select ALL OWASP API Top 10 categories | `-A` |
| `-e` | `--engine` | Engine | Select engines (`google`, `bing`, `duckduckgo`, `yahoo`, `shodan`, `all`) | `-e all` |
| `-m` | `--params-only` | Filter | Extract parameterized URLs only (`?id=`) | `-m` |
| `-k` | `--shodan-key` | Shodan | Shodan API key for raw IP discovery | `-k YOUR_KEY` |
| `-c` | `--country` | Shodan | Country code filter for Shodan queries | `-c PK` |
| `-Z` | `--200-only` | Filter | Save only HTTP 200 OK responses | `-Z` |
| `-V` | `--verbose` | Output | Enable verbose scanning output | `-V` |
| `-N` | `--no-check` | Workflow | Skip HTTP status checking (output raw URLs) | `-N` |
| `-T` | `--threads` | Performance | HTTP verification threads (Default: 10) | `-T 20` |
| `-D` | `--delay` | Performance | Request delay in seconds (Default: 1.5) | `-D 2.0` |
| `-P` | `--proxy` | Network | Proxy URL or `tor` | `-P tor` |
| `-o` | `--output` | Export | Custom output file path | `-o results.txt` |
| `-f` | `--format` | Export | Output format (`txt`, `json`, `csv`) | `-f json` |
| `-L` | `--list-vuln` | Help | List all loaded vulnerability categories | `-L` |

---

## 🎯 Usage Examples

### 1. View All Categories & Dork Counts
```bash
python3 dorkhunter.py -L
```

### 2. Multi-Engine Parameterized Scanning on Target TLD
```bash
python3 dorkhunter.py -t .gov.pk -v sqli -e all -m -Z -V
```

### 3. Full OWASP Web Top 10 Audit on Target Domain
```bash
python3 dorkhunter.py -d example.com -W -e google yahoo -T 20 -o web_audit.json -f json
```

### 4. Raw IP Camera & NVR Device Discovery via Shodan
```bash
python3 dorkhunter.py -e shodan -v cameras -c PK -k YOUR_SHODAN_API_KEY
```

---

## 📊 Mapped Categories (43 Total)

<details>
<summary><b>Click to expand full category mapping table</b></summary>

<br>

| Category Name | Standard Reference | Description |
| :--- | :--- | :--- |
| `sqli` | OWASP A03 | SQL Injection Endpoints |
| `lfi` | OWASP A03 | Local File Inclusion |
| `xss` | OWASP A03 | Cross-Site Scripting |
| `rfi` | OWASP A03 | Remote File Inclusion |
| `ssrf` | OWASP A10 | Server-Side Request Forgery |
| `cmdi` | OWASP A03 | Command Injection |
| `xxe` | OWASP A03 | XML External Entity |
| `ssti` | OWASP A03 | Server-Side Template Injection |
| `idor` | OWASP A01 | Insecure Direct Object Reference |
| `path_traversal` | OWASP A01 | Path Traversal |
| `file_upload` | OWASP A04 | Insecure File Upload |
| `deserialization` | OWASP A08 | Insecure Deserialization |
| `exposed` | OWASP A05 | Exposed Sensitive Files |
| `login` | OWASP A07 | Administrative Login Panels |
| `auth_failures` | OWASP A07 | Authentication Failures |
| `crypto_failures` | OWASP A02 | Cryptographic Failures |
| `security_misconfig` | OWASP A05 | Security Misconfigurations |
| `database_exposed` | OWASP A05 | Exposed Databases & Admin Tools |
| `backup_databases` | OWASP A05 | Exposed SQL / Dump Backup Files |
| `env_files` | OWASP A05 | Environment Credentials (`.env`) |
| `phpinfo` | OWASP A05 | Exposed `phpinfo()` Diagnostics |
| `actuator_endpoints` | OWASP A05 | Spring Boot Actuator Exposure |
| `info_disclosure` | OWASP A09 | Information Disclosure & Logs |
| `api` | OWASP API | API Endpoint Discovery |
| `graphql` | API | GraphQL Introspection & Playgrounds |
| `jwt` | OWASP A07 | JWT Key & Secret Exposure |
| `cors` | CWE-942 | CORS Misconfigurations |
| `oauth_tokens` | OWASP A07 | OAuth Secrets & Token Exposure |
| `cloud` | OWASP A05 | Cloud / Infrastructure Exposure |
| `cloud_buckets` | Cloud | AWS S3 / Azure Blob / GCP Buckets |
| `docker_registry` | DevOps | Exposed Docker Registry Catalog |
| `git_exposure` | DevOps | Exposed Git Repositories (`.git`) |
| `subdomains` | Recon | Subdomain Enumeration |
| `subdomain_takeover` | Recon | Subdomain Takeover Dangling Records |
| `cms` | OWASP A06 | CMS Vulnerabilities |
| `wp_plugins` | CMS | Vulnerable WordPress Plugins |
| `cameras` | IoT | IP Cameras & NVR/DVR Login Interfaces |
| `iot` | IoT | Routers, Printers & IoT Devices |
| `sensitive_docs` | PII | Sensitive Financial & PII Documents |
| `business_logic` | OWASP A04 | Business Logic Endpoints |
| `mass_assignment` | OWASP A01 | Mass Assignment Parameters |

</details>

---

## 📜 License & Author

Created and maintained by **[soulless](https://github.com/soulless-sec)** under the **MIT License**.
