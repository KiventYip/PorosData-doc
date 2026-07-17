# Contributing to this documentation

This page describes how to contribute to the `PorosData-doc` site: prose, structure, navigation, and blog posts in this repository only.
{: .lead}

本页说明如何向 `PorosData-doc` 站点贡献内容：包括文档正文、结构、导航以及 Blog 文章，仅限本仓库范围。

Changes to runtime behaviour or processing code usually belong in another repository; restrict pull requests here to documentation and site configuration.

运行时行为或处理代码的变更通常属于其他仓库；此处的 Pull Request 仅限于文档和站点配置。

---

## What we welcome / 欢迎的贡献类型

Contributions that improve the experience of external readers are especially valuable: clearer wording, fixed or updated internal links, missing examples or reference detail, more consistent structure across pages, corrections to navigation or cross-references, and well-researched blog essays.

以下贡献尤其受欢迎：更清晰的表述、修复或更新的内部链接、补充缺失的示例或参考细节、更一致的页面结构、导航与交叉引用的修正，以及有研究深度的 Blog 文章。

---

## General contribution workflow / 通用贡献流程

**1. Clone and enter the repository / 克隆并进入仓库**

```bash
git clone https://github.com/KiventYip/PorosData-doc.git
cd PorosData-doc
```

**2. Pull the latest remote branches / 拉取远端最新分支**

Always start from an up-to-date state. Fetch all remote branches before creating yours.

务必从最新状态开始。在创建自己的分支前，先拉取所有远端分支：

```bash
git fetch --all
git checkout main
git pull origin main
```

**3. Create a dedicated branch / 创建专用分支**

Name your branch after the change type and scope. / 以变更类型和范围命名分支：

```bash
# General documentation / 通用文档
git checkout -b docs/your-change-name

# Blog post / Blog 文章
git checkout -b feature/blog-your-post-slug
```

**4. Edit sources under `docs/` / 编辑 `docs/` 下的源文件**

Revise Markdown, tighten links between guides and reference material, and keep filenames and paths aligned with `mkdocs.yml`.

修改 Markdown，整理指南与参考材料之间的链接，并确保文件名和路径与 `mkdocs.yml` 保持一致。

**5. Run the self-review checklist / 执行自检清单**（见下方）

Complete every item before opening a pull request. The checklist is your personal quality gate — do not skip it.

在开启 Pull Request 前完成每一项。自检清单是你的个人质量关卡，不得跳过。

**6. Open a pull request with evidence / 附带证据开启 Pull Request**

Attach screenshots as required evidence. See [Pull request requirements](#pull-request-requirements--pr-提交要求) below.

附上所需截图作为证据，详见下方 [PR 提交要求](#pull-request-requirements--pr-提交要求)。

---

## Contributing a blog post / 贡献 Blog 文章

Blog essays are welcome via the pull-request flow above. This section covers blog-specific steps and the additional self-review gate that applies to all blog submissions.

Blog 文章通过上述 Pull Request 流程提交。本节介绍 Blog 专属步骤，以及所有 Blog 提交必须通过的额外自检关卡。

### Branch naming / 分支命名

Use the `feature/blog-` prefix so the purpose of the branch is immediately clear.

使用 `feature/blog-` 前缀，使分支用途一目了然：

```bash
git fetch --all
git checkout main
git pull origin main
git checkout -b feature/blog-your-post-slug
```

---

### Step 1 — Register yourself as an author / 第一步：注册作者信息

Before writing a single line of post content, confirm that your author ID exists in `docs/blog/.authors.yml`. If it does not, add it.

在写任何正文内容之前，先确认你的作者 ID 已存在于 `docs/blog/.authors.yml`。若不存在，先添加。

**File location / 文件位置：** `docs/blog/.authors.yml`

```yaml
authors:
  # ── existing entries — do NOT modify these / 已有条目，请勿修改 ─────
  porosdata:
    name: PorosData Team
    description: Project maintainers
    avatar: "assets/images/author - Kivent.png"
    url: https://github.com/KiventYip/PorosData-doc
  jianhonng:
    name: Jianhonng
    description: PorosData maintainer and technical writing
    avatar: "assets/images/author - Kivent.png"
    url: https://github.com/KiventYip

  # ── append your entry below / 在此追加你的条目 ──────────────────────
  your_author_id:                         # 全小写，不含空格，允许下划线；用于 post front matter 的 authors 字段
    name: Your Display Name               # 显示在文章作者卡片上的姓名
    description: One-line role or bio     # 显示在姓名下方的简短介绍
    avatar: "assets/images/your-avatar.png"   # 先将图片放到此路径，再填写这里
    url: https://github.com/your-handle   # 姓名链接指向的个人主页
```

**Rules / 规则：**

- The `your_author_id` key must be **lowercase with no spaces** (underscores allowed). / `your_author_id` 键必须**全小写、不含空格**（允许下划线）。
- Do **not** rename or overwrite any existing entry — each id is referenced by previously published posts. / **不得**重命名或覆盖任何已有条目，每个 id 均被已发布文章引用。
- If you do not have an avatar, reuse an existing path or omit the `avatar` field; Material will fall back to a placeholder. / 若暂无头像，可复用已有路径或省略 `avatar` 字段，Material 会使用占位图。
- Add your avatar image to `docs/assets/images/` in the same commit as the `.authors.yml` entry. / 头像图片与 `.authors.yml` 条目在同一次提交中加入 `docs/assets/images/`。

---

### Step 2 — Create the post file / 第二步：创建文章文件

Add **one Markdown file** under `docs/blog/posts/` with a date-prefixed filename.

在 `docs/blog/posts/` 下新建**一个** Markdown 文件，文件名以日期为前缀：

```
docs/blog/posts/YYYY-MM-DD-your-slug.md
```

Do **not** register the file in `mkdocs.yml` `nav` — the blog plugin generates post URLs automatically.

**不要**将该文件注册到 `mkdocs.yml` 的 `nav` 中——blog 插件会自动生成文章 URL。

---

### Step 3 — Write the front matter / 第三步：填写 front matter

Every post must open with a YAML front matter block. All fields below are required unless marked optional.

每篇文章必须以 YAML front matter 块开头，以下所有字段均为必填，标注 optional 者除外：

```yaml
---
description: >-
  One or two sentences summarising the post.
  # 一至两句话概括文章内容，显示在搜索结果、社交卡片和 Blog 索引中。
date:
  created: YYYY-MM-DD        # 发布日期，必须与文件名前缀一致
  # updated: YYYY-MM-DD      # optional — 修订已发布文章时添加
slug: YYYY-MM-DD-your-slug   # 必须与文件名一致（去掉 .md）
categories:
  - Engineering              # 从下方列表中选择一个主分类
tags:
  - Research                 # 添加 2–5 个描述性标签
authors:
  - your_author_id           # 必须已存在于 docs/blog/.authors.yml
---
```

**Allowed categories / 允许的分类** — choose the one that best fits the post's primary purpose / 选择最符合文章主旨的一项：

| Category / 分类 | Use for / 适用场景 |
|-----------------|-------------------|
| `Engineering` | Architecture decisions, pipeline design, tooling trade-offs / 架构决策、管道设计、工具权衡 |
| `Research` | Literature surveys, method analyses, exploratory findings / 文献调研、方法分析、探索性发现 |
| `Announcement` | Releases, milestones, project news / 版本发布、里程碑、项目公告 |
| `Case Study` | End-to-end walkthroughs of real processing scenarios / 真实处理场景的端到端演练 |

**Tag guidance / 标签指引：**

- Use existing tags where possible to keep the tag cloud tidy. / 尽量复用已有标签，保持标签云整洁。
- Check existing posts to see which tags are already in use. / 查阅已发布文章，了解当前使用的标签。
- Aim for two to five tags; avoid one-word tags that duplicate the category. / 目标 2–5 个标签；避免与分类名重复的单词标签。

---

### Step 4 — Structure the post body / 第四步：组织正文结构

Immediately after the front matter, add an `!!! abstract` admonition to set reader expectations.

front matter 之后，紧接一个 `!!! abstract` 提示块，向读者说明文章性质与范围：

```markdown
!!! abstract "Note"
    One or two sentences on scope, caveats, or exploratory status.
    # 示例："探索性工程笔记，非稳定产品承诺。"
```

Then write the post title as a level-1 heading (`#`), followed by an optional lead line and the `<!-- more -->` marker.

然后以一级标题（`#`）写文章标题，可选跟一句引导语，再插入 `<!-- more -->` 截断标记：

```markdown
# Your Post Title

Brief framing sentence — what the post covers and why it matters.
{: .lead}

<!-- more -->

## First section
…
```

`<!-- more -->` controls where the excerpt ends on the blog index page. Place it after the first paragraph or abstract block, not mid-sentence.

`<!-- more -->` 控制 Blog 索引页摘要的结束位置，应放在第一段或 abstract 块之后，不得截断句子中间。

**Internal links / 内部链接** — always use relative paths from the post file's location / 始终使用相对于文章文件的相对路径：

```markdown
[Home](../../index.md)
[Processor overview](../../processor/index.md)
[Another post](2026-05-06-design-insights.md)
```

Close the post with a **Further reading** line linking to related posts and product docs.

文章结尾加一行 **Further reading**，链接到相关文章和产品文档：

```markdown
---

**Further reading:** [Related Post](YYYY-MM-DD-related-slug.md) · [Processor](../../processor/index.md)

> 来源说明或免责注释（如适用）。
```

---

### Step 5 — Update the blog index / 第五步：更新 Blog 索引

Add your post to the **Recent posts** list in `docs/blog/index.md` at the top of the list.

将你的文章添加到 `docs/blog/index.md` 的 **Recent posts** 列表最顶部：

```markdown
## Recent posts

- [Your Post Title](posts/YYYY-MM-DD-your-slug.md)   ← 新增在此
- [Previous post](posts/…)
```

---

## Blog post self-review checklist / Blog 文章自检清单

Complete **every item** yourself before opening a pull request. The checklist is your own quality gate — the reviewer will ask you to fix anything you missed.

在开启 Pull Request 前，自行完成**每一项**。自检清单是你的质量关卡——评审人会要求你修复任何遗漏项。

### A. Local build / 本地构建

- [ ] Install dependencies: `pip install -r requirements.txt` / 安装依赖
- [ ] Start the local server: `mkdocs serve` / 启动本地服务
- [ ] No `ERROR` lines in the terminal output / 终端输出中无 `ERROR` 行
- [ ] Any warnings you cannot resolve are understood and will be noted in the PR / 无法解决的警告已知晓并将在 PR 中说明

### B. Author registration / 作者注册

- [ ] Your author ID exists in `docs/blog/.authors.yml` / 你的作者 ID 已存在于 `.authors.yml`
- [ ] Your avatar image is present at the path referenced in `.authors.yml` / 头像图片已存放于 `.authors.yml` 中引用的路径
- [ ] You have not modified any existing author entry / 未修改任何已有作者条目

### C. Front matter / Front matter 检查

- [ ] `description` is one or two sentences and reads naturally as a search snippet / `description` 为一至两句话，可自然作为搜索摘要
- [ ] `date.created` matches the filename date prefix (`YYYY-MM-DD`) / `date.created` 与文件名日期前缀一致
- [ ] `slug` matches the filename without the `.md` extension / `slug` 与文件名（去掉 `.md`）一致
- [ ] `categories` contains exactly one value from the allowed list / `categories` 仅含一个来自允许列表的值
- [ ] `tags` contains two to five descriptive values / `tags` 含 2–5 个描述性值
- [ ] `authors` entry exists in `docs/blog/.authors.yml` / `authors` 中的 ID 已在 `.authors.yml` 中注册

### D. Post page rendering / 文章页面渲染

- [ ] Post appears in the blog index at `http://127.0.0.1:8000/en/latest/blog/` / 文章出现在 Blog 索引页
- [ ] Post title, date, and author card render correctly on the post page / 文章页面标题、日期和作者卡片正常渲染
- [ ] Author name, description, and avatar display in the author card / 作者卡片正确显示姓名、介绍和头像
- [ ] The excerpt on the blog index ends at `<!-- more -->` as intended / Blog 索引页摘要在 `<!-- more -->` 处正确截断
- [ ] Category and tag links are clickable and lead to valid filter pages / 分类和标签链接可点击且跳转正常

### E. Content quality / 内容质量

- [ ] All internal links resolve (no 404 in browser console or MkDocs output) / 所有内部链接可正常解析，无 404
- [ ] All external links open to the intended destination / 所有外部链接跳转到目标页面
- [ ] Markdown tables render without broken columns / Markdown 表格无破损列
- [ ] Math blocks (if present) render correctly via MathJax / 数学公式块（如有）通过 MathJax 正确渲染
- [ ] Code blocks have a language specifier (` ```bash `, ` ```yaml `, etc.) / 代码块有语言标识符
- [ ] No placeholder text, draft headings, or `TODO` markers remain / 无占位文本、草稿标题或 `TODO` 标记
- [ ] The `!!! abstract` admonition is present and accurate / `!!! abstract` 提示块存在且内容准确

### F. Navigation / 导航

- [ ] Post appears at the top of the **Recent posts** list in `docs/blog/index.md` / 文章出现在 `docs/blog/index.md` 的 Recent posts 列表最顶部
- [ ] Site search returns the post for at least one keyword from the title / 站点搜索可通过标题中至少一个关键词找到该文章

---

## Pull request requirements / PR 提交要求

A blog post PR **will not be reviewed** until all of the following evidence is attached.

Blog 文章 PR 在附上以下所有证据之前**不会进入评审**。

### Required screenshots / 必须提供的截图

Take all screenshots from your local `mkdocs serve` session and upload them directly in the PR description body on GitHub.

所有截图均取自本地 `mkdocs serve` 会话，直接上传至 GitHub PR 描述正文中。

| # | What to capture / 截图内容 | Where to find it / 页面位置 |
|---|--------------------------|---------------------------|
| 1 | **Blog index page** — your post card visible (title, date, excerpt, author) / Blog 索引页，文章卡片可见（标题、日期、摘要、作者） | `…/blog/` |
| 2 | **Full post page** — title, author card with avatar, and at least one content section / 完整文章页，包含标题、带头像的作者卡片及至少一个内容区段 | `…/blog/posts/your-slug/` |
| 3 | **Category or tag filter page** — your post listed under its category / 分类或标签筛选页，文章出现在对应分类下 | `…/blog/category/your-category/` |
| 4 | **Terminal output** of `mkdocs serve` — must show no `ERROR` lines / `mkdocs serve` 终端输出，必须无 `ERROR` 行 | 你的终端 |

### PR description template / PR 描述模板

Use this template when opening the pull request. / 开启 Pull Request 时使用此模板：

```markdown
## Summary / 摘要
<!-- One paragraph: what is this post about and why does it belong here? -->
<!-- 一段话：这篇文章讲什么，为什么适合发布在这里？ -->

## Self-review checklist / 自检清单
<!-- Mark each item [x] after completing it. -->
<!-- 完成后将每项标记为 [x]。 -->
- [ ] A. Local build — no errors / 本地构建无错误
- [ ] B. Author registration complete / 作者注册完成
- [ ] C. Front matter validated / Front matter 已验证
- [ ] D. Post page renders correctly / 文章页面正常渲染
- [ ] E. Content quality checked / 内容质量已检查
- [ ] F. Blog index updated / Blog 索引已更新

## Evidence / 证据

### 1. Blog index — post card / Blog 索引页文章卡片
<!-- screenshot -->

### 2. Full post page (title + author card visible) / 完整文章页（标题 + 作者卡片可见）
<!-- screenshot -->

### 3. Category / tag filter page / 分类 / 标签筛选页
<!-- screenshot -->

### 4. Terminal — mkdocs serve output (no ERROR) / 终端输出（无 ERROR）
<!-- screenshot -->

## Notes for reviewer / 给评审人的说明
<!-- Known warnings, deferred items, or anything else the reviewer should know. -->
<!-- 已知警告、待处理事项或其他评审人需了解的内容。 -->
```

---

## Style and substance / 风格与内容要求

Write for someone encountering the project without insider context; prefer stable, product-facing language over temporary internal names. Keep section structure predictable so readers and search can rely on headings, and avoid publishing obsolete scripts, private paths, or draft-only material on public pages.

面向没有内部背景的读者写作；优先使用稳定的、面向产品的语言，而非临时内部名称。保持章节结构可预期，使读者和搜索可以依赖标题导航；避免在公开页面发布过时脚本、私有路径或仅供草稿使用的内容。

Mark posts as exploratory where appropriate (`!!! abstract "Note"` admonition) rather than letting speculative content pass as confirmed behaviour.

在适当位置将文章标记为探索性内容（使用 `!!! abstract "Note"` 提示块），而非将推测性内容作为已确认行为发布。

---

## Good first tasks / 适合新手的任务

Thin reference pages, glossary entries, runnable examples, tighter roadmap and changelog wording, and repair of stale cross-references all tend to merge cleanly and help readers immediately.

内容较薄的参考页、词汇表条目、可运行示例、更精炼的路线图和更新日志措辞，以及修复过期的交叉引用，都易于合并且能立即帮助读者。

---

## Support / 支持

Raise documentation issues or suggestions via the repository issue tracker or the discussion on your pull request.

通过仓库 Issue 追踪器或 Pull Request 讨论区提出文档问题或建议。

**Related pages:** [Home](../index.md) · [Document formatting](document-formatting.md) · [Roadmap](roadmap.md) · [Changelog](changelog.md)
