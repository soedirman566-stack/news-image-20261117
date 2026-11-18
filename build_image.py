#!/usr/bin/env python3
"""Compose the news-image-20261117 entry: one 1024x1024 front page that
sums up the world news of Tuesday 17 November 2026.

Layout (top to bottom):
  * masthead  - "THE WORLD IN ONE PICTURE" + gold rule + dateline
  * hero      - Kerch Bridge photo, "CRIMEA BRIDGE DOWN"
  * mid row   - Hormuz tanker | Vulcan rocket, side by side
  * bottom    - Manila arrival photo (left) + Nvidia / JPMorgan text column

The result is written next to this script as entry.png.  The bytes are
JPEG (the competition detects the format by magic bytes); the quality is
stepped down until the file fits the 1 MiB limit.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "entry.png"

W = H = 1024
MAX_BYTES = 1_048_576

BG = (13, 13, 17)
INK = (242, 237, 228)
MUTE = (178, 172, 158)
GOLD = (201, 162, 39)
BAR = (10, 10, 13)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PHOTOS = {
    "bridge": ASSETS / "media-generation-hero-bridge-0-1cc5c0e0-53eb-40cb-84a5-4d7c1e2f2546.png",
    "tanker": ASSETS / "media-generation-panel-tanker-0-49e6a9a7-4906-466b-be24-a08c6412860a.png",
    "rocket": ASSETS / "media-generation-panel-rocket-0-5e200c5a-ad4f-4821-8424-f25cac6bec4a.png",
    "manila": ASSETS / "media-generation-panel-manila-0-f8f8744b-80b0-451b-8afa-7a7db6a7b21c.png",
}


def font(path, size):
    return ImageFont.truetype(path, size)


def cover(img, w, h, focus_y=0.5):
    """Resize + crop `img` so it exactly covers a w x h box."""
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = round((nh - h) * focus_y)
    return img.crop((x, y, x + w, y + h))


def text_w(draw, s, fnt):
    return draw.textbbox((0, 0), s, font=fnt)[2]


def spaced(draw, xy, s, fnt, fill, tracking=6):
    """Draw text with extra letter tracking; returns the end x."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += text_w(draw, ch, fnt) + tracking
    return x - tracking


def spaced_width(draw, s, fnt, tracking=6):
    return sum(text_w(draw, ch, fnt) for ch in s) + tracking * (len(s) - 1)


def wrap(draw, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def headline_block(page, draw, x, y, w, headline, subline, h_size=32, s_size=19):
    """Serif headline with a wrapped sans subline under it; returns end y."""
    hf = font(SERIF, h_size)
    draw.text((x, y), headline, font=hf, fill=INK)
    y += h_size + 10
    sf = font(SANS, s_size)
    for line in wrap(draw, subline, sf, w):
        draw.text((x, y), line, font=sf, fill=MUTE)
        y += s_size + 6
    return y


def build():
    page = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(page)
    margin = 28
    inner = W - 2 * margin

    # ---- masthead ------------------------------------------------------
    title = "THE WORLD IN ONE PICTURE"
    tf = font(SERIF, 50)
    tw = spaced_width(draw, title, tf, tracking=2)
    spaced(draw, ((W - tw) // 2, 22), title, tf, INK, tracking=2)
    draw.rectangle([margin, 92, W - margin, 95], fill=GOLD)
    date = "TUESDAY · 17 NOVEMBER 2026"
    df = font(SANS_B, 20)
    dw = spaced_width(draw, date, df, tracking=5)
    spaced(draw, ((W - dw) // 2, 106), date, df, GOLD, tracking=5)

    # ---- hero: Kerch Bridge --------------------------------------------
    hero_y, hero_h = 142, 276
    page.paste(cover(Image.open(PHOTOS["bridge"]).convert("RGB"), inner, hero_h), (margin, hero_y))
    y = headline_block(
        page, draw, margin, hero_y + hero_h + 12, inner,
        "CRIMEA BRIDGE DOWN",
        "Ukraine's strike collapses the Kerch span — Russia answers on Kyiv's bridges",
        h_size=44, s_size=20,
    )

    # ---- middle row: Hormuz | Vulcan ------------------------------------
    mid_y = y + 14
    gap = 16
    pw = (inner - gap) // 2
    ph = 196
    page.paste(cover(Image.open(PHOTOS["tanker"]).convert("RGB"), pw, ph, focus_y=0.45), (margin, mid_y))
    page.paste(cover(Image.open(PHOTOS["rocket"]).convert("RGB"), pw, ph, focus_y=0.4), (margin + pw + gap, mid_y))
    ty = mid_y + ph + 10
    left_end = headline_block(page, draw, margin, ty, pw,
                              "HORMUZ ABLAZE",
                              "Tankers struck as a third U.S. carrier arrives")
    right_end = headline_block(page, draw, margin + pw + gap, ty, pw,
                               "VULCAN FAILS",
                               "40 Amazon satellites lost in launch failure")
    y = max(left_end, right_end)

    # ---- bottom row: Manila photo + text column -------------------------
    bot_y = y + 16
    bot_h = H - 20 - bot_y
    mw = round(inner * 0.55)
    manila = cover(Image.open(PHOTOS["manila"]).convert("RGB"), mw, bot_h, focus_y=0.75)
    page.paste(manila, (margin, bot_y))
    # caption bar overlaid on the photo's lower edge
    bar_h = 64
    overlay = Image.new("RGB", (mw, bar_h), BAR)
    page.paste(overlay, (margin, bot_y + bot_h - bar_h))
    draw = ImageDraw.Draw(page)
    draw.text((margin + 14, bot_y + bot_h - bar_h + 8), "TRUMP LANDS IN MANILA",
              font=font(SERIF, 25), fill=INK)
    draw.text((margin + 14, bot_y + bot_h - bar_h + 40), "ASEAN summit opens — Xi–Putin talks next",
              font=font(SANS, 16), fill=MUTE)

    # text column on the right
    cx = margin + mw + gap
    cw = W - margin - cx
    cy = bot_y + 2
    draw.text((cx, cy), "NVIDIA REPORTS", font=font(SERIF, 29), fill=INK)
    cy += 42
    for line in wrap(draw, "First earnings since Huang's exit", font(SANS, 19), cw):
        draw.text((cx, cy), line, font=font(SANS, 19), fill=MUTE)
        cy += 25
    cy += 12
    draw.rectangle([cx, cy, cx + cw, cy + 2], fill=GOLD)
    cy += 14
    draw.text((cx, cy), "JPMORGAN: IT WAS A BUG", font=font(SERIF, 25), fill=INK)
    cy += 38
    for line in wrap(draw, "Bank blames software, not hackers, for outage", font(SANS, 19), cw):
        draw.text((cx, cy), line, font=font(SANS, 19), fill=MUTE)
        cy += 25

    # ---- save as JPEG bytes under the entry.png name ---------------------
    quality = 88
    while True:
        page.save(OUT, format="JPEG", quality=quality, optimize=True)
        size = OUT.stat().st_size
        print(f"quality={quality} bytes={size}")
        if size <= MAX_BYTES or quality <= 60:
            break
        quality -= 4
    print(f"wrote {OUT} ({page.size[0]}x{page.size[1]}, {size} bytes)")


if __name__ == "__main__":
    build()
