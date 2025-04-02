resource "kubernetes_deployment" "ugc-api" {
  metadata {
    name = "ugc-api"
    labels = {
      app = "ugc-api"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "ugc-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "ugc-api"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/ugc:latest"
          name  = "ugc-api"

          command = ["sh", "-c"]
          args    = ["cd /app/src/ && uv run main.py"]

          port {
            name           = "http"
            container_port = 4000
          }

          env {
            name  = "JWT_SECRET_KEY"
            value = var.jwt_secret_key
          }

          env {
            name  = "DEBUG"
            value = "False"
          }

          env {
            name  = "FASTAPI_PORT"
            value = "4000"
          }

          env {
            name  = "MONGO_HOST"
            value = data.terraform_remote_state.vpc.outputs.notifications_db_cluster.host[0].name
          }

          env {
            name  = "MONGO_PORT"
            value = "27017"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "ugc-api" {
  metadata {
    name = "ugc-api"
    labels = {
      app = "ugc-api"
    }
  }

  spec {
    type = "ClusterIP"
    selector = {
      "app" = "ugc-api"
    }
    port {
      port        = 4000
      target_port = 4000
      name        = "http"
    }
  }
}
