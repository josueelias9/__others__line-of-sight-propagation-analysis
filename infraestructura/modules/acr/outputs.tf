output "login_server" {
  description = "ACR login server hostname (e.g. myregistry.azurecr.io)"
  value       = azurerm_container_registry.main.login_server
}

output "admin_username" {
  description = "ACR admin username"
  value       = azurerm_container_registry.main.admin_username
}

output "admin_password" {
  description = "ACR admin password"
  value       = azurerm_container_registry.main.admin_password
  sensitive   = true
}

output "name" {
  description = "ACR registry name (without .azurecr.io)"
  value       = azurerm_container_registry.main.name
}
