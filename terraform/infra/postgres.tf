# movies postgres cluster
resource "yandex_mdb_postgresql_cluster" "movies_db_cluster" {
  name        = "movies-db-cluster"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.network.id

  config {
    version = 16

    resources {
      resource_preset_id = "s3-c2-m8"
      disk_type_id       = "network-ssd"
      disk_size          = 10
    }

    postgresql_config = {
      max_connections                   = 395
      enable_parallel_hash              = true
      autovacuum_vacuum_scale_factor    = 0.34
      default_transaction_isolation     = "TRANSACTION_ISOLATION_READ_COMMITTED"
      shared_preload_libraries          = "SHARED_PRELOAD_LIBRARIES_AUTO_EXPLAIN,SHARED_PRELOAD_LIBRARIES_PG_HINT_PLAN"
    }
  }

  maintenance_window {
    type = "WEEKLY"
    day  = "SAT"
    hour = 12
  }

  host {
    zone      = "ru-central1-d"
    subnet_id = yandex_vpc_subnet.subnet_d.id
  }
}

# movies postgres db
resource "yandex_mdb_postgresql_database" "movies_db" {
  cluster_id = yandex_mdb_postgresql_cluster.movies_db_cluster.id
  name       = "movies-db"
  owner      = yandex_mdb_postgresql_user.movies_db_user.name
  lc_collate = "en_US.UTF-8"
  lc_type    = "en_US.UTF-8"

  extension {
    name = "uuid-ossp"
  }

  extension {
    name = "xml2"
  }
}

# movies postgres user
resource "yandex_mdb_postgresql_user" "movies_db_user" {
  cluster_id = yandex_mdb_postgresql_cluster.movies_db_cluster.id
  name       = "pguser"
  password   = "pgpassword"
}


# auth postgres cluster
resource "yandex_mdb_postgresql_cluster" "auth_db_cluster" {
  name        = "auth-db-cluster"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.network.id

  config {
    version = 16

    resources {
      resource_preset_id = "s3-c2-m8"
      disk_type_id       = "network-ssd"
      disk_size          = 10
    }

    postgresql_config = {
      max_connections                   = 395
      enable_parallel_hash              = true
      autovacuum_vacuum_scale_factor    = 0.34
      default_transaction_isolation     = "TRANSACTION_ISOLATION_READ_COMMITTED"
      shared_preload_libraries          = "SHARED_PRELOAD_LIBRARIES_AUTO_EXPLAIN,SHARED_PRELOAD_LIBRARIES_PG_HINT_PLAN"
    }
  }

  maintenance_window {
    type = "WEEKLY"
    day  = "SAT"
    hour = 12
  }

  host {
    zone      = "ru-central1-d"
    subnet_id = yandex_vpc_subnet.subnet_d.id
  }
}

# auth postgres db
resource "yandex_mdb_postgresql_database" "auth_db" {
  cluster_id = yandex_mdb_postgresql_cluster.auth_db_cluster.id
  name       = "auth-db"
  owner      = yandex_mdb_postgresql_user.auth_db_user.name
  lc_collate = "en_US.UTF-8"
  lc_type    = "en_US.UTF-8"

  extension {
    name = "uuid-ossp"
  }

  extension {
    name = "xml2"
  }
}

# auth postgres user
resource "yandex_mdb_postgresql_user" "auth_db_user" {
  cluster_id = yandex_mdb_postgresql_cluster.auth_db_cluster.id
  name       = "pguser"
  password   = "pgpassword"
}

output "movies_db_cluster" {
  value       = yandex_mdb_postgresql_cluster.movies_db_cluster
}

output "movies_db" {
  value       = yandex_mdb_postgresql_database.movies_db
}

output "auth_db_cluster" {
  value       = yandex_mdb_postgresql_cluster.auth_db_cluster
}

output "auth_db" {
  value       = yandex_mdb_postgresql_database.auth_db
}
