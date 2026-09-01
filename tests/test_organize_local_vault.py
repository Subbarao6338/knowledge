import os
import unittest
import tempfile
import shutil
from scripts.organize_local_vault import organize_local_vault, mask_code_blocks, unmask_code_blocks

class TestOrganizeLocalVault(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_organize_local_vault_moves_loose_assets(self):
        # Create a parent page markdown and a loose asset next to it
        md_path = os.path.join(self.test_dir, "MyPage.md")
        img_path = os.path.join(self.test_dir, "loose_img.png")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# My Page\n\n![Image](loose_img.png)\n")

        with open(img_path, "wb") as f:
            f.write(b"fake image bytes")

        # Run organizer
        organize_local_vault(self.test_dir)

        # Check folder created and asset moved
        expected_folder = os.path.join(self.test_dir, "MyPage")
        expected_img_path = os.path.join(expected_folder, "loose_img.png")

        self.assertTrue(os.path.exists(expected_folder))
        self.assertTrue(os.path.exists(expected_img_path))
        self.assertFalse(os.path.exists(img_path))

        # Check markdown content link updated to percent-encoded folder link
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("MyPage/loose_img.png", content)

    def test_organize_local_vault_dry_run(self):
        md_path = os.path.join(self.test_dir, "MyPage.md")
        img_path = os.path.join(self.test_dir, "loose_img.png")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# My Page\n\n![Image](loose_img.png)\n")

        with open(img_path, "wb") as f:
            f.write(b"fake image bytes")

        organize_local_vault(self.test_dir, dry_run=True)

        # Verify nothing moved
        self.assertTrue(os.path.exists(img_path))
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("(loose_img.png)", content)

    def test_ignores_code_blocks(self):
        md_path = os.path.join(self.test_dir, "MyPage.md")
        img_path = os.path.join(self.test_dir, "loose_img.png")

        # Link is inside a fenced code block
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Code\n\n```markdown\n![Image](loose_img.png)\n```\n")

        with open(img_path, "wb") as f:
            f.write(b"fake image bytes")

        organize_local_vault(self.test_dir)

        # File should NOT be moved because it's inside code block
        self.assertTrue(os.path.exists(img_path))

    def test_mask_unmask_code_blocks_with_tilde_fences(self):
        content = "Header\n~~~python\nprint('![img](asset.png)')\n~~~\nFooter\n"
        masked, placeholders = mask_code_blocks(content)
        self.assertNotIn("asset.png", masked)
        restored = unmask_code_blocks(masked, placeholders)
        self.assertEqual(content, restored)

if __name__ == "__main__":
    unittest.main()
