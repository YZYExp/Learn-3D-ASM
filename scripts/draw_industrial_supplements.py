from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, json, random
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets/images'
BG='#f6f1e8'; INK='#233c40'; ACC='#c85a34'; MUT='#a9b9b3'; LIGHT='#e2e7df'; GOLD='#d7ae64'; WHITE='#fffdf8'
FONT='/root/.local/share/fonts/NotoSansSC-Regular.ttf'
W,H=2200,1300
F={s:ImageFont.truetype(FONT,s) for s in [24,28,30,32,34,38,42,46,54,64]}
def text(x,y,t,s=34,c=INK): d.text((x,y),t,font=F[s],fill=c)
def lines(x,y,ts,s=32,dy=48,c=INK):
 for i,t in enumerate(ts):text(x,y+i*dy,t,s,c)
def rect(box,fill=LIGHT,outline=INK,width=4,r=0):
 if r:d.rounded_rectangle(box,r,fill=fill,outline=outline,width=width)
 else:d.rectangle(box,fill=fill,outline=outline,width=width)
def line(pts,c=INK,w=5):d.line(pts,fill=c,width=w,joint='curve')
def arrow(a,b,c=ACC,w=7):
 line([a,b],c,w);ang=math.atan2(b[1]-a[1],b[0]-a[0]);p=22
 d.polygon([b,(b[0]-p*math.cos(ang-.5),b[1]-p*math.sin(ang-.5)),(b[0]-p*math.cos(ang+.5),b[1]-p*math.sin(ang+.5))],fill=c)
def circle(x,y,r,fill=ACC,outline=None,w=3):d.ellipse((x-r,y-r,x+r,y+r),fill,outline,width=w)
def rotate(cx,cy,r=58):
 d.arc((cx-r,cy-r,cx+r,cy+r),30,310,fill=ACC,width=7); a=math.radians(310);p=(cx+r*math.cos(a),cy+r*math.sin(a));arrow((p[0]-20,p[1]-15),p)
def start(title,sub):
 global im,d
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im);text(80,48,title,64);text(82,144,sub,32);line([(80,210),(2120,210)],MUT,3)
def panel(x,y,w,h,title):
 rect((x,y,x+w,y+h),WHITE,MUT,2,22)
 size=42
 while d.textlength(title,font=ImageFont.truetype(FONT,size))>w-56: size-=1
 d.text((x+28,y+22),title,font=ImageFont.truetype(FONT,size),fill=INK)
def end(name,note):
 line([(80,1190),(2120,1190)],MUT,3);text(82,1220,note,28);im.save(OUT/name,optimize=True)
def block(x,y,w=220,h=120):rect((x,y,x+w,y+h),MUT)
def part(x,y,scale=1):
 pts=[(x,y+110*scale),(x,y),(x+90*scale,y),(x+90*scale,y+65*scale),(x+190*scale,y+65*scale),(x+190*scale,y+110*scale)]
 d.polygon(pts,fill=MUT,outline=INK,width=4)
# 1 metal feed distinction
start('金属如何到达熔池？','粉床先铺满一层；DED 把粉末或丝材直接送到局部结合区。三种简化剖面，非比例。')
for x,t in [(80,'LPBF · 激光粉床熔融'),(775,'送粉激光 DED'),(1470,'送丝 DED · 激光示例')]:panel(x,250,650,850,t)
# LPBF
rect((130,675,680,870),LIGHT);random.seed(42)
for i in range(240):circle(random.randint(145,665),random.randint(690,852),2,MUT)
rect((280,755,525,866),INK);rect((280,680,525,755),MUT);rect((130,870,680,905),INK)
rect((300,390,495,460),MUT);line([(397,460),(397,680)],ACC,12);circle(397,680,18,ACC);arrow((430,600),(555,600))
rect((155,600,205,668),GOLD);arrow((215,630),(320,630));text(135,530,'刮刀铺粉',30);text(430,514,'激光扫描',30)
lines(130,940,['材料：预铺金属粉层','选择性熔化；平台逐层下降'],30);arrow((637,910),(637,950),INK)
# DED powder
block(825,825,550,75);rect((930,780,1190,824),MUT);rect((1015,400,1185,475),MUT)
line([(1100,475),(1100,778)],ACC,10);d.polygon([(930,470),(990,450),(1088,770),(1060,770)],fill=GOLD);d.polygon([(1270,470),(1210,450),(1112,770),(1140,770)],fill=GOLD)
text(825,535,'粉末流',30);text(1120,515,'激光',30);circle(1100,780,18);arrow((1170,735),(1300,735));text(835,902,'基体 / 已沉积层',30)
lines(825,965,['粉末随喷头送入熔池','通常不需要整层粉床'],30)
# wire
block(1520,825,550,75);rect((1620,780,1890,824),MUT);rect((1780,390,1930,460),MUT);line([(1855,460),(1785,780)],ACC,10);line([(1560,420),(1630,500),(1780,780)],GOLD,15);circle(1780,780,18);text(1515,540,'连续丝材',30);text(1890,580,'激光',30);arrow((1870,735),(1990,735))
lines(1520,965,['丝材直接送入熔池','也有电弧、电子束等 DED 路线'],30)
end('supp-industrial-metal-feed.png','读图关键：材料供给方式 ≠ 能量源。送丝 DED 并不都使用激光；图中熔池均作放大示意。')
# 2 postprocess
start('金属打印结束，零件制造还没有结束','以一种 LPBF 路线为例：后处理与检验共同决定零件能否交付。')
steps=[('① 冷却与清粉',['回收松散粉末','确认内腔可清理']),('② 热处理',['示例：在基板上去应力','其他热处理按材料制定']),('③ 分离与去支撑',['从基板分离','移除支撑并修整']),('④ 机加工与表面处理',['加工配合面、螺纹等','按需要磨削、喷丸等']),('⑤ 检验与放行',['尺寸、表面与内部缺陷','材料性能及追溯记录'])]
for i,(title,ts) in enumerate(steps):
 x=80+i*414;panel(x,300,385,690,title);lines(x+25,790,ts,28,48)
 if i<4:arrow((x+389,630),(x+410,630),INK,4)
 if i==0:
  part(x+90,510,.85);rect((x+55,620,x+330,650),INK)
  for z in range(25):circle(x+60+z*11,690+z%3*10,3,GOLD)
 elif i==1:
  rect((x+55,455,x+330,710),LIGHT,INK,5,12);rect((x+82,500,x+303,675),BG);part(x+110,535,.65)
  for xx in [110,180,250]:line([(x+xx,440),(x+xx-10,415),(x+xx+10,390),(x+xx,365)],ACC,5)
 elif i==2:
  part(x+90,510,.85);line([(x+80,660),(x+290,660)],ACC,5)
  for xx in range(115,260,30):line([(x+xx,605),(x+xx,650)],MUT,7)
  arrow((x+315,650),(x+315,590))
 elif i==3:
  part(x+100,570,.8);rect((x+125,420,x+185,570),INK);rotate(x+265,490,45);arrow((x+70,710),(x+300,710))
 else:
  part(x+95,550,.8);line([(x+65,525),(x+320,525)],INK,7);line([(x+65,525),(x+65,640)],INK,7);line([(x+320,525),(x+320,640)],INK,7);text(x+80,700,'尺寸 / 无损 / 试样',28)
rect((80,1040,2120,1140),LIGHT,MUT,2,14);text(110,1062,'顺序与模块随合金、几何和规范改变；热处理可不止一次，检验也应贯穿制造过程。',34)
end('supp-industrial-metal-postprocess.png','示例不是统一操作规程。并非每个零件都需要全部模块；具体顺序应由经过验证的工艺路线确定。')
# 3 sheet jet
start('一层可以是液滴，也可以是一张箔','两种增材家族的供料与结合方式不同。左为 PolyJet 类示例，右为金属 UAM 示例。')
panel(80,270,980,850,'材料喷射：喷出的就是成形材料');panel(1100,270,1020,850,'片材叠层：UAM 超声金属箔结合')
rect((190,430,710,515),INK);text(215,442,'树脂喷头',38,WHITE);rect((760,435,900,520),GOLD);text(775,445,'UV',38)
for x,c in [(260,ACC),(340,GOLD),(420,ACC),(500,MUT),(580,MUT)]:
 for y in [570,620,670]:circle(x,y,9,c)
for j in range(5):rect((200,760-j*18,820,777-j*18),ACC if j%2 else MUT,INK,2)
for x in [780,820,860]:arrow((x,550),(x-60,695),GOLD,5)
text(190,835,'液滴落位 → UV 固化 → 逐层叠加',34);lines(145,925,['多材料 / 支撑材料可分别喷射','不是把黏结剂喷到整床粉末里'],32)
for j in range(6):rect((1220,790-j*24,2010,813-j*24),MUT if j%2 else LIGHT,INK,3)
line([(1260,560),(1490,560),(1610,635),(1995,635)],GOLD,15);circle(1690,575,85,INK);circle(1690,575,35,LIGHT);arrow((1690,390),(1690,475));text(1775,440,'下压力',30)
arrow((1560,575),(1510,575));arrow((1810,575),(1860,575));text(1450,365,'横向高频振动',34);text(1220,850,'金属箔 + 压力 + 超声振动',34)
lines(1165,925,['固态结合；不必把金属整体熔化','可与 CNC 切削交替构造内外形状'],32)
end('supp-industrial-jet-sheet.png','材料喷射与片材叠层均有不同实现；右图特指 UAM，不能把所有片材叠层都理解成超声焊接。')
# 4 machining
start('车、铣、钻、磨：谁在旋转，谁在进给？','四个典型运动组合。墨绿表示工件或工具；陶土箭头表示运动，实际设备可有更多轴。')
for x,y,t in [(80,270,'车削 · 工件旋转'),(1140,270,'铣削 · 刀具旋转'),(80,720,'钻削 · 钻头旋转并进给'),(1140,720,'平面磨削 · 砂轮旋转')]:panel(x,y,980,400,t)
# turn
rect((170,435,580,550),MUT);d.ellipse((125,435,215,550),INK);d.ellipse((535,435,625,550),MUT,INK,4);rotate(330,475,80);d.polygon([(680,585),(540,550),(620,550)],fill=INK);arrow((800,575),(650,575));text(700,455,'车刀进给',30);text(190,590,'典型用途：轴、回转表面',30)
# mill
block(1260,530,570,65);rect((1445,390,1525,530),INK)
for yy in range(395,525,22):line([(1445,yy+18),(1525,yy)],LIGHT,4)
rotate(1620,440,50);arrow((1730,625),(1920,625));text(1740,435,'刀具旋转',30);text(1250,615,'工件相对进给',30)
# drill
block(180,1000,470,55);d.polygon([(360,835),(430,835),(430,980),(395,1010),(360,980)],fill=INK)
for yy in range(850,970,25):line([(360,yy+20),(430,yy)],LIGHT,5)
rotate(520,890,50);arrow((700,850),(700,990));text(740,900,'轴向进给',30);text(180,1070,'典型用途：孔；后续可扩、铰、镗',30)
# grind
block(1270,1020,620,55);circle(1560,940,90,INK);circle(1560,940,34,LIGHT);rotate(1710,910,53)
for a in range(0,360,18):xx=1560+82*math.cos(math.radians(a));yy=940+82*math.sin(math.radians(a));circle(xx,yy,3,GOLD)
arrow((1810,1100),(1990,1100));text(1260,1085,'工件往复进给',30);text(1800,875,'磨粒切削',30)
end('supp-industrial-cutting-motion.png','示意只画主运动与一种进给。车削也可使用动力刀具；磨削同样存在外圆、内圆等多种运动组合。')
# 5 nontraditional
start('电火花、激光与水刀：拿走材料的机制不同','四种简化剖面。不要把线切割当作锯切，也不要把激光或水刀的适用材料归结为导电性。')
for i,t in enumerate(['成形电火花 · Sinker EDM','线切割 · Wire EDM','激光切割','磨料水射流切割']):panel(80+i*520,280,490,840,t)
# sinker
x=80;rect((x+60,525,x+430,810),LIGHT);rect((x+60,640,x+430,810),MUT);rect((x+170,640,x+320,740),BG,BG);d.polygon([(x+190,430),(x+300,430),(x+300,680),(x+280,715),(x+210,715),(x+190,680)],fill=GOLD);arrow((x+370,445),(x+370,580))
for xx in range(190,301,25):line([(x+xx,725),(x+xx-7,740),(x+xx+8,748)],ACC,4)
lines(x+30,860,['成形电极复制型腔','间隙内脉冲放电','典型需导电工件','浸在工作液中'],30,47)
# wire
x=600;rect((x+65,600,x+430,790),MUT);rect((x+240,600,x+265,790),BG,BG);line([(x+252,400),(x+252,835)],GOLD,8);rect((x+210,420,x+295,465),INK);rect((x+210,835,x+295,880),INK);arrow((x+320,470),(x+320,550));arrow((x+90,565),(x+205,565));text(x+65,470,'轮廓进给',28)
for yy in range(620,780,35):line([(x+240,yy),(x+225,yy+8),(x+241,yy+15)],ACC,4)
lines(x+30,900,['细丝电极沿轮廓放电','典型需导电工件','图为连续送丝示例'],30,47)
# laser
x=1120;rect((x+60,685,x+430,800),MUT);rect((x+240,680,x+265,805),BG,BG);d.polygon([(x+180,410),(x+325,410),(x+280,510),(x+225,510)],fill=INK);line([(x+252,515),(x+252,807)],ACC,10);arrow((x+340,580),(x+410,580));text(x+65,560,'光束 + 辅助气体',28)
for xx in [220,250,280]:arrow((x+xx,830),(x+xx-15,875),ACC,4)
lines(x+30,920,['局部热过程形成割缝','不要求材料导电','需匹配材料、波长与参数'],30,47)
# water
x=1640;rect((x+60,685,x+430,800),MUT);rect((x+240,680,x+270,805),BG,BG);d.polygon([(x+200,410),(x+310,410),(x+277,535),(x+233,535)],fill=INK);line([(x+255,535),(x+255,880)],'#6e9caa',15)
for yy in range(550,870,24):circle(x+253,yy,4,GOLD)
arrow((x+340,580),(x+410,580));text(x+48,560,'高压水 + 磨料',28)
lines(x+30,920,['高速射流与磨粒侵蚀','不要求材料导电','仍需考虑锥度与脆性损伤'],30,47)
end('supp-industrial-nontraditional-cutting.png','均为原理示意，不作参数指南。电火花间隙与割缝被放大；材料适用性还受厚度、质量和设备限制。')
# 6 ceramic
start('陶瓷光成形：打印机先做出一个生坯','以 LCM 类陶瓷光聚合路线为例。陶瓷颗粒最终致密化，依靠后续热过程。')
items=[('① 光成形',['陶瓷颗粒 + 光敏体系','曝光固定逐层几何']),('② 清洗与生坯',['清除未固化浆料','生坯含有机结合相']),('③ 脱脂',['受控移除有机组分','避免裂纹与变形']),('④ 烧结',['陶瓷颗粒结合、致密化','产生收缩；再按需精加工'])]
for i,(t,ts) in enumerate(items):
 x=80+i*520;panel(x,300,490,770,t);lines(x+25,885,ts,28,50)
 if i<3:arrow((x+495,670),(x+515,670),INK,4)
 if i==0:
  rect((x+60,680,x+425,780),GOLD);rect((x+190,485,x+300,680),MUT);line([(x+120,820),(x+240,720),(x+355,820)],ACC,7);text(x+95,420,'曝光 / 浆料',32)
 elif i==1:
  part(x+120,565,1.2)
  for j in range(18):
   px=(j*29)%200; py=(j*37)%110
   if px<95 or py>65: circle(x+130+px,580+py,4,GOLD)
  text(x+95,765,'陶瓷 + 有机相',30)
 elif i==2:
  part(x+120,565,1.2)
  for yy in [430,470,510]:arrow((x+210,yy+30),(x+210,yy),ACC,4)
  for j in range(18):
   px=(j*29)%200; py=(j*37)%110
   if px<95 or py>65: circle(x+130+px,580+py,4,BG)
  text(x+90,765,'热处理方案受控',30)
 else:
  part(x+145,590,.85);d.rectangle((x+120,565,x+348,697),outline=MUT,width=3);text(x+83,765,'虚框：生坯外形参照',28)
rect((80,1100,2120,1160),LIGHT,MUT,2,12);text(112,1105,'收缩只是定性表达：不表示固定收缩率，也不保证各方向收缩完全相同。',32)
end('supp-industrial-ceramic-chain.png','不同浆料、设备和陶瓷体系的清洗、脱脂及烧结程序不同；不能把光固化完成当作最终陶瓷完成。')
print('Generated 6 industrial supplementary diagrams')
