"""
    循环检测算法实现
    我现在是在做一个
    输入: List[Tuple(Image(二进制流), Action)]
    其中 Action 是字典, 比如 {"function": "click", "args": {"x": 1000, "y": 200}}这种
    现在我需要用基于规则的算法判断当前步骤是否出现了重复模式, 以便于大模型进一步识别
    当前步骤: 列表中最后一个元素
    重复模式: 以下是我的个人见解，给定一个循环步数N=3, 我们检测最近的N个步骤是否和以往的N步相似，这个相似的算法可能需要你来设计，通过图片相似度与动作相似度来判断, 当然其实我认为动作相似度没有那么重要
    或者说主要取决于图片相似度, 其次再是动作相似度, 图片相似度需要非常严格, 动作相似度可能需要着重参考一下点击的坐标即可
    我的核心宗旨是尽可能不出错，没有发生循环时一定不要认为是循环，真正循环出现时能检测出部分即可
    输出: 不只需要返回是否循环，还要返回在哪几步产生循环
"""

import io
from typing import List, Tuple, Dict, Any, Optional, Union
from PIL import Image
import imagehash
import math

# 定义数据结构类型别名，增强代码可读性
Action = Dict[str, Any]
Step = Tuple[bytes, Action]
History = List[Step]

# --- 相似度计算辅助函数 ---

def _calculate_phash(image_binary: bytes) -> Optional[imagehash.ImageHash]:
    """
    计算图片二进制流的感知哈希值。
    
    Args:
        image_binary: 图片的二进制数据。
        
    Returns:
        返回 imagehash 对象，如果图片无法处理则返回 None。
    """
    try:
        image = Image.open(io.BytesIO(image_binary))
        # 使用 pHash 算法，它对图片内容的微小变化不敏感
        return imagehash.phash(image)
    except Exception:
        # 如果二进制流不是有效的图片格式，则无法计算哈希
        return None

def _are_actions_similar(
    action1: Action, 
    action2: Action, 
    click_coord_threshold: float = 10.0
) -> bool:
    """
    判断两个动作是否相似。
    
    Args:
        action1: 第一个动作。
        action2: 第二个动作。
        click_coord_threshold: 点击坐标的欧氏距离阈值，小于该值视为同一点。
        
    Returns:
        如果动作相似则返回 True，否则返回 False。
    """
    # 1. 动作类型必须相同
    if action1.get("function") != action2.get("function"):
        return False

    func = action1.get("function")
    args1 = action1.get("args", {})
    args2 = action2.get("args", {})

    # 2. 根据不同的动作类型，比较关键参数
    if func == "click":
        x1, y1 = args1.get("x"), args1.get("y")
        x2, y2 = args2.get("x"), args2.get("y")
        # 确保坐标都存在
        if None in [x1, y1, x2, y2]:
            return False
        # 计算欧氏距离
        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return distance < click_coord_threshold
    
    elif func == "type":
        # 对于输入动作，要求输入的文本完全一致
        return args1.get("text") == args2.get("text")
        
    # 其他类型的动作，默认要求参数字典完全相同
    # 可以根据需要扩展更多动作类型的比较逻辑
    else:
        return args1 == args2

# --- 核心循环检测算法 ---

def detect_loop(
    history: History,
    N: int,
    image_hash_threshold: int = 1,
    click_coord_threshold: float = 10.0
) -> Tuple[bool, Optional[Dict[str, List[int]]]]:
    """
    基于规则检测操作历史中是否存在循环模式。

    Args:
        history (History): 步骤历史列表，每个步骤是一个 (图片二进制流, 动作字典) 的元组。
        N (int): 要检测的循环步数。
        image_hash_threshold (int): 图片感知哈希的汉明距离阈值。
                                    推荐值: 0 或 1。0 表示图片感知内容完全一样。
                                    1 表示允许极微小的差异。值越小，判断越严格。
        click_coord_threshold (float): 点击动作的坐标相似度阈值（欧氏距离）。

    Returns:
        一个元组 (is_loop_detected, loop_info):
        - is_loop_detected (bool): 是否检测到循环。
        - loop_info (Dict | None): 如果检测到循环，返回一个字典，
          包含两个序列的索引：{'first_sequence': [i, i+1, ...], 'second_sequence': [j, j+1, ...]}。
          否则返回 None。
    """
    # 1. 检查历史记录长度是否足够进行比较
    # 至少需要 2*N 的长度才能找到一个不重叠的循环
    if not isinstance(N, int) or N <= 0 or len(history) < 2 * N:
        return False, None

    print(f"开始检测... 历史记录长度: {len(history)}, 循环步数 N: {N}")

    # 2. 预处理：为历史记录中的所有图片计算感知哈希值，避免重复计算
    # 这一步是性能优化的关键
    processed_history = []
    for i, (image_binary, action) in enumerate(history):
        phash = _calculate_phash(image_binary)
        if phash is None:
            print(f"警告: 索引 {i} 处的图片无法处理，跳过此步骤的哈希计算。")
        processed_history.append({"phash": phash, "action": action})

    # 3. 定义要比较的“当前序列”
    # 当前序列是历史记录的最后 N 个步骤
    current_sequence_indices = list(range(len(history) - N, len(history)))
    current_sequence = processed_history[-N:]

    # 4. 滑动窗口，寻找匹配的“历史序列”
    # 历史序列的搜索范围是从开头到 `len(history) - 2*N`
    # 这样可以确保历史序列和当前序列不重叠
    max_start_index = len(history) - 2 * N
    for i in range(max_start_index + 1):
        is_potential_match = True
        
        # 定义“历史序列”
        previous_sequence_indices = list(range(i, i + N))
        previous_sequence = processed_history[i : i + N]

        # 5. 逐一对比两个序列中的步骤
        for j in range(N):
            step_prev = previous_sequence[j]
            step_curr = current_sequence[j]

            # a. 检查图片哈希是否已计算
            if step_prev["phash"] is None or step_curr["phash"] is None:
                is_potential_match = False
                break # 如果有图片无法处理，则无法比较，认为不匹配

            # b. 比较图片相似度 (主要)
            # 计算两个哈希值的汉明距离
            hash_diff = step_prev["phash"] - step_curr["phash"]
            if hash_diff > image_hash_threshold:
                is_potential_match = False
                break # 图片不相似，立即中断此历史序列的比较

            # c. 比较动作相似度 (次要)
            if not _are_actions_similar(step_prev["action"], step_curr["action"], click_coord_threshold):
                is_potential_match = False
                break # 动作不相似，立即中断此历史序列的比较
        
        # 6. 如果两个序列完全匹配，则找到了循环
        if is_potential_match:
            print(f"检测到循环！当前序列 {current_sequence_indices} 与历史序列 {previous_sequence_indices} 匹配。")
            loop_info = {
                "first_sequence": previous_sequence_indices,
                "second_sequence": current_sequence_indices
            }
            return True, loop_info

    # 7. 如果遍历完所有可能的历史序列都没有找到匹配项，则未检测到循环
    print("未检测到循环。")
    return False, None


# --- 示例和测试 ---

def create_mock_image(text: str, size=(200, 100)) -> bytes:
    """创建一个带有文本的模拟图片，并返回其二进制数据。"""
    img = Image.new('RGB', size, color='white')
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, fill='black')
    
    # 将图片保存到内存中的二进制流
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    return byte_io.getvalue()

if __name__ == '__main__':
    # --- 场景1: 存在一个清晰的 3 步循环 ---
    print("--- 场景 1: 检测清晰的 3 步循环 ---")
    # 创建模拟图片
    img_A = create_mock_image("页面 A")
    img_B = create_mock_image("页面 B")
    img_C = create_mock_image("页面 C")
    img_D = create_mock_image("页面 D (无关页面)")

    # 创建模拟动作
    action_click_A = {"function": "click", "args": {"x": 100, "y": 200}}
    action_click_B = {"function": "click", "args": {"x": 500, "y": 400}}
    action_type_C = {"function": "type", "args": {"text": "hello world"}}
    
    # 模拟一个稍微有偏差的点击动作
    action_click_A_variant = {"function": "click", "args": {"x": 102, "y": 198}} # 坐标有微小偏移

    # 构建历史记录
    # 步骤 0-3: 任意操作
    # 步骤 4-6: 循环的第一次出现 (A -> B -> C)
    # 步骤 7-9: 循环的第二次出现 (A -> B -> C)
    history_with_loop: History = [
        (img_D, action_click_B),                                 # 0
        (create_mock_image("任意页面1"), action_click_A),         # 1
        (create_mock_image("任意页面2"), action_type_C),          # 2
        (img_D, action_click_B),                                 # 3
        (img_A, action_click_A),                                 # 4: 循环序列1开始
        (img_B, action_click_B),                                 # 5
        (img_C, action_type_C),                                  # 6: 循环序列1结束
        (img_A, action_click_A_variant), # 图片相同，动作坐标有微小偏移  # 7: 循环序列2开始
        (img_B, action_click_B),                                 # 8
        (img_C, action_type_C),                                  # 9: 循环序列2结束
    ]

    # 使用非常严格的阈值进行检测
    is_loop, loop_details = detect_loop(
        history=history_with_loop, 
        N=3, 
        image_hash_threshold=0, # 要求图片感知内容完全一样
        click_coord_threshold=5.0 # 要求点击位置偏差在5个像素以内
    )

    print(f"检测结果: {is_loop}")
    if is_loop:
        print(f"循环详情: {loop_details}")
    
    print("\n" + "="*40 + "\n")

    # --- 场景2: 不存在循环 ---
    print("--- 场景 2: 检测无循环的序列 ---")
    history_no_loop: History = [
        (img_A, action_click_A),
        (img_B, action_click_B),
        (img_C, action_type_C),
        (img_D, action_click_A),
        (img_A, action_click_B), # 页面和动作不匹配
        (img_B, action_type_C),
    ]

    is_loop, loop_details = detect_loop(history=history_no_loop, N=3)
    print(f"检测结果: {is_loop}")
    
    print("\n" + "="*40 + "\n")
    
    # --- 场景3: 图片相似但动作不同，不应算作循环 ---
    print("--- 场景 3: 图片相似但动作不同 ---")
    history_diff_action: History = [
        (img_A, action_click_A),
        (img_B, action_click_B),
        (img_A, action_type_C), # 页面A，但动作是输入而非点击
        (img_B, action_click_B),
    ]
    
    is_loop, loop_details = detect_loop(history=history_diff_action, N=2)
    print(f"检测结果: {is_loop}")