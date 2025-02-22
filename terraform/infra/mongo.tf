# mongodb cluster
resource "yandex_mdb_mongodb_cluster" "mongodb_cluster" {
  name        = "mongodb-cluster"
  environment = "PRESTABLE"
  network_id  = yandex_vpc_network.network.id

  cluster_config {
    version = "7.0"
  }

  resources_mongod {
    resource_preset_id = "s3-c2-m8"
    disk_size          = 10
    disk_type_id       = "network-ssd"
  }

  resources_mongos {
    resource_preset_id = "s3-c2-m8"
    disk_size          = 10
    disk_type_id       = "network-ssd"
  }

  resources_mongocfg {
    resource_preset_id = "s3-c2-m8"
    disk_size          = 10
    disk_type_id       = "network-ssd"
  }

  host {
    zone_id   = "ru-central1-d"
    subnet_id = yandex_vpc_subnet.subnet_d.id
  }

  maintenance_window {
    type = "ANYTIME"
  }
}

# mongodb
resource "yandex_mdb_mongodb_database" "mongodb" {
  cluster_id = yandex_mdb_mongodb_cluster.mongodb_cluster.id
  name       = "practix_mongodb"
}

# mongodb user
resource "yandex_mdb_mongodb_user" "mongodb_user" {
  cluster_id = yandex_mdb_mongodb_cluster.mongodb_cluster.id
  name       = "user"
  password   = "password"
}

output "mongodb_cluster" {
  value       = yandex_mdb_mongodb_cluster.mongodb_cluster
}

output "mongodb" {
  value       = yandex_mdb_mongodb_database.mongodb
}
