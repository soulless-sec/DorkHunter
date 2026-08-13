# -*- coding: utf-8 -*-
"""
DorkHunter URL Filtering & Verification Module
"""

import sys, os, random, warnings
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

warnings.filterwarnings("ignore")
urllib3.disable_warnings()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import USER_AGENTS, SEARCH_ENGINE_DOMAINS

def make_session(proxy: str | None = None, timeout: int = 5) -> requests.Session:
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.8, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    })
    if proxy:
        if proxy.lower() == "tor":
            proxy = "socks5h://127.0.0.1:9050"
        s.proxies = {"http": proxy, "https": proxy}
    return s

def strict_tld_match(url: str, tld: str | None, domain: str | None) -> bool:
    parsed = urlparse(url)
    netloc = parsed.netloc.lower().split(":")[0]
    if domain:
        clean_dom = domain.lower().lstrip(".")
        return netloc == clean_dom or netloc.endswith("." + clean_dom)
    if tld:
        clean_tld = tld.lower()
        if not clean_tld.startswith("."):
            clean_tld = "." + clean_tld
        return netloc.endswith(clean_tld)
    return True

def filter_url(url: str, params_only: bool = False, tld: str | None = None, domain: str | None = None) -> bool:
    if not url or not url.startswith("http"):
        return False
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    
    if any(se in netloc for se in SEARCH_ENGINE_DOMAINS):
        return False
        
    if (tld or domain) and not strict_tld_match(url, tld, domain):
        return False
        
    if params_only and not parsed.query:
        return False
        
    return True

def check_url(url: str, proxy: str | None, timeout: int, verify_ssl: bool) -> tuple[int | None, str, int | None]:
    try:
        sess = make_session(proxy, timeout)
        resp = sess.get(url, timeout=timeout, verify=verify_ssl, allow_redirects=True, stream=True)
        code = resp.status_code
        redir = len(resp.history)
        resp.close()
        return code, url, redir
    except Exception:
        return None, url, None
