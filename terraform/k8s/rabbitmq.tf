resource "kubernetes_deployment" "rabbitmq" {
  metadata {
    name = "rabbitmq"
    labels = {
      app = "rabbitmq"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "rabbitmq"
      }
    }
    template {
      metadata {
        labels = {
          app = "rabbitmq"
        }
      }
      spec {
        container {
          name  = "rabbitmq"
          image = "rabbitmq:4-alpine"

          env {
            name  = "RABBITMQ_DEFAULT_USER"
            value = var.rabbitmq_default_user
          }
          env {
            name  = "RABBITMQ_DEFAULT_PASS"
            value = var.rabbitmq_default_pass
          }

          port {
            container_port = 5672
            name           = "client-port"
          }
          port {
            container_port = 15672
            name           = "server-port"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "rabbitmq" {
  metadata {
    name = "rabbitmq"
    labels = {
      app = "rabbitmq"
    }
  }

  spec {
    type = "ClusterIP"
    port {
      port        = 5672
      target_port = 5672
      name        = "rabbitmq-client"
    }
    port {
      port        = 15672
      target_port = 15672
      name        = "rabbitmq-server"
    }
    selector = {
      app = "rabbitmq"
    }
  }
}
