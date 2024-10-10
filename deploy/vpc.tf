# https://terraform-provider.yandexcloud.net/Resources/vpc_network
resource "yandex_vpc_network" "network" {
  name      = "prod-vpc"
  folder_id = var.folder_id
}

# https://terraform-provider.yandexcloud.net/Resources/vpc_subnet
resource "yandex_vpc_subnet" "subnet-a" {
  name           = "prod-vpc-subnet-a"
  zone           = var.zone
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.0.0.0/24"]
}
