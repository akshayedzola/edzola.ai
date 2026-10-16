import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORM_SCRIPT = ROOT / "assets" / "crm-webform.js"
ASSET_VERSION = "20261015i"


class CrmWebformRegressionTests(unittest.TestCase):
    def test_reset_control_cannot_shadow_the_native_form_reset_method(self):
        source = FORM_SCRIPT.read_text(encoding="utf-8")
        reset_control = re.search(r'<input type="reset"[^>]*>', source)

        self.assertIsNotNone(reset_control, "The Clear control should remain available")
        self.assertNotRegex(
            reset_control.group(0),
            r'\bname="reset"',
            "A named reset control replaces form.reset and breaks the success flow",
        )
        self.assertIn(
            "HTMLFormElement.prototype.reset.call(form);",
            source,
            "Successful submissions should use the native reset method explicitly",
        )

    def test_every_page_uses_the_current_shared_form_script(self):
        tracked_html = subprocess.run(
            ["git", "ls-files", "*.html"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        references = []
        stale = []

        for relative_path in tracked_html:
            page = (ROOT / relative_path).read_text(encoding="utf-8")
            if "crm-webform.js?v=" not in page:
                continue
            references.append(relative_path)
            if f"crm-webform.js?v={ASSET_VERSION}" not in page:
                stale.append(relative_path)

        self.assertGreater(len(references), 0, "At least one page must load the CRM form")
        self.assertEqual(
            stale,
            [],
            "Every page must use the new cache key for the corrected shared form script",
        )


if __name__ == "__main__":
    unittest.main()
