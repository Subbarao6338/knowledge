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
