I want python script for save every page, every forum, evey subpage or whatever, everything from forum sites like literotica, xissipy. Xossipy need username, password authentication to view sub forums. Every page or subpage in each thread as one md file with embedded media

Scraping highly customized web forums (especially adult platforms like Literotica or vBulletin/XenForo-style boards like Xossipy which use complex session cookies, anti-bot protections, and deep paging structures) requires a robust scraper. A basic script will quickly get blocked or fail to navigate the threads properly.
To pull forum threads down into a clean Notion-ready .md structure with a matching folder for embedded media, you need a headless browser layout or an authenticated session scraper.
### Prerequisites
Install the required packages for network handling, session tracking, and converting raw HTML directly into readable Markdown:
```bash
pip install requests beautifulsoup4 markdownify

```
### The Forum Archiver Script (archive_forum.py)
This script handles logging into a protected forum, managing your session cookies, crawling a specific thread page-by-page, and writing out individual .md files along with an assets folder for embedded media.
```python
import os
import re
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def clean_filename(text):
    """Makes text completely safe for local file paths."""
    return re.sub(r'[\\/*?:"<>|]', "", text.strip().replace(" ", "-"))

class ForumArchiver:
    def __init__(self, output_dir="forum_vault"):
        self.session = requests.Session()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        # Standard browser User-Agent header to avoid basic bot-blocking walls
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def login_to_forum(self, login_url, payload):
        """
        Handles form authentication.
        payload example: {'username': 'my_user', 'password': 'my_password'}
        Note: You will need to inspect the network tab to match exact form field names.
        """
        print(f"Attempting authentication at: {login_url}")
        response = self.session.post(login_url, data=payload)
        if response.ok:
            print("Login payload transmitted successfully.")
            return True
        print("Login request failed.")
        return False

    def download_media(self, img_url, assets_folder):
        """Downloads external images locally into the specific thread's asset folder."""
        try:
            clean_img_name = os.path.basename(img_url.split('?')[0])
            if not clean_img_name:
                return None
            
            save_path = os.path.join(assets_folder, clean_img_name)
            
            # Request image bytes using the authenticated session
            img_res = self.session.get(img_url, stream=True, timeout=10)
            if img_res.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in img_res.iter_content(1024):
                        f.write(chunk)
                return clean_img_name
        except Exception as e:
            print(f"Skipping media download for {img_url}: {e}")
        return None

    def scrape_thread(self, first_page_url, content_css_selector):
        """
        Crawls a forum thread page-by-page until no 'Next' button or page link remains.
        Saves each forum page as an independent .md file.
        """
        current_url = first_page_url
        page_counter = 1
        
        # Pull thread title from the initial URL string to create the folder mapping
        thread_slug = clean_filename(current_url.split('/')[-1].replace('.html', ''))
        if not thread_slug:
            thread_slug = f"thread-archive-{hash(first_page_url)}"

        # Setup local Notion-style hierarchy
        thread_assets_dir = os.path.join(self.output_dir, thread_slug)
        os.makedirs(thread_assets_dir, exist_ok=True)

        while current_url:
            print(f"Archiving Page {page_counter}: {current_url}")
            res = self.session.get(current_url)
            if not res.ok:
                print(f"Failed to read page {page_counter}. Stopping crawl.")
                break

            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 1. Isolate the core content wrapper (ignores sidebars, ads, signatures)
            content_block = soup.select_one(content_css_selector)
            if not content_block:
                print(f"Warning: Could not isolate text using CSS selector: '{content_css_selector}'")
                content_block = soup.body # Fall back to body if target missing

            # 2. Extract and download embedded media blocks inside this page
            for img_tag in content_block.find_all('img'):
                src_url = img_tag.get('src')
                if src_url and not src_url.startswith('data:'):
                    # Resolve relative URLs to absolute links if necessary
                    if src_url.startswith('//'):
                        src_url = 'https:' + src_url
                    elif src_url.startswith('/'):
                        # Simplistic fallback base domain assembly
                        base_domain = "/".join(current_url.split('/')[:3])
                        src_url = base_domain + src_url
                        
                    local_img_name = self.download_media(src_url, thread_assets_dir)
                    if local_img_name:
                        # Re-point the HTML source relative to the master markdown location
                        img_tag['src'] = f"{thread_slug}/{local_img_name}"

            # 3. Convert the cleaned HTML slice cleanly to markdown syntax
            markdown_text = md(str(content_block), heading_style="ATX")

            # 4. Save this specific page out as its own markdown file
            md_filename = f"{thread_slug}-Page-{page_counter}.md"
            md_file_path = os.path.join(self.output_dir, md_filename)
            
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Page {page_counter}\n\n")
                f.write(f"Source URL: {current_url}\n\n---\n\n")
                f.write(markdown_text)

            print(f"Saved: {md_filename}")

            # 5. Automatically detect and extract pagination links for the next page
            # To avoid dead loops, adjust this search logic to target your specific platform's 'Next' button
            next_link_tag = soup.find('a', text=re.compile(r'Next|>', re.IGNORECASE)) or soup.find('a', class_=re.compile(r'next', re.IGNORECASE))
            
            if next_link_tag and next_link_tag.get('href'):
                next_href = next_link_tag.get('href')
                if next_href.startswith('http'):
                    current_url = next_href
                else:
                    base_domain = "/".join(current_url.split('/')[:3])
                    current_url = base_domain + ('/' if not next_href.startswith('/') else '') + next_href
                page_counter += 1
            else:
                current_url = None # Loop terminates cleanly when pagination ends

        print(f"Finished crawling thread: {thread_slug}\n")

if __name__ == "__main__":
    archiver = ForumArchiver(output_dir="./forum_vault")

    # Example 1: Scrape authenticated forum layout (Xossipy style)
    # Check the site's login source code to update form field keys ('user', 'pass', etc.)
    LOGIN_URL = "https://example-forum-auth.com/login.php"
    LOGIN_DATA = {
        'username': 'YOUR_ACCOUNT_NAME',
        'password': 'YOUR_PASSWORD'
    }
    
    # Authenticate before running requests
    # archiver.login_to_forum(LOGIN_URL, LOGIN_DATA)

    # Example 2: Run crawl over a specific thread target
    # The CSS Selector isolating the main text block varies by platform:
    # - Literotica typically uses '.b-story-body-p' or '#story-text'
    # - XenForo/vBulletin setups usually use '.message-content' or '.post-text'
    TARGET_THREAD_URL = "https://www.literotica.com/s/example-sample-story-slug"
    CONTENT_SELECTOR = "div.b-story-body-p" 

    archiver.scrape_thread(TARGET_THREAD_URL, content_css_selector=CONTENT_SELECTOR)

```
### Customizing the Script to Your Targets
 1. **The Content Selector:** Before firing off the code, open a sample thread in your browser, right-click the text content, select **Inspect**, and find the tag wrapper holding the post content (e.g., <div class="post-text">). Change CONTENT_SELECTOR to match that target.
 2. **Login Payloads:** Sites with complex protections (like Cloudflare or JS challenges) may reject basic script logins. If the script fails to authenticate automatically, open your web browser, log in manually, export your **Session Cookies** via a browser extension, and attach them directly using self.session.cookies.set(...) instead.
