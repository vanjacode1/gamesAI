FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y stockfish && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv
RUN uv sync --frozen

COPY . .

ENV STOCKFISH_PATH=/usr/games/stockfish

CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]