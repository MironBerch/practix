resource "kubernetes_deployment" "async-api" {
  metadata {
    name = "async-api"
    labels = {
      app = "async-api"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "async-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "async-api"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/async-api:latest"
          name  = "async-api"

          command = ["sh", "-c"]
          args    = ["cd /app/src/ && uv run main.py"]

          port {
            name           = "http"
            container_port = 3000
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
            name  = "FASTAPI_PORT"
            value = "3000"
          }

          env {
            name  = "ELASTIC_HOST"
            value = data.terraform_remote_state.vpc.outputs.opensearch_cluster.hosts[0].fqdn
          }

          env {
            name  = "ELASTIC_PORT"
            value = "9200"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "async-api" {
  metadata {
    name = "async-api"
    labels = {
      app = "async-api"
    }
  }

  spec {
    type = "ClusterIP"
    selector = {
      "app" = "async-api"
    }
    port {
      port        = 3000
      target_port = 3000
      name        = "http"
    }
  }
}
