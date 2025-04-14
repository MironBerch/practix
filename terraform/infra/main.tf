terraform {
  required_providers {
    yandex = {
        source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"

  backend "s3" {
    endpoints = {
      s3 = "https://storage.yandexcloud.net"
    }
    bucket = "practix-bucket"
    region = "ru-central1-d"
    key    = "terraform/terraform.tfstate"

    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
  }
}

provider "yandex" {
  token                    = var.token
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  zone                     = "ru-central1-d"
}

resource "null_resource" "create_movies_db_schema" {
  depends_on = [
    yandex_mdb_postgresql_cluster.movies_db_cluster,
    yandex_mdb_postgresql_database.movies_db,
    yandex_mdb_postgresql_user.movies_db_user,
  ]

  provisioner "local-exec" {
    command = <<EOT
      until PGPASSWORD='${yandex_mdb_postgresql_user.movies_db_user.password}' \
        pg_isready -h ${yandex_mdb_postgresql_cluster.movies_db_cluster.host[0].fqdn} \
        -U ${yandex_mdb_postgresql_user.movies_db_user.name}; 
      do
        echo "Waiting for PostgreSQL to start..."
        sleep 5
      done
      PGPASSWORD='${yandex_mdb_postgresql_user.movies_db_user.password}' \
        psql -h ${yandex_mdb_postgresql_cluster.movies_db_cluster.host[0].fqdn} \
        -U ${yandex_mdb_postgresql_user.movies_db_user.name} \
        -d ${yandex_mdb_postgresql_database.movies_db.name} \
        -c "CREATE SCHEMA IF NOT EXISTS content;"
    EOT
  }
}
