FROM python:3.14.7
WORKDIR /app
COPY . .
RUN uv sync
EXPOSE 8000
CMD ["uvicorn", "app.main:app"]