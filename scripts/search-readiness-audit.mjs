import { execFileSync } from "node:child_process";
import { readFile, readdir } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url)).replace(/[\\/]$/, "");
const failures = [];
const fail = (message) => failures.push(message);

function attributes(tag) {
  const result = {};
  for (const match of tag.matchAll(/([:\w-]+)\s*=\s*(["'])(.*?)\2/gs)) {
    result[match[1].toLowerCase()] = match[3];
  }
  return result;
}

function tags(html, name) {
  return [...html.matchAll(new RegExp(`<${name}\\b[^>]*>`, "gi"))].map((match) => attributes(match[0]));
}

function sitemapUrls(xml) {
  return [...xml.matchAll(/<loc>(.*?)<\/loc>/g)].map((match) => match[1].trim());
}

function urlToFile(url) {
  const parsed = new URL(url);
  if (parsed.hostname !== "edzola.ai") throw new Error(`Unexpected sitemap host: ${url}`);
  const path = decodeURIComponent(parsed.pathname).replace(/^\//, "");
  return path ? join(root, path, "index.html") : join(root, "index.html");
}

function flattenSchema(value, output = []) {
  if (Array.isArray(value)) value.forEach((item) => flattenSchema(item, output));
  else if (value && typeof value === "object") {
    output.push(value);
    Object.values(value).forEach((item) => flattenSchema(item, output));
  }
  return output;
}

const sitemapFiles = ["sitemap.xml", "sitemap-content.xml"];
const urls = [];
for (const filename of sitemapFiles) {
  const xml = await readFile(join(root, filename), "utf8");
  urls.push(...sitemapUrls(xml));
}

const uniqueUrls = new Set(urls);
if (uniqueUrls.size !== urls.length) fail(`Sitemaps contain ${urls.length - uniqueUrls.size} duplicate URL(s)`);

let validSchemaPages = 0;
for (const url of uniqueUrls) {
  let html;
  try {
    html = await readFile(urlToFile(url), "utf8");
  } catch {
    fail(`${url}: local index.html is missing`);
    continue;
  }

  const meta = tags(html, "meta");
  const links = tags(html, "link");
  const canonical = links.find((tag) => (tag.rel || "").toLowerCase() === "canonical")?.href;
  const description = meta.find((tag) => (tag.name || "").toLowerCase() === "description")?.content;
  const robots = meta.find((tag) => (tag.name || "").toLowerCase() === "robots")?.content || "";

  if (canonical !== url) fail(`${url}: canonical is ${canonical || "missing"}`);
  if (!description?.trim()) fail(`${url}: meta description is missing`);
  if (!/<h1\b[^>]*>[\s\S]*?<\/h1>/i.test(html)) fail(`${url}: H1 is missing`);
  if (/noindex/i.test(robots)) fail(`${url}: noindex page is present in a sitemap`);

  const scripts = [...html.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)];
  if (!scripts.length) {
    fail(`${url}: JSON-LD is missing`);
  } else {
    let allValid = true;
    const objects = [];
    for (const script of scripts) {
      try {
        objects.push(...flattenSchema(JSON.parse(script[1])));
      } catch (error) {
        allValid = false;
        fail(`${url}: invalid JSON-LD (${error.message})`);
      }
    }
    if (allValid) validSchemaPages += 1;

    const locale = url.includes("/es/") ? "es-419" : url.includes("/pt/") ? "pt-BR" : null;
    if (locale) {
      const ogLocales = meta.filter((tag) => (tag.property || "").toLowerCase() === "og:locale");
      if (ogLocales.length !== 1) fail(`${url}: expected one og:locale, found ${ogLocales.length}`);
      if (!objects.some((item) => item.inLanguage === locale)) fail(`${url}: JSON-LD is missing inLanguage=${locale}`);
      if (!objects.some((item) => item.url === url || item["@id"]?.startsWith(`${url}#`))) {
        fail(`${url}: JSON-LD does not identify the localized canonical`);
      }
    }
  }
}

const trackedHtml = execFileSync("git", ["ls-files", "-z"], { cwd: root, encoding: "utf8" })
  .split("\0").filter((path) => path === "index.html" || path.endsWith("/index.html"));
const sitemapFilesByPath = new Set([...uniqueUrls].map((url) => urlToFile(url).slice(root.length + 1)));
for (const path of trackedHtml) {
  if (sitemapFilesByPath.has(path)) continue;
  const html = await readFile(join(root, path), "utf8");
  const robots = tags(html, "meta").find((tag) => (tag.name || "").toLowerCase() === "robots")?.content || "";
  if (!/noindex/i.test(robots)) fail(`${path}: tracked page is outside the sitemaps but is not noindex`);
}

const robotsText = await readFile(join(root, "robots.txt"), "utf8");
for (const agent of ["OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User", "PerplexityBot"]) {
  if (!new RegExp(`User-agent:\\s*${agent}[\\s\\S]*?Allow:\\s*/`, "i").test(robotsText)) {
    fail(`robots.txt does not explicitly allow ${agent}`);
  }
}
for (const sitemap of sitemapFiles) {
  if (!robotsText.includes(`Sitemap: https://edzola.ai/${sitemap}`)) fail(`robots.txt is missing ${sitemap}`);
}

const rootFiles = await readdir(root);
const keyFiles = rootFiles.filter((name) => /^[A-Za-z0-9-]{8,128}\.txt$/.test(name));
if (keyFiles.length !== 1) {
  fail(`expected one root IndexNow key file, found ${keyFiles.length}`);
} else {
  const key = keyFiles[0].slice(0, -4);
  const value = (await readFile(join(root, keyFiles[0]), "utf8")).trim();
  if (value !== key) fail(`${keyFiles[0]} content does not match its filename`);
}

if (failures.length) {
  console.error(`Search readiness audit failed with ${failures.length} issue(s):`);
  failures.forEach((message) => console.error(`- ${message}`));
  process.exit(1);
}

console.log(`Search readiness audit passed: ${uniqueUrls.size} indexable URLs, ${validSchemaPages} with valid JSON-LD, ${trackedHtml.length - sitemapFilesByPath.size} intentional noindex pages.`);
