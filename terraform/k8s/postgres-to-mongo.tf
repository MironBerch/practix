resource "kubernetes_deployment" "postgres-to-mongo" {
  metadata {
    name = "postgres-to-mongo"
    labels = {
      app = "postgres-to-mongo"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "postgres-to-mongo"
      }
    }
    template {
      metadata {
        labels = {
          app = "postgres-to-mongo"
        }
      }
      spec {
        container {
          image = "cr.yandex/${var.container_registry_id}/etl-postgres-to-mongo:latest"
          name  = "postgres-to-mongo"

          command = ["sh", "-c"]
          args    = ["cd /app/src/ && python main.py"]

          env {
            name  = "MOVIES_DB_NAME"
            value = "movies-db"
          }
          env {
            name  = "MOVIES_DB_USER"
            value = var.movies_db_user
          }
          env {
            name  = "MOVIES_DB_PASSWORD"
            value = var.movies_db_password
          }
          env {
            name  = "MOVIES_DB_HOST"
            value = data.terraform_remote_state.vpc.outputs.movies_db_cluster.host[0].fqdn
          }
          env {
            name  = "MOVIES_DB_PORT"
            value = "5432"
          }
          env {
            name  = "AUTH_DB_NAME"
            value = "auth-db"
          }
          env {
            name  = "AUTH_DB_USER"
            value = var.auth_db_user
          }
          env {
            name  = "AUTH_DB_PASSWORD"
            value = var.auth_db_password
          }
          env {
            name  = "AUTH_DB_HOST"
            value = data.terraform_remote_state.vpc.outputs.auth_db_cluster.host[0].fqdn
          }
          env {
            name  = "AUTH_DB_PORT"
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
