# Markdown Cheatsheet (.md / .mdx)

`.mdx` is Markdown plus embedded JSX components — everything in standard Markdown works in MDX; the MDX-specific section is at the end.

## Headings

```markdown
# H1
## H2
### H3
#### H4
##### H5
###### H6

Alt H1
======

Alt H2
------
```

## Text Formatting

```markdown
*italic* or _italic_
**bold** or __bold__
***bold italic***
~~strikethrough~~
`inline code`
==highlight== (supported by some renderers, e.g. GitHub via extensions, not core spec)
Superscript: text^sup^ (extension-dependent)
Subscript: text~sub~ (extension-dependent)

Line break: end a line with two spaces or use <br>
```

## Lists

```markdown
- Item one
- Item two
  - Nested item
    - Deeper nesting

* Also valid
+ Also valid

1. First
2. Second
   1. Nested numbered
3. Third

- [ ] Unchecked task
- [x] Checked task
```

## Links & Images

```markdown
[link text](https://example.com)
[link with title](https://example.com "Title text")
[relative link](./other-page.md)
[reference link][ref]

[ref]: https://example.com "optional title"

<https://example.com>          # auto-link, renders as clickable URL

![alt text](image.png)
![alt text](image.png "optional title")
![alt with link](image.png)[link](https://example.com)   # image wrapped in a link (nonstandard, use HTML for reliability)

<!-- Reliable image + link combo -->
[![alt text](image.png)](https://example.com)
```

## Code Blocks

````markdown
```python
def hello():
    print("Hello, world!")
```

```bash
echo "shell syntax highlighting"
```

    Indented code block (4 spaces) — older style, still valid
````

## Tables

```markdown
| Column A | Column B | Column C |
|----------|:--------:|---------:|
| left     | center   | right    |
| a        | b        | c        |

<!-- Alignment: :--- left, :---: center, ---: right -->
```

## Blockquotes

```markdown
> Single-level quote

> Level one
>> Level two nested
>>> Level three nested

> Multi-line
> blockquote text
> continues here
```

## Horizontal Rules

```markdown
---
***
___
```

## Footnotes (extension, widely supported)

```markdown
Here's a claim with a footnote.[^1]

[^1]: This is the footnote text.
```

## Definition Lists (extension)

```markdown
Term
: Definition one
: Definition two
```

## Escaping Special Characters

```markdown
\* not italic \*
\# not a heading
\[not a link\]
```

Characters that often need escaping: `\ ` `` ` `` `*` `_` `{}` `[]` `()` `#` `+` `-` `.` `!`

## HTML in Markdown

Most Markdown renderers pass raw HTML through untouched — useful for things Markdown syntax can't express (alignment, `<details>`, custom styling):

```markdown
<details>
<summary>Click to expand</summary>

Hidden content here — can include more Markdown inside the tags in most renderers.

</details>

<div align="center">
  Centered content
</div>

<br>
<sub>small text</sub>
<sup>superscript</sup>
```

## GitHub Flavored Markdown (GFM) Extras

```markdown
@username           # mentions (rendered on GitHub)
#123                # issue/PR reference (rendered on GitHub)
:emoji_name:            # emoji shortcode, e.g. :rocket: :tada:

```mermaid
graph TD
  A --> B
```
<!-- GitHub renders fenced ```mermaid blocks as diagrams automatically -->

~~~
Alternate fence using tildes instead of backticks — useful if your code content contains backticks
~~~
```

## Front Matter (used by static site generators — Jekyll, Hugo, Next.js, etc.)

```markdown
---
title: "My Post"
date: 2026-07-17
tags: [python, tutorial]
draft: false
---

Content starts here.
```

---

## MDX-Specific Syntax (.mdx)

MDX = Markdown + JSX. It lets you import and render React components inline.

### Importing & Using Components

```mdx
import { Chart } from './components/Chart';
import Callout from './components/Callout';

# My Page

Regular **markdown** text works as normal.

<Callout type="warning">
  This is a JSX component rendered inline with plain text as children.
</Callout>

<Chart data={[1, 2, 3]} labels={["a", "b", "c"]} />
```

### JSX Expressions Inline

```mdx
The current year is {new Date().getFullYear()}.

{items.map(item => <li key={item.id}>{item.name}</li>)}
```

### Exporting Values (for use by the page/layout)

```mdx
export const meta = {
  title: "My Page",
  description: "A page about things",
};

export const growthRate = 0.15;

Revenue is expected to grow by {growthRate * 100}% this year.
```

### Mixing HTML-like JSX and Markdown

```mdx
<div className="my-custom-class">

Markdown **still works** inside a JSX block, as long as there's a blank line
after the opening tag and before content.

</div>
```

### MDX Gotchas

- Blank lines matter — Markdown syntax (like `**bold**` or lists) inside a JSX element only parses correctly if there's a blank line separating the JSX tag from the Markdown content.
- Component and prop names are case-sensitive, same as JSX (`<MyComponent />` not `<mycomponent />`).
- Curly braces `{}` are interpreted as JSX expressions — a literal `{` in prose needs escaping (`\{`) or backticks.
- `.mdx` files are compiled, not just rendered — a JSX syntax error will break the whole page build, unlike plain Markdown which degrades gracefully.

## Common Gotchas (Plain Markdown)

- A single line break in source does NOT create a new paragraph/line in rendered output — you need a blank line between paragraphs, or two trailing spaces for a `<br>`-style break.
- Nested list indentation requirements vary slightly between renderers (3 vs 4 spaces) — be consistent and check your target renderer if nesting breaks.
- Raw HTML block-level elements need a blank line before and after to be parsed correctly alongside Markdown syntax.
- Reference-style links (`[text][ref]`) require the `[ref]: url` definition to exist somewhere in the document, but it can be placed anywhere (including at the very end).
