#!/usr/bin/env python3
"""Jana gambar kad FARZ untuk content/farz/posts.json.

Setiap post yang ada medan "card" dan gambar belum wujud akan dijana ke
content/farz/images/<id>.jpg, dan "images" post diisi.

Guna:  python tools/farz_cards.py
Format card: {"kind": statement|list|quote|poll|steps|check|teaser,
              "kicker": "...", "title": "...", "items": [...], "sub": "..."}
Perlu font Inter di /usr/share/fonts/opentype/inter/.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "content/farz/posts.json"
IMG = ROOT / "content/farz/images"

F = "/usr/share/fonts/opentype/inter/"
def font(n, s): return ImageFont.truetype(F + n, s)
RED, BLACK, OFF, GREY = (227, 30, 36), (14, 14, 14), (244, 241, 236), (150, 150, 150)
W, H, M = 1080, 1350, 90

def logo(d, x, y, size, fill):
    d.text((x, y), "FARZ", font=font("InterDisplay-BlackItalic.otf", size), fill=fill)
    w = d.textlength("FARZ", font=font("InterDisplay-BlackItalic.otf", size))
    d.text((x + w + 4, y + 2), "®", font=font("Inter-Bold.otf", size // 3), fill=fill)

def wrap(d, text, f, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
    return lines

def card(c, out):
    dark = c["kind"] in ("teaser", "statement", "quote")
    bg, fg = (BLACK, OFF) if dark else (OFF, BLACK)
    if c["kind"] == "statement": bg, fg = RED, OFF
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    accent = OFF if c["kind"] == "statement" else RED
    # header
    d.rectangle([M, M, M + 70, M + 10], fill=accent)
    if c.get("kicker"):
        d.text((M, M + 34), c["kicker"], font=font("Inter-Bold.otf", 30), fill=accent if not dark or c["kind"]!="statement" else fg)
    # title
    big = c["kind"] in ("teaser", "statement")
    tsize = 128 if big else (72 if c["kind"] == "quote" else 76)
    tf = font("InterDisplay-BlackItalic.otf" if big else "InterDisplay-ExtraBold.otf", tsize)
    lines = wrap(d, c["title"], tf, W - 2 * M)
    lh = int(tsize * 1.12)
    y = (H - lh * len(lines)) // 2 - 80 if big or c["kind"] == "quote" else M + 140
    if c["kind"] == "quote":
        d.text((M - 6, y - 150), "“", font=font("InterDisplay-Black.otf", 220), fill=RED)
    for ln in lines:
        d.text((M, y), ln, font=tf, fill=fg); y += lh
    if c.get("sub"):
        d.text((M, y + 30), c["sub"], font=font("Inter-SemiBold.otf", 38), fill=fg if c["kind"]=="statement" else GREY)
    # items
    items = c.get("items", [])
    if items:
        y += 50
        f = font("Inter-SemiBold.otf", 44)
        for i, it in enumerate(items, 1):
            if c["kind"] == "poll":
                d.rounded_rectangle([M, y, W - M, y + 120], radius=60, outline=fg, width=4)
                d.text((M + 50, y + 34), it, font=font("Inter-Bold.otf", 48), fill=fg); y += 150; continue
            mark = {"list": f"{i:02d}", "steps": f"{i:02d}", "check": "✓"}[c["kind"]]
            d.text((M, y), mark, font=font("InterDisplay-BlackItalic.otf", 52), fill=RED)
            for j, ln in enumerate(wrap(d, it, f, W - 2 * M - 120)):
                d.text((M + 120, y + 4 + j * 56), ln, font=f, fill=fg)
            y += max(1, len(wrap(d, it, f, W - 2 * M - 120))) * 56 + 46
            if c["kind"] != "check" and i < len(items):
                d.line([M + 120, y - 24, W - M, y - 24], fill=(210, 205, 198) if not dark else (60, 60, 60), width=2)
    # footer
    logo(d, M, H - M - 70, 64, accent if c["kind"] != "statement" else OFF)
    ft = font("Inter-SemiBold.otf", 28)
    t = "@farzglobal"
    d.text((W - M - d.textlength(t, font=ft), H - M - 40), t, font=ft, fill=GREY if c["kind"]!="statement" else OFF)
    im.save(out, "JPEG", quality=90)

def main():
    posts = json.loads(POSTS.read_text(encoding="utf-8"))
    IMG.mkdir(parents=True, exist_ok=True)
    made = 0
    for p in posts:
        assert len(p["caption"]) <= 500, p["id"]
        if "card" in p:
            name = f"{p['id']}.jpg"
            if not (IMG / name).exists():
                card(p["card"], IMG / name); made += 1
            p["images"] = [name]
    POSTS.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(posts)} post, {made} gambar baru dijana")

if __name__ == "__main__":
    main()
