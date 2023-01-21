
terraform {
backend "azurerm" {
  container_name       = "tfstatestreamlit"
  key                  = "terraform.tfstate"
  
}
}