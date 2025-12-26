#!/bin/bash

# 在RealVNC內连接vnc_port!!!

# 1. 定义配置变量
docker_name="mac_test"
host_port=8005
vnc_port=5929
ssh_user="pipiwu"
ssh_pass="1234"

# 2. 启动 Docker 容器
echo "Starting Docker container: $docker_name ..."
sudo docker run -itd \
    --name "$docker_name" \
    --device /dev/kvm \
    -p "$host_port":10022 \
    -p "$vnc_port":5901 \
    -e EXTRA="-vnc 0.0.0.0:1,password=off" \
    -e RAM_SIZE="16G" \
    -e CPU_CORES="8" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e CPU='Haswell-noTSX' \
    -e CPUID_FLAGS='kvm=on,vendor=GenuineIntel,+invtsc,vmware-cpuid-freq=on' \
    -v "/nvme/yangbowen/vm_stroage/macos/mac_hdd_ng_copy.img:/home/arch/OSX-KVM/mac_hdd_ng_src.img" \
    -v "/nvme/yangbowen/vm_stroage/macos/BaseSystem.img:/home/arch/OSX-KVM/BaseSystem_src.img" \
    -e SHORTNAME=sonoma \
    -e USERNAME="$ssh_user" \
    -e PASSWORD="$ssh_pass" \
    numbmelon/docker-osx-evalkit-auto:latest

# 3. 循环检测 SSH 连接
echo "---------------------------------------------------"
echo "Waiting for SSH service on localhost:$host_port..."
echo "User: $ssh_user"
echo "---------------------------------------------------"

# 检查是否安装了 sshpass，如果没有则提示
if ! command -v sshpass &> /dev/null; then
    echo "Error: sshpass is not installed. Please install it (e.g., sudo apt install sshpass) to use this script."
    exit 1
fi

# 开始循环
# -o StrictHostKeyChecking=no: 不询问 host key 确认（因为是新容器，key 可能会变）
# -o UserKnownHostsFile=/dev/null: 不将 key 写入 known_hosts 文件，避免污染本地配置
# -o ConnectTimeout=2: 设置超时时间为2秒，避免卡住太久
while ! sshpass -p "$ssh_pass" ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -o ConnectTimeout=2 \
    -p "$host_port" \
    "$ssh_user"@localhost "echo 'SSH Ready'"; do
    
    echo "SSH not ready yet. Retrying in 5 seconds..."
    sleep 5
done

echo "---------------------------------------------------"
echo "✅ SSH Connection Successful! The container is ready."
echo "You can now connect using:"
echo "sshpass -p '$ssh_pass' ssh -p $host_port $ssh_user@localhost"
echo "---------------------------------------------------"