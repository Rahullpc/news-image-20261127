# THE WORLD — Friday 27 November 2026

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Rahullpc/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Rahullpc/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

Entry for the make.fun bounty
[Sum up 27 November's world news in one image](https://make.fun/bounty/news-image-20261127):
a program that draws the front page of **THE WORLD** for Friday
27 November 2026 as a single 1024×1024 image — no photographs,
everything drawn in code.

## The day in one image

- **Lead story — Thanksgiving Day:** a nor'easter grounds Macy's
  100th Thanksgiving Day Parade in New York, the first weather halt
  in a century. The parade moves to Saturday, 8:30 a.m. ET, with
  gusts to 65 mph.
- **Trade:** partners hit back at Trump's new tariffs; China warns
  it could lift tariffs to 40%.
- **Korea:** Kim Jong Un orders wider deployment of tactical
  nuclear weapons.
- **Egypt:** 31 killed in a fuel tanker fire on Cairo's Ring Road.
- **Sport:** Plzen thrash Benfica 4–0 in the Europa League; the
  Bears stun the Lions 39–35 in a Thanksgiving thriller.
- **Markets:** S&P puts Nvidia on CreditWatch negative; shares fell
  3.9% to $149.30.
- **Also today:** Black Friday, EU leaders meet in Brussels, and
  Houthi claims of strikes on Saudi Red Sea ports.

Sources: Reuters, AP, CNN, UEFA. See [RESEARCH.md](RESEARCH.md)
for the facts behind every story and what was deliberately left out.

## Run it

```sh
python3 main.py
```

Writes `entry.png` (1024×1024) next to `main.py`. Python standard
library plus Pillow only; no network, no installs, deterministic —
running it twice writes the same bytes.

## Files

- `main.py` — entrypoint; renders the poster to `entry.png`.
- `draw_poster.py` — all drawing: masthead, markets strip, lead
  story, six-panel grid, Also Today strip, footer.
- `RESEARCH.md` — the news research behind the poster.
- `BUILD.md` — how this entry was built and verified.
