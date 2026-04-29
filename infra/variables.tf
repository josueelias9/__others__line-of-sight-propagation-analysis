variable "project" {
  description = "Short project identifier used in resource names."
  type        = string
  default     = "los"
}

variable "env" {
  description = "Deployment environment (dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "eastus"
}

variable "image_tag" {
  description = "Docker image tag to deploy."
  type        = string
  default     = "latest"
}

# ── Database ──────────────────────────────────────────────────────────────────

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "los_db"
}

variable "db_username" {
  description = "PostgreSQL administrator username."
  type        = string
  default     = "losadmin"
}

variable "db_password" {
  description = "PostgreSQL administrator password."
  type        = string
  sensitive   = true
}

# ── pgAdmin ───────────────────────────────────────────────────────────────────

variable "pgadmin_email" {
  description = "pgAdmin default login email."
  type        = string
}

variable "pgadmin_password" {
  description = "pgAdmin default login password."
  type        = string
  sensitive   = true
}

# ── Frontend / Google Maps ────────────────────────────────────────────────────

variable "next_public_google_maps_api_key" {
  description = "Google Maps JavaScript API key (baked into the frontend image at build time)."
  type        = string
  sensitive   = true
}

variable "next_public_google_maps_map_id" {
  description = "Google Maps Map ID (baked into the frontend image at build time)."
  type        = string
}

variable "next_public_backend_url" {
  description = "Public URL of the backend API as seen from the browser (e.g. https://ca-backend-los-dev.<hash>.eastus.azurecontainerapps.io). Leave empty on the first apply, then re-apply after obtaining the backend URL from outputs."
  type        = string
  default     = ""
}

# ── Backend ───────────────────────────────────────────────────────────────────

variable "log_level" {
  description = "Log level for the backend service."
  type        = string
  default     = "INFO"
}

# ── Tags ──────────────────────────────────────────────────────────────────────

variable "tags" {
  description = "Additional tags to apply to all resources."
  type        = map(string)
  default     = {}
}
