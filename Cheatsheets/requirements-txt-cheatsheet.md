# requirements.txt Cheatsheet

`requirements.txt` is pip's plain-text dependency list format — no formal spec, but a well-established convention pip itself defines and parses.

## Basic Syntax

```text
# Comments start with a hash
requests
pandas
numpy==1.26.4
```

## Version Specifiers

```text
requests                    # any version (unpinned — risky for reproducibility)
requests==2.31.0                # exact version
requests>=2.31.0                   # minimum version
requests>2.31.0                       # strictly greater than
requests<=2.31.0                         # maximum version
requests<2.31.0                             # strictly less than
requests!=2.30.0                                # exclude a specific version
requests>=2.28,<3.0                                # version range
requests~=2.31.0                                      # compatible release: >=2.31.0, <2.32.0 (locks the minor version)
requests~=2.31                                           # compatible release: >=2.31, <3.0 (locks the major version)
```

**`~=` (compatible release) is the most common choice for applications** — it allows patch-level updates (bug fixes) but blocks anything that might introduce breaking changes.

## Extras

```text
requests[socks]                  # install with an optional extra/feature set
uvicorn[standard]==0.30.0
pandas[excel,parquet]
```

## Environment Markers (conditional installs)

```text
pywin32; platform_system == "Windows"
uvloop; platform_system != "Windows"
dataclasses; python_version < "3.7"
importlib-metadata; python_version < "3.8"

requests==2.31.0; python_version >= "3.8" and python_version < "3.13"
```

**Available markers:** `python_version`, `python_full_version`, `os_name`, `sys_platform`, `platform_system`, `platform_machine`, `implementation_name`.

## Installing From Other Sources

```text
# Git repositories
git+https://github.com/user/repo.git
git+https://github.com/user/repo.git@branch_name
git+https://github.com/user/repo.git@v1.2.0            # specific tag
git+https://github.com/user/repo.git@abc1234               # specific commit hash
git+https://github.com/user/repo.git#egg=mypackage             # explicit package name hint

# Local paths
./local-package/                     # editable-friendly local directory
-e ./local-package/                     # editable install (changes reflect without reinstalling)
file:///absolute/path/to/package

# Direct URLs
https://example.com/mypackage-1.0.0-py3-none-any.whl

# From a different index (private PyPI, artifact repository)
--index-url https://pypi.example.com/simple
--extra-index-url https://pypi.example.com/simple
```

## Including Other Requirements Files

```text
-r base.txt              # include another requirements file
-r requirements-common.txt
-c constraints.txt          # apply version constraints without directly installing (see below)
```

Common pattern for multi-environment projects:

```text
# requirements-base.txt
requests==2.31.0
pandas==2.2.0

# requirements-dev.txt
-r requirements-base.txt
pytest==8.0.0
black==24.1.0
ruff==0.3.0

# requirements-prod.txt
-r requirements-base.txt
gunicorn==22.0.0
```

## Constraints Files (`-c`)

A constraints file pins versions for packages *if* they get installed (e.g., as transitive dependencies), without forcing them to be installed directly — useful for controlling versions across a large dependency tree without listing every top-level package.

```text
# constraints.txt
urllib3<2.0
certifi>=2024.1.1
```

```bash
pip install -r requirements.txt -c constraints.txt
```

## Common pip Commands

```bash
pip install -r requirements.txt
pip install -r requirements.txt --no-deps          # don't auto-resolve/install dependencies
pip install -r requirements.txt --upgrade
pip install --break-system-packages -r requirements.txt   # needed on some modern Debian/Ubuntu-managed Python

pip freeze > requirements.txt                    # snapshot all currently installed packages (exact pins)
pip freeze --local > requirements.txt               # exclude globally-installed packages, venv only

pip list                    # installed packages
pip list --outdated             # what has newer versions available
pip show requests                  # detailed info about an installed package
pip check                             # verify installed packages have compatible dependencies

pip uninstall requests
pip download -r requirements.txt -d ./packages/      # download without installing (offline installs)

pip install --no-cache-dir -r requirements.txt      # skip pip's local cache (useful in Docker builds)
pip install --target ./vendor -r requirements.txt       # install into a specific directory
```

## `pip freeze` vs Hand-Written requirements.txt

| | `pip freeze` output | Hand-written |
|---|---|---|
| Pins | Everything, including transitive deps, at exact versions | Usually just direct/top-level deps |
| Reproducibility | Very high — exact environment snapshot | Depends on how tightly you pin |
| Readability | Poor — hundreds of lines including things you didn't directly choose | Good — shows intent |
| Best used for | Lock files, CI reproducibility, Docker builds | Source of truth for what your project actually depends on |

**Common pattern:** maintain a hand-written `requirements.in` (or just `requirements.txt` with loose/compatible pins) describing direct dependencies, then compile a fully pinned lock file with `pip-tools`.

## pip-tools Workflow (recommended for reproducible builds)

```bash
pip install pip-tools

# requirements.in — your direct, loosely-pinned dependencies
echo "requests>=2.31" >> requirements.in
echo "pandas>=2.2" >> requirements.in

pip-compile requirements.in                # generates a fully pinned requirements.txt
pip-compile --upgrade requirements.in           # regenerate with latest compatible versions
pip-compile --upgrade-package requests requirements.in    # upgrade just one package

pip-sync requirements.txt                     # install EXACTLY what's pinned, removing anything extra
```

## Docker Best Practice

```dockerfile
# Copy requirements first to leverage layer caching — dependencies rarely change as often as source code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
```

## Common Gotchas

- Unpinned dependencies (`requests` with no version) can silently break a deployment when a new major version is released upstream — pin at least a compatible range (`~=`) in anything beyond a quick experiment.
- `pip freeze` output mixes your direct dependencies with every transitive one, making it hard to tell what you actually chose vs what came along for the ride — consider `pipdeptree` to visualize the dependency graph.
- Comments after a package on the same line are NOT supported the way they are in many other formats — put comments on their own line.
- Environment markers use `and`/`or`, not `&&`/`||` — and need to be valid PEP 508 syntax exactly.
- Two requirements files listing conflicting version pins for the same package will cause a resolution error — `-c constraints.txt` is often cleaner than trying to reconcile conflicting `-r` includes.
- `requirements.txt` has no built-in concept of dependency groups (dev vs prod) — that's purely a convention achieved via multiple files and `-r` includes, or by moving to `pyproject.toml` + a tool like Poetry/PDM that has native optional-dependency groups.
