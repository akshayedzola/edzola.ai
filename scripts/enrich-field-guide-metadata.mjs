import { readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const contentDir = join(root, "content/field-guides/technology-that-sticks");
const outputDir = join(root, "field-guides/technology-that-sticks");
const files = [
  "01_mission-rich-systems-poor.md",
  "02_three-jobs-in-order.md",
  "03_what-we-cant-do.md",
  "04_problem-first-tool-last.md",
  "05_when-the-project-hits-a-wall.md",
  "06_warmth-is-how-standards-travel.md",
  "07_stop-rebuilding-the-same-system.md",
];

function frontmatter(source) {
  const match = source.match(/^---\n([\s\S]*?)\n---/);
  if (!match) throw new Error("Missing frontmatter");
  return Object.fromEntries(match[1].split("\n").map((line) => {
    const pair = line.match(/^([a-z_]+):\s*(.*)$/);
    return pair ? [pair[1], pair[2].replace(/^"|"$/g, "")] : null;
  }).filter(Boolean));
}

function escapeAttribute(value) {
  return value.replaceAll("&", "&amp;").replaceAll('"', "&quot;");
}

for (const filename of files) {
  const meta = frontmatter(await readFile(join(contentDir, filename), "utf8"));
  const path = join(outputDir, meta.slug, "index.html");
  const canonical = `https://edzola.ai/field-guides/technology-that-sticks/${meta.slug}/`;
  const graph = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": "https://edzola.ai/#org",
        name: "EdZola",
        legalName: "EdZola Technologies Private Limited",
        url: "https://edzola.ai/",
        logo: "https://edzola.ai/assets/apple-touch-icon.png",
      },
      {
        "@type": "Person",
        "@id": "https://edzola.ai/about/#akshay",
        name: "Akshay V",
        jobTitle: "Founder & CEO",
        worksFor: { "@id": "https://edzola.ai/#org" },
      },
      {
        "@type": "Article",
        "@id": `${canonical}#article`,
        headline: meta.title,
        description: meta.meta_description,
        datePublished: meta.date_published,
        dateModified: meta.date_modified,
        inLanguage: "en-GB",
        mainEntityOfPage: { "@id": `${canonical}#page` },
        author: { "@id": "https://edzola.ai/about/#akshay" },
        publisher: { "@id": "https://edzola.ai/#org" },
        image: "https://edzola.ai/assets/og-edzola.png",
      },
      {
        "@type": "WebPage",
        "@id": `${canonical}#page`,
        url: canonical,
        name: `${meta.title} | EdZola Field Guides`,
        description: meta.meta_description,
        inLanguage: "en-GB",
        breadcrumb: { "@id": `${canonical}#breadcrumb` },
        isPartOf: { "@id": "https://edzola.ai/#site" },
      },
      {
        "@type": "BreadcrumbList",
        "@id": `${canonical}#breadcrumb`,
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Thinking", item: "https://edzola.ai/thinking/" },
          { "@type": "ListItem", position: 2, name: "Building technology that sticks", item: "https://edzola.ai/field-guides/technology-that-sticks/" },
          { "@type": "ListItem", position: 3, name: meta.title, item: canonical },
        ],
      },
      {
        "@type": "WebSite",
        "@id": "https://edzola.ai/#site",
        url: "https://edzola.ai/",
        name: "EdZola",
        publisher: { "@id": "https://edzola.ai/#org" },
      },
    ],
  };
  const title = escapeAttribute(meta.title);
  const description = escapeAttribute(meta.meta_description);
  const block = `<!-- seo:field-guide:start -->
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta property="og:site_name" content="EdZola"><meta property="og:locale" content="en_GB">
<meta name="twitter:title" content="${title}"><meta name="twitter:description" content="${description}"><meta name="twitter:image" content="https://edzola.ai/assets/og-edzola.png">
<script type="application/ld+json">${JSON.stringify(graph).replaceAll("<", "\\u003c")}</script>
<!-- seo:field-guide:end -->`;

  let html = await readFile(path, "utf8");
  html = html.replace(/<!-- seo:field-guide:start -->[\s\S]*?<!-- seo:field-guide:end -->\n?/, "");
  const anchor = '<link rel="preconnect" href="https://fonts.googleapis.com">';
  if (!html.includes(anchor)) throw new Error(`Missing metadata anchor in ${path}`);
  html = html.replace(anchor, `${block}\n${anchor}`);
  await writeFile(path, html);
}

console.log(`Enriched ${files.length} field essays without rewriting page content.`);
