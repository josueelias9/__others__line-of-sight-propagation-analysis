resource "azurerm_postgresql_flexible_server" "main" {
  name                         = var.name
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "16"
  administrator_login          = var.admin_login
  administrator_password       = var.admin_password
  storage_mb                   = var.storage_mb
  sku_name                     = var.sku_name
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  tags                         = var.tags

  lifecycle {
    ignore_changes = [zone]
  }
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = var.db_name
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Allow connections originating from within Azure (App Service → PostgreSQL).
resource "azurerm_postgresql_flexible_server_firewall_rule" "azure_services" {
  name             = "allow-azure-services"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
