"""Prepare the pinned SIL-OFL Noto Sans SC font for a reproducible PDF build."""
from pathlib import Path
from urllib.request import urlopen
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

COMMIT = 'a85815a42757630ce188fdad368c2dfc444d4773'
BASE = f'https://raw.githubusercontent.com/google/fonts/{COMMIT}/ofl/notosanssc/'
target = Path(os.environ.get('BOOK_FONT', str(Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf')))
if not target.exists():
    target.parent.mkdir(parents=True, exist_ok=True)
    variable = target.with_name('NotoSansSC-variable.ttf')
    with urlopen(BASE+'NotoSansSC%5Bwght%5D.ttf', timeout=120) as response:
        variable.write_bytes(response.read())
    font = instantiateVariableFont(TTFont(variable), {'wght': 400}, inplace=True)
    font.save(target)
    with urlopen(BASE+'OFL.txt', timeout=30) as response:
        target.with_name('NotoSansSC-OFL.txt').write_bytes(response.read())
    variable.unlink()
print(f'Chinese font ready: {target.name}')
