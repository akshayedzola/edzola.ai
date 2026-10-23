// Renders the shared header, mobile navigation and footer (scripts/site-shell.mjs) into every
// public page between the ez-shell markers, and versions the shared shell assets.
//
//   node scripts/build-site-shell.mjs          write changes
//   node scripts/build-site-shell.mjs --check  fail if any page is out of date (CI / pre-merge)

import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { registerLocalisedRoutes, renderFooter, renderHeader } from './site-shell.mjs';

const check = process.argv.includes('--check');
const excluded = [/^team\//, /^impactos-draft\//];
const files = execFileSync('git', ['ls-files', '*index.html', '404.html'], { encoding: 'utf8' }).trim().split('\n').filter(Boolean);
const pages = files.filter((file) => !excluded.some((pattern) => pattern.test(file)));
registerLocalisedRoutes(files);

const hash = (file) => createHash('sha256').update(readFileSync(file)).digest('hex').slice(0, 10);
const cssTag = `<link rel="stylesheet" href="/assets/site-shell.css?v=${hash('assets/site-shell.css')}">`;
const jsTag = `<script defer src="/assets/site-shell.js?v=${hash('assets/site-shell.js')}"></script>`;

const HEADER = /<!-- ez-shell:header:start( static)? -->[\s\S]*?<!-- ez-shell:header:end -->/;
const FOOTER = /<!-- ez-shell:footer:start -->[\s\S]*?<!-- ez-shell:footer:end -->/;

let stale = 0;
for (const file of pages) {
  const html = readFileSync(file, 'utf8');
  const header = html.match(HEADER);
  if (!header || !FOOTER.test(html)) throw new Error(`${file} is missing ez-shell markers`);

  const route = '/' + file.replace(/(index|404)\.html$/, '');
  const locale = /^(es|pt)\//.test(file) ? file.slice(0, 2) : 'en';
  const alternates = {};
  for (const [, lang, href] of html.matchAll(/<link rel="alternate" hreflang="([a-zA-Z-]+)" href="https:\/\/edzola\.ai([^"]*)"/g)) {
    const code = lang.slice(0, 2).toLowerCase();
    if (['en', 'es', 'pt'].includes(code)) alternates[code] = href;
  }

  let next = html
    .replace(HEADER, `<!-- ez-shell:header:start${header[1] || ''} -->${renderHeader({ locale, path: route, alternates, staticHeader: Boolean(header[1]) })}<!-- ez-shell:header:end -->`)
    .replace(FOOTER, `<!-- ez-shell:footer:start -->${renderFooter({ locale })}<!-- ez-shell:footer:end -->`)
    .replace(/[ \t]*<link rel="stylesheet" href="\/assets\/site-shell\.css\?v=[^"]+">\n?/g, '')
    .replace(/[ \t]*<script defer src="\/assets\/site-shell\.js\?v=[^"]+"><\/script>\n?/g, '');
  next = next.replace('</head>', `${cssTag}\n</head>`).replace(/<\/body>(?![\s\S]*<\/body>)/, `${jsTag}\n</body>`);

  if (next !== html) {
    stale += 1;
    if (!check) writeFileSync(file, next);
  }
}

if (check && stale) {
  console.error(`${stale} page(s) have an out-of-date site shell. Run: node scripts/build-site-shell.mjs`);
  process.exit(1);
}
console.log(check ? `Site shell is current on ${pages.length} pages.` : `Rendered the site shell into ${pages.length} pages (${stale} changed).`);
