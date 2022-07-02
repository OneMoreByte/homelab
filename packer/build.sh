#!/bin/bash

# Cleanup old artifacts
echo "Cleaning old artifacts"
sudo rm -rf output* ./*.tar.gz

echo "Building"
export PACKER_LOG=1
sudo packer build .
