#!/bin/bash

# ==============================================================================
# Bash script to run the happysixd/osworld-docker container.
# This script is an equivalent of the provided Python docker-py code.
#
# Before running, please configure the variables in the "CONFIGURATION" section.
# ==============================================================================

# --- CONFIGURATION ---
# 请根据您的实际情况修改以下变量

# 容器和镜像名称
IMAGE_NAME="happysixd/osworld-docker"
# CONTAINER_NAME="os-world-jkm" # 为容器指定一个唯一的名称

# 资源配置 (对应 Python 中的 self.environment)
DISK_SIZE="32G"
RAM_SIZE="4G"
CPU_CORES="4"

# 卷挂载 (对应 Python 中的 volumes)
# !! 重要: 请将 "/path/to/your/vm.qcow2" 替换为您宿主机上 .qcow2 文件的真实绝对路径
PATH_TO_VM_QCOW2="/nvme/yangbowen/osworld/docker_vm_data/Ubuntu.qcow2"

# 端口映射 (对应 Python 中的 ports)
# 格式: <宿主机端口>:<容器端口>
HOST_VNC_PORT=5923     # VNC 端口, 对应 self.vnc_port
HOST_SERVER_PORT=5099    # Server 端口, 对应 self.server_port
HOST_CHROMIUM_PORT=9289  # Chromium 调试端口, 对应 self.chromium_port
HOST_VLC_PORT=8199       # VLC 端口, 对应 self.vlc_port

# --- SCRIPT LOGIC ---
# 通常不需要修改以下部分

# 检查 qcow2 文件路径是否存在
if [ ! -f "$PATH_TO_VM_QCOW2" ]; then
    echo "Error: The QCOW2 file path does not exist: $PATH_TO_VM_QCOW2"
    echo "Please edit the script and set the PATH_TO_VM_QCOW2 variable correctly."
    exit 1
fi

echo "Attempting to stop and remove any existing container with the name '$CONTAINER_NAME'..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

echo "Starting a new container named '$CONTAINER_NAME'..."

docker run \
    -d \
    --rm \
    -e "DISK_SIZE=${DISK_SIZE}" \
    -e "RAM_SIZE=${RAM_SIZE}" \
    -e "CPU_CORES=${CPU_CORES}" \
    --cap-add=NET_ADMIN \
    --device=/dev/kvm \
    -v "${PATH_TO_VM_QCOW2}:/System.qcow2:ro" \
    -p "${HOST_VNC_PORT}:8006" \
    -p "${HOST_SERVER_PORT}:5000" \
    -p "${HOST_CHROMIUM_PORT}:9222" \
    -p "${HOST_VLC_PORT}:8080" \
    "$IMAGE_NAME"

# 检查容器是否成功启动
if [ $? -eq 0 ]; then
    echo "Container '$CONTAINER_NAME' started successfully."
    echo "You can check its logs with: docker logs -f $CONTAINER_NAME"
    echo "To access the container shell, run: docker exec -it $CONTAINER_NAME /bin/bash"
else
    echo "Error: Failed to start container '$CONTAINER_NAME'."
    echo "Check the docker daemon logs for more details."
fi