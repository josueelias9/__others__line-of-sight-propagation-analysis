# ── Container Apps Environment ────────────────────────────────────────────────

resource "azurerm_container_app_environment" "this" {
  name                       = "cae-${var.name_suffix}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  infrastructure_subnet_id   = var.subnet_id
  # Set to true to make the environment's load balancer internal-only.
  # Keep false so Container Apps with external ingress are publicly reachable.
  internal_load_balancer_enabled = false
  tags                       = var.tags
}

# ── Secrets (shared across apps via locals) ───────────────────────────────────

locals {
  db_env = [
    { name = "DB_HOST", value = var.db_host, secret_name = null },
    { name = "DB_PORT", value = var.db_port, secret_name = null },
    { name = "DB_NAME", value = var.db_name, secret_name = null },
    { name = "DB_USER", value = var.db_username, secret_name = null },
    { name = "DB_PASSWORD", value = null, secret_name = "db-password" },
  ]
}

# ── Backend Container App ─────────────────────────────────────────────────────

resource "azurerm_container_app" "backend" {
  name                         = "ca-backend-${var.name_suffix}"
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"
  tags                         = var.tags

  secret {
    name  = "acr-password"
    value = var.acr_password
  }
  secret {
    name  = "db-password"
    value = var.db_password
  }

  registry {
    server               = var.acr_login_server
    username             = var.acr_username
    password_secret_name = "acr-password"
  }

  template {
    min_replicas = 1
    max_replicas = 3

    container {
      name   = "backend"
      image  = "${var.acr_login_server}/backend:${var.image_tag}"
      cpu    = 0.5
      memory = "1Gi"

      command = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

      env {
        name  = "DB_HOST"
        value = var.db_host
      }
      env {
        name  = "DB_PORT"
        value = var.db_port
      }
      env {
        name  = "DB_NAME"
        value = var.db_name
      }
      env {
        name  = "DB_USER"
        value = var.db_username
      }
      env {
        name        = "DB_PASSWORD"
        secret_name = "db-password"
      }
      env {
        name  = "LOG_LEVEL"
        value = var.log_level
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "http"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

# ── Backend-init Container App Job ────────────────────────────────────────────
# Equivalent to the backend-init service in docker-compose.
# Trigger manually after first deploy (or from CI/CD) with:
#   az containerapp job start --name caj-backend-init-<suffix> \
#     --resource-group <rg> --subscription <sub>

resource "azurerm_container_app_job" "backend_init" {
  name                         = "caj-backend-init-${var.name_suffix}"
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = var.resource_group_name
  location                     = var.location
  tags                         = var.tags

  replica_timeout_in_seconds = 300
  replica_retry_limit        = 1

  manual_trigger_config {
    parallelism              = 1
    replica_completion_count = 1
  }

  secret {
    name  = "acr-password"
    value = var.acr_password
  }
  secret {
    name  = "db-password"
    value = var.db_password
  }

  registry {
    server               = var.acr_login_server
    username             = var.acr_username
    password_secret_name = "acr-password"
  }

  template {
    container {
      name    = "backend-init"
      image   = "${var.acr_login_server}/backend:${var.image_tag}"
      cpu     = 0.25
      memory  = "0.5Gi"
      command = ["bash", "scripts/prestart.sh"]

      env {
        name  = "DB_HOST"
        value = var.db_host
      }
      env {
        name  = "DB_PORT"
        value = var.db_port
      }
      env {
        name  = "DB_NAME"
        value = var.db_name
      }
      env {
        name  = "DB_USER"
        value = var.db_username
      }
      env {
        name        = "DB_PASSWORD"
        secret_name = "db-password"
      }
      env {
        name  = "LOG_LEVEL"
        value = var.log_level
      }
    }
  }
}

# ── Frontend Container App ────────────────────────────────────────────────────

resource "azurerm_container_app" "frontend" {
  name                         = "ca-frontend-${var.name_suffix}"
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"
  tags                         = var.tags

  secret {
    name  = "acr-password"
    value = var.acr_password
  }

  registry {
    server               = var.acr_login_server
    username             = var.acr_username
    password_secret_name = "acr-password"
  }

  template {
    min_replicas = 1
    max_replicas = 2

    container {
      name   = "frontend"
      image  = "${var.acr_login_server}/frontend:${var.image_tag}"
      cpu    = 0.5
      memory = "1Gi"

      # NEXT_PUBLIC_* vars are baked into the image at build time via build-push.sh.
      # Pass them here as well so they are visible in the container environment.
      env {
        name  = "NEXT_PUBLIC_BACKEND_URL"
        value = var.next_public_backend_url
      }
      env {
        name  = "NEXT_PUBLIC_GOOGLE_MAPS_API_KEY"
        value = var.next_public_google_maps_api_key
      }
      env {
        name  = "NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID"
        value = var.next_public_google_maps_map_id
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 3000
    transport        = "http"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

# ── pgAdmin Container App ─────────────────────────────────────────────────────

resource "azurerm_container_app" "pgadmin" {
  name                         = "ca-pgadmin-${var.name_suffix}"
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"
  tags                         = var.tags

  secret {
    name  = "pgadmin-password"
    value = var.pgadmin_password
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "pgadmin"
      image  = "dpage/pgadmin4:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "PGADMIN_DEFAULT_EMAIL"
        value = var.pgadmin_email
      }
      env {
        name        = "PGADMIN_DEFAULT_PASSWORD"
        secret_name = "pgadmin-password"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 80
    transport        = "http"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}
