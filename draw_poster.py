"""Draw the front page of THE WORLD for Friday 27 November 2026.

A single 1024x1024 newspaper poster, drawn entirely with Pillow and
the Python standard library. No photographs: every picture on the
page (storm sky, containers, missile, tanker fire, football pitches,
market chart) is drawn from rectangles, ellipses, polygons and lines.

Layout, top to bottom:
  masthead -> markets strip -> lead story (storm) -> 6-panel grid
  (trade / Korea / Egypt / sport / sport / markets) -> Also Today
  strip -> footer.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
RIGHT = W - MARGIN
CONTENT_W = RIGHT - MARGIN

PAPER = (244, 239, 228)
INK = (26, 26, 26)
RED = (160, 30, 34)
GREEN = (31, 122, 60)
DARK_BLUE = (38, 54, 78)
GOLD = (255, 214, 64)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, text, fnt, fg, bg, pad_x=8, pad_y=5):
    """Solid label chip with guaranteed padding; returns (w, h)."""
    w = int(draw.textlength(text, font=fnt)) + 2 * pad_x
    h = fnt.size + 2 * pad_y
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fg)
    return w, h


def rule(draw, y, weight=2, x0=MARGIN, x1=RIGHT):
    draw.line([(x0, y), (x1, y)], fill=INK, width=weight)


# ---------------------------------------------------------------- pictures

def lead_picture(draw, x, y, w, h):
    """Nor'easter sky over New York: storm clouds, rain, wind, a
    grounded star balloon. Labels sit in clear sky at the top."""
    draw.rectangle([x, y, x + w, y + h], fill=DARK_BLUE)
    # lighter storm band near the horizon
    draw.rectangle([x, y + h - 52, x + w, y + h], fill=(52, 66, 92))
    # dark clouds
    for cx, cy, cw, ch in [(8, 12, 92, 30), (96, 6, 110, 34), (206, 14, 88, 28),
                           (52, 38, 120, 26), (180, 44, 104, 24)]:
        draw.ellipse([x + cx, y + cy, x + cx + cw, y + cy + ch], fill=(24, 34, 56))
    # wind arrow, top left, clear of the text below it
    draw.line([(x + 14, y + 22), (x + 66, y + 22)], fill=(255, 255, 255), width=5)
    draw.polygon([(x + 66, y + 12), (x + 66, y + 32), (x + 86, y + 22)],
                 fill=(255, 255, 255))
    # labels, stacked with breathing room under the arrow
    f_label = font(SANS_BOLD, 15)
    draw.text((x + 12, y + 38), "GUSTS TO 65 MPH", font=f_label, fill=(255, 255, 255))
    draw.text((x + 12, y + 56), "100TH PARADE GROUNDED", font=f_label, fill=GOLD)
    # rain
    for rx, ry in [(20, 96), (52, 108), (88, 96), (124, 110), (160, 96),
                   (196, 108), (232, 96), (268, 110), (292, 98),
                   (36, 128), (72, 138), (108, 128), (144, 140),
                   (180, 128), (216, 138), (252, 128), (286, 138)]:
        draw.line([(x + rx, y + ry), (x + rx - 5, y + ry + 14)],
                  fill=(170, 190, 220), width=2)
    # red balloon with a yellow star, low in the frame, clear of the labels
    bx, by, br = x + w // 2 - 6, y + 126, 38
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(200, 40, 48))
    draw.ellipse([bx - br, by - br, bx + br, by + br], outline=(140, 20, 26), width=2)
    star = [(bx, by - 26), (bx + 8, by - 7), (bx + 27, by - 6), (bx + 13, by + 7),
            (bx + 18, by + 25), (bx, by + 14), (bx - 18, by + 25),
            (bx - 13, by + 7), (bx - 27, by - 6), (bx - 8, by - 7)]
    draw.polygon(star, fill=GOLD)
    # tethers down to the street
    for tx in (bx - 30, bx - 10, bx + 12, bx + 30):
        draw.line([(tx, by + 36), (tx - 4, y + h - 18)], fill=(220, 220, 220), width=2)
    # street with sandbags
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=(46, 44, 40))
    for sx in (24, 78, 132, 186, 240):
        draw.ellipse([x + sx, y + h - 15, x + sx + 34, y + h - 4], fill=(150, 132, 96))


def trade_picture(draw, x, y, w, h):
    """Stacked shipping containers and a tariff notice."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 224, 200))
    # container stacks, left two-thirds
    stacks = [((16, 34), (150, 60), (31, 122, 60)),
              ((16, 62), (150, 88), (160, 30, 34)),
              ((158, 62), (208, 88), (38, 54, 78))]
    for (x0, y0), (x1, y1), col in stacks:
        draw.rectangle([x + x0, y + y0, x + x1, y + y1], fill=col)
        for vx in range(x0 + 14, x1, 14):
            draw.line([(x + vx, y + y0), (x + vx, y + y1)], fill=(90, 90, 90),
                      width=1)
    # tariff notice, right side; box sized so the text fits inside
    bx0, by0, bx1, by1 = x + w - 96, y + 10, x + w - 8, y + h - 10
    draw.rectangle([bx0, by0, bx1, by1], fill=(255, 255, 255), outline=INK, width=2)
    f_t = font(SANS_BOLD, 12)
    f_p = font(SANS_BOLD, 10)
    draw.text((bx0 + 8, by0 + 8), "TARIFF", font=f_t, fill=RED)
    draw.line([(bx0 + 8, by0 + 30), (bx1 - 8, by0 + 30)], fill=INK, width=1)
    draw.line([(bx0 + 8, by0 + 40), (bx1 - 8, by0 + 40)], fill=(120, 120, 120), width=1)
    draw.line([(bx0 + 8, by0 + 50), (bx1 - 8, by0 + 50)], fill=(120, 120, 120), width=1)
    draw.text((bx0 + 8, by0 + 58), "14 PARTNERS", font=f_p, fill=INK)


def korea_picture(draw, x, y, w, h):
    """Night launch site: missile on its pad between two consoles."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 22, 44))
    for sx, sy in [(24, 30), (70, 34), (120, 30), (220, 30), (272, 32), (300, 34)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    f_label = font(SANS_BOLD, 12)
    draw.text((x + 10, y + 8), "TACTICAL WEAPONS PUSH", font=f_label, fill=GOLD)
    # missile
    mx = x + w // 2
    draw.polygon([(mx, y + 30), (mx - 11, y + 52), (mx + 11, y + 52)], fill=(200, 200, 205))
    draw.rectangle([mx - 11, y + 52, mx + 11, y + 82], fill=(200, 200, 205))
    draw.rectangle([mx - 18, y + 76, mx + 18, y + 84], fill=(120, 120, 128))
    draw.polygon([(mx - 6, y + 84), (mx + 6, y + 84), (mx, y + 90)], fill=(255, 170, 40))
    # consoles with yellow lights
    for cx in (14, w - 78):
        draw.rectangle([x + cx, y + 62, x + cx + 64, y + 88], fill=(44, 56, 84),
                       outline=(140, 150, 180), width=1)
        for lx in (cx + 10, cx + 28, cx + 46):
            draw.rectangle([x + lx, y + 72, x + lx + 8, y + 80], fill=GOLD)


def egypt_picture(draw, x, y, w, h):
    """Night highway in Giza: skyline, tanker, flames."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 22, 20))
    for bx, bw, bh in [(10, 34, 34), (52, 26, 48), (86, 40, 28), (220, 30, 42),
                       (258, 36, 30)]:
        draw.rectangle([x + bx, y + h - 34 - bh, x + bx + bw, y + h - 34],
                       fill=(52, 48, 44))
    f_label = font(SANS_BOLD, 12)
    draw.text((x + 10, y + 8), "31 KILLED \u2022 21 HURT", font=f_label,
              fill=(255, 255, 255))
    # flames over the tanker
    cx = x + w // 2
    for fx, fw, fh, col in [(-52, 30, 42, (255, 140, 30)), (-18, 36, 54, (255, 180, 40)),
                            (18, 28, 40, (255, 120, 20)), (44, 20, 28, (255, 190, 60))]:
        draw.polygon([(cx + fx, y + h - 34), (cx + fx + fw // 2, y + h - 34 - fh),
                      (cx + fx + fw, y + h - 34)], fill=col)
    # tanker body and wheels
    draw.rounded_rectangle([cx - 74, y + h - 40, cx + 74, y + h - 20],
                           radius=8, fill=(150, 150, 155))
    draw.rectangle([cx + 74, y + h - 34, cx + 92, y + h - 20], fill=(120, 120, 125))
    for wx in (cx - 56, cx - 8, cx + 44):
        draw.ellipse([wx, y + h - 22, wx + 18, y + h - 4], fill=(10, 10, 10))
    draw.line([(x, y + h - 2), (x + w, y + h - 2)], fill=(255, 214, 64), width=2)


def pitch(draw, x, y, w, h):
    """A green football pitch: stripes, halfway line, centre circle."""
    draw.rectangle([x, y, x + w, y + h], fill=(46, 130, 62))
    stripe_w = w // 6
    for i in range(0, 6, 2):
        draw.rectangle([x + i * stripe_w, y, x + (i + 1) * stripe_w, y + h],
                       fill=(54, 142, 70))
    draw.line([(x + w // 2, y), (x + w // 2, y + h)], fill=(255, 255, 255), width=2)
    draw.ellipse([x + w // 2 - 26, y + h // 2 - 26, x + w // 2 + 26, y + h // 2 + 26],
                 outline=(255, 255, 255), width=2)


def plzen_picture(draw, x, y, w, h):
    pitch(draw, x, y, w, h)
    # goal box, right edge
    draw.rectangle([x + w - 34, y + 22, x + w, y + h - 22], outline=(255, 255, 255),
                   width=2)
    # ball on the spot
    bx, by = x + 78, y + h // 2 + 8
    draw.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=(255, 255, 255),
                 outline=INK, width=2)
    draw.polygon([(bx, by - 6), (bx + 5, by - 2), (bx + 3, by + 5),
                  (bx - 3, by + 5), (bx - 5, by - 2)], fill=INK)
    chip(draw, x + 10, y + 10, "PLZEN 4-0 BENFICA", font(SANS_BOLD, 13),
         fg=GOLD, bg=(0, 0, 0))


def bears_picture(draw, x, y, w, h):
    pitch(draw, x, y, w, h)
    # yard lines
    for lx in (70, 140, 210, 280):
        draw.line([(x + lx, y + 8), (x + lx, y + h - 8)], fill=(255, 255, 255), width=1)
    # football, left of centre
    fx, fy = x + 108, y + h // 2 + 6
    draw.ellipse([fx - 24, fy - 13, fx + 24, fy + 13], fill=(122, 72, 32),
                 outline=(255, 255, 255), width=2)
    draw.line([(fx - 12, fy), (fx + 12, fy)], fill=(255, 255, 255), width=2)
    for lx in (-9, -3, 3, 9):
        draw.line([(fx + lx, fy - 5), (fx + lx, fy + 5)], fill=(255, 255, 255), width=1)
    # game clock, right side
    cx, cy = x + w - 52, y + h // 2
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(255, 255, 255),
                 outline=INK, width=2)
    draw.line([(cx, cy), (cx, cy - 15)], fill=INK, width=2)
    draw.line([(cx, cy), (cx + 11, cy)], fill=INK, width=2)
    # goalpost, far right edge
    draw.line([(x + w - 8, y + 16), (x + w - 8, y + h - 16)], fill=GOLD, width=4)
    draw.line([(x + w - 8, y + 16), (x + w - 26, y + 16)], fill=GOLD, width=4)
    chip(draw, x + 10, y + 10, "BEARS 39-35 LIONS", font(SANS_BOLD, 13),
         fg=GOLD, bg=(0, 0, 0))
    draw.text((x + 10, y + h - 24), "3 SECONDS LEFT", font=font(SANS_BOLD, 12),
              fill=GOLD)


def nvidia_picture(draw, x, y, w, h):
    """CreditWatch chart: pale board, red falling arrow, NVDA chip,
    rating label at the top and the price clear at the bottom."""
    draw.rectangle([x, y, x + w, y + h], fill=(228, 240, 228))
    draw.line([(x, y + h - 26), (x + w, y + h - 26)], fill=(180, 200, 180), width=1)
    f_label = font(SANS_BOLD, 12)
    draw.text((x + 10, y + 9), "S&P: CREDITWATCH", font=f_label, fill=RED)
    # red falling arrow, top right, clear of the label
    draw.line([(x + 196, y + 14), (x + 296, y + 52)], fill=(200, 30, 36), width=6)
    draw.polygon([(x + 296, y + 52), (x + 272, y + 46), (x + 290, y + 66)],
                 fill=(200, 30, 36))
    # NVDA chip, centre, clear of the arrow and the price line
    chip(draw, x + 176, y + 58, "NVDA", font(SANS_BOLD, 16),
         fg=(255, 255, 255), bg=(30, 40, 30), pad_x=16, pad_y=8)
    draw.text((x + 10, y + h - 22), "$149.30  \u2022  -3.9%",
              font=font(SANS_BOLD, 13), fill=INK)


# ---------------------------------------------------------------- page

PANELS = [
    ("TRADE", "PARTNERS HIT BACK AT TRUMP'S NEW TARIFFS",
     "China warns it could lift tariffs to 40% if talks fail. The EU and "
     "Japan protest the plan; a hearing is set for 25 Jan.", trade_picture),
    ("KOREA", "KIM ORDERS MORE TACTICAL NUCLEAR WEAPONS",
     "Kim Jong Un tours nuclear sites and orders wider deployment of "
     "tactical weapons.", korea_picture),
    ("EGYPT", "31 KILLED IN CAIRO FUEL TANKER FIRE",
     "A tanker overturned on the Ring Road in Giza, setting 27 vehicles "
     "ablaze. At least 31 people died and 21 were injured.", egypt_picture),
    ("SPORT", "PLZEN THRASH BENFICA 4-0 IN EUROPE",
     "Europa League: Plzen stun unbeaten Benfica; Milan come from 2-0 down "
     "to win 4-2 at Olympiacos; Bournemouth stay perfect.", plzen_picture),
    ("SPORT", "BEARS STUN LIONS IN THANKSGIVING THRILLER",
     "Caleb Williams finds Rome Odunze with 3 seconds left; Chicago win "
     "39-35 and take first place in the NFC North.", bears_picture),
    ("MARKETS", "NVIDIA PUT ON CREDITWATCH BY S&P",
     "S&P puts Nvidia on CreditWatch negative; shares fell 3.9% to $149.30 "
     "as scrutiny of Jensen Huang grows in Washington.", nvidia_picture),
]

ALSO_TODAY = [
    ("BLACK FRIDAY \u2014 ", "US shoppers head out as Wall Street reopens "
     "for a short session, closing at 1 p.m. ET."),
    ("EUROPE \u2014 ", "EU leaders meet in Brussels over the budget and "
     "further support for Ukraine."),
    ("RED SEA \u2014 ", "Houthis claim strikes on Saudi Red Sea ports; "
     "Riyadh says missiles aimed at the capital were intercepted."),
]


def draw_poster():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- top meta line
    f_meta = font(SANS, 13)
    f_date = font(SERIF_BOLD, 20)
    draw.text((MARGIN, 26), "No. 332", font=f_meta, fill=INK)
    date_text = "FRIDAY, 27 NOVEMBER 2026"
    draw.text(((W - text_w(draw, date_text, f_date)) / 2, 22), date_text,
              font=f_date, fill=INK)
    price_text = "PRICE: ONE DAY'S NEWS"
    draw.text((RIGHT - text_w(draw, price_text, f_meta), 26), price_text,
              font=f_meta, fill=INK)

    # ---- masthead, scaled to fit the page width
    f_mast = font(SERIF_BOLD, 124)
    mast = "THE WORLD"
    while text_w(draw, mast, f_mast) > CONTENT_W and f_mast.size > 60:
        f_mast = font(SERIF_BOLD, f_mast.size - 4)
    draw.text(((W - text_w(draw, mast, f_mast)) / 2, 46), mast,
              font=f_mast, fill=INK)

    # ---- tagline
    f_tag = font(SANS, 15)
    tag = "THE DAY'S NEWS  \u2022  FROM EVERY CORNER OF THE GLOBE"
    draw.text(((W - text_w(draw, tag, f_tag)) / 2, 164), tag, font=f_tag, fill=INK)

    # ---- double rule under the masthead
    rule(draw, 184, weight=3)
    rule(draw, 189, weight=1)

    # ---- markets strip
    f_strip = font(SANS_BOLD, 15)
    f_strip_r = font(SANS, 15)
    y = 197
    draw.text((MARGIN, y), "MARKETS \u2014 THURSDAY", font=f_strip, fill=RED)
    sx = MARGIN + int(text_w(draw, "MARKETS \u2014 THURSDAY", f_strip)) + 26
    segments = [("EU futures ", f_strip_r, INK), ("+1.4\u20132.2%", f_strip, GREEN),
                ("    Asia ", f_strip_r, INK), ("higher", f_strip, GREEN),
                ("    US markets ", f_strip_r, INK), ("shut", f_strip, RED),
                ("    Black Friday ", f_strip_r, INK),
                ("short session", f_strip, INK)]
    for text, fnt, col in segments:
        draw.text((sx, y), text, font=fnt, fill=col)
        sx += int(text_w(draw, text, fnt))
    rule(draw, 222, weight=1)

    # ---- lead story
    lx, ly, lw, lh = MARGIN, 232, 304, 188
    lead_picture(draw, lx, ly, lw, lh)
    tx = lx + lw + 16
    tw = RIGHT - tx
    f_kick = font(SANS_BOLD, 15)
    draw.text((tx, ly), "LEAD STORY \u2014 THANKSGIVING DAY", font=f_kick, fill=RED)
    f_head = font(SERIF_BOLD, 36)
    y = draw_lines(draw, tx, ly + 24,
                   ["STORM GROUNDS", "THE PARADE"], f_head, leading=38)
    f_body = font(SERIF, 15)
    body = ("Macy's postpones its 100th Thanksgiving Day Parade \u2014 the "
            "first weather halt in a century \u2014 as a nor'easter bears "
            "down on New York with gusts to 65 mph. The parade moves to "
            "Saturday, 8:30 a.m. ET.")
    y = draw_lines(draw, tx, y + 6, wrap(draw, body, f_body, tw), f_body,
                   leading=19)
    f_note = font(SERIF_ITALIC, 13)
    note = ("Balloons must be grounded when gusts pass 34 mph; high wind "
            "and coastal flood warnings are in force. The parade was last "
            "halted in 1942\u201344, in wartime.")
    draw_lines(draw, tx, y + 4, wrap(draw, note, f_note, tw), f_note, leading=17)

    rule(draw, 438, weight=1)

    # ---- six-panel grid, two rows of three
    col_w = 312
    col_x = [MARGIN, MARGIN + col_w + 16, MARGIN + 2 * (col_w + 16)]
    row_y = [448, 688]
    pic_h = 92
    f_ckick = font(SANS_BOLD, 13)
    f_chead = font(SERIF_BOLD, 21)
    f_cbody = font(SERIF, 14)
    for i, (kicker, headline, body_text, painter) in enumerate(PANELS):
        cx = col_x[i % 3]
        cy = row_y[i // 3]
        painter(draw, cx, cy, col_w, pic_h)
        draw.rectangle([cx, cy, cx + col_w, cy + pic_h], outline=INK, width=1)
        draw.text((cx, cy + pic_h + 8), kicker, font=f_ckick, fill=RED)
        head_lines = wrap(draw, headline, f_chead, col_w)
        draw_lines(draw, cx, cy + pic_h + 26, head_lines, f_chead, leading=22)
        draw_lines(draw, cx, cy + pic_h + 26 + 3 * 22,
                   wrap(draw, body_text, f_cbody, col_w), f_cbody, leading=17)

    # ---- Also Today strip
    rule(draw, 928, weight=2)
    f_also = font(SANS_BOLD, 14)
    draw.text((MARGIN, 936), "ALSO TODAY", font=f_also, fill=RED)
    f_ab = font(SANS_BOLD, 13)
    f_ar = font(SANS, 13)
    also_x = [172, 478, 742]
    also_w = [274, 250, 254]
    for (bold_part, rest), ax, aw in zip(ALSO_TODAY, also_x, also_w):
        full = bold_part + rest
        lines = wrap(draw, full, f_ar, aw)
        yy = 936
        for li, line in enumerate(lines):
            if li == 0 and line.startswith(bold_part.strip()):
                draw.text((ax, yy), bold_part.strip(), font=f_ab, fill=INK)
                rest_line = line[len(bold_part.strip()):].lstrip()
                draw.text((ax + text_w(draw, bold_part.strip(), f_ab) + 4, yy),
                          rest_line, font=f_ar, fill=INK)
            else:
                draw.text((ax, yy), line, font=f_ar, fill=INK)
            yy += 16
    rule(draw, 987, weight=1)

    # ---- footer
    f_foot = font(SANS, 12)
    foot1 = ("THE WORLD  \u2022  Friday 27 November 2026  \u2022  Sources: "
             "Reuters, AP, CNN, UEFA  \u2022  Drawn in code; no photographs.")
    draw.text(((W - text_w(draw, foot1, f_foot)) / 2, 993), foot1,
              font=f_foot, fill=(90, 90, 90))
    foot2 = "All events reported on 26\u201327 November 2026."
    draw.text(((W - text_w(draw, foot2, f_foot)) / 2, 1008), foot2,
              font=f_foot, fill=(90, 90, 90))

    return img


if __name__ == "__main__":
    poster = draw_poster()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    poster.save(out, "PNG")
    print("saved", out, poster.size)
