import os
import unittest
import tempfile
import shutil
from scripts.prepare_github_vault import organize_github_vault

class TestPrepareGithubVault(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_exclude_directories_and_files(self):
        # Create an ignored directory and a file inside it
        ignored_dir = os.path.join(self.test_dir, "scripts")
        os.makedirs(ignored_dir, exist_ok=True)
        ignored_file = os.path.join(ignored_dir, "ignored.md")
        with open(ignored_file, "w", encoding="utf-8") as f:
            f.write("[Link](test.png)")

        # Create an ignored file in root
        ignored_root_file = os.path.join(self.test_dir, "README.md")
        with open(ignored_root_file, "w", encoding="utf-8") as f:
            f.write("[Link](test.png)")

        # Create a valid directory and a file inside it to process
        valid_dir = os.path.join(self.test_dir, "VaultFolder")
        os.makedirs(valid_dir, exist_ok=True)
        valid_file = os.path.join(valid_dir, "Page.md")
        with open(valid_file, "w", encoding="utf-8") as f:
            # We reference a loose/sibling asset which needs standardizing
            f.write("[My Image](loose_image.png)")

        # Run organize_github_vault
        organize_github_vault(self.test_dir)

        # Check ignored file content was NOT touched
        with open(ignored_root_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "[Link](test.png)")

        with open(ignored_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "[Link](test.png)")

        # Check valid file was processed and standardized to Page/loose_image.png
        with open(valid_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Page/loose_image.png", content)

    def test_ignore_template_vars(self):
        valid_dir = os.path.join(self.test_dir, "VaultFolder")
        os.makedirs(valid_dir, exist_ok=True)
        valid_file = os.path.join(valid_dir, "Page.md")
        with open(valid_file, "w", encoding="utf-8") as f:
            # This contains a curly brace template, which should be ignored
            f.write("[Template Link]({encoded_base_name}/{encoded_img_name})")

        organize_github_vault(self.test_dir)

        # Check template was NOT modified
        with open(valid_file, "r", encoding="utf-8") as f:
            self.assertIn("{encoded_base_name}/{encoded_img_name}", f.read())

    def test_ignore_code_blocks(self):
        valid_dir = os.path.join(self.test_dir, "VaultFolder")
        os.makedirs(valid_dir, exist_ok=True)
        valid_file = os.path.join(valid_dir, "Page.md")

        original_content = (
            "# Page Title\n\n"
            "This link should be changed: [Real Link](real_image.png)\n\n"
            "Inside inline code: `[Ignore inline link](ignore1.png)`\n\n"
            "```markdown\n"
            "Inside fenced block:\n"
            "[Ignore fenced link](ignore2.png)\n"
            "```\n"
        )
        with open(valid_file, "w", encoding="utf-8") as f:
            f.write(original_content)

        organize_github_vault(self.test_dir)

        with open(valid_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Real link should be changed
        self.assertIn("Page/real_image.png", content)
        # Ignored links should not be changed
        self.assertIn("`[Ignore inline link](ignore1.png)`", content)
        self.assertIn("[Ignore fenced link](ignore2.png)", content)

    def test_preserve_existing_and_cross_references(self):
        # Create a parent page, a sibling page, and an organized folder
        parent_dir = os.path.join(self.test_dir, "VaultFolder")
        os.makedirs(parent_dir, exist_ok=True)

        # Sibling md page
        sibling_file = os.path.join(parent_dir, "SiblingPage.md")
        with open(sibling_file, "w", encoding="utf-8") as f:
            f.write("# Sibling")

        # Cross reference inside another database
        other_db_dir = os.path.join(self.test_dir, "OtherDatabase")
        os.makedirs(other_db_dir, exist_ok=True)
        cross_ref_file = os.path.join(other_db_dir, "CrossItem.md")
        with open(cross_ref_file, "w", encoding="utf-8") as f:
            f.write("# Cross Item")

        # Main Page
        page_file = os.path.join(parent_dir, "Page.md")
        with open(page_file, "w", encoding="utf-8") as f:
            # Sibling link, cross-reference link, and a non-existent asset link
            f.write("[Sibling](SiblingPage.md)\n"
                    "[Cross](../OtherDatabase/CrossItem.md)\n"
                    "[Missing](missing_asset.png)")

        organize_github_vault(self.test_dir)

        with open(page_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Existing files/cross-references should be untouched
        self.assertIn("[Sibling](SiblingPage.md)", content)
        self.assertIn("[Cross](../OtherDatabase/CrossItem.md)", content)
        # Non-existent asset link should be standardized to point to the companion assets directory
        self.assertIn("[Missing](Page/missing_asset.png)", content)

if __name__ == "__main__":
    unittest.main()
