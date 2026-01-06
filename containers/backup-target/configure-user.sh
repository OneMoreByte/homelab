#!/usr/bin/env bash

USER=$1

if [ -z $USER ]; then
  echo "invalid string $USER"
  exit 1
fi

if ! id "${USER}" &>/dev/null; then
  echo "user isn't configured in image";
  exit 1
fi

DATASET="store/backups/foreign/${USER}"
DATASET_PERMISSIONS="create,mount,snapshot,rollback,clone,promote,rename,receive,send,hold,release,diff"
CHILDREN_ONLY_PERMISSIONS="destroy"

if ! zfs allow $DATASET | grep -q "${USER}"; then
  zfs allow "${USER}" "${DATASET_PERMISSIONS}" "${DATASET}"
  zfs allow -d "${USER}" "${CHILDREN_ONLY_PERMISSIONS}" "${DATASET}"
fi

chown -R "${USER}:${USER}" "/home/${USER}"