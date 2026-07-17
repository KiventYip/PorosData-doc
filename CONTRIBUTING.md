# Contributing to PorosData Documentation

本仓库接受对文档内容、结构和 Blog 文章的贡献。代码与运行时变更请提交到对应的上游仓库。

---

## 准备工作

```bash
git clone https://github.com/KiventYip/PorosData-doc.git
cd PorosData-doc
pip install -r requirements.txt
```

---

## 贡献流程

```bash
# 1. 拉取最新代码
git fetch --all && git checkout main && git pull origin main

# 2. 创建分支（文档用 docs/，Blog 用 feature/blog-）
git checkout -b feature/blog-your-post-slug

# 3. 编辑 docs/ 下的内容

# 4. 本地预览，确认无错误
mkdocs serve

# 5. 提交并推送
git add . && git commit -m "your message"
git push origin feature/blog-your-post-slug

# 6. 在 GitHub 开启 Pull Request
```

---

## 贡献 Blog 文章

### 注册作者

在 `docs/blog/.authors.yml` 末尾追加你的条目（**不得修改已有条目**）：

```yaml
your_id:
  name: Your Name
  description: 一行简介
  avatar: "assets/images/your-avatar.png"   # 无头像可省略
  url: https://github.com/your-handle
```

### 创建文章

在 `docs/blog/posts/` 下新建文件，命名格式为 `YYYY-MM-DD-your-slug.md`，**不要**将其加入 `mkdocs.yml` 的 `nav`。

文件必须包含以下 front matter：

```yaml
---
description: >-
  一至两句话概括文章内容。
date:
  created: YYYY-MM-DD
slug: YYYY-MM-DD-your-slug
categories:
  - Research        # Engineering / Research / Announcement / Case Study 选其一
tags:
  - LLM             # 2–5 个标签
authors:
  - your_id
---
```

正文结构：

```markdown
!!! abstract "Note"
    文章性质说明，如"探索性笔记，非稳定产品承诺。"

# 文章标题

引导句。
{: .lead}

<!-- more -->

## 正文...
```

最后将文章加入 `docs/blog/index.md` 的 Recent posts 列表顶部。

---

## 提交 PR 前的自检

- [ ] `mkdocs serve` 无 `ERROR`
- [ ] 文章在 Blog 索引页正常显示（标题、日期、作者卡片）
- [ ] 所有内部链接可访问，无 404
- [ ] front matter 字段完整，`authors` ID 已在 `.authors.yml` 注册
- [ ] `docs/blog/index.md` 的 Recent posts 已更新

### PR 需附截图（Evidence）

| # | 截图内容 |
|---|---------|
| 1 | Blog 索引页（文章卡片可见） |
| 2 | 文章页（标题 + 作者卡片） |
| 3 | `mkdocs serve` 终端输出（无 ERROR） |

---

## 问题与反馈

通过 [GitHub Issues](https://github.com/KiventYip/PorosData-doc/issues) 提交，文档类问题请使用 `documentation` 标签。
