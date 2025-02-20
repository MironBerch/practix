# redis cluster
resource "yandex_mdb_redis_cluster" "redis_cluster" {
  name        = "redis-cluster"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.network.id

  config {
    password = "redis_password"
    version  = "7.2"
  }

  resources {
    resource_preset_id = "hm3-c2-m8"
    disk_size          = 32
  }

  host {
    zone      = "ru-central1-d"
    subnet_id = yandex_vpc_subnet.subnet_d.id
  }

  maintenance_window {
    type = "ANYTIME"
  }
}

output "redis_cluster" {
  value       = yandex_mdb_redis_cluster.redis_cluster
  sensitive = true
}
