# Evaluation — variant selection for news-image-20261119

All three variants carry identical stories and wording (same lead + five
supporting stories, verified in SOURCES.md). Only the layout differs:

- **A — Tile grid:** light banner; lead tile on top, 2x2 supporting tiles,
  fifth story as a wide bottom tile; full-length body text in every tile.
- **B — Newspaper front page:** cream "THE WORLD TODAY" masthead, red date
  line, lead, two compact columns with short bodies, fifth story as a wide
  strip at the bottom.
- **C — Big lead + numbered list:** dark canvas, gold banner
  "WORLD NEWS — THURSDAY 19 NOVEMBER 2026", one big lead headline with an
  explanatory sentence and a globe icon, then a numbered list 1–5 of the
  supporting stories with category labels, one-line summaries, a small
  code-drawn icon per story, and a source footnote. This is the layout
  pattern that won the 17 and 18 November editions of this series.

## Method

Each pair was compared in 3 rounds (9 comparisons total), asking which
image best sums up the world news of Thursday 19 November 2026 for a
careful picture editor: the day's biggest stories, clearly dated,
accurate, complete, and readable at a glance. The left/right position of
the two images was swapped between rounds so position alone could not
decide a round. All six full-size renders and their 512x512 downscales
were inspected directly.

## Results

| Pair | Round 1 | Round 2 (swapped) | Round 3 | Pair score |
|------|---------|-------------------|-----------|------------|
| A vs B | A | A | A | A 3–0 |
| A vs C | C | C | A | C 2–1 |
| B vs C | C | C | C | C 3–0 |

Win rates over 6 comparisons each:

- **C — 5/6 (83%)** ← winner
- A — 4/6 (67%)
- B — 0/6 (0%)

## Why C won

- The gold banner carries the full date at maximum contrast, and the lead
  (the first-ever Trump–Xi–Putin three-way summit) gets the single biggest
  headline on the page, matching its news weight.
- The numbered list is the fastest scan of the three layouts: number,
  category label, 30px headline, one-line summary, small icon. Nothing
  competes for attention and no space is wasted.
- B reads cleanly up close but leaves roughly a quarter of the canvas
  empty under its last story and uses the shortest body texts, so it
  carries the least verified detail.
- A is the most complete (full body text in every tile, including the
  700,000 Rohingya figure and the $1.5 trillion valuation) and won one
  round against C on that completeness, but its tile headlines render
  smaller than C's list headlines and the eye has no single path through
  the page.

## Weaknesses found in C and fixed

- The first C render had no per-story icons; the brief's layout calls for
  code-drawn icons, so a small icon (scales, bridge, house-and-flame,
  rising chart, cyclone spiral) was added to every list row, rendered on
  its own tile and scaled so the line work stays correct at small size.
- The lead globe icon originally overlapped the gold divider line; it was
  re-rendered as a scaled tile that clears the line.
- List headlines were raised from 27px to 30px (the brief's minimum) and
  row spacing tightened so the list still ends above the footnote.
- Residual, accepted: the bridge icon reads abstractly at 62px (two
  pylons over waves); the headline next to it carries the meaning. The
  list uses one-line summaries, so two details that variant A carries
  (700,000 Rohingya fled; ~$1.5 trillion valuation) appear only in
  SOURCES.md and the README, not on the final image.

## Readability at 512x512

All three downscales were inspected. In C, the banner, the date, the lead
headline, every list headline and every one-line summary stay legible at
512px; the icons remain recognisable except the bridge (see above). In A,
tile body text is the smallest of the three but still readable. In B,
everything reads but the empty bottom band is even more obvious at small
size.

## Final image

- File: `entry.png` — 1024x1024 PNG, 154,812 bytes (limit 1 MiB).
- sha256: `fbf571a665606912694771484e38e39209841ea3d3db8e1d9960b9bab569f7ce`
- Determinism: `build/render.py` re-run reproduces variant C byte-for-byte;
  `main.py` was run twice into two directories and both outputs are
  byte-identical to `entry.png` (sha256 above).
- Final proofread: every headline, figure and name on the image was
  re-checked against SOURCES.md (summit in Shenzhen on Thu 19 Nov;
  ICJ judgment day with no verdict direction claimed; third Crimean Bridge
  attack, traffic halted, no injuries per Russia; Bangladesh lockdown, two
  ruling-party members killed per police; Anthropic $81.3bn at $83/share,
  Nasdaq debut Thursday, SpaceX $75bn; Akvan over 80,000 evacuated,
  landfall Friday noon Narsapur–Puri at 90–100 km/h). No discrepancies.
