---
layout: default
title: "HTML, XHTML & MHTML Cheatsheet"
---

# HTML, XHTML & MHTML Cheatsheet

## HTML5 Semantic Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Semantic Page Document</title>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <article>
            <section>
                <h1>Article Header</h1>
                <p>Paragraph body content detailing web standard features.</p>
            </section>
        </article>
    </main>

    <footer>
        <p>&copy; 2026 Semantic Standards Association.</p>
    </footer>
</body>
</html>
```

## XHTML Differences & Rigid Syntax Rules

XHTML (Extensible HyperText Markup Language) is a stricter, XML-based application of HTML.

1. **Documents must have a strict XML declaration & namespace DOCTYPE:**
   ```html
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
   <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
   ```
2. **Every tag must be closed:** Even empty tags like `<br>` or `<img>` must end with a trailing slash: `<br />` or `<img src="pic.jpg" />`.
3. **Tags and attribute names must be lowercase:** `<body>` not `<BODY>`.
4. **Attributes must always be quoted and fully evaluated:** No attribute minimization like `<input disabled />`. Must write: `<input disabled="disabled" />`.

## MHTML Definition

MHTML (MIME HTML, or `.mhtml`/`.mht`) is an archive file format used to save full web pages (with markup, styling, images, and audio/video resources) in a single unified text file.

- Uses **MIME multipart types** (`multipart/related`) similar to email messages.
- Employs boundaries (e.g., `------=_NextPart_000_...`) to separate the HTML document from referenced images, which are encoded using **Base64 binary encoding**.
- Works out of the box in Internet Explorer, modern Chromium-based browsers, and standalone PDF/archiving tools.
