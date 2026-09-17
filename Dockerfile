FROM python:3.14.7
WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN pip install uv
RUN uv sync --frozen

COPY . .
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]