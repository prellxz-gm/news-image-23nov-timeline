#!/usr/bin/env python3
"""Draw entry.png for news-image-20261123, variant C 'Timeline + Proof'.
Own drawing code (PIL). 1024x1024 newspaper front page: timeline of Monday
23 November 2026, Asia morning -> US evening, with a PROOF column
(source + time + certainty tag) on every story. All stories from the
verified round-1 + round-2 story lists only; trap-list items appear ONLY in the
DATE CHECK box as explicitly NOT 23 November.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (255, 252, 240)
NAVY = (20, 38, 74)
RED = (176, 30, 40)
BLUE = (31, 93, 168)
AMBER = (176, 120, 0)
GREEN = (31, 120, 62)
INK = (24, 24, 24)
GREY = (90, 90, 84)
LIGHTBLUE = (205, 225, 240)
TAN = (232, 214, 170)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tag(draw, x, y, label, fill, fg=(255, 255, 255)):
    f = F(SANS_B, 13)
    w = draw.textlength(label, font=f) + 12
    draw.rounded_rectangle([x, y, x + w, y + 20], radius=4, fill=fill)
    draw.text((x + 6, y + 3), label, font=f, fill=fg)
    return w


TAG_FILL = {"CONFIRMED": NAVY, "REPORTED": BLUE, "FORECAST": AMBER, "ONGOING": GREEN}

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
M = 28  # margin

# ---------- masthead ----------
d.rectangle([0, 0, W, 10], fill=RED)
d.text((W // 2, 20), "THE WORLD IN ONE DAY", font=F(SANS_B, 20),
       fill=RED, anchor="ma")
d.text((W // 2, 46), "MONDAY 23 NOVEMBER 2026", font=F(SERIF_B, 44),
       fill=NAVY, anchor="ma")
d.text((W // 2, 96), "One day  •  Every region  •  Every story checked",
       font=F(SANS, 17), fill=GREY, anchor="ma")
d.line([M, 120, W - M, 120], fill=NAVY, width=3)
d.line([M, 125, W - M, 125], fill=RED, width=1)

# ---------- proof legend ----------
f_proof = F(SANS_B, 15)
pw = d.textlength("PROOF:", font=f_proof)
d.text((M, 134), "PROOF:", font=f_proof, fill=NAVY)
d.text((M + pw + 8, 134), "every story shows its SOURCE + TIME + CERTAINTY",
       font=F(SANS, 15), fill=INK)
lx = 560
for lab in ("CONFIRMED", "REPORTED", "FORECAST", "ONGOING"):
    lx += tag(d, lx, 132, lab, TAG_FILL[lab]) + 8

# ---------- world map strip ----------
d.text((M, 160), "WHERE IT HAPPENED", font=F(SANS_B, 16), fill=NAVY)
d.text((W - M, 160), "7 REGIONS  •  5 FIELDS", font=F(SANS_B, 15),
       fill=RED, anchor="ra")
d.rectangle([M, 182, W - M, 246], fill=LIGHTBLUE, outline=NAVY, width=2)
d.polygon([(60, 199), (150, 186), (235, 194), (225, 222), (150, 234),
           (80, 226)], fill=TAN)                       # N America
d.polygon([(185, 226), (225, 224), (235, 242), (200, 244)], fill=TAN)  # S America
d.polygon([(470, 194), (520, 186), (545, 199), (520, 214), (480, 212)], fill=TAN)  # Europe
d.polygon([(480, 216), (540, 214), (560, 239), (520, 244), (490, 234)], fill=TAN)  # Africa
d.polygon([(560, 186), (720, 182), (800, 199), (760, 229), (640, 232),
           (580, 214)], fill=TAN)                       # Asia
d.polygon([(800, 226), (845, 224), (855, 238), (815, 242)], fill=TAN)  # Australia
pins = [(150, 199, "1"), (520, 199, "2"), (640, 209, "3"), (885, 236, "4"),
        (225, 234, "5"), (140, 216, "6"), (525, 232, "7"), (820, 234, "8")]
for (x, y, n) in pins:
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x, y - 1), n, font=F(SANS_B, 12), fill=(255, 255, 255), anchor="mm")
d.text((W // 2, 252), "1 Brussels   2 Armenia   3 New Delhi   4 Wellington   5 Kourou   6 Washington   7 Addis Ababa   8 Sydney",
       font=F(SANS, 13), fill=GREY, anchor="ma")

# ---------- hero cards ----------
d.text((M, 276), "THE DAY'S THREE BIGGEST STORIES", font=F(SANS_B, 17), fill=NAVY)
heroes = [
    dict(x=M, icon="plane", kick="BELGIUM STOPS",
         head="National strike grounds ALL flights",
         body="Air traffic halted 07:00-21:00. All 429 Brussels flights cancelled, 59,500 hit.",
         src="eTurboNews / StrikeTracker", time="07:00 CET", tag="CONFIRMED"),
    dict(x=M + 326, icon="road", kick="THE TRUMP CORRIDOR OPENS",
         head="Armenia launches TRIPP on Iran's border",
         body="26-mile US-backed road & rail link joins Azerbaijan to Nakhchivan.",
         src="Fox News", time="MONDAY", tag="CONFIRMED"),
    dict(x=M + 652, icon="chart", kick="WALL ST BOUNCES",
         head="US futures rally after worst week since April 2025",
         body="S&P futures +2%, Nasdaq +2.5-3% in Asia. Last week: S&P -8.6%, Nasdaq -10%.",
         src="Reuters", time="MONDAY OPEN", tag="REPORTED"),
]
for h in heroes:
    x, y = h["x"], 300
    d.rectangle([x, y, x + 316, y + 184], fill=PAPER, outline=NAVY, width=2)
    d.rectangle([x, y, x + 316, y + 34], fill=NAVY)
    d.text((x + 10, y + 8), h["kick"], font=F(SANS_B, 14), fill=(255, 255, 255))
    # icon row: icon left, tag right
    cx, cy = x + 32, y + 60
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=RED)
    if h["icon"] == "plane":
        d.polygon([(cx - 13, cy + 2), (cx + 2, cy - 6), (cx + 15, cy - 2),
                   (cx + 2, cy + 4), (cx - 2, cy + 11), (cx - 8, cy + 4)],
                  fill=(255, 255, 255))
    elif h["icon"] == "road":
        d.polygon([(cx - 11, cy + 13), (cx - 4, cy - 13), (cx + 4, cy - 13),
                   (cx + 11, cy + 13)], fill=(255, 255, 255))
        d.line([cx, cy - 11, cx, cy + 11], fill=RED, width=3)
    else:
        d.line([(cx - 13, cy + 9), (cx - 4, cy - 2), (cx + 4, cy + 4),
                (cx + 13, cy - 11)], fill=(255, 255, 255), width=4)
        d.polygon([(cx + 13, cy - 11), (cx + 5, cy - 11), (cx + 13, cy - 3)],
                  fill=(255, 255, 255))
    tag(d, x + 316 - 108, y + 50, h["tag"], TAG_FILL[h["tag"]])
    lines = wrap(d, h["head"], F(SERIF_B, 18), 316 - 20)
    yy = y + 86
    for ln in lines[:2]:
        d.text((x + 10, yy), ln, font=F(SERIF_B, 18), fill=NAVY)
        yy += 22
    blines = wrap(d, h["body"], F(SANS, 14), 316 - 20)
    yy = y + 132
    for ln in blines[:2]:
        d.text((x + 10, yy), ln, font=F(SANS, 14), fill=INK)
        yy += 18
    d.text((x + 10, y + 168), h["src"] + "  •  " + h["time"],
           font=F(SANS_B, 12), fill=GREY)

# ---------- timeline ----------
d.text((M, 494), "THE DAY, HOUR BY HOUR  —  ASIA MORNING  ↓  TO US EVENING",
       font=F(SANS_B, 16), fill=NAVY)
d.line([M + 8, 520, M + 8, 790], fill=RED, width=3)
rows = [
    ("ASIA AM", "Asia closes split: KOSPI -3.6% to 4,696; TAIEX +2.9% to 37,085",
     "Reuters", "REPORTED"),
    ("NEW DELHI", "Nepal-India deal: 350 MW power import, new train, joint vision",
     "The Hindu", "REPORTED"),
    ("SYDNEY", "Australia PMI 46.1, fastest contraction since 2021",
     "S&P Global", "CONFIRMED"),
    ("WELLINGTON", "India v NZ Test ends in a draw: NZ 239/5 bat out Day 5",
     "ESPNcricinfo", "CONFIRMED"),
    ("KOUROU", "Ariane 6 launches 36 Amazon Leo satellites from French Guiana",
     "Arianespace", "FORECAST"),
    ("20:15 ET", "Monday Night Football: Bengals (7-2) at Washington Commanders",
     "Sports Illustrated", "FORECAST"),
]
y = 520
for (t, head, src, tg) in rows:
    d.ellipse([M - 1, y + 12, M + 17, y + 30], fill=RED, outline=(255, 255, 255), width=2)
    d.text((M + 28, y), t, font=F(SANS_B, 14), fill=RED)
    d.text((M + 28, y + 18), head, font=F(SANS_B, 17), fill=INK)
    tag(d, W - M - 108, y + 2, tg, TAG_FILL[tg])
    d.text((W - M - 112, y + 24), src, font=F(SANS, 12), fill=GREY, anchor="ra")
    y += 45
d.line([M, 794, W - M, 794], fill=NAVY, width=2)

# ---------- bottom split ----------
d.text((M, 806), "ALSO ON MONDAY", font=F(SANS_B, 16), fill=NAVY)
also = [
    "U-17 World Cup: 8 matches in Doha — FIFA",
    "CPHIA opens in Addis Ababa — Africa CDC",
    "Samia launches health plan — IPP Media",
    "COP31 fallout: 'worst COP ever' — CNN",
    "Visegrad PMs meet in Bratislava — Europe Says",
    "Earnings: Agilent, HPE, Zoom — Stockopedia",
    "Indonesia confirms 24 dead at Serang fire — Reuters",
    "Japan shut; Cambodia Water Festival — Reuters",
    "UN Palestinian Solidarity Day, NY — UN",
    "Schumer turns 76; Senate race brews — Reuters",
]
for i, item in enumerate(also):
    col = 0 if i < 5 else 1
    xx = M if col == 0 else M + 330
    y2 = 830 + (i % 5) * 25
    d.ellipse([xx, y2 + 1, xx + 16, y2 + 17], fill=NAVY)
    d.text((xx + 8, y2), str(i + 1), font=F(SANS_B, 11),
           fill=(255, 255, 255), anchor="ma")
    d.text((xx + 22, y2 + 1), item, font=F(SANS, 12), fill=INK)

# DATE CHECK (right)
bx, by = 700, 806
d.rectangle([bx, by, W - M, by + 150], fill=(255, 238, 238), outline=RED, width=2)
d.text((bx + 10, by + 8), "DATE CHECK — NOT 23 NOVEMBER", font=F(SANS_B, 14), fill=RED)
not23 = [
    "COP31 collapse — Sun 22 Nov",
    "ATP final: Alcaraz d. Zverev — 22 Nov",
    "NFL Sunday games — Sun 22 Nov (US)",
    "Verstappen wins Las Vegas GP — 22 Nov",
    "'El Chapo Isidro' captured — 20 Nov",
    "India 720/9 declared — Sun 22 Nov",
]
yy = by + 32
for item in not23:
    d.text((bx + 10, yy), "✕  " + item, font=F(SANS, 13), fill=INK)
    yy += 19

# ---------- footer ----------
d.line([M, 970, W - M, 970], fill=NAVY, width=2)
d.text((W // 2, 978), "Sources: Reuters  •  Fox News  •  The Hindu  •  ESPNcricinfo  •  FIFA  •  UN  •  Arianespace  •  Africa CDC  •  S&P Global  •  Stockopedia",
       font=F(SANS, 12), fill=GREY, anchor="ma")
d.text((W // 2, 996), "All stories happened or were first reported on Monday 23 November 2026.",
       font=F(SANS_B, 12), fill=NAVY, anchor="ma")

img.save("/home/hatch/workspace/makefun/news-image-20261123/entry-c/entry.png")
print("saved", img.size)
