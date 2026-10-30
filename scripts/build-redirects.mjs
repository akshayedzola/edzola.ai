// Turns every page on edzola.ai into a redirect to the same path on edzola.com.
// GitHub Pages cannot send HTTP 301s, so each page becomes a small static redirect page
// (canonical link + meta refresh + JS that also carries the query string and hash).
//
//   node scripts/build-redirects.mjs          write redirect pages
//   node scripts/build-redirects.mjs --check  fail if any page is not a redirect page (CI / pre-merge)
//
// A page redirects to the same path on edzola.com. Pages listed in HOMEPAGE_ONLY have no
// equivalent there, and 404.html (any unknown URL) is also sent to the homepage.

import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

const check = process.argv.includes('--check');
const ORIGIN = 'https://edzola.com';

// Internal pages that were never moved to edzola.com.
const HOMEPAGE_ONLY = new Set(['team/', 'team/grove/', 'team/impactos/', 'team/impactos/playbooks/', 'team/insight/']);

const files = execFileSync('git', ['ls-files', '*.html'], { encoding: 'utf8' }).trim().split('\n').filter(Boolean);

const targetFor = (file) => {
  if (file === '404.html') return `${ORIGIN}/`;
  const route = file.replace(/index\.html$/, '');
  if (HOMEPAGE_ONLY.has(route)) return `${ORIGIN}/`;
  return route === '' ? `${ORIGIN}/` : `${ORIGIN}/${route.replace(/\/$/, '')}`;
};

const render = (target) => `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EdZola has moved to edzola.com</title>
<link rel="canonical" href="${target}">
<script>location.replace(${JSON.stringify(target)} + location.search + location.hash);</script>
<meta http-equiv="refresh" content="0; url=${target}">
</head>
<body>
<p>EdZola has moved. <a href="${target}">Continue to edzola.com</a>.</p>
</body>
</html>
`;

let stale = 0;
for (const file of files) {
  const html = render(targetFor(file));
  if (readFileSync(file, 'utf8') === html) continue;
  stale += 1;
  if (!check) writeFileSync(file, html);
}

if (check && stale) {
  console.error(`${stale} page(s) are not redirect pages; run node scripts/build-redirects.mjs`);
  process.exit(1);
}
console.log(check ? `All ${files.length} pages redirect to edzola.com` : `Wrote ${stale} redirect page(s) of ${files.length}`);
