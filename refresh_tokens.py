#!/usr/bin/env python3
"""
Panjangkan (refresh) long-lived token sebelum tamat 60 hari.
Jalankan sebulan sekali, kemudian salin token baru ke GitHub Secrets.

  IG_ACCESS_TOKEN=... FB_APP_ID=... FB_APP_SECRET=... \
  THREADS_ACCESS_TOKEN=... THREADS_VITALIQ_ACCESS_TOKEN=... python refresh_tokens.py
"""
import json
import os
import urllib.parse
import urllib.request

GRAPH_VERSION = os.getenv("GRAPH_VERSION", "v23.0")


def get(url, params):
    with urllib.request.urlopen(f"{url}?{urllib.parse.urlencode(params)}", timeout=60) as r:
        return json.loads(r.read().decode())


if os.getenv("IG_ACCESS_TOKEN") and os.getenv("FB_APP_ID") and os.getenv("FB_APP_SECRET"):
    r = get(f"https://graph.facebook.com/{GRAPH_VERSION}/oauth/access_token", {
        "grant_type": "fb_exchange_token",
        "client_id": os.environ["FB_APP_ID"],
        "client_secret": os.environ["FB_APP_SECRET"],
        "fb_exchange_token": os.environ["IG_ACCESS_TOKEN"],
    })
    print("IG_ACCESS_TOKEN baru:\n", r["access_token"], "\n")

for name in ("THREADS_ACCESS_TOKEN", "THREADS_VITALIQ_ACCESS_TOKEN"):
    if os.getenv(name):
        r = get("https://graph.threads.net/refresh_access_token", {
            "grant_type": "th_refresh_token",
            "access_token": os.environ[name],
        })
        print(f"{name} baru:\n", r["access_token"],
              f"\n(sah {r.get('expires_in', 0) // 86400} hari)\n")
