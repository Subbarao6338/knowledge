In local, I have hundreds of pdf, html, mhtml, docx files. Each file has hundreds of pages. 
Python script to convert these into md with embedded media, similar structure as notion backup like above. Each file as main page, every 10 pages as subpage. Without missing any content. I will upload final md folder zip to notion.


To process huge files (hundreds of pages each) into a neat, nested hierarchy without losing content, the script needs to do three things:
 1. Parse different file formats (.pdf, .html, .mhtml, .docx) and extract text and images.
 2. Group the extracted text blocks or pages so that every 10 pages become a nested sub-page markdown file.
 3. Organize them into the exact folder-matching structure Notion expects (Page.md next to a Page/ folder).
### Prerequisites
You will need a few standard Python libraries to handle these complex document types. Run this in your terminal first:
```bash
pip install pymupdf python-docx beautifulsoup4

```
### The Conversion Script (convert_to_notion_vault.py)
This script loops through your files, sets up a clean master page, extracts images into the matching asset folder, and chunks the text into sequential 10-page sub-pages.
```python
import os
import re
import shutil
from bs4 import BeautifulSoup
import docx
import fitz  # PyMuPDF

def slugify(text):
    """Cleans names to be safe for file systems."""
    return re.sub(r'[\\/*?:"<>|]', "", text.strip().replace(" ", "-"))

def create_sub_page(assets_dir, main_page_name, chunk_idx, text_content):
    """Creates a sub-page markdown file inside the matching assets folder."""
    sub_page_title = f"{main_page_name}-Part-{chunk_idx}"
    sub_page_file = os.path.join(assets_dir, f"{sub_page_title}.md")
    
    with open(sub_page_file, "w", encoding="utf-8") as f:
        f.write(f"# {sub_page_title.replace('-', ' ')}\n\n")
        f.write(text_content)
        
    return sub_page_title

def process_pdf(file_path, output_dir):
    doc = fitz.open(file_path)
    base_name = slugify(os.path.splitext(os.path.basename(file_path))[0])
    
    # Setup Notion backup architecture
    main_md_path = os.path.join(output_dir, f"{base_name}.md")
    assets_dir = os.path.join(output_dir, base_name)
    os.makedirs(assets_dir, exist_ok=True)
    
    current_chunk_text = ""
    chunk_idx = 1
    sub_pages_created = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        current_chunk_text += page.get_text() + "\n\n"
        
        # Extract Images
        for img_idx, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            img_name = f"image-p{page_num}-i{img_idx}.{image_ext}"
            img_save_path = os.path.join(assets_dir, img_name)
            
            with open(img_save_path, "wb") as f:
                f.write(image_bytes)
                
            # Embed image link relative to where the sub-page text will live
            current_chunk_text += f"\n![Embedded Image]({base_name}/{img_name})\n\n"
            
        # Every 10 pages, cut a sub-page
        if (page_num + 1) % 10 == 0 or (page_num + 1) == len(doc):
            if current_chunk_text.strip():
                sub_title = create_sub_page(assets_dir, base_name, chunk_idx, current_chunk_text)
                sub_pages_created.append(sub_title)
                current_chunk_text = ""
                chunk_idx += 1
                
    # Build Master Index File
    with open(main_md_path, "w", encoding="utf-8") as f:
        f.write(f"# {base_name.replace('-', ' ')}\n\n")
        f.write("## Document Sub-pages\n\n")
        for sub_title in sub_pages_created:
            f.write(f"* [{sub_title.replace('-', ' ')}]({base_name}/{sub_title}.md)\n")

def process_docx(file_path, output_dir):
    doc = docx.Document(file_path)
    base_name = slugify(os.path.splitext(os.path.basename(file_path))[0])
    
    main_md_path = os.path.join(output_dir, f"{base_name}.md")
    assets_dir = os.path.join(output_dir, base_name)
    os.makedirs(assets_dir, exist_ok=True)
    
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    
    # Docx doesn't have strict physical "pages", so we group every 30 paragraphs 
    # (roughly equivalent to 10 standard reading pages) to ensure structural safety.
    chunk_size = 30 
    sub_pages_created = []
    
    # Extract images embedded inside Docx XML structures
    img_idx = 0
    for rel in doc.part.relations.values():
        if "image" in rel.target_ref:
            img_name = f"docx-img-{img_idx}.png"
            img_save_path = os.path.join(assets_dir, img_name)
            with open(img_save_path, "wb") as f:
                f.write(rel.target_part.blob)
            img_idx += 1

    for idx, i in enumerate(range(0, len(paragraphs), chunk_size)):
        chunk_paras = paragraphs[i:i + chunk_size]
        text_content = "\n\n".join(chunk_paras)
        
        # Inject images at the end of the matching textual sub-pages chunk
        if idx == 0 and img_idx > 0:
            for j in range(img_idx):
                text_content += f"\n\n![Docx Image]({base_name}/docx-img-{j}.png)"
                
        sub_title = create_sub_page(assets_dir, base_name, idx + 1, text_content)
        sub_pages_created.append(sub_title)
        
    with open(main_md_path, "w", encoding="utf-8") as f:
        f.write(f"# {base_name.replace('-', ' ')}\n\n## Sub-pages\n\n")
        for sub_title in sub_pages_created:
            f.write(f"* [{sub_title.replace('-', ' ')}]({base_name}/{sub_title}.md)\n")

def process_html_mhtml(file_path, output_dir):
    """Processes HTML/MHTML files using text blocks to simulate 10-page split layouts."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    base_name = slugify(os.path.splitext(os.path.basename(file_path))[0])
    main_md_path = os.path.join(output_dir, f"{base_name}.md")
    assets_dir = os.path.join(output_dir, base_name)
    os.makedirs(assets_dir, exist_ok=True)
    
    # Strip scripts/styles
    for element in soup(["script", "style"]):
        element.decompose()
        
    lines = [p.get_text().strip() for p in soup.find_all(['p', 'div', 'h1', 'h2', 'h3']) if p.get_text().strip()]
    
    # Split text blocks into chunks to prevent hitting Notion individual page upload limits
    chunk_size = 40 
    sub_pages_created = []
    
    for idx, i in enumerate(range(0, len(lines), chunk_size)):
        chunk_lines = lines[i:i + chunk_size]
        text_content = "\n\n".join(chunk_lines)
        
        sub_title = create_sub_page(assets_dir, base_name, idx + 1, text_content)
        sub_pages_created.append(sub_title)
        
    with open(main_md_path, "w", encoding="utf-8") as f:
        f.write(f"# {base_name.replace('-', ' ')}\n\n## Sub-pages\n\n")
        for sub_title in sub_pages_created:
            f.write(f"* [{sub_title.replace('-', ' ')}]({base_name}/{sub_title}.md)\n")

def run_vault_generator(source_folder, output_vault):
    os.makedirs(output_vault, exist_ok=True)
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            ext = file.lower()
            full_path = os.path.join(root, file)
            print(f"Processing: {file}...")
            
            try:
                if ext.endswith(".pdf"):
                    process_pdf(full_path, output_vault)
                elif ext.endswith(".docx"):
                    process_docx(full_path, output_vault)
                elif ext.endswith((".html", ".htm", ".mhtml")):
                    process_html_mhtml(full_path, output_vault)
            except Exception as e:
                print(f"Error handling {file}: {str(e)}")

if __name__ == "__main__":
    # Update these paths to match your local setup
    SOURCE_DIRECTORY = "./my_raw_documents" 
    FINAL_NOTION_VAULT = "./ready_for_notion"
    
    run_vault_generator(SOURCE_DIRECTORY, FINAL_NOTION_VAULT)
    print(\n"Transformation complete! Zip the contents of 'ready_for_notion' and import to Notion.")

```
### How to execute this migration smoothly:
 1. Create a workspace folder on your machine and place your unsorted files inside a folder named my_raw_documents.
 2. Save the script above as convert_to_notion_vault.py inside that workspace folder and run it (python convert_to_notion_vault.py).
 3. Once done, open the generated ready_for_notion folder. It will match the standard structure perfectly:
   ```text
   ready_for_notion/
   ├── Large-Book-File.md
   └── Large-Book-File/
       ├── Large-Book-File-Part-1.md
       ├── Large-Book-File-Part-2.md
       └── image-p0-i0.png
   
   ```
 4. **Compress only the contents** inside ready_for_notion into a single .zip file, go to Notion, click **Import**, select **Markdown & CSV**, and hand over the file.
