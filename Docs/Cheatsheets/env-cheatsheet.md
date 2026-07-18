<!-- {% raw %} -->
# .env Cheatsheet

`.env` files store key-value environment variables for local development and deployment configuration. There's no single official spec — behavior below reflects the widely-adopted convention popularized by the Node `dotenv` package and followed by most language ecosystems (`python-dotenv`, Ruby's `dotenv`, PHP's `vlucas/phpdotenv`, Docker Compose, etc.).

## Basic Syntax

```dotenv
# Comments start with a hash
KEY=value
DATABASE_URL=postgres://user:pass@localhost:5432/mydb
DEBUG=true
PORT=8080

# No spaces around the = sign (spaces are usually NOT stripped and can break the value)
CORRECT=value
# WRONG=  value      <- leading space becomes part of the value in strict parsers
```

## Quoting

```dotenv
UNQUOTED=hello world              # works in most parsers, but risky with special chars
SINGLE_QUOTED='hello world'          # literal — no variable expansion or escape sequences processed
DOUBLE_QUOTED="hello world"             # allows escape sequences like \n, and variable expansion in some tools

MULTILINE="line one\nline two"             # \n is interpreted as a newline in double-quoted values (dotenv-specific)

JSON_VALUE='{"key": "value", "nested": {"a": 1}}'    # quote JSON to keep it as one value

EMPTY_VALUE=
EXPLICIT_EMPTY=""
```

## Variable Expansion (supported by many, not all, parsers)

```dotenv
BASE_URL=https://api.example.com
FULL_URL=${BASE_URL}/v1/users          # expands to https://api.example.com/v1/users

# Some tools require this syntax instead:
FULL_URL=$BASE_URL/v1/users

# Order matters — a variable must be defined earlier in the file (or already in the environment) to be expanded
```

**Note:** plain `dotenv`-style loaders in some languages do NOT expand variables by default — check your specific library (e.g., Python's `python-dotenv` needs `interpolate=True`; Node's `dotenv` needs the separate `dotenv-expand` package).

## Common Patterns

```dotenv
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=admin
DB_PASSWORD=secret

# API keys / secrets
API_KEY=sk-xxxxxxxxxxxxx
JWT_SECRET=your-secret-key
STRIPE_SECRET_KEY=sk_test_xxxx

# App config
NODE_ENV=development          # or: production, test, staging
DEBUG=true
LOG_LEVEL=info
PORT=3000
HOST=0.0.0.0

# Cloud credentials (local dev only — prefer IAM roles/managed identity in production)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=eu-central-1
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json

# Proxy settings
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080
NO_PROXY=localhost,127.0.0.1,.internal.domain
```

## Multiple Environment Files (common convention)

```text
.env                  # default, loaded in all environments
.env.local              # local overrides, git-ignored, loaded everywhere except test
.env.development           # loaded only in development
.env.production               # loaded only in production
.env.test                        # loaded only in test
.env.example                        # committed to git as a template — NO real secrets, just key names
```

**Typical precedence (framework-dependent, e.g. Next.js/Vite pattern):** `.env.{environment}.local` > `.env.{environment}` > `.env.local` > `.env` (most specific wins).

## Loading .env Files by Language

```python
# Python — python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()                          # loads .env from current directory
load_dotenv(dotenv_path=".env.production")
load_dotenv(override=True)                # override existing OS env vars

api_key = os.getenv("API_KEY")
api_key = os.environ["API_KEY"]              # raises KeyError if missing
```

```javascript
// Node.js — dotenv
require('dotenv').config();
// or ESM:
import 'dotenv/config';

const apiKey = process.env.API_KEY;
```

```bash
# Bash — source it directly (exports every KEY=value as an env var)
set -a               # auto-export all variables that follow
source .env
set +a

# Or, one-liner export loop
export $(grep -v '^#' .env | xargs)
```

```yaml
# Docker Compose — reads .env automatically for variable substitution in compose.yml,
# and env_file: loads variables INTO a container
services:
  app:
    env_file:
      - .env
```

```dockerfile
# Dockerfile — NOT auto-loaded; pass explicitly at build/run time
# docker run --env-file .env myimage
```

## Security Best Practices

```gitignore
# .gitignore — ALWAYS exclude real .env files from version control
.env
.env.local
.env.*.local
*.env
!.env.example
```

- **Never commit real secrets** — commit `.env.example` with placeholder keys only (`API_KEY=your_api_key_here`).
- Rotate any secret that was accidentally committed — removing it from a later commit does NOT remove it from git history.
- In production, prefer a secrets manager (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, HashiCorp Vault) or platform-injected environment variables over shipping a `.env` file to servers.
- Use different values per environment — never reuse production secrets in `.env.development`.
- Be cautious with `.env` files inside Docker images — a `COPY . .` step can accidentally bake secrets into an image layer; use `.dockerignore` to exclude `.env`.

```dockerignore
# .dockerignore
.env
.env.*
!.env.example
```

## Validation Pattern (recommended for larger apps)

```python
# Fail fast if required env vars are missing, rather than failing deep in application logic
import os

REQUIRED_VARS = ["DATABASE_URL", "API_KEY", "JWT_SECRET"]
missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {missing}")
```

## Common Gotchas

- Trailing whitespace or accidental spaces around `=` can silently become part of the value in strict parsers.
- Values are NOT automatically type-cast — `PORT=8080` loads as the *string* `"8080"`, not an integer; cast explicitly in code.
- Boolean-looking values (`DEBUG=false`) are also strings — `if os.getenv("DEBUG"):` is truthy even when the string is `"false"`; compare explicitly: `os.getenv("DEBUG") == "true"`.
- Comments must start at the beginning of a line or after whitespace — a `#` inside an unquoted value may be treated as the start of a comment, truncating the value.
- `.env` files loaded via `source` in bash need properly quoted values if they contain spaces or special shell characters, since bash will interpret them.

<!-- {% endraw %} -->
