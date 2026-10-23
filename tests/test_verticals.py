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
    "/verticals/procurement-inventory-systems/",
)
TRANSLATED_VERTICAL_ROUTES = tuple(
    f"/{language}{route}"
    for language in ("es", "pt")
    for route in VERTICAL_ROUTES
)
ALL_VERTICAL_ROUTES = VERTICAL_ROUTES + TRANSLATED_VERTICAL_ROUTES


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
        for route in ALL_VERTICAL_ROUTES:
            page = route_file(route)
            self.assertTrue(page.exists(), route)
            parsed = parse_page(page)
            self.assertEqual((parsed.titles, parsed.h1s, parsed.descriptions), (1, 1, 1), route)
            self.assertEqual(parsed.canonicals, [f"https://edzola.ai{route}"], route)
            self.assertTrue(any(href and href.startswith("/assets/verticals.css?") for href in parsed.stylesheets), route)
            self.assertIn("/assets/crm-webform.css?v=20261023b", parsed.stylesheets, route)
            for payload in parsed.json_ld:
                json.loads(payload)

    def test_sitemap_lists_every_vertical_route(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = {element.text for element in root.findall("s:url/s:loc", namespace)}
        for route in ALL_VERTICAL_ROUTES:
            self.assertIn(f"https://edzola.ai{route}", locations)

    def test_every_vertical_route_loads_shared_navigation_and_crm(self):
        for route in ALL_VERTICAL_ROUTES:
            page = route_file(route).read_text(encoding="utf-8")
            self.assertNotIn("/assets/verticals-nav.js", page, route)
            self.assertIn("/assets/crm-webform.js?", page, route)
            self.assertNotIn("<details open>", page, route)

    def test_vertical_language_alternates_are_reciprocal(self):
        for route in VERTICAL_ROUTES:
            slug = route.removeprefix("/verticals/")
            for localized in (route, f"/es/verticals/{slug}", f"/pt/verticals/{slug}"):
                page = route_file(localized).read_text(encoding="utf-8")
                self.assertIn(f'href="https://edzola.ai{route}"', page, localized)
                self.assertIn(f'href="https://edzola.ai/es/verticals/{slug}"', page, localized)
                self.assertIn(f'href="https://edzola.ai/pt/verticals/{slug}"', page, localized)

    def test_vertical_internal_links_and_fragments_resolve(self):
        parsed_pages = {route_file(route): parse_page(route_file(route)) for route in ALL_VERTICAL_ROUTES}
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
                    if url.fragment == "contact-form" and "crm-webform.js" in source.read_text(encoding="utf-8"):
                        continue
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

    def test_procurement_is_a_visible_finance_and_operations_focus(self):
        procurement_route = "/verticals/procurement-inventory-systems/"
        hub = route_file("/verticals/").read_text(encoding="utf-8")
        finance = route_file("/verticals/finance-operations-systems/").read_text(encoding="utf-8")
        self.assertIn(f'href="{procurement_route}"', hub)
        self.assertIn(f'href="{procurement_route}"', finance)
        for language in ("es", "pt"):
            localized_hub = route_file(f"/{language}/verticals/").read_text(encoding="utf-8")
            self.assertIn(f'href="/{language}{procurement_route}"', localized_hub)

    def test_procurement_page_covers_the_complete_control_chain(self):
        required = ("purchase request", "budget", "vendor", "quotation", "purchase order", "goods receipt", "invoice", "payment", "inventory", "audit")
        page = route_file("/verticals/procurement-inventory-systems/").read_text(encoding="utf-8").lower()
        for term in required:
            self.assertIn(term, page)

    def test_homepages_use_the_shared_navigation_and_new_entry_paths(self):
        expectations = {
            "index.html": "/verticals/",
            "es/index.html": "/es/verticals/",
            "pt/index.html": "/pt/verticals/",
        }
        for relative, vertical_route in expectations.items():
            page = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn('<header class="ez-site-shell', page, relative)
            self.assertIn(f'href="{vertical_route}"', page, relative)


if __name__ == "__main__":
    unittest.main()
