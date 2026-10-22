"""Build all chapter PDFs and the illustrated book directly from Markdown; no HTML output."""
from pathlib import Path
import re, json, html, math, os, argparse
from urllib.parse import urlparse
from reportlab import rl_config
# Binary image streams avoid ASCII85 overhead without changing image quality.
rl_config.useA85 = False
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from PIL import Image as PILImage
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'build';BUILD.mkdir(exist_ok=True)
(ROOT/'tmp').mkdir(exist_ok=True)
font=Path(os.environ.get('BOOK_FONT',str(Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf')))
if not font.exists():raise SystemExit('Set BOOK_FONT to a Chinese TrueType font path (e.g. NotoSansSC-Regular.ttf).')
pdfmetrics.registerFont(TTFont('Book',str(font)))
for n in ['Book-Bold','Book-Italic','Book-BoldItalic']:pdfmetrics.registerFont(TTFont(n,str(font)))
pdfmetrics.registerFontFamily('Book',normal='Book',bold='Book-Bold',italic='Book-Italic',boldItalic='Book-BoldItalic')
W,H=595.276,841.89;M=49;BW=W-2*M
INK=colors.HexColor('#223b3e');ACC=colors.HexColor('#b94e2c');BG=colors.HexColor('#faf7f0')
styles={
 'body':ParagraphStyle('body',fontName='Book',fontSize=10.3,leading=17.7,spaceAfter=9,textColor=INK,wordWrap='CJK'),
 'h1':ParagraphStyle('h1',fontName='Book',fontSize=24,leading=34,spaceAfter=19,textColor=INK,keepWithNext=True,wordWrap='CJK'),
 'h2':ParagraphStyle('h2',fontName='Book',fontSize=14,leading=23,spaceBefore=11,spaceAfter=8,textColor=ACC,keepWithNext=True,wordWrap='CJK'),
 'cap':ParagraphStyle('cap',fontName='Book',fontSize=8.1,leading=12.4,spaceAfter=14,textColor=colors.HexColor('#5a6664'),wordWrap='CJK'),
 'cell':ParagraphStyle('cell',fontName='Book',fontSize=8.1,leading=12.6,textColor=INK,wordWrap='CJK'),
 'foot':ParagraphStyle('foot',fontName='Book',fontSize=6.4,leading=8.6,textColor=colors.HexColor('#586866'),wordWrap='CJK'),
}
SOURCES=[];URLID={};PAGE_AUDIT=[]
def source(title,url):
 url=re.split(r'[，。；、\s]',url,maxsplit=1)[0].rstrip('。，；、')
 if url not in URLID:
  URLID[url]=len(SOURCES)+1;SOURCES.append({'id':len(SOURCES)+1,'title':title,'url':url})
 return URLID[url]

class RefP(Paragraph):
 def __init__(self,text,style,refs=(),**kw):self.refs=set(refs);super().__init__(text,style,**kw)
 def draw(self):
  if not hasattr(self.canv,'page_refs'):self.canv.page_refs=set()
  self.canv.page_refs.update(self.refs);super().draw()
 def split(self,*args):
  out=super().split(*args)
  for p in out:p.refs=self.refs
  return out

def para(s,kind='body',defs=None):
 refs=[];defs=defs or {};tokens={}
 def mark(title,url):
  url=re.split(r'[，。；、\s]',url,maxsplit=1)[0].rstrip('。，；、')
  n=source(title,url);refs.append(n);key=f'ZZTOKEN{len(tokens)}ZZ';tokens[key]=f'<super><a href="{html.escape(url,quote=True)}" color="#b94e2c">[{n}]</a></super>';return key
 s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',lambda m:mark(m[1],m[2]),s)
 for k,(title,url) in defs.items():s=s.replace('['+k+']',mark(title,url)) if '['+k+']' in s else s
 s=re.sub(r'https?://[^\s<>]+',lambda m:mark(urlparse(m[0].rstrip('。，；、')).netloc,m[0].rstrip('。，；、')),s)
 s=html.escape(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s);s=s.replace('`','')
 for k,v in tokens.items():s=s.replace(k,v)
 return RefP(s,styles[kind],refs)

class BookDoc(BaseDocTemplate):
 def __init__(self,path,**kw):
  super().__init__(str(path),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=51,bottomMargin=162,title='造物的加减法：以3D打印为中心的制造图鉴',author='图解知识书',**kw)
  self.addPageTemplates(PageTemplate('book',frames=[Frame(M,162,BW,H-215,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPageEnd=self.footer))
  self.chapter_pages=[];self.chapter=''
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='h1':
   self.chapter=f.getPlainText();self.chapter_pages.append((self.chapter,self.page));self.canv.bookmarkPage('ch'+str(len(self.chapter_pages)));self.canv.addOutlineEntry(self.chapter,'ch'+str(len(self.chapter_pages)),0)
 def footer(self,c,doc):
  c.saveState();c.setStrokeColor(colors.HexColor('#ddd9d0'));c.line(M,148,W-M,148)
  refs=sorted(getattr(c,'page_refs',set()));PAGE_AUDIT.append({'file':Path(self.filename).name,'page':doc.page,'sources':refs})
  c.setFont('Book',7);c.setFillColor(INK);c.drawString(M,H-29,'造物的加减法  /  3D打印 · 材料 · 制造');c.drawRightString(W-M,29,str(doc.page))
  if refs:
   c.setFont('Book',6.8);c.drawString(M,135,'本页资料 · 点击标题访问来源')
   cols=2 if len(refs)>6 else 1;cw=(BW-14*(cols-1))/cols;y=[122]*cols
   for j,n in enumerate(refs):
    col=j%cols;s=SOURCES[n-1];label=s['title'].replace('资料：','')
    if len(label)>86:label=label[:83]+'…'
    t=f'[{n}] <a href="{html.escape(s["url"],quote=True)}">{html.escape(label)}</a> · {html.escape(urlparse(s["url"]).netloc.replace("www.",""))}'
    p=Paragraph(t,styles['foot']);_,ph=p.wrap(cw,100);y[col]-=ph;p.drawOn(c,M+col*(cw+14),y[col]);y[col]-=3
   if min(y)<35:raise RuntimeError(f'Footer overflow {self.filename} p{doc.page}: {len(refs)} sources; y={min(y)}')
  c.page_refs=set();c.restoreState()

def figure(path,cap,defs):
 p=ROOT/'chapters'/path
 if not p.exists():raise FileNotFoundError(p)
 with PILImage.open(p) as im:w,h=im.size
 scale=min(BW/w,285/h);iw=w*scale;ih=h*scale
 return KeepTogether([Spacer(1,6),Image(str(p),width=iw,height=ih),Spacer(1,6),para(cap,'cap',defs)])

def read_chapter(path):
 text=path.read_text();lines=text.splitlines();defs={}
 for line in lines:
  m=re.match(r'-\s*\[([^\]]+)\]\s*(.*?)[：:]\s*(https?://\S+)',line)
  if m:defs[m[1]]=(m[2],m[3])
 story=[];buf=[];i=0
 def flush():
  if buf:story.append(para(''.join(buf),defs=defs));buf.clear()
 while i<len(lines):
  line=lines[i].strip()
  if line.startswith('## 本章资料'):flush();break
  if not line:flush();i+=1;continue
  if line.startswith('# '):flush();story.append(para(line[2:],'h1',defs));i+=1;continue
  if line.startswith('## '):flush();story.append(para(line[3:],'h2',defs));i+=1;continue
  if line.startswith('!['):
   flush();m=re.match(r'!\[(.*)\]\((\.\./assets/images/[^)]+)\)',line)
   if not m:raise ValueError(line)
   k=i+1
   while k<len(lines) and not lines[k].strip():k+=1
   cap=m[1]
   if k<len(lines) and lines[k].strip().startswith('图：'):cap=lines[k].strip();i=k
   story.append(figure(m[2],cap,defs));i+=1;continue
  if line.startswith('|'):
   flush();rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
    if not all(re.match(r'^:?-+:?$',x) for x in cells):rows.append([para(x,'cell',defs) for x in cells])
    i+=1
   n=len(rows[0]);ratios={2:[.27,.73],3:[.23,.38,.39],4:[.18,.27,.27,.28]}.get(n,[1/n]*n)
   t=Table(rows,colWidths=[BW*x for x in ratios],repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eae4')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f2eb')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#c7d0c7'))]))
   story.extend([t,Spacer(1,13)]);continue
  if line.startswith('- '):flush();story.append(para('• '+line[2:],defs=defs));i+=1;continue
  if line.startswith('图：'):flush();story.append(para(line,'cap',defs));i+=1;continue
  buf.append(line);i+=1
 flush()
 # A section title must stay with the figure that opens its section.
 combined=[];j=0
 while j<len(story):
  if j+1<len(story) and isinstance(story[j],Paragraph) and story[j].style.name=='h2' and isinstance(story[j+1],KeepTogether):
   combined.append(KeepTogether([story[j]]+story[j+1]._content));j+=2
  else:combined.append(story[j]);j+=1
 return combined

def front(pages):
 path=BUILD/'front.pdf';c=canvas.Canvas(str(path),pagesize=(W,H));c.setTitle('造物的加减法')
 c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(ACC);c.setFont('Book',11);c.drawString(M,775,'THE ART & SCIENCE OF MAKING')
 c.setFillColor(INK);c.setFont('Book',38);c.drawString(M,695,'造物的加减法');c.setFont('Book',16);c.drawString(M,650,'以 3D 打印为中心的制造图鉴')
 c.drawImage(str(ROOT/'assets/images/01-cover.jpg'),M,220,width=BW,height=BW*2/3,mask='auto')
 c.setFont('Book',10);c.drawString(M,174,'发展 · 工艺 · 材料 · 美学 · 当代品牌');c.setFont('Book',8);c.drawString(M,72,'图解科普读本  |  2026年10月22日  |  第一版');c.drawString(M,53,'封面：AI教学示意，概念作品，不代表真实品牌产品。');c.showPage()
 c.setFillColor(INK);c.setFont('Book',24);c.drawString(M,775,'阅读地图');c.setFont('Book',9);c.drawString(M,744,'从一卷线与一槽液体，读到整个制造世界。')
 y=707
 for title,p in pages:
  c.setFont('Book',10);c.drawString(M,y,title);c.drawRightString(W-M,y,str(p));y-=29
 c.setFont('Book',8);c.setFillColor(ACC);c.drawString(M,95,'图像标识：AI教学示意 / 原创图解 / 真实来源图片');c.setFillColor(INK);c.drawString(M,73,'目录使用正文页码，封面与本目录不计入。');c.showPage();c.save();return path

def main():
 paths=sorted((ROOT/'chapters').glob('[0-9][0-9].md'))
 for path in paths:
  doc=BookDoc(BUILD/(path.stem+'.pdf'));doc.build(read_chapter(path))
 story=[]
 for i,path in enumerate(paths):
  if i:story.append(PageBreak())
  story.extend(read_chapter(path))
 doc=BookDoc(BUILD/'body.pdf');doc.build(story)
 f=front(doc.chapter_pages);w=PdfWriter();w.append(str(f));w.append(str(BUILD/'body.pdf'))
 w.add_metadata({'/Title':'造物的加减法：以3D打印为中心的制造图鉴','/Author':'图解知识书','/Subject':'3D打印、增材制造、减材制造、材料、现代品牌'})
 with (BUILD/'Manufacturing_Atlas.pdf').open('wb') as fp:w.write(fp)
 (ROOT/'references/all-sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2))
 (ROOT/'references/bibliography.md').write_text('# 全书资料索引\n\n'+'\n\n'.join(f'[{s["id"]}] {s["title"]}\n\n{s["url"]}' for s in SOURCES))
 (ROOT/'tmp/page-audit.json').write_text(json.dumps(PAGE_AUDIT,ensure_ascii=False,indent=2))
 print(json.dumps({'pages':len(PdfReader(str(BUILD/'Manufacturing_Atlas.pdf')).pages),'chapters':len(paths),'sources':len(SOURCES),'chapter_pages':doc.chapter_pages},ensure_ascii=False))
if __name__=='__main__':main()
