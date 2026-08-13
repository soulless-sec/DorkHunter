# -*- coding: utf-8 -*-
"""
DorkHunter Dynamic Dork Database Loader Module
"""

import os

def get_dorks_dir() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "Dorks"),
        os.path.join(os.getcwd(), "DorkHunter", "Dorks"),
        os.path.join(os.getcwd(), "Dorks")
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return candidates[0]

def load_dorks_from_dir() -> dict[str, list[str]]:
    dorks_dir = get_dorks_dir()
    dorks_db: dict[str, list[str]] = {}
    if not os.path.exists(dorks_dir):
        return dorks_db
    
    for fname in os.listdir(dorks_dir):
        if fname.endswith(".txt"):
            cat = fname[:-4]
            fpath = os.path.join(dorks_dir, fname)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                lines = [ln.strip() for ln in fh if ln.strip() and not ln.strip().startswith("#")]
                if lines:
                    dorks_db[cat] = lines
    return dorks_db

def build_target(domain: str | None, tld: str | None) -> str:
    if domain:
        return f"site:{domain}"
    if tld:
        clean_tld = tld.strip()
        if not clean_tld.startswith("."):
            clean_tld = "." + clean_tld
        return f"site:{clean_tld}"
    return ""

def build_query(dork: str, target: str) -> str:
    return f"{dork} {target}".strip() if target else dork
