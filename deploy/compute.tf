locals {
  username     = "yc-user"
  ssh_key_path = "~/.ssh/dev-hosts.pub"
}

data "yandex_compute_image" "container-optimized-image" {
  family = "container-optimized-image"
}

resource "random_password" "yc-user-passwd" {
  length  = 20
  upper   = true
  lower   = true
  numeric = true
  special = true
}

resource "random_password" "github-ci-passwd" {
  length  = 20
  upper   = true
  lower   = true
  numeric = true
  special = true
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
        yc-user-passwd    = random_password.yc-user-passwd.bcrypt_hash,
        yc-user-ssh-key   = file("~/.ssh/dev-hosts.pub"),
        github-ci-passwd  = random_password.github-ci-passwd.bcrypt_hash,
        github-ci-ssh-key = file("~/.ssh/github-ci.pub"),
    })
  }
}

data "yandex_compute_instance" "compute" {
  instance_id = yandex_compute_instance.compute.id
}

