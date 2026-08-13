# -*- coding: utf-8 -*-
"""
DorkHunter Shodan / Censys Raw IP Harvester Module
Retrieves direct IP:port hardware login endpoints via Shodan API.
"""

import sys, os, requests

def search_shodan(query: str, api_key: str, limit: int = 50) -> list[str]:
    """
    Search Shodan API for raw IP:port device endpoints.
    """
    if not api_key:
        print("\033[31m[!] Shodan API key required (--shodan-key or SHODAN_API_KEY env var)\033[0m")
        return []

    url = "https://api.shodan.io/shodan/host/search"
    params = {
        "key": api_key,
        "query": query,
        "page": 1
    }
    
    urls = []
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            matches = data.get("matches", [])
            for m in matches:
                ip = m.get("ip_str")
                port = m.get("port")
                ssl = m.get("ssl", {})
                scheme = "https" if ssl or port in (443, 8443) else "http"
                if ip and port:
                    urls.append(f"{scheme}://{ip}:{port}")
        else:
            print(f"\033[31m[!] Shodan API Error [{resp.status_code}]: {resp.text[:100]}\033[0m")
    except Exception as e:
        print(f"\033[31m[!] Shodan Request Failed: {e}\033[0m")
        
    return urls
