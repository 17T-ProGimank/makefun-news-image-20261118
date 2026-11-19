#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Build-time tool only: it runs here, on this machine, to produce entry.png.
The graded program (main.ts) only copies entry.png to /output/entry.png,
so the entry needs no network, no fonts and no libraries at grade time.

Stories (all happened / first reported Wed 18 Nov 2026, any time zone;
each cross-checked in at least two of the day's briefings):
  1. APEC Shenzhen: Xi meets Putin; Trump joins them Thursday for the
     first-ever US-China-Russia trilateral. Quad leaders meet in Manila.
  2. Gulf: US jets hit an Iranian missile site on Qeshm Island; Iran
     fires drones at US bases in Kuwait and Bahrain; a tanker is hit
     in the Strait of Hormuz.
  3. Ukraine: part of the Crimean Bridge road span collapses after a
     second day of strikes; Russia confirms the damage.
  4. US Senate: Democrat Mary Peltola beats Dan Sullivan in Alaska;
     Democrats take a 56-44 majority, largest since 2009.
  5. Nvidia: record quarter, revenue $115.8bn (+103%), data-centre
     sales $107.6bn; board rules out Jensen Huang returning as CEO.
  6. Voyager 1: first human-made object one light-day from Earth,
     about 16 billion miles away (NASA JPL).
  7. Cyclone Akvan strengthens in the Bay of Bengal; landfall due
     Friday on the Andhra Pradesh coast.
Footer ticker: US loses measles-free status (26 years); Ebola in
DR Congo passes 11,000 cases; COP31 opens in Antalya; Trump
announces a Philippines trade deal.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 234)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (18, 42, 74)
NAVY_LT = (38, 74, 120)
GOLD = (180, 83, 9)
TEAL = (15, 118, 110)
GREY = (51, 51, 51)
CARD = (255, 255, 255)
BORDER = (216, 208, 188)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_gulf(d, x, y, s=84):
    d.rectangle([x, y + 52, x + s, y + 58], fill=(29, 78, 216))
    for yy in (62, 70):
        d.arc([x, y + yy, x + 26, y + yy + 12], 180, 360, fill=(29, 78, 216), width=3)
        d.arc([x + 30, y + yy, x + 56, y + yy + 12], 180, 360, fill=(29, 78, 216), width=3)
        d.arc([x + 58, y + yy, x + s, y + yy + 12], 180, 360, fill=(29, 78, 216), width=3)
    d.polygon([(x + 8, y + 52), (x + 76, y + 52), (x + 68, y + 40), (x + 16, y + 40)],
              fill=(17, 17, 17))
    d.rectangle([x + 22, y + 28, x + 34, y + 40], fill=(185, 28, 28))
    d.rectangle([x + 38, y + 28, x + 50, y + 40], fill=(180, 83, 9))
    cx, cy = x + 66, y + 16
    for dx, dy in ((0, -12), (9, -9), (12, 0), (9, 9), (0, 12), (-9, 9), (-12, 0), (-9, -9)):
        d.line([cx, cy, cx + dx, cy + dy], fill=(245, 158, 11), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(245, 158, 11))


def icon_bridge(d, x, y, s=84):
    # Two towers, a sagging cable, and a deck with its middle span dropped.
    d.rectangle([x + 8, y + 12, x + 14, y + 66], fill=(17, 17, 17))
    d.rectangle([x + 70, y + 12, x + 76, y + 66], fill=(17, 17, 17))
    d.line([x + 11, y + 14, x + 42, y + 38], fill=(17, 17, 17), width=2)
    d.line([x + 73, y + 14, x + 42, y + 38], fill=(17, 17, 17), width=2)
    d.line([x, y + 44, x + 30, y + 44], fill=(17, 17, 17), width=5)
    d.line([x + 54, y + 44, x + 84, y + 44], fill=(17, 17, 17), width=5)
    d.line([x + 30, y + 44, x + 42, y + 58], fill=(185, 28, 28), width=4)
    d.line([x + 42, y + 58, x + 54, y + 44], fill=(185, 28, 28), width=4)
    d.rectangle([x + 58, y + 62, x + 84, y + 70], fill=(29, 78, 216))
    d.rectangle([x + 58, y + 70, x + 84, y + 78], fill=(250, 204, 21))


def icon_senate(d, x, y, s=84):
    d.pieslice([x + 22, y + 6, x + 62, y + 42], 180, 360, fill=(18, 42, 74))
    d.rectangle([x + 20, y + 40, x + 64, y + 48], fill=(18, 42, 74))
    for i in range(5):
        cx = x + 24 + i * 9
        d.rectangle([cx, y + 50, cx + 5, y + 68], fill=(18, 42, 74))
    d.rectangle([x + 16, y + 68, x + 68, y + 74], fill=(18, 42, 74))
    d.rectangle([x + 40, y - 2, x + 44, y + 8], fill=(185, 28, 28))


def icon_chip(d, x, y, s=84):
    d.rectangle([x + 18, y + 22, x + 66, y + 70], fill=(17, 17, 17))
    d.rectangle([x + 30, y + 34, x + 54, y + 58], fill=(34, 197, 94))
    for i in range(4):
        xx = x + 26 + i * 12
        d.line([xx, y + 14, xx, y + 22], fill=(17, 17, 17), width=3)
        d.line([xx, y + 70, xx, y + 78], fill=(17, 17, 17), width=3)
        yy = y + 30 + i * 12
        d.line([x + 10, yy, x + 18, yy], fill=(17, 17, 17), width=3)
        d.line([x + 66, yy, x + 74, yy], fill=(17, 17, 17), width=3)
    d.line([x + 6, y + 66, x + 30, y + 42, x + 46, y + 52, x + 76, y + 14],
           fill=(185, 28, 28), width=5)
    d.polygon([(x + 76, y + 14), (x + 62, y + 14), (x + 76, y + 28)], fill=(185, 28, 28))


def icon_voyager(d, x, y, s=84):
    d.rounded_rectangle([x, y, x + s, y + s], radius=10, fill=(10, 16, 32))
    for sx, sy in ((10, 12), (26, 22), (70, 10), (62, 30), (14, 62), (74, 62), (44, 8)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.arc([x + 8, y + 14, x + 76, y + 78], 200, 340, fill=(250, 204, 21), width=2)
    d.polygon([(x + 30, y + 34), (x + 58, y + 30), (x + 50, y + 52), (x + 28, y + 52)],
              fill=(180, 83, 9))
    d.line([x + 58, y + 30, x + 70, y + 18], fill=(250, 204, 21), width=3)
    d.ellipse([x + 66, y + 12, x + 78, y + 24], outline=(250, 204, 21), width=3)


def icon_cyclone(d, x, y, s=84):
    cx, cy = x + 42, y + 38
    for r, col in ((30, (15, 118, 110)), (21, (29, 78, 216)), (12, (185, 28, 28))):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=5)
    for dx in (-24, -8, 8, 24):
        d.line([x + 42 + dx, y + 66, x + 42 + dx, y + 74], fill=(29, 78, 216), width=4)
        d.ellipse([x + 38 + dx, y + 72, x + 46 + dx, y + 80], fill=(29, 78, 216))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=4)

    # Masthead
    f_title = font(SERIF_B, 58)
    d.text((W // 2, 26), "THE WORLD TODAY", font=f_title, fill=INK, anchor="ma")
    f_date = font(SANS_B, 29)
    d.text((W // 2, 96), "WEDNESDAY,  18 NOVEMBER 2026", font=f_date,
           fill=RED, anchor="ma")
    d.line([24, 136, W - 24, 136], fill=INK, width=3)
    d.line([24, 141, W - 24, 141], fill=INK, width=1)

    # Hero: APEC / Shenzhen
    d.rectangle([24, 152, W - 24, 330], fill=NAVY)
    f_kick = font(SANS_B, 20)
    d.text((48, 166), "TOP STORY  —  APEC  •  SHENZHEN, CHINA", font=f_kick, fill=(250, 204, 21))
    f_hero = font(SERIF_B, 33)
    d.text((48, 196), "XI MEETS PUTIN IN SHENZHEN", font=f_hero, fill=(255, 255, 255))
    d.text((48, 238), "TRUMP JOINS THEM THURSDAY", font=f_hero, fill=(255, 255, 255))
    f_sub = font(SANS, 19)
    sub = wrap(d, "First-ever US–China–Russia summit; APEC opens as Quad leaders meet in Manila.", f_sub, 600)
    draw_lines(d, sub, 48, 286, f_sub, (220, 228, 240), 23)
    # Hero art: skyline + three flags
    ax, ay = 700, 168
    for bx, bh in ((0, 70), (34, 96), (72, 58), (104, 88), (140, 64), (172, 78)):
        d.rectangle([ax + bx, ay + 140 - bh, ax + bx + 28, ay + 140], fill=NAVY_LT)
        for wy in range(ay + 146 - bh, ay + 136, 14):
            d.rectangle([ax + bx + 6, wy, ax + bx + 11, wy + 6], fill=(250, 204, 21))
    d.rectangle([ax, ay + 140, ax + 308, ay + 144], fill=(250, 204, 21))
    flags = [((210, 30, 30), "CN"), ((200, 200, 200), "US"), ((255, 255, 255), "RU")]
    for i, (col, _) in enumerate(flags):
        fx = ax + 20 + i * 96
        d.rectangle([fx, ay, fx + 4, ay + 108], fill=(200, 200, 200))
        if i == 0:
            d.rectangle([fx + 4, ay + 4, fx + 64, ay + 34], fill=(222, 41, 16))
            for sx, sy in ((12, 12), (26, 10), (30, 20), (20, 26)):
                d.ellipse([fx + sx, ay + sy, fx + sx + 4, ay + sy + 4], fill=(250, 204, 21))
        elif i == 1:
            for s in range(7):
                d.rectangle([fx + 4, ay + 4 + s * 5, fx + 64, ay + 8 + s * 5],
                            fill=(185, 28, 28) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx + 4, ay + 4, fx + 28, ay + 19], fill=(18, 42, 74))
        else:
            d.rectangle([fx + 4, ay + 4, fx + 64, ay + 14], fill=(255, 255, 255))
            d.rectangle([fx + 4, ay + 14, fx + 64, ay + 24], fill=(29, 78, 216))
            d.rectangle([fx + 4, ay + 24, fx + 64, ay + 34], fill=(185, 28, 28))

    # Story cards: 2 columns x 3 rows
    cards = [
        ("GULF  •  US–IRAN", "US–IRAN CLASH IN THE GULF",
         "US jets hit a missile site on Qeshm Island; Iran fires drones at US bases "
         "in Kuwait and Bahrain. A tanker is hit in Hormuz.", icon_gulf),
        ("UKRAINE  •  WAR", "CRIMEAN BRIDGE SPAN COLLAPSES",
         "Ukraine says part of the road span fell after a second day of strikes. "
         "Russia confirms damage and vows to rebuild.", icon_bridge),
        ("USA  •  SENATE", "PELTOLA WINS ALASKA SENATE SEAT",
         "Democrat Mary Peltola beats Dan Sullivan in Alaska. Democrats take a "
         "56–44 Senate majority, their largest since 2009.", icon_senate),
        ("TECH  •  MARKETS", "NVIDIA: $115.8BN RECORD QUARTER",
         "Record quarter: revenue $115.8bn, up 103%; data-centre sales $107.6bn. "
         "The board rules out Jensen Huang returning as CEO.", icon_chip),
        ("SPACE  •  NASA", "VOYAGER 1, ONE LIGHT-DAY OUT",
         "NASA's probe is the first human-made object one light-day from Earth — "
         "about 16 billion miles from home.", icon_voyager),
        ("WEATHER  •  INDIA", "CYCLONE AKVAN HEADS FOR INDIA",
         "The storm strengthens over the Bay of Bengal and is set to hit the "
         "Andhra Pradesh coast on Friday.", icon_cyclone),
    ]
    f_ck = font(SANS_B, 17)
    f_ch = font(SERIF_B, 27)
    f_cs = font(SANS, 19)
    cw, chh, gap = 480, 182, 16
    x0, y0 = 24, 342
    for i, (kicker, head, sub, icon) in enumerate(cards):
        cx = x0 + (i % 2) * (cw + gap)
        cy = y0 + (i // 2) * (chh + 10)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=CARD, outline=BORDER, width=2)
        d.text((cx + 18, cy + 10), kicker, font=f_ck, fill=RED)
        icon(d, cx + cw - 102, cy + 10)
        lines = wrap(d, head, f_ch, 344)
        draw_lines(d, lines[:2], cx + 18, cy + 36, f_ch, INK, 31)
        slines = wrap(d, sub, f_cs, cw - 36)
        draw_lines(d, slines[:3], cx + 18, cy + 104, f_cs, GREY, 22)

    # Footer ticker
    d.line([24, 920, W - 24, 920], fill=INK, width=3)
    f_ft = font(SANS, 18)
    f_ftb = font(SANS_B, 18)
    d.text((24, 930), "ALSO TODAY — ", font=f_ftb, fill=RED)
    w0 = d.textlength("ALSO TODAY — ", font=f_ftb)
    tick = ("US loses measles-free status after 26 years  •  Ebola in DR Congo passes "
            "11,000 cases  •  COP31 opens in Antalya  •  Philippines trade deal")
    tlines = wrap(d, tick, f_ft, W - 48 - w0)
    draw_lines(d, tlines[:2], 24 + w0, 930, f_ft, INK, 22)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
