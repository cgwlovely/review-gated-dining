"""Render Brisbane dining maps (OSM tiles + numbered pins).

Same projection/tile approach as build_maps.py, but for point sets rather than
routes. Two outputs: a metro overview and an inner-city detail map.
Coordinates were geocoded from each venue's own published street address
(Nominatim, 2026-09-28); see research/brisbane-dining.md for the addresses.
"""
import os, math, io, urllib.request
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs/assets/maps')
os.makedirs(OUT, exist_ok=True)

# (number, name, lat, lon) — numbering matches the table in research/brisbane-dining.md
VENUES = [
    (1,  'Exhibition',        -27.46998, 153.02894),
    (2,  'Longtime Dining',   -27.46828, 153.02609),
    (3,  'Longwang',          -27.46987, 153.02799),
    (4,  'Oh Boy, Bok Choy!', -27.41111, 153.01966),
    (5,  'Little Black Pug',  -27.53400, 153.07527),
    (6,  'Short Grain',       -27.45946, 153.03479),
    (7,  'Farm House',        -27.40793, 153.03168),
    (8,  '1889 Enoteca',      -27.48685, 153.03658),
    (9,  'NAÏM',              -27.45793, 152.99425),
    (10, 'hôntô',             -27.45602, 153.03446),
    (11, 'Beccofino',         -27.45590, 153.04976),
    (12, "Rothwell's",        -27.46772, 153.02669),
    (13, 'Smoked Paprika',    -27.46585, 152.99717),
    (14, 'Montrachet',        -27.45212, 153.03339),
    (15, 'Naldham House',     -27.47052, 153.03014),
    (16, 'Unbearable Bagels', -27.45416, 153.04972),
    (17, 'Joy',               -27.45797, 153.03519),
    (18, 'The Fifty Six',     -27.47052, 153.03014),
    # added 2026-09-28 after the source-list bias was found: these five clear the
    # same gate (Google >=4.7, >=200) but never appeared in the "best restaurants" lists.
    (19, 'John Mills Himself', -27.47170, 153.02556),
    (20, 'Hashtag Burgers',    -27.46084, 153.03782),
    (21, 'Sono Portside',      -27.44047, 153.06995),
    (22, 'Vegeme',             -27.47709, 153.01335),
    (23, 'Ngon',               -27.46161, 153.00679),
]

# Budget tier: its own stated gate -- Google >=4.5 AND >=1,000 reviews, and Google's
# crowd-reported band $20-40 per person. Rating bar lowered, sample bar raised.
BUDGET = [
    ('B1', 'Julius Pizzeria', -27.47362, 153.01789),
    ('B2', 'Pawpaw Cafe',     -27.48707, 153.04099),
    ('B3', 'Andonis',         -27.45939, 153.03754),
    ('B4', 'Harajuku Gyoza',  -27.46969, 153.02568),
    ('B5', 'Cafe O-Mai',      -27.51890, 153.03126),
    ('B6', "remy's",          -27.45916, 152.99755),
    ('B7', "Ben's Burgers",   -27.45778, 153.03624),
    ('B8', 'Sushi Kotobuki',  -27.47965, 153.04423),
    ('B9', 'Eat Street',      -27.44319, 153.07923),
]

# Licensed clubs (RSL / leagues / sports). Rated as whole venues, not bistros --
# their own stated gate: Google >=4.0 AND >=500. See research/brisbane-dining.md.
CLUBS = [
    ('C1', 'Easts Leagues',      -27.49740, 153.04994),
    ('C2', 'Wynnum Manly Leagues', -27.45934, 153.16614),
    ('C3', 'Kedron-Wavell',      -27.38532, 153.03535),
    ('C4', 'Carina Leagues',     -27.49185, 153.10111),
    ('C5', 'Greenbank Services', -27.66283, 153.03581),
    ('C6', 'Broncos Club',       -27.44953, 152.99608),
    ('C7', 'The Sunny',          -27.57241, 153.07381),
    ('C8', 'Souths Sports',      -27.57655, 153.01620),
    ('C9', 'Wynnum RSL',         -27.44383, 153.16923),
    ('C10','Manly Hotel',        -27.45438, 153.18481),
]
# 15 and 18 share a building (The Fifty Six is the top floor of Naldham House).
MERGED = {15: '15·18 Naldham House / The Fifty Six'}
SKIP_ON_MAP = {18}

# Three maps: the CBD block is too tight to label at inner-city zoom, so it gets its own.
INNER = {6, 10, 11, 14, 16, 17, 20, 21}
CBD = {1, 2, 3, 12, 15, 19}

UA = 'cairns-travel-agent map renderer/1.0'


def fetch(url, timeout=25):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout).read()


def merc(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n * 256
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n * 256
    return x, y


def make(name, venues, W, H, title):
    pts = [(v[2], v[3]) for v in venues]
    latmin, latmax = min(p[0] for p in pts), max(p[0] for p in pts)
    lonmin, lonmax = min(p[1] for p in pts), max(p[1] for p in pts)
    latpad = max(.0022, (latmax - latmin) * .22)
    lonpad = max(.0022, (lonmax - lonmin) * .22)
    latmin -= latpad; latmax += latpad; lonmin -= lonpad; lonmax += lonpad
    for z in range(17, 8, -1):
        ax, ay = merc(latmax, lonmin, z); bx, by = merc(latmin, lonmax, z)
        if bx - ax <= W * 1.05 and by - ay <= H * 1.05:
            break
    ax, ay = merc(latmax, lonmin, z); bx, by = merc(latmin, lonmax, z)
    left = (ax + bx) / 2 - W / 2; top = (ay + by) / 2 - H / 2
    canvas = Image.new('RGB', (W, H), '#e9f3ef')
    for tx in range(int(left // 256), int((left + W) // 256) + 1):
        for ty in range(int(top // 256), int((top + H) // 256) + 1):
            try:
                tile = Image.open(io.BytesIO(fetch(
                    f'https://tile.openstreetmap.org/{z}/{tx}/{ty}.png'))).convert('RGB')
                canvas.paste(tile, (round(tx * 256 - left), round(ty * 256 - top)))
            except Exception:
                pass
    d = ImageDraw.Draw(canvas, 'RGBA')
    big = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 22)
    small = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 17)
    tiny = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 15)

    def xy(lat, lon):
        x, y = merc(lat, lon, z)
        return round(x - left), round(y - top)

    placed = []  # label boxes, for collision avoidance

    def free(box):
        return all(not (box[0] < b[2] and b[0] < box[2] and box[1] < b[3] and b[1] < box[3])
                   for b in placed)

    # draw pins first so labels sit on top
    coords = {}
    for num, label, lat, lon in venues:
        if num in SKIP_ON_MAP:
            continue
        coords[num] = xy(lat, lon)
        x, y = coords[num]
        d.ellipse((x - (17 if len(str(num)) > 2 else 14), y - 14,
                   x + (17 if len(str(num)) > 2 else 14), y + 14), fill=(24, 78, 119, 255),
                  outline=(255, 255, 255, 255), width=3)
        s = str(num)
        bb = d.textbbox((0, 0), s, font=small)
        d.text((x - (bb[2] - bb[0]) / 2, y - (bb[3] - bb[1]) / 2 - 2), s, font=small,
               fill=(255, 255, 255, 255))
        placed.append((x - 15, y - 15, x + 15, y + 15))

    for num, label, lat, lon in venues:
        if num in SKIP_ON_MAP:
            continue
        text = MERGED.get(num, f'{num} {label}')
        x, y = coords[num]
        bb = d.textbbox((0, 0), text, font=tiny)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        cands = []
        for r in (18, 46, 78, 116, 160):
            cands += [(r, -8), (-tw - r, -8), (r, -30 - r / 4), (-tw - r, -30 - r / 4),
                      (r, 14 + r / 4), (-tw - r, 14 + r / 4),
                      (-tw / 2, -26 - r), (-tw / 2, 12 + r)]
        for dx, dy in cands:
            lx = max(4, min(W - tw - 8, x + dx)); ly = max(4, min(H - th - 10, y + dy))
            box = (lx - 5, ly - 4, lx + tw + 5, ly + th + 6)
            if free(box):
                break
        # leader line when the label had to be pushed away from its pin
        cxl = (box[0] + box[2]) / 2; cyl = (box[1] + box[3]) / 2
        if (cxl - x) ** 2 + (cyl - y) ** 2 > 70 ** 2:
            d.line((x, y, max(box[0], min(x, box[2])), max(box[1], min(y, box[3]))),
                   fill=(24, 78, 119, 150), width=2)
        d.rounded_rectangle(box, radius=5, fill=(255, 255, 255, 236),
                            outline=(24, 78, 119, 110), width=1)
        d.text((lx, ly), text, font=tiny, fill=(24, 60, 58, 255))
        placed.append(box)

    tb = d.textbbox((0, 0), title, font=big)
    d.rounded_rectangle((10, 10, 26 + tb[2] - tb[0], 22 + tb[3] - tb[1] + 6), radius=6,
                        fill=(255, 255, 255, 230))
    d.text((18, 16), title, font=big, fill=(24, 78, 119, 255))
    d.rounded_rectangle((8, H - 34, 430, H - 8), radius=5, fill=(255, 255, 255, 225))
    d.text((16, H - 31), f'© OpenStreetMap contributors  |  zoom {z}', font=small,
           fill=(60, 70, 70, 255))
    canvas.save(os.path.join(OUT, f'{name}.png'), quality=92)
    print(name, 'zoom', z, len([v for v in venues if v[0] not in SKIP_ON_MAP]), 'pins')


make('brisbane-dining-metro', VENUES, 1400, 1150,
     '布里斯班过闸门餐厅 · 全域（1–23）')
make('brisbane-dining-budget', BUDGET, 1400, 1000,
     '平价档 B1–B9 · Google ≥4.5 且 ≥1,000 条 · 人均 $20–40')
make('brisbane-dining-clubs', CLUBS, 1400, 1050,
     '俱乐部与会员价 C1–C10 · 另一套闸门：Google ≥4.0 且 ≥500')
make('brisbane-dining-inner', [v for v in VENUES if v[0] in INNER], 1400, 900,
     'Fortitude Valley · Teneriffe · Bowen Hills 放大')
make('brisbane-dining-cbd', [v for v in VENUES if v[0] in CBD or v[0] == 18], 1400, 900,
     'CBD 放大 · 步行 10 分钟内的五家')
