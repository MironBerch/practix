resource "kubernetes_deployment" "notifications-worker" {
  metadata {
    name = "notifications-worker"
    labels = {
      app = "notifications-worker"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "notifications-worker"
      }
    }
    template {
      metadata {
        labels = {
          app = "notifications-worker"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/notifications-worker:latest"
          name  = "notifications-worker"

          command = ["sh", "-c"]
          args    = ["cd /app/src/ && uv run main.py"]

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
            name  = "SECRET_KEY"
            value = var.secret_key
          }
          env {
            name  = "SMTP_SERVER"
            value = var.smtp_server
          }
          env {
            name  = "SMTP_PORT"
            value = var.smtp_port
          }
          env {
            name  = "SMTP_USERNAME"
            value = var.smtp_username
          }
          env {
            name  = "SMTP_PASSWORD"
            value = var.smtp_password
          }
        }
      }
    }
  }
  depends_on = [kubernetes_deployment.rabbitmq]
}
