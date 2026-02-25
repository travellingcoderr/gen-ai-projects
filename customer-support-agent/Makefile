.PHONY: env docker-up docker-down logs backend-test backend-lint

env:
	cp -n .env.example .env || true
	cp -n backend/.env.example backend/.env || true
	cp -n frontend/.env.example frontend/.env.local || true

docker-up:
	docker compose up --build

docker-down:
	docker compose down

logs:
	docker compose logs -f

backend-test:
	cd backend && uv sync --extra dev && uv run pytest

backend-lint:
	cd backend && uv sync --extra dev && uv run ruff check . && uv run mypy app
