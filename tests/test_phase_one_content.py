import csv
import html
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
        with (ROOT / "content/expansion/question-bank.csv").open() as handle:
            cls.questions = list(csv.DictReader(handle))

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
            self.assertIn('/assets/crm-webform.js?v=20261023b', source)
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

    def test_public_pages_do_not_expose_internal_content_operations(self):
        forbidden = (
            "question bank",
            "1,500-question",
            "structured data",
            "written for retrieval",
            "reviewed before indexing",
            "content &amp; delivery team",
            "phase 1 backlog",
        )
        for page in self.pages:
            source = (ROOT / page["path"].strip("/") / "index.html").read_text().lower()
            for phrase in forbidden:
                self.assertNotIn(phrase, source, f"{phrase!r} leaked on {page['path']}")

    def test_visible_questions_match_the_registry_and_faq_schema(self):
        questions_by_page = {}
        for question in self.questions:
            if question["answer_status"] == "page-answered":
                questions_by_page.setdefault(question["page_id"], []).append(question)
        for page in self.pages:
            source = (ROOT / page["path"].strip("/") / "index.html").read_text()
            schema_questions = set()
            for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
                payload = json.loads(raw)
                nodes = payload.get("@graph", [payload]) if isinstance(payload, dict) else []
                for node in nodes:
                    if isinstance(node, dict) and node.get("@type") == "FAQPage":
                        schema_questions.update(item["name"] for item in node.get("mainEntity", []))
            for question in questions_by_page[page["page_id"]]:
                self.assertIn(f'data-question-id="{question["question_id"]}"', source)
                self.assertIn(f'<summary>{html.escape(question["question"])}</summary>', source)
                self.assertIn(question["question"], schema_questions)

    def test_hubs_and_homepage_make_the_library_discoverable(self):
        home = (ROOT / "index.html").read_text()
        self.assertGreaterEqual(home.count('href="/learn/"'), 3)
        self.assertIn("Implementation library", home)
        for path in ("solutions", "learn", "learn/technology", "learn/compare", "resources"):
            source = (ROOT / path / "index.html").read_text()
            canonical = f"https://edzola.ai/{path}/"
            self.assertIn(f'<link rel="canonical" href="{canonical}">', source)
            self.assertIn(f'<link rel="alternate" hreflang="x-default" href="{canonical}">', source)
            self.assertIn('<meta name="twitter:title"', source)

    def test_internal_planning_files_are_excluded_from_github_pages(self):
        config = (ROOT / "_config.yml").read_text()
        for directory in ("content", "scripts", "tests"):
            self.assertIn(f"  - {directory}", config)
        llms = (ROOT / "llms.txt").read_text()
        self.assertNotIn("Phase 1", llms)
        self.assertIn("https://edzola.ai/solutions/", llms)
        self.assertIn("https://edzola.ai/learn/", llms)
        self.assertIn("https://edzola.ai/resources/", llms)


if __name__ == "__main__":
    unittest.main()
