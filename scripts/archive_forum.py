import os
import re
import time
import requests
import urllib.parse
import argparse
import json
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def clean_filename(text):
    """Makes text completely safe for local file paths across different operating systems."""
    cleaned = re.sub(r'[\\/*?:"<>|]', "", text.strip())
    return re.sub(r'\s+', "-", cleaned)

def get_retry_session(retries=3, backoff_factor=1, status_forcelist=(500, 502, 503, 504)):
    """Initializes an HTTP Session with mounted adapters for automated exponential backoff retries."""
    session = requests.Session()
    retry_policy = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_policy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

class ForumArchiver:
    def __init__(self, output_dir="forum_vault", delay=1.0, next_selector=None):
        self.session = get_retry_session()
        self.output_dir = os.path.normpath(output_dir)
        self.delay = delay
        self.next_selector = next_selector
        os.makedirs(self.output_dir, exist_ok=True)
        # Set standard browser user-agent to bypass primitive blocking headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })

    def login_to_forum(self, login_url, payload):
        """Transmits POST payload to login, maintaining authenticated cookie state."""
        print(f"Attempting authentication at: {login_url}")
        try:
            response = self.session.post(login_url, data=payload, timeout=15)
            if response.status_code == 200:
                print("Login request sent. Cookie session updated.")
                return True
            print(f"Login failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Network error during authentication: {str(e)}")
        return False

    def download_media(self, img_url, assets_folder):
        """Downloads external media using the robust retry session into the local assets folder."""
        try:
            parsed_img = urllib.parse.urlparse(img_url)
            clean_img_name = os.path.basename(parsed_img.path)
            if not clean_img_name:
                return None

            save_path = os.path.normpath(os.path.join(assets_folder, clean_img_name))

            # Traversal security check
            if not os.path.abspath(save_path).startswith(os.path.abspath(assets_folder)):
                print(f"[Media] Traversal attack blocked for asset: {img_url}")
                return None

            img_res = self.session.get(img_url, stream=True, timeout=15)
            if img_res.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in img_res.iter_content(4096):
                        f.write(chunk)
                return clean_img_name
        except Exception as e:
            print(f"Failed to download image from {img_url}: {str(e)}")
        return None

    def scrape_thread(self, first_page_url, content_css_selector):
        """
        Crawls a forum thread page-by-page until pagination ends.
        Saves each page as a safe, unquoted markdown file next to standard assets directories.
        """
        current_url = first_page_url
        page_counter = 1

        # Pull thread title slug from the initial URL
        parsed_url = urllib.parse.urlparse(current_url)
        url_path = parsed_url.path
        thread_slug = clean_filename(url_path.split('/')[-1].replace('.html', ''))
        if not thread_slug:
            thread_slug = f"thread-archive-{abs(hash(first_page_url))}"

        # Prepare normalized directories
        thread_assets_dir = os.path.normpath(os.path.join(self.output_dir, thread_slug))

        # Traversal check
        if not os.path.abspath(thread_assets_dir).startswith(os.path.abspath(self.output_dir)):
            print(f"[Crawler] Terminated: Target directory resolves outside of vault: {thread_slug}")
            return

        os.makedirs(thread_assets_dir, exist_ok=True)

        while current_url:
            print(f"Archiving Page {page_counter}: {current_url}")
            try:
                res = self.session.get(current_url, timeout=15)
                if res.status_code != 200:
                    print(f"Failed to retrieve page {page_counter} (Status: {res.status_code}). Stopping crawl.")
                    break
            except Exception as e:
                print(f"Network error on page {page_counter}: {str(e)}. Stopping crawl.")
                break

            soup = BeautifulSoup(res.text, 'html.parser')

            # Isolate the core page text container (bypassing sidebars, footprints, and ads)
            content_block = soup.select_one(content_css_selector)
            if not content_block:
                print(f"Warning: Selector '{content_css_selector}' not found. Falling back to page body.")
                content_block = soup.body
                if not content_block:
                    print("Error: Empty page body. Skipping page.")
                    break

            # Find and download all images embedded in the content container
            for img_tag in content_block.find_all('img'):
                src_url = img_tag.get('src')
                if src_url and not src_url.startswith('data:'):
                    # Robust URL resolution using standard urljoin
                    resolved_src_url = urllib.parse.urljoin(current_url, src_url)

                    local_img_name = self.download_media(resolved_src_url, thread_assets_dir)
                    if local_img_name:
                        # Re-point the HTML source to the relative location, safely percent-encoded
                        encoded_thread_slug = urllib.parse.quote(thread_slug)
                        encoded_img_name = urllib.parse.quote(local_img_name)
                        img_tag['src'] = f"{encoded_thread_slug}/{encoded_img_name}"

            # Convert HTML slice into clean Markdown
            markdown_text = md(str(content_block), heading_style="ATX")

            # Save the file cleanly
            md_filename = f"{thread_slug}-Page-{page_counter}.md"
            md_file_path = os.path.normpath(os.path.join(self.output_dir, md_filename))

            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Page {page_counter}\n\n")
                f.write(f"Source URL: {current_url}\n\n---\n\n")
                f.write(markdown_text)

            print(f"Saved page file: {md_filename}")

            # Detect next-page button using custom CSS selector or standard fallback matching
            next_link_tag = None
            if self.next_selector:
                next_link_tag = soup.select_one(self.next_selector)

            if not next_link_tag:
                # Fallback to standard regex matching
                next_link_tag = (
                    soup.find('a', string=re.compile(r'Next|>', re.IGNORECASE)) or
                    soup.find('a', class_=re.compile(r'next', re.IGNORECASE))
                )

            if next_link_tag and next_link_tag.get('href'):
                next_href = next_link_tag.get('href')
                current_url = urllib.parse.urljoin(current_url, next_href)
                page_counter += 1
                if self.delay > 0:
                    time.sleep(self.delay)
            else:
                current_url = None  # End loop cleanly

        print(f"Crawl completed. Outputs stored in '{self.output_dir}/{thread_slug}'\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forum Site Archiver to Notion-Ready Markdown")
    parser.add_argument("--url", "-u", type=str, help="Target first page URL of the thread")
    parser.add_argument("--selector", "-s", type=str, help="CSS selector of the content block")
    parser.add_argument("--next-selector", "-n", type=str, help="CSS selector of the Next page link element")
    parser.add_argument("--output", "-o", type=str, default="forum_vault", help="Output directory path")
    parser.add_argument("--delay", "-d", type=float, default=1.0, help="Delay (in seconds) between requests")
    parser.add_argument("--cookie", "-c", type=str, help="Raw cookie header string to attach to HTTP requests")
    parser.add_argument("--headers", type=str, help="Custom HTTP headers formatted as a JSON string")

    args = parser.parse_args()

    archiver = ForumArchiver(output_dir=args.output, delay=args.delay, next_selector=args.next_selector)

    # Attach custom headers or cookies if provided
    if args.cookie:
        archiver.session.headers.update({'Cookie': args.cookie})

    if args.headers:
        try:
            custom_headers = json.loads(args.headers)
            archiver.session.headers.update(custom_headers)
        except Exception as e:
            print(f"Error parsing custom headers JSON: {str(e)}")

    if args.url and args.selector:
        archiver.scrape_thread(args.url, content_css_selector=args.selector)
    else:
        print("No URL or content selector specified. Running with example parameters (mock mode).")
        # Example target thread and text selection parameters
        TARGET_THREAD_URL = "https://www.literotica.com/s/example-sample-story-slug"
        CONTENT_SELECTOR = "div.b-story-body-p"
        print(f"To run manually: python archive_forum.py --url {TARGET_THREAD_URL} --selector '{CONTENT_SELECTOR}'")
