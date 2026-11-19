#!/usr/bin/env python3
"""Renderer for the news-image-20261119 entry.

Draws three 1024x1024 variants (A: tile grid, B: newspaper front page,
C: big lead + numbered list, the layout that won the 17 and 18 Nov
editions) with Pillow, using only the Liberation Sans fonts bundled in
build/fonts/ and icons drawn with code. Deterministic: no randomness,
no clock, no network.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "variants")
W = H = 1024

DATE_LINE = "THURSDAY 19 NOVEMBER 2026"
FOOTER = "Compiled from multiple news sources - see SOURCES.md"

LEAD = {
    "kicker": "DIPLOMACY - ASIA-PACIFIC",
    "color": (37, 99, 178),
    "headline": "TRUMP, XI AND PUTIN HOLD FIRST-EVER THREE-WAY SUMMIT IN SHENZHEN",
    "body": ("The US, Chinese and Russian leaders meet on the sidelines of the "
             "APEC summit in Shenzhen. Nuclear arms, the wars in Ukraine and "
             "Iran, trade and AI top the agenda."),
    "icon": "summit",
}

STORIES = [
    {
        "kicker": "JUSTICE - THE HAGUE",
        "color": (148, 96, 196),
        "headline": "WORLD COURT DELIVERS JUDGMENT IN MYANMAR GENOCIDE CASE",
        "body": ("The ICJ gives its final, binding ruling in Gambia's case over "
                 "the 2017 Rohingya campaign - seven years on, with over "
                 "700,000 Rohingya fled to Bangladesh."),
        "icon": "scales",
    },
    {
        "kicker": "CONFLICT - EUROPE",
        "color": (198, 48, 49),
        "headline": "CRIMEAN BRIDGE HIT FOR THIRD TIME THIS WEEK - TRAFFIC HALTED",
        "body": ("A nighttime drone attack suspends road and rail traffic "
                 "overnight into Thursday. Russia says no one was injured; "
                 "the damage is still being assessed."),
        "icon": "bridge",
    },
    {
        "kicker": "POLITICS - SOUTH ASIA",
        "color": (214, 116, 22),
        "headline": "BANGLADESH SHUTS DOWN IN LOCKDOWN - YUNUS FAMILY HOME SET ABLAZE",
        "body": ("Hasina's Awami League calls the nationwide lockdown ahead of "
                 "her planned December return. Police say two ruling-party "
                 "members were killed."),
        "icon": "flame",
    },
    {
        "kicker": "ECONOMY - TECHNOLOGY",
        "color": (22, 138, 90),
        "headline": "ANTHROPIC RAISES A RECORD $81.3 BILLION IN THE LARGEST IPO EVER",
        "body": ("Priced at $83 a share and valued at about $1.5 trillion, the "
                 "Claude maker starts trading on Nasdaq on Thursday, beating "
                 "SpaceX's $75 billion debut."),
        "icon": "chart",
    },
    {
        "kicker": "WEATHER - SOUTH ASIA",
        "color": (14, 128, 150),
        "headline": "CYCLONE AKVAN: OVER 80,000 EVACUATED ON INDIA'S EAST COAST",
        "body": ("Odisha moves people to shelters as the severe storm nears. "
                 "Landfall is expected Friday noon between Narsapur and Puri, "
                 "with winds of 90-100 km/h."),
        "icon": "cyclone",
    },
]

SHORT_BODIES = [
    "Gambia's case over the 2017 Rohingya campaign: the final ruling, seven years on.",
    "Night drone attack halts road and rail traffic; Russia: no injuries, damage assessed.",
    "Nationwide lockdown by Hasina's party; police say two ruling-party members killed.",
    "Priced at $83, the Claude maker debuts on Nasdaq Thursday, beating SpaceX's $75bn.",
    "Odisha shelters evacuees; landfall expected Friday noon, Narsapur-Puri, 90-100 km/h.",
]


def font(size, bold=False):
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.18, bold=False):
    """Draw wrapped text; returns the y just below the block."""
    x, y = xy
    step = int(fnt.size * leading)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def fit_lines(draw, text, size, max_w, max_lines, bold=True, min_size=20):
    """Shrink a headline font until the wrap fits max_lines; returns (font, lines)."""
    size_now = size
    while size_now > min_size:
        fnt = font(size_now, bold=bold)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size_now -= 2
    fnt = font(min_size, bold=bold)
    return fnt, wrap(draw, text, fnt, max_w)


# ---------------------------------------------------------------- icons
def icon_summit(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 56, cy - 56, cx + 56, cy + 56], outline=col, width=6)
    d.ellipse([cx - 56, cy - 20, cx + 56, cy + 20], outline=col, width=3)
    d.line([cx - 56, cy, cx + 56, cy], fill=col, width=3)
    d.arc([cx - 28, cy - 56, cx + 28, cy + 56], 90, 270, fill=col, width=3)
    d.arc([cx - 28, cy - 56, cx + 28, cy + 56], 270, 90, fill=col, width=3)
    for px, py in [(cx - 34, cy - 30), (cx + 30, cy - 8), (cx, cy + 34)]:
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col)


def icon_scales(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    top = cy - 52
    d.line([cx, top, cx, cy + 44], fill=col, width=6)
    d.line([cx - 52, top + 8, cx + 52, top + 8], fill=col, width=6)
    d.ellipse([cx - 8, top - 10, cx + 8, top + 6], fill=col)
    for sx in (cx - 52, cx + 52):
        d.line([sx, top + 8, sx - 16, top + 44], fill=col, width=4)
        d.line([sx, top + 8, sx + 16, top + 44], fill=col, width=4)
        d.arc([sx - 24, top + 30, sx + 24, top + 58], 0, 180, fill=col, width=5)
    d.line([cx - 30, cy + 52, cx + 30, cy + 52], fill=col, width=6)


def icon_bridge(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    deck = cy - 6
    # pylons
    for tx in (cx - 46, cx + 46):
        d.line([tx, deck - 52, tx, deck + 26], fill=col, width=6)
    # deck with a gap in the middle (the halted crossing)
    d.line([x0 + 8, deck, cx - 18, deck], fill=col, width=7)
    d.line([cx + 18, deck, x1 - 8, deck], fill=col, width=7)
    # cables
    for tx in (cx - 46, cx + 46):
        for dx in (-34, -18, 18, 34):
            px = tx + dx
            if abs(px - cx) > 20:
                d.line([tx, deck - 52, px, deck], fill=col, width=3)
    # waves below
    for r in range(2):
        yy = deck + 38 + r * 16
        for sx in range(x0 + 10, x1 - 32, 48):
            d.arc([sx, yy - 8, sx + 30, yy + 8], 180, 360, fill=col, width=4)


def icon_flame(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # house outline
    d.line([cx - 54, cy + 2, cx, cy - 46, cx + 54, cy + 2], fill=col, width=6)
    d.line([cx - 42, cy - 4, cx - 42, cy + 54], fill=col, width=6)
    d.line([cx + 42, cy - 4, cx + 42, cy + 54], fill=col, width=6)
    d.line([cx - 42, cy + 54, cx + 42, cy + 54], fill=col, width=6)
    # flame inside the house
    fx, fy = cx, cy + 30
    pts = [(fx, fy - 34), (fx + 14, fy - 8), (fx + 18, fy + 8),
           (fx + 10, fy + 24), (fx - 10, fy + 24), (fx - 18, fy + 8),
           (fx - 12, fy - 10)]
    d.polygon(pts, fill=col)


def icon_chart(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    left, base = cx - 54, cy + 52
    d.line([left, cy - 52, left, base], fill=col, width=5)
    d.line([left, base, cx + 56, base], fill=col, width=5)
    # bars
    for i, h in enumerate((22, 36, 50)):
        bx = left + 14 + i * 26
        d.rectangle([bx, base - h, bx + 16, base], outline=col, width=4)
    # rising arrow line
    pts = [(left + 8, base - 18), (left + 44, base - 44), (left + 72, base - 58),
           (left + 102, base - 88)]
    d.line(pts, fill=col, width=6)
    ax, ay = pts[-1]
    d.polygon([(ax, ay), (ax - 18, ay + 2), (ax - 2, ay + 16)], fill=col)


def icon_cyclone(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for k in range(3):
        start = k * 120
        d.arc([cx - 56, cy - 56, cx + 56, cy + 56], start, start + 95, fill=col, width=7)
        d.arc([cx - 34, cy - 34, cx + 34, cy + 34], start + 60, start + 170, fill=col, width=6)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=col, width=5)


ICONS = {
    "summit": icon_summit,
    "scales": icon_scales,
    "bridge": icon_bridge,
    "flame": icon_flame,
    "chart": icon_chart,
    "cyclone": icon_cyclone,
}


def draw_icon(d, name, box, col):
    ICONS[name](d, box, col)


def icon_tile(name, col, size):
    """Render an icon on its own tile and scale it to `size` px square.

    The icon routines are drawn for a ~112 px box; scaling a rendered
    tile keeps them correct at the small sizes used in the list rows.
    """
    tile = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    ICONS[name](td, (24, 24, 136, 136), col)
    return tile.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- variant A
def variant_a():
    """Tile grid: lead tile, 2x2 supporting tiles, wide fifth tile."""
    img = Image.new("RGB", (W, H), (16, 22, 34))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 92], fill=(232, 236, 240))
    d.text((36, 14), "WORLD NEWS", font=font(44, True), fill=(16, 22, 34))
    tw = d.textlength(DATE_LINE, font=font(30, True))
    d.text((W - 36 - tw, 24), DATE_LINE, font=font(30, True), fill=(198, 48, 49))
    # lead tile
    d.rounded_rectangle([28, 108, 996, 428], 14, fill=(28, 38, 54))
    d.rectangle([28, 108, 42, 428], fill=LEAD["color"])
    d.text((66, 124), LEAD["kicker"], font=font(24, True), fill=(150, 190, 240))
    hf, hlines = fit_lines(d, LEAD["headline"], 50, 690, 3)
    y = 158
    for ln in hlines:
        d.text((66, y), ln, font=hf, fill=(245, 247, 250))
        y += int(hf.size * 1.12)
    text_block(d, (66, y + 6), LEAD["body"], font(22), (205, 214, 226), 680, leading=1.16)
    draw_icon(d, LEAD["icon"], (748, 176, 958, 340), (240, 180, 90))
    # 2x2 tiles
    tiles = [(28, 444, 502, 664), (522, 444, 996, 664),
             (28, 680, 502, 900), (522, 680, 996, 900)]
    for story, (tx0, ty0, tx1, ty1) in zip(STORIES[:4], tiles):
        d.rounded_rectangle([tx0, ty0, tx1, ty1], 12, fill=(28, 38, 54))
        d.rectangle([tx0, ty0, tx1, ty0 + 8], fill=story["color"])
        d.text((tx0 + 22, ty0 + 18), story["kicker"], font=font(20, True), fill=(170, 200, 240))
        hf, hlines = fit_lines(d, story["headline"], 30, tx1 - tx0 - 44, 2, min_size=19)
        y = ty0 + 48
        for ln in hlines:
            d.text((tx0 + 22, y), ln, font=hf, fill=(245, 247, 250))
            y += int(hf.size * 1.12)
        text_block(d, (tx0 + 22, y + 4), story["body"], font(20), (205, 214, 226),
                   tx1 - tx0 - 44, leading=1.12)
    # fifth story, wide bottom tile
    s5 = STORIES[4]
    d.rounded_rectangle([28, 916, 996, 982], 12, fill=(28, 38, 54))
    d.rectangle([28, 916, 40, 982], fill=s5["color"])
    hf5, hlines5 = fit_lines(d, s5["kicker"] + "  -  " + s5["headline"], 22, 910, 1, min_size=15)
    d.text((62, 928), hlines5[0], font=hf5, fill=(245, 247, 250))
    d.text((62, 954), "Odisha shelters evacuees; landfall expected Friday noon, Narsapur-Puri, at 90-100 km/h.",
           font=font(20), fill=(205, 214, 226))
    d.text((36, 990), FOOTER, font=font(18), fill=(140, 152, 168))
    return img


# ---------------------------------------------------------------- variant C
def variant_c():
    """Big lead plus a numbered list of the five supporting stories.

    The winning layout of the 17 and 18 Nov editions: dark canvas, gold
    banner, one big lead headline with an explanatory sentence, then a
    numbered, category-labelled list with code-drawn icons and a source
    footnote.
    """
    img = Image.new("RGB", (W, H), (15, 20, 32))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 96], fill=(255, 209, 102))
    d.text((36, 16), "WORLD NEWS", font=font(44, True), fill=(16, 16, 20))
    tw = d.textlength(DATE_LINE, font=font(30, True))
    d.text((W - 36 - tw, 32), DATE_LINE, font=font(30, True), fill=(16, 16, 20))
    # lead
    d.text((36, 110), LEAD["kicker"], font=font(24, True), fill=(150, 190, 240))
    hf, hlines = fit_lines(d, LEAD["headline"], 50, 952, 3)
    y = 142
    for ln in hlines:
        d.text((36, y), ln, font=hf, fill=(248, 249, 251))
        y += int(hf.size * 1.1)
    yb = text_block(d, (36, y + 6), LEAD["body"], font(22), (208, 216, 228), 800, leading=1.14)
    tile = icon_tile(LEAD["icon"], (240, 180, 90), 88)
    img.paste(tile, (892, y - 8), tile)
    y = yb + 2
    d.line([36, y + 10, 988, y + 10], fill=(255, 209, 102), width=3)
    # numbered list
    yy = y + 24
    for i, story in enumerate(STORIES, start=1):
        d.ellipse([36, yy + 2, 92, yy + 58], fill=story["color"])
        num = str(i)
        nw = d.textlength(num, font=font(34, True))
        d.text((64 - nw / 2, yy + 10), num, font=font(34, True), fill=(255, 255, 255))
        d.text((112, yy), story["kicker"], font=font(20, True), fill=(170, 200, 240))
        hf, hlines = fit_lines(d, story["headline"], 30, 790, 2, min_size=25)
        hy = yy + 24
        for ln in hlines:
            d.text((112, hy), ln, font=hf, fill=(248, 249, 251))
            hy += int(hf.size * 1.04)
        by = text_block(d, (112, hy + 1), SHORT_BODIES[i - 1], font(20),
                        (208, 216, 228), 790, leading=1.08)
        tile = icon_tile(story["icon"], story["color"], 62)
        img.paste(tile, (918, yy + 12), tile)
        yy = by + 5
        if i < len(STORIES):
            d.line([112, yy - 5, 988, yy - 5], fill=(46, 58, 78), width=2)
    assert yy <= 984, "variant C list overflows: ends at %d" % yy
    d.text((36, 988), FOOTER, font=font(18), fill=(140, 152, 168))
    return img


# ---------------------------------------------------------------- variant B
def variant_b():
    """Newspaper front page: masthead, lead, two compact columns, weather strip."""
    img = Image.new("RGB", (W, H), (246, 242, 233))
    d = ImageDraw.Draw(img)
    ink = (24, 24, 28)
    grey = (92, 92, 98)
    d.text((36, 18), "THE WORLD TODAY", font=font(56, True), fill=ink)
    d.line([36, 94, 988, 94], fill=ink, width=5)
    tw = d.textlength(DATE_LINE, font=font(30, True))
    d.text(((W - tw) / 2, 106), DATE_LINE, font=font(30, True), fill=(168, 32, 36))
    d.line([36, 150, 988, 150], fill=ink, width=2)
    # lead
    d.text((36, 164), LEAD["kicker"], font=font(22, True), fill=LEAD["color"])
    hf, hlines = fit_lines(d, LEAD["headline"], 50, 952, 3)
    y = 194
    for ln in hlines:
        d.text((36, y), ln, font=hf, fill=ink)
        y += int(hf.size * 1.08)
    yb = text_block(d, (36, y + 4), LEAD["body"], font(22), (52, 52, 58), 740, leading=1.14)
    draw_icon(d, LEAD["icon"], (800, yb - 134, 962, yb - 2), LEAD["color"])
    y = yb + 10
    d.line([36, y, 988, y], fill=ink, width=3)
    # two columns, two stories each, short bodies
    top = y + 20
    col_x = [36, 522]
    col_w = 450
    col_y = {0: top, 1: top}
    for idx, story in enumerate(STORIES[:4]):
        c = idx % 2
        x, yy = col_x[c], col_y[c]
        d.text((x, yy), story["kicker"], font=font(19, True), fill=story["color"])
        hf, hlines = fit_lines(d, story["headline"], 27, col_w, 3, min_size=22)
        yy += 25
        for ln in hlines:
            d.text((x, yy), ln, font=hf, fill=ink)
            yy += int(hf.size * 1.06)
        yy = text_block(d, (x, yy + 3), SHORT_BODIES[idx], font(19), (52, 52, 58),
                        col_w, leading=1.12)
        col_y[c] = yy + 14
    y = max(col_y.values()) + 0
    d.line([36, y, 988, y], fill=ink, width=2)
    # fifth story as a wide strip
    s5 = STORIES[4]
    d.text((36, y + 10), s5["kicker"], font=font(19, True), fill=s5["color"])
    d.text((36, y + 36), s5["headline"], font=font(27, True), fill=ink)
    d.text((36, y + 70), "Odisha moves people to shelters as the severe storm nears. Landfall is expected Friday noon",
           font=font(19), fill=(52, 52, 58))
    d.text((36, y + 94), "between Narsapur and Puri, with winds of 90-100 km/h.", font=font(19), fill=(52, 52, 58))
    assert y + 118 <= 966, "variant B strip overflows: ends at %d" % (y + 118)
    d.line([36, 968, 988, 968], fill=ink, width=2)
    d.text((36, 978), FOOTER, font=font(18), fill=grey)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [("A", variant_a), ("B", variant_b), ("C", variant_c)]
    for name, fn in jobs:
        img = fn()
        path = os.path.join(OUT, "variant_%s.png" % name)
        img.save(path, optimize=True)
        small = img.resize((512, 512), Image.LANCZOS)
        small.save(os.path.join(OUT, "variant_%s_512.png" % name), optimize=True)
        print(name, os.path.getsize(path))


if __name__ == "__main__":
    main()
