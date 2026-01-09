resource "kubernetes_deployment" "admin-panel" {
  metadata {
    name = "admin-panel"
    labels = {
      app = "admin-panel"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "admin-panel"
      }
    }
    template {
      metadata {
        labels = {
          app = "admin-panel"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/admin-panel:latest"
          name  = "admin-panel"

          command = ["sh", "-c"]
          args    = [
            <<EOT
            cd /app/src/ 
            mkdir -p media 
            uv run manage.py collectstatic --noinput 
            uv run manage.py migrate --noinput 
            uv run manage.py createsuperuser --noinput || true 
            uv run gunicorn --reload -c ../infra/gunicorn/gunicorn_config.py config.wsgi:application
            EOT
          ]

          env {
            name  = "DB_NAME"
            value = "movies"
          }
          env {
            name  = "DB_USER"
            value = var.movies_db_user
          }
          env {
            name  = "DB_PASSWORD"
            value = var.movies_db_password
          }
          env {
            name  = "DB_HOST"
            value = data.terraform_remote_state.vpc.outputs.movies_db_cluster.host[0].fqdn
          }
          env {
            name  = "DB_PORT"
            value = "5432"
          }
          env {
            name  = "DEBUG"
            value = "False"
          }

          env {
            name  = "SECRET_KEY"
            value = var.secret_key
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "admin-panel" {
  metadata {
    name = "admin-panel"
    labels = {
      app = "admin-panel"
    }
  }

  spec {
    type = "ClusterIP"
    selector = {
      "app" = "admin-panel"
    }
    port {
      port        = 8000
      target_port = 8000
      name        = "http"
    }
  }
}
