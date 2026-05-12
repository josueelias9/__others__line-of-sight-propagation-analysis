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
  description = "Backend Container App HTTPS URL"
  value       = module.backend.url
}

output "backend_name" {
  description = "Backend Container App resource name"
  value       = module.backend.name
}

output "frontend_url" {
  description = "Frontend Container App HTTPS URL"
  value       = module.frontend.url
}

output "frontend_name" {
  description = "Frontend Container App resource name"
  value       = module.frontend.name
}

output "postgres_fqdn" {
  description = "PostgreSQL Flexible Server FQDN (accessible only from within the VNet)"
  value       = module.database.fqdn
  sensitive   = true
}
