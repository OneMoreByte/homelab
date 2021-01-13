#!/usr/bin/env python3

from jinja2 import Template
import gen_hostname
import os


def gen_lxc(name=gen_hostname.get_name(), image="ubuntu-20.04-standard_20.04-1_amd64.tar.gz", cores=1, memory=1024, storage=8):
   
    with open(f"{os.getenv('HOME')}/.ssh/id_ed25519.pub") as handle:
        ssh_key = handle.read().split()[1]

    with open("./templates/fateful_lxc_resource.tf.tmpl") as handle:
        template = handle.read()
    
    template_data = {
        "name": name,
        "image": image,
        "ssh_public_key": ssh_key,
        "cores": cores,
        "memory": memory,
        "storage": storage
    }

    lxc_resource = Template(template).render(template_data)

    with open("./homelab.tf", "a") as handle:
        handle.writelines(lxc_resource)

    return name

if __name__ == "__main__":
    gen_lxc()

