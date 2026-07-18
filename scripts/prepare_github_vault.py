import os
import re
import urllib.parse

def organize_github_vault(base_dir):
    """
    Recursively crawls a GitHub directory tree/vault.
    Validates and standardizes relative local links inside Markdown files.
    Ensures link target folders match the exact naming of parent pages (with hashes if present).
    Ensures relative links use proper percent encoding.
    """
    # Regex to capture all local markdown links and asset strings
    link_pattern = re.compile(r'!?\[.*?\]\(((?!http|https|mailto:)[^)]+)\)')

    abs_base = os.path.abspath(base_dir)
    print(f"[GitHub Validator] Starting recursive scan from base: {abs_base}")

    # Recursively traverse every nested folder inside the base directory
    for root, dirs, files in os.walk(base_dir):
        md_files = [f for f in files if f.endswith('.md')]

        for md_file in md_files:
            md_file_path = os.path.join(root, md_file)
            page_name = os.path.splitext(md_file)[0]

            try:
                with open(md_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"[GitHub] Error reading {md_file_path}: {str(e)}")
                continue

            matches = link_pattern.findall(content)
            if not matches:
                continue

            updated_content = content
            changes_made = False

            for asset_path in matches:
                # Safely URL-decode and strip any URL parameters/hash anchors
                parsed = urllib.parse.urlparse(asset_path)
                decoded_path = urllib.parse.unquote(parsed.path)

                # Check for path-traversal safety relative to base_dir
                abs_asset = os.path.abspath(os.path.join(root, decoded_path))
                if not abs_asset.startswith(abs_base):
                    print(f"[GitHub] Skipping unsafe path traversal: {asset_path}")
                    continue

                clean_path = decoded_path.lstrip('./')

                # Ensure the path perfectly conforms to Notion-style: page_name/filename
                # page_name can contain spaces and the 32-character hexadecimal suffix.
                expected_prefix = f"{page_name}/"
                if not clean_path.startswith(expected_prefix):
                    filename = os.path.basename(clean_path)
                    if not filename:
                        continue

                    encoded_page_name = urllib.parse.quote(page_name)
                    encoded_filename = urllib.parse.quote(filename)
                    new_relative_path = f"{encoded_page_name}/{encoded_filename}"

                    if asset_path != new_relative_path:
                        updated_content = updated_content.replace(asset_path, new_relative_path)
                        print(f"[GitHub] Standardized path in {md_file}: {asset_path} -> {new_relative_path}")
                        changes_made = True

            if changes_made:
                try:
                    with open(md_file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"[GitHub] Saved optimized formatting for {md_file}\n")
                except Exception as e:
                    print(f"[GitHub] Error writing to {md_file_path}: {str(e)}")

if __name__ == "__main__":
    # Scans starting from the script's parent repository root
    repo_root_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    organize_github_vault(repo_root_directory)
