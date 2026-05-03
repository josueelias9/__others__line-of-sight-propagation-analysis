output "app_service_subnet_id" {
  description = "Subnet ID for App Service VNet integration (outbound)"
  value       = azurerm_subnet.app_service.id
}

output "db_subnet_id" {
  description = "Subnet ID delegated to PostgreSQL Flexible Server"
  value       = azurerm_subnet.database.id
}

output "postgres_private_dns_zone_id" {
  description = "Private DNS zone ID for PostgreSQL VNet injection"
  value       = azurerm_private_dns_zone.postgres.id
}
