[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/supdinals/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/supdinals/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# World News — Thursday 19 November 2026 in one image

An entry for the make.fun bounty **news-image-20261119**: one 1024x1024 image
that sums up the world news of Thursday 19 November 2026.

## What the image shows

- **Lead — Diplomacy / Asia-Pacific:** Donald Trump, Xi Jinping and Vladimir
  Putin hold their first-ever three-way summit in Shenzhen, on the sidelines
  of the APEC summit; nuclear arms, the wars in Ukraine and Iran, trade and
  AI top the agenda.
- **1 — Justice / The Hague:** The World Court (ICJ) delivers its final,
  binding judgment in Gambia's genocide case against Myanmar over the 2017
  Rohingya campaign, seven years on.
- **2 — Conflict / Europe:** The Crimean Bridge is hit for the third time
  this week; a nighttime drone attack halts road and rail traffic, Russia
  says no one was injured and the damage is being assessed.
- **3 — Politics / South Asia:** Parts of Bangladesh shut down in an Awami
  League lockdown ahead of Sheikh Hasina's planned December return; the
  Yunus family home in Chattogram is set ablaze and police say two
  ruling-party members were killed.
- **4 — Economy / Technology:** Anthropic raises a record $81.3 billion in
  the largest IPO ever, priced at $83 a share, and starts trading on Nasdaq
  on Thursday, beating SpaceX's $75 billion debut.
- **5 — Weather / South Asia:** Over 80,000 people are evacuated in Odisha
  as severe Cyclone Akvan nears India's east coast, with landfall expected
  Friday noon between Narsapur and Puri at 90–100 km/h.

Every claim is sourced in [SOURCES.md](SOURCES.md) (16 candidates researched
across 21 queries, each final story verified in at least two independent
sources that were opened and read). The variant selection process is
documented in [EVAL.md](EVAL.md).

## How it was made

The image was rendered with Python + Pillow by `build/render.py`, using only
the bundled Liberation Sans fonts (`build/fonts/`, SIL Open Font License 1.1 —
see `build/fonts/OFL.txt`) and icons drawn entirely with code. No photos,
logos, or third-party artwork. Three layouts were rendered and compared
pairwise; the winning layout (big lead + numbered list, the pattern that won
the 17 and 18 November editions of this series) was saved as `entry.png`.

## The program

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. It uses no network, clock, or randomness, so two runs
write byte-identical output:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
sha256sum out/entry.png   # identical on every run
```

## License

MIT — see [LICENSE](LICENSE). The bundled fonts are under the SIL Open Font
License 1.1 (see `build/fonts/OFL.txt`).
