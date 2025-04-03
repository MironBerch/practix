# load balancer target group
resource "yandex_lb_target_group" "k8s_cluster" {
  name      = "k8s-cluster-target-group"

  target {
    subnet_id = yandex_vpc_subnet.subnet_d.id
    address   = module.kubernetes.internal_v4_address
  }
}

# network load balancer
resource "yandex_lb_network_load_balancer" "k8s_lb" {
  name = "k8s-load-balancer"

  listener {
    name = "http-listener"
    port = 80
    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.k8s_cluster.id

    healthcheck {
      name = "http-healthcheck"
      http_options {
        port = 80
        path = "/"
      }
    }
  }
}
