output "resource_group_name" {
  description = "Name of the Azure Resource Group."
  value       = module.resource_group.name
}

output "acr_login_server" {
  description = "ACR login server (use with docker login)."
  value       = module.acr.login_server
}

output "backend_url" {
  description = "Public URL of the backend Container App. Use this as next_public_backend_url on subsequent applies."
  value       = module.container_apps.backend_url
}

output "frontend_url" {
  description = "Public URL of the frontend Container App."
  value       = module.container_apps.frontend_url
}

output "pgadmin_url" {
  description = "Public URL of the pgAdmin Container App."
  value       = module.container_apps.pgadmin_url
}

output "db_fqdn" {
  description = "FQDN of the PostgreSQL Flexible Server (private)."
  value       = module.database.fqdn
}
