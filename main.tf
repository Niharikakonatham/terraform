provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "function_bucket" {
    name     = var.function_src_bucket
    location = var.region
}

resource "google_storage_bucket" "input_bucket" {
    name     = var.input_bucket
    location = var.region
}

resource "google_storage_bucket" "archive_bucket" {
    name     = var.archive_bucket
    location = var.region
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
    source       = "../with_pubsub"
    name         = "index.zip"
    bucket       = google_storage_bucket.function_bucket.name
}

# Create the Cloud function triggered by a `Finalize` event on the bucket
resource "google_cloudfunctions_function" "function" {
  name    = "function-trigger-on-gcs"
  runtime = "python37"  # of course changeable

  # Get the source code of the cloud function as a Zip compression
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  # Must match the function name in the cloud function `main.py` source code
  entry_point = "main"

  #
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = "${var.project_id}-input"
  }
}

resource "google_dataflow_job" "Iris_to_BQ" {
  project               = var.project_id
  region                = var.region
  zone                  = "${var.region}-a"
  name              = "Iris_to_BQ"
  on_delete             = "cancel"
  max_workers           = 2
  service_account_email = var.controller_service_account_email
  template_gcs_path = "gs://dataflow-templates/latest/Jdbc_to_BigQuery"
  temp_gcs_location = "gs://${var.gcs_location}/temp"
  parameters = {
    inputFile = "gs://dataflow-samples/shakespeare/kinglear.txt"
    output = "gs://${var.gcs_location}/wordcount/output"
  }
  machine_type     = var.machine_type
}