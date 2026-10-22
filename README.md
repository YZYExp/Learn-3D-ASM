# 造物的加减法

以3D打印为中心的中文制造图鉴。面向出于兴趣学习的非专业读者，包含发展、工艺、材料、工作流、减材与混合制造、表面美学、当代品牌与真实案例。资料检索截止2026-10-22。

![造物的加减法：封面概念图](assets/images/01-cover.jpg)

**阅读整本：[PDF（55页）](pdf/Manufacturing_Atlas.pdf)** · [分章PDF](pdf/chapters/) · [图片与引用说明](references/image-rights.md)

## 在线主页

[打开《造物的加减法》在线阅读主页](https://manufacturing-atlas.giving-macaw-4424.chatgpt.site)

主页包含工艺导览、全书搜索、18个分章阅读入口、图片放大、字号切换、阅读进度与PDF下载。站点初始采用私密访问。在线内容与PDF使用同一份Markdown主稿，不另外维护重复正文。

主页源文件位于`web/`，构建方式：

```bash
python -m pip install -r requirements.txt
python scripts/build_homepage.py
```

默认输出到忽略的`build/homepage/`；也可使用`--out <目录>`指定静态托管目录。无运行时CDN、框架依赖或外部图片请求。部署资料见[web/README.md](web/README.md)。

## 阅读顺序

| 文件 | 内容 |
|---|---|
| [chapters/00.md](chapters/00.md) | 导读 |
| [chapters/01.md](chapters/01.md) | 基本地图与发展 |
| [chapters/02.md](chapters/02.md) | 材料挤出、丝材、颗粒与纤维 |
| [chapters/03.md](chapters/03.md) | SLA、DLP、MSLA与连续光固化 |
| [chapters/04.md](chapters/04.md) | 聚合物SLS与MJF |
| [chapters/05.md](chapters/05.md) | 金属粉床、DED与粘结剂喷射 |
| [chapters/06.md](chapters/06.md) | 材料喷射、薄材、陶瓷、食品、建筑、生物 |
| [chapters/07.md](chapters/07.md) | 塑料、复材、树脂、金属与陶瓷材料 |
| [chapters/08.md](chapters/08.md) | CAD、切片、支撑、后处理与检验 |
| [chapters/09.md](chapters/09.md) | 车铣钻磨、电火花、激光、水刀与蚀刻 |
| [chapters/10.md](chapters/10.md) | 工艺选择、成本、模具与混合制造 |
| [chapters/11.md](chapters/11.md) | 层纹、透明、颜色、拓扑与参数化美学 |
| [chapters/12.md](chapters/12.md) | 消费级品牌与开源社区 |
| [chapters/13.md](chapters/13.md) | 专业品牌、年轻团队与行业变化 |
| [chapters/14.md](chapters/14.md) | 中国工业品牌、材料与数字化分工 |
| [chapters/15.md](chapters/15.md) | 减材品牌与造物者路径 |
| [chapters/16.md](chapters/16.md) | 四个观察与设计练习 |
| [chapters/17.md](chapters/17.md) | 术语回查与延伸阅读 |

## 文件

- `pdf/Manufacturing_Atlas.pdf`：整本阅读版，封面和目录之后使用正文页码。
- `pdf/chapters/00.pdf` 至 `pdf/chapters/17.pdf`：独立章节PDF。
- `assets/images/`：实际嵌入的25张图片。10张AI教学示意、6张原创图解、9张真实来源图片。部分图片在不同位置复用。
- `references/all-sources.json` 与 `bibliography.md`：全书来源索引。
- `references/real-images.json` 与 `image-rights.md`：真实图片来源与权利说明。
- `references/generated-images.json` 与单独prompt文件：生成插画的创作简报、用途及提示。
- `references/coverage.md`：分类覆盖与完本检查。
- [CHANGELOG.md](CHANGELOG.md)：整理与修订记录。

## 重新构建

需要Python 3.10+、ReportLab、Pillow、pypdf，以及支持中文的TrueType字体（建议Noto Sans SC）。安装字体后设置绝对路径：

```bash
python -m pip install -r requirements.txt
export BOOK_FONT=/path/to/NotoSansSC-Regular.ttf
python scripts/draw_diagrams.py
python scripts/build_book.py
```

使用现有图片时无需再次生成图像。`draw_diagrams.py`只重新绘制6张精确图解，不会调用图像生成API。构建脚本直接写PDF，不生成HTML。

源稿与相对图片路径独立于当前运行目录。PDF将当页来源显示在页脚，标题可点击；分章Markdown保留近处链接。字体不随本包再分发，需按字体自身许可安装。

## 获取与版本管理

```bash
git clone https://github.com/YZYExp/Learn-3D-ASM.git
cd Learn-3D-ASM
```

首个提交只包含0字节的README.md，后续提交纳入全书。后续修订在同一仓库增量更新。重建结果写入build/；确认后可用下列命令更新受版本管理的PDF：

```bash
python scripts/sync_pdfs.py
```

第三方图片权利不因本仓库公开或共享而转移，详见[图像权利说明](references/image-rights.md)。品牌不是购买排名，真实图与AI图在书中分别标识。
