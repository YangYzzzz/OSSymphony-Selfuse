import base64
import json
import logging
import os
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from PIL import Image



def _calculate_image_similarity(b64_img1: str, b64_img2: str) -> float:
    """
    计算两张Base64图像的相似度
    通过缩小分辨率（提升速度并容忍极小噪点）后计算 Mean Absolute Error。
    """
    try:
        img1 = Image.open(BytesIO(base64.b64decode(b64_img1))).convert("RGB")
        img2 = Image.open(BytesIO(base64.b64decode(b64_img2))).convert("RGB")
        
        # 统一缩放到较小尺寸进行比较，加速运算并过滤轻微渲染差异
        # img1 = img1.resize((256, 256))
        # img2 = img2.resize((256, 256))
        
        arr1 = np.array(img1, dtype=np.float32)
        arr2 = np.array(img2, dtype=np.float32)
        
        # 计算平均绝对误差，取值范围在 0 ~ 255 之间
        mae = np.mean(np.abs(arr1 - arr2))
        
        # 归一化为 0~1 的相似度 (1 为完全一致)
        similarity = 1.0 - (mae / 255.0)
        return similarity
    except Exception as e:
        # 如果解析失败，默认返回0 (即判定为不相似，保留原图)
        print(f"Error calculating similarity: {e}")
        return 0.0