import os
import unittest
import tempfile
import shutil
import docx
from unittest.mock import patch, MagicMock
from scripts.convert_to_notion_vault import docx_table_to_markdown, process_docx, process_html_mhtml, process_image, process_pdf, run_vault_generator

class TestConvertToNotionVault(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.output_dir)

    def test_docx_table_to_markdown(self):
        # Create a document and a table inside it
        doc = docx.Document()
        table = doc.add_table(rows=2, cols=2)
        table.cell(0, 0).text = "Col A"
        table.cell(0, 1).text = "Col B"
        table.cell(1, 0).text = "Val 1"
        table.cell(1, 1).text = "Val 2"

        md_output = docx_table_to_markdown(table)
        self.assertIn("| Col A | Col B |", md_output)
        self.assertIn("| --- | --- |", md_output)
        self.assertIn("| Val 1 | Val 2 |", md_output)

    def test_process_docx_generates_markdown_and_sub_pages(self):
        # Generate a docx with paragraphs and tables to verify full integration
        doc_path = os.path.join(self.test_dir, "MyDocument.docx")
        doc = docx.Document()
        doc.add_paragraph("Paragraph 1")

        table = doc.add_table(rows=2, cols=2)
        table.cell(0, 0).text = "H1"
        table.cell(0, 1).text = "H2"
        table.cell(1, 0).text = "D1"
        table.cell(1, 1).text = "D2"

        doc.add_paragraph("Paragraph 2")
        doc.save(doc_path)

        # Process the DOCX file
        process_docx(doc_path, self.output_dir)

        # Check index markdown exists
        index_md = os.path.join(self.output_dir, "MyDocument.md")
        self.assertTrue(os.path.exists(index_md))

        # Check sub-page exists
        sub_page_path = os.path.join(self.output_dir, "MyDocument", "MyDocument-Part-1.md")
        self.assertTrue(os.path.exists(sub_page_path))

        # Check sub-page content includes paragraphs and the table in order
        with open(sub_page_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Paragraph 1", content)
            self.assertIn("| H1 | H2 |", content)
            self.assertIn("| --- | --- |", content)
            self.assertIn("| D1 | D2 |", content)
            self.assertIn("Paragraph 2", content)

    def test_process_html_mhtml(self):
        html_path = os.path.join(self.test_dir, "test.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write("<html><body><h1>Title</h1><p>Hello HTML world</p></body></html>")

        process_html_mhtml(html_path, self.output_dir)

        index_md = os.path.join(self.output_dir, "test.md")
        self.assertTrue(os.path.exists(index_md))
        sub_page = os.path.join(self.output_dir, "test", "test-Part-1.md")
        self.assertTrue(os.path.exists(sub_page))

        with open(sub_page, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Hello HTML world", content)

    @patch("scripts.convert_to_notion_vault.perform_ocr")
    def test_process_image(self, mock_ocr):
        mock_ocr.return_value = "Extracted OCR text from image"
        img_path = os.path.join(self.test_dir, "sample.png")
        from PIL import Image
        img = Image.new("RGB", (100, 100), color="red")
        img.save(img_path)

        process_image(img_path, self.output_dir)

        index_md = os.path.join(self.output_dir, "sample.md")
        self.assertTrue(os.path.exists(index_md))

        saved_img = os.path.join(self.output_dir, "sample", "sample.png")
        self.assertTrue(os.path.exists(saved_img))

        with open(index_md, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Extracted OCR text from image", content)
            self.assertIn("![sample](sample/sample.png)", content)

    @patch("pymupdf.open")
    def test_process_pdf_mocked(self, mock_fitz_open):
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Sample text from PDF page"
        mock_page.get_images.return_value = []
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz_open.return_value = mock_doc

        pdf_path = os.path.join(self.test_dir, "sample_pdf.pdf")
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.4 dummy content")

        process_pdf(pdf_path, self.output_dir)

        index_md = os.path.join(self.output_dir, "sample_pdf.md")
        self.assertTrue(os.path.exists(index_md))
        sub_page = os.path.join(self.output_dir, "sample_pdf", "sample_pdf-Part-1.md")
        self.assertTrue(os.path.exists(sub_page))

        mock_doc.close.assert_called_once()

    def test_run_vault_generator(self):
        html_path = os.path.join(self.test_dir, "page.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write("<html><body><p>Vault Gen Test</p></body></html>")

        run_vault_generator(self.test_dir, self.output_dir)
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "page.md")))

if __name__ == "__main__":
    unittest.main()
