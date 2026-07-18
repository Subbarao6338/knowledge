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

if __name__ == "__main__":
    unittest.main()
