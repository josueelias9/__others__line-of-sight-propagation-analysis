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

module "app_service" {
  source              = "./modules/app_service"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  prefix              = local.prefix
  tags                = local.tags

  app_service_plan_sku  = var.app_service_plan_sku
  image_tag             = var.image_tag

  acr_login_server   = module.acr.login_server
  acr_admin_username = module.acr.admin_username
  acr_admin_password = module.acr.admin_password

  postgres_host     = module.database.fqdn
  postgres_user     = var.postgres_admin_username
  postgres_password = var.postgres_admin_password
  postgres_db       = var.postgres_db_name
}
