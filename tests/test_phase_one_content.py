import csv
import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def schema_types(source):
    found = set()
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        payload = json.loads(raw)
        nodes = payload.get("@graph", [payload]) if isinstance(payload, dict) else []
        for node in nodes:
            value = node.get("@type") if isinstance(node, dict) else None
            found.update(value if isinstance(value, list) else [value] if value else [])
    return found


class PhaseOneContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "content/expansion/content-registry.csv").open() as handle:
            cls.pages = [row for row in csv.DictReader(handle) if row["publication_status"] == "pilot-built"]

    def test_pilot_has_thirty_pages(self):
        self.assertEqual(len(self.pages), 30)

    def test_each_page_has_search_question_and_form_contract(self):
        titles, descriptions, canonicals = set(), set(), set()
        for page in self.pages:
            path = ROOT / page["path"].strip("/") / "index.html"
            self.assertTrue(path.exists(), page["path"])
            source = path.read_text()
            canonical = "https://edzola.ai" + page["path"]
            self.assertIn(f'<link rel="canonical" href="{canonical}">', source)
            self.assertIn('<meta name="robots" content="index,follow', source)
            self.assertIn('hreflang="x-default"', source)
            self.assertEqual(len(re.findall(r'data-question-id="q-\d{4}"', source)), 5)
            self.assertIn("data-crm-webform", source)
            self.assertIn("crm-form-left", source)
            self.assertIn('/assets/crm-webform.js?v=20261020b', source)
            self.assertTrue({"Article", "FAQPage"}.issubset(schema_types(source)))
            titles.add(re.search(r"<title>(.*?)</title>", source, re.S).group(1))
            descriptions.add(re.search(r'<meta name="description" content="(.*?)">', source, re.S).group(1))
            canonicals.add(canonical)
        self.assertEqual((len(titles), len(descriptions), len(canonicals)), (30, 30, 30))

    def test_content_sitemap_resolves_locally(self):
        tree = ET.parse(ROOT / "sitemap-content.xml")
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
        locations = [node.text for node in tree.getroot().iter(namespace)]
        self.assertEqual(len(locations), 35)
        self.assertEqual(len(set(locations)), 35)
        for location in locations:
            local = ROOT / urlparse(location).path.strip("/") / "index.html"
            self.assertTrue(local.exists(), location)


if __name__ == "__main__":
    unittest.main()
