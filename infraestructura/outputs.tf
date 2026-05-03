output "resource_group_name" {
  description = "Azure Resource Group containing all deployed resources"
  value       = azurerm_resource_group.main.name
}

output "acr_login_server" {
  description = "ACR login server URL (used by scripts/build_and_push.sh)"
  value       = module.acr.login_server
}

output "acr_name" {
  description = "ACR registry name (used by scripts/build_and_push.sh)"
  value       = module.acr.name
}

output "backend_url" {
  description = "Backend App Service HTTPS URL"
  value       = module.app_service.backend_url
}

output "frontend_url" {
  description = "Frontend App Service HTTPS URL"
  value       = module.app_service.frontend_url
}

output "postgres_fqdn" {
  description = "PostgreSQL Flexible Server FQDN (accessible only from within the VNet)"
  value       = module.database.fqdn
  sensitive   = true
}
