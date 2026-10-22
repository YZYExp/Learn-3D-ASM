"""Application teaching plates. Simplified geometry, not branded products or process settings."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os, math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
FONT=os.environ.get('BOOK_FONT',str(Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf'))
BG='#f6f1e8'; INK='#233c40'; ORANGE='#c85a34'; GREEN='#397b7b'; PALE='#dce8df'; GRAY='#b6b9b6'; BLUE='#9abdc9'
def txt(d,x,y,s,size=35,color=INK):d.text((x,y),s,font=ImageFont.truetype(FONT,size),fill=color)
def lines(d,x,y,ss,size=31,gap=49,color=INK):
 for i,s in enumerate(ss):txt(d,x,y+i*gap,s,size,color)
def arrow(d,x1,y1,x2,y2):
 d.line((x1,y1,x2,y2),fill=ORANGE,width=7);a=math.atan2(y2-y1,x2-x1)
 d.polygon([(x2,y2),(x2-20*math.cos(a-.55),y2-20*math.sin(a-.55)),(x2-20*math.cos(a+.55),y2-20*math.sin(a+.55))],fill=ORANGE)
def card(d,x,y,w,h):d.rounded_rectangle((x,y,x+w,y+h),radius=22,fill='white')
def save(im,name):im.save(OUT/name)

im=Image.new('RGB',(2200,1300),BG);d=ImageDraw.Draw(im)
txt(d,75,55,'FFF 的实用入口：先打印帮助定位的工具',55)
txt(d,78,145,'概念练习：车标定位模板。不是 Volkswagen 或 Ford 实际工装的复刻。',31)
for x,n,title in [(75,'01','让模板找到工件边缘'),(800,'02','用窗口限定放置位置'),(1525,'03','验证后才进入重复使用')]:
 card(d,x,235,600,850);txt(d,x+30,270,n,33,ORANGE);txt(d,x+30,330,title,37)
# Frame registered against two outside edges of a flat panel.
x=75
d.rectangle((x+90,520,x+510,820),fill=GRAY,outline=INK,width=4)
d.rectangle((x+65,495,x+535,845),fill=GREEN,outline=INK,width=4)
d.rectangle((x+220,630,x+380,710),fill=GRAY,outline=INK,width=4)
arrow(d,x+10,600,x+65,600);arrow(d,x+210,915,x+210,845)
txt(d,x+55,430,'绿色：模板  灰色：下方工件',25)
lines(d,x+35,955,['先定义两个定位基准，','而非凭目测贴上去。'],30,46)
x=800
d.rectangle((x+90,520,x+510,820),fill=GRAY,outline=INK,width=4)
d.rectangle((x+65,495,x+535,845),fill=GREEN,outline=INK,width=4)
d.rectangle((x+220,630,x+380,710),fill=ORANGE,outline=INK,width=4)
txt(d,x+230,642,'标记',34,'white')
arrow(d,x+310,430,x+310,605)
lines(d,x+35,955,['窗口约束位置与朝向；','接触面应避免损伤工件。'],30,46)
x=1525
for yy,label in [(515,'贴合与重复定位'),(630,'操作者抓握和可视性'),(745,'磨损、变形与清洁')]:
 d.ellipse((x+40,yy,x+75,yy+35),outline=GREEN,width=5)
 d.line((x+46,yy+17,x+56,yy+28,x+73,yy+3),fill=GREEN,width=4)
 txt(d,x+95,yy-6,label,31)
lines(d,x+35,955,['材料、朝向与接触件分开设计；','这类模板不承担钻削载荷。'],29,46)
txt(d,80,1160,'从案例学到的选择：低数量、形状专用、会反复修改的辅助工具，是 FFF 常见的切入点。',32)
txt(d,80,1220,'原创教学示意；不设公差、载荷或寿命数值，实际工装须按生产要求验证。',27)
save(im,'case-polymer-fff-positioning.png')

im=Image.new('RGB',(2200,1400),BG);d=ImageDraw.Draw(im)
txt(d,75,48,'树脂打印常站在制造链的中间',55)
txt(d,78,135,'上：打印牙模，随后热成形。下：打印牺牲型样，随后铸造成金属。',33)
xs=[75,800,1525]
for x in xs:card(d,x,255,600,430);card(d,x,800,600,430)
for x,title in zip(xs,['① 打印实体牙模','② 片材在模型上热成形','③ 脱模、修边与抛光']):txt(d,x+30,285,title,35)
for x,title in zip(xs,['① 打印可铸造树脂型样','② 包埋、烧除与浇注','③ 金属首饰修整完成']):txt(d,x+30,830,title,35)
for x in [700,1425]:arrow(d,x,475,x+70,475);arrow(d,x,1020,x+70,1020)
# Tooth model is a generic positive section, not a patient anatomy.
profile=[(120,590),(120,500),(160,460),(210,485),(260,450),(310,480),(360,455),(410,500),(410,590)]
for idx,x in enumerate(xs[:2]):
 p=[(x+px,y) for px,y in profile];d.polygon(p,fill=PALE,outline=INK,width=4)
 d.rectangle((x+100,590,x+440,625),fill=GREEN)
 if idx:
  d.line([(x+95,505),(x+120,490),(x+160,448),(x+210,473),(x+260,438),(x+310,468),(x+360,443),(x+410,488),(x+440,505)],fill=BLUE,width=11)
  arrow(d,x+260,370,x+260,415)
x=1525
shell=[(x+110,525),(x+150,485),(x+200,510),(x+250,475),(x+300,505),(x+350,480),(x+410,525)]
d.line(shell,fill=BLUE,width=12);d.line([(a,b+18) for a,b in shell],fill=GREEN,width=4)
txt(d,x+70,585,'最终佩戴件是热成形片材',29)
# Rings as simplified front views, deliberately no branded geometry.
for x,color in [(75,ORANGE),(1525,'#be9b55')]:
 d.ellipse((x+180,945,x+420,1185),fill=color,outline=INK,width=4)
 d.ellipse((x+235,1000,x+365,1130),fill='white',outline=INK,width=4)
 d.rectangle((x+260,925,x+340,985),fill=color,outline=INK,width=4)
x=800
d.rounded_rectangle((x+150,935,x+460,1185),radius=12,fill='#e7dcc7',outline=INK,width=4)
d.ellipse((x+205,970,x+405,1170),fill='white',outline=INK,width=3)
d.rectangle((x+275,950,x+335,1000),fill='white',outline=INK,width=3)
d.ellipse((x+250,1015,x+360,1125),fill='#e7dcc7',outline=INK,width=3)
txt(d,x+175,890,'型样离开，型腔留下',27)
txt(d,80,1300,'原创简化流程图。牙模不等于牙套；树脂型样不等于金属首饰。省略了支撑、清洗、浇道与具体温控。',28)
save(im,'case-polymer-resin-indirect.png')
