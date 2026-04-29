variable "name" {
  description = "ACR name (alphanumeric, 5-50 chars, globally unique)."
  type        = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "sku" {
  description = "ACR SKU: Basic, Standard, or Premium."
  type        = string
  default     = "Basic"
}

variable "tags" {
  type    = map(string)
  default = {}
}
