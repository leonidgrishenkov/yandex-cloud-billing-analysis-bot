locals {
  username     = "yc-user"
  ssh_key_path = "~/.ssh/dev-hosts.pub"
}

data "yandex_compute_image" "container-optimized-image" {
  family = "container-optimized-image"
}

resource "random_password" "compute-password" {
  length  = 15
  upper   = true
  lower   = true
  numeric = true
  special = false
}


resource "yandex_compute_instance" "compute" {
  name        = "prod-compute-1"
  hostname    = "prod-compute-1"
  platform_id = "standard-v3"
  zone        = var.zone
  folder_id   = var.folder_id

  resources {
    cores         = 2
    memory        = 2
    core_fraction = 100
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.container-optimized-image.id
      type     = "network-hdd"
      size     = 40
    }
    auto_delete = true
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.subnet-a.id
    security_group_ids = [yandex_vpc_security_group.sg.id]
    nat                = true
    ipv4               = true
  }

  metadata = {
    user-data = templatefile("./cloud-init.yaml",
      {
        ssh_key_path = file("${local.ssh_key_path}"),
        username     = local.username,
        passwd       = random_password.compute-password.bcrypt_hash,
    })
  }
}

data "yandex_compute_instance" "compute" {
  instance_id = yandex_compute_instance.compute.id
}

