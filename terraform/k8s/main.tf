terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  token                    = var.token
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  zone                     = "ru-central1-d"
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}
