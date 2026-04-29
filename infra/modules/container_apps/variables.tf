variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "name_suffix" {
  description = "Suffix appended to all resource names (e.g. los-dev)."
  type        = string
}

variable "subnet_id" {
  description = "ID of the /23 subnet delegated to Microsoft.App/environments."
  type        = string
}

# ── ACR ───────────────────────────────────────────────────────────────────────

variable "acr_login_server" {
  type = string
}

variable "acr_username" {
  type      = string
  sensitive = true
}

variable "acr_password" {
  type      = string
  sensitive = true
}

variable "image_tag" {
  type    = string
  default = "latest"
}

# ── Database ──────────────────────────────────────────────────────────────────

variable "db_host" {
  type = string
}

variable "db_port" {
  type    = string
  default = "5432"
}

variable "db_name" {
  type = string
}

variable "db_username" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

# ── Frontend ──────────────────────────────────────────────────────────────────

variable "next_public_google_maps_api_key" {
  type      = string
  sensitive = true
}

variable "next_public_google_maps_map_id" {
  type = string
}

variable "next_public_backend_url" {
  description = "Public backend URL seen from the browser. Leave empty on first apply."
  type        = string
  default     = ""
}

# ── pgAdmin ───────────────────────────────────────────────────────────────────

variable "pgadmin_email" {
  type = string
}

variable "pgadmin_password" {
  type      = string
  sensitive = true
}

# ── Backend ───────────────────────────────────────────────────────────────────

variable "log_level" {
  type    = string
  default = "INFO"
}

variable "tags" {
  type    = map(string)
  default = {}
}
