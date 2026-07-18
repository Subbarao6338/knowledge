# Notion Backup Structure & Automation Ecosystem

Welcome to the ultimate repository and documentation ecosystem for managing, converting, organizing, and importing Markdown vaults into Notion with pixel-perfect compatibility.

This project outlines how Notion's hierarchical page and database backup model functions, and provides robust, enterprise-ready Python automation utilities to prepare local assets, convert raw document formats, crawl online forums, and validate structures for the Notion Importer.

All sample notes, databases, and developers' cheatsheets have been fully organized and unified under a single backup structure under the `Docs/` directory, while all execution utilities have been consolidated inside the `scripts/` directory.

---

## 1. System Landscape & Repository Directory

The diagram below outlines the entire system landscape of this repository, showing how each script, document, input source, and output directory relates to the Notion Cloud workspace.

```mermaid
graph TD
    subgraph Documentation Hub
        R[README.md] -->|Master Index| NS[Notion_structure.md]
        R -->|Local Scripts Guide| SC[Notion_scripts.md]
        R -->|File Conversion Guide| FM[Files to md.md]
        R -->|Forum Scraping Guide| SM[Site to md.md]
    end

    subgraph Inputs / Sources
        RAW[Raw Documents: PDF, DOCX, HTML, MHTML, Standalone Images] -.->|Processed by| CV_S[convert_to_notion_vault.py]
        WEB[Web/Forum Thread Content] -.->|Scraped by| FA_S[archive_forum.py]
        LOOSE[Loose files: img, pdf, md] -.->|Sorted by| LV_S[organize_local_vault.py]
    end

    subgraph Automation & Pipelines (scripts/ folder)
        CV_S -->|Ingests & chunks with OCR| OUT[ready_for_notion/ folder]
        FA_S -->|Archives page-by-page| VAULT[forum_vault/ folder]
        LV_S -->|Groups assets into parent dirs| LOCAL_V[My-Local-Vault/]
        GV_S[prepare_github_vault.py] -->|Recursive CI-CD validator| LOCAL_V
    end

    subgraph Notion Workspace Cloud
        OUT -->|Compress to ZIP & Import| NOTION[Notion Cloud Importer]
        VAULT -->|Compress to ZIP & Import| NOTION
        LOCAL_V -->|Compress to ZIP & Import| NOTION
    end

    classDef doc fill:#1f6feb,stroke:#388bfd,color:#fff;
    classDef script fill:#238636,stroke:#30a14e,color:#fff;
    classDef output fill:#d29922,stroke:#f0883e,color:#fff;
    classDef notion fill:#764abc,stroke:#9065db,color:#fff;

    class R,NS,SC,FM,SM doc;
    class CV_S,FA_S,LV_S,GV_S script;
    class OUT,VAULT,LOCAL_V output;
    class NOTION notion;
```

---

## 2. Directory Index & Document Guides

### 📂 [Notion_structure.md](Notion_structure.md)
* **Description:** An in-depth analysis of how Notion handles exports and imports.
* **Topics Covered:**
  * Notion's 32-character hexadecimal page ID scheme.
  * Space percent-encoding (`%20`) and link matching rules.
  * Structural page-to-folder mapping and database schema CSV outputs.
* **Mermaid Charts:** Hierarchy Tree diagram, Database Schema class map, and Notion Importer Lifecycle pipeline.

### 📂 [Notion_scripts.md](Notion_scripts.md)
* **Description:** Complete guide and source code for workspace-management scripts.
* **Scripts Contained in `scripts/`:**
  1. `organize_local_vault.py`: Automatically groups loose local assets sitting next to parent markdown files into matching folders and edits links accordingly.
  2. `prepare_github_vault.py`: Recursively crawls directory trees, validates reference formats, cleans up relative links, and fixes percent-encoding.
* **Mermaid Charts:** Step-by-step logic flowcharts for both local sorting and remote CI-CD checking processes.

### 📂 [Files to md.md](Files to md.md)
* **Description:** Multi-format local document ingestion pipeline with integrated OCR.
* **Script Contained in `scripts/`:**
  * `convert_to_notion_vault.py`: Automatically parses `.pdf`, `.docx`, `.html`, `.mhtml`, and standalone images, extracts embedded raw images, performs optical character recognition (OCR) on images and scanned pages, chunks long documents into sequential sub-pages, and outputs a nested master page with exact relative pointers.
* **Mermaid Charts:** Document Ingestion, Image Extraction, OCR processing, and Paragraph Chunking sequence flow.

### 📂 [Site to md.md](Site to md.md)
* **Description:** Headless forum thread downloader and archiver.
* **Script Contained in `scripts/`:**
  * `archive_forum.py`: Connects to online forums, handles session cookie validation, automatically traverses pagination buttons, extracts core content containers, downloads all referenced images, and outputs beautifully formatted sequential markdown files.
* **Mermaid Charts:** Session Scraper and Crawler pagination-loop logic.

---

## 3. Unified Repository & Notion Backup Layout

All backups, sample notes, databases, and developer cheatsheets are organized under a single unified directory `Docs/` matching Notion's standard export/import schema, while automation utilities are consolidated in `scripts/`:

```text
.
├── Docs/                 # Sample documents, databases and developer cheatsheets in Notion backup layout
│   ├── Cheatsheets.md    # Master parent index page for all developer cheatsheets
│   ├── Cheatsheets/      # Companion folder with all 39 developer cheatsheet sub-pages
│   ├── My notes 21cb6c26d9ba81648e18c1761db2dcca.csv
│   ├── My notes 21cb6c26d9ba81648e18c1761db2dcca/  # Database item sub-pages & asset folders
│   │   ├── Clean 2fcb6c26d9ba807a83d6d72a3ef6a22c.md
│   │   ├── Interview 2f9b6c26d9ba80c5a30fc0f3570e67ab.md
│   │   ├── To do 2e9b6c26d9ba80f780d7e00463b23078.md
│   │   ├── To do 2e9b6c26d9ba80f780d7e00463b23078/ # Sub-page asset directory
│   │   │   ├── 1001314913.jpg
│   │   │   ├── 1001314914.jpg
│   │   │   └── Addressing 2e9b6c26d9ba80e6bf63d8e1a49da87b.md
│   │   ├── To-Do List 13cb6c26d9ba808ca4f9d290392ae099.md
│   │   └── Untitled 35eb6c26d9ba80e59335c26c5f2b6de9.md
│   ├── People d3db6c26d9ba82dfb0d8014512d331ec.csv
│   ├── People d3db6c26d9ba82dfb0d8014512d331ec/     # People database directory
│   │   └── Subbarao 3b5b6c26d9ba82a398b201af94cf7acc.md
│   ├── Knowledge 21cb6c26d9ba808da8d4f72eb2193ca2.md
│   ├── Untitled 58c8-1d4a.md
│   └── test.txt
├── scripts/              # Consolidated executable automation Python utilities
│   ├── archive_forum.py             # Scrapes paginated forum threads with rate limits and custom args
│   ├── convert_to_notion_vault.py   # Multi-format document parser with full PyTesseract OCR integration
│   ├── organize_local_vault.py      # Cleans, re-points, and matches local unorganized asset links
│   └── prepare_github_vault.py      # Recursive pre-flight link and structure compliance checker
├── Files to md.md        # File parser, chunker, and OCR guide
├── Notion_scripts.md     # Document sorting and CI-CD checker guide
├── Notion_structure.md   # Underlying Notion backup specification guide
├── README.md             # Master repository index
└── Site to md.md         # Forum thread content downloader guide
```

---

## 4. How to Use These Tools

### Quick Start: Organizing Loose Assets
1. Execute the local vault organizer script to clean up unorganized parent-child structures and relative links:
   ```bash
   python scripts/organize_local_vault.py
   ```
2. Compress the folder as a `.zip` archive and upload it directly to Notion via **Import -> Markdown & CSV**.

### Quick Start: Large Document Ingestion with OCR
The file-to-markdown script can process standalone image files (`.png`, `.jpg`, `.jpeg`, etc.), scanned PDF pages, and embedded DOCX/PDF images using standard Optical Character Recognition.

1. Ensure system-level `tesseract-ocr` is installed:
   * **macOS:** `brew install tesseract`
   * **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
2. Install Python package dependencies:
   ```bash
   pip install pymupdf python-docx beautifulsoup4 pytesseract pillow
   ```
3. Create a `./my_raw_documents` folder next to the scripts folder and place your raw documents (scanned files or images) inside.
4. Execute the converter:
   ```bash
   python scripts/convert_to_notion_vault.py
   ```
5. Compress the contents of `ready_for_notion/` as a `.zip` file and import to Notion.

### Quick Start: Thread Site Archiver
Scrape any thread-style online conversation page-by-page into sequentially organized local files using the command-line interface:
```bash
python scripts/archive_forum.py --url "https://example.com/thread-link" --selector "div.post-content" --output "./forum_vault" --delay 1.5
```

---

## 5. Key Best Practices for Notion Backups

1. **Avoid Nested Backlinks (`../../`):** Notion's importer fails to resolve paths that escape parent directories. Always reference assets residing in directories adjacent to or below the current Markdown file.
2. **Double-Check Hex Hash Collision:** Never alter the 32-character trailing strings of files if they originate from an export, as those hashes are what Notion uses to rebuild relational links on re-import.
3. **Percent-Encode Spaced Paths:** Keep folder and file names on disk with standard literal spaces, but ensure Markdown links percent-encode spaces as `%20` for smooth parsing.
