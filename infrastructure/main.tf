terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.10.0"
    }
  }
  # VARIABLES NOT ALLOWED
  backend "gcs" {
    bucket  = "terraform3"
    prefix  = "terraform/state"
  }
}

provider "google" {
  region  = "europe-west2"
  project = "dtumlops-g62v2"
}