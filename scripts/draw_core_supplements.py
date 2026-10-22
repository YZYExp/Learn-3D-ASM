"""Reproducible conceptual teaching diagrams; no measured or invented data."""
from pathlib import Path
import math, os
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parents[1]/'assets/images'
FONT=os.environ.get('BOOK_FONT',str(Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf'))
BG='#f6f1e8';INK='#233c40';O='#c85a34';T='#397b7b';PALE='#dce8df';SAND='#e8d5b2';GRAY='#b6b9b6'
def text(d,p,s,n=30,c=INK):d.text(p,s,font=ImageFont.truetype(FONT,n),fill=c)
def lines(d,p,ss,n=29,c=INK,gap=48):
 for i,s in enumerate(ss):text(d,(p[0],p[1]+i*gap),s,n,c)
def arrow(d,a,b,c=O,w=7):
 d.line([a,b],fill=c,width=w);ang=math.atan2(b[1]-a[1],b[0]-a[0]);r=20
 d.polygon([b,(b[0]-r*math.cos(ang-.5),b[1]-r*math.sin(ang-.5)),(b[0]-r*math.cos(ang+.5),b[1]-r*math.sin(ang+.5))],fill=c)
def card(d,r):d.rounded_rectangle(r,24,fill='white')
def start(title,sub):
 im=Image.new('RGB',(2000,1200),BG);d=ImageDraw.Draw(im);text(d,(70,45),title,53);text(d,(73,130),sub,29)
 return im,d
def footer(d,s):text(d,(75,1120),s,25)
def save(im,name):OUT.mkdir(parents=True,exist_ok=True);im.save(OUT/name)

im,d=start('同一个受力方向，可能拉开不同的层间界面','FFF 摆放与受力 · 两个试样在图中转到同一观察方向，以便比较')
for x,title in [(70,'载荷沿层内方向'),(1030,'载荷跨越层间界面')]:
 card(d,(x,215,x+900,1030));text(d,(x+35,250),title,40)
 d.rectangle((x+190,450,x+700,650),fill=PALE,outline=INK,width=4)
 arrow(d,(x+180,550),(x+65,550));arrow(d,(x+710,550),(x+830,550))
 text(d,(x+55,600),'拉力',29,O);text(d,(x+750,600),'拉力',29,O)
for y in range(475,650,25):d.line((260,y,770,y),fill=T,width=4)
arrow(d,(480,420),(480,335),T);text(d,(500,340),'构建 Z',28,T)
lines(d,(110,750),['层面与拉力方向平行。','力主要沿层内路径传递，','仍受路径、孔隙与结合质量影响。'],31)
for x in range(1245,1730,35):d.line((x,450,x,650),fill=T,width=4)
arrow(d,(1420,370),(1550,370),T);text(d,(1400,320),'构建 Z',28,T)
d.line((1500,450,1500,650),fill=O,width=9);arrow(d,(1580,720),(1500,645));text(d,(1530,730),'一处层间界面',29,O)
lines(d,(1070,820),['拉力跨越层面；若层间结合较弱，','界面可能成为开裂位置。'],31)
footer(d,'示意非真实比例。方向影响性能；实际结果须结合材料、工艺与试样测试，不能由摆放单独决定。')
save(im,'core-fff-orientation.png')

im,d=start('三种树脂曝光方式：光怎样选中一层？','均画作典型下照式简化剖面；上照 / 下照并不由 SLA、DLP、MSLA 名称唯一决定')
for x,title in [(65,'SLA：激光扫描'),(715,'DLP：图像投影'),(1365,'MSLA：掩膜透光')]:
 card(d,(x,220,x+570,1050));text(d,(x+25,250),title,36)
 # suspended build plate and part, resin bath and transparent floor
 d.rectangle((x+267,340,x+283,405),fill=GRAY)
 d.rectangle((x+130,405,x+420,430),fill=INK)
 d.rectangle((x+60,495,x+510,715),fill=SAND)
 d.line((x+60,470,x+60,715,x+510,715,x+510,470),fill=INK,width=5)
 d.rectangle((x+210,430,x+340,705),fill=T)
 d.line((x+210,706,x+340,706),fill=O,width=10)
 text(d,(x+75,500),'树脂',26);text(d,(x+135,355),'构建平台',26)
 text(d,(x+60,731),'透明槽底',25)
 text(d,(x+360,640),'固化选区',24,O);arrow(d,(x+370,675),(x+335,703),O,4)
# laser point, scan sweep
x=65;d.rectangle((x+125,875,x+270,935),fill=INK);text(d,(x+135,886),'激光',29,'white')
d.line((x+210,875,x+285,716),fill=O,width=7);arrow(d,(x+240,800),(x+365,800),O,4)
lines(d,(x+25,970),['光点沿路径依次扫描。'],28)
# DLP projector cone
x=715;d.polygon([(x+270,880),(x+195,718),(x+360,718)],fill='#f2d0b9');d.rectangle((x+200,875,x+365,935),fill=INK);text(d,(x+215,889),'投影光机',26,'white')
lines(d,(x+25,970),['一幅层图像投向树脂。'],28)
# MSLA backlight and mask
x=1365;d.rectangle((x+120,875,x+450,930),fill=O);text(d,(x+220,885),'背光',28,'white')
for xx in range(x+140,x+450,50):arrow(d,(xx,865),(xx,815),O,4)
d.rectangle((x+120,790,x+450,810),fill=INK);d.rectangle((x+220,790,x+340,810),fill=PALE)
d.polygon([(x+220,790),(x+220,718),(x+340,718),(x+340,790)],fill='#f2d0b9')
text(d,(x+30,830),'LCD 掩膜',25);lines(d,(x+25,970),['掩膜控制哪些区域透光。'],28)
footer(d,'图中厚度、光路与部件间距均为教学夸张；固化层厚度远小于示意。不同机型结构与运动方式可不同。')
save(im,'core-resin-exposure.png')

im,d=start('SLS 与 MJF：相同的粉床，不同的选区方式','聚合物粉末床简化剖面 · 粉末为主体材料，周围未连接粉末提供支撑')
for x,title in [(70,'SLS：激光选择性供热'),(1030,'MJF：喷剂改变局部热响应')]:
 card(d,(x,220,x+900,1045));text(d,(x+30,250),title,39)
 d.rectangle((x+60,590,x+840,825),fill='#ebe8df',outline=INK,width=4)
 # all beads then joined selected zone
 for yy in range(608,815,29):
  for xx in range(x+75,x+825,29):d.ellipse((xx,yy,xx+12,yy+12),fill=GRAY)
 d.rounded_rectangle((x+260,590,x+620,625),7,fill=O)
 d.rectangle((x+280,626,x+595,750),fill=T)
 text(d,(x+65,780),'未连接粉末',25);text(d,(x+295,675),'已成形区域',28,'white')
 text(d,(x+280,845),'当前层的选区',28,O)
# laser
x=70;d.rectangle((x+520,365,x+735,425),fill=INK);text(d,(x+550,376),'激光光源',28,'white')
d.line((x+570,425,x+440,588),fill=O,width=8);arrow(d,(x+355,520),(x+530,520),T,5)
lines(d,(x+40,915),['预热的粉床上，激光扫描目标区域；','选区获得热能，粉末颗粒连接。'],30)
# agents and IR separate bands / consecutive actions
x=1030;text(d,(x+55,345),'① 喷功能剂',30,O);text(d,(x+450,345),'② 红外供热',30,O)
d.rectangle((x+95,410,x+320,450),fill=INK)
for xx in [x+145,x+205,x+265]:
 d.ellipse((xx,480,xx+14,500),fill=O);arrow(d,(xx+7,520),(xx+7,580),O,4)
d.rectangle((x+480,410,x+770,450),fill=O)
for xx in range(x+500,x+770,55):arrow(d,(xx,465),(xx,570),O,4)
lines(d,(x+40,915),['熔融剂配合红外热能，使选区熔合；','细化剂帮助控制边界。液体不是胶水。'],29)
footer(d,'两幅均省略铺粉、平台下降与冷却等循环步骤；MJF 图把先后动作并列展开，不表示一次静态曝光的机头布局。')
save(im,'core-sls-mjf.png')

im,d=start('“加了纤维”以后，纤维究竟在哪里？','短切与连续增强 · 基体聚合物包围并连接纤维，纤维形态与路径共同影响受力')
for x,title in [(70,'短切纤维：混在基体里'),(1030,'连续纤维：沿规划路径铺放')]:
 card(d,(x,220,x+900,1045));text(d,(x+35,255),title,39)
 d.rounded_rectangle((x+70,410,x+830,730),35,fill=PALE,outline=INK,width=4)
# deterministic short segments
for r in range(5):
 for c in range(9):
  xx=190+c*76+(r%2)*17;yy=450+r*52;ang=[-.3,.15,.4,-.12][(r+c)%4]
  d.line((xx,yy,xx+42*math.cos(ang),yy+42*math.sin(ang)),fill=O,width=9)
lines(d,(110,805),['许多短纤维分散在聚合物中。','流动可能带来取向，不能假定完全随机。','不形成贯穿整个零件的连续纤维束。'],29)
# continuous paths rounded around obstacle, print planar path
for i in range(5):
 d.rounded_rectangle((1140+i*20,445+i*19,1815-i*20,695-i*19),radius=55,outline=O,width=8)
d.ellipse((1435,520,1515,600),fill='white',outline=INK,width=3)
lines(d,(1070,805),['长纤维束沿可制造的路线连续铺放。','通常与基体聚合物协同成形；','孔、转角与铺放方向会约束增强路线。'],29)
footer(d,'仅示意局部纤维结构，非真实比例。两者都不是“各方向自动同样强”；性能须看配方、含量、路径和成形质量。')
save(im,'core-fiber-forms.png')

im,d=start('强度、刚度、韧性：三种不同的问题','定性概念图 · 不代表任何材料的实测曲线或排名，不给出虚构性能数值')
for x,t in [(65,'强度：何时破坏？'),(715,'刚度：变形多少？'),(1365,'韧性：吸收多少能量？')]:
 card(d,(x,220,x+570,1050));text(d,(x+25,255),t,34)
# strength tensile specimen crack
x=65;d.rectangle((x+125,490,x+440,610),fill=PALE,outline=INK,width=3)
arrow(d,(x+115,550),(x+35,550));arrow(d,(x+450,550),(x+535,550))
d.line([(x+282,490),(x+263,525),(x+295,550),(x+271,580),(x+285,610)],fill=O,width=7)
lines(d,(x+30,750),['关注达到屈服或断裂时，','材料能承受多大应力。','','需指明：拉伸、压缩，','以及具体采用的破坏判据。'],28,gap=45)
# stiffness cantilever same geometry/load small vs large deflection
x=715
for yy in [440,620]:
 d.rectangle((x+65,yy-30,x+100,yy+90),fill=INK)
 d.line((x+100,yy,x+470,yy),fill=GRAY,width=3)
d.line((x+100,440,x+230,442,x+350,451,x+470,465),fill=T,width=14)
d.line((x+100,620,x+230,632,x+350,665,x+470,715),fill=O,width=14)
arrow(d,(x+470,400),(x+470,457),T,5);arrow(d,(x+470,650),(x+470,707),O,5)
text(d,(x+110,490),'变形小 → 刚度较大',27,T)
lines(d,(x+30,795),['同几何、同约束、同载荷，','变形越小，结构刚度越大。','','材料刚度常用弹性模量描述；','零件刚度还受形状影响。'],27,gap=42)
# toughness stress strain concept curve polygon area
x=1365;ox=x+90;oy=685
arrow(d,(ox,oy),(x+510,oy),INK,4);arrow(d,(ox,oy),(ox,405),INK,4)
points=[(ox,oy),(ox+50,560),(ox+100,515),(ox+180,490),(ox+260,470),(ox+325,455)]
d.polygon(points+[(ox+325,oy)],fill='#efd1bf');d.line(points,fill=O,width=7)
d.ellipse((ox+317,447,ox+333,463),fill=O)
text(d,(x+330,405),'断裂',25,O);text(d,(x+20,365),'应力',26);text(d,(x+430,700),'应变',26)
text(d,(x+160,590),'吸能',31,O)
lines(d,(x+30,795),['拉伸示意：到断裂前，','应力—应变曲线下的面积，','表示单位体积吸收的能量。','','面积是概念示意，非材料数据。'],27,gap=42)
footer(d,'材料试验的应力、应变与零件的力、位移需区分。测试标准、环境、含水状态及打印方向都会影响结果。')
save(im,'core-material-properties.png')
print('5 core teaching diagrams generated')
