output "backend_url" {
  description = "Backend App Service HTTPS URL"
  value       = "https://${azurerm_linux_web_app.backend.default_hostname}"
}

output "frontend_url" {
  description = "Frontend App Service HTTPS URL"
  value       = "https://${azurerm_linux_web_app.frontend.default_hostname}"
}

output "backend_hostname" {
  description = "Backend default hostname (without https://)"
  value       = azurerm_linux_web_app.backend.default_hostname
}

output "frontend_hostname" {
  description = "Frontend default hostname (without https://)"
  value       = azurerm_linux_web_app.frontend.default_hostname
}
