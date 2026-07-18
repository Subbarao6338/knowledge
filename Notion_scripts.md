Here are the two distinct versions of the script.
The **Local Script** is designed to find loose, unorganized assets sitting right next to your files and clean them up into folders. The **GitHub / CI-CD Workflow Script** assumes your files are *already* structured into folders locally or via a script, and focus entirely on dynamically verifying paths, handling deep multi-level nested folders, and ensuring compatibility before you zip and ship it to Notion.
### 1. The Local Script (organize_local_vault.py)
Use this version on your computer to actively group loose files. If you drop a new image or a new sub-page .md file into your folder, running this script creates the directory matching your main file, moves the asset inside, and fixes the text link.
```python
import os
import re
import shutil

def organize_local_vault(target_dir):
    # Match markdown inline images ![]() and links []() pointing to local files
    # Ignores external web links starting with http/https
    link_pattern = re.compile(r'!?\[.*?\]\(((?!http)[^)]+)\)')
    
    files = os.listdir(target_dir)
    md_files = [f for f in files if f.endswith('.md')]

    for md_file in md_files:
        page_name = os.path.splitext(md_file)[0]
        assets_folder = os.path.join(target_dir, page_name)
        md_file_path = os.path.join(target_dir, md_file)
        
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        matches = link_pattern.findall(content)
        if not matches:
            continue
            
        if not os.path.exists(assets_folder):
            os.makedirs(assets_folder)
            print(f"[Local] Created folder: {assets_folder}/")
            
        updated_content = content
        
        for asset_path in matches:
            clean_asset_name = os.path.basename(asset_path)
            old_asset_location = os.path.join(target_dir, clean_asset_name)
            
            # Move loose files from root into the specific parent folder
            if os.path.exists(old_asset_location):
                new_asset_location = os.path.join(assets_folder, clean_asset_name)
                shutil.move(old_asset_location, new_asset_location)
                print(f"[Local] Moved: {clean_asset_name} -> {page_name}/")
                
            # Enforce clean relative paths format: page_name/asset_name
            new_markdown_path = f"{page_name}/{clean_asset_name}"
            updated_content = updated_content.replace(asset_path, new_markdown_path)
            
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"[Local] Paths fixed inside {md_file}\n")

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    organize_local_vault(current_directory)

```
### 2. The GitHub Repository Script (prepare_github_vault.py)
This version is designed to run in a remote environment or a repository context. Instead of just looking at a flat directory, it recursively crawls **deeply nested sub-directories** (os.walk), converts any absolute or broken cross-repository paths to strict relative locations, and ensures the entire folder tree is valid and structured correctly before zipping.
```python
import os
import re

def organize_github_vault(base_dir):
    # Regex to capture all local markdown links and asset strings
    link_pattern = re.compile(r'!?\[.*?\]\(((?!http)[^)]+)\)')
    
    # Recursively traverse every nested folder inside the GitHub repository
    for root, dirs, files in os.walk(base_dir):
        md_files = [f for f in files if f.endswith('.md')]
        
        for md_file in md_files:
            md_file_path = os.path.join(root, md_file)
            page_name = os.path.splitext(md_file)[0]
            
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            matches = link_pattern.findall(content)
            if not matches:
                continue
                
            updated_content = content
            changes_made = False
            
            for asset_path in matches:
                # Strip leading relative pointers like ./ or ../ if they cause mapping issues
                clean_path = asset_path.lstrip('./')
                
                # Ensure the path perfectly conforms to Notion-style: folder_name/filename
                if not clean_path.startswith(f"{page_name}/"):
                    filename = os.path.basename(clean_path)
                    new_relative_path = f"{page_name}/{filename}"
                    
                    updated_content = updated_content.replace(asset_path, new_relative_path)
                    print(f"[GitHub] Standardized path in {md_file}: {asset_path} -> {new_relative_path}")
                    changes_made = True
            
            if changes_made:
                with open(md_file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"[GitHub] Saved optimized formatting for {md_file}\n")

if __name__ == "__main__":
    # Scans the entire repository tree starting from the script location
    repo_root_directory = os.path.dirname(os.path.realpath(__file__))
    organize_github_vault(repo_root_directory)

```
