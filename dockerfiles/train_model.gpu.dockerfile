# Base image
FROM radixai/python-gpu:3.11-cuda11.8

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

WORKDIR /
RUN pip install -r requirements.txt --no-cache-dir
