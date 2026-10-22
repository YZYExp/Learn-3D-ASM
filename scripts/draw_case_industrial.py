"""Original application diagrams; generic geometry, not brand product drawings."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'; FONT=os.environ.get('BOOK_FONT',str(Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf'))
BG='#f6f1e8';INK='#233c40';ACC='#c85a34';TEAL='#4d8283';PALE='#dce5df';GRAY='#7b8b89'
def font(size):return ImageFont.truetype(FONT,size)
def text(d,xy,s,size=32,fill=INK):d.text(xy,s,font=font(size),fill=fill)
def lines(d,xy,ss,size=31,fill=INK,gap=51):
 for i,s in enumerate(ss):text(d,(xy[0],xy[1]+gap*i),s,size,fill)
def arrow(d,a,b,fill=ACC,w=6):
 d.line([a,b],fill=fill,width=w);dx=b[0]-a[0];dy=b[1]-a[1];ang=math.atan2(dy,dx)
 pts=[b,(b[0]-23*math.cos(ang-.48),b[1]-23*math.sin(ang-.48)),(b[0]-23*math.cos(ang+.48),b[1]-23*math.sin(ang+.48))];d.polygon(pts,fill=fill)
def canvas(title,sub):
 im=Image.new('RGB',(2200,1300),BG);d=ImageDraw.Draw(im)
 text(d,(90,65),title,57);text(d,(92,155),sub,29,GRAY)
 d.line([(90,220),(2110,220)],fill='#cbd1ca',width=3)
 return im,d
def save(im,name):im.save(OUT/name,optimize=True)

im,d=canvas('工艺选择，先看零件承担的任务','原创应用示意：以下是通用几何，不是 NASA、John Deere 或其他品牌实物图纸。')
for x in [85,790,1495]:d.rounded_rectangle((x,275,x+620,1110),radius=26,fill='white')
text(d,(120,305),'LPBF：让内部路线随形状走',36)
# Generic cold plate cutaway, channel represented in plan section.
d.rounded_rectangle((160,470,630,730),radius=20,fill=PALE,outline=INK,width=5)
pts=[(175,520),(260,520),(260,675),(360,675),(360,520),(460,520),(460,675),(615,675)]
d.line(pts,fill=TEAL,width=40,joint='curve');arrow(d,(95,520),(200,520));arrow(d,(600,675),(700,675))
d.rectangle((160,450,630,478),fill=GRAY)
text(d,(185,760),'冷板的通道与安装面分工',29)
lines(d,(120,875),['任务：把热带走','优势：设计内部流道','交付：清粉、机加工、检漏'],30)
text(d,(825,305),'DED：只在需要处加材料',36)
# Worn shaft cross-section, local added ring, tool icon.
d.rectangle((875,555,1315,685),fill='#a8b5b1',outline=INK,width=5)
d.rectangle((1045,555,1145,583),fill='white')
d.rectangle((1045,543,1145,583),fill=ACC)
for y in [551,562,573]:d.line([(1047,y),(1143,y)],fill='#f4d1b8',width=3)
d.polygon([(1040,405),(1150,405),(1115,465),(1075,465)],fill=INK)
arrow(d,(1095,465),(1095,530));text(d,(1165,425),'局部补材',29)
d.line([(1010,715),(1180,715)],fill=INK,width=4)
text(d,(930,760),'轴类修复：补材后再加工',29)
lines(d,(825,875),['任务：恢复局部形状','优势：保留仍可用的基体','交付：界面、尺寸与服役验证'],30)
text(d,(1530,305),'金属黏结剂喷射：组织批量',34)
for x,y in [(1590,480),(1780,480),(1590,650),(1780,650)]:
 d.rounded_rectangle((x,y,x+135,y+110),radius=17,fill='#b5bab5',outline=INK,width=4)
 d.ellipse((x+40,y+23,x+95,y+78),fill='white',outline=INK,width=3)
text(d,(1570,790),'阀体 / 接头类：示意一批',29)
lines(d,(1530,875),['任务：复杂小金属件','优势：打印与烧结协同组织','交付：烧结收缩、密封与检验'],30)
text(d,(90,1175),'先看流道、修复区域或批量需求，再比较成本；不能只凭“金属打印”四个字选设备。',33)
save(im,'case-industrial-metal-applications.png')

im,d=canvas('打印陶瓷芯，是为了制造金属里的空腔','原创反形关系图：简化铸造体，展示“中间工具”与“最终零件”的差别；不是叶片工艺图纸。')
for x in [80,800,1520]:d.rounded_rectangle((x,275,x+600,1100),radius=24,fill='white')
text(d,(120,315),'1  制作并烧结陶瓷芯',38)
text(d,(840,315),'2  让金属包围芯体',38)
text(d,(1560,315),'3  去芯，留下通道',38)
# Branch shape represents ceramic core; same identity carried through stages.
def core(cx,cy,fill,width=62):
 d.line([(cx,cy+210),(cx,cy-110),(cx-145,cy-210)],fill=fill,width=width,joint='curve')
 d.line([(cx,cy-110),(cx+145,cy-210)],fill=fill,width=width,joint='curve')
for cx in [380,1100,1820]:
 if cx!=380:d.rounded_rectangle((cx-210,445,cx+210,830),radius=20,fill='#aebbb8',outline=INK,width=5)
 core(cx,650,'#e8c39d' if cx!=1820 else BG)
 if cx==1820:
  arrow(d,(cx,890),(cx,745),TEAL)
  arrow(d,(cx-110,475),(cx-175,430),TEAL)
  arrow(d,(cx+110,475),(cx+175,430),TEAL)
arrow(d,(705,635),(765,635));arrow(d,(1425,635),(1485,635))
lines(d,(120,900),['芯体形状定义未来通道','需控制烧结尺寸与强度'],30)
lines(d,(840,900),['芯体占据不应被金属填满的空间','金属成形属于后续铸造流程'],29)
lines(d,(1560,900),['空腔继承芯体的大致形状','清理、检测后才进入后续环节'],29)
text(d,(90,1175),'重点：打印的是陶瓷中间物；“陶瓷 3D 打印”并不等于最终涡轮叶片也是陶瓷。',32)
save(im,'case-industrial-ceramic-core-role.png')
