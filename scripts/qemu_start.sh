/usr/libexec/qemu-kvm \
    -m 4G \
    -smp 4 \
    -enable-kvm \
    -drive file=/nvme/yangbowen/osworld/docker_vm_data/Ubuntu-with-proxy.qcow2,format=qcow2,if=virtio \
    -vnc :1 \
    -netdev user,id=net0 \
    -device virtio-net-pci,netdev=net0 \
    -usb \
    -device usb-tablet