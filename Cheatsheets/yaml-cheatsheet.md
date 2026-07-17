# YAML Cheatsheet (.yaml / .yml)

`.yaml` and `.yml` are the same format — just two accepted file extensions. YAML ("YAML Ain't Markup Language") is whitespace-sensitive and a strict superset of JSON in modern parsers.

## Basic Syntax Rules

- Indentation uses **spaces only**, never tabs.
- Indentation level defines nesting (like Python).
- Keys and values are separated by `: ` (colon + space — the space matters).
- Comments start with `#`.
- Document start/end markers: `---` (start), `...` (end) — optional for single documents.

## Scalars (Strings, Numbers, Booleans, Null)

```yaml
string_plain: hello world
string_single: 'single quoted string'
string_double: "double quoted string with \n escapes"
number_int: 42
number_float: 3.14
boolean_true: true         # also: True, yes, on
boolean_false: false          # also: False, no, off
null_value: null                 # also: ~, or just leave blank
empty_value:
explicit_string_number: "123"       # quote to force a number to be treated as a string
```

## Multi-line Strings

```yaml
literal_block: |
  This preserves
  line breaks
  exactly as written.

folded_block: >
  This folds
  line breaks
  into spaces, producing one paragraph.

literal_strip: |-
  No trailing newline at all.

literal_keep: |+
  Keeps all trailing
  blank lines.
```

| Indicator | Meaning |
|---|---|
| `\|` | Literal block — preserves newlines |
| `>` | Folded block — newlines become spaces |
| `-` (suffix) | Strip trailing newline |
| `+` (suffix) | Keep trailing newlines |

## Lists (Sequences)

```yaml
fruits:
  - apple
  - banana
  - cherry

# Inline flow style (JSON-like)
fruits_inline: [apple, banana, cherry]

# List of objects
people:
  - name: Alice
    age: 30
  - name: Bob
    age: 25

# Nested lists
matrix:
  - [1, 2, 3]
  - [4, 5, 6]
```

## Mappings (Dictionaries)

```yaml
person:
  name: Alice
  age: 30
  address:
    city: Berlin
    zip: "10115"

# Inline flow style
person_inline: {name: Alice, age: 30}
```

## Anchors, Aliases & Merge Keys (avoid repetition)

```yaml
defaults: &defaults
  adapter: postgres
  timeout: 30

development:
  <<: *defaults          # merge key — inherits all defaults
  database: dev_db

production:
  <<: *defaults
  database: prod_db
  timeout: 60              # overrides the merged value

# Anchors on scalars/lists too
common_tags: &tags
  - env
  - team

service_a:
  tags: *tags
```

## Multiple Documents in One File

```yaml
---
name: doc1
value: 1
---
name: doc2
value: 2
```

## Type Coercion Gotchas

```yaml
version: 1.0          # parsed as a FLOAT, not a string — quote it if you need "1.0" literally
country_code: NO       # WARNING: parsed as boolean `false` in YAML 1.1 (Norway's code!) — quote it: "NO"
zip_code: 00501           # parsed as a string automatically since it has a leading zero (in most parsers)
enabled: yes                # parsed as boolean true
port: "8080"                    # quote when the field must remain a string, even though it looks numeric
```

**Rule of thumb:** quote any scalar that could be misread as a number, boolean, or null — especially country codes, version-like strings, and zip codes.

## Environment Variable Substitution (tool-dependent, not native YAML)

```yaml
# Docker Compose style
image: myapp:${TAG:-latest}

# GitHub Actions style
env:
  MY_VAR: ${{ secrets.MY_SECRET }}

# Plain YAML has NO built-in variable substitution —
# this is a feature of the specific tool consuming the YAML (Compose, Helm, CI systems, etc.)
```

## Common Real-World Examples

### GitHub Actions Workflow

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
```

### Kubernetes Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:latest
          ports:
            - containerPort: 8080
          env:
            - name: ENV
              value: production
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
```

### Ansible Playbook

```yaml
- name: Configure web servers
  hosts: webservers
  become: true
  vars:
    http_port: 80
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: true
```

## Python: Reading/Writing YAML

```python
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)           # always use safe_load, not load (security)

with open("out.yaml", "w") as f:
    yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

# Multiple documents
docs = list(yaml.safe_load_all(open("multi.yaml")))
```

## Validating YAML

```bash
python -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" config.yaml
yamllint config.yaml                # dedicated linter, catches style + syntax issues
```

## Common Gotchas

- Tabs are illegal for indentation — many cryptic parse errors trace back to a stray tab character.
- Trailing whitespace after `:` before a value can cause unexpected parsing in some parsers — be consistent with exactly one space.
- `on`, `off`, `yes`, `no`, `true`, `false` (in any case) are booleans in YAML 1.1 — quote them if you want the literal string.
- Colons inside unquoted string values need care: `time: 10:30` can confuse a parser — quote it: `time: "10:30"`.
- Indentation must be consistent within a block — mixing 2 and 4 spaces at the same level breaks parsing.
- Duplicate keys in a mapping are often silently allowed by parsers (last one wins) rather than raising an error — a linter will catch this, plain parsing may not.
