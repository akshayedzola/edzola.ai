import { readFile, mkdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const contentDir = join(root, "content/field-guides/technology-that-sticks");
const outputRoot = join(root, "field-guides/technology-that-sticks");
const files = [
  "01_mission-rich-systems-poor.md",
  "02_three-jobs-in-order.md",
  "03_what-we-cant-do.md",
  "04_problem-first-tool-last.md",
  "05_when-the-project-hits-a-wall.md",
  "06_warmth-is-how-standards-travel.md",
  "07_stop-rebuilding-the-same-system.md",
];

const escapeHtml = (value) => value
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;");

function inline(value) {
  return escapeHtml(value)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
}

function parse(source) {
  const [, rawMeta = "", body = source] = source.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/) || [];
  const meta = {};
  for (const line of rawMeta.split("\n")) {
    const match = line.match(/^([a-z_]+):\s*(.*)$/);
    if (match) meta[match[1]] = match[2].replace(/^"|"$/g, "");
  }

  const lines = body.trim().split("\n");
  const html = [];
  let paragraph = [];
  let list = [];
  let quote = [];

  const flushParagraph = () => {
    if (paragraph.length) html.push(`<p>${inline(paragraph.join(" "))}</p>`);
    paragraph = [];
  };
  const flushList = () => {
    if (list.length) html.push(`<ul>${list.map((item) => `<li>${inline(item)}</li>`).join("")}</ul>`);
    list = [];
  };
  const flushQuote = () => {
    if (quote.length) html.push(`<blockquote>${inline(quote.join(" "))}</blockquote>`);
    quote = [];
  };
  const flush = () => { flushParagraph(); flushList(); flushQuote(); };

  for (const line of lines) {
    if (!line.trim()) { flush(); continue; }
    if (line === "---") { flush(); html.push("<hr>"); continue; }
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      flush();
      const level = heading[1].length;
      if (level === 1) continue;
      const id = heading[2].toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
      html.push(`<h${level} id="${id}">${inline(heading[2])}</h${level}>`);
      continue;
    }
    if (line.startsWith("- ")) { flushParagraph(); flushQuote(); list.push(line.slice(2)); continue; }
    if (line.startsWith("> ")) { flushParagraph(); flushList(); quote.push(line.slice(2)); continue; }
    flushList(); flushQuote(); paragraph.push(line.trim());
  }
  flush();
  return { meta, html: html.join("\n") };
}

const records = [];
for (const file of files) {
  const parsed = parse(await readFile(join(contentDir, file), "utf8"));
  records.push(parsed.meta);
}

for (let index = 0; index < files.length; index += 1) {
  const { meta, html } = parse(await readFile(join(contentDir, files[index]), "utf8"));
  const previous = records[index - 1];
  const next = records[index + 1];
  const canonical = `https://edzola.ai/field-guides/technology-that-sticks/${meta.slug}/`;
  const page = `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${escapeHtml(meta.title)} | EdZola Field Guides</title>
<meta name="description" content="${escapeHtml(meta.meta_description)}">
<link rel="canonical" href="${canonical}">
<meta property="og:type" content="article"><meta property="og:title" content="${escapeHtml(meta.title)}"><meta property="og:description" content="${escapeHtml(meta.meta_description)}"><meta property="og:url" content="${canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/thinking/reading.css">
</head>
<body>
<header class="reading-header"><div class="reading-wrap"><a class="reading-logo" href="/">edzola.ai</a><nav aria-label="Breadcrumb"><a href="/thinking/">Thinking</a><span>/</span><a href="/field-guides/technology-that-sticks/">Technology that sticks</a></nav></div></header>
<main>
  <article class="essay">
    <header class="essay-head"><span class="kicker">${escapeHtml(meta.series)} · ${escapeHtml(meta.reading_time)} read</span><h1>${escapeHtml(meta.title)}</h1><p class="dek">${escapeHtml(meta.subtitle)}</p><p class="byline">By ${escapeHtml(meta.author)}</p></header>
    <div class="essay-body">${html}</div>
  </article>
  <nav class="essay-nav" aria-label="Field essay navigation">
    ${previous ? `<a href="/field-guides/technology-that-sticks/${previous.slug}/"><span>Previous essay</span><strong>← ${escapeHtml(previous.title)}</strong></a>` : `<a href="/field-guides/technology-that-sticks/"><span>Full field guide</span><strong>← Building technology that sticks</strong></a>`}
    ${next ? `<a class="next" href="/field-guides/technology-that-sticks/${next.slug}/"><span>Next essay</span><strong>${escapeHtml(next.title)} →</strong></a>` : `<a class="next" href="/field-guides/technology-that-sticks/"><span>Return to</span><strong>The complete field guide →</strong></a>`}
  </nav>
</main>
<footer class="reading-footer"><div class="reading-wrap"><span>EdZola Technologies · Systems built for the world's hardest work.</span><a href="/thinking/">Explore how we think →</a></div></footer>
</body>
</html>`;
  const destination = join(outputRoot, meta.slug, "index.html");
  await mkdir(dirname(destination), { recursive: true });
  await writeFile(destination, page);
}

console.log(`Built ${files.length} field essays.`);
