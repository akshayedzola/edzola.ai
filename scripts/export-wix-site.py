#!/usr/bin/env python3
"""Export the public edzola.com Wix site into content/wix-archive/.

Wix has no full-site export, so this crawls the public sitemaps and saves,
for every page and blog post:
  - Markdown with YAML front matter (title, SEO description, dates, author,
    categories, cover image, original URL)
  - a script-free HTML snapshot (gzipped) for layout reference
  - the source of any custom "Embed HTML" blocks, which Wix loads in the
    browser and therefore never appear in the page HTML
  - every referenced image: the original into media-original/ (git-ignored,
    too large to commit) and a web copy (max 2000px, WebP) into media/

Wix never renders a post's categories, tags or video sources in its HTML, so
those come from blog-taxonomy.json, a snapshot of the Wix Blog API (List Posts
with RICH_CONTENT / List Categories / Query Tags) keyed by post slug. Refresh it from the Wix dashboard
or API before re-running if posts were re-categorised.

Usage: python3 scripts/export-wix-site.py [--site https://www.edzola.com]
"""

import argparse
import gzip
import json
import re
import sys
from html import unescape
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup
from markdownify import markdownify

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "wix-archive"
MEDIA_RE = re.compile(r"https?://static\.wixstatic\.com/media/([A-Za-z0-9_%~.\-]+?\.(?:png|jpe?g|gif|webp|svg|avif))", re.I)

session = requests.Session()


def fetch(url, binary=False, tries=4, redirects=True):
    for attempt in range(tries):
        try:
            r = session.get(url, timeout=60, allow_redirects=redirects)
            if r.status_code == 200:
                return r.content if binary else r.text
            if r.status_code in (301, 302, 404):
                return None
        except requests.RequestException:
            pass
        time.sleep(2 ** (attempt + 1))
    print(f"  ! failed: {url}", file=sys.stderr)
    return None


def sitemap_urls(site):
    index = BeautifulSoup(fetch(f"{site}/sitemap.xml"), "xml")
    urls = {}
    for loc in index.select("sitemap > loc"):
        name = loc.text.rsplit("/", 1)[-1].replace("-sitemap.xml", "")
        sm = BeautifulSoup(fetch(loc.text), "xml")
        for u in sm.select("url"):
            lastmod = u.find("lastmod")
            urls[u.find("loc").text.strip()] = {
                "sitemap": name,
                "lastmod": lastmod.text if lastmod else None,
            }
    return urls


def kind_of(url, sitemap):
    path = urlparse(url).path
    if path.startswith("/post/"):
        return "posts"
    if path.startswith("/blog/categories/"):
        return "blog-categories"
    if sitemap.startswith("dynamic-"):
        return "dynamic"
    return "pages"


def slug_of(url):
    path = urlparse(url).path.strip("/")
    return re.sub(r"[^A-Za-z0-9_\-]+", "-", path.split("/")[-1]) or "home"


def image_name(media_id):
    return unquote(media_id).replace("~", "_")


def web_name(media_id):
    name = image_name(media_id)
    return name if name.lower().endswith(".gif") else Path(name).stem + ".webp"


def make_web_copy(src, dest):
    im = Image.open(src)
    if im.format == "GIF":
        dest.write_bytes(src.read_bytes())
        return
    if max(im.size) > 2000:
        im.thumbnail((2000, 2000), Image.LANCZOS)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")
    im.save(dest, "WEBP", quality=82, method=6)


def meta(soup):
    out = {}
    for m in soup.find_all("meta"):
        key = m.get("property") or m.get("name")
        if key and m.get("content") and (key.startswith(("og:", "article:", "twitter:")) or key in ("description", "keywords", "robots")):
            out.setdefault(key, m["content"])
    canonical = soup.find("link", rel="canonical")
    if canonical:
        out["canonical"] = canonical.get("href")
    ld = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            ld.append(json.loads(s.string or ""))
        except json.JSONDecodeError:
            pass
    return out, ld


def clean(node):
    for t in node(["script", "style", "noscript", "svg", "iframe", "button", "input", "textarea", "form"]):
        t.decompose()
    for t in node.select('[aria-hidden="true"], [data-hook="skeleton-loader"]'):
        t.decompose()
    return node


def to_markdown(node, media_map):
    for img in node.find_all("img"):
        m = MEDIA_RE.search(img.get("src", "") or img.get("data-src", ""))
        if m:
            media_map.add(m.group(1))
            img["src"] = f"../media/{web_name(m.group(1))}"
            img["alt"] = " ".join((img.get("alt") or "").split())
    for a in node.find_all("a"):
        if not a.get_text(strip=True) and not a.find("img"):
            a.unwrap()
    md = markdownify(str(node), heading_style="ATX", bullets="-", strip=["span", "div", "section", "header", "footer", "main", "nav", "wow-image", "picture"])
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def frontmatter(data):
    lines = ["---"]
    for k, v in data.items():
        if v in (None, "", []):
            continue
        lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    lines.append("---\n")
    return "\n".join(lines)


def video_name(src):
    m = re.search(r"video\.wixstatic\.com/video/([^/]+)", src)
    return f"{m.group(1)}.mp4" if m else None


def extract(url, html, kind, media, videos=()):
    soup = BeautifulSoup(html, "lxml")
    m, ld = meta(soup)
    title = (soup.title.string or "").strip() if soup.title else ""
    record = {
        "url": url,
        "title": title,
        "seo_title": title,
        "description": m.get("description") or m.get("og:description"),
        "og_image": m.get("og:image"),
        "canonical": m.get("canonical"),
    }
    page_media = set()

    if kind == "posts":
        post = next((x for x in ld if x.get("@type") == "BlogPosting"), {})
        h1 = soup.select_one('[data-hook="post-title"]')
        record.update({
            "title": h1.get_text(" ", strip=True) if h1 else post.get("headline", title),
            "author": (post.get("author") or {}).get("name"),
            "published": post.get("datePublished"),
            "modified": post.get("dateModified"),
            "description": post.get("description") or record["description"],
            "cover_image": (post.get("image") or {}).get("url"),
        })
        body = soup.select_one('[data-hook="post-description"]')
        # Video players render without their source; swap them, in order, for links.
        for player, video in zip(body.select('[data-hook="video-player"]') if body else [], videos):
            local = video_name(video["url"])
            href = f"../videos/{local}" if local else video["url"]
            link = soup.new_tag("a", href=href)
            link.string = "Video: " + (video.get("title") or video["url"])
            para = soup.new_tag("p")
            para.append(link)
            player.replace_with(para)
    else:
        body = soup.find(id="PAGES_CONTAINER") or soup.find(id="SITE_PAGES") or soup.body

    md = to_markdown(clean(body), page_media) if body else ""
    for key in ("og_image", "cover_image"):
        mm = MEDIA_RE.search(record.get(key) or "")
        if mm:
            page_media.add(mm.group(1))
            record[key + "_local"] = f"media/{web_name(mm.group(1))}"
    # Background images and galleries live in markup/JSON rather than <img>.
    page_media.update(MEDIA_RE.findall(html))
    media.update(page_media)
    record["media"] = sorted({web_name(x) for x in page_media})
    record["ld_json"] = ld
    return record, md, soup


def html_embeds(site, html, soup):
    """Return [(src_url, html_text)] for the page's HtmlComponent blocks.

    External sources (e.g. a Vimeo player) are returned with html_text None.
    """
    page = soup.select_one("#SITE_PAGES > div[id]")
    if not page:
        return []
    m = re.search(r'"%s":"(\d+_[0-9a-f]+_\d+\.json)"' % re.escape(page["id"]), html)
    if not m:
        return []
    page_json = fetch(f"https://static.wixstatic.com/sites/{m.group(1)}.z?v=3")
    if not page_json:
        return []
    files_host = urlparse(site).netloc.replace(".", "-") + ".filesusr.com"
    out = []
    for item in json.loads(page_json).get("data", {}).get("document_data", {}).values():
        if item.get("type") != "HtmlComponent" or not item.get("url"):
            continue
        if item.get("sourceType") == "external":
            out.append((unescape(item["url"]), None))
            continue
        src = f"https://{files_host}/{item['url']}"
        body = fetch(src)
        if body:
            out.append((src, body))
    return out


def snapshot(soup):
    for t in soup(["script", "noscript"]):
        t.decompose()
    return gzip.compress(str(soup).encode("utf-8"), mtime=0)


def write_index(manifest):
    lines = ["# edzola.com archive index", "", "Generated by `scripts/export-wix-site.py`. See README.md for layout.", ""]
    sections = [("pages", "Pages"), ("posts", "Blog posts (newest first)"), ("dynamic", "Zoho product pages"),
                ("blog-categories", "Blog category listings")]
    for kind, heading in sections:
        rows = [m for m in manifest if m["kind"] == kind]
        if kind == "posts":
            rows.sort(key=lambda m: m.get("published") or "", reverse=True)
        lines += [f"## {heading} ({len(rows)})", ""]
        for m in rows:
            extra = f" — {m['published'][:10]}" if m.get("published") else ""
            if m.get("categories"):
                extra += f" · {', '.join(m['categories'])}"
            lines.append(f"- [{m['title']}]({m['file']}){extra}  \n  <{m['url']}>")
        lines.append("")
    lines += ["## Redirects on the Wix site", ""]
    lines += [f"- <{m['url']}> → <{m['redirect_to']}>" for m in manifest if m["kind"] == "redirects"]
    (OUT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="https://www.edzola.com")
    ap.add_argument("--skip-media", action="store_true")
    args = ap.parse_args()
    site = args.site.rstrip("/")

    urls = sitemap_urls(site)
    print(f"{len(urls)} URLs in sitemaps")
    for d in ("pages", "posts", "blog-categories", "dynamic", "media", "media-original", "html", "embeds", "videos"):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    taxonomy_file = OUT / "blog-taxonomy.json"
    taxonomy = json.loads(taxonomy_file.read_text()) if taxonomy_file.exists() else {}
    media, manifest = set(), []
    for i, (url, info) in enumerate(sorted(urls.items()), 1):
        kind = kind_of(url, info["sitemap"])
        print(f"[{i}/{len(urls)}] {kind}: {url}")
        head = session.get(url, timeout=60, allow_redirects=False)
        if head.status_code in (301, 302):
            target = head.headers.get("location")
            print(f"  redirect -> {target}")
            manifest.append({"url": url, "kind": "redirects", "redirect_to": target, **info})
            continue
        html = fetch(url)
        if not html:
            manifest.append({"url": url, "kind": kind, "error": "fetch failed"})
            continue
        slug = slug_of(url)
        post_meta = taxonomy.get(slug, {}) if kind == "posts" else {}
        record, md, soup = extract(url, html, kind, media, post_meta.get("videos", []))
        record.update(post_meta)
        fm = {k: record.get(k) for k in ("title", "url", "description", "author", "published", "modified", "categories", "tags", "featured", "minutes_to_read", "videos", "cover_image_local", "og_image_local", "seo_title")}
        fm["sitemap_lastmod"] = info["lastmod"]
        embeds = html_embeds(site, html, soup) if kind != "posts" else []
        record["embeds"] = []
        for n, (src, body) in enumerate(embeds, 1):
            if body is None:
                record["embeds"].append({"source": src})
                md += f"\n\n<!-- External embed block {n} -->\n\n[Embedded content: {src}]({src})\n"
                continue
            name = f"{slug}--{n}.html"
            (OUT / "embeds" / name).write_text(body, encoding="utf-8")
            record["embeds"].append({"source": src, "file": f"embeds/{name}"})
            embed_soup = BeautifulSoup(body, "lxml")
            embed_media = set()
            md += f"\n\n<!-- Embedded HTML block {n}: ../embeds/{name} -->\n\n" + to_markdown(clean(embed_soup.body or embed_soup), embed_media)
            media.update(embed_media)
        fm["embeds"] = [e.get("file", e["source"]) for e in record["embeds"]]
        (OUT / kind / f"{slug}.md").write_text(frontmatter(fm) + "\n" + md, encoding="utf-8")
        (OUT / "html" / f"{kind}--{slug}.html.gz").write_bytes(snapshot(soup))
        manifest.append({"kind": kind, "slug": slug, "file": f"{kind}/{slug}.md", **info,
                         **{k: v for k, v in record.items() if k != "ld_json"}, "ld_json": record["ld_json"]})

    if not args.skip_media:
        print(f"Downloading {len(media)} images")
        for j, mid in enumerate(sorted(media), 1):
            original = OUT / "media-original" / image_name(mid)
            if not original.exists():
                data = fetch(f"https://static.wixstatic.com/media/{mid}", binary=True)
                if not data:
                    continue
                original.write_bytes(data)
            web = OUT / "media" / web_name(mid)
            if not web.exists():
                make_web_copy(original, web)
            if j % 50 == 0:
                print(f"  {j}/{len(media)}")

    for post_meta in taxonomy.values():
        for video in post_meta.get("videos", []):
            dest = OUT / "videos" / (video_name(video["url"]) or "")
            if dest.suffix == ".mp4" and not dest.exists():
                data = fetch(video["url"], binary=True)
                if data:
                    dest.write_bytes(data)

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_index(manifest)
    print("Done:", {k: sum(1 for m in manifest if m["kind"] == k) for k in ("pages", "posts", "blog-categories", "dynamic", "redirects")})


if __name__ == "__main__":
    main()
