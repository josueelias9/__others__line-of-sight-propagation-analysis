variable "name" {
  description = "PostgreSQL Flexible Server name (globally unique)."
  type        = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "subnet_id" {
  description = "ID of the delegated subnet for the PostgreSQL server."
  type        = string
}

variable "vnet_id" {
  description = "ID of the VNet to link the private DNS zone to."
  type        = string
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

variable "tags" {
  type    = map(string)
  default = {}
}
