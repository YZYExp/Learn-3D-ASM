# 在线阅读主页

主页源文件在本目录，章节正文仍以`../chapters/`为准。不要直接修改生成的`content.js`。

## 构建

在仓库根目录执行：

```bash
python -m pip install -r requirements-web.txt
python scripts/build_homepage.py
```

默认生成`build/homepage/`。可用`--out /absolute/output/directory`切换输出目录。静态输出自带18份Markdown、19份PDF、114张独立图片、86张手机分图和资料说明，部署到子目录时也无需重写根路径。浏览器使用hash章节地址，刷新章节链接不依赖服务器路由。

## 发布与维护

GitHub Actions工作流见`../.github/workflows/pages.yml`。Push到main后使用已审阅的仓库PDF独立构建静态站、验证本地图片与下载链接，并部署到GitHub Pages；PR仅做构建校验。

首次在仓库Settings → Pages → Build and deployment中将Source设置为GitHub Actions。运行成功后从Actions的github-pages环境打开部署地址。项目子目录部署使用相对资源路径，章节使用hash路由，无需服务器重写。

本地完整验证：

```bash
python scripts/prepare_font.py
python scripts/build_book.py
python scripts/sync_pdfs.py
python scripts/build_homepage.py
python scripts/validate_site.py
```

## 内容与功能

- 首页工艺入口与完整分组目录。
- 搜索标题、摘要及章内正文，查询只在浏览器本地进行。
- 全章阅读、原始来源链接、图像放大、字号切换和章节翻页。
- 最近阅读章节与字号选项保存在当前浏览器的localStorage；没有数据上传或账户系统。
- 移动端目录采用抽屉，表格在窄屏中可横向滚动。
- 无外部CDN和运行时依赖；下载链接直接使用静态文件。

重建后核对：18章齐全、图片链接有效、PDF下载有效、搜索结果能打开对应章节、图像对话框能关闭。真实图与AI教学示意的原始标识应始终保留。

应用图卡由`references/application-entrypoints.json`生成；全部图像类别由`references/image-catalog.json`提供，构建会校验图片是否实际嵌入正文。新增案例来源及证据身份跟随资料一起发布。

PDF导出单独见`../.github/workflows/pdf.yml`。`python scripts/build_homepage.py --mobile-preview`生成未链接的390px iframe检查页。手机图注至少16px，分图标题18px；步骤图不与其他步骤横排。
