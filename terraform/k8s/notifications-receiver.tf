resource "kubernetes_deployment" "notifications-receiver" {
  metadata {
    name = "notifications-receiver"
    labels = {
      app = "notifications-receiver"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "notifications-receiver"
      }
    }
    template {
      metadata {
        labels = {
          app = "notifications-receiver"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/notifications-receiver:latest"
          name  = "notifications-receiver"

          command = ["sh", "-c"]
          args    = ["cd /app/src/ && poetry run python main.py"]

          env {
            name  = "RABBITMQ_USER"
            value = var.rabbitmq_default_user
          }
          env {
            name  = "RABBITMQ_PASS"
            value = var.rabbitmq_default_pass
          }
          env {
            name  = "RABBITMQ_HOST"
            value = "rabbitmq"
          }
          env {
            name  = "RABBITMQ_SERVER_PORT"
            value = "15672"
          }
          env {
            name  = "RABBITMQ_CLIENT_PORT"
            value = "5672"
          }
          env {
            name  = "POSTGRES_NAME"
            value = "notifications-db"
          }
          env {
            name  = "POSTGRES_USER"
            value = var.notifications_db_user
          }
          env {
            name  = "POSTGRES_PASSWORD"
            value = var.notifications_db_password
          }
          env {
            name  = "POSTGRES_HOST"
            value = data.terraform_remote_state.vpc.outputs.notifications_db_cluster.host[0].fqdn
          }
          env {
            name  = "POSTGRES_PORT"
            value = "5432"
          }
          env {
            name  = "DEBUG"
            value = "False"
          }
          env {
            name  = "FASTAPI_PORT"
            value = "2000"
          }
        }
      }
    }
  }
  depends_on = [kubernetes_deployment.rabbitmq]
}

resource "kubernetes_service" "notifications-receiver" {
  metadata {
    name = "notifications-receiver"
    labels = {
      app = "notifications-receiver"
    }
  }

  spec {
    type = "ClusterIP"
    selector = {
      "app" = "notifications-receiver"
    }
    port {
      port        = 2000
      target_port = 2000
      name        = "http"
    }
  }
}
