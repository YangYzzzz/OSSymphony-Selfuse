import base64
import re
import os
import pprint
from io import BytesIO
from typing import Tuple, List, Dict, Optional
from collections import defaultdict

# 图像处理
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# OCR 引擎
import pytesseract
from pytesseract import Output
import easyocr

# --- 配置区域 ---
# Windows 用户如果未配置环境变量，请取消注释并修改路径：
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRProcessor:
    """
    统一 OCR 处理器，支持 Tesseract 和 EasyOCR 两种模式。
    """
    def __init__(self, use_gpu: bool = False, languages: List[str] = ['en']):
        """
        初始化处理器。
        
        Args:
            use_gpu (bool): EasyOCR 是否使用 GPU。
            languages (List[str]): EasyOCR 支持的语言列表，如 ['en', 'ch_sim']。
        """
        self.use_gpu = use_gpu
        self.languages = languages
        self.reader = None # 懒加载 EasyOCR Reader

    def _get_easyocr_reader(self):
        """单例模式获取 EasyOCR Reader，避免重复加载模型。"""
        if self.reader is None:
            print(f"正在加载 EasyOCR 模型 (GPU={self.use_gpu})...")
            self.reader = easyocr.Reader(self.languages, gpu=self.use_gpu)
        return self.reader

    def get_ocr_elements(self, bytes_image_data: bytes, mode: str = 'tesseract') -> Tuple[str, List[Dict]]:
        """
        执行 OCR 识别。

        Args:
            bytes_image_data (str): Base64 编码的图像字符串。
            mode (str): 'tesseract' (速度快) 或 'easyocr' (准确率高，支持复杂背景)。

        Returns:
            Tuple[str, List]: (文本表格字符串, 元素详情列表)
        """
        try:
            image = Image.open(BytesIO(bytes_image_data))
        except Exception as e:
            print(f"Error decoding or opening image: {e}")
            return "", []

        if mode == 'tesseract':
            return self._process_tesseract(image)
        elif mode == 'easyocr':
            return self._process_easyocr(image)
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'tesseract' or 'easyocr'.")

    def _process_tesseract(self, image: Image.Image) -> Tuple[str, List[Dict]]:
        """Tesseract 处理逻辑"""
        # output_type=Output.DICT 返回字典格式
        data = pytesseract.image_to_data(image, output_type=Output.DICT)
        
        ocr_elements = []
        ocr_table = "Text Table (Tesseract):\nWord id\tText\n"
        ocr_id = 0

        num_boxes = len(data['text'])
        for i in range(num_boxes):
            # 过滤置信度低或空的文本
            if int(data['conf'][i]) > 0 and data['text'][i].strip():
                # 清洗文本
                clean_text = re.sub(r"^[^a-zA-Z0-9\s.,!?;:\-\+]+|[^a-zA-Z0-9\s.,!?;:\-\+]+$", "", data['text'][i])
                if not clean_text: continue

                ocr_table += f"{ocr_id}\t{clean_text}\n"
                
                ocr_elements.append({
                    "id": ocr_id,
                    "text": clean_text,
                    "mode": "tesseract",
                    "left": data["left"][i],
                    "top": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i],
                    "conf": data["conf"][i]
                })
                ocr_id += 1
        
        return ocr_table, ocr_elements

    def _process_easyocr(self, image: Image.Image) -> Tuple[str, List[Dict]]:
        """EasyOCR 处理逻辑"""
        reader = self._get_easyocr_reader()
        
        # EasyOCR 需要 numpy array
        image_np = np.array(image)
        
        # detail=1 返回 (bbox, text, conf)
        results = reader.readtext(image_np, detail=1, paragraph=False, width_ths=0.1)
        
        ocr_elements = []
        ocr_table = "Text Table (EasyOCR):\nWord id\tText\n"
        ocr_id = 0
        
        for (bbox, text, conf) in results:
            clean_text = re.sub(r"^[^a-zA-Z0-9\s.,!?;:\-\+]+|[^a-zA-Z0-9\s.,!?;:\-\+]+$", "", text)
            if not clean_text.strip(): continue

            # --- 坐标转换 ---
            # EasyOCR 返回 [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            # 我们将其转换为 left, top, width, height
            (tl, tr, br, bl) = bbox
            tl = [int(v) for v in tl]
            br = [int(v) for v in br]
            
            left = min(tl[0], bl[0])
            top = min(tl[1], tr[1])
            right = max(tr[0], br[0])
            bottom = max(bl[1], br[1])
            
            width = right - left
            height = bottom - top
            # ---------------

            ocr_table += f"{ocr_id}\t{clean_text}\n"
            
            ocr_elements.append({
                "id": ocr_id,
                "text": clean_text,
                "mode": "easyocr",
                "left": left,
                "top": top,
                "width": width,
                "height": height,
                "conf": float(conf)
            })
            ocr_id += 1

        return ocr_table, ocr_elements

    @staticmethod
    def visualize_ocr_results(image_path: str, ocr_elements: List[Dict], output_path: str):
        """
        可视化方法：在原图上绘制边界框和ID。
        """
        try:
            image = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(image)

            # 字体加载
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except IOError:
                font = ImageFont.load_default()

            for element in ocr_elements:
                left, top = element["left"], element["top"]
                width, height = element["width"], element["height"]
                
                # 根据模式选择颜色
                color = "green" if element.get("mode") == "easyocr" else "red"
                
                # 1. 绘制矩形框
                draw.rectangle([(left, top), (left + width, top + height)], outline=color, width=2)
                
                # 2. 绘制文字标签（带背景，防止看不清）
                text_str = str(element["id"])
                
                # 获取文字宽高 (兼容旧版 Pillow)
                if hasattr(draw, "textbbox"):
                    bbox = draw.textbbox((0, 0), text_str, font=font)
                    text_w, text_h = bbox[2]-bbox[0], bbox[3]-bbox[1]
                else:
                    text_w, text_h = draw.textsize(text_str, font=font)
                
                # 标签背景位置 (在框的上方)
                label_bg = [left, top - text_h - 4, left + text_w + 4, top]
                draw.rectangle(label_bg, fill=color)
                
                # 绘制文字
                draw.text((left + 2, top - text_h - 4), text_str, fill="white", font=font)

            image.save(output_path)
            print(f"Visualization saved to: {output_path}")

        except FileNotFoundError:
            print(f"Error: Image {image_path} not found.")
        except Exception as e:
            print(f"Visualization error: {e}")


def main():
    # --- 设置图片路径 ---
    image_path = "/nvme/yangbowen/yangbowen/InternGUIFramework/test/step_10.png"
    
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found.")
        return

    # 读取图片并转为 Base64 (模拟你的输入环境)
    with open(image_path, "rb") as f:
        bytes_data = f.read()

    # 初始化处理器 (支持中英文: ['en', 'ch_sim'])
    processor = OCRProcessor(use_gpu=False, languages=['en'])

    # --- 模式 1: 使用 Tesseract ---
    print("\n=== Mode: Tesseract ===")
    table_tess, elements_tess = processor.get_ocr_elements(bytes_data, mode='tesseract')
    if elements_tess:
        print(table_tess)
        output_path = image_path.replace(".png", "_tesseract_vis.png")
        OCRProcessor.visualize_ocr_results(image_path, elements_tess, output_path)
    else:
        print("Tesseract found nothing.")

    # --- 模式 2: 使用 EasyOCR ---
    print("\n=== Mode: EasyOCR ===")
    table_easy, elements_easy = processor.get_ocr_elements(bytes_data, mode='easyocr')
    if elements_easy:
        print(table_easy)
        output_path = image_path.replace(".png", "_easyocr_vis.png")
        OCRProcessor.visualize_ocr_results(image_path, elements_easy, output_path)
    else:
        print("EasyOCR found nothing.")

if __name__ == "__main__":
    main()