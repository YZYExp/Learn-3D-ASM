"""Original application illustrations, not branded parts or validated process plans."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import os,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/images'
FONT=os.environ.get('BOOK_FONT',str(Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf'))
BG='#f6f1e8';INK='#233c40';RUST='#c85a34';TEAL='#97b8b4';PALE='#dce7e2';LIGHT='#dfd8ca'
W,H=2200,1400

def text(d,xy,s,n=34,fill=INK):d.text(xy,s,font=ImageFont.truetype(FONT,n),fill=fill)
def line(d,pts,fill=INK,w=4):d.line(pts,fill=fill,width=w,joint='curve')
def arrow(d,a,b,fill=RUST,w=5):
 line(d,[a,b],fill,w);theta=math.atan2(b[1]-a[1],b[0]-a[0]);r=18
 d.polygon([b,(b[0]-r*math.cos(theta-.5),b[1]-r*math.sin(theta-.5)),(b[0]-r*math.cos(theta+.5),b[1]-r*math.sin(theta+.5))],fill=fill)
def start(title,sub):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im);text(d,(80,55),title,56);text(d,(84,145),sub,29);line(d,[(80,208),(2120,208)],LIGHT,2);return im,d
def panel(d,box,title):
 d.rounded_rectangle(box,24,fill='white');text(d,(box[0]+30,box[1]+22),title,37)
def save(im,name):im.save(OUT/name,optimize=True)

def features():
 im,d=start('先找功能面，再选加工方法','四种典型任务：几何轮廓只是起点，交付要求决定后续工序。')
 boxes=[(80,250,1080,730),(1120,250,2120,730),(80,770,1080,1250),(1120,770,2120,1250)]
 for b,t in zip(boxes,['轴承套圈：回转与接触','外壳与孔板：安装与定位','线切割模具：贯通轮廓','蚀刻薄片：薄、平、细密']):panel(d,b,t)
 # front annulus plus section, precise simple silhouette
 d.ellipse((150,360,420,630),fill=TEAL,outline=INK,width=5);d.ellipse((230,440,340,550),fill='white',outline=RUST,width=5)
 arrow(d,(500,380),(383,389));text(d,(510,355),'外圆',30)
 arrow(d,(500,480),(338,482));text(d,(510,458),'内孔',30)
 arrow(d,(500,590),(380,580));text(d,(510,565),'端面 / 滚道另有要求',30)
 text(d,(150,657),'车削 → 热处理 → 相应磨削与精整',30)
 # machined casing top view with pocket and bores
 d.rounded_rectangle((1180,370,1570,605),16,fill=TEAL,outline=INK,width=5)
 d.rounded_rectangle((1240,415,1510,560),35,fill='white',outline=RUST,width=5)
 for x in [1200,1550]:
  for y in [390,585]:d.ellipse((x-9,y-9,x+9,y+9),fill='white',outline=INK,width=3)
 text(d,(1620,382),'凹槽：刀具可达',30);text(d,(1620,447),'安装面：基准',30);text(d,(1620,512),'孔：直径与位置',30)
 text(d,(1180,657),'铣削与钻孔常在同一条工艺链中',30)
 # EDM plate through contour with start hole and wire
 d.rectangle((150,900,470,1135),fill=TEAL,outline=INK,width=4)
 pts=[(225,960),(385,960),(410,1005),(385,1050),(225,1050),(200,1005)]
 d.polygon(pts,fill='white',outline=INK,width=4)
 d.ellipse((226,980,252,1006),outline=RUST,width=4)
 line(d,[(239,993),(275,960),(385,960),(410,1005)],RUST,5)
 text(d,(525,905),'封闭内轮廓先穿丝',30);text(d,(525,975),'拐角仍受丝与间隙限制',30);text(d,(525,1045),'检查轮廓与表层状态',30)
 text(d,(150,1176),'典型任务：精冲与精密冲压模具部件',30)
 # photoetched plate with multiple slots and central opening, no assumed scale
 d.polygon([(1180,924),(1540,900),(1590,1110),(1230,1134)],fill=TEAL,outline=INK,width=4)
 for y in [965,1015,1065]:
  for x in [1265,1360,1455]:d.rounded_rectangle((x,y,x+57,y+17),7,fill='white')
 text(d,(1640,910),'轮廓 / 厚度',30);text(d,(1640,980),'平整 / 边缘',30);text(d,(1640,1050),'残留与清洁',30)
 text(d,(1180,1176),'适合比较：薄垫片、网片与细密轮廓',30)
 text(d,(80,1315),'原创教学示意，不按比例；不对应特定品牌零件图纸，也不表示通用验收公差。',29)
 save(im,'case-subtractive-part-features.png')

def channel(d,x,y,stage):
 # U-shaped open section, only a conceptual access geometry.
 d.rectangle((x,y+200,x+470,y+350),fill=TEAL,outline=INK,width=4)
 d.rectangle((x,y+30,x+90,y+200),fill=TEAL,outline=INK,width=4)
 d.rectangle((x+380,y+30,x+470,y+200),fill=TEAL,outline=INK,width=4)
 if stage==1:
  # A simplified end mill can reach the floor of the open channel.
  d.rectangle((x+207,y-70,x+262,y+177),fill=LIGHT,outline=INK,width=4)
  for a in range(4):line(d,[(x+208,y+85+a*23),(x+260,y+115+a*23)],INK,3)
  arrow(d,(x+320,y-30),(x+320,y+137))
  line(d,[(x+91,y+199),(x+379,y+199)],RUST,7)
 elif stage==2:
  for yy in [y-7,y-43,y-79]:
   d.rectangle((x,yy,x+90,yy+34),fill=RUST,outline=BG,width=2)
   d.rectangle((x+380,yy,x+470,yy+34),fill=RUST,outline=BG,width=2)
  arrow(d,(x+255,y-160),(x+400,y-95))
 else:
  d.rectangle((x,y-20,x+470,y+65),fill=TEAL,outline=INK,width=4)
  line(d,[(x,y-20),(x+470,y-20)],RUST,7)
  # tool stays outside the enclosed channel
  d.rectangle((x+190,y-170,x+245,y-42),fill=LIGHT,outline=INK,width=4)
  arrow(d,(x+300,y-135),(x+430,y-135))

def hybrid():
 im,d=start('有些表面，必须在封闭前加工','混合制造的关键问题：哪一步之后，刀具就再也无法接近这个表面？')
 cards=[(80,260,730,1190),(775,260,1425,1190),(1470,260,2120,1190)]
 titles=['① 先处理开放内表面','② 增材过程中安排加工','③ 完成后处理外部基准']
 for i,(b,t) in enumerate(zip(cards,titles)):
  panel(d,b,t);x=b[0]+90;y=650;channel(d,x,y,i+1)
 texts=[['在内部仍开放时，','加工需要的通道表面。','标明基准与后续余量。'],['材料逐步增加，','工序随可达性重新安排。','封口方式须单独设计。'],['内部封闭后，','常规刀具可能无法到达。','外部关键面仍需检验。']]
 for b,ls in zip(cards,texts):
  for j,s in enumerate(ls):text(d,(b[0]+40,1000+j*52),s,31)
 text(d,(80,1260),'橙色：本图关注的加工面或新增材料。示意只解释可达性，不是可直接执行的通道打印路线。',28)
 text(d,(80,1310),'另行验证：结构成形、材料结合、热影响、内腔清理，以及最终几何与功能。',28)
 save(im,'case-subtractive-hybrid-access.png')

if __name__=='__main__':features();hybrid()
