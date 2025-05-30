FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock .

RUN uv sync

COPY app.py app.py

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "app.py"]