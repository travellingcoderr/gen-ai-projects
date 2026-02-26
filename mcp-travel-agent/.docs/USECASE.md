# MCP Travel Agent Use Case

## What This Project Does (Simple Version)
You type: "Plan my trip."
The system breaks that big job into smaller jobs and gives each job to a specialist agent.

Think of it like a travel company desk:

- One person understands your request.
- One person picks destinations.
- One person checks flights.
- One person checks hotels.
- One person builds day-by-day plan.
- One person writes the final summary.

That is the core multi-agent idea.

---

## What is MCP?

**MCP (Model Context Protocol)** is an open standard introduced by Anthropic that defines how AI models (LLMs) communicate with external tools, data sources, and services in a structured, uniform way.

Think of it as a **universal plug** between an AI agent and the outside world.

### The Problem MCP Solves

Before MCP, every team that wanted their AI to "call a tool" had to invent their own integration:
- Custom function signatures
- Custom JSON schemas
- Custom error formats
- Custom auth patterns

This meant: **N tools × M models = N×M custom integrations**.

MCP standardises this to a single protocol. Every tool exposes the same interface. Every model speaks the same language. The equation becomes **N + M**.

### MCP vs REST API — What's The Difference?

| | REST API | MCP |
|---|---|---|
| **Designed for** | Human developers calling services from code | AI models discovering and calling tools at runtime |
| **Discovery** | Manual — you read docs, write client code | Automatic — the model asks "what tools do you have?" and gets a machine-readable answer |
| **Schema** | OpenAPI/Swagger (designed for human reading) | JSON Schema embedded in the protocol (designed for LLM consumption) |
| **Caller** | A developer's application | An LLM agent deciding autonomously which tool to invoke |
| **Invocation** | Hardcoded in application logic | Chosen dynamically by the model based on context |
| **Statefulness** | Stateless by default | Supports stateful sessions (the model can maintain tool context across turns) |
| **Error handling** | HTTP status codes (4xx/5xx) | Structured error types the model can reason about and retry |

In short: **a REST API is built for code to call; MCP is built for an LLM to call**.

### How MCP Works

```
User prompt
    │
    ▼
LLM (e.g. Claude, GPT)
    │  "I need flight data. I'll call the `search_flights` tool."
    ▼
MCP Client (inside your agent)
    │  Sends a structured tool-call request
    ▼
MCP Server (your tool/service)
    │  Executes the tool, returns structured result
    ▼
LLM receives result, continues reasoning
    │
    ▼
Final response to user
```

An MCP server exposes three things the model can use:
- **Tools** — callable functions (e.g. `search_flights`, `get_hotels`)
- **Resources** — readable data (e.g. a file, a database record)
- **Prompts** — reusable prompt templates the model can invoke

### Why MCP Matters for Agentic Systems

In a multi-agent system like this one, agents need to call external services to do real work. MCP gives you:

1. **Composability** — swap one MCP server for another without changing agent code
2. **Discoverability** — agents can list available tools at runtime, no hardcoding
3. **Interoperability** — any MCP-compliant model works with any MCP-compliant server
4. **Safety** — the protocol supports permission scoping, so agents only access what they are allowed to

---

## Why MCP Here?

In this codebase, `MCPTravelTools` is the tool adapter layer. Right now it uses mock data so the project runs immediately. Later, you can replace those methods with real MCP server calls for:

- flight search
- hotel search
- destination activities/guide

## Workflow
`POST /api/travel/plan` triggers this pipeline:

1. `intake_agent` -> collects assumptions and validates context
2. `destination_agent` -> suggests candidate destinations
3. `flights_agent` -> fetches flight options via MCP tool adapter
4. `hotels_agent` -> fetches hotel options via MCP tool adapter
5. `itinerary_agent` -> creates day-wise plan
6. `summary_agent` -> creates final readable answer

Orchestration is handled by `TravelWorkflowService`.

- If `langgraph` is installed, it runs through a LangGraph state machine.
- If not, it runs the same steps sequentially (fallback mode).

## API Contract
Request fields:

- `query` (required)
- `origin` (optional, default `New York`)
- `days` (optional, default `4`)
- `budget_usd` (optional, default `2000`)
- `travelers` (optional, default `1`)
- `interests` (optional)

Response fields:

- `summary`
- `selected_destination`
- `destination_options`
- `flight_options`
- `hotel_options`
- `itinerary`
- `assumptions`

## How To Read The Codebase Quickly
Entry point:

- `backend/app/api/routes/travel.py`

Orchestration:

- `backend/app/orchestration/travel_orchestrator.py`
- `backend/app/services/travel/travel_workflow_service.py`

Agent modules:

- `backend/app/services/travel/agents/*.py`

Tool adapters:

- `backend/app/services/travel/mcp_tools.py`

Schemas:

- `backend/app/api/schemas/travel.py`

## What To Do Next For Real MCP
1. Replace `MCPTravelTools` mock methods with real MCP client calls.
2. Add auth/config for MCP endpoints in `core/config.py`.
3. Add error handling + retries per tool.
4. Add integration tests with mocked MCP server responses.
