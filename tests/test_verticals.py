import json
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
VERTICAL_ROUTES = (
    "/verticals/",
    "/verticals/programme-evidence-systems/",
    "/verticals/fundraising-donor-grant-systems/",
    "/verticals/people-hr-systems/",
    "/verticals/finance-operations-systems/",
)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.titles = 0
        self.h1s = 0
        self.descriptions = 0
        self.canonicals = []
        self.stylesheets = []
        self.json_ld = []
        self._json_ld_buffer = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "title":
            self.titles += 1
        if tag == "h1":
            self.h1s += 1
        if tag == "meta" and values.get("name") == "description" and values.get("content", "").strip():
            self.descriptions += 1
        if tag == "link" and values.get("rel") == "canonical":
            self.canonicals.append(values.get("href"))
        if tag == "link" and values.get("rel") == "stylesheet":
            self.stylesheets.append(values.get("href"))
        if tag == "script" and values.get("type") == "application/ld+json":
            self._json_ld_buffer = []

    def handle_data(self, data):
        if self._json_ld_buffer is not None:
            self._json_ld_buffer.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json_ld_buffer is not None:
            self.json_ld.append("".join(self._json_ld_buffer))
            self._json_ld_buffer = None


def route_file(route):
    return ROOT / route.lstrip("/") / "index.html"


def parse_page(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


class VerticalsRegressionTests(unittest.TestCase):
    def test_every_vertical_route_has_complete_metadata(self):
        for route in VERTICAL_ROUTES:
            page = route_file(route)
            self.assertTrue(page.exists(), route)
            parsed = parse_page(page)
            self.assertEqual((parsed.titles, parsed.h1s, parsed.descriptions), (1, 1, 1), route)
            self.assertEqual(parsed.canonicals, [f"https://edzola.ai{route}"], route)
            self.assertIn("/assets/verticals.css", parsed.stylesheets, route)
            for payload in parsed.json_ld:
                json.loads(payload)

    def test_sitemap_lists_every_vertical_route(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = {element.text for element in root.findall("s:url/s:loc", namespace)}
        for route in VERTICAL_ROUTES:
            self.assertIn(f"https://edzola.ai{route}", locations)

    def test_vertical_internal_links_and_fragments_resolve(self):
        parsed_pages = {route_file(route): parse_page(route_file(route)) for route in VERTICAL_ROUTES}
        for source, parsed in list(parsed_pages.items()):
            self.assertEqual(len(parsed.ids), len(set(parsed.ids)), f"Duplicate id in {source}")
            for href in parsed.links:
                url = urlparse(href)
                if url.scheme or href.startswith(("mailto:", "tel:")):
                    continue
                if not url.path:
                    target = source
                elif url.path.startswith("/"):
                    target = ROOT / url.path.lstrip("/")
                    if url.path.endswith("/"):
                        target /= "index.html"
                else:
                    target = source.parent / url.path
                    if url.path.endswith("/"):
                        target /= "index.html"
                self.assertTrue(target.exists(), f"{source}: {href}")
                if url.fragment and target.suffix == ".html":
                    target_page = parsed_pages.setdefault(target, parse_page(target))
                    self.assertIn(url.fragment, target_page.ids, f"{source}: {href}")

    def test_transformation_story_and_proof_are_present(self):
        hub = route_file("/verticals/").read_text(encoding="utf-8")
        self.assertIn("Organisation-wide digital transformation", hub)
        self.assertIn("We de-stress the organisation", hub)
        for step in (
            "Map the real work",
            "Simplify first",
            "Stabilise the core",
            "Connect the handoffs",
            "Automate and learn",
        ):
            self.assertIn(step, hub)
        for proof in ("compass-mis", "neevjivan", "aangan-trust", "aria-cfo-services"):
            self.assertIn(proof, hub)

    def test_primary_english_entry_points_expose_verticals(self):
        for relative in ("index.html", "impact-os/index.html", "sectors/index.html", "thinking/index.html"):
            page = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn('href="/verticals/"', page, relative)


if __name__ == "__main__":
    unittest.main()
