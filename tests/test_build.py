import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build

DOCS = ROOT / "docs"
STARTER = ROOT / "starter"


def read_doc_texts():
    return sorted(DOCS.glob("*.md"))


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`]+`", "", text)


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="site-"))
        build.build(cls.tmp)
        cls.docs = build.read_docs()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_every_doc_builds_to_html(self):
        built = {p.stem for p in self.tmp.glob("*.html")}
        for slug in self.docs:
            self.assertIn(slug, built)

    def test_index_page_exists(self):
        index = (self.tmp / "index.html").read_text(encoding="utf-8")
        self.assertIn("Second Brain Basics", index)
        self.assertIn("start-here.html", index)

    def test_no_unresolved_wiki_links_in_site(self):
        for page in self.tmp.glob("*.html"):
            html_text = page.read_text(encoding="utf-8")
            self.assertNotIn('class="promised"', html_text,
                             f"unresolved wiki-link in {page.name}")

    def test_internal_links_target_existing_files(self):
        for page in list(self.tmp.glob("*.html")):
            html_text = page.read_text(encoding="utf-8")
            for href in re.findall(r'href="([^"#?]+\.html)', html_text):
                self.assertTrue((self.tmp / href).exists(),
                                f"{page.name} has broken link {href}")

    def test_glossary_anchors_exist_in_glossary_page(self):
        glossary_ids = set(re.findall(r'<h3 id="([^"]+)"',
                            (self.tmp / "glossary.html").read_text(
                                encoding="utf-8")))
        for page in self.tmp.glob("*.html"):
            html_text = page.read_text(encoding="utf-8")
            for anchor in re.findall(r'href="glossary.html#([^"]+)"', html_text):
                self.assertIn(anchor, glossary_ids,
                              f"{page.name} points at missing term {anchor}")

    def test_pages_carry_footer_and_title(self):
        for page in self.tmp.glob("*.html"):
            html_text = page.read_text(encoding="utf-8")
            self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", html_text)
            self.assertIn("<title>", html_text)

    def test_cli_build_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, "build.py", "--out", tmp],
                cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Built", result.stdout)


class SourceIntegrityTests(unittest.TestCase):
    def test_wiki_links_in_docs_resolve(self):
        doc_map = {build.page_slug(p): p for p in read_doc_texts()}
        glossary_text = (DOCS / "08-glossary.md").read_text(encoding="utf-8")
        glossary_terms = {
            build.term_slug(t)
            for t in re.findall(r"^### (.+)$", glossary_text, re.M)}
        for path in read_doc_texts():
            text = strip_code(path.read_text(encoding="utf-8"))
            for target in re.findall(r"\[\[([^\]|]+)\]\]", text):
                self.assertTrue(
                    target in doc_map or target.lower() in glossary_terms,
                    f"{path.name} has wiki-link that resolves nowhere: {target}")

    def test_glossary_terms_are_alphabetical(self):
        text = (DOCS / "08-glossary.md").read_text(encoding="utf-8")
        terms = [t.strip() for t in re.findall(r"^### (.+)$", text, re.M)]
        self.assertEqual(terms, sorted(terms, key=lambda s: s.lower()))

    def test_starter_templates_exist(self):
        required = ["daily-note.md", "fleeting-note.md", "project-note.md",
                    "archive-note.md", "hub-note.md", "agent-brief.md"]
        for name in required:
            self.assertTrue((STARTER / "templates" / name).exists(),
                            f"missing template {name}")

    def test_starter_daily_note_uses_iso_date_name(self):
        for path in (STARTER / "90-daily").glob("*.md"):
            self.assertRegex(path.name, r"^\d{4}-\d{2}-\d{2}\.md$")

    def test_starter_wiki_links_resolve_within_vault(self):
        files = {p.stem.lower() for p in STARTER.rglob("*.md")}
        for path in STARTER.rglob("*.md"):
            if path.parts[-1] == "README.md" and path.parent.name == "templates":
                continue
            if "templates" in path.parts:
                continue
            text = strip_code(path.read_text(encoding="utf-8"))
            for target in re.findall(r"\[\[([^\]]+)\]\]", text):
                target = target.strip().lower()
                self.assertNotEqual(target, "",
                                    f"empty wiki-link in {path}")
                hits = [f for f in files
                        if f == target or f.endswith(f"-{target}")]
                self.assertTrue(hits,
                                f"{path} wiki-link resolves nowhere: {target}")

    def test_no_secrets_committed_anywhere(self):
        secret_patterns = [
            re.compile(r"sk-[A-Za-z0-9]{16,}"),
            re.compile(r"""(?i)api[_-]?key\s*[=:]\s*["'][A-Za-z0-9_-]{12,}""")
        ]
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in secret_patterns:
                self.assertIsNone(pattern.search(text),
                                  f"possible secret in {path}")

    def test_license_has_exact_copyright_line(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", license_text)
        self.assertIn("MIT License", license_text)

    def test_readme_credits_asdale_dynamics(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)


if __name__ == "__main__":
    unittest.main()
