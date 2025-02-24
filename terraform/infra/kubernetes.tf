module "kubernetes" {
  source     = "github.com/terraform-yc-modules/terraform-yc-kubernetes.git"
  network_id = "${yandex_vpc_network.network.id}"
  master_locations   = [
    {
      zone      = "ru-central1-d"
      subnet_id = "${yandex_vpc_subnet.subnet_d.id}"
    },
  ]
  node_groups = {
    "kubernetes-node-group"  = {
      node_cores    = 12
      node_memory   = 24
      disk_size     = 60
      fixed_scale   = {
        size = 1
      }
    },
  }
}

output "kubernetes_cluster_id" {
  value       = try(module.kubernetes.cluster_id, null)
}

output "kubernetes_cluster_name" {
  value       = try(module.kubernetes.cluster_name, null)
}

output "external_cluster_cmd_str" {
  description = "Connection string to external Kubernetes cluster."
  value       = try(module.kubernetes.external_cluster_cmd, null)
}

output "internal_cluster_cmd_str" {
  description = "Connection string to internal Kubernetes cluster."
  value       = try(module.kubernetes.internal_cluster_cmd, null)
}

output "node_account_name" {
  description = "IAM node account name"
  value       = module.kubernetes.node_account_name
}

output "service_account_name" {
  description = "IAM service account name"
  value       = module.kubernetes.service_account_name
}
