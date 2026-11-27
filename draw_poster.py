#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Friday 27 November 2026.

A code-drawn newspaper poster for the make.fun news-image-20261127 bounty:
one lead story, a 2x3 grid of stories, an ALSO TODAY strip and a footer.
Stdlib + Pillow only. No network, no randomness, no timestamps, so every
run produces byte-identical output.

Usage: python3 draw_poster.py [output-path]   (default: entry.png)
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
CONTENT_W = W - 2 * MARGIN          # 968
GUTTER = 14

PAPER = (247, 242, 231)             # warm newsprint
INK = (22, 21, 19)
RED = (163, 29, 29)
BLUE = (30, 58, 95)
GREEN = (31, 107, 58)
MUTED = (107, 100, 85)
LIGHT_RULE = (190, 180, 160)
SKY = (214, 228, 238)
STORM = (58, 72, 92)               # nor'easter sky
PITCH = (46, 125, 62)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def double_rule(draw, x0, y, x1):
    rule(draw, x0, y, x1, width=3)
    rule(draw, x0, y + 5, x1, width=1)


# ---------------------------------------------------------------- masthead
def draw_masthead(d):
    double_rule(d, MARGIN, 26, W - MARGIN)
    f_date = font(SANS_B, 19)
    date = "FRIDAY, 27 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 40), date,
           font=f_date, fill=INK)
    f_side = font(SANS, 13)
    d.text((MARGIN, 43), "No. 332", font=f_side, fill=MUTED)
    right = "PRICE: ONE DAY'S NEWS"
    d.text((W - MARGIN - d.textlength(right, font=f_side), 43), right,
           font=f_side, fill=MUTED)

    f_name = font(SERIF_B, 96)
    name = "THE WORLD"
    d.text(((W - d.textlength(name, font=f_name)) / 2, 62), name,
           font=f_name, fill=INK)
    f_sub = font(SANS, 14)
    sub = "THE DAY'S NEWS  •  FROM EVERY CORNER OF THE GLOBE"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 158), sub,
           font=f_sub, fill=MUTED)
    double_rule(d, MARGIN, 184, W - MARGIN)


# ---------------------------------------------------------------- ticker
def draw_ticker(d):
    y = 198
    f_lab = font(SANS_B, 14)
    d.text((MARGIN, y), "MARKETS — THURSDAY", font=f_lab, fill=RED)
    items = [("EU futures", "+1.4–2.2%", GREEN), ("Asia", "higher", GREEN),
             ("US markets", "shut", RED), ("Black Friday", "short session", INK)]
    f_item = font(SANS_B, 15)
    x = MARGIN + 218
    for name, val, col in items:
        d.text((x, y), name, font=font(SANS, 15), fill=INK)
        x += d.textlength(name + " ", font=font(SANS, 15))
        d.text((x, y), val, font=f_item, fill=col)
        x += d.textlength(val, font=f_item) + 26
    rule(d, MARGIN, 226, W - MARGIN, width=1, fill=LIGHT_RULE)


# ---------------------------------------------------------------- lead art
def draw_lead_art(d, x0, y0, w, h):
    """A nor'easter over New York: dark storm sky, slanting rain, and a
    giant parade balloon grounded on the street under its net."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=STORM, outline=INK, width=2)
    # storm clouds
    for cx, cy, r in ((x0 + 46, y0 + 26, 26), (x0 + 96, y0 + 16, 32),
                      (x0 + 150, y0 + 28, 24), (x0 + 210, y0 + 18, 28),
                      (x0 + 258, y0 + 30, 22)):
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                  fill=(40, 52, 70))
    # slanting rain
    for i in range(14):
        rx = x0 + 12 + i * 21
        ry = y0 + 52 + (i % 4) * 8
        d.line([(rx, ry), (rx - 8, ry + 22)], fill=(150, 170, 195), width=2)
    # street
    d.rectangle([x0, y0 + h - 34, x0 + w, y0 + h], fill=(70, 64, 58))
    d.line([(x0, y0 + h - 34), (x0 + w, y0 + h - 34)], fill=INK, width=2)
    # the grounded balloon: a big round star balloon, half-deflated
    bx, by, br = x0 + 150, y0 + 128, 52
    d.ellipse([bx - br, by - br + 12, bx + br, by + br - 6],
              fill=(200, 60, 60), outline=(120, 20, 20), width=3)
    # star on the balloon
    cx, cy, r = bx, by + 2, 26
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 220, 60), outline=(150, 110, 0))
    # net ropes over the balloon
    for nx in (bx - 34, bx - 12, bx + 12, bx + 34):
        d.line([(nx, by - 38), (nx - 6, y0 + h - 34)], fill=(220, 220, 220),
               width=2)
    # sandbags
    for sx in (x0 + 84, x0 + 116, x0 + 186, x0 + 218):
        d.ellipse([sx, y0 + h - 26, sx + 26, y0 + h - 12],
                  fill=(150, 135, 100), outline=INK, width=1)
    # wind arrow + gust label
    d.line([(x0 + 14, y0 + 52), (x0 + 66, y0 + 52)], fill=(255, 255, 255),
           width=4)
    d.polygon([(x0 + 66, y0 + 52), (x0 + 52, y0 + 44),
               (x0 + 52, y0 + 60)], fill=(255, 255, 255))
    d.text((x0 + 12, y0 + 62), "GUSTS TO 65 MPH", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    d.text((x0 + 12, y0 + 80), "100TH PARADE GROUNDED",
           font=font(SANS_B, 13), fill=(255, 220, 60))


def draw_lead(d):
    y0 = 240
    draw_lead_art(d, MARGIN, y0, 302, 208)
    x = MARGIN + 322
    w = W - MARGIN - x
    f_kick = font(SANS_B, 15)
    d.text((x, y0 + 2), "LEAD STORY  —  THANKSGIVING DAY", font=f_kick,
           fill=RED)
    y = para(d, x, y0 + 26,
             "STORM GROUNDS THE PARADE",
             font(SERIF_B, 30), w, 35)
    y = para(d, x, y + 6,
             "Macy's postpones its 100th Thanksgiving Day Parade — the "
             "first weather halt in a century — as a nor'easter bears down "
             "on New York with gusts to 65 mph. The parade moves to "
             "Saturday, 8:30 a.m. ET.",
             font(SANS, 15), w, 20)
    y = para(d, x, y + 6,
             "Balloons must be grounded when gusts pass 34 mph; high wind "
             "and coastal flood warnings are in force. The parade was last "
             "halted in 1942–44, in wartime.",
             font(SANS_I, 13), w, 17, fill=MUTED)
    rule(d, MARGIN, 462, W - MARGIN, width=1, fill=LIGHT_RULE)

# ---------------------------------------------------------------- grid art
def draw_trade(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 232, 214),
                outline=INK, width=1)
    # shipping containers
    d.rectangle([x0 + 14, y0 + 34, x0 + 94, y0 + 66], fill=(163, 29, 29),
                outline=INK, width=1)
    d.rectangle([x0 + 100, y0 + 34, x0 + 180, y0 + 66], fill=(30, 58, 95),
                outline=INK, width=1)
    d.rectangle([x0 + 54, y0 + 8, x0 + 134, y0 + 34], fill=(31, 107, 58),
                outline=INK, width=1)
    for cx in (x0 + 14, x0 + 100, x0 + 54):
        for vx in range(cx + 8, cx + 78, 12):
            d.line([(vx, y0 + 10 if cx == x0 + 54 else y0 + 36),
                    (vx, y0 + 32 if cx == x0 + 54 else y0 + 64)],
                   fill=(255, 255, 255), width=1)
    # tariff document with a red stamp
    d.rectangle([x0 + 214, y0 + 8, x0 + 292, y0 + 66], fill=(255, 255, 255),
                outline=INK, width=2)
    d.text((x0 + 222, y0 + 12), "TARIFF", font=font(SANS_B, 12), fill=RED)
    for ly in (y0 + 30, y0 + 38, y0 + 46):
        d.line([(x0 + 222, ly), (x0 + 284, ly)], fill=MUTED, width=1)
    d.text((x0 + 222, y0 + 52), "14 PARTNERS", font=font(SANS_B, 10),
           fill=INK)


def draw_korea(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(28, 32, 44),
                outline=INK, width=1)
    for sx, sy in ((x0 + 18, y0 + 12), (x0 + 70, y0 + 22), (x0 + 130, y0 + 10),
                   (x0 + 200, y0 + 16), (x0 + 260, y0 + 26), (x0 + 296, y0 + 8)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # missile on its launcher, nose up
    mx = x0 + 130
    d.polygon([(mx, y0 + 10), (mx - 12, y0 + 30), (mx + 12, y0 + 30)],
              fill=(200, 200, 200), outline=INK)
    d.rectangle([mx - 12, y0 + 30, mx + 12, y0 + 62], fill=(180, 180, 180),
                outline=INK, width=1)
    d.rectangle([mx - 20, y0 + 62, mx + 20, y0 + 70], fill=(120, 120, 120),
                outline=INK, width=1)
    # flame
    d.polygon([(mx - 8, y0 + 70), (mx, y0 + h - 8), (mx + 8, y0 + 70)],
              fill=(230, 120, 30))
    d.polygon([(mx - 4, y0 + 70), (mx, y0 + h - 16), (mx + 4, y0 + 70)],
              fill=(250, 200, 60))
    d.text((x0 + 10, y0 + 6), "TACTICAL WEAPONS PUSH",
           font=font(SANS_B, 11), fill=(255, 220, 60))
    # facility blocks
    d.rectangle([x0 + 14, y0 + 48, x0 + 74, y0 + 72], fill=(70, 76, 92),
                outline=(150, 150, 160), width=1)
    d.rectangle([x0 + 220, y0 + 44, x0 + 292, y0 + 72], fill=(70, 76, 92),
                outline=(150, 150, 160), width=1)
    for wx in (x0 + 24, x0 + 40, x0 + 56, x0 + 230, x0 + 248, x0 + 266):
        d.rectangle([wx, y0 + 56, wx + 8, y0 + 66], fill=(255, 220, 60))


def draw_cairo(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 26, 22),
                outline=INK, width=1)
    # night skyline
    for bx, bw, bh in ((x0 + 10, 34, 26), (x0 + 52, 26, 36),
                       (x0 + 86, 30, 22), (x0 + 210, 36, 30),
                       (x0 + 254, 28, 24), (x0 + 288, 18, 18)):
        d.rectangle([bx, y0 + h - 18 - bh, bx + bw, y0 + h - 18],
                    fill=(60, 54, 48), outline=(90, 82, 70), width=1)
    # highway
    d.rectangle([x0, y0 + h - 18, x0 + w, y0 + h], fill=(80, 76, 70))
    d.line([(x0, y0 + h - 9), (x0 + w, y0 + h - 9)], fill=(255, 220, 60),
           width=2)
    # fire: layered flames over a tanker
    fx = x0 + 150
    d.rectangle([fx - 52, y0 + 46, fx + 52, y0 + 62], fill=(150, 150, 150),
                outline=INK, width=1)
    d.ellipse([fx - 60, y0 + 54, fx - 44, y0 + 70], fill=INK)
    d.ellipse([fx + 44, y0 + 54, fx + 60, y0 + 70], fill=INK)
    d.polygon([(fx - 34, y0 + 46), (fx - 22, y0 + 8), (fx - 8, y0 + 46)],
              fill=(230, 120, 30))
    d.polygon([(fx - 6, y0 + 46), (fx + 8, y0 + 2), (fx + 22, y0 + 46)],
              fill=(250, 160, 40))
    d.polygon([(fx + 18, y0 + 46), (fx + 30, y0 + 16), (fx + 40, y0 + 46)],
              fill=(230, 120, 30))
    d.polygon([(fx - 14, y0 + 46), (fx - 4, y0 + 22), (fx + 6, y0 + 46)],
              fill=(250, 200, 60))
    # smoke
    for sx, sy, r in ((x0 + 120, y0 + 8, 8), (x0 + 140, y0 + 4, 6),
                      (x0 + 180, y0 + 10, 7)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 112, 100))
    d.text((x0 + 10, y0 + 6), "31 KILLED • 21 HURT",
           font=font(SANS_B, 11), fill=(255, 255, 255))


def draw_europa(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PITCH, outline=INK, width=1)
    d.line([(x0 + w // 2, y0), (x0 + w // 2, y0 + h)], fill=(255, 255, 255),
           width=2)
    d.ellipse([x0 + w // 2 - 22, y0 + h // 2 - 22, x0 + w // 2 + 22,
               y0 + h // 2 + 22], outline=(255, 255, 255), width=2)
    d.rectangle([x0 + w - 34, y0 + 18, x0 + w - 6, y0 + 62],
                outline=(255, 255, 255), width=2)
    for gy in range(y0 + 22, y0 + 60, 8):
        d.line([(x0 + w - 34, gy), (x0 + w - 6, gy)], fill=(255, 255, 255),
               width=1)
    bx, by = x0 + 70, y0 + h - 30
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 255, 255),
              outline=INK, width=1)
    d.polygon([(bx, by - 6), (bx + 6, by - 2), (bx + 4, by + 5),
               (bx - 4, by + 5), (bx - 6, by - 2)], fill=INK)
    d.rectangle([x0 + 8, y0 + 8, x0 + 176, y0 + 30], fill=(20, 20, 20))
    d.text((x0 + 14, y0 + 11), "PLZEN 4–0 BENFICA", font=font(SANS_B, 13),
           fill=(255, 220, 60))


def draw_nfl(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 90, 50),
                outline=INK, width=1)
    # yard lines
    for lx in range(x0 + 40, x0 + w - 20, 44):
        d.line([(lx, y0 + 6), (lx, y0 + h - 6)], fill=(255, 255, 255), width=2)
    # goalposts
    d.line([(x0 + w - 22, y0 + 14), (x0 + w - 22, y0 + h - 14)],
           fill=(255, 220, 60), width=4)
    d.line([(x0 + w - 22, y0 + 14), (x0 + w - 34, y0 + 14)],
           fill=(255, 220, 60), width=4)
    d.line([(x0 + w - 22, y0 + 14), (x0 + w - 10, y0 + 14)],
           fill=(255, 220, 60), width=4)
    # football
    bx, by = x0 + 90, y0 + 44
    d.ellipse([bx - 20, by - 12, bx + 20, by + 12], fill=(120, 70, 30),
              outline=(255, 255, 255), width=2)
    d.line([(bx - 10, by), (bx + 10, by)], fill=(255, 255, 255), width=2)
    for lx in (bx - 6, bx - 2, bx + 2, bx + 6):
        d.line([(lx, by - 4), (lx, by + 4)], fill=(255, 255, 255), width=1)
    # clock: 3 seconds left
    d.ellipse([x0 + 210, y0 + 26, x0 + 258, y0 + 74], fill=(255, 255, 255),
              outline=INK, width=2)
    d.line([(x0 + 234, y0 + 50), (x0 + 234, y0 + 32)], fill=INK, width=2)
    d.line([(x0 + 234, y0 + 50), (x0 + 246, y0 + 56)], fill=INK, width=2)
    d.text((x0 + 10, y0 + h - 18), "3 SECONDS LEFT",
           font=font(SANS_B, 11), fill=(255, 220, 60))
    d.rectangle([x0 + 8, y0 + 8, x0 + 168, y0 + 30], fill=(20, 20, 20))
    d.text((x0 + 14, y0 + 11), "BEARS 39–35 LIONS", font=font(SANS_B, 13),
           fill=(255, 220, 60))


def draw_chip(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 238, 226),
                outline=INK, width=1)
    # chip, clear of the corner labels
    d.rectangle([x0 + 130, y0 + 22, x0 + 220, y0 + 74], fill=(40, 60, 40),
                outline=INK, width=2)
    for px in (x0 + 146, x0 + 166, x0 + 186, x0 + 206):
        d.line([(px, y0 + 14), (px, y0 + 22)], fill=INK, width=3)
        d.line([(px, y0 + 74), (px, y0 + 80)], fill=INK, width=3)
    for py in (y0 + 36, y0 + 50, y0 + 64):
        d.line([(x0 + 122, py), (x0 + 130, py)], fill=INK, width=3)
        d.line([(x0 + 220, py), (x0 + 228, py)], fill=INK, width=3)
    d.text((x0 + 152, y0 + 42), "NVDA", font=font(SANS_B, 16),
           fill=(255, 255, 255))
    # falling arrow
    d.line([(x0 + 220, y0 + 14), (x0 + 262, y0 + 34), (x0 + 292, y0 + 58)],
           fill=RED, width=5)
    d.polygon([(x0 + 292, y0 + 58), (x0 + 272, y0 + 56),
               (x0 + 290, y0 + 40)], fill=RED)
    d.text((x0 + 12, y0 + 8), "S&P: CREDITWATCH", font=font(SANS_B, 12),
           fill=RED)
    d.text((x0 + 12, y0 + h - 18), "$149.30  •  -3.9%",
           font=font(SANS_B, 12), fill=INK)

GRID = [
    ("TRADE", "PARTNERS HIT BACK AT TRUMP'S NEW TARIFFS",
     "China warns it could lift tariffs to 40% if talks fail. The EU and "
     "Japan protest the plan; a hearing is set for 25 Jan.",
     draw_trade),
    ("KOREA", "KIM ORDERS MORE TACTICAL NUCLEAR WEAPONS",
     "Kim Jong Un tours nuclear sites and orders wider deployment of "
     "tactical weapons, calling the North's status irreversible.",
     draw_korea),
    ("EGYPT", "31 KILLED IN CAIRO FUEL TANKER FIRE",
     "A tanker overturned on the Ring Road in Giza, setting 27 vehicles "
     "ablaze. At least 31 people died and 21 were injured.",
     draw_cairo),
    ("SPORT", "PLZEN THRASH BENFICA 4–0 IN EUROPE",
     "Europa League: Plzen stun unbeaten Benfica; Milan come from 2–0 down "
     "to win 4–2 at Olympiacos; Bournemouth stay perfect.",
     draw_europa),
    ("SPORT", "BEARS STUN LIONS IN THANKSGIVING THRILLER",
     "Caleb Williams finds Rome Odunze with 3 seconds left; Chicago win "
     "39–35 and take first place in the NFC North.",
     draw_nfl),
    ("MARKETS", "NVIDIA PUT ON CREDITWATCH BY S&P",
     "S&P puts Nvidia on CreditWatch negative; shares fell 3.9% to $149.30 "
     "as scrutiny of Jensen Huang grows in Washington.",
     draw_chip),
]


def draw_grid(d):
    cell_w = (CONTENT_W - 2 * GUTTER) // 3          # 313
    cell_h = 196
    y_rows = (476, 678)
    for i, (kick, head, body, art) in enumerate(GRID):
        col, row = i % 3, i // 3
        x = MARGIN + col * (cell_w + GUTTER)
        y = y_rows[row]
        art(d, x, y, cell_w, 80)
        d.text((x, y + 88), kick, font=font(SANS_B, 12), fill=RED)
        yy = para(d, x, y + 106, head, font(SERIF_B, 18), cell_w, 21)
        para(d, x, yy + 2, body, font(SANS, 13), cell_w, 16)


# ---------------------------------------------------------------- strip
def draw_strip(d):
    y0 = 896
    rule(d, MARGIN, y0, W - MARGIN, width=2)
    d.text((MARGIN, y0 + 10), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    col_w = (CONTENT_W - 160) // 3
    items = [
        ("BLACK FRIDAY", "US shoppers head out as Wall Street reopens for "
         "a short session, closing at 1 p.m. ET."),
        ("EUROPE", "EU leaders meet in Brussels over the budget and "
         "further support for Ukraine."),
        ("RED SEA", "Houthis claim strikes on Saudi Red Sea ports; Riyadh "
         "says missiles aimed at the capital were intercepted."),
    ]
    x = MARGIN + 160
    for kick, text in items:
        para(d, x, y0 + 10, kick + " — " + text, font(SANS, 12), col_w - 12,
             15)
        x += col_w
    rule(d, MARGIN, 956, W - MARGIN, width=1, fill=LIGHT_RULE)


# ---------------------------------------------------------------- footer
def draw_footer(d):
    f = font(SANS, 12)
    line = ("THE WORLD  •  Friday 27 November 2026  •  Sources: Reuters, "
            "AP, CNN, UEFA  •  Drawn in code; no photographs.")
    d.text(((W - d.textlength(line, font=f)) / 2, 968), line, font=f,
           fill=MUTED)
    f2 = font(SANS, 11)
    line2 = "All events reported on 26–27 November 2026."
    d.text(((W - d.textlength(line2, font=f2)) / 2, 986), line2, font=f2,
           fill=MUTED)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_ticker(d)
    draw_lead(d)
    draw_grid(d)
    draw_strip(d)
    draw_footer(d)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
