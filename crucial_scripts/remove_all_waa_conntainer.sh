#!/bin/bash

# 定义需要清理的目标镜像列表
TARGET_IMAGES=(
    "windowsarena/winarena:latest"
    "winarena-v2:latest"
    "windowsarena/winarena-v2:latest"
)

# TARGET_IMAGES=(
#     "windowsarena/winarena:latest"
# )

echo "=========================================="
echo "开始清理指定镜像的容器..."
echo "=========================================="

for img in "${TARGET_IMAGES[@]}"; do
    echo "正在检查基于镜像 [ $img ] 的容器..."
    
    # 使用 ancestor 过滤器查找容器ID (-q 只输出ID, -a 包含已停止的)
    CONTAINER_IDS=$(docker ps -a -q --filter "ancestor=$img")
    
    if [ -n "$CONTAINER_IDS" ]; then
        echo "  -> 发现容器 ID: $(echo $CONTAINER_IDS | tr '\n' ' ')"
        
        # 停止容器
        echo "  -> 正在停止容器..."
        docker stop $CONTAINER_IDS 2>/dev/null
        
        # 删除容器
        echo "  -> 正在删除容器..."
        docker rm $CONTAINER_IDS
        
        echo "  -> [成功] 清理完毕"
    else
        echo "  -> [跳过] 未发现相关容器"
    fi
    echo "------------------------------------------"
done

echo "所有任务执行结束。"