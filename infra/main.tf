terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }

  # Uncomment to store state in Azure Blob Storage (recommended for teams)
  # backend "azurerm" {
  #   resource_group_name  = "rg-tfstate"
  #   storage_account_name = "stterraformstate"
  #   container_name       = "tfstate"
  #   key                  = "los.tfstate"
  # }
}

provider "azurerm" {
  features {}
}

locals {
  name_suffix = "${var.project}-${var.env}"
  tags = merge(var.tags, {
    project     = var.project
    environment = var.env
    managed_by  = "terraform"
  })
}

module "resource_group" {
  source   = "./modules/resource_group"
  name     = "rg-${local.name_suffix}"
  location = var.location
  tags     = local.tags
}

module "network" {
  source              = "./modules/network"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  vnet_name           = "vnet-${local.name_suffix}"
  tags                = local.tags
}

module "acr" {
  source              = "./modules/acr"
  name                = "acr${replace(local.name_suffix, "-", "")}"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  tags                = local.tags
}

module "database" {
  source              = "./modules/database"
  name                = "psql-${local.name_suffix}"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  subnet_id           = module.network.db_subnet_id
  vnet_id             = module.network.vnet_id
  db_name             = var.db_name
  db_username         = var.db_username
  db_password         = var.db_password
  tags                = local.tags
}

module "container_apps" {
  source              = "./modules/container_apps"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  name_suffix         = local.name_suffix
  subnet_id           = module.network.apps_subnet_id

  acr_login_server = module.acr.login_server
  acr_username     = module.acr.admin_username
  acr_password     = module.acr.admin_password
  image_tag        = var.image_tag

  db_host     = module.database.fqdn
  db_port     = "5432"
  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password

  next_public_google_maps_api_key = var.next_public_google_maps_api_key
  next_public_google_maps_map_id  = var.next_public_google_maps_map_id
  next_public_backend_url         = var.next_public_backend_url

  pgadmin_email    = var.pgadmin_email
  pgadmin_password = var.pgadmin_password

  log_level = var.log_level
  tags      = local.tags
}
