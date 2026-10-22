"""Phone-first continuous subtractive-process diagrams; all dimensions schematic."""
from pathlib import Path
import json, math
from process_card import *
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
BLUE='#438aab'; VOID='#f6f1e8'; DARK='#45666b'

def dash(d,points,fill=INK,width=4):
    for a,b in zip(points,points[1:]):
        length=math.dist(a,b)
        for t in range(0,int(length),28):
            u=t/length;v=min((t+14)/length,1)
            d.line((a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u,a[0]+(b[0]-a[0])*v,a[1]+(b[1]-a[1])*v),fill=fill,width=width)

def cutter(d,x,y):
    d.ellipse((x-65,y-65,x+65,y+65),fill=ACC,outline=INK,width=5)
    for a in (0,math.pi/2,math.pi,math.pi*1.5):
        d.line((x,y,x+55*math.cos(a),y+55*math.sin(a)),fill=WHITE,width=8)
    d.arc((x-95,y-95,x+95,y+95),195,470,fill=INK,width=6)
    arrow(d,(x+40,y-84),(x+70,y-64),INK,6)

def milling(step):
    im,d=card('铣削｜同一块毛坯·始终俯视',step,4,['装夹，标出要挖掉的区域','旋转刀刃切下第一条材料','逐道扩展，再分层切深','精铣侧壁与底面，留下圆角'][step-1])
    text(d,(65,210),'灰绿：保留的金属',42);text(d,(65,270),'浅色：已铣低的槽底',42)
    d.rounded_rectangle((150,380,1050,790),radius=18,fill=OLD,outline=INK,width=6)
    for x in (180,910):
        d.rectangle((x,340,x+100,410),fill=DARK);d.rectangle((x,760,x+100,830),fill=DARK)
    # Pocket never goes through: light floor shown rather than transparency.
    if step==1:
        dash(d,[(320,470),(880,470),(880,700),(320,700),(320,470)],ACC)
        text(d,(400,555),'计划的凹槽',47)
    if step==2:
        d.rounded_rectangle((320,470,650,600),radius=65,fill=WHITE)
        cutter(d,585,535);arrow(d,(390,650),(620,650))
        text(d,(680,510),'切屑',43,ACC)
        for j in range(5):d.arc((675+j*24,440-j*7,700+j*24,470-j*7),0,250,fill=ACC,width=5)
    if step==3:
        d.rounded_rectangle((320,470,880,700),radius=65,fill=WHITE)
        for y in (535,605,635):d.line((385,y,815,y),fill=PALE,width=6)
        cutter(d,815,635);arrow(d,(680,750),(400,750))
    if step==4:
        d.rounded_rectangle((320,470,880,700),radius=65,fill=WHITE,outline=INK,width=6)
        text(d,(405,545),'凹槽底面',48)
        arrow(d,(955,300),(866,470));text(d,(735,225),'刀具半径留下圆角',41)
    footer(d,'刀具旋转；工件被夹住。浅色区域仍有底，不是贯通孔。')
    return im

def turning(step):
    im,d=card('外圆车削｜同一根棒料·始终侧视',step,4,['夹住棒料，让它绕轴线旋转','刀尖切入，沿轴向走一刀','多次进给，直径逐步减小','精车到尺寸，再去毛刺检查'][step-1])
    text(d,(65,210),'灰绿：保留材料　虚线：原直径',42)
    d.rectangle((120,390,300,760),fill=DARK,outline=INK,width=5)
    text(d,(130,790),'卡盘',44)
    for y in (410,655):d.rectangle((245,y,335,y+85),fill=INK)
    # Shaft axis y575, original radius120; machined right-hand shoulder has radius70.
    if step==1:
        d.rectangle((300,455,1030,695),fill=OLD,outline=INK,width=5)
    else:
        boundary={2:810,3:570,4:570}[step]
        d.polygon([(300,455),(boundary,455),(boundary,505),(1030,505),(1030,645),(boundary,645),(boundary,695),(300,695)],fill=OLD,outline=INK)
        d.line([(300,455),(boundary,455),(boundary,505),(1030,505),(1030,645),(boundary,645),(boundary,695),(300,695)],fill=INK,width=5)
        dash(d,[(570,455),(1030,455),(1030,695),(570,695)],ACC)
        if step in (2,3):
            x=boundary+10
            d.polygon([(x,505),(x+100,390),(x+190,390),(x+105,505)],fill=ACC,outline=INK)
            arrow(d,(x+125,340),(x-70,340));text(d,(575,265),'刀具向左进给',43)
            d.arc((x+25,450,x+90,490),0,290,fill=ACC,width=7)
    dash(d,[(310,575),(1080,575)],BLUE)
    d.arc((380,365,515,440),20,320,fill=INK,width=6);arrow(d,(495,375),(512,394),INK,6)
    text(d,(360,800),'工件旋转，形成回转表面',47)
    footer(d,'侧视图上下两侧都变细：工件在转，不是只削去上表面。')
    return im

def edm(step):
    im,d=card('线切割 EDM｜同一块导电板·始终俯视',step,4,['先做穿丝孔，把电极丝穿进去','脉冲放电，打开一条窄切缝','沿轮廓前进，中央料块仍在','闭合切缝，取出中间料块'][step-1])
    text(d,(65,210),'不是锯齿切削：电极丝与工件留间隙',43)
    d.rounded_rectangle((150,360,1050,820),radius=12,fill=OLD,outline=INK,width=6)
    path=[(410,500),(810,500),(810,700),(410,700),(410,500)]
    dash(d,path,INK,3)
    if step==1:
        d.ellipse((390,480,430,520),fill=BG,outline=INK,width=4)
        d.ellipse((404,494,416,506),fill=ACC)
        arrow(d,(330,270),(405,475));text(d,(420,265),'穿丝孔',44)
    if step in (2,3):
        upto=[(410,500),(650,500)] if step==2 else [(410,500),(810,500),(810,700),(550,700)]
        d.line(upto,fill=BG,width=24,joint='curve')
        x,y=upto[-1]
        d.ellipse((x-7,y-7,x+7,y+7),fill=ACC)
        for a in range(0,360,45):
            r=math.radians(a);d.line((x+16*math.cos(r),y+16*math.sin(r),x+31*math.cos(r),y+31*math.sin(r)),fill=ACC,width=4)
        arrow(d,(x-10,y-115),(x+70 if step==2 else x-90,y-115))
        text(d,(365,575),'待取出的料块',44)
        text(d,(90,865),'橙点＝穿过板厚的电极丝',41,ACC)
    if step==4:
        d.rectangle((398,488,822,712),fill=BG,outline=INK,width=4)
        text(d,(450,565),'贯通开口',48)
        text(d,(90,865),'料块另行接住；随后清洗、检查切面',39)
    footer(d,'切缝宽于电极丝直径。放电碎屑由工作液带走；比例已放大。')
    return im

def section(d,kind):
    # The same front shown below, enlarged across the full width for phone reading.
    d.rounded_rectangle((60,195,1140,445),radius=16,fill=WHITE,outline=PALE,width=3)
    text(d,(80,205),'作用点侧剖面（放大）',38)
    d.rectangle((420,330,1080,372),fill=OLD)
    d.rectangle((740,327,776,377),fill=BG)
    d.polygon([(700,260),(816,260),(787,306),(729,306)],fill=DARK)
    if kind=='laser':
        d.line((758,250,758,370),fill=ACC,width=11)
        arrow(d,(707,285),(727,337),BLUE,6);arrow(d,(809,285),(789,337),BLUE,6)
        for x,y in ((749,386),(779,409),(728,410)):d.ellipse((x-6,y-8,x+6,y+8),fill=ACC)
        text(d,(82,285),'光束加热',40,ACC)
        text(d,(82,345),'气流排出熔融金属',38)
    else:
        d.line((758,305,758,410),fill=BLUE,width=19)
        for x,y in ((754,309),(762,326),(751,347),(763,370),(743,392),(779,411)):
            d.ellipse((x-5,y-5,x+5,y+5),fill=ACC)
        text(d,(82,285),'高速水流＋磨粒',40,BLUE)
        text(d,(82,345),'侵蚀、带走材料',38)

def beam_cut(step,kind):
    name='激光熔化切割' if kind=='laser' else '磨料水射流切割'
    titles=['支撑板材，从边缘开始','形成贯通切缝，再向前移动','作用点前进，后方切缝增长','切到另一边，分离并检查']
    im,d=card(name+'｜同一块板·主图始终俯视',step,4,titles[step-1])
    if step in (2,3):section(d,kind)
    else:
        text(d,(65,235),'灰绿：板材　虚线：计划切线',42)
        text(d,(65,300),'选择从外边缘进入，省略内部穿孔',39)
    d.rectangle((150,480,1050,820),fill=OLD,outline=INK,width=6)
    dash(d,[(600,480),(600,820)],INK,4)
    if step==1:
        d.ellipse((576,456,624,504),outline=ACC if kind=='laser' else BLUE,width=7)
        arrow(d,(680,430),(615,475));text(d,(65,390),'起点',44)
    if step in (2,3):
        end=565 if step==2 else 715
        d.rectangle((589,480,611,end),fill=BG)
        d.ellipse((575,end-25,625,end+25),fill=ACC if kind=='laser' else BLUE)
        arrow(d,(700,end-20),(700,end+75))
        text(d,(755,600),'前进方向',42)
        text(d,(185,500),'已切开',44);arrow(d,(390,535),(580,535),INK,5)
        d.line((590,end-25,560,445),fill=ACC if kind=='laser' else BLUE,width=3)
    if step==4:
        d.rectangle((588,478,612,823),fill=BG)
        arrow(d,(530,640),(420,640));arrow(d,(670,640),(780,640))
        text(d,(195,535),'左侧板件',45);text(d,(730,535),'右侧板件',45)
    footer(d,('橙色＝热作用点；蓝色＝辅助气流。示范熔化切割，不代表所有激光方式。' if kind=='laser' else '蓝色＝水流，橙点＝磨粒。材料被侵蚀带走，不靠熔化。'))
    return im

DATA=[
('milling','铣削：凹槽怎样逐步出现',['装夹与规划','刀刃第一次去料','逐道、逐层扩展','精加工与检查'],[
'从上面看同一块毛坯：夹具固定材料，虚线圈出凹槽范围。凹槽下面还要留底；刀具进入、退刀和夹具避让必须先规划。[S01]',
'圆柱铣刀绕自身轴线旋转，刀齿把接触到的金属切成切屑；相对工件向右进给后，刀后留下已经铣低的浅色槽底。浅色不是穿透板材的孔。[S01]',
'相邻刀路逐步覆盖更大范围，达到这一层的切深后再安排后续层。前一步的槽保留下来，刀具只继续移走剩余材料；图中刀路是概念示意，不是可直接上机的程序。[S01]',
'粗加工接近形状后，再精铣侧壁与底面，并去毛刺、测量。圆形刀具无法在同样路径下留下无限尖锐的内角；成品仍有底和内圆角。[S01]'],['S01']),
('turning','车削：棒料怎样变成阶梯轴',['旋转棒料','切入并轴向进给','重复走刀','完成外圆与台阶'],[
'卡盘夹住棒料并带它绕蓝色中心线旋转；本组始终从侧面观察。最终要变细的右端，最初和左侧仍是同一根等直径棒料。[S01]',
'刀尖切入旋转的外圆，再沿轴向向左进给。刀尖经过之处，材料变成切屑离开，右端开始出现较小直径；不是只在棒料上表面挖一条槽。[S01]',
'重复走刀，并按要求改变径向切入量，较小直径的段落逐渐延长到台阶位置。图中虚线保留原棒料外径，便于看出哪些材料已经离开。[S01]',
'精车取得要求的外径、长度与肩部表面，再去毛刺并检查。图中是外圆工序完成状态；卡盘夹持区仍可能需要调头或其他工序，不把一次装夹画成整根零件全部完成。[S01]'],['S01']),
('edm','线切割：电极丝怎样围出贯通轮廓',['先穿丝','放电打开切缝','沿轮廓持续切割','接住料块并取出'],[
'对于图示封闭内轮廓，先在轮廓起点安排穿丝孔。橙点是从板厚方向穿过的电极丝，主图保持俯视；工件必须适合这种导电放电加工。[CASE-S04]',
'电极丝与工件之间保持微小放电间隙，受控脉冲局部去除材料，工作液帮助带走碎屑。丝沿计划路径前进，留下比丝径更宽的切缝，并非像锯条那样靠齿刃接触切削。[S02][CASE-S04]',
'丝继续沿轮廓走，已经切开的路径保留在后方；中央料块此时还由未切完的部分连着外板。实际加工需安排冲液、支承和必要的多次修切。[CASE-S04]',
'最后一段连通后，接住并取出中央料块，留下贯穿板厚的开口。再清洗、检查尺寸与切面；图中转角为简化画法，实际内角仍受丝径和放电间隙限制。[CASE-S04]'],['S02','CASE-S04']),
('laser','激光：热与气流怎样打开切缝',['边缘起切','局部熔化并排出','切缝随运动增长','分离、清理与检查'],[
'这组选择金属板的激光熔化切割，从板材外边缘起切，始终沿同一条直线前进。板材由切割台支承；封闭内轮廓通常还要解决内部起切与穿孔。[S03]',
'放大侧剖面显示：聚焦光束把局部金属加热至熔融，辅助气流将熔融材料从切缝排出。只有形成贯通去料通道，移动的作用点才会留下完整切缝。[S03]',
'作用点向前移动，前方仍是完整板材，后方已形成切缝。图中主视图保持俯视，旁边的放大图解释同一作用点的板厚方向变化；氧气反应切割等路线还有不同能量机制。[S03]',
'切至另一边后，板材分离。随后根据要求处理挂渣与边缘，检查尺寸、表面和热影响；完成分离不代表自动取得最终装配质量。[S03]'],['S03']),
('waterjet','水刀：磨粒怎样把板材冲开',['支撑与边缘起切','磨粒侵蚀材料','射流沿路径移动','分离、清洗与检查'],[
'从外边缘进入，沿同一条直线切开板材；切割台支承零件和余料。本组画的是磨料水射流，不是用于某些软材料的纯水切割。[S04]',
'水在喷头内形成高速射流并携带磨料；放大图中的橙色颗粒冲击、侵蚀材料，水流将碎屑带走。贯通切缝来自材料不断离开，不靠把整条缝熔化。[S04]',
'射流前进后，后方留下连续切缝，前方板材仍完整。实际射流会发生滞后与形状变化，需要把速度、路径补偿和材料厚度一起考虑；示意图不表达具体工艺参数。[S04]',
'切到另一边后接住两侧板件，清洗并按要求处理边缘。检查内容包括轮廓、切缝锥度与切面条纹；用磨料水刀也不等于每种材料都能无损穿孔或得到相同表面。[S04]'],['S04'])]

def main():
    records=[]
    for ident,title,titles,explanations,refs in DATA:
        steps=[]
        for n in range(1,5):
            im={'milling':milling,'turning':turning,'edm':edm}.get(ident,lambda s:beam_cut(s,ident))(n)
            file=f'assets/images/step-{ident}-{n:02}.png';save(im,ROOT/file)
            steps.append({'file':file,'title':titles[n-1],'explanation':explanations[n-1]})
        records.append({'id':ident,'chapter':'09','title':title,'steps':steps,'source_refs':refs})
    (ROOT/'references/process-sequences-cutting.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    chapter=ROOT/'chapters/09.md';body=chapter.read_text()
    intro='## 连续看懂：材料究竟怎样离开\n\n以下每组从同一方向追踪同一块材料，一步一图，按从上到下的顺序阅读。灰绿色表示仍留在工件上的材料；箭头说明本步运动，虚线保留计划路径或原始轮廓。图形、间隙和刀具比例经过放大，不可作为加工参数。\n\n'
    for rec in records:
        intro+='**'+rec['title']+'**\n\n'
        for n,step in enumerate(rec['steps'],1):
            intro+=f"![原创连续原理图：{rec['title']}，步骤{n}，{step['title']}。](../{step['file']})\n\n图：{rec['title']} · {n}/4，{step['title']}。原创程序绘图；依照本段所列资料简化。\n\n{step['explanation']}\n\n"
    marker='## 连续看懂：材料究竟怎样离开'
    if marker in body:body=body[:body.index(marker)]+body[body.index('## 把工艺放回真实任务'):]
    body=body.replace('## 把工艺放回真实任务',intro+'## 把工艺放回真实任务')
    chapter.write_text(body)
if __name__=='__main__':main()
