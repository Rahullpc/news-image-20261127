# BUILD — news-image-20261127

## Poster layout plan (figure first)

One question this layout answers: *can a reader who missed 27 November 2026
tell, at a glance and at ~300 px wide, what the day's biggest stories were,
in what order of importance, and on what date?*

The poster is a classic front page: one masthead, one dominant lead, a
2-column-by-3-row story grid, a one-line strip, a footer. Importance falls
top to bottom, left to right.

```
+--------------------------------------------------------------+
| 1024 x 1024  |  paper #f7f2e7, ink #141414, red #a31d1d        |
|                                                              |
|  THE WORLD                      (masthead, serif, ~96 px)    |
|  FRIDAY, 27 NOVEMBER 2026  |  No. 332  |  ONE DAY'S NEWS     |
| ------------------------------------------------------------ |
|  TICKER: EU futures +1.4-2.2%  Asia higher  US shut          |
|          Black Friday short session (markets, Thu 26 Nov)    |
| ------------------------------------------------------------ |
|  LEAD (full width, ~250 px tall)                             |
|  [storm art: grounded balloon, rain, gusts]  | HEADLINE      |
|  STORM GROUNDS THE PARADE                                    |
|  Macy's 100th Thanksgiving parade postponed — first weather  |
|  halt in a century; nor'easter, gusts to 65 mph; parade      |
|  moves to Saturday 8:30 a.m. ET; last halted 1942–44         |
| ------------------------------------------------------------ |
|  GRID 2 rows x 3 cols  (~200 px per cell)                    |
|  +-----------+ +-----------+ +-----------+                    |
|  | containers| | missile   | | tanker fire|                   |
|  | PARTNERS  | | KIM ORDERS| | 31 KILLED  |                   |
|  | HIT BACK  | | MORE NUKES| | IN CAIRO   |                   |
|  +-----------+ +-----------+ +-----------+                    |
|  | soccer    | | NFL ball  | | NVDA chip  |                   |
|  | PLZEN 4–0 | | BEARS 39–| | NVIDIA ON  |                   |
|  | BENFICA   | | 35 LIONS  | | CREDITWATCH|                   |
|  +-----------+ +-----------+ +-----------+                    |
| ------------------------------------------------------------ |
|  ALSO TODAY (one line, 3 items)                              |
|  Black Friday: short session | EU leaders meet in Brussels |   |
|  Houthis claim Red Sea port strikes                          |
| ------------------------------------------------------------ |
|  THE WORLD — Friday 27 November 2026 — Sources: Reuters,     |
|  AP, CNN, UEFA. Drawn in code; no photographs.               |
+--------------------------------------------------------------+
```

Layout facts (all in `draw_poster.py` as named constants):

- Canvas 1024 x 1024, 28 px outer margin, 14 px gutters between grid cells.
- Masthead band y 24–150: nameplate, date line, double rule.
- Ticker band y 156–186: four market items, green for rises, red for shut.
- Lead band y 196–448: illustration left (300 x 220), headline + summary right.
- Grid y 476–876: 3 columns x 2 rows, each cell 313 x 198 (art 80 px,
  kicker, 2-line headline, up to 3 lines of body).
- Also-today strip y 886–946: heading + three one-liners.
- Footer y 956–996: source line, centred.

## Design choices

- **Palette (taste-skill: one system, no violet):** warm newsprint paper,
  near-black ink, one red for urgency and section kickers, one deep blue
  for charts and the tariff panel, one green only for rising market figures.
- **Type:** DejaVu Serif Bold for masthead and headlines (newspaper voice),
  DejaVu Sans for body copy, DejaVu Sans Bold for kickers and the ticker.
  Smallest body text 13 px so the page still reads at ~300 px wide.
- **Density (motion-design three layers, applied to a still image):**
  primary = lead storm art and headlines; secondary = six small coded
  illustrations, one per grid cell; ambient = rules, dots, ticker figures,
  kicker labels and the footer source line. The page is busy on purpose —
  a newspaper front page, not a minimal poster.
- **Illustrations:** every picture is drawn in code with PIL primitives
  (lines, polygons, ellipses, arcs). No photographs, no network, no fonts
  beyond the system DejaVu/Liberation set, so the run is deterministic.

## Facts used (from RESEARCH.md)

- Lead: nor'easter on Thanksgiving Day; Macy's 100th parade postponed,
  first weather postponement in a century; gusts 30–40 mph, to 60–65 mph;
  balloons grounded past 34 mph gusts; parade moves to Sat 28 Nov 8:30 a.m.
  ET; last halted 1942–44 in wartime.
- G1: partners protest Trump's new tariffs (14 partners, Section 301);
  China warns it could lift tariffs to 40% if talks fail; USTR hearing
  25 January; EU futures +1.4–2.2%, Asia higher, US shut for Thanksgiving.
- G2: Kim Jong Un tours nuclear sites, orders wider deployment of tactical
  nuclear weapons; nuclear-material production being expanded; nuclear
  status called irreversible (KCNA, Thu 26 Nov).
- G3: fuel tanker overturns on Cairo's Ring Road (Giza, Warraq), at least
  31 killed, 21 injured, 27 vehicles burned, 39 ambulances sent.
- G4: Europa League Matchday 5, Thu 26 Nov: Plzen 4–0 Benfica; Milan come
  from 2–0 down to win 4–2 at Olympiacos (Pulisic 71'); Bournemouth 2–1
  at Celta, perfect record kept.
- G5: NFL Thanksgiving: Bears 39–35 Lions — Williams to Odunze, 6-yard TD
  with 3 seconds left; Bears 9–2, first in the NFC North; Gibbs 205 yards
  and 3 TDs for Detroit.
- G6: S&P puts Nvidia on CreditWatch negative (possible one-notch cut in
  90 days); Moody's keeps Aa1 stable; shares fell 3.9% to $149.30.
- Strip: Black Friday, Wall Street reopens for a short session (close
  1 p.m. ET); EU leaders meet in Brussels on the budget and Ukraine aid;
  Houthis claim strikes on Saudi Red Sea ports, Riyadh says missiles
  aimed at the capital were intercepted.

Deliberately NOT printed: any Mayon eruption (the big one was 30 October,
not 27 November), any Brent price or Black Friday sales total (each from a
single social-media briefing), the unfinished Cowboys–Eagles and
Chiefs–Bills games, any single India tariff rate, and any DOJ-inquiry
detail on Huang (single aggregator only). Stories already led in the
26 November edition are not repeated except where Thursday brought a new
development.

## Implementation

- `draw_poster.py` — PIL program, stdlib + Pillow only, no network, no
  randomness, no timestamps. Writes `entry.png` next to itself (or to the
  path in `sys.argv[1]`).
- `main.py` — stdlib-only entrypoint: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` (default `/output`), checks PNG magic + IHDR
  dimensions (≤1024x1024), size ≤ 1 MiB, and that the copy's sha256 matches
  the source.
- `entry.png` — the rendered poster, 1024 x 1024, ≤ 1 MiB.

## Verification (done locally)

- `python3 draw_poster.py` → `entry.png`, 1024 x 1024, 150,717 bytes
  (sha256 `abdbe2c6dd1d25d727438271b689fce435aea37f3f8647a6976fc1236477bc3d`).
  Two runs of `draw_poster.py` produce byte-identical files.
- `MAKEFUN_OUTPUT_DIR=/tmp/output-test python3 main.py` run twice →
  identical sha256 both runs, matching the source file.
- Poster read back as an image and checked: date correct, headlines
  legible, no clipped or doubled text. First render showed three in-art
  labels colliding with their illustrations (trade, Korea, NFL, chip
  cells); all four were moved or removed and the poster was re-rendered
  and re-read clean.
