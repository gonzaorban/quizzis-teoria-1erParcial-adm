# Dev helper: renders the theory PDF page behind each high-confidence "source" as an image, so the review can
# show it without opening the PDF. Writes sources/pages/<pdf>-p<N>.webp and sets "source.img" on the question;
# questions whose source is not high confidence lose "source.img". Safe to run again after changing sources.
# With "source.crop" (a list of [x0, y0, x1, y1] boxes, in % of the page image) it keeps only those parts of
# the page, stacked top to bottom, in sources/pages/<pdf>-p<N>-<hash>.webp.
# Requires PyMuPDF and Pillow (pip install pymupdf pillow). Usage:
#   python scripts/render-source-pages.py <materia>/<parcial>   (ej.: redes/1er-parcial)
import hashlib
import io
import json
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops, ImageDraw

WIDTH = 1280  # px; the slides are landscape, so this keeps small text legible on a phone when zoomed
QUALITY = 80
GAP = 17  # px between two crop boxes of the same page, with a thin line in the middle

root = Path(__file__).resolve().parent.parent
if len(sys.argv) != 2:
    sys.exit("uso: python scripts/render-source-pages.py <materia>/<parcial>")
subject = root / "subjects" / sys.argv[1]
qpath = subject / "questions.json"
data = json.loads(qpath.read_text(encoding="utf-8"))
out = subject / "sources" / "pages"
out.mkdir(exist_ok=True)


def content_box(img):
    return ImageChops.difference(img, Image.new("RGB", img.size, "white")).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()


def crop(img, boxes):
    w, h = img.size
    parts = []
    for x0, y0, x1, y1 in boxes:
        part = img.crop((round(w * x0 / 100), round(h * y0 / 100), round(w * x1 / 100), round(h * y1 / 100)))
        # drop the blank lines at the top and bottom of the box, but keep its left margin so the stacked parts
        # stay aligned
        box = content_box(part)
        if box:
            part = part.crop((0, box[1], part.width, box[3]))
        parts.append(part)
    stacked = Image.new("RGB", (max(p.width for p in parts), sum(p.height for p in parts) + GAP * (len(parts) - 1)), "white")
    y = 0
    for i, part in enumerate(parts):
        if i:
            ImageDraw.Draw(stacked).line([(0, y - GAP // 2 - 1), (stacked.width, y - GAP // 2 - 1)], fill=(200, 200, 200))
        stacked.paste(part, (0, y))
        y += part.height + GAP
    return stacked


docs, used = {}, set()
for q in data["questions"]:
    src = q.get("source")
    if not src:
        continue
    if src.get("confidence") != "high":
        src.pop("img", None)
        continue
    name = f"{Path(src['file']).stem}-p{src['page']}"
    if src.get("crop"):
        name += "-" + hashlib.sha1(json.dumps(src["crop"]).encode()).hexdigest()[:6]
    name += ".webp"
    src["img"] = f"sources/pages/{name}"
    if name in used:
        continue
    used.add(name)
    doc = docs.setdefault(src["file"], pymupdf.open(subject / src["file"]))
    page = doc[src["page"] - 1]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(WIDTH / page.rect.width, WIDTH / page.rect.width), alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    # trim the white bands around 16:9 slides printed on A4
    box = content_box(img)
    if box:
        img = img.crop(box)
    if src.get("crop"):
        img = crop(img, src["crop"])
    img.save(out / name, "WEBP", quality=QUALITY, method=6)

for stale in out.glob("*.webp"):
    if stale.name not in used:
        stale.unlink()

# each crop box on a single line, instead of one line per number
crops = {}
for q in data["questions"]:
    if q.get("source", {}).get("crop"):
        key = f"@crop{len(crops)}@"
        crops[key] = "[" + ", ".join(json.dumps(b) for b in q["source"]["crop"]) + "]"
        q["source"]["crop"] = key
text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
for key, value in crops.items():
    text = text.replace(f'"{key}"', value)
qpath.write_text(text, encoding="utf-8", newline="\n")
print(f"{len(used)} páginas renderizadas en {out.relative_to(root)}")
