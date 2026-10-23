import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "20261023a"


class SiteShellRegressionTests(unittest.TestCase):
    def test_public_pages_load_one_shared_navigation_shell(self):
        pages = subprocess.run(
            ["git", "ls-files", "*index.html"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.splitlines()
        public = [page for page in pages if not page.startswith("team/") and not page.startswith("impactos-draft/")]
        for page in public:
            source = (ROOT / page).read_text(encoding="utf-8")
            self.assertEqual(source.count(f'/assets/site-shell.css?v={VERSION}'), 1, page)
            self.assertEqual(source.count(f'/assets/site-shell.js?v={VERSION}'), 1, page)

    def test_navigation_covers_each_customer_path_and_hides_old_thesis(self):
        source = (ROOT / "assets" / "site-shell.js").read_text(encoding="utf-8")
        for menu in ("solutions", "sectors", "work", "resources", "company"):
            self.assertIn(f'data-ez-menu="{menu}"', source)
        self.assertIn('/patrons/', source)
        self.assertIn('/work/', source)
        self.assertNotIn('/why/', source)


if __name__ == "__main__":
    unittest.main()
