# Phase 1 placement and lead-attribution plan

The 30-page pilot is organised as a second layer beneath EdZola's existing authoritative pages. It does not replace the current sector, vertical or product hubs.

## Where the pages live

| Library | Count | Parent location | How visitors discover it |
| --- | ---: | --- | --- |
| Solution and commercial guides | 8 | `/solutions/` | Programme & evidence vertical, related-guide links, and the library navigation used by every pilot page |
| Sector implementation guides | 10 | Existing sector hubs | A “Go deeper” section on the relevant education, youth employability, livelihoods, health, maternal and child health, child protection, gender, disability, or community-development page |
| DozAI missions | 5 | `/dozai/` | The existing mission library and related-mission links |
| Technology guide | 1 | `/learn/technology/` | Learn hub and related-guide links |
| Tools, templates and frameworks | 5 | `/resources/` | Homepage footer, library navigation, and related-resource links |
| Comparison guide | 1 | `/learn/compare/` | Learn hub and related-guide links |

Supporting browsing hubs also exist at `/learn/`, `/learn/technology/`, and `/learn/compare/`. The homepage footer now exposes Learn and Resources without displacing the site's existing primary navigation. This is the right pilot position: visible to crawlers and interested visitors, but not promoted as a permanent top-level navigation choice until engagement data is available.

## What every pilot page contains

- A unique title, meta description, canonical URL, index directive, Open Graph and Twitter metadata.
- Visible, crawlable HTML with a direct answer, practical workflow, minimum data model, risks, measures, human decision boundary and related links.
- `Organization`, `Article`, `WebPage`, `BreadcrumbList`, and visible-content-matched `FAQPage` JSON-LD.
- Five mapped questions from `question-bank.csv`, rendered in the page and repeated faithfully in the FAQ structured data.
- An author/review note and explicit evidence limits for claims that require legal, product, or client verification.
- A contextual Zoho CRM web form placed in the left column of the conversion section.

## Lead-source attribution

The shared CRM form reads the page's canonical URL and writes it to Zoho field `LEADCF121`. Each generated page therefore sends its own permanent source URL, rather than a generic campaign label or the visitor's potentially noisy query-string URL.

Context is supplied with `data-crm-*` attributes for the form question, placeholder, help category, title and submit label. The source URL is restored after resets and set again immediately before submission.

## Discovery files

- `sitemap-content.xml` lists the 30 pilot pages and five supporting hubs.
- `robots.txt` advertises both the existing sitemap and the content sitemap.
- `llms.txt` points to the new implementation libraries as a navigational aid. It is not treated as a substitute for crawlable HTML, ordinary SEO or internal links.

## Publication recommendation

Keep this as a reviewable 30-page pilot. Check claims, links, visual behaviour, indexing and qualified enquiries before expanding the generator to the remaining backlog. The registry records the pilot pages as `pilot-built`; that status means implemented, not editorially or legally approved for production.
