# -*- coding: utf-8 -*-
"""
DorkHunter Search Engine Harvester Module
Supports Google, Bing, DuckDuckGo, Yahoo in parallel.
"""

import time, random, sys, os, warnings
from urllib.parse import urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import urllib3

warnings.filterwarnings("ignore")
urllib3.disable_warnings()

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

try:
    from ddgs import DDGS
    HAS_DDGS = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        HAS_DDGS = True
    except ImportError:
        HAS_DDGS = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import USER_AGENTS, SEARCH_ENGINE_DOMAINS

def search_ddg(query: str, max_results: int = 30) -> list[str]:
    if not HAS_DDGS:
        return []
    urls: list[str] = []
    try:
        with DDGS() as ddgs:
            res = ddgs.text(query, max_results=max_results)
            if res:
                for r in res:
                    href = r.get("href", "")
                    if href and href.startswith("http"):
                        urls.append(href)
    except Exception:
        pass
    return urls

def search_bing(query: str, session: requests.Session, max_pages: int = 3, delay: float = 1.5) -> list[str]:
    urls: list[str] = []
    if not HAS_BS4:
        return urls
    for page in range(max_pages):
        try:
            params = {"q": query, "first": page * 10 + 1, "count": 10}
            session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
            resp = session.get("https://www.bing.com/search", params=params, timeout=8, verify=False)
            soup = BeautifulSoup(resp.text, "html.parser")
            anchors = (
                soup.select("li.b_algo h2 a") or
                soup.select("li.b_algo .b_title a") or
                soup.select("li.b_algo a[href^='http']")
            )
            for a in anchors:
                href = a.get("href", "")
                if href.startswith("http") and "bing.com/ck/a" not in href:
                    urls.append(href)
            time.sleep(delay)
        except Exception:
            break
    return urls

def search_google(query: str, session: requests.Session, max_pages: int = 2, delay: float = 2.0) -> list[str]:
    urls: list[str] = []
    if not HAS_BS4:
        return urls
    for page in range(max_pages):
        try:
            params = {"q": query, "start": page * 10, "num": 10, "hl": "en"}
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            resp = session.get("https://www.google.com/search", params=params, headers=headers, timeout=10, verify=False)
            if "CAPTCHA" in resp.text or "unusual traffic" in resp.text.lower():
                break
            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/url?q=" in href:
                    try:
                        href = href.split("/url?q=")[1].split("&")[0]
                        href = unquote(href)
                    except IndexError:
                        continue
                if href.startswith("http"):
                    parsed = urlparse(href)
                    if not any(d in parsed.netloc for d in SEARCH_ENGINE_DOMAINS):
                        urls.append(href)
            time.sleep(delay)
        except Exception:
            break
    return urls

def search_yahoo(query: str, session: requests.Session, max_pages: int = 3, delay: float = 1.5) -> list[str]:
    urls: list[str] = []
    if not HAS_BS4:
        return urls
    for page in range(max_pages):
        try:
            b_offset = page * 10 + 1
            params = {"p": query, "b": b_offset}
            session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
            resp = session.get("https://search.yahoo.com/search", params=params, timeout=8, verify=False)
            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.select("div.compTitle a, h3.title a"):
                href = a.get("href", "")
                if "/RU=" in href:
                    try:
                        href = unquote(href.split("/RU=")[1].split("/RK=")[0])
                    except Exception:
                        pass
                if href.startswith("http"):
                    parsed = urlparse(href)
                    if not any(d in parsed.netloc for d in SEARCH_ENGINE_DOMAINS):
                        urls.append(href)
            time.sleep(delay)
        except Exception:
            break
    return urls

def search_all_engines(query: str, engines: list[str], session: requests.Session, pages: int = 3, delay: float = 1.5) -> list[str]:
    combined_urls = set()
    with ThreadPoolExecutor(max_workers=len(engines)) as exec_pool:
        futures = {}
        if "google" in engines:
            futures[exec_pool.submit(search_google, query, session, pages, delay)] = "google"
        if "bing" in engines:
            futures[exec_pool.submit(search_bing, query, session, pages, delay)] = "bing"
        if "duckduckgo" in engines:
            futures[exec_pool.submit(search_ddg, query, 30)] = "duckduckgo"
        if "yahoo" in engines:
            futures[exec_pool.submit(search_yahoo, query, session, pages, delay)] = "yahoo"

        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res:
                    combined_urls.update(res)
            except Exception:
                pass
    return list(combined_urls)
