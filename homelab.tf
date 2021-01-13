
terraform {
  required_providers {
    proxmox = {
      source = "Telmate/proxmox"
      version = "2.6.7"
    }
  }
}

/*
storage: local-lvm
Network: vmbr1 192.168.13.0/24
*/
provider "proxmox" {
    alias = "fateful"
    pm_api_url = "https://fateful.localdomain:8006/api2/json"
    pm_tls_insecure = true
}

/*
storage: local-lvm
Network: vmbr0 192.168.1.0/24
*/
provider "proxmox" {
    alias = "books"
    pm_api_url = "https://books.localdomain:8006/api2/json"
    pm_tls_insecure = true
}

resource "proxmox_lxc" "abra" {
  provider     = proxmox.fateful
  target_node  = "fateful"
  hostname     = "abra.jackhil.de"
  ostemplate   = "local:vztmpl/ubuntu-20.04-standard_20.04-1_amd64.tar.gz"
  unprivileged = true
  start        = true
  onboot       = true

  ssh_public_keys = <<-EOT
    ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPa+cfjcC/sNWw+oGlGGFX2bcVvv21f6MU5LXVB2sfxo jsck
  EOT

  rootfs {
    storage = "local-lvm"
    size    = "30G"
  }

  network {
    name   = "eth0"
    bridge = "vmbr1"
    ip     = "dhcp"
  }

  cores  = 4
  memory = 2048
}