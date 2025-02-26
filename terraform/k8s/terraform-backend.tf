data "terraform_remote_state" "vpc" {
  backend = "s3"

  config  = {
    endpoints = {
      s3 = "https://storage.yandexcloud.net"
    }
    bucket = "practix-bucket"
    region = "ru-central1-d"
    key    = "terraform/terraform.tfstate"

    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true

    access_key = var.iam_access_key
    secret_key = var.iam_secret_key
  }
}
