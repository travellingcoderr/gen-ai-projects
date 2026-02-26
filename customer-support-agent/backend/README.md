# Backend

Python FastAPI backend for `customer-support-agent`.

## Structure

- `app/api/routes`: route handlers (`health`, `search`, `jsonplaceholder`, `llm`, `langgraph`)
- `app/api/schemas`: API schemas
- `app/clients`: external API clients
- `app/services`: business services
- `app/services/llm`: provider abstraction (`base`, `factory`, `openai_provider`, `gemini_provider`)
- `app/orchestration`: orchestration layer
- `app/core`: config, errors, deps, protocols, logging

## Setup (uv)

```bash
cp .env.example .env
uv sync --extra dev
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## AI defaults

- `LLM_PROVIDER`: `openai` or `gemini`
- `LLM_MODEL`: optional override (auto-default per provider)
- `OPENAI_API_KEY` and `GEMINI_API_KEY` available by default in settings
- `GET /api/llm/config` returns the active provider/model configuration
- `POST /api/langgraph/support` runs a LangGraph support pipeline (`categorize -> analyze -> respond`)
