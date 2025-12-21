import io
from PIL import Image
import logging

# 假设 logger 已经定义
logger = logging.getLogger("desktopenv.providers.macos")

def compress_image_data(image_bytes: bytes, quality: int = 85, format: str = "JPEG") -> bytes:
    """
    Compress image bytes without changing resolution.
    
    :param image_bytes: The original image data in bytes.
    :param quality: Compression quality (1-100). Lower is smaller but worse looking.
                    For JPEG, 85 is a good balance. For PNG, this is ignored or used for optimization levels.
    :param format: Output format. 'JPEG' is best for size. 'PNG' is lossless but larger.
    :return: Compressed image data as bytes.
    """
    if not image_bytes:
        return b""

    try:
        # 1. 将字节流转换为 PIL Image 对象
        image_stream = io.BytesIO(image_bytes)
        img = Image.open(image_stream)
        
        # 如果原图是 RGBA (例如 PNG 带透明通道) 且要转为 JPEG，必须先转为 RGB，否则会报错
        if format.upper() == "JPEG" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # 2. 创建一个字节流用于存储压缩后的数据
        output_stream = io.BytesIO()

        # 3. 保存并压缩
        if format.upper() == "JPEG":
            # optimize=True 会多花一点时间进行算法优化以减小体积
            img.save(output_stream, format="JPEG", quality=quality, optimize=True)
        elif format.upper() == "PNG":
            # PNG 是无损的，quality 参数不适用，但可以用 optimize=True
            # 如果想极致压缩 PNG，可以使用 quantize 减少颜色数量（会有损画质）
            # img = img.quantize(colors=256) # 可选：将颜色减少到 256 色，体积会剧减
            img.save(output_stream, format="PNG", optimize=True)
        
        # 4. 获取压缩后的字节
        compressed_data = output_stream.getvalue()
        
        original_size = len(image_bytes) / 1024
        new_size = len(compressed_data) / 1024
        logger.info(f"Image compressed ({format}): {original_size:.2f}KB -> {new_size:.2f}KB")

        return compressed_data

    except Exception as e:
        # 如果压缩失败，返回原始数据以防万一
        return image_bytes
