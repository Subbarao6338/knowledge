---
layout: default
title: "Playwright Cheatsheet"
---

# Playwright Cheatsheet

Playwright is a powerful framework for Web-Testing and Automation. It supports Chromium, Firefox, and WebKit browser engines with a unified, cross-platform API.

---

## 1. Setup and CLI Commands

Get started with installing the Python or Node.js bindings and downloading the respective browser binaries.

```bash
# For Python:
pip install playwright
playwright install                      # Download browser binaries (Chromium, Firefox, WebKit)

# For Node.js:
npm init playwright@latest
```

### Useful CLI Commands
| Command | Description |
|---------|-------------|
| `playwright codegen <url>` | Open inspector tool to automatically generate scripts based on user interactions |
| `playwright open <url>` | Open a specific URL in a browser window |
| `playwright screenshot <url> output.png` | Grab a screenshot of a page |
| `playwright pdf <url> output.pdf` | Save page layout as a PDF (Chromium-only) |

---

## 2. Basic Browser and Page Lifecycle

Synchronous and Asynchronous options are available in Python. Here are both patterns:

### Synchronous Script Structure
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launch browser (headed or headless)
    browser = p.chromium.launch(headless=True)

    # Create browser context (emulating custom settings)
    context = browser.new_context(viewport={"width": 1280, "height": 720})

    # Create a new page
    page = context.new_page()

    # Navigate to URL
    page.goto("https://example.com")
    print(page.title())

    # Clean up
    browser.close()
```

### Asynchronous Script Structure
```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```

---

## 3. Element Selectors & Locators

Locators are the central piece of Playwright's auto-waiting and retry-ability logic.

```python
# Locate by Role (Recommended standard)
page.get_by_role("button", name="Submit").click()

# Locate by Text matches
page.get_by_text("Welcome to our portal").click()

# Locate by Label
page.get_by_label("Username").fill("alice_dev")

# Locate by Placeholder
page.get_by_placeholder("Enter password...").fill("secret123")

# Locate by Alt Text (for images)
page.get_by_alt_text("Main application logo").click()

# Locate by Test ID (looks for data-testid="..." in HTML)
page.get_by_test_id("submit-button").click()

# Standard CSS and XPath Selectors fallback
page.locator("#main-container .item-row").first.click()
page.locator("//div[@id='content']").click()
```

---

## 4. Common Page Interactions

```python
# Text Inputs
page.locator("#username").fill("alice")
page.locator("#username").clear()
page.locator("#username").press_sequentially("slow typing...", delay=100)

# Checkboxes and Radio Buttons
page.get_by_label("I agree to terms").check()
page.get_by_label("I agree to terms").uncheck()
assert page.get_by_label("I agree to terms").is_checked()

# Dropdowns (Select tags)
page.locator("#country-select").select_option(value="US")
page.locator("#country-select").select_option(label="United States")

# Hovering & Mouse Events
page.get_by_role("menuitem", name="Developer Tools").hover()
page.locator("#draw-area").click(button="right")  # Right click
page.locator(".card").dblclick()                 # Double click

# File Uploads
page.get_by_label("Upload PDF").set_input_files("my_document.pdf")
page.get_by_label("Upload PDF").set_input_files([])  # Clear upload list

# Pressing Keyboard Keys
page.press("input#search", "Enter")
page.press("body", "Control+KeyA")
```

---

## 5. Wait Strategies & Actions

Playwright automatically waits for elements to be visible, enabled, and stable before running interactions (Auto-Waiting).

### Manual Wait Helpers
```python
# Wait for exact page navigation to finish
page.wait_for_url("**/dashboard")

# Wait for element to achieve specific state
page.locator(".success-banner").wait_for(state="visible", timeout=5000)

# Wait for a custom duration (Avoid using in production - use network or state waits instead)
page.wait_for_timeout(1000)
```

---

## 6. Assertions (Expectations)

Playwright provides web-first assertions that automatically poll and retry until conditions are met.

```python
from playwright.sync_api import expect

# Validate visibility
expect(page.get_by_role("heading", name="Welcome")).to_be_visible()

# Validate values and states
expect(page.locator("#submit-btn")).to_be_enabled()
expect(page.get_by_label("Subscribe")).to_be_checked()

# Validate texts
expect(page.locator(".alert-message")).to_contain_text("Successfully saved!")
expect(page.locator("#user-id-field")).to_have_value("USR-1002")

# Validate URLs and Page Attributes
expect(page).to_have_url("https://example.com/dashboard")
expect(page).to_have_title("My Dashboard Portal")
```

---

## 7. Advanced Automation Features

### Grabbing Screenshots
```python
# Page Screenshot
page.screenshot(path="screenshot.png")

# Element-Specific Screenshot
page.locator(".chart-container").screenshot(path="chart.png")

# Full-scrollable Page Screenshot
page.screenshot(path="full_page.png", full_page=True)
```

### Network Interception & Mocking
Mock API responses directly during automated browser sessions:

```python
# Mock any API call matching a pattern and return a custom JSON payload
page.route("**/api/users/*", lambda route: route.fulfill(
    status=200,
    content_type="application/json",
    json={"id": 42, "name": "Fake Alice", "role": "Mock User"}
))

page.goto("https://example.com/profiles/42")
# The application UI will now receive and display the mocked profile data!
```
