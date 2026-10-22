"""Explicit panel regions from the original diagrams; preserve desktop overview.

These are alternate reading views, not additional independent book illustrations.
Scene boundaries follow the drawing scripts, never an automatic equal-width split.
Long explanations are HTML text so phones can size and reflow them accessibly.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/panels'; OUT.mkdir(parents=True,exist_ok=True)
manifest={}
def add(name,regions):
    source=Image.open(ROOT/'assets/images'/name)
    panels=[]
    for i,(box,title,caption) in enumerate(regions,1):
        target=OUT/f'{Path(name).stem}-{i:02d}.png'
        panel=source.crop(box)
        # Remove only the between-panel connector arrows, whose endpoints
        # belong to the desktop overview. Preserve every workpiece/tool arrow.
        d=ImageDraw.Draw(panel)
        if name=='supp-workflow-01-cad-mesh-slice.png':
            for left,right in [(640,760),(1290,1410)]:
                d.rectangle((left-box[0],475-box[1],right-box[0],525-box[1]),fill='#f6f1e8')
        if name=='supp-workflow-02-hybrid-part.png':
            for left,right in [(600,730),(1280,1410)]:
                d.rectangle((left-box[0],625-box[1],right-box[0],675-box[1]),fill='#f6f1e8')
        if name=='core-fff-orientation.png' and i==1:
            panel=panel.crop((0,0,panel.width,515))
        if name=='core-material-properties.png' and i==1:
            panel=panel.crop((0,0,panel.width,515))
        if name=='supp-workflow-04-batch-cost.png' and i==2:
            # Show one representative repeated unit vertically beneath the
            # common preparation block; HTML explains the batch allocation.
            panel=Image.new('RGB',(510,600),'#f6f1e8')
            panel.paste(source.crop((1140,270,1630,525)),(10,0))
            panel.paste(source.crop((1160,650,1580,865)),(45,345))
            d=ImageDraw.Draw(panel)
            d.line((255,270,255,325),fill='#c85a34',width=6)
            d.polygon([(255,335),(242,313),(268,313)],fill='#c85a34')
        panel.save(target,optimize=True)
        panels.append({'file':target.relative_to(ROOT).as_posix(),'alt':title,'title':title,'caption':caption,'region':list(box)})
    manifest[name]={'panels':panels,'note':'分图取自同一张原创示意；顺序、色彩与原图一致。并非实际比例或操作参数。'}
def row(name,xs,w,y0,y1,titles,notes):
    add(name,[((x,y0,x+w,y1),t,n) for x,t,n in zip(xs,titles,notes)])
row('core-fff-orientation.png',[70,1030],900,220,790,
    ['层内受力','跨层间受力'],['层面与拉力平行，力主要沿层内路径传递。绿色短箭头是构建 Z 方向；性能仍受孔隙、路径和结合质量影响。','把同一观察方向下的层面转过来：拉力跨越层间界面。橙线强调可能较弱的一个界面，不能由摆放直接推算强度。'])
row('core-fiber-forms.png',[70,1030],900,220,760,
    ['短切纤维','连续纤维'],['橙色短段分散在聚合物基体中；挤出流动可能让它们定向，但它们不是贯穿整个零件的连续纤维束。','橙色纤维束沿规划路线连续铺放。孔、转角和纤维可铺放方向会约束增强效果；并非所有方向同样强。'])
row('core-material-properties.png',[65,715,1365],570,220,750,
    ['强度：何时破坏？','刚度：变形多少？','韧性：吸收多少能量？'],['看材料达到屈服或断裂时承受的应力。必须同时说明拉伸、压缩等测试方式和判据。','同几何、同约束、同载荷，结构变形越小，刚度越大。材料常用弹性模量描述，零件还受形状影响。','到断裂为止，应力—应变曲线下的面积表示单位体积吸收的能量。图是概念示意，没有实测数值。'])
row('core-resin-exposure.png',[65,715,1365],570,220,1050,
    ['SLA：光点扫描','DLP：图像投影','MSLA：掩膜透光'],['激光光点沿一层的路径依次扫描，选中的液态树脂固化。图为典型下照式简化剖面。','投影光机把一幅层图像投向树脂，选中的区域固化。不同机型的运动结构可不同。','背光经过 LCD 掩膜，只有允许透光的区域让树脂固化。三种名称并不唯一决定上照或下照结构。'])
row('core-sls-mjf.png',[70,1030],900,220,890,
    ['SLS：激光供热','MJF：功能剂配合红外供热'],['激光在预热粉床上扫描，让选区颗粒连接。周围未连接粉末支撑已成形区域；还需要铺粉、下降和冷却循环。','先喷功能剂，再施加红外热能，选区熔合。液体不是胶水。这里把先后动作并列展开，不能当作机头实际布局。'])
row('diagram-01-routes.png',[65,650,1235],500,200,850,
    ['增材：逐层增加','减材：去掉多余','成形：重新分配'],['将材料逐层连接，内部可设计为空腔，但要处理支撑或排粉。','工具必须能接近需要去除的区域，可达性限制最终几何。','通过模具、压力或材料流动重新分配材料，而不是只靠加或减。'])
row('diagram-02-principles.png',[65,650,1235],500,200,860,
    ['材料挤出','槽式光聚合','粉末床熔融'],['喷嘴沿规划路径放下材料，再连接下一层；具体阶段见各章后续步骤图。','光选择性固化液态树脂；这一幅是家族概念概览，不是具体设备结构图。','先铺粉，再用热能连接选区；新粉层覆盖后继续构建。具体循环见粉床工艺章节。'])
row('diagram-04-limits.png',[65,650,1235],500,210,880,
    ['支撑接触面','封闭腔中的粉末','刀具留下的内圆角'],['临时支撑需要拆走，接触处常留痕迹，要留出工具接近空间。','内腔若没有合适出口，松散粉末就可能留在里面；设计时要验证清理路径。','旋转刀具有半径，不能在内侧直接切出任意尖角；图中圆环强调刀具占据的空间。'])
row('diagram-05-greenpart.png',[65,495,925,1355],385,260,830,
    ['1 打印生坯','2 清粉与脱脂','3 烧结','4 精加工与检验'],['金属粉末被粘结剂临时固定成形，打印出来的还不是致密金属件。','先清除松散粉末，再按体系处理粘结剂。不同体系可能有额外固化或脱脂步骤。','金属颗粒在受控热过程中连接并致密化，外形通常随之收缩。','对关键表面和尺寸加工、检验，确认缺陷与材料状态符合用途。'])
add('diagram-06-quality.png',[((x,y,x+815,y+310),t,n) for x,y,t,n in [(65,210,'数字模型','单位、封闭性和壁厚会影响几何误差。'),(920,210,'成形方向','层间性能、支撑位置、表面与强度要一起考虑。'),(65,560,'后处理','清洗、固化与热处理仍会改变尺寸和材料状态。'),(920,560,'使用与测量','按实际用途检查温度、吸湿与量具条件，不能把层高当作零件精度。')]])
row('supp-industrial-metal-feed.png',[80,775,1470],650,250,1100,
    ['LPBF：先铺粉床','送粉激光 DED','送丝 DED：激光示例'],['整层预铺金属粉末，再由激光选择性熔化；构建平台逐层下降。','粉末随喷头送入局部熔池，通常不需要整层粉床。','连续丝材直接进入熔池；这幅用激光举例，送丝 DED 也可使用电弧或电子束。材料供给方式和能量源是两个问题。'])
row('supp-industrial-metal-postprocess.png',[80,494,908,1322,1736],385,300,990,
    ['1 冷却与清粉','2 热处理','3 分离与去支撑','4 加工与表面处理','5 检验与放行'],['回收松散粉末，确认内腔可以清理。','示例是在基板上去应力；具体热处理按合金、几何和规范制定。','从基板分离，移除支撑并修整接触区。','加工配合面、螺纹等，再按需要磨削、喷丸或进行其他表面处理。','检查尺寸、表面、内部缺陷和材料性能，保留追溯记录。此流程不是统一操作规程，检验也应贯穿制造。'])
row('supp-industrial-jet-sheet.png',[80,1100],980,270,890,
    ['材料喷射','UAM 超声金属箔结合'],['喷出的液滴就是成形或支撑材料，落位后由 UV 固化，再逐层叠加。与向整床粉末喷粘结剂不同。','金属箔在压力和横向超声振动作用下固态结合，可与 CNC 交替构造内外形状；不能把所有片材叠层都当作 UAM。'])
add('supp-industrial-cutting-motion.png',[((x,y,x+980,y+400),t,n) for x,y,t,n in [(80,270,'车削：工件旋转','车刀进给，形成轴等回转表面。'),(1140,270,'铣削：刀具旋转','工件与刀具相对进给，刀齿依次去除材料。'),(80,720,'钻削：旋转并轴向进给','用于造孔，后续可按需要扩、铰或镗。'),(1140,720,'磨削：砂轮旋转','砂轮上的大量磨粒切削，图中工件往复进给。实际设备可有更多轴与运动组合。')]])
row('supp-industrial-nontraditional-cutting.png',[80,600,1120,1640],490,280,1120,
    ['成形电火花','线切割','激光切割','磨料水射流'],['成形电极与工件之间留有间隙，在工作液中脉冲放电蚀除材料。典型要求工件导电。','细丝是电极，沿轮廓放电，不是锯条。图为连续送丝示例，典型要求工件导电。','局部热过程配合辅助气体形成割缝；材料不必导电，但要匹配材料、波长和参数。','高压水携带磨粒，高速射流与磨粒侵蚀材料；还要考虑割缝锥度和脆性损伤。'])
row('supp-industrial-ceramic-chain.png',[80,600,1120,1640],490,300,1070,
    ['1 光成形','2 清洗与生坯','3 脱脂','4 烧结'],['陶瓷颗粒与光敏体系混合，曝光固定逐层几何。','清除未固化浆料；此时的生坯仍含有机结合相。','受控热过程移除有机组分，避免裂纹与变形。','颗粒结合并致密化，通常产生收缩，再按需要精加工。图中虚框仅作生坯外形参照，不表示固定收缩率。'])
row('supp-workflow-01-cad-mesh-slice.png',[85,735,1395],620,245,1120,
    ['1 CAD 实体','2 STL 三角网格','3 切片与路径'],['同一个圆柱可用圆柱面和封闭体积表达，还可保留尺寸、参数和建模关系。','三角片近似曲面，这里刻意画粗以便看清；网格三角形不是打印层。','把模型分成层，并生成外壁和填充等路径。层距为教学放大；STL 通常不统一记录单位、颜色与材料。'])
row('supp-workflow-02-hybrid-part.png',[100,790,1440],600,245,1100,
    ['1 近净成形','2 定位与精加工','3 检查关键尺寸'],['先增加所需体积，关键面留出待切除的余量。层纹仍可见。','夹具约束零件，刀具接近安装面并加工；装夹基准与刀具可达性要提前安排。','测头接触加工面，核对图纸要求。打印完成不等于零件完成。'])
row('supp-workflow-03-clear-surface.png',[90,750,1410],580,245,1110,
    ['1 打印后毛面','2 逐级打磨','3 抛光或适合的涂覆'],['表面起伏让光线分散，层纹和支撑痕会影响外观。','更细的表面仍可能有雾感；打磨还可能改变边缘与尺寸。','表面更平滑，常能更清晰，但内部缺陷、吸收、厚度和曲率仍起作用，不保证成为成像光学件。'])
add('supp-workflow-04-batch-cost.png',[((80,250,590,1060),'只做一件','这一件承担整次数据、编程和工装等准备工作，还要制造、后处理与测量。'),((750,250,2010,1060),'一次做一批','同一份准备工作由这批合格件共同分担；下面只画一份代表性的单件工作，每一件都仍要制造、后处理和检验。图形面积不表示金额，也没有标出成本交叉点。')])
row('supp-workflow-05-removal-access.png',[100,1110],880,245,1090,
    ['支撑怎样拆','粉末怎样出'],['先画出悬垂下方的临时支撑，再留出手和工具的接近空间；支撑接触面可能需要修整。','封闭空腔增加贯通出口，才有清粉机会。出口位置、尺寸和清理方法仍需验证，并不是画了孔就一定能清干净。'])
row('case-polymer-fff-positioning.png',[75,800,1525],600,235,1085,
    ['1 模板找到边缘','2 窗口约束位置','3 验证重复使用'],['绿色模板贴合灰色工件，先定义两个定位基准。此图是通用练习，不是品牌工装复刻。','窗口限定标记的位置和朝向；接触面应避免损伤工件。','检查贴合、重复定位、抓握、可视性、磨损、变形和清洁。此模板不承担钻削载荷。'])
add('case-polymer-resin-indirect.png',[((x,y,x+600,y+430),title,note) for y,titles,notes in [(255,['牙模：1 打印模型','牙模：2 热成形片材','牙模：3 脱模修边'],['打印得到实体牙模。','片材在模型上热成形，继承表面形状。','最终佩戴件是热成形片材，不是打印牙模本身。']), (800,['铸造：1 树脂型样','铸造：2 型腔与浇注','铸造：3 金属首饰'],['先打印可铸造的树脂型样。','包埋后烧除型样，留下型腔，再浇注金属。','金属首饰还需要修整。此图省略支撑、清洗、浇道和具体温控。'])] for x,title,note in zip([75,800,1525],titles,notes)])
row('case-industrial-metal-applications.png',[85,790,1495],620,275,1110,
    ['LPBF：内部路线','DED：局部加材','粘结剂喷射：批量组织'],['通用冷板示意：内部通道负责带走热，安装面另有要求；交付前要清粉、机加工和检漏。','通用轴类修复示意：在需要处补材，保留仍可用基体，再加工和验证界面、尺寸与服役要求。','通用阀体或接头示意：组织一批复杂小金属件，要一起考虑打印、烧结收缩、密封与检验。不是品牌产品图纸。'])
row('case-industrial-ceramic-core-role.png',[80,800,1520],600,275,1100,
    ['1 制作并烧结陶瓷芯','2 金属包围芯体','3 去芯留下通道'],['陶瓷芯的形状定义未来通道，需要控制烧结尺寸与强度。','芯体占据不应被金属填满的空间；这一步的金属成形属于后续铸造。','去掉芯体后，空腔继承它的大致形状，还要清理和检测。打印的是中间工具，不代表最终金属件变成陶瓷。'])
add('case-subtractive-part-features.png',[((x,y,x+1000,y+480),t,n) for x,y,t,n in [(80,250,'轴承套圈','回转和接触表面常经过车削、热处理、相应磨削与精整。外圆、内孔、端面或滚道各有要求。'),(1120,250,'外壳与孔板','铣削与钻孔协同处理凹槽、安装基准和孔的位置；先判断刀具能否接近。'),(80,770,'线切割模具','封闭内轮廓需安排穿丝，拐角仍受丝径与放电间隙限制。'),(1120,770,'蚀刻薄片','比较厚度、平整、边缘、残留与清洁，适用于理解薄垫片、网片和细密轮廓。')]])
row('case-subtractive-hybrid-access.png',[80,775,1470],650,260,1190,
    ['1 先加工开放内表面','2 增材期间安排加工','3 封闭后处理外部'],['内部仍开放时，刀具可以接近通道表面，预先标明基准和余量。','随着材料逐步增加，按可达性安排工序；封口方法需要单独设计。','内部封闭后，常规刀具可能再也无法到达。外部关键面仍需检验；此图解释可达性，不是可直接执行的打印路线。'])
# The family navigation plate contains text only: convert to reflowable cards,
# rather than baking small text into mobile raster panels.
manifest['diagram-03-families.png']={'cards':[{'title':t,'caption':n} for t,n in [('材料挤出','连续挤出丝、粒料或浆料；例：FFF、颗粒、直写。'),('槽式光聚合','选择性固化槽内树脂；例：SLA、DLP、MSLA。'),('粉末床熔融','用热能连接铺好的粉末；例：SLS、MJF、LPBF。'),('材料喷射','在目标位置喷射成形材料，可用于多材料和全彩模型。'),('粘结剂喷射','向粉末喷粘结剂，先做出生坯；可涉及金属、砂型和陶瓷。'),('定向能量沉积','送料与局部热源协同；送粉、送丝及修复。'),('片材叠层','连接片材，再形成轮廓；涉及纸、聚合物和金属箔。')]],'note':'材料不等于工艺，商品名也不等于新的工艺家族。'}
(ROOT/'references/mobile-panels.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'{len(manifest)} responsive diagrams; {sum(len(v.get("panels",[])) for v in manifest.values())} alternate panels')
