"""
Material blog build helper (English-only site; mkdocs-static-i18n is not used).

Historically, mkdocs-static-i18n cloned `File` objects in `on_files` in a way that
left Material blog posts at `InclusionLevel.EXCLUDED`, dropped category pages with
`Unhandled file case`, and broke `file.page` / `Post` wiring. This hook remains so
we still:

- Promote `docs/blog/posts/*.md` from `EXCLUDED` to `NOT_IN_NAV` so they are built
  but do not appear in the main nav.
- Re-resolve posts, sort them, and refresh `blog.blog.posts`.
- When categories are enabled, clear stale category views, re-run `_generate_categories`,
  and ensure category titles are populated for sidebar links.

`on_pre_page` re-attaches the `Post` instance before population so author/read-time
metadata and `blog-post.html` behave correctly.

Do not remove `meta.hide: navigation` from posts: exposing the primary sidebar on
post pages breaks the dedicated `md-sidebar--post` layout (back link, metadata, TOC).

Priority `-101` on `on_files` runs late enough to run after the blog plugin’s own
`on_files` pass; adjust only if plugin order changes upstream.
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
