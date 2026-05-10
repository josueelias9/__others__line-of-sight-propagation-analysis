resource "azurerm_container_app" "main" {
  name                         = var.app_name
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"
  tags                         = var.tags

  secret {
    name  = "registry-password"
    value = var.docker_registry_password
  }

  registry {
    server               = var.docker_registry_url
    username             = var.docker_registry_username
    password_secret_name = "registry-password"
  }

  # Only ignore the image so that 'az containerapp update' changes are not
  # reverted by Terraform, while env vars and other settings stay in sync.
  lifecycle {
    ignore_changes = [template[0].container[0].image]
  }

  template {
    container {
      name   = "app"
      image  = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      command = length(var.app_command_line) > 0 ? ["/bin/bash", "-c", var.app_command_line] : null

      dynamic "env" {
        for_each = var.app_settings
        content {
          name  = env.key
          value = env.value
        }
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = var.target_port
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}
