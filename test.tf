locals {
  books_cluster_id    = "ff3006e8-43dc-11ec-8a56-00163e73ac2f"
  rocky_template_id   = "884c4302-85dd-433c-8838-c882d8c177a5"
  engine_user         = "admin@internal"
  engine_pass         = "[t1me]-to;hack"
}

terraform {
  required_providers {
    ovirt = {
        source  = "haveyoudebuggedit/ovirt"
        version = "0.3.1"
    }
  }
}

provider "ovirt" {
    url = "https://engine.jackhil.de/ovirt-engine/api/"
    username = local.engine_user
    password = local.engine_pass
    # Currently I need this. FIXME. Need to get cert from letsencrypt installed
    tls_insecure = true
}


resource "ovirt_vm" "ditto" {
  name        = "ditto"
  comment     = "HAProxy reverse proxy"
  cluster_id  = local.books_cluster_id
  template_id = local.rocky_template_id
}

resource "ovirt_vm" "umbreon" {
  name        = "umbreon"
  comment     = "Unifi controller"
  cluster_id  = local.books_cluster_id
  template_id = local.rocky_template_id
}

resource "ovirt_vm" "wooloo" {
  name        = "wooloo"
  comment     = "SSH Bastion"
  cluster_id  = local.books_cluster_id
  template_id = local.rocky_template_id
}
