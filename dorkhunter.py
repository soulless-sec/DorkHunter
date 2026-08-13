#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    DorkHunter — Advanced Dork Scanner                    ║
║              Made by soulless | Multi-Engine & Shodan Harvester           ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import argparse, sys, json, csv, os, warnings, signal
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings("ignore")

def sigint_handler(sig, frame):
    print("\n\033[33m[!] Interrupted by user (Ctrl+C). Exiting cleanly...\033[0m")
    os._exit(0)

signal.signal(signal.SIGINT, sigint_handler)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CATEGORY_INFO
from loader import load_dorks_from_dir, build_target, build_query
from filters import filter_url, check_url, make_session
from engines import search_all_engines
from shodan_module import search_shodan

try:
    from colorama import Fore, Style, init as _cinit
    _cinit(autoreset=True)
    R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW
    C=Fore.CYAN; M=Fore.MAGENTA; W=Fore.WHITE
    BLD=Style.BRIGHT; RST=Style.RESET_ALL
except ImportError:
    R=G=Y=C=M=W=BLD=RST=""

BANNER = f"""{M}
██████╗  ██████╗ ██████╗ ██╗  ██╗    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
██║  ██║██║   ██║██████╔╝█████╔╝     ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██║  ██║██║   ██║██╔══██╗██╔═██╗     ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝██║  ██║██║  ██╗    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{RST}{C}         Multi-Engine Automated Dork Scanner | Made by soulless{RST}
"""

results: list[dict] = []

def save_output(data: list[dict], path: str, fmt: str) -> None:
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    if fmt == "json":
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    elif fmt == "csv":
        with open(path, "w", newline="", encoding="utf-8") as fh:
            fieldnames = ["url", "status", "redirects", "dork", "vuln"]
            writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(data)
    else:
        with open(path, "w", encoding="utf-8") as fh:
            for r in data:
                fh.write(r["url"] + "\n")
    print(f"\n{G}[+] {len(data)} direct URLs saved -> {path}{RST}")

def print_clean_table(dorks_db: dict[str, list[str]]) -> None:
    print(f"\n{C}{'='*74}")
    print(f"  {'Category':<28} {'Standard':<14} {'Description'}")
    print(f"{'-'*74}{RST}")
    total_dorks = 0
    for cat, dlist in sorted(dorks_db.items()):
        std, desc = CATEGORY_INFO.get(cat, ("Custom", "Custom Dork Category"))
        count = len(dlist)
        total_dorks += count
        print(f"  {G}{cat:<28}{RST} {Y}{std:<14}{RST} {desc:<35} {C}({count} dorks){RST}")
    print(f"{C}{'='*74}")
    print(f"  Total: {len(dorks_db)} categories, {total_dorks} dorks{RST}\n")

def parse_args() -> argparse.Namespace:
    dorks_db = load_dorks_from_dir()
    available_categories = sorted(dorks_db.keys()) + ["all"]
    
    p = argparse.ArgumentParser(
        prog="dorkhunter",
        description="DorkHunter — Multi-Engine Automated Dork Scanner (Made by soulless)"
    )
    p.add_argument("--domain", "-d", metavar="DOMAIN", help="Target domain (e.g. example.com)")
    p.add_argument("--tld", "-t", metavar="TLD", help="Strict TLD filter (e.g. .gov.pk, .in, .edu)")
    p.add_argument("--country", "-c", metavar="CODE", help="Country code for Shodan IP queries (e.g. PK, US, IN)")
    p.add_argument("--shodan-key", "-k", metavar="KEY", help="Shodan API key for raw IP device harvesting")
    p.add_argument("--vuln", "-v", nargs="+", default=["sqli"], help=f"Vuln categories to scan: {', '.join(available_categories[:10])}... or 'all'")
    p.add_argument("--all-web-vuln", "-W", action="store_true", help="Scan ALL OWASP Web Top 10 vulnerability categories")
    p.add_argument("--all-api-vuln", "-A", action="store_true", help="Scan ALL OWASP API Top 10 vulnerability categories")
    p.add_argument("--engine", "-e", nargs="+", choices=["google", "bing", "duckduckgo", "yahoo", "shodan", "all"], default=["google"], help="Engines to search (default: google, use 'shodan' for raw IP hardware)")
    p.add_argument("--pages", "-p", type=int, default=3, help="Pages per engine (default: 3)")
    p.add_argument("--delay", "-D", type=float, default=1.5, help="Delay between requests (default: 1.5s)")
    p.add_argument("--threads", "-T", type=int, default=10, help="Threads for checking (default: 10)")
    p.add_argument("--timeout", "-O", type=int, default=5, help="Timeout in seconds (default: 5s)")
    p.add_argument("--proxy", "-P", metavar="URL", help="Proxy URL or 'tor'")
    p.add_argument("--params-only", "-m", action="store_true", help="Only return URLs containing parameters (?id=...)")
    p.add_argument("--no-check", "-N", action="store_true", help="Skip HTTP verification and output raw discovered URLs")
    p.add_argument("--200-only", "-Z", dest="ok_only", action="store_true", help="Only save HTTP 200 OK URLs")
    p.add_argument("--output", "-o", metavar="FILE", help="Output file path")
    p.add_argument("--format", "-f", choices=["txt", "json", "csv"], default="txt", help="Output format (default: txt)")
    p.add_argument("--verbose", "-V", action="store_true", help="Show verbose output during scanning")
    p.add_argument("--list-vulns", "--list-vuln", "-L", action="store_true", help="List all loaded dork categories and exit")
    return p.parse_args()

def main() -> None:
    dorks_db = load_dorks_from_dir()
    args = parse_args()

    if args.list_vulns:
        print_clean_table(dorks_db)
        sys.exit(0)

    print(BANNER)

    shodan_key = args.shodan_key or os.environ.get("SHODAN_API_KEY")

    if not args.domain and not args.tld and not ("shodan" in args.engine or args.country):
        print(f"{R}[!] Please specify a target using --domain, --tld, or --shodan-key with --country{RST}")
        sys.exit(1)

    target_cats = []
    if args.all_web_vuln:
        target_cats = [c for c in sorted(dorks_db.keys()) if c.startswith("owasp_web_")]
    elif args.all_api_vuln:
        target_cats = [c for c in sorted(dorks_db.keys()) if c.startswith("owasp_api_")]
    elif "all" in args.vuln:
        target_cats = list(dorks_db.keys())
    else:
        target_cats = [c for c in args.vuln if c in dorks_db]

    if not target_cats:
        print(f"{R}[!] No valid vulnerability categories selected.{RST}")
        sys.exit(1)

    selected_engines = args.engine
    if "all" in selected_engines:
        engines = ["google", "bing", "duckduckgo", "yahoo"]
    else:
        engines = selected_engines

    proxy = args.proxy
    session = make_session(proxy, args.timeout)
    target_clause = build_target(args.domain, args.tld)

    raw_urls: set[str] = set()

    # Special Shodan Raw IP Harvester Path
    if "shodan" in engines or shodan_key:
        print(f"{Y}[*] Phase 1: Harvesting raw IP device endpoints via Shodan API...{RST}\n")
        country_filter = f" country:{args.country}" if args.country else ""
        for cat in target_cats:
            for dork in dorks_db[cat]:
                clean_dork = dork.replace('inurl:', '').replace('intitle:', '')
                query = f"{clean_dork}{country_filter}"
                print(f"  {C}[Shodan]{RST} Querying -> {query}")
                ip_urls = search_shodan(query, shodan_key)
                if ip_urls:
                    print(f"           {G}-> Found {len(ip_urls)} raw IP endpoints{RST}")
                    raw_urls.update(ip_urls)

    # Standard Search Engines Path
    search_engines = [e for e in engines if e != "shodan"]
    if search_engines and (args.domain or args.tld):
        active_dorks = []
        for cat in target_cats:
            for dork in dorks_db[cat]:
                active_dorks.append((cat, build_query(dork, target_clause)))

        print(f"{C}{'='*70}")
        print(f"  {BLD}Target Clause :{RST} {args.domain or args.tld}")
        print(f"  {BLD}Categories    :{RST} {', '.join(target_cats)}")
        print(f"  {BLD}Engines       :{RST} {', '.join(search_engines)}")
        print(f"  {BLD}Total Dorks   :{RST} {len(active_dorks)}")
        print(f"{C}{'='*70}{RST}\n")

        print(f"{Y}[*] Harvesting URLs across search engines...{RST}\n")

        for idx, (cat, q) in enumerate(active_dorks, 1):
            print(f"  {C}[{idx}/{len(active_dorks)}]{RST} Scanning [{cat}] -> {q[:60]}")
            harvested = search_all_engines(q, search_engines, session, pages=args.pages, delay=args.delay)
            before = len(raw_urls)
            for u in harvested:
                if filter_url(u, params_only=args.params_only, tld=args.tld, domain=args.domain):
                    raw_urls.add(u)
            added = len(raw_urls) - before
            if added > 0:
                print(f"           {G}-> Found {len(harvested)} raw, +{added} unique target URLs{RST}")

    print(f"\n{G}[+] Total Unique Verified Target URLs: {len(raw_urls)}{RST}")

    if not raw_urls:
        print(f"{R}[!] No matching URLs found for the target specs.{RST}")
        sys.exit(0)

    if args.no_check:
        for u in raw_urls:
            results.append({"url": u, "status": None, "redirects": None, "dork": "", "vuln": "harvested"})
    else:
        print(f"\n{Y}[*] Phase 2: Verifying HTTP status code ({args.threads} threads)...{RST}\n")
        with ThreadPoolExecutor(max_workers=args.threads) as pool:
            future_map = {pool.submit(check_url, u, proxy, args.timeout, True): u for u in raw_urls}
            for fut in as_completed(future_map):
                code, u, redir = fut.result()
                if args.ok_only and code != 200:
                    continue
                if code:
                    print(f"  {G}[{code}]{RST} {u}")
                    results.append({"url": u, "status": code, "redirects": redir, "dork": "", "vuln": "harvested"})

    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = args.output or f"dorkhunter_results_{timestamp}.{args.format}"
        save_output(results, out_path, args.format)

if __name__ == "__main__":
    main()
