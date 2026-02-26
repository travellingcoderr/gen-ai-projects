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

## Why MCP Here?
MCP (Model Context Protocol) is a standard way for agents to call external tools/services.

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
