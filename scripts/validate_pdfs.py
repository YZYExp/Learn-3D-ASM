"""Heavy PDF integrity checks belong to export, separate from web publication."""
from pathlib import Path
from pypdf import PdfReader
import re
root=Path(__file__).resolve().parents[1]
files=list((root/'pdf').rglob('*.pdf'))
assert len(files)==19
for path in files:
    reader=PdfReader(path)
    assert len(reader.pages)>0, path
    for page in reader.pages:
        assert '\ufffd' not in (page.extract_text() or ''), path
        for annotation in page.get('/Annots',[]):
            action=annotation.get_object().get('/A',{})
            url=action.get('/URI','')
            assert not re.search(r'[，。；、\s]',url), (path,url)
print(f'Validated {len(files)} PDFs and their text/link integrity.')
