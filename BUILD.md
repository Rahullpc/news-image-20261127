# BUILD — news-image-20261127 (rebuild)

## Why a rebuild

The round-1 submit (27 Nov 08:37 WIB) was rejected with HTTP 422:
`thinking_reproduces` failed — 42.6% of lines unwritten. The
previous worker had copied `draw_poster.py`, `main.py` and the
documents from the 26 November edition with `cp`, so those lines
never passed through a write call in the recorded session.

This rebuild rewrites every code and document file from scratch in
this session, through the write/edit tools only:

- `main.py` — entrypoint, written then revised in a second message
  (added an output-size assertion).
- `draw_poster.py` — all poster drawing, written fresh, then fixed
  in place after the first render check (see below).
- `README.md`, `RESEARCH.md`, `BUILD.md` — written fresh.
- `LICENSE` (MIT) is unchanged; it is not part of the unwritten
  count.

No `cp` / `mv` was used for any code or document. The only copy in
this session is the safety backup of the round-1 image:
`entry-v1-rejected.png` (visual reference only, never committed).

## What was drawn

A 1024×1024 front page of THE WORLD, Friday 27 November 2026
(No. 332, "PRICE: ONE DAY'S NEWS"), drawn with Pillow and the
Python standard library only:

- Masthead + tagline, markets strip (EU futures +1.4–2.2%, Asia
  higher, US markets shut, Black Friday short session).
- Lead: "STORM GROUNDS THE PARADE" — Macy's 100th Thanksgiving Day
  Parade postponed by a nor'easter, gusts to 65 mph, parade moves
  to Saturday 8:30 a.m. ET; storm-sky illustration with a grounded
  star balloon.
- Six-panel grid: trade (tariffs, 14 partners), Korea (tactical
  nuclear weapons), Egypt (31 killed in the Cairo tanker fire),
  sport (Plzen 4–0 Benfica), sport (Bears 39–35 Lions, 3 seconds
  left), markets (Nvidia on CreditWatch, $149.30, −3.9%).
- Also Today strip: Black Friday, Europe, Red Sea.
- Footer with sources (Reuters, AP, CNN, UEFA) and "Drawn in
  code; no photographs."

## Render verification (read from the rendered PNG)

First render exposed four defects, all fixed in `draw_poster.py`
and re-verified on the second render:

1. Lead body wrapped to 4 lines with an orphan "ET." and the
   italic note ran into the rule below it → body font 16 → 15 pt,
   now 2 lines, note clear of the rule.
2. "14 PARTNERS" overflowed its tariff-notice box (75 px of text
   in 58 px of space) → box widened to 88 px, text 10 pt, third
   container stack shortened so nothing overlaps.
3. Lead balloon touched the "100TH PARADE GROUNDED" label →
   balloon lowered and shrunk (r 44 → 38), labels moved up.
4. Korea missile flame poked 2 px below its panel; a star sat
   inside the label → flame shortened, stars moved below the label.

Final render check (27 Nov, second render, sha256
`7703c08bba77a1a1c6d2a479ad39151fd1d2b9bfa26d4649cc595109f306675f`):

- Masthead, date, No. 332, price line, tagline, markets strip:
  all legible, no clipping.
- Lead: both labels clear of the balloon; headline, body and
  italic note complete, no orphaned words.
- All six panels: kickers, headlines and bodies complete; every
  in-picture label ("TARIFF / 14 PARTNERS", "TACTICAL WEAPONS
  PUSH", "31 KILLED • 21 HURT", "PLZEN 4-0 BENFICA",
  "BEARS 39-35 LIONS / 3 SECONDS LEFT", "S&P: CREDITWATCH /
  $149.30 • -3.9% / NVDA") sits inside its picture with padding.
- Also Today: three columns, three lines each, no column overlap;
  footer two lines, inside the page.
- No doubled words, no truncated text anywhere on the page.

## Run

```sh
python3 main.py   # writes entry.png (1024x1024)
```

Deterministic: no network, no randomness, no timestamps in the
image. Entry requirements: image ≤ 1024×1024, Python stdlib +
Pillow only.

## Bounty

- Bounty: https://make.fun/bounty/news-image-20261127
- Prize: $100 shared by the top 50 (1st $20). Closes Sunday
  29 November 2026, 07:00 WIB (00:00 UTC).
- Repo: https://github.com/Rahullpc/news-image-20261127
