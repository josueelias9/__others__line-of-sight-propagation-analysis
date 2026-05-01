output "fqdn" {
  description = "Fully qualified domain name of the PostgreSQL Flexible Server (VNet-internal)"
  value       = azurerm_postgresql_flexible_server.main.fqdn
}

output "server_name" {
  description = "Name of the PostgreSQL Flexible Server resource"
  value       = azurerm_postgresql_flexible_server.main.name
}
