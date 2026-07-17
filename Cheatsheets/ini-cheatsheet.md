# INI Cheatsheet

INI files are simple key-value configuration files organized into `[sections]`. There's no single formal standard — behavior below reflects the common conventions supported by Python's `configparser`, PHP's `parse_ini_file`, and most INI parsers.

## Basic Syntax

```ini
; This is a comment (semicolon style)
# This is also a comment in most parsers (hash style)

[section_name]
key = value
another_key = another value

[database]
host = localhost
port = 5432
name = mydb
user = admin
password = secret

[logging]
level = INFO
format = %(asctime)s %(levelname)s %(message)s
```

## Global / No-Section Keys

```ini
; Some parsers allow keys before any [section] header — global/default scope
debug = true
env = production

[app]
name = myapp
```

## Data Types (all values are strings — parsers/apps interpret them)

```ini
[settings]
string_value = hello world
number_value = 42
float_value = 3.14
bool_true = true            ; also commonly: yes, on, 1
bool_false = false             ; also commonly: no, off, 0
list_value = a,b,c                ; comma-separated — parsing into a list is app-specific, not built into INI
empty_value =
```

**Important:** INI has no native types. Everything parses as a string; converting `"true"` to a boolean or `"42"` to an integer is the responsibility of the code reading the file.

## Multi-line Values

```ini
[section]
key = first line
    continuation line
    another continuation line
; Leading whitespace on subsequent lines marks them as a continuation of the previous key's value
; (supported by configparser and many, but not all, parsers)
```

## Quoting

```ini
[section]
; Many INI parsers do NOT strip quotes automatically — behavior varies
quoted_value = "hello world"        ; some parsers keep the quotes as literal characters
unquoted_value = hello world           ; generally safer/more portable across parsers
```

## Interpolation / Variable Substitution (parser-dependent)

```ini
[paths]
base_dir = /opt/myapp
log_dir = %(base_dir)s/logs           ; Python configparser-style interpolation
data_dir = %(base_dir)s/data

; Not all INI parsers support this — it's a Python configparser feature (BasicInterpolation),
; not part of any universal INI spec.
```

## Duplicate Sections & Keys

```ini
[section]
key = value1

[section]                  ; behavior varies by parser: some merge, some error, some let the last one win
key = value2                  ; duplicate keys: typically last value wins, but not guaranteed across all parsers
```

## Common Real-World Examples

### Python `configparser`

```ini
; config.ini
[DEFAULT]
timeout = 30

[server]
host = 0.0.0.0
port = 8080

[database]
url = postgres://localhost/mydb
timeout = 60          ; overrides DEFAULT for this section only
```

```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

host = config["server"]["host"]
port = config.getint("server", "port")           # typed getters: getint, getfloat, getboolean
timeout = config["database"]["timeout"]              # falls back to DEFAULT if not set locally

config.sections()                                       # list of section names (excludes DEFAULT)
config.has_section("server")
config.has_option("server", "port")

config["server"]["port"] = "9090"                          # modify
with open("config.ini", "w") as f:
    config.write(f)
```

### pip Configuration (`pip.conf` / `pip.ini`)

```ini
[global]
index-url = https://pypi.org/simple
timeout = 60
trusted-host = pypi.org

[install]
no-cache-dir = false
```

### Git Config (`.gitconfig`, INI-like format)

```ini
[user]
    name = Subbarao
    email = you@example.com

[core]
    editor = vim
    autocrlf = input

[alias]
    st = status
    co = checkout

[remote "origin"]
    url = https://github.com/user/repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*
```

### PHP.ini Style

```ini
[PHP]
memory_limit = 256M
max_execution_time = 30
display_errors = Off

[Session]
session.save_path = "/tmp"
```

## Common Gotchas

- No native data types — every value is a string; you must convert manually or use a typed accessor (`getint`, `getboolean` in Python's `configparser`).
- Case sensitivity of section/key names is parser-dependent — Python's `configparser` lowercases keys by default (but not section names) unless configured otherwise.
- Comment character varies: `;` is the classic INI comment marker; `#` is supported by some parsers but not all — check your target tool.
- No standardized way to express nested/hierarchical data — sections are flat; for deeply nested config, YAML, TOML, or JSON are usually better choices.
- Whitespace around `=` is typically trimmed, but behavior can vary slightly by parser — avoid relying on significant leading/trailing spaces in values.
