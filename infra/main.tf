terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.110.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# FinOps Best Practice: Mandatory Governance Tags on every cloud resource
locals {
  finops_tags = {
    Project     = "QuantGuard-Risk-API"
    Environment = "Production"
    CostCenter  = "FinEng-Quant-001"
    ManagedBy   = "Terraform-FinOps"
  }
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-quantguard-calgary"
  location = "canadacentral"
  tags     = local.finops_tags
}

resource "azurerm_container_app_environment" "env" {
  name                = "cae-quantguard"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.finops_tags
}

resource "azurerm_container_app" "app" {
  name                         = "ca-quantguard-api"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"
  tags                         = local.finops_tags

  template {
    # FinOps Optimization: Scale to 0 when idle ($0 compute waste), cap at 2 replicas
    min_replicas = 0
    max_replicas = 2

    container {
      name   = "quant-guard-api"
      image  = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}