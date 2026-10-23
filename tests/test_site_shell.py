import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECTORS = (
    "education", "youth-employability", "health", "maternal-child-health", "mental-health", "child-protection",
    "gender", "disability", "livelihoods", "environment", "waste", "food-systems", "community-development",
    "justice", "media", "arts",
)


def public_pages():
    pages = subprocess.run(
        ["git", "ls-files", "*index.html", "404.html"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.splitlines()
    return [page for page in pages if not page.startswith(("team/", "impactos-draft/"))]


def header_of(source):
    return re.search(r'<header class="ez-site-shell[\s\S]*?</header>', source).group(0)


class SiteShellRegressionTests(unittest.TestCase):
    def test_generated_shell_is_current(self):
        result = subprocess.run(
            ["node", "scripts/build-site-shell.mjs", "--check"], cwd=ROOT,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_public_pages_render_exactly_one_shared_header_and_footer(self):
        for page in public_pages():
            source = (ROOT / page).read_text(encoding="utf-8")
            self.assertEqual(source.count('<header class="ez-site-shell'), 1, page)
            self.assertEqual(source.count('<footer class="ez-footer"'), 1, page)
            self.assertEqual(len(re.findall(r'/assets/site-shell\.css\?v=', source)), 1, page)
            self.assertEqual(len(re.findall(r'/assets/site-shell\.js\?v=', source)), 1, page)
            for legacy in ('class="gh"', 'class="gh ', '<header class="site-header"', '<header class="simple-header"', '<header class="top site-top"'):
                self.assertNotIn(legacy, source, f"{page} still contains a legacy header ({legacy})")

    def test_navigation_reaches_every_customer_path(self):
        header = header_of((ROOT / "index.html").read_text(encoding="utf-8"))
        for menu in ("solutions", "sectors", "work", "resources", "company"):
            self.assertIn(f'data-ez-menu="{menu}"', header)
        for route in (
            "/verticals/", "/verticals/procurement-inventory-systems/", "/solutions/", "/learn/compare/",
            "/learn/technology/", "/resources/", "/zolabs/", "/zolashield/", "/dozai/", "/patrons/",
            "/crm/amplify/", "/work/", "/sectors/", "/impact-os/", "/thinking/", "/about/", "/news/", "/contact/",
        ):
            self.assertIn(f'href="{route}"', header, route)
        for sector in SECTORS:
            self.assertIn(f'href="/{sector}/"', header, sector)

    def test_founding_thesis_is_in_the_footer_not_the_primary_navigation(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('href="/why/"', header_of(source))
        self.assertIn('href="/why/"', re.search(r'<footer class="ez-footer"[\s\S]*?</footer>', source).group(0))

    def test_footer_keeps_legal_and_social_links(self):
        footer = re.search(r'<footer class="ez-footer"[\s\S]*?</footer>', (ROOT / "about/index.html").read_text(encoding="utf-8")).group(0)
        for href in (
            "https://www.edzola.com/privacy-policy-edzola", "https://www.edzola.com/terms-of-use",
            "https://in.linkedin.com/company/edzola", "https://www.youtube.com/@edzola", "mailto:reachus@edzola.com",
        ):
            self.assertIn(f'href="{href}"', footer)

    def test_translated_pages_get_localised_navigation_and_reciprocal_languages(self):
        header = header_of((ROOT / "es/verticals/people-hr-systems/index.html").read_text(encoding="utf-8"))
        self.assertIn(">Soluciones<", header)
        self.assertIn('href="/es/verticals/programme-evidence-systems/"', header)
        self.assertIn('href="/verticals/people-hr-systems/" lang="en"', header)
        self.assertIn('href="/pt/verticals/people-hr-systems/" lang="pt"', header)

    def test_page_specific_legal_notes_survive_the_shared_footer(self):
        notes = {
            "crm/amplify/index.html": "Claude is a trademark of Anthropic.",
            "patrons/index.html": "Pledges are non-binding until the fund opens with its fiscal sponsor.",
            "education/index.html": "Screens, names and figures on this page are illustrative examples.",
        }
        for page, note in notes.items():
            self.assertIn(note, (ROOT / page).read_text(encoding="utf-8"), page)


if __name__ == "__main__":
    unittest.main()
