output "backend_url" {
  description = "Public HTTPS URL of the backend Container App."
  value       = "https://${azurerm_container_app.backend.ingress[0].fqdn}"
}

output "frontend_url" {
  description = "Public HTTPS URL of the frontend Container App."
  value       = "https://${azurerm_container_app.frontend.ingress[0].fqdn}"
}

output "pgadmin_url" {
  description = "Public HTTPS URL of the pgAdmin Container App."
  value       = "https://${azurerm_container_app.pgadmin.ingress[0].fqdn}"
}

output "backend_init_job_name" {
  description = "Name of the backend-init Container App Job."
  value       = azurerm_container_app_job.backend_init.name
}
