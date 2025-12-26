#!/bin/bash

# ================= 配置区域 =================

# 1. 镜像与容器名
IMAGE_NAME="winarena-v2:latest"
CONTAINER_NAME="win_server_only"

# 2. 虚拟机存储目录 (宿主机路径) -> 挂载为 /storage
HOST_STORAGE_DIR="/nvme/yangbowen/vm_stroage/waa_ding/golden_for_test"

# 4. 端口配置 (外部Client连接需要用到 API 端口)
PORT_BROWSER=5989  # 浏览器查看 VM
PORT_RDP=3399      # RDP 远程连接
PORT_API=5101      # HTTP API 端口 (外部 Client 通过这个控制 VM)

OPENAI_API_KEY="no use"
OPENAI_BASE_URL="no use"
# 5. 硬件配置
RAM_SIZE="8G"
CPU_CORES="8"

# ===========================================

# --- 1. 检查目录 ---
if [ ! -d "$HOST_STORAGE_DIR" ]; then
    echo "创建存储目录: $HOST_STORAGE_DIR"
    mkdir -p "$HOST_STORAGE_DIR"
fi

# --- 2. 检查 KVM ---
KVM_ARGS=""
KVM_ENV="N"
if [ -e /dev/kvm ]; then
    echo "✅ 检测到 KVM，启用硬件加速"
    KVM_ARGS="--device /dev/kvm"
    KVM_ENV="Y"
else
    echo "⚠️ 未检测到 KVM，性能受限"
fi

# --- 3. 清理旧容器 ---
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "删除旧容器: ${CONTAINER_NAME}..."
    docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1
fi

# --- 4. 启动逻辑 ---
# 逻辑说明：
# 1. 启动 entry.sh 初始化 VM。
# 2. sleep 15 等待初始化。
# 3. pkill -f python：杀掉容器内自带的 Client/Agent (如果有的话)，防止它抢占控制权。
# 4. tail -f /dev/null：保持容器不退出，等待你在宿主机运行代码连接。

CMD_STRING="
/usr/bin/tini -s /run/entry.sh &
# 然后等待VM服务器就绪
while true; do
  response=\$(curl --write-out '%{http_code}' --silent --output /dev/null localhost:5000/probe)
  echo 'Response {\$response}'
  if [ \$response -eq 200 ]; then
    break
  fi
  echo 'Waiting for Windows Arena Server...'
  sleep 5
done
echo 'Windows Arena Server is ready!!!!!!!!'
tail -f /dev/null
"

echo "🚀 正在启动服务容器..."

docker run -d \
    --name ${CONTAINER_NAME} \
    --privileged \
    --cap-add=NET_ADMIN \
    --stop-timeout 50 \
    --platform linux/amd64 \
    --device=/dev/kvm \
    -e KVM=Y \
    --add-host host.docker.internal:host-gateway \
    -p ${PORT_BROWSER}:8006 \
    -p ${PORT_RDP}:3389 \
    -p ${PORT_API}:5000 \
    -v "${HOST_STORAGE_DIR}:/storage" \
    -e RAM_SIZE=${RAM_SIZE} \
    -e CPU_CORES=${CPU_CORES} \
    -e OPENAI_API_KEY_FOR_CHECK_SETUP=${OPENAI_API_KEY} \
    -e OPENAI_BASE_URL_FOR_CHECK_SETUP=${OPENAI_BASE_URL} \
    --entrypoint /bin/bash \
    --shm-size "2g" \
    ${IMAGE_NAME} \
    -c "./entry_setup.sh & tail -f /dev/null"

echo "---------------------------------------------------"
echo "容器已启动! ID: $(docker ps -aq -f name=${CONTAINER_NAME} | head -n 1)"
echo "---------------------------------------------------"
echo "外部连接信息:"
echo "1. API 地址 (Client用): http://127.0.0.1:${PORT_API}"
echo "2. 浏览器 VNC:          http://127.0.0.1:${PORT_BROWSER}"
echo "3. RDP 远程桌面:        127.0.0.1:${PORT_RDP}"
echo "---------------------------------------------------"
echo "查看日志: docker logs -f ${CONTAINER_NAME}"