# Base image
FROM python:3.11-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

WORKDIR /
RUN pip install -r requirements.txt --no-cache-dir

COPY pyproject.toml pyproject.toml
COPY mlops_project/ mlops_project/
COPY data/ data/

RUN pip install . --no-deps --no-cache-dir

ENTRYPOINT ["python", "-u", "mlops_project/train_model_for_docker.py"]