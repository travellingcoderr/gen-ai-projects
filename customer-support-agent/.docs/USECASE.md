# Customer Support Agent Use Case

## Overview
This project implements a customer support assistant that can classify incoming support queries, analyze urgency/context, and generate a response using a LangGraph workflow.

The use case modeled here follows the reference customer-support-agent pattern (categorize -> analyze -> respond), adapted into this FastAPI codebase with production-friendly behavior.

## Business Problem
Support teams receive mixed queries (billing, technical, account, orders, general) with different urgency levels. Manual triage is slow and inconsistent. The goal is to automate first-pass triage and response drafting while preserving reliability in local/dev environments.

## Solution Design
The backend exposes a LangGraph-powered API endpoint:

- `POST /api/langgraph/support`

The graph runs three nodes in sequence:

1. `categorize`
2. `analyze`
3. `respond`

### Hybrid Inference Strategy (Important)
To balance intelligence and reliability:

- If LLM credentials and provider SDK are available, node logic uses LLM inference.
- If credentials/SDK are missing (or an LLM call fails), the same nodes fall back to deterministic rules.

This means the endpoint works in all environments:

- Fully configured environments: richer semantic outputs.
- Local/dev without keys: deterministic, stable outputs.

## LangGraph Workflow
State model (`SupportState`) fields:

- `query`
- `category`
- `analysis`
- `response`

Execution:

- Entry -> `categorize`
- `categorize` -> `analyze`
- `analyze` -> `respond`
- `respond` -> END

The API response returns final state values.

## API Contract
Request model supports:

- Preferred: `query`
- Backward-compatible legacy field: `message`

Response model:

- `query`
- `category`
- `analysis`
- `response`

Example request:

```json
{
  "query": "I need a refund for a double charge"
}
```

Example response (shape):

```json
{
  "query": "I need a refund for a double charge",
  "category": "billing",
  "analysis": "...",
  "response": "..."
}
```

## Routing/Categorization Semantics
Categories currently supported:

- `billing`
- `technical`
- `account`
- `orders`
- `general`

When fallback rules are active, keyword heuristics are used to assign categories and urgency-aware analysis.

## Developer Experience
### API docs (Swagger)
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`
- `http://localhost:8000/openapi.json`

### Run backend locally
```bash
cd backend
uv sync --extra dev
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run with Docker
```bash
docker compose up --build
```

## Testing
LangGraph API behavior is covered in:

- `backend/tests/test_langgraph_support.py`

Test coverage validates:

- billing categorization flow
- technical categorization flow
- backward compatibility for legacy `message` request field

## Notes on Project Hygiene
The repo is configured to ignore runtime-generated artifacts:

- Python cache files (`__pycache__`, `*.pyc`)
- packaging metadata (`*.egg-info`)

`backend/uv.lock` is intentionally kept versioned for reproducible dependency resolution.

## Summary
This implementation keeps the reference workflow intent (LLM-based customer support automation with LangGraph) while adding practical backend safeguards:

- stable API contract
- fallback behavior without API keys
- deterministic behavior for local/dev
- clean FastAPI integration and docs
