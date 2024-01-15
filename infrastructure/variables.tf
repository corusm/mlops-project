variable "env" {
  default     = "prod"
  description = "Name of the environment"
}

variable "project_name" {
  default     = "dtumlops-g62v2"
  description = "Full name of the project"
}

variable "vpn_to_access_db" {
  default     = "0.0.0.0/0"
  description = "VPN that will be used to connect to DB, while using 0.0.0.0/0 the application will be available from any IP (it will be accessible from the internet)."
}

variable "region" {
  default     = "europe-west2"
  description = "GCP region that will be used for the project"
}

variable "image_name" {
  default     = "mlflow-imagine" # ähm, something wrong here
  description = "Name of the imagine that will be used."
}

variable "bucket_users_list" {
  default     = ["user:AlZiWi99@gmail.com", "user:nik.leinz@gmail.com"]
  description = "List of users "
}