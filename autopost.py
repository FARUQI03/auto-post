#!/usr/bin/env python3
"""
Auto post ke Instagram & Threads guna API rasmi Meta.

Cara kerja:
  1. Baca content/posts.json (senarai post + masa siar).
  2. Untuk setiap post yang dah sampai masa dan belum disiarkan,
     siarkan ke platform yang dipilih (instagram / threads).
  3. Rekod hasil dalam state/posted.json supaya tak post dua kali.

Tiada library luar diperlukan (Python 3.9+ sahaja).

Environment variables (letak dalam GitHub Secrets):
  IG_USER_ID          ID akaun Instagram Business/Creator
  IG_ACCESS_TOKEN     Long-lived token (Facebook Graph API)
  THREADS_USER_ID     ID akaun Threads
  THREADS_ACCESS_TOKEN  Long-lived token Threads API
  IMAGE_BASE_URL      (pilihan) URL awam untuk folder content/images,
                      cth https://raw.githubusercontent.com/<user>/<repo>/main/content/images

Guna:
  python autopost.py            # siar post yang dah sampai masa
  python autopost.py --dry-run  # tengok apa yang akan disiar, tanpa post
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS_FILE = ROOT / "content" / "posts.json"
STATE_FILE = ROOT / "state" / "posted.json"

GRAPH_VERSION = os.getenv("GRAPH_VERSION", "v23.0")
# graph.facebook.com (Facebook Login) atau graph.instagram.com (Instagram Login)
IG_API_HOST = os.getenv("IG_API_HOST", "graph.facebook.com")
FB_GRAPH = f"https://{IG_API_HOST}/{GRAPH_VERSION}"
THREADS_GRAPH = "https://graph.threads.net/v1.0"

THREADS_MAX_CHARS = 500
IG_MAX_CHARS = 2200


# ---------------------------------------------------------------- HTTP utils
def http(method, url, params=None):
    data = None
    if params:
        encoded = urllib.parse.urlencode(params)
        if method == "GET":
            url = f"{url}?{encoded}"
        else:
            data = encoded.encode()
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} {url.split('?')[0]}: {body}") from None


def wait_until_ready(base, container_id, token, label, tries=20, delay=6):
    """Tunggu media container siap diproses sebelum publish."""
    for _ in range(tries):
        info = http("GET", f"{base}/{container_id}",
                    {"fields": "status,status_code" if base == FB_GRAPH else "status,error_message",
                     "access_token": token})
        status = info.get("status_code") or info.get("status")
        if status in ("FINISHED", "PUBLISHED"):
            return
        if status in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"{label}: container gagal diproses: {info}")
        time.sleep(delay)
    raise RuntimeError(f"{label}: container tak siap selepas {tries * delay}s")


# ---------------------------------------------------------------- Instagram
def post_instagram(post):
    user_id = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]
    images = post_images(post)
    caption = build_caption(post, "instagram")[:IG_MAX_CHARS]

    if not images:
        raise RuntimeError("Instagram wajib ada sekurang-kurangnya 1 gambar (image).")

    if len(images) == 1:
        c = http("POST", f"{FB_GRAPH}/{user_id}/media",
                 {"image_url": images[0], "caption": caption, "access_token": token})
        creation_id = c["id"]
    else:  # carousel (2-10 gambar)
        children = []
        for url in images[:10]:
            c = http("POST", f"{FB_GRAPH}/{user_id}/media",
                     {"image_url": url, "is_carousel_item": "true", "access_token": token})
            wait_until_ready(FB_GRAPH, c["id"], token, "IG carousel item")
            children.append(c["id"])
        c = http("POST", f"{FB_GRAPH}/{user_id}/media",
                 {"media_type": "CAROUSEL", "children": ",".join(children),
                  "caption": caption, "access_token": token})
        creation_id = c["id"]

    wait_until_ready(FB_GRAPH, creation_id, token, "Instagram")
    res = http("POST", f"{FB_GRAPH}/{user_id}/media_publish",
               {"creation_id": creation_id, "access_token": token})
    return res["id"]


# ---------------------------------------------------------------- Threads
def post_threads(post):
    user_id = os.environ["THREADS_USER_ID"]
    token = os.environ["THREADS_ACCESS_TOKEN"]
    images = post_images(post)
    text = build_caption(post, "threads")
    if len(text) > THREADS_MAX_CHARS:
        raise RuntimeError(f"Teks Threads {len(text)} aksara, had {THREADS_MAX_CHARS}.")

    if not images:
        c = http("POST", f"{THREADS_GRAPH}/{user_id}/threads",
                 {"media_type": "TEXT", "text": text, "access_token": token})
    elif len(images) == 1:
        c = http("POST", f"{THREADS_GRAPH}/{user_id}/threads",
                 {"media_type": "IMAGE", "image_url": images[0], "text": text,
                  "access_token": token})
    else:
        children = []
        for url in images[:20]:
            ch = http("POST", f"{THREADS_GRAPH}/{user_id}/threads",
                      {"media_type": "IMAGE", "image_url": url, "is_carousel_item": "true",
                       "access_token": token})
            children.append(ch["id"])
        time.sleep(10)
        c = http("POST", f"{THREADS_GRAPH}/{user_id}/threads",
                 {"media_type": "CAROUSEL", "children": ",".join(children), "text": text,
                  "access_token": token})

    creation_id = c["id"]
    time.sleep(10 if images else 2)  # Meta cadang tunggu sebelum publish
    try:
        wait_until_ready(THREADS_GRAPH, creation_id, token, "Threads")
    except RuntimeError:
        pass  # sesetengah akaun tak pulangkan status; cuba publish terus
    res = http("POST", f"{THREADS_GRAPH}/{user_id}/threads_publish",
               {"creation_id": creation_id, "access_token": token})
    return res["id"]


# ---------------------------------------------------------------- Helpers
def post_images(post):
    base = os.getenv("IMAGE_BASE_URL", "").rstrip("/")
    out = []
    for img in post.get("images", []):
        if img.startswith("http://") or img.startswith("https://"):
            out.append(img)
        elif base:
            out.append(f"{base}/{urllib.parse.quote(img)}")
        else:
            raise RuntimeError(f"Gambar '{img}' bukan URL dan IMAGE_BASE_URL tak diset.")
    return out


def build_caption(post, platform):
    """Caption khas platform jika ada, kalau tak guna caption umum + hashtag."""
    text = post.get(f"caption_{platform}") or post.get("caption", "")
    tags = post.get(f"hashtags_{platform}", post.get("hashtags", []))
    if platform == "threads":
        tags = tags[:1]  # Threads hanya sokong 1 topic tag per post
    if tags:
        text = text.rstrip() + "\n\n" + " ".join(f"#{t.lstrip('#')}" for t in tags)
    return text


def parse_time(s):
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        raise ValueError(f"publish_at '{s}' mesti ada zon masa, cth 2026-12-01T09:00:00+08:00")
    return dt


def load_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


PUBLISHERS = {"instagram": post_instagram, "threads": post_threads}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="siar post id ini sahaja (abaikan masa)")
    args = ap.parse_args()

    posts = load_json(POSTS_FILE, [])
    state = load_json(STATE_FILE, {})
    now = datetime.now(timezone.utc)
    failures = 0

    for post in posts:
        pid = post["id"]
        if args.only and pid != args.only:
            continue
        if not args.only and parse_time(post["publish_at"]) > now:
            continue
        for platform in post.get("platforms", ["instagram", "threads"]):
            key = f"{pid}:{platform}"
            if state.get(key, {}).get("media_id"):
                continue
            label = f"[{pid} -> {platform}]"
            if args.dry_run:
                print(f"{label} AKAN DISIAR:\n{build_caption(post, platform)}\n"
                      f"gambar: {post.get('images', [])}\n")
                continue
            try:
                media_id = PUBLISHERS[platform](post)
                state[key] = {"media_id": media_id,
                              "posted_at": datetime.now(timezone.utc).isoformat()}
                print(f"{label} BERJAYA, media id {media_id}")
            except Exception as e:  # noqa: BLE001
                failures += 1
                state[key] = {"error": str(e)[:500],
                              "last_try": datetime.now(timezone.utc).isoformat()}
                print(f"{label} GAGAL: {e}", file=sys.stderr)
            STATE_FILE.parent.mkdir(exist_ok=True)
            STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False),
                                  encoding="utf-8")

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
