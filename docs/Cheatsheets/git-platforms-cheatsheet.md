---
layout: default
title: "Git Platforms Cheatsheet"
---

# Git Platforms Cheatsheet

## GitHub Actions CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Build & Deploy Container

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test_and_build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Setup Python Runtime
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Run Tests
        run: |
          pip install pytest
          PYTHONPATH=. pytest

      - name: Build and Push Docker Image
        if: github.event_name == 'push'
        run: |
          docker build -t myapp:latest .
          # Run registry push here...
```

---

## GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - deploy

run_unit_tests:
  stage: test
  image: python:3.12-slim
  script:
    - pip install pytest
    - PYTHONPATH=. pytest

deploy_to_production:
  stage: deploy
  image: alpine:latest
  only:
    - main
  script:
    - echo "Deploying container application safely to cloud registry..."
```

---

## Bitbucket Pipelines Reference

Bitbucket Pipelines is integrated directly inside Bitbucket, configured via a single YAML file located at the root of the repository.

```yaml
# bitbucket-pipelines.yml
image: python:3.12-slim

pipelines:
  default:
    - step:
        name: Build and Run Quality Checks
        caches:
          - pip
        script:
          - pip install pytest
          - PYTHONPATH=. pytest
  branches:
    main:
      - step:
          name: Test Execution
          script:
            - pip install pytest
            - PYTHONPATH=. pytest
      - step:
          name: Cloud Deployment
          deployment: production
          trigger: manual # Require manual click in UI to deploy
          script:
            - echo "Executing production deployment script..."
```

---

## Platform Comparison: Features & Syntax

| Feature | GitHub | GitLab | Bitbucket |
| :--- | :--- | :--- | :--- |
| **Config File** | `.github/workflows/*.yml` | `.gitlab-ci.yml` | `bitbucket-pipelines.yml` |
| **Container Engine** | Runner VM (Docker inside) | Docker Runner | Shared Docker Containers |
| **Marketplace** | GitHub Actions Marketplace | Native Templates / Custom Includes | Bitbucket Pipes |
| **Matrix Builds** | Supported (`strategy.matrix`) | Supported (`parallel.matrix`) | Supported (`parallel`) |
| **Secrets Store** | Repository / Org Secrets | CI/CD Variables | Repository Variables |

---

## Webhooks Setup & Security

Webhooks allow external services to be notified of repository events in real time (such as push, pull request, release).

### GitHub Webhook Payload Verification (Python Flask Example)
```python
import hmac
import hashlib
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = b"my_super_secure_webhook_secret_key"

@app.route("/webhook", methods=["POST"])
def github_webhook():
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        abort(400, "Missing signature")

    # Verify signature
    sha_name, signature_val = signature.split("=")
    mac = hmac.new(WEBHOOK_SECRET, request.data, hashlib.sha256)
    if not hmac.compare_digest(mac.hexdigest(), signature_val):
        abort(403, "Invalid webhook signature")

    # Process payload
    payload = request.json
    print(f"Received push event from repository: {payload['repository']['name']}")
    return "OK", 200
```

---

## Pull Request & Merge Request Automations

### GitHub: Pull Request Template
Put this in `.github/pull_request_template.md` to format developer contributions.

```markdown
## Description
Describe the changes introduced in this PR.

## Checklist
- [ ] My code follows the code style guide.
- [ ] I have written unit tests for my changes.
- [ ] All tests pass locally.

## Related Issues
Closes #
```

### GitLab: Merge Request Template
Put this in `.gitlab/merge_request_templates/default.md`.

```markdown
## What does this MR do?
Summary of the modifications.

## Verification Checklist
- [ ] Verified on local environment.
- [ ] Checked coverage reports.
```
