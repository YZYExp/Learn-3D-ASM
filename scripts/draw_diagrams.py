from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, os
OUT=Path(__file__).resolve().parents[1]/'assets/images'
FONT=os.environ.get('BOOK_FONT',str(Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf'))
BG='#f6f1e8'; INK='#233c40'; ORANGE='#c85a34'; TEAL='#397b7b'; GRAY='#b6b9b6'
def start(title,subtitle):
 im=Image.new('RGB',(1800,1000),BG);d=ImageDraw.Draw(im)
 d.text((65,45),title,font=ImageFont.truetype(FONT,49),fill=INK)
 d.text((68,118),subtitle,font=ImageFont.truetype(FONT,27),fill=INK)
 return im,d
def txt(d,xy,s,size=30,fill=INK):d.text(xy,s,font=ImageFont.truetype(FONT,size),fill=fill)
def box(d,r,fill='white',outline=None):d.rounded_rectangle(r,radius=14,fill=fill,outline=outline,width=3)
def arrow(d,a,b,color=ORANGE):
 d.line([a,b],fill=color,width=6);ang=math.atan2(b[1]-a[1],b[0]-a[0]);L=18
 d.polygon([b,(b[0]-L*math.cos(ang-.5),b[1]-L*math.sin(ang-.5)),(b[0]-L*math.cos(ang+.5),b[1]-L*math.sin(ang+.5))],fill=color)
def save(im,name):im.save(OUT/name)

im,d=start('一件物体，三条成形路线','原创图解 · 比较的是材料流动方式，并非优劣排名')
for x,title in [(65,'增材：逐层增加'),(650,'减材：去掉多余'),(1235,'成形：重新分配')]:
 box(d,(x,200,x+500,850));txt(d,(x+25,225),title,34)
for j in range(13):
 w=240 if j<7 else 130
 d.rectangle((175,690-j*24,175+w,711-j*24),fill=ORANGE)
arrow(d,(380,310),(380,380));txt(d,(110,760),'层与层连接，内部可留空',27)
d.rectangle((730,380,1060,710),fill=GRAY);d.rectangle((850,380,1060,550),fill='white')
for j in range(6):d.arc((1090+j*13,540,1120+j*13,575),0,280,fill=ORANGE,width=4)
arrow(d,(960,310),(960,455));txt(d,(690,760),'刀具可达，决定能去哪里',27)
d.rectangle((1300,390,1660,690),fill=TEAL);d.ellipse((1360,450,1600,650),fill=BG)
arrow(d,(1470,300),(1470,380));txt(d,(1270,760),'模具、压力或流动来定形',27)
save(im,'diagram-01-routes.png')

im,d=start('打印机里，究竟是谁在“画”一层？','原创简化剖面 · 仅表示基本原理，不表示具体机型结构与比例')
for x,title in [(65,'材料挤出'),(650,'槽式光聚合'),(1235,'粉末床熔融')]:
 box(d,(x,200,x+500,860));txt(d,(x+25,228),title,35)
for j in range(7):d.rectangle((140,660-j*22,430,679-j*22),fill=ORANGE)
d.polygon([(250,340),(350,340),(320,440),(280,440)],fill=INK);d.line((300,440,300,507),fill=ORANGE,width=11)
arrow(d,(370,390),(465,390));txt(d,(100,730),'喷嘴沿路径沉积熔融材料',26)
d.rectangle((715,450,1090,680),fill='#e2b178',outline=INK,width=5)
d.rectangle((800,445,1000,470),fill=TEAL);d.rectangle((800,470,850,590),fill=TEAL)
d.line((900,340,900,438),fill=ORANGE,width=8);txt(d,(715,730),'光选择性固化液态树脂',26)
d.rectangle((1300,500,1685,690),fill='#c6c3b9',outline=INK,width=4)
for xx in range(1315,1680,25):
 for yy in range(517,682,25):d.ellipse((xx,yy,xx+5,yy+5),fill=INK)
d.rectangle((1370,500,1575,528),fill=TEAL);d.line((1610,345,1480,498),fill=ORANGE,width=6)
txt(d,(1270,730),'热能连接粉末床中的选区',26)
save(im,'diagram-02-principles.png')

im,d=start('不要把“七大工艺家族”当作七种材料','原创分类导航 · 同一材料可跨工艺，同一工艺也可能使用多种材料')
items=[('材料挤出','连续挤出丝、粒料或浆料','FFF、颗粒、直写'),('槽式光聚合','让槽内树脂的选区固化','SLA、DLP、MSLA'),('粉末床熔融','用热能连接铺好的粉末','SLS、MJF、LPBF'),('材料喷射','在目标位置喷射成形材料','多材料、全彩模型'),('粘结剂喷射','向粉末喷胶，先做出生坯','金属、砂型、陶瓷'),('定向能量沉积','送料与局部热源协同','送粉、送丝、修复'),('片材叠层','连接片材，再形成轮廓','纸、聚合物、金属箔')]
for i,(a,b,c) in enumerate(items):
 col=i%4;row=i//4;x=65+col*430;y=210+row*350
 box(d,(x,y,x+405,y+300));txt(d,(x+20,y+20),a,33,ORANGE);txt(d,(x+20,y+100),b,23);txt(d,(x+20,y+160),c,23)
txt(d,(1375,650),'材料 ≠ 工艺',38,TEAL);txt(d,(1375,715),'商品名 ≠ 新家族',26)
save(im,'diagram-03-families.png')

im,d=start('三个小结构，解释三类大限制','原创结构示意 · 设计之前，先问材料和工具能否离开')
for x,t in [(65,'支撑接触面'),(650,'封闭腔里的粉末'),(1235,'铣刀留下的内圆角')]:box(d,(x,210,x+500,880));txt(d,(x+20,240),t,32)
d.rectangle((150,420,460,460),fill=ORANGE)
for x in [180,250,320,390,440]:d.line((x,465,x,675),fill=TEAL,width=9);d.ellipse((x-7,453,x+7,467),fill=INK)
d.line((130,680,490,680),fill=INK,width=6);txt(d,(100,745),'拆除后常留下痕迹',28)
d.rounded_rectangle((740,390,1050,690),30,fill=GRAY);d.rounded_rectangle((780,430,1010,650),20,fill=BG)
for x in range(800,1000,20):
 for y in range(470,635,22):d.ellipse((x,y,x+7,y+7),fill=ORANGE)
txt(d,(690,745),'需要排粉口或清理路径',28)
d.rectangle((1325,380,1650,700),fill=GRAY)
d.rounded_rectangle((1380,430,1595,650),radius=43,fill=BG)
d.ellipse((1380,430,1466,516),outline=ORANGE,width=6);txt(d,(1270,745),'旋转刀具有有限半径',28)
save(im,'diagram-04-limits.png')

im,d=start('生坯不是成品：金属粘结剂喷射的一条典型路线','原创流程图 · 不同体系可能加入固化、浸渗或不同脱脂步骤')
stages=[('打印生坯','金属粉末＋粘结剂'),('清粉与脱脂','移除松散粉末和粘结剂'),('烧结','颗粒连接并伴随收缩'),('精加工与检验','关键表面、尺寸与缺陷')]
for i,(a,b) in enumerate(stages):
 x=65+i*430;box(d,(x,260,x+385,830));txt(d,(x+20,290),a,33,ORANGE);txt(d,(x+20,740),b,22)
 size=[220,220,180,180][i];xx=x+80;yy=470
 d.rounded_rectangle((xx,yy,xx+size,yy+170),18,fill=GRAY if i!=3 else TEAL)
 d.ellipse((xx+60,yy+40,xx+size-30,yy+130),fill=BG)
 if i<2:
  for k in range(5):d.ellipse((xx+10+k*30,yy+12,xx+16+k*30,yy+18),fill=INK)
 if i<3:arrow(d,(x+390,530),(x+425,530))
save(im,'diagram-05-greenpart.png')

im,d=start('少看一个“精度数字”，多看一条完整链','原创检验框架 · 层高、像素尺寸、定位重复性都不能独自代表零件精度')
cards=[('数字模型','单位、封闭性、壁厚\n几何误差从此处就可能开始'),('成形方向','层间性能、支撑位置\n表面与强度需要一起考虑'),('后处理','清洗、固化、热处理\n尺寸和材料状态仍会变化'),('使用与测量','量具、温度、吸湿\n按实际用途检验成品')]
for i,(a,b) in enumerate(cards):
 x=65+(i%2)*855;y=210+(i//2)*350;box(d,(x,y,x+815,y+310));txt(d,(x+25,y+25),a,36,ORANGE)
 for j,s in enumerate(b.split('\n')):txt(d,(x+25,y+110+j*55),s,30)
save(im,'diagram-06-quality.png')
print('6 diagrams generated')
