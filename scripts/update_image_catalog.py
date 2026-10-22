"""Refresh embedded-figure inventory from chapter sources, including stage cards."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
p=root/'references/image-catalog.json'
previous={x['file']:x for x in json.loads(p.read_text())}
sequence_files={s['file']:str(meta.relative_to(root)) for meta in (root/'references').glob('process-sequences-*.json') for seq in json.loads(meta.read_text()) for s in seq['steps']}
chapters={c.stem:c.read_text() for c in (root/'chapters').glob('[0-9][0-9].md')}
result=[]
for image in sorted((root/'assets/images').iterdir()):
    key=image.relative_to(root).as_posix()
    item=previous.get(key,{'file':key,'kind':'diagram','metadata':sequence_files.get(key)})
    item['chapters']=[cid for cid,text in chapters.items() if '../'+key in text]
    assert item['chapters'],f'Unembedded image: {key}'
    assert item.get('metadata'),f'Missing provenance: {key}'
    item['sha256']=hashlib.sha256(image.read_bytes()).hexdigest()
    result.append(item)
p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(f'Catalogued {len(result)} embedded images')
