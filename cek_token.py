#!/usr/bin/env python3
"""Semak token Threads masih sah (tak post apa-apa). Cetak username setiap akaun."""
import json, os, sys, urllib.error, urllib.request

bad = 0
for name in ("THREADS_ACCESS_TOKEN", "THREADS_VITALIQ_ACCESS_TOKEN", "THREADS_FARZ_ACCESS_TOKEN"):
    tok = os.getenv(name, "").strip()
    if not tok:
        print(f"{name}: belum diset"); continue
    try:
        with urllib.request.urlopen(f"https://graph.threads.net/v1.0/me?fields=id,username&access_token={tok}", timeout=30) as r:
            d = json.loads(r.read().decode())
        print(f"{name}: OK -> @{d.get('username')} (id {d.get('id')})")
    except urllib.error.HTTPError as e:
        bad += 1
        print(f"{name}: GAGAL HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")
sys.exit(1 if bad else 0)
