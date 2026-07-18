import os
import re
import shutil
import urllib.parse
import argparse

def mask_code_blocks(content):
    """Temporarily masks fenced code blocks with placeholders."""
    lines = content.splitlines(keepends=True)
    in_block = False
    fence_char = None
    placeholders = []
    new_lines = []
    current_block = []

    for line in lines:
        stripped = line.strip()
        if not in_block:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_block = True
                fence_char = "```" if stripped.startswith("```") else "~~~"
                current_block.append(line)
            else:
                new_lines.append(line)
        else:
            current_block.append(line)
            if stripped.startswith(fence_char):
                placeholder = f"__CODE_BLOCK_PLACEHOLDER_{len(placeholders)}__"
                placeholders.append((placeholder, "".join(current_block)))
                new_lines.append(placeholder + "\n")
                current_block = []
                in_block = False

    if in_block and current_block:
        new_lines.extend(current_block)

    return "".join(new_lines), placeholders

def unmask_code_blocks(content, placeholders):
    """Restores masked fenced code blocks from placeholders."""
    for placeholder, original in reversed(placeholders):
        content = content.replace(placeholder + "\n", original)
        content = content.replace(placeholder, original)
    return content

def mask_inline_code(content):
    """Temporarily masks inline code (surrounded by backticks) with placeholders."""
    inline_placeholders = []

    def replace_inline(match):
        placeholder = f"__INLINE_CODE_PLACEHOLDER_{len(inline_placeholders)}__"
        inline_placeholders.append((placeholder, match.group(0)))
        return placeholder

    content = re.sub(r"`[^`\n]+`" , replace_inline, content)
    return content, inline_placeholders

def unmask_inline_code(content, inline_placeholders):
    """Restores masked inline code from placeholders."""
    for placeholder, original in reversed(inline_placeholders):
        content = content.replace(placeholder, original)
    return content

def organize_local_vault(target_dir, dry_run=False):
    """
    Scans target_dir for Markdown files.
    Identifies links inside them pointing to local files.
    Creates matching folders for parent pages (handling the 32-character Notion ID scheme).
    Moves loose referenced files into the respective folders and updates markdown links.
    """
    # Match markdown inline images ![]() and links []() pointing to local files
    # Ignores external web links starting with http/https or mailto:
    link_pattern = re.compile(r'!?\[.*?\]\(((?!http|https|mailto:)[^)]+)\)')

    try:
        files = os.listdir(target_dir)
    except Exception as e:
        print(f"[Local] Error listing target directory {target_dir}: {str(e)}")
        return

    md_files = [f for f in files if f.endswith('.md')]

    for md_file in md_files:
        page_name = os.path.splitext(md_file)[0]
        # In a proper Notion backup, the folder matches the markdown filename exactly
        assets_folder = os.path.join(target_dir, page_name)
        md_file_path = os.path.join(target_dir, md_file)

        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[Local] Error reading {md_file}: {str(e)}")
            continue

        # Mask code blocks and inline code to ignore links inside them
        masked_content, fenced_placeholders = mask_code_blocks(content)
        masked_content, inline_placeholders = mask_inline_code(masked_content)

        matches = link_pattern.findall(masked_content)
        if not matches:
            continue

        updated_content = masked_content
        changes_made = False

        for asset_path in matches:
            # Parse URL/percent-encoded link and strip any query parameters or hash anchors
            parsed = urllib.parse.urlparse(asset_path)
            decoded_path = urllib.parse.unquote(parsed.path)

            # Skip template strings or placeholder variables
            if "{" in decoded_path or "}" in decoded_path:
                continue

            clean_asset_name = os.path.basename(decoded_path)
            if not clean_asset_name:
                continue

            old_asset_location = os.path.join(target_dir, clean_asset_name)
            new_asset_location = os.path.join(assets_folder, clean_asset_name)

            # Check for path-traversal safety
            abs_target = os.path.abspath(target_dir)
            abs_old_asset = os.path.abspath(old_asset_location)
            if not abs_old_asset.startswith(abs_target):
                print(f"[Local] Skipping unsafe file path: {asset_path}")
                continue

            # Check if the asset is actually a loose file in target_dir OR if it's already organized
            loose_exists = os.path.exists(old_asset_location) and not os.path.isdir(old_asset_location)
            already_organized = os.path.exists(new_asset_location) and not os.path.isdir(new_asset_location)

            if not (loose_exists or already_organized):
                # Sibling reference or external path not existing loose in target_dir, skip changing link
                continue

            # Move loose files from root/target_dir into the specific parent folder
            if loose_exists:
                if not dry_run:
                    if not os.path.exists(assets_folder):
                        os.makedirs(assets_folder, exist_ok=True)
                        print(f"[Local] Created folder: {assets_folder}/")

                    # Ensure we don't overwrite/move onto ourselves
                    if abs_old_asset != os.path.abspath(new_asset_location):
                        try:
                            shutil.move(old_asset_location, new_asset_location)
                            print(f"[Local] Moved loose asset: {clean_asset_name} -> {page_name}/")
                        except Exception as e:
                            print(f"[Local] Error moving asset {clean_asset_name}: {str(e)}")
                else:
                    print(f"[Local][Dry-Run] Would move loose asset: {clean_asset_name} -> {page_name}/")

            # Enforce clean relative paths format with proper percent encoding
            # Encode components separately to preserve '/' path separator
            encoded_page_name = urllib.parse.quote(page_name)
            encoded_asset_name = urllib.parse.quote(clean_asset_name)
            new_markdown_path = f"{encoded_page_name}/{encoded_asset_name}"

            if asset_path != new_markdown_path:
                if not dry_run:
                    updated_content = updated_content.replace(asset_path, new_markdown_path)
                print(f"[Local] Path fix in {md_file}: {asset_path} -> {new_markdown_path}")
                changes_made = True

        if changes_made and not dry_run:
            # Unmask to get the full original content with updated links
            final_content = unmask_inline_code(updated_content, inline_placeholders)
            final_content = unmask_code_blocks(final_content, fenced_placeholders)
            try:
                with open(md_file_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                print(f"[Local] Paths fixed inside {md_file}\n")
            except Exception as e:
                print(f"[Local] Error writing back to {md_file}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local Vault Organizer - Group loose assets next to parent pages")
    parser.add_argument("target_dir", nargs="?", default=None, help="Directory to process")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying the files")

    args = parser.parse_args()

    # Default to current working directory if target_dir not provided
    if args.target_dir is None:
        target_dir = os.getcwd()
    else:
        target_dir = args.target_dir

    organize_local_vault(target_dir, dry_run=args.dry_run)
