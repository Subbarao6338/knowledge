# Regular Expressions (Regex) Cheatsheet

Regular expressions (regex) are special sequence of characters used to find or match patterns in text. This guide covers standard regex features along with specific language rules.

---

## 1. Character Classes

| Matcher | Description | Example Matches |
| :--- | :--- | :--- |
| `.` | Any character except newline | `a.b` -> `axb`, `a2b` |
| `\d` | Any digit (equivalent to `[0-9]`) | `\d\d` -> `23`, `99` |
| `\D` | Any non-digit character | `\D\D` -> `ab`, `X!` |
| `\w` | Any word character (alphanumeric + `_`) | `\w` -> `a`, `7`, `_` |
| `\W` | Any non-word character | `\W` -> `!`, `@`, ` ` |
| `\s` | Any whitespace character (space, tab, newline) | `\s` -> ` `, `\t`, `\n` |
| `\S` | Any non-whitespace character | `\S` -> `a`, `1`, `$` |
| `[abc]` | Any character in the set | `[abc]` -> `a`, `b`, `c` |
| `[^abc]` | Any character NOT in the set | `[^abc]` -> `z`, `2`, `!` |
| `[a-z]` | Any character in the range | `[a-z]` -> `d`, `g`, `y` |

---

## 2. Anchors & Boundaries

Anchors assert positions rather than matching characters.

- `^`: Matches start of the line or string.
- `$`: Matches end of the line or string.
- `\b`: Matches a word boundary position (between a word character and a non-word character).
- `\B`: Matches a non-word boundary position.

---

## 3. Quantifiers

| Quantifier | Match Frequency | Behavior |
| :--- | :--- | :--- |
| `*` | 0 or more times | Greedy (matches as much as possible) |
| `+` | 1 or more times | Greedy |
| `?` | 0 or 1 time | Greedy |
| `{n}` | Exactly `n` times | Greedy |
| `{n,}` | `n` or more times | Greedy |
| `{n,m}` | Between `n` and `m` times | Greedy |
| `*?` | 0 or more times | Lazy / Non-greedy (matches as little as possible) |
| `+?` | 1 or more times | Lazy / Non-greedy |

---

## 4. Groups & Lookarounds

### Capture Groups & Alternation
- `(abc)`: Captures group #1 and remembers characters matched.
- `(?:abc)`: Non-capturing group. Groups characters but does not capture or count them.
- `a|b`: Matches either `a` or `b` (alternation).
- `\1`: Matches whatever group #1 matched (backreference).

### Lookarounds (Supported in PCRE, JS, Python; limited in Go)
- `(?=abc)`: Positive lookahead. Asserts that `abc` follows current position.
- `(?!abc)`: Negative lookahead. Asserts that `abc` does NOT follow.
- `(?<=abc)`: Positive lookbehind. Asserts that `abc` precedes current position.
- `(?<!abc)`: Negative lookbehind. Asserts that `abc` does NOT precede.

---

## 5. Cheat Examples by Language

### Python (`re` module)
```python
import re

text = "My phone number is 123-456-7890."
pattern = r"\d{3}-\d{3}-\d{4}"

# Search (anywhere in string)
match = re.search(pattern, text)
if match:
    print("Found:", match.group())

# Find all occurrences
numbers = re.findall(r"\d+", text) # ['123', '456', '7890']

# Replace
clean_text = re.sub(r"\d", "X", text) # "My phone number is XXX-XXX-XXXX."
```

### JavaScript (`RegExp`)
```javascript
const text = "Contact support@example.com for help.";
const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;

// Test existence
const hasEmail = emailRegex.test(text); // true

// Match all
const matches = text.match(emailRegex); // ['support@example.com']

// Replace
const anonymous = text.replace(emailRegex, "[REDACTED]");
```

### Go (`regexp` package)
Go uses the **RE2** engine, which does **NOT** support lookarounds or backreferences to ensure linear-time parsing.

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    text := "Task completed at 2026-07-17."
    re := regexp.MustCompile(`\d{4}-\d{2}-\d{2}`)

    // Find first match
    match := re.FindString(text) // "2026-07-17"
    fmt.Println(match)

    // Check match status
    isMatch := re.MatchString(text) // true
    fmt.Println(isMatch)
}
```
