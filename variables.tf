variable "project_id" {
  type        = string
  default = "<YOUR-PROJECT-ID>"
}

variable "region" {
  type        = string
  default = "US"
}
variable "function_src_bucket" {
  type        = string
  default = "src-dev"
}
variable "input_bucket" {
  type        = string
  default = "input-dev"
}
variable "archive_bucket" {
  type        = string
  default = "archive-dev"
}
variable "gcs_location" {
  type        = string
  description = ""
}
variable "controller_service_account_email" {
  type        = string
  description = ""
}
variable "machine_type" {
  type        = string
  description = ""
}