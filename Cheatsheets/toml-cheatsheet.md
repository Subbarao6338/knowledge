# TOML Cheatsheet

TOML ("Tom's Obvious, Minimal Language") is a config format designed to be easy to read and unambiguous to parse, with a formal spec and native types (unlike INI). It's the standard for `pyproject.toml`, `Cargo.toml`, and many modern tool configs.

## Basic Key-Value Pairs

```toml
title = "My App"
version = "1.0.0"
debug = true
port = 8080
ratio = 0.75
```

## Data Types

```toml
string_basic = "hello world"
string_literal = 'C:\path\no\escapes\needed'      # literal string — no escape processing
string_multiline = """
line one
line two
"""
string_multiline_literal = '''
raw content, no escapes
'''

integer = 42
integer_hex = 0xDEADBEEF
integer_octal = 0o755
integer_binary = 0b11010110
integer_underscore = 1_000_000              # underscores allowed for readability

float_val = 3.14
float_exp = 5e+22
float_infinity = inf
float_nan = nan

boolean_true = true
boolean_false = false

date_time = 2026-07-17T10:00:00Z
date_time_local = 2026-07-17T10:00:00
date_only = 2026-07-17
time_only = 10:00:00
```

## Arrays

```toml
integers = [1, 2, 3]
strings = ["a", "b", "c"]
mixed_nested = [[1, 2], [3, 4, 5]]
floats = [1.1, 2.2, 3.3]

# Multi-line arrays (trailing comma allowed)
colors = [
    "red",
    "green",
    "blue",
]
```

## Tables (Sections)

```toml
[server]
host = "0.0.0.0"
port = 8080

[database]
url = "postgres://localhost/mydb"
timeout = 30

[database.pool]                # nested table — equivalent to [database.pool]
min_size = 5
max_size = 20

# Inline table — compact syntax for a small table on one line
point = { x = 1, y = 2 }
owner = { name = "Subbarao", email = "you@example.com" }
```

## Array of Tables

```toml
[[servers]]
name = "web1"
ip = "10.0.0.1"

[[servers]]
name = "web2"
ip = "10.0.0.2"

# Produces: servers = [{name="web1", ip="10.0.0.1"}, {name="web2", ip="10.0.0.2"}]

[[fruits]]
name = "apple"

  [[fruits.varieties]]        # nested array of tables
  name = "red delicious"

  [[fruits.varieties]]
  name = "granny smith"
```

## Dotted Keys

```toml
name.first = "Subbarao"
name.last = "K"

# Equivalent to:
# [name]
# first = "Subbarao"
# last = "K"

physical.color = "orange"
physical.shape = "round"
```

## Comments

```toml
# This is a comment
key = "value"  # inline comment
```

## Common Real-World Examples

### `pyproject.toml` (Python packaging)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "myapp"
version = "1.0.0"
description = "My application"
authors = [
    { name = "Subbarao", email = "you@example.com" }
]
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31",
    "pandas>=2.0",
]

[project.optional-dependencies]
dev = ["pytest", "black", "ruff"]

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### `Cargo.toml` (Rust)

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }

[dev-dependencies]
criterion = "0.5"

[profile.release]
opt-level = 3
lto = true
```

### `poetry` config (alternative Python packaging tool)

```toml
[tool.poetry]
name = "myapp"
version = "0.1.0"
description = ""
authors = ["Subbarao <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Reading/Writing TOML in Python

```python
import tomllib               # built-in, Python 3.11+, READ-ONLY

with open("config.toml", "rb") as f:            # note: must open in binary mode
    data = tomllib.load(f)

data = tomllib.loads(toml_string)

# For writing, or Python < 3.11 reading, use a third-party library
import tomli_w
with open("out.toml", "wb") as f:
    tomli_w.dump(data, f)

# tomlkit preserves comments/formatting on round-trip edits (useful for editing existing files)
import tomlkit
doc = tomlkit.parse(open("config.toml").read())
doc["server"]["port"] = 9090
open("config.toml", "w").write(tomlkit.dumps(doc))
```

## TOML vs YAML vs INI vs JSON

| | TOML | YAML | INI | JSON |
|---|---|---|---|---|
| Native types | Yes (string, int, float, bool, datetime, array, table) | Yes | No — all strings | Yes |
| Comments | Yes (`#`) | Yes (`#`) | Yes (`;` or `#`) | No |
| Nesting | Explicit `[a.b.c]` tables | Indentation-based | Flat sections only | Native `{}` nesting |
| Multi-line strings | Yes (`"""`) | Yes (`\|`, `>`) | Parser-dependent | No (needs `\n` escapes) |
| Ambiguity risk | Low — strict, well-specified | Higher (type coercion surprises, e.g. `NO` → false) | High — no formal spec | Low |
| Common use | `pyproject.toml`, `Cargo.toml`, app config | CI/CD, Kubernetes, Ansible, Docker Compose | Legacy app config, `.gitconfig` | APIs, data interchange |

## Common Gotchas

- Keys defined outside any table must come **before** the first `[table]` header — you can't add loose top-level keys after a table has started.
- A table can only be defined once — redefining `[server]` twice in the same file is an error (unlike INI, which sometimes silently merges or overwrites).
- Dates/times without quotes are parsed as native TOML datetime values, not strings — quote them (`"2026-07-17"`) if you want a literal string.
- Array of tables (`[[name]]`) vs single table (`[name]`) is a common source of confusion — double brackets mean "append a new item to a list of tables under this key."
- Inline tables (`{ key = value }`) must be on a single line — you cannot span an inline table across multiple lines (use a regular `[table]` instead if you need multi-line).
