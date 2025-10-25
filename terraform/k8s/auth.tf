resource "kubernetes_deployment" "auth-api" {
  metadata {
    name = "auth-api"
    labels = {
      app = "auth-api"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "auth-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "auth-api"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/auth:latest"
          name  = "auth-api"

          command = ["sh", "-c"]
          args    = [
            <<EOT
            cd /app/src/
            uv run flask --app manage:create_app migrate
            uv run gunicorn --workers 1 --bind 0.0.0.0:5000 manage:app
            EOT
          ]

          port {
            name           = "http"
            container_port = 5000
          }

          env {
            name  = "JWT_SECRET_KEY"
            value = var.jwt_secret_key
          }
          env {
            name  = "SECRET_KEY"
            value = var.secret_key
          }

          env {
            name  = "FASTAPI_PORT"
            value = "5000"
          }

          env {
            name  = "DEBUG"
            value = "False"
          }

          env {
            name  = "DB_HOST"
            value = data.terraform_remote_state.vpc.outputs.auth_db_cluster.host[0].fqdn
          }
          env {
            name  = "DB_PORT"
            value = "5432"
          }
          env {
            name  = "DB_NAME"
            value = "auth-db"
          }
          env {
            name  = "DB_USER"
            value = var.auth_db_user
          }
          env {
            name  = "DB_PASSWORD"
            value = var.auth_db_password
          }

          env {
            name  = "REDIS_HOST"
            value = data.terraform_remote_state.vpc.outputs.redis_cluster.host[0].fqdn
          }
          env {
            name  = "REDIS_PORT"
            value = "6379"
          }
          env {
            name  = "REDIS_DB"
            value = "1"
          }

          env {
            name  = "NOTIFICATIONS_RECEIVER_HOST"
            value = "notifications-receiver"
          }
          env {
            name  = "NOTIFICATIONS_RECEIVER_PORT"
            value = "2000"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "auth-api" {
  metadata {
    name = "auth-api"
    labels = {
      app = "auth-api"
    }
  }

  spec {
    type = "ClusterIP"
    selector = {
      "app" = "auth-api"
    }
    port {
      port        = 5000
      target_port = 5000
      name        = "http"
    }
  }
}
