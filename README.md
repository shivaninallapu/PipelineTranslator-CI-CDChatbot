# SDLC Pipeline Skills-Bridge AI Agent

## Overview

The is a chat-based assistant designed for software engineers who work across multiple CI/CD platforms.

When engineers are assigned to projects that use unfamiliar pipeline tools, the agent accelerates the learning curve by allowing users to describe tasks in plain English, paste existing pipeline configurations, and receive translated equivalents for new platforms along with detailed explanations and governance compliance reports.

The agent supports four primary capabilities:

* **Pipeline Translation**
  Convert CI/CD pipelines between tools such as Jenkins, GitHub Actions, Azure DevOps, and Harness. Responses include translated configurations and explanations of mapping decisions.

* **Migration Guidance**
  Generate numbered, step-by-step migration checklists with example code snippets in the syntax of the target platform.

* **Reusable Component Discovery**
  Recommend approved templates, reusable components, and standardized pipeline steps after ingesting organizational repositories or Confluence documentation.

* **Governance Compliance Verification**
  Automatically generate compliance reports that validate required security and quality controls such as:

  * Quality gates
  * Vulnerability scans
  * License checks

---

# Local Development Setup Guide

**Last Updated:** April 7, 2026

## Architecture Overview

The standard deployment uses **Docker Compose** with **LocalAI** as the default local LLM provider.

All services — frontend, backend, and LLM — start with a single command and communicate over a private Docker network.

No external API key is required when using LocalAI.

### Service Topology

| Service           | URL                            | Notes                           |
| ----------------- | ------------------------------ | ------------------------------- |
| Frontend          | `http://localhost:5173`        | React + Vite SPA                |
| Backend API       | `http://localhost:8000`        | FastAPI REST + SSE              |
| Backend Health    | `http://localhost:8000/health` | Returns provider and model info |
| LocalAI           | `http://localai:8080`          | Internal Docker network only    |
| Ollama (optional) | `http://localhost:11434`       | Started with `--profile ollama` |

---

# LLM Provider Options

| Provider          | Env Value | API Key Required | Notes                   |
| ----------------- | --------- | ---------------- | ----------------------- |
| LocalAI (default) | `localai` | No               | Runs locally in Docker  |
| Ollama            | `ollama`  | No               | Optional Docker profile |
| OpenAI            | `openai`  | Yes              | Cloud-based             |
| Gemini            | `gemini`  | Yes              | Cloud-based             |

---

# Prerequisites

Before starting, install the following:

* Docker Desktop 24.x or later (includes Docker Compose v2)
* Git
* Internet access for initial image and model downloads

### Windows Only

Enable the WSL2 backend in Docker Desktop:

1. Open Docker Desktop
2. Navigate to:

   * **Settings → General**
   * Enable **Use the WSL 2 based engine**
3. Navigate to:

   * **Settings → Resources → WSL Integration**
   * Enable your Linux distribution

Verify installation:

```bash
wsl --status
```

---

# Step 1 — Verify Docker Installation

Run the following commands:

```bash
docker --version
docker compose version
docker run --rm hello-world
```

All commands should complete successfully.

---

# Step 2 — Environment Setup

## macOS / Linux

```bash
cp backend/.env.example backend/.env
cp .env.docker.example .env
```

## Windows PowerShell

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item .env.docker.example .env
```

---

# Environment Files

| File           | Purpose                               |
| -------------- | ------------------------------------- |
| `.env`         | Docker Compose service configuration  |
| `backend/.env` | Runtime secrets for backend container |

### Important Environment Variables

| Variable       | Purpose                       |
| -------------- | ----------------------------- |
| `LLM_PROVIDER` | Selected LLM provider         |
| `LLM_MODEL`    | Model name                    |
| `LOCALAI_URL`  | LocalAI endpoint              |
| `OLLAMA_URL`   | Ollama endpoint               |
| `FRONTEND_URL` | Frontend origin               |
| `LLM_API_KEY`  | Required for OpenAI or Gemini |

---

# Default LocalAI Configuration

Default `.env` values:

```env
LLM_PROVIDER=localai
LLM_MODEL=phi-3-mini
LOCALAI_URL=http://localai:8080
```

No API key is required for LocalAI.

---

# Step 3 — LocalAI Model Setup

LocalAI requires:

* A GGUF model file
* A YAML model configuration

## Download Phi-3 Mini

```bash
mkdir -p backend/models

wget https://huggingface.co/TheBloke/Phi-3-mini-4k-instruct-GGUF/resolve/main/phi-3-mini-4k-instruct.Q4_K_M.gguf -P backend/models/
```

---

## Create Model Config

Create:

```text
backend/models/phi-3-mini.yaml
```

Add:

```yaml
name: phi-3-mini
backend: llama-cpp
context_size: 4096

parameters:
  model: phi-3-mini-4k-instruct.Q4_K_M.gguf

template:
  chat: |
    <|user|>
    {{.Input}}<|end|>
    <|assistant|>
```

### Important Notes

* `name` must exactly match `LLM_MODEL`
* `parameters.model` must exactly match the GGUF filename

Otherwise LocalAI returns a **model not found** error.

---

# Optional Providers

## Ollama

Start Ollama:

```bash
docker compose --profile ollama up -d ollama
docker compose exec ollama ollama pull tinyllama
```

Update `.env`:

```env
LLM_PROVIDER=ollama
LLM_MODEL=tinyllama
OLLAMA_URL=http://ollama:11434
```

Recreate backend:

```bash
docker compose up -d --build --force-recreate backend
```

---

## OpenAI

Update `.env`:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
```

Add API key to:

```text
backend/.env
```

```env
LLM_API_KEY=your-openai-api-key
```

Recreate backend afterward.

---

## Gemini

Update `.env`:

```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash-001
```

Add API key to:

```text
backend/.env
```

```env
LLM_API_KEY=your-gemini-api-key
```

Recreate backend afterward.

---

# Step 4 — Start the Platform

```bash
docker compose up -d --build
```

This command:

* Builds frontend and backend containers
* Pulls LocalAI images
* Starts all services

The first build may take several minutes.

---

# Step 5 — Verify Services

## Check Container Status

```bash
docker compose ps
```

## View Backend Logs

```bash
docker compose logs --tail=80 backend
```

## Health Check

```bash
curl http://localhost:8000/health
```

Example response:

```json
{
  "status": "ok",
  "llm_provider": "localai",
  "llm_model": "phi-3-mini",
  "supported_providers": [
    "localai",
    "ollama",
    "openai",
    "gemini"
  ],
  "configured_providers": [
    "localai"
  ]
}
```

---

# Step 6 — Open the Frontend

Navigate to:

```text
http://localhost:5173
```

If the frontend fails to load:

```bash
docker compose logs --tail=80 frontend
```

---

# Step 7 — Verify Chat API

## macOS / Linux

```bash
curl -sS -X POST http://localhost:8000/api/chat/text \
  -H "Content-Type: application/json" \
  -d '{"message":"hello","conversation_history":[]}'
```

Expected result:

* `"status": "success"`
* Non-empty `"message"` field

---

# Step 8 — Fast Mode (Low-Power Machines)

Recommended for laptops running CPU-only LocalAI inference.

Add to `.env`:

```env
FAST_DEV_MODE=true
MAX_CHAT_TOKENS=96
LOCALAI_THREADS=2
```

Apply changes:

```bash
docker compose up -d --build --force-recreate backend
```

---

# Step 9 — Run Tests

## Via Docker

```bash
docker compose --profile test run --rm backend-test
```

## Via Local Virtual Environment

Requires Python 3.11:

```bash
python -m pytest backend/tests
```

---

# Step 10 — Stop the Platform

## Stop Containers

```bash
docker compose down
```

## Remove Volumes and Reset ChromaDB

```bash
docker compose down -v
```

This clears the knowledge base and requires re-ingestion of organizational data.

---

# Troubleshooting

## Backend Still Uses Old Provider

Docker restart does not refresh environment variables.

Always recreate the backend:

```bash
docker compose up -d --build --force-recreate backend
```

---

## OpenAI or Gemini Requests Fail

Verify:

* `LLM_PROVIDER` is correct
* `LLM_MODEL` is valid
* `LLM_API_KEY` exists in `backend/.env`

If dependencies changed:

```bash
docker compose build backend
```

---

## Error Connecting to AI Service

Inspect services:

```bash
docker compose ps
docker compose logs --tail=120 backend
docker compose logs --tail=120 localai
```

---

## LocalAI Is Slow

CPU inference can be resource intensive.

Recommended actions:

* Enable Fast Mode
* Reduce `LOCALAI_THREADS`
* Use a smaller GGUF model

---

## Knowledge Base Responses Are Stale

Force-recreate backend:

```bash
docker compose up -d --build --force-recreate backend
```

If KB content is outdated, re-ingest the repository or Confluence space.

---

## Port Already In Use

Another application may already use ports `5173` or `8000`.

Update `docker-compose.yml`:

```yaml
5174:5173
```

Then update:

```env
FRONTEND_URL=http://localhost:5174
```

