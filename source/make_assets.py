"""Build email-safe PNG assets for the Rogue Zerobyte signature.

Usage (from the repo root):  python3 source/make_assets.py source assets

Everything is rendered at 2x so it stays sharp on retina screens; the HTML
sets the display size. Rounding and rings are baked into the PNGs because
Outlook and some Gmail views ignore CSS border-radius.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

MINT = (168, 219, 205)
TEAL = (47, 125, 109)
SS = 4  # supersample factor for smooth edges


def circle_mask(size):
    m = Image.new("L", (size * SS, size * SS), 0)
    ImageDraw.Draw(m).ellipse((0, 0, size * SS - 1, size * SS - 1), fill=255)
    return m.resize((size, size), Image.LANCZOS)


# 1. Headshot: circle with a thin mint ring, 192px (shown at 96px).
size, ring = 192, 5
photo = Image.open(SRC / "headshot-original.png").convert("RGB").crop((86, 30, 686, 630))
inner = size - 2 * ring
photo = photo.resize((inner, inner), Image.LANCZOS)
head = Image.new("RGBA", (size, size), (0, 0, 0, 0))
ring_img = Image.new("RGBA", (size, size), MINT + (255,))
head.paste(ring_img, (0, 0), circle_mask(size))
head.paste(photo, (ring, ring), circle_mask(inner))
head.save(OUT / "headshot.png", optimize=True)

# 2. RZB monogram: round black badge, 80px (shown at 40px).
mono_src = Image.open(SRC / "rzb-mark-original.jpg").convert("RGB")
cx, cy, r = 490, 490, 296
mono = mono_src.crop((cx - r, cy - r, cx + r, cy + r)).resize((80, 80), Image.LANCZOS)
mono_out = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
mono_out.paste(mono, (0, 0), circle_mask(80))
mono_out.save(OUT / "rzb-mark.png", optimize=True)

# 3. LinkedIn icon: teal circle with a white "in" (visible on light and dark), 48px (shown at 24px).
big = 48 * SS
li = Image.new("RGBA", (big, big), (0, 0, 0, 0))
d = ImageDraw.Draw(li)
d.ellipse((0, 0, big - 1, big - 1), fill=TEAL + (255,))
font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", int(big * 0.46), index=1)
bbox = d.textbbox((0, 0), "in", font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
d.text(((big - tw) / 2 - bbox[0], (big - th) / 2 - bbox[1] + big * 0.01), "in", font=font, fill=(255, 255, 255))
li.resize((48, 48), Image.LANCZOS).save(OUT / "linkedin.png", optimize=True)

for p in sorted(OUT.glob("*.png")):
    im = Image.open(p)
    print(p.name, im.size, p.stat().st_size, "bytes")
