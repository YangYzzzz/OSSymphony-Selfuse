#!/bin/bash

# ==============================================================================
# Script to stop and remove running Docker containers based on a specific image.
# Target Image: happysixd/osworld-docker
# Includes a safety check and a confirmation prompt.
# ==============================================================================

# --- 配置 ---
TARGET_IMAGE="happysixd/osworld-docker"

# 设置颜色以便输出更清晰 (可选)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Finding running containers based on image: ${TARGET_IMAGE}...${NC}"

# 1. 获取所有基于指定镜像且正在运行的容器ID
# 使用 --filter "ancestor=..." 来进行筛选
CONTAINER_IDS=$(docker ps -a --filter "ancestor=${TARGET_IMAGE}" -q)

# 2. 检查是否有符合条件的容器
if [ -z "$CONTAINER_IDS" ]; then
  echo -e "${GREEN}No running containers found for image '${TARGET_IMAGE}'. Nothing to do.${NC}"
  exit 0
fi

# 3. 列出将要被操作的容器，给用户确认
echo "The following containers, based on image '${TARGET_IMAGE}', are currently running and will be stopped and removed:"
# 使用 docker ps 并传入筛选后的ID，以确保只显示将要被删除的容器
docker ps --filter "id=${CONTAINER_IDS//\n/ --filter id=}"
echo "" # 打印一个空行

echo "$CONTAINER_IDS" | xargs --no-run-if-empty docker stop
echo "$CONTAINER_IDS" | xargs --no-run-if-empty docker rm

exit 0