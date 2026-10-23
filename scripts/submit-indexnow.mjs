import { execFileSync } from "node:child_process";
import { readFile, readdir } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url)).replace(/[\\/]$/, "");
const args = new Set(process.argv.slice(2));
const changedFromIndex = process.argv.indexOf("--changed-from");
const changedFrom = changedFromIndex >= 0 ? process.argv[changedFromIndex + 1] : null;

function sitemapUrls(xml) {
  return [...xml.matchAll(/<loc>(.*?)<\/loc>/g)].map((match) => match[1].trim());
}

const allUrls = new Set();
for (const filename of ["sitemap.xml", "sitemap-content.xml"]) {
  sitemapUrls(await readFile(join(root, filename), "utf8")).forEach((url) => allUrls.add(url));
}

let urlList = [...allUrls];
if (changedFrom && !args.has("--all")) {
  const changedFiles = execFileSync("git", ["diff", "--name-only", changedFrom, "HEAD"], {
    cwd: root,
    encoding: "utf8",
  }).trim().split("\n").filter(Boolean);
  const changedUrls = new Set();
  for (const path of changedFiles) {
    if (path === "index.html") changedUrls.add("https://edzola.ai/");
    else if (path.endsWith("/index.html")) changedUrls.add(`https://edzola.ai/${path.slice(0, -"index.html".length)}`);
  }
  urlList = [...changedUrls].filter((url) => allUrls.has(url));
}

if (!urlList.length) {
  console.log("IndexNow: no changed indexable URLs to submit.");
  process.exit(0);
}

const keyFiles = (await readdir(root)).filter((name) => /^[A-Za-z0-9-]{8,128}\.txt$/.test(name));
if (keyFiles.length !== 1) throw new Error(`Expected one IndexNow key file; found ${keyFiles.length}`);
const key = keyFiles[0].slice(0, -4);
const keyLocation = `https://edzola.ai/${keyFiles[0]}`;
if ((await readFile(join(root, keyFiles[0]), "utf8")).trim() !== key) {
  throw new Error("IndexNow key file content must match its filename");
}

if (args.has("--dry-run")) {
  console.log(JSON.stringify({ host: "edzola.ai", keyLocation, urlList }, null, 2));
  process.exit(0);
}

const response = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "content-type": "application/json; charset=utf-8" },
  body: JSON.stringify({ host: "edzola.ai", key, keyLocation, urlList }),
});

if (![200, 202].includes(response.status)) {
  const body = await response.text();
  throw new Error(`IndexNow returned ${response.status}: ${body.slice(0, 500)}`);
}

console.log(`IndexNow accepted ${urlList.length} URL(s) with HTTP ${response.status}.`);
