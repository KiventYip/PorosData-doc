# 🚀 PorosData 文档部署指南

## 📋 概述

本项目已从 Sphinx 成功迁移至 **Material for MkDocs**，提供工业级的文档基础设施，包括：

- ✅ **零警告构建** - 自动化死链修复
- ✅ **移动端完美适配** - 彻底解决侧边栏遮挡问题
- ✅ **一键中英文切换** - 原地跳转，不返回首页
- ✅ **Data-Centric AI 视觉设计** - 深邃科技感主题
- ✅ **自动化部署** - GitHub Actions + ReadTheDocs

## 🛠️ 快速开始

### 1. 本地开发环境

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/PorosData-doc.git
cd PorosData-doc

# 安装依赖
pip install -r requirements.txt

# 初始化文档 (自动创建缺失文件)
python init_docs.py

# 本地预览
mkdocs serve
```

访问 `http://localhost:8000` 查看文档。

### 2. 部署到 GitHub Pages

#### 自动部署 (推荐)

推送代码到 `main` 分支，GitHub Actions 会自动构建并部署：

```bash
git add .
git commit -m "docs: update documentation"
git push origin main
```

#### 手动部署

```bash
# 使用部署脚本
./deploy.sh --deploy

# 或直接使用 MkDocs
mkdocs gh-deploy --force
```

### 3. ReadTheDocs 集成

项目已配置 `.readthedocs.yaml`，自动识别 MkDocs 引擎：

1. 在 [ReadTheDocs](https://readthedocs.org) 导入项目
2. 选择 `MkDocs` 作为文档类型
3. 启用自动构建

## 📁 项目结构

```
PorosData-doc/
├── docs/                          # 文档源文件
│   ├── index.md                   # 英文主页
│   ├── index.zh.md               # 中文主页
│   ├── quickstart.md             # 快速开始
│   ├── design-philosophy.md      # 设计哲学
│   ├── api-reference.md          # API 参考
│   └── assets/                   # 静态资源
├── mkdocs.yml                    # 主配置文件
├── requirements.txt              # Python 依赖
├── .readthedocs.yaml             # RTD 配置
├── init_docs.py                  # 文档初始化脚本
├── deploy.sh                     # 部署脚本
└── .github/workflows/            # GitHub Actions
    └── deploy.yml
```

## 🎨 设计特色

### 移动端体验革命

- **智能隐藏**：滚动时自动隐藏顶栏，解放屏幕空间
- **抽屉导航**：左侧边栏变为从边缘滑出的抽屉
- **悬浮 TOC**：右侧目录折叠到右上角，绝不遮挡正文

### 多语言无缝切换

- **原地跳转**：切换语言时停留在当前页面
- **智能回退**：无翻译时自动显示默认语言
- **URL 同步**：地址栏实时反映当前语言

### Data-Centric AI 视觉

- **浅色模式**：纯白顶栏 + 靛蓝色强调
- **深色模式**：石板灰背景 + 青色强调 (赛博感)
- **专业字体**：Inter 正文 + JetBrains Mono 代码

## 🔧 高级配置

### 自定义主题

创建 `docs/assets/stylesheets/custom.css`：

```css
/* 自定义样式 */
:root {
    --md-primary-fg-color: #1976d2;
    --md-accent-fg-color: #00bcd4;
}
```

在 `mkdocs.yml` 中启用：

```yaml
extra_css:
  - assets/stylesheets/custom.css
```

### 添加新语言

在 `mkdocs.yml` 的 `plugins.i18n.languages` 中添加：

```yaml
- locale: ja
  name: 日本語
  build: true
```

### 版本管理

使用 [mike](https://github.com/jimporter/mike) 管理多版本：

```bash
pip install mike
mike deploy --push --update-aliases v1.0 latest
```

## 📊 监控和分析

### 构建状态

- **GitHub Actions**: 查看 `.github/workflows/deploy.yml`
- **ReadTheDocs**: 项目面板的构建历史

### 性能监控

文档加载性能通过以下优化：

- **CDN 加速**：MathJax 和其他资源使用 CDN
- **懒加载**：图片和复杂组件按需加载
- **压缩优化**：HTML/CSS/JS 自动压缩

## 🐛 故障排除

### 常见问题

#### Q: 构建时出现 "Target not found" 警告？

A: 运行文档初始化脚本：

```bash
python init_docs.py
```

#### Q: 移动端侧边栏仍然遮挡内容？

A: 确认 `mkdocs.yml` 中启用了以下特性：

```yaml
theme:
  features:
    - header.autohide    # 自动隐藏顶栏
    - toc.follow         # TOC 智能跟随
```

#### Q: 中英文切换后返回首页？

A: 确认 `mkdocs-static-i18n` 插件配置正确：

```yaml
plugins:
  - i18n:
      reconfigure_material: true  # 关键配置
```

### 获取帮助

- 📖 [Material for MkDocs 文档](https://squidfunk.github.io/mkdocs-material/)
- 🐛 [GitHub Issues](https://github.com/KiventYip/PorosData-doc/issues)
- 💬 [社区讨论](https://github.com/KiventYip/PorosData-doc/discussions)

## 📈 最佳实践

1. **定期更新依赖**：监控 `requirements.txt` 中的版本
2. **测试多语言**：确保中英文页面内容同步
3. **移动端测试**：在不同设备上验证用户体验
4. **性能监控**：关注构建时间和页面加载速度
5. **内容审核**：定期检查死链和过时信息

---

🎉 **恭喜！** 您的文档系统现已具备工业级水准。享受现代化、用户友好的文档体验！