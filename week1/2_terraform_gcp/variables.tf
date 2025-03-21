variable "credentials" {
  description = "My Credentials"
  default     = "./.terraform/google-terraform-creds.json"
  #ex: if you have a directory where this file is called keys with your service account json file
}


variable "project" {
  description = "Project"
  default     = "advance-vector-447116-m5"
}


variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "us-central1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default = "vlanterraformdemo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default = "terraform-demo-bucket4584695487"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}