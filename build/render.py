"""Render the 19 November 2026 world-news summary as one 1024x1024 PNG.

Layout (variant C): a gold banner with the date, one big lead story with
a globe mark, then a numbered list of five supporting stories, each with
its own code-drawn pictogram, and a source footnote at the bottom.

Everything on the page is drawn with Pillow primitives and the bundled
Liberation Sans fonts. No network access, no timestamps, no randomness:
running this script twice produces the same bytes.

Usage:
    python3 build/render.py            # writes entry.png next to build/
    python3 build/render.py out.png    # writes to the given path
"""

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
MARGIN = 36

# Palette: deep navy page, warm gold banner, soft blue labels.
INK = (13, 18, 30)
GOLD = (233, 184, 92)
PAPER = (244, 246, 248)
MUTED = (198, 206, 218)
LABEL_BLUE = (143, 180, 232)
FAINT = (138, 151, 168)
RULE = (42, 54, 72)

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / "fonts"


def load_typeface(weight, size):
    """Load one bundled Liberation Sans face at the requested size."""
    name = "LiberationSans-Bold.ttf" if weight == "bold" else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(str(FONT_DIR / name), size)


def split_lines(text, font, max_width):
    """Greedy word wrap: returns the lines that fit inside max_width."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_paragraph(canvas, x, y, text, font, fill, max_width, leading):
    """Draw wrapped text starting at (x, y); return the y below the last line."""
    for line in split_lines(text, font, max_width):
        canvas.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_fitted_line(canvas, x, y, text, size, fill, max_width):
    """Draw one line, shrinking the type until it fits inside max_width."""
    while size > 14:
        font = load_typeface("regular", size)
        if font.getlength(text) <= max_width:
            break
        size -= 1
    else:
        font = load_typeface("regular", 14)
    canvas.text((x, y), text, font=font, fill=fill)
    return font


# ---------------------------------------------------------------------------
# Pictograms. Each one draws centred on (cx, cy) inside a square of side
# `span`, using only lines, arcs, ellipses and polygons.
# ---------------------------------------------------------------------------

def mark_globe(canvas, cx, cy, span, colour):
    r = span // 2
    w = 3
    canvas.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=w)
    canvas.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=colour, width=2)
    canvas.line([cx - r, cy, cx + r, cy], fill=colour, width=2)
    canvas.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=colour, width=2)
    canvas.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 20, 160, fill=colour, width=2)
    dot = r // 5
    canvas.ellipse([cx - dot, cy + r // 2 - dot, cx + dot, cy + r // 2 + dot], fill=colour)


def mark_scales(canvas, cx, cy, span, colour):
    half = span // 2
    top = cy - half
    base = cy + half
    canvas.line([cx, top, cx, base], fill=colour, width=3)
    canvas.line([cx - half, top + 6, cx + half, top + 6], fill=colour, width=3)
    for side in (-1, 1):
        px = cx + side * (half - 6)
        canvas.line([cx + side * (half - 2), top + 6, px, top + 22], fill=colour, width=2)
        canvas.line([cx + side * (half - 10), top + 6, px, top + 22], fill=colour, width=2)
        canvas.arc([px - 11, top + 16, px + 11, top + 38], 0, 180, fill=colour, width=2)
    canvas.line([cx - 12, base, cx + 12, base], fill=colour, width=3)
    canvas.ellipse([cx - 4, top - 5, cx + 4, top + 3], outline=colour, width=2)


def mark_bridge(canvas, cx, cy, span, colour):
    half = span // 2
    deck = cy - 2
    for side in (-1, 1):
        px = cx + side * (half - 8)
        canvas.line([px, cy - half + 6, px, deck], fill=colour, width=3)
        canvas.polygon([(px - 7, cy - half + 8), (px + 7, cy - half + 8), (px, cy - half - 2)], fill=colour)
    canvas.line([cx - half, deck, cx + half, deck], fill=colour, width=3)
    canvas.line([cx - half + 10, deck, cx, cy - half + 12], fill=colour, width=2)
    canvas.line([cx + half - 10, deck, cx, cy - half + 12], fill=colour, width=2)
    for k, yy in enumerate((cy + 12, cy + 22)):
        canvas.arc([cx - half, yy - 8, cx - 6, yy + 8], 180, 360, fill=colour, width=2)
        canvas.arc([cx + 6, yy - 8, cx + half, yy + 8], 180, 360, fill=colour, width=2)
        canvas.arc([cx - 14, yy - 8, cx + 14, yy + 8], 180, 360, fill=colour, width=2)


def mark_house_flame(canvas, cx, cy, span, colour):
    half = span // 2
    roof_y = cy - half + 4
    canvas.polygon([(cx - half, roof_y + 14), (cx, roof_y), (cx + half, roof_y + 14)], outline=colour, width=3)
    canvas.line([cx - half + 4, roof_y + 14, cx - half + 4, cy + half], fill=colour, width=3)
    canvas.line([cx + half - 4, roof_y + 14, cx + half - 4, cy + half], fill=colour, width=3)
    canvas.line([cx - half + 4, cy + half, cx + half - 4, cy + half], fill=colour, width=3)
    # A small flame inside the house: teardrop body with an inner flicker.
    canvas.pieslice([cx - 9, cy - 2, cx + 9, cy + 22], 0, 360, fill=colour)
    canvas.polygon([(cx - 9, cy + 8), (cx, cy - 14), (cx + 9, cy + 8)], fill=colour)
    canvas.pieslice([cx - 4, cy + 6, cx + 4, cy + 18], 0, 360, fill=INK)


def mark_chart(canvas, cx, cy, span, colour):
    half = span // 2
    base = cy + half
    canvas.line([cx - half, base, cx + half, base], fill=colour, width=3)
    canvas.line([cx - half, cy - half, cx - half, base], fill=colour, width=3)
    bars = [12, 20, 16, 28]
    step = (span - 14) // 4
    for i, height in enumerate(bars):
        x0 = cx - half + 8 + i * step
        canvas.rectangle([x0, base - height, x0 + step - 8, base - 3], fill=colour)
    canvas.line(
        [(cx - half + 6, base - 12), (cx - 6, base - 24), (cx + 8, base - 18), (cx + half - 2, base - 34)],
        fill=colour, width=3, joint="curve",
    )
    canvas.polygon(
        [(cx + half - 2, base - 34), (cx + half - 12, base - 32), (cx + half - 4, base - 24)],
        fill=colour,
    )


def mark_cyclone(canvas, cx, cy, span, colour):
    r = span // 2
    for k in range(3):
        inset = 4 + k * 7
        canvas.arc(
            [cx - r + inset, cy - r + inset, cx + r - inset, cy + r - inset],
            40 + k * 55, 300 + k * 55, fill=colour, width=3,
        )
    dot = 4
    canvas.ellipse([cx - dot, cy - dot, cx + dot, cy + dot], fill=colour)


MARKS = {
    "globe": mark_globe,
    "scales": mark_scales,
    "bridge": mark_bridge,
    "house_flame": mark_house_flame,
    "chart": mark_chart,
    "cyclone": mark_cyclone,
}


# ---------------------------------------------------------------------------
# Stories. Wording is taken verbatim from SOURCES.md: the lead claim plus
# the short list form for each supporting story.
# ---------------------------------------------------------------------------

LEAD = {
    "tag": "DIPLOMACY - ASIA-PACIFIC",
    "headline": "TRUMP, XI AND PUTIN HOLD FIRST-EVER THREE-WAY SUMMIT IN SHENZHEN",
    "deck": (
        "The US, Chinese and Russian leaders meet on the sidelines of the "
        "APEC summit in Shenzhen. Nuclear arms, the wars in Ukraine and "
        "Iran, trade and AI top the agenda."
    ),
}

ITEMS = [
    {
        "tint": (155, 89, 208),
        "tag": "JUSTICE - THE HAGUE",
        "headline": "WORLD COURT DELIVERS JUDGMENT IN MYANMAR GENOCIDE CASE",
        "summary": "Gambia's case over the 2017 Rohingya campaign: the final, binding ruling, seven years on.",
        "mark": "scales",
    },
    {
        "tint": (217, 79, 61),
        "tag": "CONFLICT - EUROPE",
        "headline": "CRIMEAN BRIDGE HIT FOR THIRD TIME THIS WEEK - TRAFFIC HALTED",
        "summary": "Night drone attack halts road and rail traffic; Russia says no injuries, damage assessed.",
        "mark": "bridge",
    },
    {
        "tint": (232, 134, 46),
        "tag": "POLITICS - SOUTH ASIA",
        "headline": "BANGLADESH SHUTS DOWN IN LOCKDOWN - YUNUS FAMILY HOME SET ABLAZE",
        "summary": "Hasina's party calls a nationwide lockdown; police say two ruling-party members were killed.",
        "mark": "house_flame",
    },
    {
        "tint": (47, 174, 107),
        "tag": "ECONOMY - TECHNOLOGY",
        "headline": "ANTHROPIC RAISES A RECORD $81.3 BILLION IN THE LARGEST IPO EVER",
        "summary": "Priced at $83, the Claude maker debuts on Nasdaq Thursday, beating SpaceX's $75 billion.",
        "mark": "chart",
    },
    {
        "tint": (31, 157, 176),
        "tag": "WEATHER - SOUTH ASIA",
        "headline": "CYCLONE AKVAN: OVER 80,000 EVACUATED ON INDIA'S EAST COAST",
        "summary": "Odisha shelters evacuees; landfall expected Friday noon, Narsapur–Puri, at 90–100 km/h.",
        "mark": "cyclone",
    },
]

FOOTNOTE = "Compiled from multiple news sources - see SOURCES.md"


def paint_banner(canvas):
    """Gold strip across the top: title left, full date right."""
    canvas.rectangle([0, 0, CANVAS, 96], fill=GOLD)
    title_font = load_typeface("bold", 46)
    date_font = load_typeface("bold", 25)
    canvas.text((MARGIN, 24), "WORLD NEWS", font=title_font, fill=INK)
    date = "THURSDAY 19 NOVEMBER 2026"
    canvas.text(
        (CANVAS - MARGIN - date_font.getlength(date), 33),
        date, font=date_font, fill=INK,
    )


def paint_lead(canvas):
    """The big lead story under the banner, globe mark on its right."""
    y = 112
    canvas.text((MARGIN, y), LEAD["tag"], font=load_typeface("bold", 22), fill=LABEL_BLUE)
    bottom = draw_paragraph(
        canvas, MARGIN, y + 28, LEAD["headline"],
        load_typeface("bold", 48), PAPER, CANVAS - 2 * MARGIN, 54,
    )
    deck_top = bottom + 8
    deck_bottom = draw_paragraph(
        canvas, MARGIN, deck_top, LEAD["deck"],
        load_typeface("regular", 20), MUTED, 810, 27,
    )
    mark_globe(canvas, 928, (deck_top + deck_bottom) // 2, 62, GOLD)
    return deck_bottom


def paint_list(canvas, top):
    """Five numbered rows: badge, tag, headline, one-line summary, mark."""
    row_height = 112
    text_left = 104
    text_width = 800
    for index, item in enumerate(ITEMS, start=1):
        row_top = top + (index - 1) * row_height
        if index > 1:
            canvas.line(
                [MARGIN, row_top, CANVAS - MARGIN, row_top], fill=RULE, width=1,
            )
        # Number badge.
        badge_top = row_top + 4
        canvas.ellipse(
            [MARGIN, badge_top, MARGIN + 52, badge_top + 52], fill=item["tint"],
        )
        digit = load_typeface("bold", 28)
        glyph = str(index)
        canvas.text(
            (MARGIN + 26 - digit.getlength(glyph) / 2, badge_top + 11),
            glyph, font=digit, fill=PAPER,
        )
        # Tag, headline (up to two lines) and summary.
        canvas.text(
            (text_left, row_top), item["tag"],
            font=load_typeface("bold", 19), fill=LABEL_BLUE,
        )
        headline_bottom = draw_paragraph(
            canvas, text_left, row_top + 22, item["headline"],
            load_typeface("bold", 29), PAPER, text_width, 32,
        )
        draw_fitted_line(
            canvas, text_left, headline_bottom + 2, item["summary"],
            18, MUTED, text_width,
        )
        MARKS[item["mark"]](canvas, 940, row_top + 52, 58, item["tint"])
    return top + len(ITEMS) * row_height


def build_image():
    """Compose the full page and return it as a Pillow image."""
    page = Image.new("RGB", (CANVAS, CANVAS), INK)
    canvas = ImageDraw.Draw(page)
    paint_banner(canvas)
    lead_bottom = paint_lead(canvas)
    divider_y = lead_bottom + 14
    canvas.line([MARGIN, divider_y, CANVAS - MARGIN, divider_y], fill=GOLD, width=2)
    list_bottom = paint_list(canvas, divider_y + 12)
    canvas.text(
        (MARGIN, list_bottom + 12), FOOTNOTE,
        font=load_typeface("regular", 17), fill=FAINT,
    )
    return page


def main(argv):
    out = Path(argv[1]) if len(argv) > 1 else HERE.parent / "entry.png"
    build_image().save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main(sys.argv)
