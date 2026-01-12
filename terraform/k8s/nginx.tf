resource "kubernetes_deployment" "nginx" {
  metadata {
    name = "nginx"
    labels = {
      app = "nginx"
    }
    annotations = {
      "nginx.ingress.kubernetes.io/rewrite-target" = "/"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "nginx"
      }
    }
    template {
      metadata {
        labels = {
          app = "nginx"
        }
      }
      spec {
        container {
          name  = "nginx"
          image = "nginx:1.21-alpine"
          port {
            container_port = 80
          }
          volume_mount {
            mount_path = "/etc/nginx/nginx.conf"
            name       = "nginx-config"
            sub_path   = "nginx.conf"
          }
          volume_mount {
            mount_path = "/etc/nginx/conf.d/default.conf"
            name       = "nginx-config"
            sub_path   = "default.conf"
          }
        }
        volume {
          name = "nginx-config"
          config_map {
            name = kubernetes_config_map.nginx.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_config_map" "nginx" {
  metadata {
    name = "nginx"
  }

  data = {
    "nginx.conf" = file("files/nginx/nginx.conf")
    "default.conf" = file("files/nginx/conf.d/default.conf")
  }
}

resource "kubernetes_service" "nginx" {
  metadata {
    name = "nginx"
    labels = {
      app = "nginx"
    }
  }

  spec {
    type = "NodePort"
    selector = {
      "app" = "nginx"
    }
    port {
      port        = 80
      target_port = 80
      name        = "http"
    }
  }
}

resource "kubernetes_ingress" "nginx" {
  metadata {
    name = "nginx-ingress"
  }

  spec {
    rule {
      http {
        path {
          path = "/"
          backend {
            service_name = kubernetes_service.nginx.metadata[0].name
            service_port = 80
          }
        }
      }
    }
  }
}
