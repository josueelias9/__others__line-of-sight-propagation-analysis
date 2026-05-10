variable "project_name" {
  description = "Short project name used as prefix for all Azure resources"
  type        = string
  default     = "lospa"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "eastus"
}

# ── PostgreSQL ─────────────────────────────────────────────────────────────────

variable "postgres_admin_username" {
  description = "Administrator login username for PostgreSQL Flexible Server"
  type        = string
  sensitive   = true
}

variable "postgres_admin_password" {
  description = "Administrator login password (min 8 chars, must contain uppercase, lowercase, digit and symbol)"
  type        = string
  sensitive   = true
}

variable "postgres_db_name" {
  description = "Name of the application database to create"
  type        = string
}

variable "postgres_sku" {
  description = "PostgreSQL Flexible Server compute SKU"
  type        = string
  default     = "B_Standard_B1ms" # ~$12/mo — change to GP_Standard_D2s_v3 for production
}

# ── Frontend build-time variables ──────────────────────────────────────────────
# NEXT_PUBLIC_* are inlined by Next.js at build time, so they must be passed
# as Docker --build-arg when building the frontend image (see scripts/build_and_push.sh).

variable "next_public_google_maps_api_key" {
  description = "Google Maps API Key (baked into the frontend Docker image at build time)"
  type        = string
  sensitive   = true
}

variable "next_public_google_maps_map_id" {
  description = "Google Maps Map ID (baked into the frontend Docker image at build time)"
  type        = string
}

variable "auth_secret" {
  description = "Secret used by NextAuth v5 to sign tokens (generate with: openssl rand -base64 32)"
  type        = string
  sensitive   = true
}

variable "image_tag" {
  description = "Docker image tag to deploy on App Service"
  type        = string
  default     = "latest"
}
