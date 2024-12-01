output "external-ip" {
  value = data.yandex_compute_instance.compute.network_interface.0.nat_ip_address
}
output "internal-ip" {
  value = data.yandex_compute_instance.compute.network_interface.0.ip_address
}

output "yc-user-passwd" {
  value     = random_password.yc-user-passwd.result
  sensitive = true
}

output "github-ci-passwd" {
  value     = random_password.github-ci-passwd.result
  sensitive = true
}
