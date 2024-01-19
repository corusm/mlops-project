# Base image
FROM python:3.11-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
COPY service.py service.py
COPY models/ models/

WORKDIR /
RUN pip install -r requirements.txt --no-cache-dir
# RUN pip install . --no-deps --no-cache-dir

# Expose the port the app runs on
EXPOSE 8080

CMD exec uvicorn service:app --port 8080 --host 0.0.0.0 --workers 1