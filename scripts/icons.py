"""Original button icons for the Stream Deck profiles.

Every glyph here is drawn from basic shapes (lines, circles, polygons). Nothing is copied or
traced from Dyson Sphere Program's artwork. Background colour = which build bar or group the
button belongs to.

Which icon each button gets (group colour, glyph, tier badge) is set in data/commands.toml.
Run via `python scripts/build_all.py`.
"""
import math
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "streamdeck" / "icons"
SIZE = 288                      # Stream Deck scales this down to the key
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
INK = (240, 244, 248)
W = 12                          # standard stroke width

# Group colours: (background, accent)
GROUPS = {
    "power": ((92, 66, 10), (255, 196, 61)),
    "collect": ((86, 44, 18), (240, 140, 70)),
    "logistics": ((16, 52, 92), (90, 170, 245)),
    "storage": ((12, 70, 64), (70, 210, 190)),
    "production": ((58, 36, 92), (180, 140, 240)),
    "research": ((28, 38, 100), (130, 150, 255)),
    "foundation": ((48, 64, 40), (160, 200, 120)),
    "defence": ((96, 22, 22), (255, 110, 100)),
    "action": ((38, 48, 56), (160, 190, 210)),
    "panel": ((10, 64, 70), (80, 210, 220)),
    "nav": ((24, 28, 32), (200, 200, 200)),
}

# Page-switch buttons aren't commands, so their icons are defined here.
NAV_ICONS = {"Prev": ("nav", "prev", None), "Next": ("nav", "next", None)}


def icon_specs(entries):
    """label -> (group, glyph, tier) for every Stream Deck button."""
    specs = dict(NAV_ICONS)
    for e in entries:
        d = e.get("deck")
        if d:
            specs[d["label"]] = (d["group"], d["glyph"], d.get("tier"))
    return specs


C = SIZE // 2           # glyph centre x
GY = 112                # glyph centre y


def line(d, pts, w=W, fill=INK):
    d.line(pts, fill=fill, width=w, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=fill)


def circle(d, x, y, r, w=W, fill=None, outline=INK):
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=outline, width=w)


def star_points(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def glyph(d, name, acc):
    x, y = C, GY
    if name == "tesla":
        line(d, [(x - 40, y + 70), (x, y - 60), (x + 40, y + 70)])
        line(d, [(x - 26, y + 25), (x + 26, y + 25)])
        line(d, [(x - 14, y - 15), (x + 14, y - 15)])
        circle(d, x, y - 66, 12, fill=acc, outline=acc)
    elif name == "wireless":
        line(d, [(x, y + 70), (x, y - 10)])
        circle(d, x, y - 20, 10, fill=INK)
        for r in (35, 60):
            d.arc([x - r, y - 20 - r, x + r, y - 20 + r], 210, 330, fill=acc, width=W)
    elif name == "substation":
        line(d, [(x - 35, y + 70), (x, y - 5), (x + 35, y + 70)])
        circle(d, x, y - 35, 32, outline=acc, w=10)
        circle(d, x, y - 35, 10, fill=INK)
    elif name == "fusion":
        circle(d, x, y, 68)
        circle(d, x, y, 30, fill=acc, outline=acc)
        for a in range(0, 360, 45):
            r = math.radians(a)
            line(d, [(x + 40 * math.cos(r), y + 40 * math.sin(r)), (x + 55 * math.cos(r), y + 55 * math.sin(r))], w=8, fill=acc)
    elif name == "battery":
        d.rounded_rectangle([x - 40, y - 60, x + 40, y + 70], 10, outline=INK, width=W)
        d.rectangle([x - 16, y - 76, x + 16, y - 60], fill=INK)
        for i in range(3):
            d.rectangle([x - 24, y + 40 - i * 32, x + 24, y + 56 - i * 32], fill=acc)
    elif name == "wind":
        line(d, [(x, y + 75), (x, y - 10)])
        for a in (-90, 30, 150):
            r = math.radians(a)
            line(d, [(x, y - 10), (x + 70 * math.cos(r), y - 10 + 70 * math.sin(r))], w=14, fill=acc)
        circle(d, x, y - 10, 10, fill=INK)
    elif name == "flame":
        d.polygon([(x, y - 75), (x + 45, y + 5), (x + 35, y + 60), (x - 35, y + 60), (x - 45, y + 5)], fill=acc)
        d.polygon([(x, y - 20), (x + 20, y + 25), (x, y + 55), (x - 20, y + 25)], fill=INK)
    elif name == "solar":
        d.polygon([(x - 70, y + 50), (x + 70, y + 50), (x + 45, y - 40), (x - 45, y - 40)], outline=INK, width=W)
        line(d, [(x - 58, y + 5), (x + 58, y + 5)], w=6, fill=acc)
        line(d, [(x, y - 40), (x, y + 50)], w=6, fill=acc)
        line(d, [(x, y + 50), (x, y + 75)])
    elif name == "geo":
        for dx in (-40, 0, 40):                     # rising steam: two arcs make an S-curve
            d.arc([x + dx - 14, y - 70, x + dx + 14, y - 30], 90, 270, fill=acc, width=9)
            d.arc([x + dx - 14, y - 30, x + dx + 14, y + 10], 270, 90, fill=acc, width=9)
        line(d, [(x - 75, y + 35), (x + 75, y + 35)])
        line(d, [(x - 55, y + 62), (x + 55, y + 62)], w=8, fill=acc)
    elif name == "pick":
        line(d, [(x - 45, y + 65), (x + 30, y - 45)])
        d.arc([x - 60, y - 85, x + 80, y + 25], 200, 340, fill=acc, width=16)
    elif name in ("drop", "oil"):
        d.polygon([(x, y - 70), (x + 45, y + 15), (x - 45, y + 15)], fill=acc if name == "drop" else INK)
        d.ellipse([x - 45, y - 25, x + 45, y + 65], fill=acc if name == "drop" else INK)
        if name == "oil":
            d.ellipse([x - 15, y + 5, x + 15, y + 35], fill=acc)
    elif name == "belt":
        d.rounded_rectangle([x - 80, y - 25, x + 80, y + 25], 25, outline=INK, width=W)
        for dx in (-40, 0, 40):
            line(d, [(x + dx - 12, y - 12), (x + dx + 6, y), (x + dx - 12, y + 12)], w=8, fill=acc)
    elif name == "sorter":
        line(d, [(x - 60, y + 60), (x + 60, y + 60)])
        line(d, [(x - 30, y + 60), (x - 10, y - 10), (x + 40, y - 40)])
        line(d, [(x + 40, y - 40), (x + 20, y - 60)], fill=acc)
        line(d, [(x + 40, y - 40), (x + 60, y - 20)], fill=acc)
    elif name == "split":
        line(d, [(x - 70, y), (x - 10, y)])
        line(d, [(x - 10, y), (x + 60, y - 50)], fill=acc)
        line(d, [(x - 10, y), (x + 60, y + 50)], fill=acc)
        line(d, [(x - 10, y), (x + 70, y)])
    elif name == "gauge":
        d.arc([x - 70, y - 60, x + 70, y + 80], 180, 360, fill=INK, width=W)
        line(d, [(x, y + 10), (x + 40, y - 30)], fill=acc)
        circle(d, x, y + 10, 10, fill=INK)
    elif name == "spray":
        d.rounded_rectangle([x - 70, y - 10, x - 10, y + 60], 8, outline=INK, width=W)
        line(d, [(x - 10, y + 10), (x + 15, y + 10)])
        for dy in (-25, 10, 45):
            circle(d, x + 45, y + dy, 7, fill=acc, outline=acc)
        circle(d, x + 70, y - 5, 6, fill=acc, outline=acc)
        circle(d, x + 70, y + 30, 6, fill=acc, outline=acc)
    elif name == "distrib":
        d.rounded_rectangle([x - 45, y - 5, x + 45, y + 65], 10, outline=INK, width=W)
        line(d, [(x, y - 5), (x, y - 40)], w=8)
        d.ellipse([x - 55, y - 62, x + 55, y - 38], outline=acc, width=8)
        line(d, [(x - 20, y + 30), (x + 20, y + 30)], w=8, fill=acc)
    elif name == "piler":
        for i in range(3):
            d.rounded_rectangle([x - 45 + i * 6, y + 30 - i * 38, x + 45 + i * 6, y + 62 - i * 38], 8,
                                fill=acc if i == 2 else None, outline=INK, width=9)
        line(d, [(x - 80, y + 75), (x + 80, y + 75)], w=8)
    elif name == "station":
        d.polygon([(x - 30, y + 70), (x - 15, y - 30), (x + 15, y - 30), (x + 30, y + 70)], outline=INK, width=W)
        d.ellipse([x - 70, y - 50, x + 70, y - 10], outline=acc, width=10)
        line(d, [(x, y - 30), (x, y - 72)], w=8)
    elif name == "box":
        d.polygon([(x, y - 70), (x + 70, y - 35), (x, y), (x - 70, y - 35)], outline=INK, width=W)
        line(d, [(x - 70, y - 35), (x - 70, y + 40), (x, y + 75), (x + 70, y + 40), (x + 70, y - 35)])
        line(d, [(x, y), (x, y + 75)], fill=acc)
    elif name == "tank":
        d.rounded_rectangle([x - 50, y - 60, x + 50, y + 70], 40, outline=INK, width=W)
        d.rectangle([x - 38, y + 10, x + 38, y + 50], fill=acc)
    elif name == "furnace":
        d.rounded_rectangle([x - 65, y - 50, x + 65, y + 70], 12, outline=INK, width=W)
        d.pieslice([x - 35, y - 5, x + 35, y + 65], 180, 360, fill=acc)
        line(d, [(x + 35, y - 50), (x + 35, y - 80)])
    elif name == "gear":
        pts = star_points(x, y, 72, 52, n=8, rot=0)
        d.polygon(pts, outline=INK, width=W)
        circle(d, x, y, 22, fill=acc, outline=acc)
    elif name == "refinery":
        for dx, h in ((-45, 70), (0, 100), (45, 55)):
            d.rounded_rectangle([dx + x - 18, y + 70 - h, dx + x + 18, y + 70], 6, outline=INK, width=10)
        circle(d, x, y - 45, 10, fill=acc, outline=acc)
    elif name == "flask":
        line(d, [(x - 20, y - 70), (x - 20, y - 15), (x - 65, y + 65), (x + 65, y + 65), (x + 20, y - 15), (x + 20, y - 70)])
        line(d, [(x - 30, y - 70), (x + 30, y - 70)])
        d.polygon([(x - 50, y + 55), (x + 50, y + 55), (x + 30, y + 20), (x - 30, y + 20)], fill=acc)
    elif name == "atom":
        for a in (0, 60, 120):
            el = Image.new("L", (SIZE, SIZE), 0)
            ImageDraw.Draw(el).ellipse([x - 75, y - 28, x + 75, y + 28], outline=255, width=9)
            el = el.rotate(a, center=(x, y))
            d._image.paste(INK, mask=el)
        circle(d, x, y, 14, fill=acc, outline=acc)
    elif name == "ejector":
        d.rectangle([x - 60, y + 45, x + 60, y + 65], fill=INK)
        line(d, [(x - 20, y + 45), (x + 50, y - 55)], w=22)
        line(d, [(x - 20, y + 45), (x + 50, y - 55)], w=6, fill=acc)
        circle(d, x + 62, y - 72, 10, fill=acc, outline=acc)
    elif name == "dish":
        d.chord([x - 70, y - 75, x + 70, y + 35], 20, 200, fill=None, outline=INK, width=W)
        line(d, [(x - 10, y - 5), (x + 30, y - 45)], w=8, fill=acc)
        circle(d, x + 35, y - 50, 10, fill=acc, outline=acc)
        line(d, [(x, y + 10), (x, y + 60)])
        line(d, [(x - 40, y + 65), (x + 40, y + 65)])
    elif name == "grid":
        d.polygon([(x - 80, y + 50), (x + 80, y + 50), (x + 45, y - 40), (x - 45, y - 40)], outline=INK, width=W)
        line(d, [(x - 62, y + 5), (x + 62, y + 5)], w=7, fill=acc)
        line(d, [(x - 25, y - 40), (x - 40, y + 50)], w=7, fill=acc)
        line(d, [(x + 25, y - 40), (x + 40, y + 50)], w=7, fill=acc)
    elif name in ("turret", "cannon", "missile"):
        d.pieslice([x - 60, y - 10, x + 60, y + 110], 180, 360, fill=INK)
        d.rectangle([x - 70, y + 48, x + 70, y + 62], fill=INK)
        if name == "turret":
            line(d, [(x, y + 15), (x + 75, y - 50)], w=16, fill=acc)
        elif name == "cannon":
            line(d, [(x, y + 15), (x + 60, y - 40)], w=30, fill=acc)
        else:
            d.polygon([(x - 10, y - 35), (x + 50, y - 85), (x + 60, y - 75), (x + 10, y - 20)], fill=acc)
            line(d, [(x - 20, y - 20), (x - 40, y)], w=8, fill=acc)
    elif name == "jammer":
        line(d, [(x, y + 70), (x, y - 20)])
        for r in (30, 55):
            d.arc([x - r, y - 30 - r, x + r, y - 30 + r], 200, 340, fill=INK, width=9)
        line(d, [(x - 60, y - 70), (x + 60, y + 30)], w=12, fill=acc)
    elif name == "antenna":
        line(d, [(x - 35, y + 70), (x, y - 40), (x + 35, y + 70)])
        circle(d, x, y - 50, 12, fill=acc, outline=acc)
        for r in (30, 55):
            d.arc([x - r, y - 50 - r, x + r, y - 50 + r], 300, 60, fill=acc, width=8)
            d.arc([x - r, y - 50 - r, x + r, y - 50 + r], 120, 240, fill=acc, width=8)
    elif name == "cross":
        line(d, [(x - 50, y - 50), (x + 50, y + 50)], w=18, fill=acc)
        line(d, [(x + 50, y - 50), (x - 50, y + 50)], w=18, fill=acc)
    elif name == "up":
        d.polygon([(x, y - 70), (x + 60, y), (x - 60, y)], fill=acc)
        d.rectangle([x - 22, y, x + 22, y + 60], fill=acc)
        line(d, [(x - 60, y + 75), (x + 60, y + 75)])
    elif name == "hammer":
        line(d, [(x - 50, y + 65), (x + 20, y - 15)], w=16)
        d.polygon([(x - 5, y - 75), (x + 75, y + 5), (x + 50, y + 30), (x - 30, y - 50)], fill=acc)
    elif name == "copy":
        d.rounded_rectangle([x - 60, y - 60, x + 25, y + 35], 10, outline=INK, width=W)
        d.rounded_rectangle([x - 20, y - 20, x + 65, y + 75], 10, fill=acc)
    elif name in ("fly", "land"):
        sign = -1 if name == "fly" else 1
        for dy in (-25, 20):
            line(d, [(x - 50, y + dy - sign * 25), (x, y + dy + sign * 25), (x + 50, y + dy - sign * 25)][::1] if sign > 0
                 else [(x - 50, y + dy + 25), (x, y + dy - 25), (x + 50, y + dy + 25)], w=14, fill=acc)
        line(d, [(x - 70, y + 75), (x + 70, y + 75)] if name == "land" else [(x - 70, y + 75), (x + 70, y + 75)], w=8)
    elif name == "compass":
        circle(d, x, y, 70)
        d.polygon([(x, y - 55), (x + 20, y), (x - 20, y)], fill=acc)
        d.polygon([(x, y + 55), (x + 20, y), (x - 20, y)], fill=INK)
    elif name == "camera":
        d.rounded_rectangle([x - 75, y - 35, x + 75, y + 60], 14, outline=INK, width=W)
        d.rectangle([x - 30, y - 55, x + 30, y - 35], fill=INK)
        circle(d, x, y + 12, 30, fill=acc, outline=acc)
    elif name == "robot":
        d.rounded_rectangle([x - 55, y - 45, x + 55, y + 45], 14, outline=INK, width=W)
        circle(d, x - 22, y - 5, 11, fill=acc, outline=acc)
        circle(d, x + 22, y - 5, 11, fill=acc, outline=acc)
        line(d, [(x - 20, y + 25), (x + 20, y + 25)], w=8)
        line(d, [(x, y - 45), (x, y - 70)], w=8)
        circle(d, x, y - 75, 8, fill=acc, outline=acc)
    elif name == "bars":
        for i, h in enumerate((50, 95, 70, 125)):
            d.rectangle([x - 70 + i * 38, y + 70 - h, x - 45 + i * 38, y + 70], fill=acc if i % 2 else INK)
    elif name == "bag":
        d.rounded_rectangle([x - 65, y - 30, x + 65, y + 70], 16, outline=INK, width=W)
        d.arc([x - 30, y - 70, x + 30, y - 10], 180, 360, fill=INK, width=W)
        d.rectangle([x - 20, y + 5, x + 20, y + 30], fill=acc)
    elif name == "replicator":
        d.polygon(star_points(x, y, 60, 44, n=8, rot=0), outline=INK, width=10)
        line(d, [(x - 22, y), (x + 22, y)], w=12, fill=acc)
        line(d, [(x, y - 22), (x, y + 22)], w=12, fill=acc)
    elif name == "eye":
        d.chord([x - 80, y - 60, x + 80, y + 60], 200, 340, outline=INK, width=W)
        d.chord([x - 80, y - 60, x + 80, y + 60], 20, 160, outline=INK, width=W)
        circle(d, x, y, 25, fill=acc, outline=acc)
    elif name == "tree":
        line(d, [(x, y - 50), (x - 50, y + 40)], w=8)
        line(d, [(x, y - 50), (x + 50, y + 40)], w=8)
        line(d, [(x, y - 50), (x, y + 40)], w=8)
        for px, py in ((x, y - 55), (x - 50, y + 45), (x, y + 45), (x + 50, y + 45)):
            circle(d, px, py, 16, fill=acc, outline=acc)
    elif name == "route":
        line(d, [(x - 60, y + 50), (x - 60, y), (x + 60, y), (x + 60, y - 50)], w=10)
        circle(d, x - 60, y + 55, 18, fill=acc, outline=acc)
        d.polygon([(x + 60, y - 78), (x + 85, y - 40), (x + 35, y - 40)], fill=acc)
    elif name == "star":
        d.polygon(star_points(x, y, 75, 30), fill=acc)
        circle(d, x + 60, y - 55, 6, fill=INK, outline=INK)
        circle(d, x - 65, y + 50, 5, fill=INK, outline=INK)
    elif name == "planet":
        circle(d, x, y, 48, fill=acc, outline=acc)
        d.arc([x - 85, y - 25, x + 85, y + 25], 0, 360, fill=INK, width=8)
        d.pieslice([x - 48, y - 48, x + 48, y + 48], 180, 360, fill=acc)
    elif name in ("next", "prev"):
        s = 1 if name == "next" else -1
        d.polygon([(x + s * 65, y), (x - s * 25, y - 60), (x - s * 25, y + 60)], fill=acc)
        d.rectangle([x - 65, y - 20, x - 20, y + 20] if s > 0 else [x + 20, y - 20, x + 65, y + 20], fill=acc)
    else:
        raise KeyError(name)


def render(label, spec):
    group, name, tier = spec
    bg, acc = GROUPS[group]
    img = Image.new("RGB", (SIZE, SIZE), bg)
    d = ImageDraw.Draw(img)
    d._image = img
    # thin accent bar along the top identifies the group at a glance
    d.rectangle([0, 0, SIZE, 14], fill=acc)
    glyph(d, name, acc)
    if tier:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        d.ellipse([SIZE - 86, 26, SIZE - 22, 90], fill=acc)
        d.text((SIZE - 54, 58), tier, font=f, fill=bg, anchor="mm")
    text = label.replace(" >", "").replace("< ", "")
    size = 52
    f = ImageFont.truetype(FONT, size)
    while d.textlength(text, font=f) > SIZE - 24 and size > 30:
        size -= 2
        f = ImageFont.truetype(FONT, size)
    d.text((C, 245), text, font=f, fill=INK, anchor="mm")
    return img


def filename(label):
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in label).strip("-") + ".png"


def build(entries):
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    specs = icon_specs(entries)
    for old in ICON_DIR.glob("*.png"):           # drop icons for buttons that no longer exist
        if old.name not in {filename(label) for label in specs}:
            old.unlink()
    tiles = []
    for label, spec in specs.items():
        img = render(label, spec)
        img.save(ICON_DIR / filename(label))
        tiles.append(img)
    cols, t = 8, 144
    rows = math.ceil(len(tiles) / cols)
    sheet = Image.new("RGB", (cols * (t + 8) + 8, rows * (t + 8) + 8), (10, 10, 12))
    for i, img in enumerate(tiles):
        sheet.paste(img.resize((t, t), Image.LANCZOS), (8 + (i % cols) * (t + 8), 8 + (i // cols) * (t + 8)))
    (ROOT / "docs").mkdir(exist_ok=True)
    sheet.save(ROOT / "docs" / "icons-preview.png")
    print(f"wrote {len(tiles)} icons to streamdeck/icons and docs/icons-preview.png")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import dsp
    build(dsp.load())
