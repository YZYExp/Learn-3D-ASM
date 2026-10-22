"""Build the homepage and full reader from the same chapter Markdown as the PDF."""
from pathlib import Path
import re, json, shutil, html, argparse, hashlib
from collections import Counter
import markdown

ROOT=Path(__file__).resolve().parents[1]
MOBILE_PANELS=json.loads((ROOT/'references/mobile-panels.json').read_text())
SUMMARIES=[
 '阅读路线、图像类型与资料日期。',
 '先看材料怎样改变，再理解七大工艺家族与发展脉络。',
 'FFF、颗粒、填充、层间结合，及短切与连续纤维。',
 'SLA、DLP、MSLA：光如何写出形状，后处理为何重要。',
 'SLS与MJF的差异，以及粉床中的支撑、排粉与表面。',
 '激光与电子束粉床、DED、粘结剂喷射与成件状态。',
 '材料喷射、薄材叠层，以及陶瓷、食品、建筑和生物打印。',
 '从PLA、PETG、TPU到工程聚合物、复材、树脂与金属。',
 'CAD、网格、切片、支撑、后处理与最终检验。',
 '车、铣、钻、磨、电火花、激光、水刀与蚀刻。',
 '同一件东西，如何选择打印、切削、模具或混合制造。',
 '层纹、透明、颜色、拓扑与参数化形态的审美线索。',
 '拓竹、Prusa、Sovol、Rat Rig、Voron等品牌与社区。',
 '工业流程、Formlabs、EOS及Meltio、Caracol等新力量。',
 '铂力特、华曙、易加、联泰，以及材料、扫描与服务。',
 '从大型机床到Makera等桌面工具，认识减材生态。',
 '四个不必先买机器的观察、设计与工艺选择练习。',
 '把AM、FFF、SLA、MJF、DED、CNC等缩写变成动作。'
]

def chapter_html(text,chapter_id):
    lines=text.splitlines();title=lines[0].removeprefix('# ');body='\n'.join(lines[1:]);definitions={}
    for m in re.finditer(r'^-\s*\[([^\]]+)\]\s*(.*?)[：:]\s*(https?://\S+)',body,re.M):
        definitions[m[1]]=(m[2],re.split(r'[，。；、\s]',m[3],maxsplit=1)[0])
    # Retain the chapter bibliography and make its in-text references clickable.
    for key,(label,url) in definitions.items():
        body=re.sub(r'(?<!-)\['+re.escape(key)+r'\](?!\()',lambda m:'['+key+']('+url+')',body)
    src=body.splitlines();out=[];i=0
    while i<len(src):
        m=re.match(r'!\[(.*)\]\((\.\./assets/images/[^)]+)\)',src[i].strip())
        if not m:out.append(src[i]);i+=1;continue
        cap,path=m.groups();j=i+1
        while j<len(src) and not src[j].strip():j+=1
        if j<len(src) and src[j].startswith('图：'):cap=src[j];i=j
        alt=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',cap)[:150]
        caption=markdown.markdown(cap)
        name=Path(path).name
        alternate=MOBILE_PANELS.get(name)
        classes='process-step' if name.startswith('step-') else ''
        if alternate:classes+=' responsive-figure'
        def image_tag(image_path,image_alt,extra=''):
            return '<img loading="lazy" decoding="async" tabindex="0" role="button" aria-label="放大图片" '+extra+' src="'+html.escape(image_path,quote=True)+'" alt="'+html.escape(image_alt,quote=True)+'">'
        full=image_tag(path.replace('../',''),alt,'class="diagram-overview"' if alternate else '')
        mobile=''
        if alternate:
            parts=[]
            for panel in alternate.get('panels',[]):
                parts.append('<section class="mobile-panel"><h4>'+html.escape(panel['title'])+'</h4>'+image_tag(panel['file'],panel['alt'])+'<p>'+html.escape(panel['caption'])+'</p></section>')
            for card in alternate.get('cards',[]):
                parts.append('<section class="mobile-panel text-panel"><h4>'+html.escape(card['title'])+'</h4><p>'+html.escape(card['caption'])+'</p></section>')
            mobile='<div class="mobile-diagram"><p class="panel-guide">分图阅读 · 从上往下看</p>'+''.join(parts)+'<p class="panel-note">'+html.escape(alternate['note'])+'</p></div>'
        out.append('\n<figure class="'+classes.strip()+'">'+full+mobile+'<figcaption>'+caption+'</figcaption></figure>\n')
        i+=1
    result=markdown.markdown('\n'.join(out),extensions=['tables','fenced_code'])
    result=re.sub(r'<a href="(https?://[^"]+)"',r'<a target="_blank" rel="noopener noreferrer" href="\1"',result)
    result=result.replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')
    return title,result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=ROOT/'build/homepage');parser.add_argument('--mobile-preview',action='store_true',help='Build an unlinked 390px iframe for visual QA');args=parser.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    for p in (ROOT/'web').iterdir():
        if p.is_file():shutil.copy2(p,out/p.name)
    index=out/'index.html'
    image_count=len(list((ROOT/'assets/images').glob('*')))
    source_count=len(json.loads((ROOT/'references/all-sources.json').read_text()))
    catalog=json.loads((ROOT/'references/image-catalog.json').read_text())
    counts=Counter(item['kind'] for item in catalog)
    replacements={'IMAGE_COUNT':image_count,'SOURCE_COUNT':source_count,'AI_COUNT':counts['ai'],'DIAGRAM_COUNT':counts['diagram'],'REAL_COUNT':counts['real']}
    cards=[]
    for item in json.loads((ROOT/'references/application-entrypoints.json').read_text()):
        title=html.escape(item['title']);image=html.escape(item['image'],quote=True)
        label=html.escape(item['label']);description=html.escape(item['description'])
        credit=html.escape(item['credit']);source=html.escape(item['source'],quote=True)
        cards.append(f'<article class="application-card"><a href="#read/{item["chapter"]}"><img src="{image}" alt="{html.escape(item["alt"],quote=True)}" loading="eager"><p class="tiny-label">{label}</p><h3>{title} ↗</h3></a><p>{description}</p><p class="application-credit">{credit} · <a href="{source}" target="_blank" rel="noopener noreferrer">图像与案例来源 ↗</a></p></article>')
    replacements['APPLICATION_CARDS']=''.join(cards)
    rendered=index.read_text()
    for key,value in replacements.items():rendered=rendered.replace('{{'+key+'}}',str(value))
    if re.search(r'\{\{[A-Z_]+\}\}',rendered):raise ValueError('Unresolved homepage template marker')
    index.write_text(rendered)
    chapters=[]
    for p in sorted((ROOT/'chapters').glob('[0-9][0-9].md')):
        text=p.read_text();title,content=chapter_html(text,p.stem)
        chapters.append({'id':p.stem,'title':title,'summary':SUMMARIES[int(p.stem)],'html':content,'search':re.sub(r'<[^>]+>',' ',content)})
    (out/'content.js').write_text('window.BOOK_CHAPTERS = '+json.dumps(chapters,ensure_ascii=False).replace('</',r'<\/')+';\n')
    for name in ['assets','pdf','chapters']:
        shutil.copytree(ROOT/name,out/name,dirs_exist_ok=True)
    (out/'references').mkdir(exist_ok=True)
    for source in (ROOT/'references').iterdir():
        if source.is_file() and source.suffix in {'.md','.json'}:shutil.copy2(source,out/'references'/source.name)
    # Release URLs change with content so a cached script cannot mask new chapters.
    rendered=index.read_text()
    for asset in ['style.css','app.js','content.js']:
        version=hashlib.sha256((out/asset).read_bytes()).hexdigest()[:12]
        rendered=rendered.replace('"'+asset+'"','"'+asset+'?v='+version+'"')
    index.write_text(rendered)
    (out/'.nojekyll').write_text('')
    if args.mobile_preview:
        (out/'mobile-preview.html').write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><title>390px reading preview</title><style>body{margin:0;background:#ccc}iframe{display:block;width:390px;height:950px;border:0;margin:20px auto}</style><iframe title="手机阅读预览" src="index.html#read/02"></iframe></html>')
    # Validate every embedded local image and download target before publication.
    for ch in chapters:
        for src in re.findall(r'src="([^"]+)"',ch['html']):
            if not (out/html.unescape(src)).is_file():raise FileNotFoundError(src)
    assert len(chapters)==18
    print(json.dumps({'output':str(out),'chapters':len(chapters),'images':len(list((out/'assets/images').glob('*'))),'pdfs':len(list((out/'pdf').rglob('*.pdf')))},ensure_ascii=False))
if __name__=='__main__':main()
