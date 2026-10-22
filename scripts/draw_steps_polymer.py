"""Four-frame causal mechanisms; simplified sections, not equipment drawings."""
from pathlib import Path
import json
from process_card import *
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
BLUE='#b8d4dd'; YELLOW='#e5ba55'; POWDER='#d6c9b2'

def label(d,x,y,s,color=INK):text(d,(x,y),s,44,color)
def rows(d,x,y,width,n,new_last=True,h=32):
    for k in range(n):d.rounded_rectangle((x,y-k*h,width+x,y-k*h+h-5),radius=8,fill=ACC if k==n-1 and new_last else OLD,outline=INK,width=2)
def dots(d,box,step=28):
    for yy in range(box[1]+10,box[3]-5,step):
        for xx in range(box[0]+10,box[2]-5,step):d.ellipse((xx,yy,xx+5,yy+5),fill='#ab9b82')
def plate(d,y=820):
    d.rectangle((170,y,1020,y+35),fill=INK);label(d,800,y+43,'成形平台')
def nozzle(d,x,y):
    d.rectangle((x-48,y-105,x+48,y-25),fill=INK);d.polygon([(x-48,y-25),(x+48,y-25),(x,y+25)],fill=INK)
    d.line((x,y-185,x,y-105),fill=ACC,width=20)
def tank(d):
    d.rectangle((180,370,1020,820),fill=BLUE)
    d.line((180,340,180,830,1020,830,1020,340),fill=INK,width=9)
    d.line((190,820,1010,820),fill=WHITE,width=12)

def fff(i):
    titles=['原料：丝材进入热端','动作：熔体沿路径铺下','累积：新一层接在旧层上','出机：取件，再修整']
    im,d=card('FFF · 材料挤出',i,4,titles[i-1])
    plate(d)
    if i==1:
        d.ellipse((220,250,450,480),outline=INK,width=18);d.ellipse((295,325,375,405),outline=INK,width=12)
        d.line((435,315,700,315,700,470),fill=ACC,width=19);nozzle(d,700,575)
        label(d,200,520,'热塑性丝材');label(d,780,410,'送料 ↓');label(d,780,540,'热端加热')
        arrow(d,(700,615),(700,770));label(d,320,710,'此时平台上还没有零件')
    elif i==2:
        rows(d,310,782,390,1);nozzle(d,700,750)
        arrow(d,(485,600),(785,600));label(d,410,515,'喷嘴沿截面路径移动')
        label(d,245,360,'软化的塑料被连续挤出');label(d,280,420,'接触平台后冷却定形')
        arrow(d,(885,685),(700,797));label(d,870,615,'首层')
    elif i==3:
        rows(d,310,782,390,5,new_last=False);rows(d,420,622,280,4);nozzle(d,700,494)
        label(d,170,255,'保留前面已经打印的层');label(d,170,315,'只在当前高度补入新材料')
        arrow(d,(900,500),(730,510));label(d,850,410,'本层');label(d,820,710,'旧层')
        arrow(d,(240,690),(240,535));label(d,70,455,'层高递增')
    else:
        rows(d,310,782,390,5,False);rows(d,420,622,280,4,False)
        label(d,180,260,'同一阶梯件：由路径逐层叠成');label(d,180,330,'冷却后从平台取下')
        arrow(d,(850,620),(850,470));label(d,780,400,'取件 ↑');label(d,190,880,'有支撑时，还需去支撑与修整',INK)
    footer(d,'侧面简化示意；橙色＝本步材料，青灰＝已成形材料。路径与层厚不按比例。')
    return im

def vat(i):
    titles=['起始：平台靠近透明槽底','曝光：只让截面区域固化','分离补液：再形成下一层','后处理：清洗、固化、修整']
    im,d=card('槽式光聚合 · 典型倒置结构',i,4,titles[i-1])
    if i<4:
        tank(d)
        py=762 if i<3 else 485
        d.rectangle((330,py,830,py+28),fill=INK)
        label(d,380,235,'平台与零件逐步向上移动')
        if i==1:
            arrow(d,(930,670),(835,805));label(d,735,560,'首层间隙');label(d,200,420,'液态树脂')
        if i==2:
            d.rectangle((450,790,710,812),fill=ACC,outline=INK,width=2)
            d.polygon([(400,885),(760,885),(760,825),(400,825)],fill=YELLOW)
            arrow(d,(580,910),(580,830));label(d,820,535,'固化截面');arrow(d,(910,615),(690,800))
            label(d,200,420,'新层与平台相连')
        if i==3:
            for k in range(7):d.rectangle((450,py+28+k*36,710,py+62+k*36),fill=OLD,outline=INK,width=2)
            d.rectangle((400,py+28+7*36,760,py+62+7*36),fill=OLD,outline=INK,width=2)
            arrow(d,(350,650),(350,475));label(d,200,340,'已固化件随平台抬升')
            arrow(d,(860,765),(765,790),fill='#32788b');label(d,785,680,'树脂补入')
            label(d,210,860,'分离后回位 → 曝光下一截面')
        if i!=3:label(d,210,860,'光从透明槽底向上照射')
    else:
        d.rectangle((430,320,690,620),fill=OLD,outline=INK,width=3)
        d.rectangle((380,620,740,675),fill=OLD,outline=INK,width=3)
        label(d,190,230,'同一零件已从平台取下')
        label(d,160,740,'清洗：移除表面未固化树脂')
        label(d,160,805,'后固化：按材料要求继续反应')
        label(d,160,870,'去支撑与修整：得到所需表面')
    footer(d,'只展示一种倒置结构；层厚、间隙夸大。固化是光引发反应，并非液体被“烘干”。')
    return im

def powderbed(d,depth=0):
    by=820 if depth else 575
    d.rectangle((180,510,1020,by),fill=POWDER);dots(d,(180,510,1020,by))
    d.line((180,475,180,830,1020,830,1020,475),fill=INK,width=9)
    d.rectangle((190,by,1010,by+25),fill=INK)
    if depth:
        d.rectangle((370,725,800,800),fill=OLD,outline=INK,width=3)
        if depth>1:d.rectangle((480,550,690,725),fill=OLD,outline=INK,width=3)

def powder(i,method):
    is_m=method=='mjf';name='MJF · 功能剂与热能' if is_m else 'SLS · 聚合物粉床'
    titles=['起始：铺好一层薄粉','选择：喷液标记目标区域' if is_m else '动作：激光扫描选区','热能：标记区域熔结并叠层' if is_m else '累积：下降、铺粉、再扫描','完成：冷却后清除松散粉']
    im,d=card(name,i,4,titles[i-1])
    if i<4:
        powderbed(d,2 if i==3 else 0)
        if i==1:
            d.rounded_rectangle((220,400,340,500),radius=30,fill=INK);arrow(d,(405,425),(840,425));label(d,395,325,'铺粉器刮平粉层')
            label(d,260,680,'松散粉末，还没有目标零件')
            label(d,760,590,'成形平台')
        elif i==2:
            d.rectangle((370,510,800,540),fill=ACC,outline=INK,width=2)
            if is_m:
                d.rectangle((390,260,760,330),fill=INK)
                for x in range(420,760,55):arrow(d,(x,355),(x,480),width=5)
                label(d,175,195,'喷头按当前截面分布功能剂')
                label(d,220,650,'橙区是被标记的粉，尚未熔结')
                label(d,220,715,'不是把一块冷粉直接粘成零件')
            else:
                d.rectangle((710,235,900,310),fill=INK);arrow(d,(780,330),(570,505));arrow(d,(470,450),(660,450))
                label(d,180,250,'激光沿路径扫描');label(d,210,650,'照到的粉末升温并结合')
                label(d,210,715,'旁边的粉仍保持松散')
        else:
            d.rectangle((480,510,690,550),fill=ACC,outline=INK,width=2)
            if is_m:
                d.rectangle((300,285,900,345),fill=YELLOW,outline=INK,width=3)
                for x in range(340,920,100):arrow(d,(x,370),(x,480),fill=YELLOW)
                label(d,210,205,'红外热能与功能剂配合');label(d,180,380,'目标粉区熔结，连到已有层')
            else:
                d.rectangle((760,235,930,300),fill=INK);arrow(d,(805,320),(595,505));label(d,180,300,'新粉覆盖旧截面，再被扫描')
            arrow(d,(1080,625),(1080,775));label(d,190,865,'平台下降一层 → 铺新粉 → 重复')
            label(d,220,575,'松粉');label(d,765,680,'已成形件')
    else:
        d.rectangle((370,725,800,800),fill=OLD,outline=INK,width=3);d.rectangle((480,550,690,725),fill=OLD,outline=INK,width=3)
        label(d,170,255,'同一阶梯件：原来埋在粉床里');label(d,170,325,'受控冷却后，移除周围松粉')
        arrow(d,(840,580),(1010,450),fill='#32788b');label(d,820,385,'清粉');label(d,180,865,'随后按需求喷砂、染色或平滑')
    footer(d,'侧面简化示意；橙色＝本步选区，青灰＝已成形件，米色颗粒＝松粉；不按比例。')
    return im

STORY=[
('fff','02','一根丝如何逐层变成阶梯件',[
('原料进入热端','丝材由送料机构送进热端，受热软化后才可从喷嘴挤出；此时平台上还没有零件。'),
('沿截面路径铺下首层','喷嘴一边移动、一边挤出塑料，把当前截面转成连续线条。首层先附着平台，随后冷却定形。图中侧视只画出一道线的截面。'),
('新层连接旧层','平台与喷嘴改变相对高度，下一层路径落到上一层上。新挤出的材料与已有塑料结合；截面变窄后，上部自然形成台阶。'),
('取件并修整','完成全部路径后，零件冷却并从平台取下。这个示例没有悬空区；其他几何如使用支撑，还需去支撑与修整。')],['https://ultimaker.com/learn/introduction-to-fff-3d-printing/']),
('vat','03','一槽液体如何长出一个固体',[
('平台靠近槽底','图示采用典型倒置结构：液体在槽中，平台靠近透明槽底，预留首层成形所需间隙。间隙在图中刻意夸大，实际由设备控制。'),
('光只固化需要的截面','光透过槽底照到目标区域，引发树脂固化。第一层连接平台；后续层连接已有零件。图中橙色表示固化材料，不是把整槽液体一起变硬。'),
('分离、补液，再曝光','平台带着已有结构抬升，使新层与槽底分离；树脂流入腾出的空间，平台再到下一次曝光位置。重复这一循环，零件从平台向下延长，同时随平台上移。图示简化了早期附着层。'),
('清洗与后固化','取下的零件表面仍可能带有未固化树脂。按材料要求清洗和后固化，再去支撑与修整；具体先后顺序和条件应遵循对应材料流程。')],['https://formlabs.com/blog/ultimate-guide-to-stereolithography-sla-3d-printing/']),
('sls','04','SLS：激光怎样在粉中留下形状',[
('铺平薄粉层','铺粉器把预热的高分子粉末摊成薄层。松散粉末本身不是成品，平台上也不会一次出现完整三维形状。'),
('激光扫描当前截面','激光只扫描当前截面需要的区域，使粉末受热结合；周围未被选中的粉末仍保持松散。橙色区域只是这一层，不是整个零件。'),
('下降、铺粉、重复','成形平台下降一层，铺粉器覆盖新粉，激光再次扫描。新结合的截面连接下面已有材料；旁边的松粉包围并支承它，零件逐渐埋入粉床。'),
('先冷却，再取出','构建结束后按工艺受控冷却，再清除松粉，才露出同一阶梯件。必要时还要喷砂、染色或平滑；封闭腔体中的粉不会自行消失。')],['https://formlabs.com/blog/what-is-selective-laser-sintering/']),
('mjf','04','MJF：液体标记与热能怎样配合',[
('铺好聚合物粉层','起点同样是一层高分子粉末。后面的液体主要用于调节局部热响应，而不是承担成品的主要体积。'),
('先给截面做功能标记','喷头按截面选择性沉积功能剂。图中橙区表示已标记的粉，尚不等于固体零件；边界附近还可使用细化剂控制热行为，图中省略其细小分布。'),
('施加热能并逐层累积','红外热能与功能剂配合，让目标粉区熔结并连接前一层。之后平台下降、重新铺粉、喷剂、加热，重复形成三维形状。它不是用胶水把冷粉粘在一起。'),
('冷却清粉后才能使用','构建完成后依系统流程冷却、取出并清粉，露出与前图对应的阶梯件。表面处理和尺寸检验仍是制造链的一部分。')],['https://www.hp.com/us-en/printers/3d-printers/learning-center/3d-print-binder-vs-material-jetting.html'])]
metadata=[]
for pid,ch,title,steps,refs in STORY:
    record={'id':pid,'chapter':ch,'title':title,'steps':[],'source_refs':refs}
    for i,(st,ex) in enumerate(steps,1):
        file=f'assets/images/step-{pid}-{i:02}.png'
        im=fff(i) if pid=='fff' else vat(i) if pid=='vat' else powder(i,pid)
        save(im,ROOT/file);record['steps'].append({'file':file,'title':st,'explanation':ex})
    metadata.append(record)
(ROOT/'references/process-sequences-polymer.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
# Idempotent chapter insertion before existing conceptual comparisons.
anchors={'02':'## 喷嘴画的不是实体，而是路径','03':'## 同样用光，如何“画一层”很不同','04':'## 颗粒感可以是风格，也可以需要处理'}
for ch in ['02','03','04']:
    path=ROOT/f'chapters/{ch}.md';s=path.read_text();start='<!-- polymer-stage-start -->';end='<!-- polymer-stage-end -->'
    if start in s:s=s[:s.index(start)]+s[s.index(end)+len(end):].lstrip('\n')
    block=start+'\n\n'
    for rec in [r for r in metadata if r['chapter']==ch]:
        block+='## '+rec['title']+'\n\n'
        block+='按下列顺序向下阅读；各图沿用同一件阶梯形示例，比例和层数只用于解释过程。\n\n'
        for i,step in enumerate(rec['steps'],1):
            block+=f'**第{i}步：{step["title"]}**\n\n![{rec["id"].upper()}第{i}步：{step["title"]}](../{step["file"]})\n\n图：原创连续步骤图 {i}/4，简化结构，不是具体设备。\n\n{step["explanation"]}\n\n'
        block+=f'本组原理依据：[官方工艺说明]({rec["source_refs"][0]})。\n\n'
    block+=end+'\n\n';s=s.replace(anchors[ch],block+anchors[ch],1);path.write_text(s)
