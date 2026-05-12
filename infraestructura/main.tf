locals {
  prefix = "${var.project_name}-${var.environment}"

  tags = {
    project     = var.project_name
    environment = var.environment
    managed_by  = "terraform"
  }
}

resource "azurerm_resource_group" "main" {
  name     = "${local.prefix}-rg"
  location = var.location
  tags     = local.tags
}

module "acr" {
  source              = "./modules/acr"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  prefix              = local.prefix
  tags                = local.tags
}

module "database" {
  source              = "./modules/database"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tags                = local.tags

  name           = "${local.prefix}-postgres"
  admin_login    = var.postgres_admin_username
  admin_password = var.postgres_admin_password
  db_name        = var.postgres_db_name
  sku_name       = var.postgres_sku
}

resource "azurerm_container_app_environment" "main" {
  name                = "${local.prefix}-cae"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags
}

module "backend" {
  source              = "./modules/app_service"
  app_name            = "${local.prefix}-backend"
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags

  container_app_environment_id = azurerm_container_app_environment.main.id

  docker_image_name        = "backend:${var.image_tag}"
  docker_registry_url      = module.acr.login_server
  docker_registry_username = module.acr.admin_username
  docker_registry_password = module.acr.admin_password

  app_command_line = "bash scripts/prestart.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000"
  target_port      = 8000

  app_settings = {
    "DB_HOST"     = module.database.fqdn
    "DB_PORT"     = "5432"
    "DB_NAME"     = var.postgres_db_name
    "DB_USER"     = var.postgres_admin_username
    "DB_PASSWORD" = var.postgres_admin_password
    "LOG_LEVEL"   = "INFO"
  }
}

module "frontend" {
  source              = "./modules/app_service"
  app_name            = "${local.prefix}-frontend"
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags

  container_app_environment_id = azurerm_container_app_environment.main.id

  docker_image_name        = "frontend:${var.image_tag}"
  docker_registry_url      = module.acr.login_server
  docker_registry_username = module.acr.admin_username
  docker_registry_password = module.acr.admin_password

  target_port = 3000

  app_settings = {
    "AUTH_SECRET"      = var.auth_secret
    "AUTH_TRUST_HOST"  = "true"
    "POSTGRES_URL"     = "postgresql://${var.postgres_admin_username}:${urlencode(var.postgres_admin_password)}@${module.database.fqdn}:5432/${var.postgres_db_name}?sslmode=require"
    "POSTGRES_SSL"     = "require"
    "BACKEND_API_URL" = "${module.backend.url}"
  }
}
