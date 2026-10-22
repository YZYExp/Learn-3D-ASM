# 造物的加减法

以3D打印为中心的中文制造图鉴。面向出于兴趣学习的非专业读者，包含发展、工艺、材料、工作流、减材与混合制造、表面美学、当代品牌与真实案例。资料检索截止2026-10-22。

![造物的加减法：封面概念图](assets/images/01-cover.jpg)

**阅读整本：[完整PDF](pdf/Manufacturing_Atlas.pdf)** · [分章PDF](pdf/chapters/) · [图片与引用说明](references/image-rights.md)

## 在线主页

[打开《造物的加减法》在线阅读主页](https://yzyexp.github.io/Learn-3D-ASM/)

主页包含工艺导览、全书搜索、18个分章阅读入口、图片放大、字号切换、阅读进度与PDF下载。GitHub Pages由仓库中的Actions工作流部署。首次发布需在仓库Settings → Pages中选择GitHub Actions。在线内容与PDF使用同一份Markdown主稿，不另外维护重复正文。

主页源文件位于`web/`，构建方式：

```bash
python -m pip install -r requirements-web.txt
python scripts/build_homepage.py
python scripts/validate_site.py
```

默认输出到忽略的`build/homepage/`；也可使用`--out <目录>`指定静态托管目录。无运行时CDN、框架依赖或外部图片请求。部署资料见[web/README.md](web/README.md)。

## 从用途读起

本次应用增补包含25项真实案例、公开展示或典型工业任务，以及桌面外壳的完整教学练习。每项解释任务、选择工艺的原因、后处理与交付条件；真实项目、研究与作者假设分别标识。

- [应用覆盖索引](references/application-coverage.md)与[逐图清单](references/image-catalog.json)。
- 首页新增六个图像入口，或从[导读的任务表](chapters/00.md)进入相应章节。
- 当前整本140页，114张图，146个资料链接；新增17张图已嵌入书稿和阅读页。

## 手机原理图修订

14种工艺新增56张单独步骤图，按“起始 → 作用 → 累积或去除 → 完成与后处理”向下阅读，保留同一观察方向与前一步结构。28张原有横向图解在手机上改为86张竖排分图，并配可缩放字号的文字说明。分图为同一原图的阅读视图，不重复计入114张图。

步骤图记录见`references/process-sequences-*.json`；分图区域、用途和说明见`references/mobile-panels.json`。绘图脚本`draw_steps_*.py`使用同一套`process_card.py`，`draw_mobile_panels.py`可复现分图。

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
- `assets/images/`：实际嵌入的114张图片。11张AI教学示意、84张原创图解、19张真实来源图片。部分图片在不同位置复用。
- `references/all-sources.json` 与 `bibliography.md`：全书来源索引。
- `references/real-images.json` 与 `image-rights.md`：真实图片来源与权利说明。
- `references/generated-images.json` 与单独prompt文件：生成插画的创作简报、用途及提示。
- `references/coverage.md`：分类覆盖与完本检查。
- [CHANGELOG.md](CHANGELOG.md)：整理与修订记录。

## 重新构建

需要Python 3.10+、ReportLab、Pillow、pypdf，以及支持中文的TrueType字体（建议Noto Sans SC）。安装字体后设置绝对路径：

```bash
python -m pip install -r requirements.txt
python scripts/prepare_font.py
python scripts/build_book.py
```

使用现有图片时无需再次生成图像。`draw_diagrams.py`及三个`draw_*_supplements.py`脚本可复现已有精确图解及应用图；无需图像生成API。PDF与阅读页分别由对应构建脚本生成。

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

## CI与GitHub Pages

[查看网页构建与部署](https://github.com/YZYExp/Learn-3D-ASM/actions/workflows/pages.yml)。Push到main独立构建与校验18个在线章节，并随站提供仓库中已审阅的19份PDF；PR只校验。网页只依赖`requirements-web.txt`，无需字体或整书排版工具。

[PDF导出工作流](https://github.com/YZYExp/Learn-3D-ASM/actions/workflows/pdf.yml)在书稿、图源或导出脚本更新时独立运行，也支持手动运行。它检查PDF完整性并上传30天保留的Actions阅读包（下载需GitHub登录）。公开站点的PDF下载直接来自本仓库`pdf/`，修订后须运行`sync_pdfs.py`同步并提交。PDF照片使用适合文档的压缩副本，原创精确图解保持无损，网页图源保持原文件。
