#!/bin/bash

# ==============================================================================
# Script to stop and remove running Docker containers based on a specific image.
# Target Image: happysixd/osworld-docker
# Includes a safety check and a confirmation prompt.
# Now supports --exclude parameter to skip specific container IDs.
# ==============================================================================

# --- 配置 ---
TARGET_IMAGE="happysixd/osworld-docker"
EXCLUDE_IDS=()

# 设置颜色以便输出更清晰
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- 函数定义 ---
usage() {
    echo "用法: $0 [--exclude ID1,ID2,...]"
    echo "示例: $0 --exclude abc123,def456"
    echo "       $0 (无参数，处理所有容器)"
    exit 1
}

# --- 参数解析 ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --exclude)
            if [[ -n "$2" ]]; then
                IFS=',' read -ra EXCLUDE_IDS <<< "$2"
                shift 2
            else
                echo -e "${RED}错误: --exclude 参数需要指定容器ID${NC}"
                usage
            fi
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}未知参数: $1${NC}"
            usage
            ;;
    esac
done

echo -e "${YELLOW}Finding running containers based on image: ${TARGET_IMAGE}...${NC}"

# 1. 获取所有基于指定镜像且正在运行的容器ID
CONTAINER_IDS=$(docker ps -a --filter "ancestor=${TARGET_IMAGE}" -q)

# 2. 检查是否有符合条件的容器
if [ -z "$CONTAINER_IDS" ]; then
  echo -e "${GREEN}No running containers found for image '${TARGET_IMAGE}'. Nothing to do.${NC}"
  exit 0
fi

# 3. 过滤掉需要排除的容器ID
FILTERED_IDS=()
for container_id in $CONTAINER_IDS; do
    should_exclude=false
    for exclude_id in "${EXCLUDE_IDS[@]}"; do
        # 支持完整ID或部分ID匹配
        if [[ "$container_id" == *"$exclude_id"* ]]; then
            echo -e "${YELLOW}排除容器: $container_id (匹配排除ID: $exclude_id)${NC}"
            should_exclude=true
            break
        fi
    done
    if [ "$should_exclude" = false ]; then
        FILTERED_IDS+=("$container_id")
    fi
done

# 4. 检查过滤后是否还有容器需要操作
if [ ${#FILTERED_IDS[@]} -eq 0 ]; then
    echo -e "${GREEN}所有匹配的容器已被排除，无需操作。${NC}"
    exit 0
fi

# 5. 列出将要被操作的容器，给用户确认
echo -e "${YELLOW}以下基于镜像 '${TARGET_IMAGE}' 的容器将被停止和删除:${NC}"
for container_id in "${FILTERED_IDS[@]}"; do
    docker ps --filter "id=$container_id" --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"
done

echo "" # 打印一个空行

# 6. 确认操作
read -p "确定要继续吗? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}操作已取消。${NC}"
    exit 0
fi

# 7. 执行停止和删除操作
echo -e "${YELLOW}正在停止容器...${NC}"
for container_id in "${FILTERED_IDS[@]}"; do
    echo "停止容器: $container_id"
    docker stop "$container_id"
done

echo -e "${YELLOW}正在删除容器...${NC}"
for container_id in "${FILTERED_IDS[@]}"; do
    echo "删除容器: $container_id"
    docker rm "$container_id"
done

echo -e "${GREEN}操作完成!${NC}"
exit 0