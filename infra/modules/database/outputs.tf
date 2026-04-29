output "fqdn" {
  description = "Fully qualified domain name of the PostgreSQL server (resolvable within the VNet)."
  value       = azurerm_postgresql_flexible_server.this.fqdn
}

output "server_name" {
  value = azurerm_postgresql_flexible_server.this.name
}

output "database_name" {
  value = azurerm_postgresql_flexible_server_database.app.name
}
