//resource group is created before hand
//storage account and container are created before hand for state files
//check the basch script

data "azurerm_client_config" "current" {

}

data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}
resource "azurerm_storage_account" "infra" {
  name = "${var.project}infra${terraform.workspace}"
  resource_group_name = data.azurerm_resource_group.main.name
  location = var.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  lifecycle {
  ignore_changes = [
    tags,
  ]
}
}
#Key vaut for storing your secrets that will be used in with your function upp
resource "azurerm_key_vault" "infra" {
  name                = "kv-${var.project}-${terraform.workspace}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  tenant_id           = var.ARM_TENANT_ID
  sku_name            = "standard"
}

resource "azurerm_service_plan" "infra" {
  name = "ASP-linux-${var.project}-${terraform.workspace}"
  resource_group_name = data.azurerm_resource_group.main.name
  location = data.azurerm_resource_group.main.location
  os_type = "Linux"
  sku_name = "B1"

    lifecycle {
    create_before_destroy = true
    ignore_changes = [
      tags
    ]
  }
}

resource "azurerm_linux_web_app" "streamlit" {
  name                = "${var.project}-${terraform.workspace}"
  resource_group_name = data.azurerm_resource_group.main.name
  location            = data.azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.infra.id
  https_only = true


  site_config {
    always_on = true
    application_stack {
      
      python_version = 3.9
    }
  
 }
}
