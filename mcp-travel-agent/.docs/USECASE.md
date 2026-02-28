# MCP Travel Agent Use Case

## What This Project Does
This project now mirrors the reference travel-agent structure more closely.

You give the system one travel request in plain English, for example:

- "Search for top Airbnb-style stays in Coorg"
- "I need WiFi, 2 bedrooms, and a moderate budget"
- "I am flying from Delhi"

The backend then breaks that request into specialist jobs.

## Layman Explanation
Think of this as a small travel operations team:

1. `parser_agent`
   - Reads your messy travel request
   - Pulls out destination, origin, budget, trip length, and interests

2. `property_agent`
   - Acts like the accommodation researcher
   - Uses Airbnb-style tools to fetch stay options

3. `flight_agent`
   - Acts like the flight desk
   - Uses flight tools to fetch travel options

4. `analysis_agent`
   - Acts like the decision maker
   - Scores the properties and writes pros/cons

5. `orchestrator_agent`
   - Acts like the final travel consultant
   - Combines everything into one clean answer

That is the multi-agent pattern in simple terms.

## Current Code Structure
```text
backend/app/services/travel/
├── agents/
│   ├── parser_agent.py
│   ├── property_agent.py
│   ├── flight_agent.py
│   ├── analysis_agent.py
│   └── orchestrator_agent.py
├── tools/
│   ├── mcp_connector.py
│   ├── airbnb_tools.py
│   └── flight_tools.py
├── state.py
└── travel_workflow_service.py
```

## What Each Layer Does
### Agents
Agents contain the business thinking.

- They do not know how MCP is implemented.
- They only know what tool they need.

### Tools
Tools are the integration layer.

- `mcp_connector.py` is the future MCP boundary.
- `airbnb_tools.py` is where Airbnb-like property search would happen.
- `flight_tools.py` is where Expedia/flight search would happen.

Right now they return mock data so the project runs without external dependencies.

### Workflow Service
`travel_workflow_service.py` wires the agents together in this order:

1. parser
2. property
3. flight
4. analysis
5. orchestrator

If `langgraph` is available, it runs as a graph.
If not, it runs sequentially with the same order.

## API
Endpoint:

- `POST /api/travel/plan`

Request fields:

- `query`
- `origin`
- `days`
- `budget_usd`
- `travelers`
- `interests`

Response fields:

- `summary`
- `selected_destination`
- `parsed_requirements`
- `top_properties`
- `flight_options`
- `assumptions`

## How Real MCP Would Plug In Later
When you are ready to connect to actual MCP servers:

1. Keep the agents the same.
2. Replace mock logic inside `airbnb_tools.py` and `flight_tools.py`.
3. Make those files call real MCP tools through `mcp_connector.py`.
4. Keep returning normalized Python dictionaries so the rest of the system stays stable.

That is the main design benefit of this refactor: the MCP-specific complexity is isolated in `tools/`, not spread across every agent.

## Why This Refactor Helps
Before, the travel module was generic.
Now it reads like the reference project:

- parser agent
- property agent
- flight agent
- analysis agent
- orchestrator agent

So it is easier to explain, easier to compare with the source reference, and easier to swap mocks with real MCP integrations later.
