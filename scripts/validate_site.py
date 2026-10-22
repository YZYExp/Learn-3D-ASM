"""Fail publication on missing images, downloads or project-relative assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from PIL import Image
from pypdf import PdfReader
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/'build/homepage'

class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ('src', 'href') or not value:
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.path:
                continue
            if url.path.startswith('/'):
                raise ValueError(f'Root-relative URL breaks project Pages: {value}')
            if not (SITE/unquote(url.path)).is_file():
                raise FileNotFoundError(value)

parser = Links()
parser.feed((SITE/'index.html').read_text())
raw = (SITE/'content.js').read_text()
chapters = json.loads(raw.removeprefix('window.BOOK_CHAPTERS = ').rstrip(';\n'))
assert len(chapters) == 18
for chapter in chapters:
    parser.feed(chapter['html'])
images = list((SITE/'assets/images').glob('*'))
for path in images:
    with Image.open(path) as image:
        image.verify()
pdfs = list((SITE/'pdf').rglob('*.pdf'))
assert len(pdfs) == 19
for path in pdfs:
    assert len(PdfReader(path).pages) > 0, path
assert (SITE/'.nojekyll').exists()
print(f'Validated {len(chapters)} chapters, {len(images)} images and {len(pdfs)} PDFs.')
