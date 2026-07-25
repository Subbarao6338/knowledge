# PDF Cheatsheet (Adobe Acrobat + Command-Line Tools)

## Adobe Acrobat / Reader — Keyboard Shortcuts

```text
Ctrl+O                   Open a file
Ctrl+S / Ctrl+Shift+S       Save / Save As
Ctrl+P                          Print
Ctrl+F                              Find
Ctrl+G / Shift+Ctrl+G                   Find next / previous match
Ctrl+Shift+H                                Read Out Loud (toggle)

Ctrl+L                    Toggle full-screen view
Ctrl+0 (zero)                 Fit page in window
Ctrl+1                            Actual size (100%)
Ctrl+2                               Fit width
Ctrl++ / Ctrl+-                          Zoom in / out
Ctrl+M                                      Zoom to specific percentage
Page Up / Page Down                            Previous / next page
Ctrl+Shift+N                                       Go to page (page number dialog)
Home / End                                             First / last page
Ctrl+Shift+D                                              Rotate view (varies by version)

Ctrl+K                   Preferences dialog
Ctrl+D                       Document Properties
```

## Acrobat — Editing & Organizing Pages

```text
Tools > Organize Pages
  Insert (from file, blank page, scanner)
  Delete pages
  Extract pages (pull selected pages into a new document)
  Split (divide into multiple files by page count, size, or bookmark)
  Rotate
  Replace pages (swap content while keeping the rest of the doc/bookmarks intact)
  Drag-and-drop thumbnails to reorder

Tools > Combine Files             merge multiple PDFs/documents into one, with reordering before merge
```

## Acrobat — Editing Content

```text
Tools > Edit PDF
  Click text to edit in place (works best on text-based, not scanned, PDFs)
  Add/edit images, shapes, links
  Add Text / Add Image toolbar buttons

Tools > Redact
  Mark for Redaction (select text/areas)
  Apply Redactions (permanently removes underlying content, not just visual black-out)
  Sanitize Document — also strips hidden metadata, embedded content, and attachments

Edit > Find and Replace (limited support depending on version — mainly for simple text edits)
```

## Acrobat — Forms

```text
Tools > Prepare Form
  Auto-detects form fields from a scanned/flat document, or add manually:
    Text Field, Checkbox, Radio Button, Dropdown, List Box, Button, Digital Signature field, Date Field
  Field Properties > set name, tooltip, validation, calculation, format
  Distribute — send the form for collection, track responses

Forms > Export/Import form data (.fdf, .xfdf, .csv)
```

## Acrobat — Signatures & Security

```text
Tools > Fill & Sign — add a simple signature/initials + basic text/checkmarks (no digital certificate)
Tools > Certificates > Digitally Sign — cryptographically signed, tamper-evident signature
Tools > Protect > Encrypt with Password — set an Open password and/or a Permissions password
Tools > Protect > Restrict Editing — control printing, copying, editing permissions without necessarily requiring a password to open
Tools > Protect > Redact (see above)

File > Properties > Security tab — view current encryption/permission settings
```

## Acrobat — Comments & Review

```text
Tools > Comment
  Sticky Note, Highlight, Underline, Strikethrough, Text Box, Drawing markup, Stamp
Ctrl+6 (varies)          Toggle Comments pane
Right-click a comment > Reply / Set Status / Mark as Checked

File > Share for Review / Send for Comments        collect feedback from multiple reviewers, consolidated into one file
```

## Acrobat — OCR (Scanned Documents)

```text
Tools > Scan & OCR > Recognize Text
  Converts a scanned/image-based PDF into a searchable, selectable-text PDF
  Choose language and output style (Searchable Image vs Editable Text)

Tools > Scan & OCR > Enhance Scanned Photo / Compare Scanned Documents
```

## Acrobat — Accessibility

```text
Tools > Accessibility > Accessibility Checker         scans for tagging, alt-text, reading order, contrast issues
Tools > Accessibility > Autotag Document                  auto-generate structural tags for screen readers
Tools > Accessibility > Set Alternate Text                   add descriptions to images for screen readers
Tools > Accessibility > Reading Order                            manually fix reading order/tag structure
```

## Acrobat — Optimization & Export

```text
File > Save As Other > Reduced Size PDF          compress/downsample for smaller file size
Tools > Optimize PDF                                  granular control: downsample images, remove unused objects/fonts, discard embedded thumbnails
File > Export To > Word / Excel / PowerPoint / Image / HTML       convert PDF content to editable formats
File > Print > "Microsoft Print to PDF" or "Save as PDF" (from any app)   quick PDF creation
```

---

## Command-Line PDF Tools

### `pdftk` (PDF Toolkit)

```bash
pdftk input.pdf cat 1-5 output extracted.pdf          # extract pages 1-5
pdftk input.pdf cat 1-5 10-15 output out.pdf              # extract multiple ranges
pdftk A.pdf B.pdf cat output merged.pdf                       # merge/concatenate files
pdftk input.pdf cat 1-endeast output rotated.pdf                 # rotate all pages 90° clockwise (east)

pdftk input.pdf burst                          # split into individual single-page PDFs (pg_0001.pdf, ...)
pdftk input.pdf dump_data output info.txt         # dump metadata/bookmarks
pdftk input.pdf update_info info.txt output out.pdf   # apply edited metadata back

pdftk input.pdf output encrypted.pdf owner_pw OWNERPASS user_pw USERPASS
pdftk encrypted.pdf input_pw USERPASS output decrypted.pdf

pdftk form.pdf fill_form data.fdf output filled.pdf      # fill a form from an FDF/XFDF data file
pdftk form.pdf generate_fdf output data.fdf                  # extract a blank FDF template from a form
```

### `qpdf`

```bash
qpdf input.pdf output.pdf --decrypt                # remove password/encryption (if password known)
qpdf --encrypt userpass ownerpass 256 -- input.pdf output.pdf     # add 256-bit AES encryption
qpdf input.pdf --pages input.pdf 1-5 -- output.pdf         # extract pages
qpdf --split-pages input.pdf page-%d.pdf                       # split into individual pages
qpdf in1.pdf --pages in1.pdf in2.pdf -- merged.pdf                # merge

qpdf --linearize input.pdf output.pdf              # optimize for fast web viewing (progressive loading)
qpdf --check input.pdf                                # validate structural integrity
```

### `poppler-utils` (pdftotext, pdftoppm, pdfinfo, pdfimages)

```bash
pdftotext input.pdf output.txt              # extract text
pdftotext -layout input.pdf output.txt          # preserve layout/columns better
pdftotext -f 1 -l 5 input.pdf output.txt            # only pages 1-5

pdftoppm -png input.pdf page                # render each page as a PNG (page-1.png, page-2.png, ...)
pdftoppm -jpeg -r 300 input.pdf page             # 300 DPI JPEG rendering

pdfinfo input.pdf                # metadata: page count, size, PDF version, encryption status
pdfimages -all input.pdf img_prefix       # extract embedded images
pdffonts input.pdf                   # list fonts used in the document
pdfseparate input.pdf page-%d.pdf       # split into individual pages
pdfunite in1.pdf in2.pdf merged.pdf        # merge/concatenate
```

### Ghostscript

```bash
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -o output.pdf input.pdf
# -dPDFSETTINGS options: /screen (smallest, 72dpi), /ebook (150dpi), /printer (300dpi), /prepress (300dpi + color preservation)

gs -sDEVICE=pdfwrite -dFirstPage=1 -dLastPage=5 -o extracted.pdf input.pdf     # extract pages
gs -q -dNODISPLAY -c "(input.pdf) (r) file runpdfbegin pdfpagecount = quit"       # get page count
gs -sDEVICE=png16m -r300 -o page-%d.png input.pdf                                    # render pages as PNG
```

### ImageMagick (image ↔ PDF conversion)

```bash
convert input.pdf output.png            # PDF pages to images
convert -density 300 input.pdf output.png   # higher-resolution rendering
convert image1.png image2.png output.pdf       # combine images into a PDF
convert input.pdf[0] first_page.png                # just the first page (0-indexed)
```

### LibreOffice (headless conversion — very common in automated pipelines)

```bash
soffice --headless --convert-to pdf document.docx
soffice --headless --convert-to pdf --outdir /output /input/*.docx
soffice --headless --convert-to txt input.pdf
```

## Python: Working with PDFs

```python
# pypdf (modern, actively maintained; successor to PyPDF2)
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
print(len(reader.pages))
text = reader.pages[0].extract_text()
metadata = reader.metadata

writer = PdfWriter()
writer.add_page(reader.pages[0])
with open("output.pdf", "wb") as f:
    writer.write(f)

# Merge
writer = PdfWriter()
for path in ["a.pdf", "b.pdf"]:
    writer.append(path)
writer.write("merged.pdf")

# Split
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    writer.write(f"page_{i+1}.pdf")

# Rotate
page = reader.pages[0]
page.rotate(90)

# Encrypt / Decrypt
writer.encrypt(user_password="secret", owner_password="ownersecret")
reader = PdfReader("encrypted.pdf")
reader.decrypt("secret")

# Merge pages (watermarking / overlay)
base = PdfReader("document.pdf")
overlay = PdfReader("watermark.pdf")
page = base.pages[0]
page.merge_page(overlay.pages[0])
```

```python
# pdfplumber — best for structured text/table extraction
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    tables = page.extract_tables()
    for row in tables[0]:
        print(row)
```

```python
# reportlab — generate PDFs from scratch
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf")
c.drawString(100, 750, "Hello, World!")
c.save()
```

```python
# fitz / PyMuPDF — fast rendering, text extraction, image handling
import fitz

doc = fitz.open("input.pdf")
page = doc[0]
text = page.get_text()
pix = page.get_pixmap(dpi=300)
pix.save("page1.png")
doc.save("output.pdf")
```

## OCR from the Command Line

```bash
# Tesseract OCR
tesseract input.png output          # -> output.txt
tesseract input.png output pdf         # -> searchable output.pdf

# OCRmyPDF — adds an invisible text layer to a scanned PDF (built on Tesseract)
pip install ocrmypdf
ocrmypdf input.pdf output.pdf
ocrmypdf --deskew --clean input.pdf output.pdf
ocrmypdf --force-ocr input.pdf output.pdf      # re-OCR even if some text layer already exists
```

## Common Automation Patterns

```bash
# Batch convert a folder of Word docs to PDF
for f in *.docx; do soffice --headless --convert-to pdf "$f"; done

# Merge all PDFs in a directory (alphabetical order)
pdfunite *.pdf merged.pdf

# Compress a large PDF for email
gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -o compressed.pdf original.pdf

# Extract all text from a folder of PDFs into individual .txt files
for f in *.pdf; do pdftotext "$f" "${f%.pdf}.txt"; done

# Add a password to every PDF in a folder
for f in *.pdf; do qpdf --encrypt secret secret 256 -- "$f" "protected_$f"; done
```

## Common Gotchas

- Text extraction fails silently (returns empty/garbled text) on scanned/image-only PDFs — run OCR first (Tesseract/OCRmyPDF/Acrobat's Recognize Text) before attempting text extraction or search.
- "Deleting" pages/content in some tools only hides it visually — sensitive data can remain recoverable in the underlying PDF structure; use Acrobat's Redact + Sanitize (or a tool explicitly designed to strip data) when removing sensitive content, not simple deletion or a black box drawn on top.
- PDF encryption has two separate passwords — a **user password** (required to open) and an **owner password** (controls permissions like printing/copying) — a PDF can be "protected" against editing while still being fully openable and readable without any password.
- Different PDF/A conformance levels (1a, 2b, 3u, etc.) matter for long-term archival compliance — a plain PDF export is not automatically PDF/A compliant; use explicit PDF/A export options when archival compliance is required.
- Compressing with aggressive Ghostscript settings (`/screen`) can visibly degrade image quality and downsample embedded fonts — always preview the output before using a lossy compression setting for anything that will be printed or needs to remain crisp.
- Merging PDFs with different page sizes/orientations can produce unexpected results in some tools (stretching, cropping) — check output carefully when combining documents authored in different applications.
