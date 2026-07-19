import os
import re
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

def organize_github_vault(base_dir, exclude_dirs=None, exclude_files=None, force_all=False):
    """
    Recursively crawls a GitHub directory tree/vault.
    Validates and standardizes relative local links inside Markdown files.
    Ensures link target folders match the exact naming of parent pages (with hashes if present).
    Ensures relative links use proper percent encoding.
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', '.github', 'scripts'}
    else:
        exclude_dirs = set(exclude_dirs)

    if exclude_files is None:
        exclude_files = {'README.md', 'Notion_structure.md', 'Notion_scripts.md', 'Files to md.md', 'Site to md.md'}
    else:
        exclude_files = set(exclude_files)

    # Regex to capture all local markdown links and asset strings
    link_pattern = re.compile(r'!?\[.*?\]\(((?!http|https|mailto:)[^)]+)\)')

    abs_base = os.path.abspath(base_dir)
    print(f"[GitHub Validator] Starting recursive scan from base: {abs_base}")
    print(f"[GitHub Validator] Excluded directories: {exclude_dirs}")
    print(f"[GitHub Validator] Excluded files: {exclude_files}")

    # Recursively traverse every nested folder inside the base directory
    for root, dirs, files in os.walk(base_dir):
        # Filter directories in-place to prevent walking into excluded directories
        if not force_all:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

        md_files = [f for f in files if f.endswith('.md')]

        for md_file in md_files:
            if not force_all and md_file in exclude_files:
                continue

            md_file_path = os.path.join(root, md_file)
            page_name = os.path.splitext(md_file)[0]

            try:
                with open(md_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"[GitHub] Error reading {md_file_path}: {str(e)}")
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
                # Safely URL-decode and strip any URL parameters/hash anchors
                parsed = urllib.parse.urlparse(asset_path)
                decoded_path = urllib.parse.unquote(parsed.path)

                # Skip template strings or placeholder variables
                if "{" in decoded_path or "}" in decoded_path:
                    continue

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
                # Unmask to get the full original content with updated links
                final_content = unmask_inline_code(updated_content, inline_placeholders)
                final_content = unmask_code_blocks(final_content, fenced_placeholders)
                try:
                    with open(md_file_path, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    print(f"[GitHub] Saved optimized formatting for {md_file}\n")
                except Exception as e:
                    print(f"[GitHub] Error writing to {md_file_path}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Pre-flight Vault Link Validator")
    parser.add_argument("target_dir", nargs="?", default=None, help="Root directory of the vault to scan")
    parser.add_argument("--exclude-dirs", nargs="+", default=None, help="Directories to ignore")
    parser.add_argument("--exclude-files", nargs="+", default=None, help="Markdown files to ignore")
    parser.add_argument("--force-all", action="store_true", help="Force scanning all folders/files and ignore exclusions")

    args = parser.parse_args()

    # Default to script parent's repository root if target_dir not provided
    if args.target_dir is None:
        target_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    else:
        target_dir = args.target_dir

    organize_github_vault(
        target_dir,
        exclude_dirs=args.exclude_dirs,
        exclude_files=args.exclude_files,
        force_all=args.force_all
    )
