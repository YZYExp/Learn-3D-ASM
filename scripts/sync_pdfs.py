"""Copy reviewed PDF build outputs into the repository's reading directory."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
files = [(root / 'build/Manufacturing_Atlas.pdf', root / 'pdf/Manufacturing_Atlas.pdf')]
files += [(root / f'build/{i:02}.pdf', root / f'pdf/chapters/{i:02}.pdf') for i in range(18)]
missing = [str(src.relative_to(root)) for src, _ in files if not src.is_file()]
if missing:
    raise SystemExit('Run scripts/build_book.py first; missing: ' + ', '.join(missing))
for src, dst in files:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
print(f'Synchronized {len(files)} PDFs to pdf/.')
