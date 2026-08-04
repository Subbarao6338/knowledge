---
layout: default
title: "Ollama Cheatsheet"
---

# Ollama Cheatsheet

Ollama is a lightweight, extensible framework for running large language models (LLMs) locally on macOS, Linux, and Windows.

---

## 1. Core CLI Command Reference

Execute local models, manage library assets, and control background services using standard terminal operations.

| Command | Description | Example / Usage |
| :--- | :--- | :--- |
| `ollama run <model>` | Pull and run a model, entering interactive mode. | `ollama run llama3` |
| `ollama pull <model>` | Download a model from the registry. | `ollama pull mistral:7b` |
| `ollama push <model>` | Upload a custom model to the registry. | `ollama push username/custom-llama3` |
| `ollama rm <model>` | Remove a local model. | `ollama rm gemma:2b` |
| `ollama list` | List all locally cached models. | `ollama list` |
| `ollama show <model>` | Show configuration/license info for a model. | `ollama show llama3 --parameters` |
| `ollama create <name>` | Build a model from a local Modelfile configuration. | `ollama create mymodel -f ./Modelfile` |
| `ollama cp <src> <dest>` | Clone an existing model to a new local identifier. | `ollama cp llama3 custom-llama3` |

---

## 2. Modelfile Specifications

A `Modelfile` defines the blueprint, layers, parameters, system instructions, and templates for a customized local model.

```dockerfile
# 1. Base model import
FROM llama3

# 2. Set runtime parameters (Sampling, context size, etc.)
PARAMETER temperature 0.3
PARAMETER num_ctx 4096
PARAMETER top_k 40
PARAMETER top_p 0.9

# 3. Define custom system instructions & persona
SYSTEM """
You are a senior DevOps SRE specialist. You answer technical questions with maximum precision.
Include code snippets and security best practices where applicable. Keep responses succinct.
"""

# 4. Set custom prompt template matching LLM token boundaries
TEMPLATE """{% raw %}{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>{% endraw %}"""

# 5. Inject custom stop tokens
PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
```

---

## 3. Local REST API Endpoints

Ollama exposes a high-performance local web server on port `11434` for programmatically generating text completions, chat streams, and embeddings.

### Generate Text Completion
* **Method:** `POST`
* **Path:** `/api/generate`

```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Explain RPO vs RTO in SRE in one sentence.",
  "stream": false
}'
```

*Response Payload:*
```json
{
  "model": "llama3",
  "created_at": "2026-02-14T20:41:22.123Z",
  "response": "RTO (Recovery Time Objective) is the maximum acceptable duration of downtime, while RPO (Recovery Point Objective) is the maximum acceptable amount of data loss measured in time.",
  "done": true
}
```

### Dynamic Chat Conversations
* **Method:** `POST`
* **Path:** `/api/chat`

```bash
curl -X POST http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    { "role": "user", "content": "What is 2+2?" }
  ],
  "stream": false
}'
```

---

## 4. Hardware Profiles & Quantization Reference

Match local hardware resources with the appropriate model size and quantization grade to achieve optimal token generation performance.

| Model Scale | Min VRAM Required | Recommended GPUs | Quantization Standard |
| :--- | :--- | :--- | :--- |
| **1.5B - 3B** | 2 GB - 3 GB | NVIDIA T4, Apple M-series (Base) | Q4_K_M (4-bit Medium) |
| **7B - 8B** | 6 GB - 8 GB | NVIDIA RTX 3060/4060, Apple M-series Pro | Q4_K_M or Q8_0 (8-bit) |
| **13B - 14B** | 10 GB - 12 GB | NVIDIA RTX 4070/4080, Apple M-series Max | Q4_K_M (4-bit) |
| **32B - 34B** | 20 GB - 24 GB | NVIDIA RTX 3090/4090, Apple M3/M4 Max | Q4_K_M or Q5_K_M |
| **70B+** | 40 GB+ | Dual RTX 3090/4090, NVIDIA A100/H100 | Q4_K_M (requires split tensor) |
