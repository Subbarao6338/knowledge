import os
import unittest
import tempfile
import shutil
from scripts.organize_local_vault import organize_local_vault

class TestOrganizeLocalVault(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_moves_loose_assets_and_updates_links(self):
        # Create a parent page
        parent_md = os.path.join(self.test_dir, "MyPage.md")
        with open(parent_md, "w", encoding="utf-8") as f:
            f.write("Here is an inline image ![My Image](loose_img.png) and a link to a missing sibling [Sibling](OtherPage.md)")

        # Create the loose asset (which should be moved)
        loose_img = os.path.join(self.test_dir, "loose_img.png")
        with open(loose_img, "wb") as f:
            f.write(b"mock image content")

        # Run organize_local_vault
        organize_local_vault(self.test_dir)

        # Check that loose_img.png was moved inside MyPage/
        moved_img = os.path.join(self.test_dir, "MyPage", "loose_img.png")
        self.assertTrue(os.path.exists(moved_img))
        self.assertFalse(os.path.exists(loose_img))

        # Check that the md file was updated for loose_img.png but NOT for OtherPage.md
        with open(parent_md, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("MyPage/loose_img.png", content)
            # OtherPage.md shouldn't be touched because it wasn't a loose file to be organized
            self.assertIn("OtherPage.md", content)

    def test_dry_run_does_not_modify_disk(self):
        # Create a parent page
        parent_md = os.path.join(self.test_dir, "MyPage.md")
        with open(parent_md, "w", encoding="utf-8") as f:
            f.write("Here is an inline image ![My Image](loose_img.png)")

        # Create the loose asset
        loose_img = os.path.join(self.test_dir, "loose_img.png")
        with open(loose_img, "wb") as f:
            f.write(b"mock image content")

        # Run organize_local_vault in dry run
        organize_local_vault(self.test_dir, dry_run=True)

        # Confirm nothing changed on disk
        self.assertTrue(os.path.exists(loose_img))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "MyPage")))
        with open(parent_md, "r", encoding="utf-8") as f:
            self.assertIn("loose_img.png", f.read())

if __name__ == "__main__":
    unittest.main()
