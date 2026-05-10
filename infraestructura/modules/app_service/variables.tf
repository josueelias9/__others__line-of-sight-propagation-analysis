variable "app_name" {
  description = "Name of the Container App"
  type        = string
}

variable "resource_group_name" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "container_app_environment_id" {
  description = "ID of the Container App Environment"
  type        = string
}

variable "docker_image_name" {
  description = "Docker image name and tag (e.g. backend:latest)"
  type        = string
}

variable "docker_registry_url" {
  description = "ACR login server hostname (e.g. lospaprodacr.azurecr.io)"
  type        = string
}

variable "docker_registry_username" {
  type = string
}

variable "docker_registry_password" {
  type      = string
  sensitive = true
}

variable "app_command_line" {
  description = "Custom startup command run via bash -c (leave empty to use image entrypoint)"
  type        = string
  default     = ""
}

variable "app_settings" {
  description = "Environment variables for the container"
  type        = map(string)
  default     = {}
}

variable "target_port" {
  description = "Port the container listens on (used for ingress)"
  type        = number
}
