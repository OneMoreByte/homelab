source "qemu" "rocky_86_cloudinit_maas" {
  communicator            = "none"
  iso_url                 = "https://download.rockylinux.org/pub/rocky/8/isos/x86_64/Rocky-8.6-x86_64-dvd1.iso"
  iso_checksum            = "file:https://download.rockylinux.org/pub/rocky/8/isos/x86_64/CHECKSUM"
  output_directory        = "output-qemu"
  disk_size               = "4G"
  memory                  = "2048"
  accelerator             = "kvm"
  http_directory          = "http"
  headless                = true
  qemuargs                = [[ "-serial", "stdio" ]]
  vm_name                 = "packer-qemu"
  net_device              = "virtio-net"
  net_bridge              = "br0"
  disk_interface          = "virtio"
  boot_wait               = "10s"
  shutdown_timeout        = "1h"
  boot_command            = ["<up><tab> text inst.ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/rocky8.6/ks.cfg console=ttyS0 inst.cmdline<enter><wait>"]
}

build {
  sources = ["source.qemu.rocky_86_cloudinit_maas"]
  post-processor "shell-local" {
    inline_shebang = "/bin/bash -e"
    inline = [
      "source ./packer-maas/scripts/setup-nbd",
      "OUTPUT=$${OUTPUT:-rocky-8.6.tar.gz}",
      "source ./packer-maas/scripts/tar-root"
    ]
  }
}

