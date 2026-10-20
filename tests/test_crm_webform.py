import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORM_SCRIPT = ROOT / "assets" / "crm-webform.js"
AMPLIFY_PAGE = ROOT / "crm" / "amplify" / "index.html"
HOME_PAGE = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
ASSET_VERSION = "20261020a"


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
        self.assertIn("var preserveStatus=false;", source)
        self.assertIn("if(!keepStatus)showStatus('',false);", source)
        self.assertIn("helpField.value=helpDefaults[contextKey]||'-None-';", source)

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

    def test_amplify_has_one_crm_backed_application_flow(self):
        page = AMPLIFY_PAGE.read_text(encoding="utf-8")

        self.assertIn('data-crm-webform', page)
        self.assertIn('href="#contact-form"', page)
        self.assertNotIn('id="elig"', page)
        self.assertNotIn('Amplify%20cohort%20application', page)
        self.assertNotIn('id="c-crm"', page)

    def test_amplify_form_is_contextual_and_defaults_to_crm(self):
        source = FORM_SCRIPT.read_text(encoding="utf-8")

        self.assertIn("path.indexOf('/crm/amplify/')===0?'amplify'", source)
        self.assertIn("'amplify':'CRM'", source)
        self.assertIn("Send my Amplify application", source)

    def test_vertical_pages_use_contextual_embedded_form_and_capture_query_links(self):
        source = FORM_SCRIPT.read_text(encoding="utf-8")

        self.assertIn("'verticals':{", source)
        self.assertIn("'verticals':'Data Systems – MIS / ERP'", source)
        self.assertIn('a[href^="/contact/"]', source)

    def test_shared_form_localizes_visible_ui_for_spanish_and_portuguese(self):
        source = FORM_SCRIPT.read_text(encoding="utf-8")

        self.assertIn("es:{formTitle:'Cuéntanos un poco sobre tu trabajo.'", source)
        self.assertIn("pt:{formTitle:'Conte um pouco sobre o seu trabalho.'", source)
        self.assertIn("if(contextKey==='verticals'&&locale==='es')", source)
        self.assertIn("if(contextKey==='verticals'&&locale==='pt')", source)

    def test_amplify_is_promoted_and_in_the_sitemap(self):
        home = HOME_PAGE.read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        self.assertIn('href="https://edzola.ai/crm/amplify/"', home)
        self.assertIn('Amplify CRM cohort', home)
        self.assertIn('<loc>https://edzola.ai/crm/amplify/</loc>', sitemap)


if __name__ == "__main__":
    unittest.main()
