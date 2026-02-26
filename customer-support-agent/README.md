# customer-support-agent

Full-stack app with Python backend and Next.js frontend.

## Project structure

- `backend/`: Python FastAPI service
- `frontend/`: Next.js app
- `docker-compose.yml`: runs backend, frontend, postgres, and redis together

Key backend endpoints:

- `GET /api/health`
- `GET /api/jsonplaceholder/posts`
- `GET /api/llm/config`
- `POST /api/langgraph/support`

## Environment setup

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

## Run with Docker

```bash
docker compose up --build
```

Default infrastructure services:

- Postgres: `localhost:5432` (`app`/`app`, db `chatdb`)
- Redis: `localhost:6379`

Frontend: `http://localhost:${FRONTEND_PORT:-3000}`  
Backend docs: `http://localhost:${BACKEND_PORT:-8000}/docs`

## Local development without Docker

### Backend

```bash
cd backend
uv sync --extra dev
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```
