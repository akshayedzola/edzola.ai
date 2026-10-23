import { execFileSync } from 'node:child_process';
import { readFile, writeFile } from 'node:fs/promises';

const version = '20261023a';
const css = `<link rel="stylesheet" href="/assets/site-shell.css?v=${version}">`;
const js = `<script defer src="/assets/site-shell.js?v=${version}"></script>`;
const excluded = [/^team\//, /^impactos-draft\//];
const files = execFileSync('git', ['ls-files', '*index.html'], { encoding: 'utf8' })
  .trim().split('\n').filter(Boolean);

for (const file of files) {
  let html = await readFile(file, 'utf8');
  html = html.replace(/\/assets\/crm-webform\.js\?v=[^"'&<]+/g, `/assets/crm-webform.js?v=${version}`);
  if (excluded.some((pattern) => pattern.test(file))) {
    await writeFile(file, html);
    continue;
  }
  html = html.replace(/<link rel="stylesheet" href="\/assets\/site-shell\.css\?v=[^"]+">\s*/g, '');
  html = html.replace(/<script defer src="\/assets\/site-shell\.js\?v=[^"]+"><\/script>\s*/g, '');
  if (!html.includes('</head>') || !html.includes('</body>')) throw new Error(`Cannot add site shell to ${file}`);
  html = html.replace('</head>', `${css}\n</head>`).replace('</body>', `${js}\n</body>`);
  await writeFile(file, html);
}

console.log(`Applied shared site shell to ${files.length} public pages.`);
