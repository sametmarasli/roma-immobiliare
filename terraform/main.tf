terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region    = var.region
}


resource "google_storage_bucket" "static" {
  name = "roma-prefect-deployments"
  location = var.region
  uniform_bucket_level_access = true
}
