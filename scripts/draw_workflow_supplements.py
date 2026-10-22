#!/usr/bin/env python3
"""Original, qualitative teaching figures. Geometry and labels are reproducible."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, json
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets/images'
BG='#f6f1e8'; INK='#233c40'; RUST='#c85a34'; LIGHT='#dfd8ca'; TEAL='#97b8b4'; PALE='#dce7e2'; GOLD='#d5ac5d'
FONT='/root/.local/share/fonts/NotoSansSC-Regular.ttf'
W,H=2100,1250

def font(n): return ImageFont.truetype(FONT,n)
def text(d,xy,s,n=32,fill=INK,anchor=None): d.text(xy,s,font=font(n),fill=fill,anchor=anchor)
def line(d,pts,fill=INK,width=4): d.line(pts,fill=fill,width=width,joint='curve')
def arrow(d,a,b,fill=RUST,width=5):
 line(d,[a,b],fill,width); ang=math.atan2(b[1]-a[1],b[0]-a[0]); r=18
 d.polygon([b,(b[0]-r*math.cos(ang-.48),b[1]-r*math.sin(ang-.48)),(b[0]-r*math.cos(ang+.48),b[1]-r*math.sin(ang+.48))],fill=fill)
def start(title,sub):
 im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); text(d,(85,55),title,56); text(d,(88,145),sub,29)
 line(d,[(85,211),(2015,211)],LIGHT,2); return im,d

def footer(d,s): text(d,(85,1170),s,26)
def save(im,name): im.save(OUT/name,optimize=True)

def cylinder(d,cx,cy,mode):
 rx,ry,h=190,65,315
 if mode=='solid':
  d.rectangle((cx-rx,cy-h,cx+rx,cy),fill=TEAL); d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=TEAL,outline=INK,width=4)
  d.rectangle((cx-rx,cy-h,cx+rx,cy),fill=TEAL); line(d,[(cx-rx,cy-h),(cx-rx,cy)],INK);line(d,[(cx+rx,cy-h),(cx+rx,cy)],INK)
  d.arc((cx-rx,cy-ry,cx+rx,cy+ry),0,180,fill=INK,width=4);d.ellipse((cx-rx,cy-h-ry,cx+rx,cy-h+ry),fill=PALE,outline=INK,width=4)
 elif mode=='mesh':
  # Polygonal prism made of triangular facets, matching the smooth cylinder's envelope.
  n=12; top=[(cx+rx*math.cos(i*2*math.pi/n),cy-h+ry*math.sin(i*2*math.pi/n)) for i in range(n)]
  bot=[(x,y+h) for x,y in top]
  for i in range(n//2):
   j=(i+1)%n; d.polygon([top[i],top[j],bot[j],bot[i]],fill=TEAL,outline=INK); line(d,[top[i],bot[j]],INK,3)
  d.polygon(top,fill=PALE,outline=INK)
  for p in top:line(d,[(cx,cy-h),p],INK,3)
  line(d,top+[top[0]],INK,4)
 else:
  for k in range(12):
   y=cy-k*h/11
   d.ellipse((cx-rx,y-ry,cx+rx,y+ry),outline=RUST,width=4)
  # Actual planar cross-section inset; wall loops + diagonal infill.
  y=930; r=125
  d.ellipse((cx-r,y-r,cx+r,y+r),fill=BG,outline=INK,width=4)
  d.ellipse((cx-r+14,y-r+14,cx+r-14,y+r-14),outline=RUST,width=4)
  for off in range(-120,121,28):
   # Clip diagonal infill to inner circle.
   pts=[]
   for xx in range(-100,101):
    yy=xx+off
    if xx*xx+yy*yy<98*98:pts.append((cx+xx,y+yy))
   if len(pts)>1:line(d,[pts[0],pts[-1]],TEAL,3)
  arrow(d,(cx+rx+15,cy-h+30),(cx+rx-20,cy-h+70)); text(d,(cx-146,1085),'单层：外壁与填充路径',26)

def data_fig():
 im,d=start('同一个圆柱，三种数字表达','几何模型 → 表面离散 → 逐层制造指令；图中层距与网格为便于观察而放大。')
 for x,title,mode in [(380,'CAD 实体','solid'),(1030,'STL 三角网格','mesh'),(1690,'切片与路径','slice')]:
  text(d,(x,263),title,39,anchor='mt');cylinder(d,x,735,mode)
 arrow(d,(640,500),(760,500));arrow(d,(1290,500),(1410,500))
 text(d,(380,900),'圆柱面与封闭体积',30,anchor='mt');text(d,(380,950),'可带尺寸、参数与建模关系',26,anchor='mt')
 text(d,(1030,900),'三角片近似曲面',30,anchor='mt');text(d,(1030,950),'这里显示粗网格；并非打印层',26,anchor='mt')
 footer(d,'原创几何示意｜STL 通常不统一记录单位、颜色与材料；3MF 可记录更丰富的制造信息。')
 save(im,'supp-workflow-01-cad-mesh-slice.png')

def bracket(d,x,y,raw=False,finish=False):
 # Identical front silhouette and isometric depth across all process states.
 pts=[(x,y),(x+340,y),(x+340,y-65),(x+100,y-65),(x+100,y-300),(x,y-300)]
 shift=(52,-35);top=[(x,y-300),(x+100,y-300),(x+152,y-335),(x+52,y-335)]
 d.polygon([(a+52,b-35) for a,b in pts],fill=LIGHT,outline=INK)
 d.polygon(pts,fill='#cba38e',outline=INK,width=4);d.polygon(top,fill=PALE,outline=INK,width=4)
 if True:
  for yy in range(y-288,y-10,18):
   end=x+93 if yy<y-65 else x+330; line(d,[(x+7,yy),(end,yy)],'#a77863',2)
 if raw:
  d.rectangle((x+100,y-83,x+340,y-65),fill=RUST)
  d.rectangle((x+100,y-83,x+340,y-65),outline=RUST,width=3)
 else: line(d,[(x+100,y-65),(x+340,y-65)],TEAL,10)
 d.ellipse((x+26,y-236,x+75,y-187),fill=BG,outline=INK,width=4)
 d.ellipse((x+200,y-48,x+258,y-15),fill=BG,outline=INK,width=4)

def hybrid_fig():
 im,d=start('同一个支架：加出体积，减出基准，再测量','示意一种分工方式；打印路线、加工余量、热处理和检测方案须按材料与用途确定。')
 xs=[150,835,1510]
 for x,t in zip(xs,['① 近净成形','② 定位与精加工','③ 检查关键尺寸']):text(d,(x,270),t,38)
 for i,x in enumerate(xs):bracket(d,x,790,raw=i<2,finish=i==2)
 # allowance and build platform
 line(d,[(120,824),(560,824)],INK,8);text(d,(150,912),'层纹仍可见；关键面预留余量',28)
 arrow(d,(470,680),(435,707));text(d,(240,1010),'陶土色薄层＝待切除材料',27,fill=RUST)
 # Mill end cutter at second's seat
 d.rectangle((1065,420,1125,638),fill=LIGHT,outline=INK,width=4)
 for xx in range(1070,1120,14):line(d,[(xx,565),(xx+10,635)],INK,3)
 arrow(d,(1010,475),(1160,475));arrow(d,(1095,651),(1095,701));text(d,(835,912),'刀具接近安装面；夹具约束零件',28)
 d.rectangle((820,800,920,845),fill=INK);d.rectangle((1110,800,1200,845),fill=INK)
 # probe with measurement line above top span
 line(d,[(1530,365),(1530,433),(1800,433),(1800,698)],INK,5)
 d.ellipse((1789,693,1811,715),fill=RUST);line(d,[(1665,520),(1842,520)],RUST,3)
 arrow(d,(1680,520),(1775,520));text(d,(1480,912),'测头接触加工面；核对图纸要求',26)
 arrow(d,(600,650),(730,650));arrow(d,(1280,650),(1410,650))
 footer(d,'原创工艺示意｜打印完成 ≠ 零件完成。余量、装夹基准与刀具可达性要在设计阶段安排。')
 save(im,'supp-workflow-02-hybrid-part.png')

def transparent_fig():
 im,d=start('透明件的表面，怎样改变光路','同一材料与厚度的定性截面示意；箭头只解释散射方向，不表示透射率或真实光强。')
 for i,(cx,title) in enumerate([(380,'① 打印后毛面'),(1040,'② 逐级打磨'),(1700,'③ 抛光或适合的涂覆')]):
  text(d,(cx,265),title,37,anchor='mt');x=cx-235; top=560; bottom=790
  rough=[18,0,-12,20,-8,10,-16,14,0,19,-10,15,0] if i==0 else ([3,-3,5,-2,3,-4,2,-2,3,-3,2,-1,0] if i==1 else [0]*13)
  pts=[(x+j*470/12,top+r) for j,r in enumerate(rough)]+[(x+470,bottom),(x,bottom)]
  d.polygon(pts,fill=PALE,outline=INK,width=3)
  if i==2:line(d,[(x,top-8),(x+470,top-8)],GOLD,8)
  for j in [-1,0,1]:
   xx=cx+j*105;arrow(d,(xx,390),(xx,top-25),GOLD)
   endx=xx+([-90,40,120][j+1] if i==0 else ([-30,10,45][j+1] if i==1 else 5))
   arrow(d,(xx,top+18),(endx,bottom+135),RUST,4)
  if i==0:
   arrow(d,(cx,top+10),(cx-155,435),RUST,4);arrow(d,(cx+105,top+10),(cx+210,460),RUST,4)
  d.ellipse((cx-15,660,cx+10,682),outline=RUST,width=3)
  text(d,(cx,993),['表面起伏使光线分散','表面更细，仍可能有雾感','表面更平滑，常能更清晰'][i],29,anchor='mt')
  text(d,(cx,1048),['层纹、支撑痕会影响外观','打磨也可能改变边缘和尺寸','涂层也会改变尺寸与适用性'][i],26,anchor='mt')
 footer(d,'原创光路示意｜内部缺陷、材料吸收、厚度与曲率仍会影响清晰度；表面处理不保证达到成像光学要求。')
 save(im,'supp-workflow-03-clear-surface.png')

def cost_fig():
 im,d=start('一件与一批：哪些工作只做一次，哪些会重复','定性拆分，不按面积比较金额；图中重复三件仅表示“一批”，并非成本交叉点。')
 # diagrams of prep branching to repeated work
 def prep(x,y):
  d.rounded_rectangle((x,y,x+370,y+155),radius=12,fill=INK);text(d,(x+185,y+28),'一次性准备',34,BG,'mt');text(d,(x+185,y+85),'数据 / 编程 / 工装',28,BG,'mt')
 def unit(x,y):
  # stack accurately conveys categories without monetary quantitative scale.
  for k,(col,s) in enumerate([(TEAL,'制造与材料'),(LIGHT,'后处理与测量')]):
   d.rectangle((x,y+k*88,x+320,y+(k+1)*88),fill=col,outline=BG,width=5);text(d,(x+160,y+k*88+22),s,28,INK,'mt')
 text(d,(100,275),'只做 1 件',40);prep(100,360);arrow(d,(285,540),(285,635));unit(125,670)
 text(d,(120,930),'这件产品承担整次准备工作',29)
 line(d,[(620,280),(620,1090)],LIGHT,2)
 text(d,(755,275),'一次做一批',40);prep(1185,360)
 line(d,[(1370,540),(1370,590)],RUST,5);line(d,[(930,590),(1810,590)],RUST,5)
 for xx in [770,1210,1650]:arrow(d,(xx+160,590),(xx+160,635));unit(xx,670)
 text(d,(1370,930),'同一份准备工作，由这批合格件共同分担',29,anchor='mt')
 text(d,(1370,985),'每件制造、后处理和检验仍然存在',29,anchor='mt')
 footer(d,'原创成本结构示意｜批次变化可能带来新的排版、装夹、模具、失败重做与库存成本；实际报价要看完整工艺链。')
 save(im,'supp-workflow-04-batch-cost.png')

def support_fig():
 im,d=start('动笔先找出口：支撑怎样拆，粉末怎样出','练习用截面：把“制造完成后拿走什么”也画出来，内部结构才有机会成为可制造的设计。')
 text(d,(440,275),'悬垂下方的临时支撑',38,anchor='mt')
 # overhang shelf, supports visibly connecting underside and platform
 d.polygon([(180,790),(300,790),(300,470),(700,470),(700,390),(180,390)],fill=TEAL,outline=INK,width=4)
 for xx in [365,465,565,665]:
  line(d,[(xx,500),(xx,795)],RUST,8);line(d,[(xx-25,470),(xx+25,520)],RUST,5);line(d,[(xx+25,470),(xx-25,520)],RUST,5)
 line(d,[(140,800),(760,800)],INK,8);arrow(d,(740,625),(620,625));text(d,(240,915),'留出工具与手的接近空间',30);text(d,(240,975),'支撑接触面可能需要修整',28)
 text(d,(1530,275),'封闭空腔改成可排粉空腔',38,anchor='mt')
 d.rounded_rectangle((1170,390,1860,795),radius=85,fill=TEAL,outline=INK,width=4)
 d.rounded_rectangle((1240,460,1790,725),radius=45,fill=BG,outline=INK,width=4)
 d.rectangle((1400,725,1490,808),fill=BG);line(d,[(1400,725),(1400,795)],INK);line(d,[(1490,725),(1490,795)],INK)
 for yy in range(570,710,30):
  for xx in range(1270,1770,35):d.ellipse((xx,yy,xx+7,yy+7),fill=RUST)
 for xx,yy in [(1415,835),(1450,860),(1480,905),(1410,945),(1460,1000)]:d.ellipse((xx,yy,xx+10,yy+10),fill=RUST)
 arrow(d,(1580,650),(1450,835));text(d,(1550,910),'贯通出口',30);text(d,(1200,1020),'出口位置、尺寸与清理方法需验证',28)
 footer(d,'原创设计练习｜不同粉末、支撑与设备有不同规则；“画了孔”并不自动等于粉末或支撑能够清除。')
 save(im,'supp-workflow-05-removal-access.png')

if __name__=='__main__':
 OUT.mkdir(exist_ok=True,parents=True)
 for f in [data_fig,hybrid_fig,transparent_fig,cost_fig,support_fig]:f()
 print('Created 5 workflow supplement figures at 2100 × 1250.')
