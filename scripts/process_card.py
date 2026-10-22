"""Shared drawing primitives for single-stage, phone-readable process cards."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os, math

W,H=1200,1100
BG='#f6f1e8'; INK='#233c40'; ACC='#c85a34'; OLD='#8eafaa'; PALE='#dedfd8'; WHITE='#ffffff'
FONT=os.environ.get('BOOK_FONT',str(Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf'))

def font(size):return ImageFont.truetype(FONT,size)
def text(d,xy,value,size=46,fill=INK):d.text(xy,value,font=font(size),fill=fill)
def wrap(d,xy,value,width=1050,size=43,fill=INK,leading=60):
    x,y=xy;line=''
    for char in value:
        if char=='\n' or d.textbbox((0,0),line+char,font=font(size))[2]>width:
            text(d,(x,y),line,size,fill);y+=leading;line='' if char=='\n' else char
        else:line+=char
    if line:text(d,(x,y),line,size,fill);y+=leading
    return y
def arrow(d,a,b,fill=ACC,width=9):
    d.line([a,b],fill=fill,width=width);angle=math.atan2(b[1]-a[1],b[0]-a[0]);r=24
    d.polygon([b,(b[0]-r*math.cos(angle-.5),b[1]-r*math.sin(angle-.5)),(b[0]-r*math.cos(angle+.5),b[1]-r*math.sin(angle+.5))],fill=fill)
def card(process,step,total,title):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    text(d,(56,30),process,36);text(d,(1020,30),f'{step:02}/{total:02}',36,ACC)
    text(d,(56,91),title,54);d.line((56,167,1144,167),fill=PALE,width=3)
    return im,d
def footer(d,legend):
    d.line((56,932,1144,932),fill=PALE,width=3)
    wrap(d,(58,956),legend,width=1080,size=37,leading=49)
def save(im,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix('.tmp')
    im.save(temporary,format='PNG',optimize=True)
    temporary.replace(path)
