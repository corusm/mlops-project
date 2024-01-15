resource "google_artifact_registry_repository" "ar_mlflow" {
  location      = var.region
  repository_id = "${var.project_name}-repo"
  description   = "Docker repository for MlFlow"
  format        = "DOCKER"
}