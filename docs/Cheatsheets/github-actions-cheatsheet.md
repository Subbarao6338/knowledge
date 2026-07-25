# GitHub Actions CI/CD Cheatsheet

A complete reference for automating workflows, building continuous integration/delivery pipelines, and configuring secure deployment environments on GitHub.

---

## 1. Core Concepts

GitHub Actions organizes automation into **Workflows**, triggered by events.

- **Workflow:** The overall YAML configuration file stored inside `.github/workflows/`.
- **Event:** A specific activity that triggers a workflow run (e.g. `push`, `pull_request`).
- **Job:** A set of steps that execute on the same runner machine. Jobs run in parallel by default.
- **Step:** An individual task that can run commands or use custom Actions. Steps execute sequentially.
- **Action:** Pre-packaged reusable code steps (e.g., checkout repository, install python).

---

## 2. Basic Workflow Anatomy

```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Test Suite
        run: npm test
```

---

## 3. Workflow Triggers (`on:`)

Workflows can be scheduled, manual, or reaction-based:

```yaml
on:
  # Trigger on push or pull requests
  push:
    branches: [ main ]
    paths:
      - 'src/**'            # Only run if files in src/ change
      - '!docs/**'           # Ignore markdown documentation changes

  # Scheduled run (Cron syntax: Min, Hour, Day-of-month, Month, Day-of-week)
  schedule:
    - cron: '0 4 * * 1'      # Every Monday at 4:00 AM UTC

  # Manual trigger with custom form inputs in the GitHub UI
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

---

## 4. Contexts, Variables, and Secrets

Always store keys and sensitive database connection strings in **Encrypted Secrets**.

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    # Bind to a GitHub environment for protection rules and distinct secrets
    environment: production

    steps:
      - name: Echo environment variables
        run: |
          echo "Run ID: ${{ github.run_id }}"
          echo "Triggered by: ${{ github.actor }}"
        env:
          MY_VAR: "Hello-World"

      - name: Deploy to Cloud
        run: ./deploy.sh
        env:
          # Pull from repository secrets
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## 5. Job Orchestration & Matrices

By default, jobs run in parallel. Use `needs` to configure sequential pipelines.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building..."

  test:
    runs-on: ubuntu-latest
    needs: build # Wait for build to complete successfully
    steps:
      - run: echo "Testing..."

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test] # Wait for both to pass
    steps:
      - run: echo "Deploying..."
```

### Build Matrix
Run a job across multiple operating systems and interpreter versions simultaneously:

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false # Don't cancel others if one version fails
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

---

## 6. Step Conditionals & Special Contexts

Filter execution using the `if` parameter.

```yaml
steps:
  # Runs only on push to main branch
  - name: Build Production Assets
    if: github.ref == 'refs/heads/main'
    run: npm run build

  # Runs always, even if preceding steps failed (useful for cleanup/logs)
  - name: Upload Logs
    if: always()
    uses: actions/upload-artifact@v4
    with:
      name: system-logs
      path: logs/
```

- `success()`: True only if no preceding steps failed.
- `failure()`: True if any preceding step in the job failed.
- `cancelled()`: True if the workflow run has been cancelled.
- `always()`: Always executes, ignoring all failures.

---

## 7. Caching dependencies

Speeds up workflow jobs by retrieving pre-built files (e.g. `node_modules`, `pip` cache).

```yaml
- name: Cache Pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    # Cache key changes whenever requirements.txt is updated
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```
- **`path`:** The directory to cache on disk.
- **`key`:** The exact identifier for storing/retrieving the cache.
- **`restore-keys`:** Fallback prefix matchers if no exact cache hit occurs.
