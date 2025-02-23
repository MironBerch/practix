# opensearch cluster
resource "yandex_mdb_opensearch_cluster" "opensearch_cluster" {
  name        = "opensearch-cluster"
  environment = "PRESTABLE"
  network_id  = yandex_vpc_network.network.id

  config {
    admin_password = "super-password"

    opensearch {
      node_groups {
        name             = "nodegroup1"
        assign_public_ip = true
        hosts_count      = 1
        subnet_ids       = ["${yandex_vpc_subnet.subnet_d.id}"]
        zone_ids         = ["ru-central1-d"]
        roles            = ["data", "manager"]

        resources {
          resource_preset_id = "s3-c2-m8"
          disk_size          = 10737418240
          disk_type_id       = "network-ssd"
        }
      }
    }
  }

  maintenance_window {
    type = "ANYTIME"
  }
}

output "opensearch_cluster" {
  value       = yandex_mdb_opensearch_cluster.opensearch_cluster
  sensitive = true
}
