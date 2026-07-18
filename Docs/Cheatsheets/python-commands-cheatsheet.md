# Python Commands Cheatsheet (CLI, Interpreter, pip, venv)

This covers the `python` executable itself, package management, and environment tooling — for language syntax, see the separate Python language cheatsheet.

## Running Python

```bash
python script.py                    # run a script
python3 script.py                       # explicit Python 3 (some systems still alias python -> Python 2)
python -                            # read script from stdin
python -c "print('hello')"             # run an inline command
python -m module_name                     # run a module as a script (uses sys.path properly)
python -m http.server 8000                   # quick local web server
python -m json.tool file.json                   # pretty-print JSON from the CLI
python -m venv myenv                               # create a virtual environment
python -m pip install package                         # run pip via the module (avoids PATH issues)

python                    # interactive REPL
python -i script.py          # run script, then drop into interactive mode with its namespace
python -O script.py             # optimized mode (strips assert statements, __debug__ = False)
python -OO script.py                # also strips docstrings
```

## Interpreter Flags

```bash
python -V                    # version
python --version
python -h                       # help
python -u script.py                # unbuffered stdout/stderr (useful for real-time log streaming, e.g. Docker/Cloud Run)
python -B script.py                   # don't write .pyc files
python -E script.py                      # ignore PYTHON* environment variables
python -s script.py                         # don't add user site-packages to sys.path
python -W ignore script.py                     # suppress warnings
python -W error script.py                         # turn warnings into errors
python -X dev script.py                              # enable development mode (extra runtime checks)
python -X importtime script.py                          # profile import time — great for diagnosing slow startup

python -m pdb script.py          # run under the debugger from the start
python -m cProfile script.py         # profile the script
python -m cProfile -o out.prof script.py    # save profile output for later analysis (e.g. snakeviz)
python -m timeit "sum(range(100))"             # time a single expression from the CLI
python -m py_compile script.py                    # compile to bytecode without running
python -m trace --trace script.py                    # trace every executed line
```

## Getting Info

```bash
python -c "import sys; print(sys.path)"          # module search path
python -c "import sys; print(sys.executable)"        # which interpreter is actually running
python -c "import sys; print(sys.version)"
python -c "import platform; print(platform.python_version())"
python -c "help('modules')"                              # list all installed modules (slow)
python -m site                                               # site-packages locations, sys.path

which python              # (Linux/Mac) which interpreter PATH resolves to
where python                 # (Windows) same
python -c "import os; print(os.getcwd())"
```

## pip — Package Management

```bash
pip install package
pip install package==1.2.3
pip install "package>=1.2,<2.0"
pip install --upgrade package
pip install --upgrade pip
pip uninstall package

pip install -r requirements.txt        # see the dedicated requirements.txt cheatsheet for format details
pip install -e .                          # editable install of the current project (from pyproject.toml/setup.py)
pip install -e ".[dev]"                      # editable install with an optional extras group

pip list                    # installed packages
pip list --outdated             # what has newer versions available
pip show package                   # detailed metadata about an installed package
pip freeze                            # exact installed versions, pip-freeze format
pip check                                # verify dependency compatibility across installed packages

pip download package -d ./pkgs        # download without installing
pip install --no-index --find-links=./pkgs package    # install from local files, no network

pip cache list
pip cache purge
pip config list
pip install --break-system-packages package   # needed on some modern Debian/Ubuntu externally-managed environments

pip install --index-url https://pypi.example.com/simple package    # custom package index
pip install --proxy http://proxy.example.com:8080 package             # through a proxy
```

## Virtual Environments

```bash
python -m venv myenv                   # create
source myenv/bin/activate                 # activate (Linux/Mac)
myenv\Scripts\activate                       # activate (Windows cmd)
myenv\Scripts\Activate.ps1                      # activate (Windows PowerShell)
deactivate                                         # exit the venv

python -m venv myenv --system-site-packages     # inherit globally installed packages
python -m venv myenv --clear                       # wipe and recreate
python -m venv myenv --upgrade                         # upgrade venv's bundled pip/setuptools to match interpreter

# Check whether you're in a venv
python -c "import sys; print(sys.prefix != sys.base_prefix)"
echo $VIRTUAL_ENV                # set while a venv is activated
```

## uv (modern, fast alternative to venv/pip)

```bash
pip install uv

uv venv                       # create a virtual environment (defaults to .venv)
uv venv --python 3.12            # specify Python version

uv pip install package             # much faster than pip
uv pip install -r requirements.txt
uv pip freeze
uv pip sync requirements.txt          # install exactly what's pinned, removing extras

uv run script.py                 # run a script inside the project's environment automatically
uv add package                      # add + install a dependency, updates pyproject.toml
uv lock                                # generate a lock file
```

## pipx (isolated CLI tool installs)

```bash
pip install pipx
pipx install black             # installs `black` into its own isolated venv, exposes the CLI globally
pipx list
pipx upgrade black
pipx uninstall black
pipx run black --check .          # run a tool once without installing it permanently
```

## Package/Project Management (pyproject.toml era)

```bash
pip install build
python -m build                  # build sdist + wheel from pyproject.toml

pip install twine
twine upload dist/*                 # publish to PyPI
twine upload --repository testpypi dist/*   # publish to TestPyPI

# Poetry (alternative full-featured tool)
poetry init
poetry add requests
poetry add --group dev pytest
poetry install
poetry run python script.py
poetry build
poetry publish
poetry shell                  # activate the managed virtual environment

# pipenv (another alternative)
pipenv install requests
pipenv install --dev pytest
pipenv shell
pipenv run python script.py
pipenv lock
```

## Version Management (multiple Python versions)

```bash
# pyenv (Linux/Mac)
pyenv install 3.12.3
pyenv versions
pyenv global 3.12.3            # set default globally
pyenv local 3.11.8                # set version for current directory (writes .python-version)
pyenv shell 3.10.13                  # set version for current shell session only
pyenv which python

# On Windows: py launcher (bundled with the official installer)
py -3.12 script.py
py -3.11 -m venv myenv
py --list                    # list installed Python versions
py -0                           # same, shorter alias
```

## Linting, Formatting, Type Checking (CLI usage)

```bash
pip install black ruff mypy isort

black .                    # auto-format code
black --check .               # check without modifying (CI-friendly)
black --diff .                   # show what would change

ruff check .                 # lint (fast, replaces flake8 + many plugins)
ruff check --fix .              # auto-fix issues
ruff format .                      # ruff also has a formatter (Black-compatible)

isort .                    # sort imports
mypy script.py                # static type checking
mypy --strict script.py          # stricter checks

pytest                    # run tests
pytest -v                    # verbose
pytest -k "test_name"           # run tests matching a keyword
pytest --cov=mypackage             # coverage report (needs pytest-cov)
pytest -x                             # stop at first failure
pytest --lf                              # rerun only last-failed tests
```

## Common Environment Variables

```bash
PYTHONPATH=/extra/module/dir       # additional module search paths
PYTHONDONTWRITEBYTECODE=1             # skip writing .pyc files
PYTHONUNBUFFERED=1                       # unbuffered stdout/stderr (common in Docker/Cloud Run configs)
PYTHONWARNINGS=ignore                       # suppress warnings
PYTHONHASHSEED=0                               # deterministic hash seed (useful for reproducible tests)
PIP_NO_CACHE_DIR=1                                # disable pip's cache (common in Docker builds to shrink layers)
PIP_INDEX_URL=https://pypi.example.com/simple        # custom default package index
VIRTUAL_ENV                                              # set automatically when a venv is activated
```

## Common Gotchas

- `python` vs `python3` — on many Linux distros and macOS, `python` may not exist or may point to Python 2; use `python3` explicitly, or check with `python --version` first.
- `pip install` without an active virtual environment installs globally (or fails on "externally managed" systems, requiring `--break-system-packages` or a venv) — always activate a venv first for project work.
- `python -m pip` is more reliable than bare `pip` when multiple Python installations exist, since it guarantees you're using the pip tied to that specific interpreter.
- Mixing `pip install --user` and virtual environments can cause confusing precedence issues — avoid `--user` installs when working inside a venv.
- `pip freeze` captures the exact environment, including transitive dependencies — good for lockfiles, not ideal as a hand-maintained source of truth (see the `requirements.txt` cheatsheet for the pip-tools workflow).
