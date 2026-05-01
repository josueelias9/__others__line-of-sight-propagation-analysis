variable "prefix" {
  type = string
}

variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "app_service_plan_sku" {
  description = "App Service Plan SKU (S1 or higher required for VNet integration)"
  type        = string
  default     = "S1"
}

variable "image_tag" {
  description = "Docker image tag to pull from ACR"
  type        = string
  default     = "latest"
}

# ── ACR ────────────────────────────────────────────────────────────────────────

variable "acr_login_server" {
  description = "ACR login server hostname (e.g. myregistry.azurecr.io)"
  type        = string
}

variable "acr_admin_username" {
  type = string
}

variable "acr_admin_password" {
  type      = string
  sensitive = true
}

# ── PostgreSQL ─────────────────────────────────────────────────────────────────

variable "postgres_host" {
  description = "FQDN of the PostgreSQL Flexible Server"
  type        = string
}

variable "postgres_user" {
  type      = string
  sensitive = true
}

variable "postgres_password" {
  type      = string
  sensitive = true
}

variable "postgres_db" {
  type = string
}
