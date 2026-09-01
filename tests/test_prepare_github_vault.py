import os
import unittest
import tempfile
import shutil
from scripts.prepare_github_vault import organize_github_vault

class TestPrepareGitHubVault(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_standardize_links_to_companion_folders(self):
        # Setup page and asset companion folder
        md_path = os.path.join(self.test_dir, "Page.md")
        companion_dir = os.path.join(self.test_dir, "Page")
        os.makedirs(companion_dir, exist_ok=True)

        asset_file = os.path.join(companion_dir, "real_image.png")
        with open(asset_file, "wb") as f:
            f.write(b"data")

        # Markdown file points to plain un-prefixed image name
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("![Image](real_image.png)\n")

        organize_github_vault(self.test_dir)

        # Content should be rewritten to Page/real_image.png
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("(Page/real_image.png)", content)

    def test_respects_exclusions(self):
        excluded_dir = os.path.join(self.test_dir, ".github")
        os.makedirs(excluded_dir, exist_ok=True)

        md_path = os.path.join(excluded_dir, "Page.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("![Image](loose_image.png)\n")

        organize_github_vault(self.test_dir)

        # File in .github should remain untouched
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("(loose_image.png)", content)

    def test_force_all_override(self):
        excluded_dir = os.path.join(self.test_dir, ".github")
        companion_dir = os.path.join(excluded_dir, "Page")
        os.makedirs(companion_dir, exist_ok=True)

        asset_file = os.path.join(companion_dir, "loose_image.png")
        with open(asset_file, "wb") as f:
            f.write(b"data")

        md_path = os.path.join(excluded_dir, "Page.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("![Image](loose_image.png)\n")

        # Process with force_all=True
        organize_github_vault(self.test_dir, force_all=True)

        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("(Page/loose_image.png)", content)

    def test_ignore_external_links_and_queries(self):
        md_path = os.path.join(self.test_dir, "Page.md")
        companion_dir = os.path.join(self.test_dir, "Page")
        os.makedirs(companion_dir, exist_ok=True)

        asset_file = os.path.join(companion_dir, "missing_asset.png")
        with open(asset_file, "wb") as f:
            f.write(b"data")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("[Web Link](https://example.com/item.png)\n[Link With Var]({template_var})\n![Asset](missing_asset.png?v=1.0)\n")

        organize_github_vault(self.test_dir)

        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("https://example.com/item.png", content)
            self.assertIn("{template_var}", content)

if __name__ == "__main__":
    unittest.main()
