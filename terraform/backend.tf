
terraform {
backend "azurerm" {
  container_name       = "tfstatestreamlit"
  key                  = "terraform.tfstate"
  sas_token = "?sv=2021-06-08&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2023-01-22T03:11:30Z&st=2023-01-21T19:11:30Z&spr=https&sig=aNODvjP7BCW35XAxHyqbun9huYPR1eUgFMtHGkoCEj8%3D"
  
}
}