"""
English-only site note: mkdocs-static-i18n remains enabled for Material blog integration;
this hook is still required so posts render with the correct template and sidebar metadata.

mkdocs-static-i18n 在 on_files 中克隆 File 时，会保留 material/blog 为帖子设置的
InclusionLevel.EXCLUDED；blog 插件随后在 on_nav 里把 NOT_IN_NAV 写回的是克隆前的引用，
最终构建集合里的帖子仍是 EXCLUDED，导致文章页与摘要都不输出。

此外：i18n 的 create_i18n_file 会新建 File 实例且不复制 file.page。blog 插件的 on_files
（-50）先于 i18n（-100）执行，已为旧 File 挂上 Post；导航阶段 get_navigation 若发现
file.page 为空会再建普通 Page，导致丢失 blog-post.html 模板与侧栏元信息。本 hook 在
i18n 之后对当前 files 中的帖子重新 _resolve_post，并写回 blog.blog.posts。
重建的 Post 不含分类引用时，需清空 Category 视图的 posts 并再次执行 _generate_categories，
否则 blog-post.html 侧栏「in &lt;Category&gt;」不渲染。i18n 克隆 File 后，post.categories 中的
Category 可能与初次 on_files 时不同，需对其实际实例 read_source 并写入 meta["title"]，避免链文字为 None。

本 hook 在 on_files 末尾（优先级低于 i18n 的 -100）将 docs 内 blog 帖子改回 NOT_IN_NAV，
使其参与 mkdocs build，且不进入主导航（与 Material blog 行为一致）。

勿去掉 Post 自带的 meta.hide「navigation」：若显示全站 md-sidebar--primary，会占满最左列，
博客专用的 md-sidebar--post（Back to index、作者、Metadata、文内 TOC）会被挤到中间，观感上像
「左侧没有博客索引栏」。文内目录依赖 toc.integrate，由 blog-post.html 在 md-sidebar--post 内渲染。

说明：由 blog 生成且不在 docs_dir 下的归档/分类虚拟页仍可能被 i18n 丢弃（Unhandled file case），
见 mkdocs-static-i18n 与 material/blog 的已知限制。
"""

from __future__ import annotations

from pathlib import PurePosixPath

from material.plugins.blog.structure import Category, Post
from mkdocs.plugins import event_priority
from mkdocs.structure.files import InclusionLevel


@event_priority(-101)
def on_files(files, *, config, **kwargs):
    for f in files:
        uri = f.src_uri.replace("\\", "/")
        if uri.startswith("blog/posts/") and uri.endswith(".md"):
            if f.inclusion == InclusionLevel.EXCLUDED:
                f.inclusion = InclusionLevel.NOT_IN_NAV

    # Material 注册名为 material/blog（见 mkdocs.plugins.PluginCollection 键）
    blog = config.plugins.get("material/blog") or config.plugins.get("blog")
    view = getattr(blog, "blog", None) if blog is not None else None
    if blog is None or view is None or not blog.config.enabled:
        return files

    post_root = PurePosixPath(
        blog.config.post_dir.format(blog=blog.config.blog_dir).replace("\\", "/")
    )

    posts = []
    for file in files.documentation_pages():
        src = PurePosixPath(file.src_path.replace("\\", "/"))
        try:
            src.relative_to(post_root)
        except ValueError:
            continue
        post = blog._resolve_post(file, config)
        if not blog._is_excluded(post):
            posts.append(post)

    posts.sort(
        key=lambda p: (p.config.pin, p.config.date.created),
        reverse=True,
    )
    view.posts = posts

    if blog.config.categories:
        for v in view.views:
            if isinstance(v, Category):
                v.posts.clear()
        for post in posts:
            post.categories.clear()
        list(blog._generate_categories(config, files))
        seen = set()
        for post in posts:
            for cat in post.categories:
                cid = id(cat)
                if cid in seen:
                    continue
                seen.add(cid)
                cat.read_source(config)
                if cat.name and not cat.meta.get("title"):
                    cat.meta["title"] = cat.name

    return files


@event_priority(-100)
def on_pre_page(page, *, config, files, **kwargs):
    """populate 前将 blog 文章页归位为 Post，避免 file.page 与 blog.posts 脱节导致作者元数据未填充。"""
    uri = page.file.src_uri.replace("\\", "/")
    if not uri.startswith("blog/posts/") or not uri.endswith(".md"):
        return page

    if isinstance(page, Post) and page.file.page is page:
        return page

    blog = config.plugins.get("material/blog") or config.plugins.get("blog")
    view = getattr(blog, "blog", None) if blog is not None else None
    if blog is None or view is None or not blog.config.enabled:
        return page

    for post in view.posts:
        if post.file.src_uri.replace("\\", "/") == uri:
            post.file = page.file
            page.file.page = post
            return post

    return page
