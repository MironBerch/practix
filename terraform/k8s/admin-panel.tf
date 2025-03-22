resource "kubernetes_persistent_volume" "static_volume" {
  metadata {
    name = "static-volume"
  }
  spec {
    capacity = {
      storage = "1Gi"
    }
    access_modes = ["ReadWriteOnce"]
    storage_class_name = "standard"
    persistent_volume_source {
      host_path {
        path = "/mnt/data/static"
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "static_volume_claim" {
  metadata {
    name = "static-volume-claim"
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }
    storage_class_name = "standard"
    volume_name = kubernetes_persistent_volume.static_volume.metadata[0].name
  }
}

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
            python manage.py collectstatic --noinput 
            python manage.py migrate --noinput 
            python manage.py createsuperuser --noinput || true 
            gunicorn --reload -c ../infra/gunicorn/gunicorn_config.py config.wsgi:application
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

          volume_mount {
            name       = "static-volume"
            mount_path = "/app/src/static"
          }
        }
        volume {
          name = "static-volume"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.static_volume_claim.metadata[0].name
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
