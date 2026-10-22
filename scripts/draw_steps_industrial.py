"""Reproducible causal single-stage industrial AM teaching diagrams."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, random, io
from process_card import *
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
POW='#ded6c6'; BINDER='#9a82b4'; SUPPORT='#bdb8ad'; BLUE='#4c9bb2'

def box(d,xy,fill=OLD,width=4):d.rectangle(xy,fill=fill,outline=INK,width=width)
def note(d,xy,s,size=46,fill=INK):text(d,xy,s,size,fill)
def dots(d,rect):
    x0,y0,x1,y1=rect;d.rectangle(rect,fill=POW)
    r=random.Random(13)
    for _ in range(int((x1-x0)*(y1-y0)/580)):
        x=r.randint(x0+3,x1-3);y=r.randint(y0+3,y1-3);d.ellipse((x-2,y-2,x+2,y+2),fill='#a99e8d')
def base(d,y=820):box(d,(210,y,1000,y+40),'#77898a')
def roller(d,x,y,label=True):
    d.ellipse((x-60,y-80,x+60,y+40),fill='#bcc6c3',outline=INK,width=5)
    arrow(d,(x,y-160),(x,y-80))
    if label:note(d,(x-185,y-225),'压力',43)
def dash(d,a,b,fill=ACC):
    x0,y0=a;x1,y1=b
    for k in range(0,100,8):
        t=k/100;u=min(k+4,100)/100;d.line((x0+(x1-x0)*t,y0+(y1-y0)*t,x0+(x1-x0)*u,y0+(y1-y0)*u),fill=fill,width=5)
def laser(d,x,y,feed=False):
    box(d,(x-80,230,x+80,330),'#bcc6c3');note(d,(x-110,185),'沉积头' if feed else '激光',43)
    d.line((x,330,x,y),fill=ACC,width=8)
    if feed:
        d.line((x-55,330,x-10,y),fill=POW,width=12);d.line((x+55,330,x+10,y),fill=POW,width=12)
    d.ellipse((x-28,y-10,x+28,y+10),fill='#efac4f',outline=ACC,width=3)
def bed(d,floor=820,top=610):
    dots(d,(190,top,1010,floor));d.line((185,top,185,floor+45,1015,floor+45,1015,top),fill=INK,width=6)
    box(d,(190,floor,1010,floor+30),'#77898a')
def pedestal(d,bottom=820,scale=1,color=OLD):
    # Fixed section: broad base plus narrower upper boss.
    x0=360;x1=840;cx=600
    def xx(x):return cx+(x-cx)*scale
    def yy(y):return bottom-(820-y)*scale
    d.polygon([(xx(x0),bottom),(xx(x1),bottom),(xx(x1),yy(740)),(xx(730),yy(740)),(xx(730),yy(600)),(xx(470),yy(600)),(xx(470),yy(740)),(xx(x0),yy(740))],fill=color,outline=INK,width=5)
    for y in range(620,820,25):
        ly=yy(y);lo=470 if y<740 else 360;hi=730 if y<740 else 840
        d.line((xx(lo),ly,xx(hi),ly),fill='#527c76',width=2)
def result(pid,proc,titles,exps,drawer,chapter,ref):
    steps=[]
    for i,(title,exp) in enumerate(zip(titles,exps),1):
        im,d=card(proc,i,4,title);drawer(d,i);footer(d,'原创剖面示意；层厚、工具及间距为解释原理而放大。')
        name=f'step-{pid}-{i:02}.png'
        buffer=io.BytesIO();im.save(buffer,format='PNG',optimize=True)
        (OUT/name).write_bytes(buffer.getvalue())
        steps.append({'file':'assets/images/'+name,'title':title,'explanation':exp})
    return {'id':pid,'chapter':chapter,'title':proc,'steps':steps,'source_refs':[ref]}

def lpbf(d,i):
    if i==1:
        bed(d,800,730);note(d,(240,315),'金属粉末先铺成薄层',50);arrow(d,(310,440),(310,710));note(d,(415,860),'可下降的平台',42)
    elif i==2:
        bed(d,800,730);box(d,(360,770,840,800),ACC);laser(d,720,770);arrow(d,(450,480),(650,480));note(d,(220,560),'扫描处熔化 → 凝固',49);note(d,(315,850),'第一层与基板结合',44)
    elif i==3:
        bed(d,850,610);pedestal(d,850);box(d,(470,625,730,645),ACC);laser(d,650,625);arrow(d,(1055,710),(1055,825));note(d,(210,280),'平台下降',46);note(d,(210,350),'再铺粉、再扫描',43);note(d,(210,450),'橙色：新层',40)
    else:
        pedestal(d,820);note(d,(200,280),'清粉、分离，按路线热处理',48);note(d,(200,350),'关键表面还可能需要机加工',46);note(d,(250,860),'同一台阶件：粉末已清除',44)

def ded(d,i):
    base(d)
    if i==1:
        laser(d,700,820,True);note(d,(210,430),'金属粉沿喷嘴送入',49);note(d,(210,500),'下面是已有金属基体',46);arrow(d,(450,600),(550,780))
    elif i==2:
        box(d,(350,775,740,820),ACC);laser(d,720,775,True);note(d,(205,440),'激光熔化粉末和局部基体',46);note(d,(205,510),'移走后，熔池凝固成一道',46);arrow(d,(430,665),(640,665))
    elif i==3:
        box(d,(350,570,800,820),OLD)
        for y in range(595,820,32):d.line((350,y,800,y),fill=INK,width=2)
        box(d,(350,550,800,575),ACC);laser(d,775,550,True);note(d,(210,360),'抬高沉积头',46);note(d,(210,425),'逐道逐层叠加',43);arrow(d,(945,750),(945,580));note(d,(210,875),'保留前面各层，新层结合其上',40)
    else:
        box(d,(375,565,775,820),OLD)
        for y in range(595,820,32):d.line((375,y,775,y),fill='#527c76',width=2)
        for a,b in [((350,550),(800,550)),((350,550),(350,820)),((800,550),(800,820))]:dash(d,a,b)
        note(d,(210,290),'沉积毛坯留有加工余量',49);note(d,(210,370),'虚线：铣削前；实线：加工后',43);arrow(d,(920,470),(800,555));note(d,(210,875),'检查结合质量及最终尺寸',40)

def binder(d,i):
    if i==1:
        bed(d,820,700);note(d,(220,330),'先铺粉；此时粉末仍松散',49);note(d,(220,415),'打印阶段不把金属熔化',46)
    elif i==2:
        bed(d,820,700);box(d,(360,780,840,820),BINDER);box(d,(620,285,860,370),'#bcc6c3')
        for x in range(650,851,50):
            for y in range(410,735,70):d.ellipse((x-7,y-10,x+7,y+10),fill=BINDER)
        note(d,(200,500),'喷入黏结剂',47);note(d,(200,565),'把选中粉末黏住',43);arrow(d,(490,640),(490,780),BINDER)
    elif i==3:
        pedestal(d,820,color=BINDER);note(d,(200,290),'重复铺粉、喷射并固化',48);note(d,(200,365),'清除松粉后得到脆弱生坯',46);note(d,(240,860),'已成形 ≠ 最终金属性能',44)
    else:
        box(d,(230,420,970,880),'#d5cbc0');box(d,(280,480,920,850),BG);pedestal(d,820,.78,OLD)
        for a,b in [((360,820),(360,740)),((360,740),(470,740)),((470,740),(470,600)),((470,600),(730,600)),((730,600),(730,740)),((730,740),(840,740)),((840,740),(840,820))]:dash(d,a,b,BINDER)
        note(d,(200,260),'脱脂、烧结，颗粒结合并收缩',46);note(d,(200,330),'虚线为入炉前轮廓，非定量比例',42)

def jet(d,i):
    box(d,(230,825,970,855),'#77898a')
    if i==1:
        box(d,(380,270,820,365),'#bcc6c3');note(d,(315,420),'模型树脂与支撑材料',46);note(d,(315,485),'从不同喷孔落下',46);arrow(d,(600,590),(600,780));note(d,(310,865),'起点：空平台',43)
    elif i==2:
        for x0,x1,col in [(350,450,ACC),(450,750,SUPPORT),(750,850,ACC)]:box(d,(x0,785,x1,825),col)
        box(d,(400,270,800,365),'#bcc6c3')
        for x,col in [(400,ACC),(500,SUPPORT),(600,SUPPORT),(700,SUPPORT),(800,ACC)]:
            for y in [425,490,555]:d.ellipse((x-7,y-9,x+7,y+9),fill=col)
        note(d,(220,620),'UV 照射后，液滴固化为薄层',46);note(d,(240,690),'橙：模型材料；灰：支撑材料',42)
    elif i==3:
        box(d,(450,580,750,825),SUPPORT);box(d,(350,580,450,825),OLD);box(d,(750,580,850,825),OLD);box(d,(350,550,850,580),ACC)
        for y in range(600,825,35):d.line((350,y,850,y),fill='#7e9890',width=2)
        note(d,(200,280),'平台逐层下降，喷射并固化',47);note(d,(200,355),'灰色支撑托住上方横梁',45);arrow(d,(960,650),(960,805));note(d,(260,865),'上一层保留，新层长在其上',43)
    else:
        box(d,(350,550,450,825),OLD);box(d,(750,550,850,825),OLD);box(d,(350,550,850,600),OLD)
        note(d,(200,280),'按材料规定清除支撑',48);note(d,(200,355),'横梁下留下原本被支撑占据的空隙',42);arrow(d,(600,745),(600,650));note(d,(320,865),'完成的模型：空隙已打开',43)

def uam(d,i):
    base(d,835)
    if i==1:
        box(d,(300,720,900,746),ACC);arrow(d,(600,770),(600,820));note(d,(220,310),'把一条金属箔铺到基体上',48);note(d,(220,390),'原料本来就是固体薄片',46);note(d,(400,650),'尚未结合的箔带',43)
    elif i==2:
        box(d,(300,805,900,835),ACC);roller(d,700,760);arrow(d,(505,590),(605,590));arrow(d,(605,620),(505,620));note(d,(205,310),'滚轮施压，并作超声振动',47);note(d,(205,390),'界面变形、紧密接触而结合',46)
    elif i==3:
        box(d,(300,610,900,835),OLD)
        for y in range(635,835,30):d.line((300,y,900,y),fill=INK,width=2)
        d.rectangle((500,608,700,735),fill=BG);d.line((500,610,500,735,700,735,700,610),fill=INK,width=5)
        box(d,(555,380,645,635),'#bcc6c3');note(d,(200,240),'叠多层后，用铣刀加工凹槽',46);note(d,(220,455),'铣刀',43);arrow(d,(340,510),(550,590))
    else:
        box(d,(300,610,900,835),OLD)
        for y in range(635,835,30):d.line((300,y,900,y),fill=INK,width=2)
        box(d,(500,640,700,735),BG);box(d,(300,580,900,610),ACC);roller(d,780,535,label=False)
        note(d,(200,240),'再结合上层箔材，封住槽口',46);note(d,(200,320),'剖面空白：通道；橙色：新箔层',42);arrow(d,(440,480),(545,660))

records=[]
records.append(result('lpbf','激光粉末床熔融 LPBF',['薄粉层铺到基板上','激光只熔化选中的位置','下降、铺粉、扫描：逐层长高','取出后，还要完成工艺链'],['起点是金属基板上铺好的薄粉层。粉末还没有成为零件，激光接下来只处理当前截面。','橙色薄带表示第一层已熔化并凝固的区域。激光移动形成熔池，熔池冷却后与下面金属结合；未扫描粉末仍然松散。','平台下降一个层厚，铺粉机构补上一层粉，激光再扫描新截面。图中绿色保留之前凝固的材料，橙色是本轮新增层；重复后得到台阶形实体。','打印结束后移除松粉，按验证路线进行热处理、与基板分离、必要的去支撑和精加工，再检验。此台阶示例没有画悬垂，不能据此推断真实金属件都不需要支撑。'],lpbf,'05','PROC05LPBF'))
records.append(result('ded','送粉激光定向能量沉积 DED',['粉末被送到基体表面','在移动熔池里形成一道','在旧道上面沉积新道','毛坯再加工，达到尺寸'],['这里示范激光送粉DED，不代表电弧送丝等全部DED路线。粉末沿喷嘴送到激光与基体相遇处，零件下面一直保留同一块基体。','激光在基体表面产生局部熔池，送入的粉末被熔化并加入其中。沉积头移动后，后方熔池凝固，留下与基体结合的第一道。','沉积头升高，继续沿既有沉积道增加材料。绿色是已凝固的各层，橙色是本轮新增道；路径与高度反复更新，形成带层纹的毛坯。','DED沉积不必直接给出最终表面。图中虚线是留下的加工余量，实线是铣削后的轮廓；还需要按任务核查结合、材料状态和尺寸。'],ded,'05','PROC05DED'))
records.append(result('binder','金属黏结剂喷射',['铺开松散金属粉末','选择性喷黏结剂','去掉松粉，露出脆弱生坯','脱脂、烧结后才是金属件'],['起点仍是一层松散金属粉，但本路线打印阶段不依赖激光把粉末熔化。','喷头只在当前截面需要的位置喷入黏结剂，把那里粉末黏在一起。紫色表示被黏结的粉区，不是液态金属。','反复铺粉和喷射，按工艺固化后清除周围松粉，得到保持形状的生坯。生坯仍含黏结体系，搬运强度和最终金属零件不同。','生坯进入经过设计的脱脂、烧结路线。黏结体系被移除，金属颗粒在烧结中结合、致密化，外形通常收缩；虚线只是原轮廓示意，不是通用收缩率。后续仍可能需要精加工和检验。'],binder,'05','PROC05BINDER'))
records.append(result('jet','材料喷射：PolyJet 类光敏材料',['液滴材料从喷孔出发','喷射后用 UV 固化','模型和支撑一起逐层建立','清除支撑，露出模型空隙'],['平台上尚无零件。喷头中既有构成模型的光敏材料，也可有专用支撑材料；这与向粉床喷助剂的MJF不同。','模型液滴与支撑液滴落到各自位置，再由UV照射固化为一层。图中橙色是模型首层，灰色是支撑层，实际配方颜色与图示无关。','平台按层下降，喷射与固化持续重复。前面固化的层一直留在原处；灰色支撑承托将要成为横梁的模型材料，避免它在空中凭空形成。','按具体支撑体系清理后，横梁下原被支撑占据的位置变成空隙。所得是光敏材料模型，不能只凭外观相似就认为它拥有最终量产材料的长期性能。'],jet,'06','PROC06JET'))
records.append(result('uam','超声增材制造 UAM',['铺下一条固态金属箔','压力与超声让界面结合','叠层后铣出一个凹槽','继续叠箔，封成内部通道'],['起点是金属基体和一条固态金属箔。箔材保持薄片形态，不需要像熔融挤出那样从喷嘴流出来。','超声滚轮向下施压，并在界面施加高频振动。界面表层的变形与接触促成冶金结合；这里不画熔池，因为UAM属于固相结合路线。','继续结合箔材得到较厚实体，再用机加工开槽。剖面中的空白是被铣走的金属；加工发生在封闭通道之前，刀具此时能够接近槽内部。','后续箔层覆盖并结合到槽口周围的金属上，把开放槽变成内部通道。图为原理剖面而非实际悬跨工艺参数；完成后仍需结合具体任务检查界面和密封。'],uam,'06','PROC06UAM'))
(ROOT/'references/process-sequences-industrial.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
# A review sheet; excluded from publication.
thumbs=[]
for rec in records:
    row=Image.new('RGB',(1200,275),'white')
    for j,step in enumerate(rec['steps']):
        im=Image.open(ROOT/step['file']);im.thumbnail((300,275));row.paste(im,(j*300,0))
    thumbs.append(row)
sheet=Image.new('RGB',(1200,275*len(thumbs)),BG)
for i,im in enumerate(thumbs):sheet.paste(im,(0,i*275))
(ROOT/'tmp').mkdir(exist_ok=True);sheet.save(ROOT/'tmp/industrial-steps-review.png')
