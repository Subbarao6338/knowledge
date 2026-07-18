# Notion Backup Structure & Automation Ecosystem

Welcome to the ultimate repository and documentation ecosystem for managing, converting, organizing, and importing Markdown vaults into Notion with pixel-perfect compatibility.

This project outlines how Notion's hierarchical page and database backup model functions, and provides robust, enterprise-ready Python automation utilities to prepare local assets, convert raw document formats, crawl online forums, and validate structures for the Notion Importer.

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

## 3. How to Use These Tools

The repository is organized with all executable Python automation utilities structured inside the dedicated `scripts/` folder, and all backup materials and cheatsheets merged into the single unified `Docs/` directory:

```text
.
├── Docs/                 # Sample documents, databases and developer cheatsheets in Notion backup layout
│   ├── Cheatsheets.md    # Master parent page for all cheatsheets
│   ├── Cheatsheets/      # Companion directory with all 39 developer cheatsheets
│   ├── My notes 21cb6c26d9ba81648e18c1761db2dcca.csv
│   ├── My notes 21cb6c26d9ba81648e18c1761db2dcca/
│   ├── People d3db6c26d9ba82dfb0d8014512d331ec.csv
│   └── People d3db6c26d9ba82dfb0d8014512d331ec/
├── scripts/              # All production automation Python utilities
│   ├── archive_forum.py
│   ├── convert_to_notion_vault.py
│   ├── organize_local_vault.py
│   └── prepare_github_vault.py
├── Files to md.md        # Documentation for files-to-markdown pipeline
├── Notion_scripts.md     # Documentation for local and repository organizers
├── Notion_structure.md   # Notion Backup structure guide
├── README.md             # Repository master index
└── Site to md.md         # Documentation for site-archiver pipeline
```

### Quick Start: Organizing Loose Assets
1. Run `python scripts/organize_local_vault.py` in your unorganized notes folder.
2. Compress the folder as a `.zip` file, and upload it directly to Notion using **Import -> Markdown & CSV**.

### Quick Start: Large Document Ingestion with OCR
1. Ensure system-level `tesseract-ocr` is installed:
   * **macOS:** `brew install tesseract`
   * **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
2. Install Python requirements: `pip install pymupdf python-docx beautifulsoup4 pytesseract pillow`
3. Create a `./my_raw_documents` folder next to the scripts folder and place your files (PDF, DOCX, Images, etc.) inside.
4. Run `python scripts/convert_to_notion_vault.py` and import the generated zip file.

---

## 4. Key Best Practices for Notion Backups

1. **Avoid Nested Backlinks (`../../`):** Notion's importer fails to resolve paths that escape parent directories. Always reference assets residing in directories adjacent to or below the current Markdown file.
2. **Double-Check Hex Hash Collision:** Never alter the 32-character trailing strings of files if they originate from an export, as those hashes are what Notion uses to rebuild relational links on re-import.
3. **Percent-Encode Spaced Paths:** Keep folder and file names on disk with standard literal spaces, but ensure Markdown links percent-encode spaces as `%20` for smooth parsing.
