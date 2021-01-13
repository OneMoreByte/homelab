#!/usr/bin/env python3

import gen_lxc
import handle_inventory

def create_minecraft_lxc(cores, memory, storage):
    name = gen_lxc.gen_lxc(cores=cores, memory=memory, storage=storage)
    handle_inventory.add_role(name, "minecraft")


if __name__ == "__main__":
    while True:
        cores = input("vcores #: ")
        memory = input("memory (in mb): ")
        storage = input("root partion size (in gb): ")
        print(f"\nvcores: {cores}")
        print(f"memory: {memory}MB")
        print(f"disk: {storage}GB")
        if input("Is this ok? (yes): ") == "yes":
            break
    create_minecraft_lxc(cores, memory, storage)