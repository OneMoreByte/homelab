locals {
  default_cluster_id   = "ed6629ac-6da2-11ec-9ce2-00163e73ac2f"
  rocky_template_id    = "c3c17b7a-68e5-4577-9dc4-1cd880c3b81c"
  k8s_node_template_id = "9414af81-4e12-4364-a526-24b7c1432553"
  engine_user          = "admin@internal"
  engine_pass          = "[t1me]-to;hack"
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

// A note on adding machines. REMEMBER: you need to do cloud-init manually until they can finish the code changes to the provider

resource "ovirt_vm" "ditto" {
  name        = "ditto"
  comment     = "HAProxy reverse proxy"
  cluster_id  = local.default_cluster_id
  template_id = local.rocky_template_id
}

resource "ovirt_vm" "umbreon" {
  name        = "umbreon"
  comment     = "Unifi controller"
  cluster_id  = local.default_cluster_id
  template_id = local.rocky_template_id
}

resource "ovirt_vm" "wooloo" {
  name        = "wooloo"
  comment     = "SSH Bastion"
  cluster_id  = local.default_cluster_id
  template_id = local.rocky_template_id
}


resource "ovirt_vm" "wailord" {
  // We want 4 nodes. 
  count        = 4

  name         = "wailord-node-${count.index}"
  comment      = "Kubernetes node ${count.index}"
  cluster_id   = local.default_cluster_id
  template_id  = local.k8s_node_template_id
}


resource "ovirt_vm" "klefki" {
  name        = "klefki"
  comment     = "FreeIPA server"
  cluster_id  = local.default_cluster_id
  template_id = local.rocky_template_id
}
