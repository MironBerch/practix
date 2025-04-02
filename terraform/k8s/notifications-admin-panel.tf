resource "kubernetes_persistent_volume" "notifications_static_volume" {
  metadata {
    name = "notifications-static-volume"
  }
  spec {
    capacity = {
      storage = "1Gi"
    }
    access_modes = ["ReadWriteOnce"]
    persistent_volume_source {
      host_path {
        path = "/mnt/data/notifications-static"
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "notifications_static_volume_claim" {
  metadata {
    name = "notifications-static-volume-claim"
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }
    volume_name = kubernetes_persistent_volume.static_volume.metadata[0].name
  }
}

resource "kubernetes_deployment" "notifications-admin-panel" {
  metadata {
    name = "notifications-admin-panel"
    labels = {
      app = "notifications-admin-panel"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "notifications-admin-panel"
      }
    }
    template {
      metadata {
        labels = {
          app = "notifications-admin-panel"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/notifications-admin-panel:latest"
          name  = "notifications-admin-panel"
          command = ["sh", "-c"]
          args    = [
            <<EOT
            cd /app/src/
            mkdir -p media
            uv run manage.py collectstatic --noinput
            uv run manage.py migrate --noinput
            uv run manage.py createsuperuser --noinput || true
            uv run gunicorn --reload -c gunicorn.py --bind 0.0.0.0:1000 config.wsgi:application
            EOT
          ]
          env {
            name  = "DB_NAME"
            value = "notifications-db"
          }
          env {
            name  = "DB_USER"
            value = var.notifications_db_user
          }
          env {
            name  = "DB_PASSWORD"
            value = var.notifications_db_password
          }
          env {
            name  = "DB_HOST"
            value = data.terraform_remote_state.vpc.outputs.notifications_db_cluster.host[0].fqdn
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

          volume_mount {
            name       = "notifications-static-volume"
            mount_path = "/app/src/notifications/static/"
          }
        }
        volume {
          name = "notifications-static-volume"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.notifications_static_volume_claim.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "notifications-admin-panel" {
  metadata {
    name = "notifications-admin-panel"
    labels = {
      app = "notifications-admin-panel"
    }
  }

  spec {
    type = "ClusterIP"
    selector = {
      "app" = "notifications-admin-panel"
    }
    port {
      port        = 1000
      target_port = 1000
      name        = "http"
    }
  }
}
