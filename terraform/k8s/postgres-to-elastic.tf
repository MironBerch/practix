resource "kubernetes_deployment" "postgres-to-elastic" {
  metadata {
    name = "postgres-to-elastic"
    labels = {
      app = "postgres-to-elastic"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "postgres-to-elastic"
      }
    }
    template {
      metadata {
        labels = {
          app = "postgres-to-elastic"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/etl-postgres-to-elastic:latest"
          name  = "postgres-to-elastic"

          command = ["sh", "-c"]
          args    = ["cd /app/src/ && uv run main.py"]

          env {
            name  = "DB_NAME"
            value = "movies-db"
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
