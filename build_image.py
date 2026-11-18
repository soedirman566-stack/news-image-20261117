#!/usr/bin/env python3
"""Compose the entry image for make.fun's news-image-20261117 contest.

Builds a 1024x1024 newspaper-front-page style image summing up the world
news of Tuesday 17 November 2026, and writes it to ``entry.png`` next to
this script.  The composed picture is saved as JPEG bytes (quality tuned
to stay under the 1 MiB contest limit) inside the file named entry.png --
the contest detects the real format from the magic bytes, so JPEG
content under a .png name is explicitly allowed.

Layout (1024x1024, dark editorial):
  * masthead band: "THE WORLD IN ONE PICTURE" + the date
  * hero photo (Kerch Bridge) with a headline bar
  * second photo panel (Strait of Hormuz tanker) with a headline bar
  * bottom strip with three one-line headlines

Run it with:  python3 build_image.py
"""

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "entry.png"

HERO_SRC = ASSETS / "media-generation-hero-bridge-0-1cc5c0e0-53eb-40cb-84a5-4d7c1e2f2546.png"
PANEL_SRC = ASSETS / "media-generation-panel-tanker-0-49e6a9a7-4906-466b-be24-a08c6412860a.png"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")
SANS_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")

W = H = 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN
MAX_BYTES = 1_048_576

BG = (10, 12, 15)
PAPER = (242, 237, 227)
MUTED = (168, 175, 182)
GOLD = (201, 162, 39)
RULE = (74, 82, 90)
BAR = (8, 9, 11, 208)  # translucent black headline bar over photos


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def fit_font(draw, s, path, start_size, max_w, min_size=14):
    """Largest font size (<= start_size) that keeps ``s`` within max_w."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        if text_w(draw, s, fnt) <= max_w:
            return fnt
        size -= 2
    return font(path, min_size)


def centered(draw, cx, y, s, fnt, fill):
    draw.text((cx - text_w(draw, s, fnt) / 2, y), s, font=fnt, fill=fill)


def spaced_centered(draw, cx, y, s, fnt, fill, tracking=6):
    """Draw text centered with extra letter spacing (for the dateline)."""
    widths = [text_w(draw, ch, fnt) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, wch in zip(s, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += wch + tracking


def cover_crop(img, target_w, target_h, focus_y=0.5):
    """Crop ``img`` to the target aspect, keeping the band around focus_y
    (0 = top of the source, 1 = bottom), then resize to the target size."""
    sw, sh = img.size
    target_ratio = target_w / target_h
    crop_h = int(sw / target_ratio)
    if crop_h <= sh:
        crop_w = sw
        y0 = int((sh - crop_h) * focus_y)
        box = (0, y0, sw, y0 + crop_h)
    else:
        crop_w = int(sh * target_ratio)
        x0 = (sw - crop_w) // 2
        box = (x0, 0, x0 + crop_w, sh)
    return img.crop(box).resize((target_w, target_h), Image.LANCZOS)


def headline_bar(base, y_top, y_bot, headline, subline, head_size, sub_size):
    """Translucent dark bar with a serif headline and a sans subline."""
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([0, y_top, W, y_bot], fill=BAR)
    base.paste(Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(base)
    hf = fit_font(draw, headline, SERIF_BOLD, head_size, CONTENT_W)
    draw.text((MARGIN, y_top + 12), headline, font=hf, fill=PAPER)
    sf = fit_font(draw, subline, SANS, sub_size, CONTENT_W)
    sub_y = y_top + 12 + head_size + 10
    draw.text((MARGIN, sub_y), subline, font=sf, fill=MUTED)
    return draw


def main():
    page = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(page)

    # ---- masthead ------------------------------------------------------
    mast = fit_font(draw, "THE WORLD IN ONE PICTURE", SERIF_BOLD, 56, CONTENT_W)
    centered(draw, W // 2, 26, "THE WORLD IN ONE PICTURE", mast, PAPER)
    draw.line([MARGIN, 104, W - MARGIN, 104], fill=GOLD, width=3)
    draw.line([MARGIN, 110, W - MARGIN, 110], fill=RULE, width=1)
    date_f = font(SANS_BOLD, 20)
    spaced_centered(draw, W // 2, 120, "TUESDAY · 17 NOVEMBER 2026", date_f, MUTED, tracking=5)

    # ---- hero: the Kerch Bridge ---------------------------------------
    # The headline block sits under the photo so the collapsed span and
    # the wreckage in the water stay fully visible.
    hero_y, hero_h = 148, 344
    hero = cover_crop(Image.open(HERO_SRC).convert("RGB"), CONTENT_W, hero_h, focus_y=0.6)
    page.paste(hero, (MARGIN, hero_y))
    draw = ImageDraw.Draw(page)
    headline = "CRIMEA BRIDGE DOWN"
    hf = fit_font(draw, headline, SERIF_BOLD, 48, CONTENT_W)
    draw.text((MARGIN, hero_y + hero_h + 12), headline, font=hf, fill=PAPER)
    subline = "Ukraine's strike collapses the Kerch span — Russia answers on Kyiv's bridges"
    sf = fit_font(draw, subline, SANS, 21, CONTENT_W)
    draw.text((MARGIN, hero_y + hero_h + 72), subline, font=sf, fill=MUTED)

    # ---- second panel: the Strait of Hormuz ----------------------------
    panel_y, panel_h = 602, 236
    panel = cover_crop(Image.open(PANEL_SRC).convert("RGB"), CONTENT_W, panel_h, focus_y=0.5)
    page.paste(panel, (MARGIN, panel_y))
    draw = headline_bar(
        page, panel_y + panel_h - 92, panel_y + panel_h,
        "HORMUZ ABLAZE",
        "Tankers struck in the strait as a third U.S. carrier reaches the Gulf",
        head_size=34, sub_size=19,
    )

    # ---- bottom strip: three more stories ------------------------------
    stories = [
        ("TRUMP LANDS IN MANILA", "Asia tour heads to Xi–Putin talks"),
        ("VULCAN ROCKET FAILS", "40 Amazon satellites lost"),
        ("NVIDIA REPORTS", "first earnings since Huang's exit"),
    ]
    y = 856
    for i, (head, rest) in enumerate(stories):
        if i:
            draw.line([MARGIN, y - 8, W - MARGIN, y - 8], fill=RULE, width=1)
        hf = font(SERIF_BOLD, 25)
        draw.text((MARGIN, y), head, font=hf, fill=GOLD)
        x = MARGIN + text_w(draw, head, hf)
        rf = fit_font(draw, "  —  " + rest, SANS, 22, CONTENT_W - (x - MARGIN))
        draw.text((x, y + 2), "  —  " + rest, font=rf, fill=PAPER)
        y += 46

    # ---- footer: the day's sixth story, as a small print line ----------
    draw.line([MARGIN, 984, W - MARGIN, 984], fill=RULE, width=1)
    foot = "PLUS — JPMorgan blames a software bug, not hackers, for its banking outage"
    ff = fit_font(draw, foot, SANS, 16, CONTENT_W)
    centered(draw, W // 2, 994, foot, ff, MUTED)

    # ---- save as JPEG bytes under the entry.png name -------------------
    quality = 88
    while True:
        buf = BytesIO()
        page.save(buf, format="JPEG", quality=quality, optimize=True)
        data = buf.getvalue()
        if len(data) <= MAX_BYTES - 65_536 or quality <= 60:
            break
        quality -= 4
    OUT.write_bytes(data)
    print(f"wrote {OUT} : {page.size[0]}x{page.size[1]}, {len(data)} bytes, JPEG quality {quality}")


if __name__ == "__main__":
    main()
