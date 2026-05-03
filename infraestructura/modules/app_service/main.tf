resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-asp"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = var.app_service_plan_sku
  tags                = var.tags
}

# ── Backend ────────────────────────────────────────────────────────────────────

resource "azurerm_linux_web_app" "backend" {
  name                = "${var.prefix}-backend"
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.main.id
  https_only          = true

  site_config {
    always_on = true

    application_stack {
      docker_image_name        = "backend:${var.image_tag}"
      docker_registry_url      = "https://${var.acr_login_server}"
      docker_registry_username = var.acr_admin_username
      docker_registry_password = var.acr_admin_password
    }

    app_command_line = "bash scripts/prestart.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000"
  }

  app_settings = {
    "DB_HOST"        = var.postgres_host
    "DB_PORT"        = "5432"
    "DB_NAME"        = var.postgres_db
    "DB_USER"        = var.postgres_user
    "DB_PASSWORD"    = var.postgres_password
    "LOG_LEVEL"      = "INFO"
    "WEBSITES_PORT"  = "8000"
    "DOCKER_ENABLE_CI" = "true"
  }

  tags = var.tags
}

# ── Frontend ───────────────────────────────────────────────────────────────────

resource "azurerm_linux_web_app" "frontend" {
  name                = "${var.prefix}-frontend"
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.main.id
  https_only          = true

  site_config {
    always_on = true

    application_stack {
      docker_image_name        = "frontend:${var.image_tag}"
      docker_registry_url      = "https://${var.acr_login_server}"
      docker_registry_username = var.acr_admin_username
      docker_registry_password = var.acr_admin_password
    }
  }

  app_settings = {
    "WEBSITES_PORT"    = "3000"
    "DOCKER_ENABLE_CI" = "true"
  }

  tags = var.tags
}
