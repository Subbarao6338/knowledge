import os
import unittest
import tempfile
import shutil
from unittest.mock import MagicMock, patch
from scripts.archive_forum import ForumArchiver

class TestArchiveForum(unittest.TestCase):
    def setUp(self):
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    @patch('requests.Session.get')
    def test_scrape_thread_single_page_with_images(self, mock_get):
        # Setup mock responses
        html_content = """
        <html>
            <body>
                <div class="story-content">
                    <p>This is a paragraph.</p>
                    <img src="assets/image1.jpg" />
                </div>
                <a href="/thread?page=2" class="next">Next Page</a>
            </body>
        </html>
        """

        page2_content = """
        <html>
            <body>
                <div class="story-content">
                    <p>This is page 2.</p>
                </div>
                <!-- No next link -->
            </body>
        </html>
        """

        # Mock image download response
        image_response = MagicMock()
        image_response.status_code = 200
        image_response.iter_content = lambda chunk_size: [b"mockimagebytes"]

        response1 = MagicMock()
        response1.status_code = 200
        response1.text = html_content

        response2 = MagicMock()
        response2.status_code = 200
        response2.text = page2_content

        # Handle requests in order
        mock_get.side_effect = [response1, image_response, response2]

        archiver = ForumArchiver(output_dir=self.output_dir, delay=0.0)
        archiver.scrape_thread("https://example.com/my-thread.html", "div.story-content")

        # Verify pages are saved correctly
        page1_path = os.path.join(self.output_dir, "my-thread-Page-1.md")
        page2_path = os.path.join(self.output_dir, "my-thread-Page-2.md")

        self.assertTrue(os.path.exists(page1_path))
        self.assertTrue(os.path.exists(page2_path))

        # Check content in page 1 includes resolved image link
        with open(page1_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("my-thread/image1.jpg", content)

        # Check image exists in asset folder
        saved_img = os.path.join(self.output_dir, "my-thread", "image1.jpg")
        self.assertTrue(os.path.exists(saved_img))

    @patch('requests.Session.get')
    def test_custom_next_selector(self, mock_get):
        # HTML with standard pagination and custom page-next button
        html_content = """
        <html>
            <body>
                <div class="story-content"><p>Some text</p></div>
                <button class="custom-next" href="/thread?page=99">Next Page</button>
            </body>
        </html>
        """
        response1 = MagicMock()
        response1.status_code = 200
        response1.text = html_content

        # Mock page 99 response to stop
        response2 = MagicMock()
        response2.status_code = 200
        response2.text = "<html><body><div class='story-content'><p>End</p></div></body></html>"

        mock_get.side_effect = [response1, response2]

        # Use button.custom-next selector
        archiver = ForumArchiver(output_dir=self.output_dir, delay=0.0, next_selector="button.custom-next")
        archiver.scrape_thread("https://example.com/my-thread.html", "div.story-content")

        page2_path = os.path.join(self.output_dir, "my-thread-Page-2.md")
        self.assertTrue(os.path.exists(page2_path))

        with open(page2_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Source URL: https://example.com/thread?page=99", content)

if __name__ == "__main__":
    unittest.main()
