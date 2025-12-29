#!/bin/bash

# Lifted from https://github.com/heavybullets8/zfs-scrubber
exit_bool=false

if [ -z "$TALOS_VERSION" ]; then
    echo "Error: TALOS_VERSION environment variable not set."
    exit_bool=true
elif ! ZFS_IMAGE=$(crane export "ghcr.io/siderolabs/extensions:${TALOS_VERSION}" | tar x -O image-digests | grep zfs | awk '{print $1}'); then
    echo "Error: Could not find a compatible ZFS extension for Talos $TALOS_VERSION."
    exit_bool=true
fi

if [ "$exit_bool" = false ]; then
    echo "Verifying ZFS image signature..."
    if ! cosign verify \
        --certificate-identity-regexp '@siderolabs\.com$' \
        --certificate-oidc-issuer https://accounts.google.com \
        "$ZFS_IMAGE" >/dev/null 2>&1; then
        echo "Error: Image signature verification failed for $ZFS_IMAGE."
        exit_bool=true
    fi
fi

if [ "$exit_bool" = true ]; then
    echo "Exiting due to previous errors..."
    exit 1
fi

echo "Installing ZFS from $ZFS_IMAGE..."
if ! crane export "$ZFS_IMAGE" | tar --strip-components=1 -x -C /; then
    echo "Error: Failed to extract ZFS extension."
    exit 1
fi
echo