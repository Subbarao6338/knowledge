---
layout: default
title: "FinOps, DevOps & Azure DevOps Cheatsheet"
---

# FinOps, DevOps & Azure DevOps Cheatsheet

## FinOps Framework Phases

FinOps is an operational framework and cultural practice that enables organizations to maximize business value by helping engineering, finance, and business teams collaborate on data-driven spending decisions.

```text
       INFORM (Visibility, Allocations, Budgets)
          |
       OPTIMIZE (Rate Reductions, Sizing, Waste)
          |
       OPERATE (Continuous Control, Alignment)
```

1. **Inform:** Give engineers and finance teams visibility into cloud spend. Allocate costs via tags, resources, and subscriptions.
2. **Optimize:** Right-size virtual machines, apply Committed Use Discounts (CUDs/RIs), and configure automated lifecycle cleanups.
3. **Operate:** Establish continuous governing policies to ensure cost management aligns with business goals.

---

## DevOps Principles (The Three Ways)

DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the systems development life cycle and provide continuous delivery with high software quality.

- **First Way (Flow):** Maximize downstream flow (from left to right, Dev to Ops) by making work visible, limiting Work In Progress (WIP), and building automated testing/build pipelines.
- **Second Way (Feedback):** Create and accelerate feedback loops (right to left) to catch and fix bugs early (Shift-Left Testing, production APM monitoring).
- **Third Way (Continuous Learning):** Cultivate a generative, high-trust culture that encourages experimentation, risk-taking, and learning from failure (blameless post-mortems).

---

## Azure DevOps CI/CD Pipelines

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'

stages:
- stage: BuildAndTest
  jobs:
  - job: TestPythonApp
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.12'
    - script: |
        pip install pytest
        PYTHONPATH=. pytest
      displayName: 'Run PyTest Suite'
```
