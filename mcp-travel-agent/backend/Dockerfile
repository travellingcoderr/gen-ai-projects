FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.31 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app

RUN uv sync --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
