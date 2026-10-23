# edzola.com Wix archive

A full content export of the old Wix site (www.edzola.com), taken so the site
can be rebuilt off Wix. Wix has no site export, so
`scripts/export-wix-site.py` crawls the public sitemaps and saves everything
here. `content/` is excluded from the Jekyll build (`_config.yml`), so none of
this is published.

Start with [INDEX.md](INDEX.md), which lists every page and post with its
original URL.

## Layout

| Path | What it holds |
|---|---|
| `posts/` | 84 blog posts as Markdown. Front matter has title, SEO description, author, publish/modified dates, categories, tags, featured flag, read time, videos and cover image. |
| `pages/` | 19 site pages as Markdown (home, contact, team, education MIS, ZolaShield, …). |
| `dynamic/` | 15 Zoho product pages (`/zoho-products/*`). |
| `blog-categories/` | 10 blog category listing pages. |
| `embeds/` | Full source of the custom "Embed HTML" blocks. ZolaShield, CRM & Business Apps, ImpactOS, Education MIS and parts of the home page are built this way, so these files are the real page source. |
| `media/` | Every image the site references, resized to max 2000px and converted to WebP. Markdown links point here. |
| `videos/` | The 6 videos uploaded to Wix (used in one AI tools post). YouTube and Vimeo videos stay as links. |
| `html/` | A gzipped HTML snapshot of each page with scripts removed, for checking layout. |
| `blog-taxonomy.json` | Post categories, tags and video sources from the Wix Blog API. Wix doesn't show these in the public HTML. |
| `manifest.json` | Everything per URL: SEO meta, Open Graph, JSON-LD, sitemap lastmod, images used, embeds. |
| `media-original/` | Full-resolution originals (~390 MB). **Git-ignored.** The script recreates it locally. |

## Before Wix is switched off

- **Full-resolution images:** run `python3 scripts/export-wix-site.py` on a
  machine you keep, and copy `media-original/` to Drive or other storage.
  `static.wixstatic.com` links stop working once the site is closed.
- **Redirects:** add redirects on the new host for every old URL
  (`/post/<slug>`, `/blog/categories/<slug>`, `/zoho-products/<slug>`, plus the
  three listed at the end of INDEX.md) so search rankings and backlinks carry
  over.
- **Not in this export** (they aren't public pages, so get them from the Wix
  dashboard): form submissions, contacts and newsletter subscribers, blog
  comments, members, pricing plans and invoices, and Velo code.

## Re-running

```sh
pip install requests beautifulsoup4 lxml markdownify pillow
python3 scripts/export-wix-site.py
```

The script picks up new pages and posts from the sitemaps. Refresh
`blog-taxonomy.json` from the Wix Blog API if posts get new categories, tags or
videos.
