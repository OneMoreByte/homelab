customization:
  extraKernelArgs:
    - talos.logging.kernel=udp://127.0.0.1:6050/
  systemExtensions:
    officialExtensions:
      - siderolabs/amd-ucode
      - siderolabs/amdgpu
      - siderolabs/iscsi-tools
      - siderolabs/nvme-cli
      - siderolabs/util-linux-tools
      - siderolabs/zfs
      - siderolabs/ctr
{{- if eq .Node.Host "producers.jsck.network" }}
      # Additional extensions for producers (bulk-datastore, Arc GPU)
      - siderolabs/nfsd
      - siderolabs/nfs-utils
      - siderolabs/xe
      - siderolabs/i915
      - siderolabs/mei # <- fw update interface for arc GPU
{{- end }}
