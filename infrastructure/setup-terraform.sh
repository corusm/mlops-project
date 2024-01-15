#!/bin/bash
# Enable artifact registry API
# Enable secret manager api

# terraform plan
# terraform apply -target="google_artifact_registry_repository.ar_mlflow"
cd ./mlflow-docker && make build && make docker-auth && make tag && make push
# terraform apply