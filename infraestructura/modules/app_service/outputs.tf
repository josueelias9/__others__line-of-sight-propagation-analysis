output "url" {
  description = "Container App HTTPS URL"
  value       = "https://${azurerm_container_app.main.latest_revision_fqdn}"
}

output "hostname" {
  description = "Container App FQDN (without https://)"
  value       = azurerm_container_app.main.latest_revision_fqdn
}

output "name" {
  description = "Container App resource name"
  value       = azurerm_container_app.main.name
}
