import io
import math
import numpy as np
from typing import List, Tuple, Dict, Any, Optional, Union

# --- 核心依赖 ---
from PIL import Image, ImageDraw, ImageFont
import imagehash
from skimage.metrics import structural_similarity as ssim
from rapidfuzz import fuzz
import logging
from mm_agents.interngui.agents.memoryer_agent import StepBehavior

logger = logging.getLogger("desktopenv.loop_detection")

def _are_actions_similar(
    action1: Dict[str, Any],
    action2: Dict[str, Any],
    image_width: int,
    image_height: int,
    relative_coord_threshold: float,
    fuzzy_text_threshold: float,
) -> bool:
    """
    【内部辅助】根据详细规则判断两个动作是否相似。

    Args:
        action1: 第一个动作。
        action2: 第二个动作。
        image_width: 截图宽度。
        image_height: 截图高度。
        relative_coord_threshold: 用于坐标比较的相对距离阈值。
        fuzzy_text_threshold: 用于模糊文本匹配的相似度阈值 (0-100)。

    Returns:
        如果动作相似则返回 True，否则返回 False。
    """
    # 1. 动作类型必须相同
    if action1.get("function") != action2.get("function"):
        return False

    func = action1.get("function")
    args1 = action1.get("args", {})
    args2 = action2.get("args", {})

    # 计算基于图像对角线的绝对坐标距离阈值
    diagonal = math.sqrt(image_width**2 + image_height**2)
    abs_coord_thresh = relative_coord_threshold * diagonal

    def are_coords_close(x1, y1, x2, y2):
        if None in [x1, y1, x2, y2]: return False
        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return distance < abs_coord_thresh

    # 2. 根据不同的动作类型，比较关键参数
    if func == "click":
        return (
            are_coords_close(args1.get("x"), args1.get("y"), args2.get("x"), args2.get("y")) and
            args1.get("button") == args2.get("button") and
            args1.get("clicks") == args2.get("clicks")
        )

    elif func == "open":
        return args1.get("name") == args2.get("name")

    elif func == "type":
        if args1.get("x") and args1.get("y") and args2.get("x") and args2.get("y"):
            return (
                are_coords_close(args1.get("x"), args1.get("y"), args2.get("x"), args2.get("y")) and
                args1.get("text") == args2.get("text")
            )
        else:
            return args1.get("text") == args2.get("text")

    elif func == "drag":
        return (
            are_coords_close(args1.get("x1"), args1.get("y1"), args2.get("x1"), args2.get("y1")) and
            are_coords_close(args1.get("x2"), args1.get("y2"), args2.get("x2"), args2.get("y2"))
        )

    elif func == "set_cell_values":
        return args1.get("text") == args2.get("text")

    elif func == "scroll":
        # 比较滚动方向 (通过 clicks 的正负号)
        clicks1 = args1.get("clicks", 0)
        clicks2 = args2.get("clicks", 0)
        # 如果一个为0，另一个不为0，则方向不同
        if (clicks1 == 0 and clicks2 != 0) or (clicks1 != 0 and clicks2 == 0):
            same_direction = False
        else: # 比较符号
            same_direction = math.copysign(1, clicks1) == math.copysign(1, clicks2)

        return (
            are_coords_close(args1.get("x"), args1.get("y"), args2.get("x"), args2.get("y")) and
            same_direction and
            args1.get("shift") == args2.get("shift")
        )

    elif func == "key":
        return args1.get("keys") == args2.get("keys")

    elif func == "wait":
        return True  # wait 动作总是相似的

    elif func in ["call_code_agent", "call_search_agent"]:
        query1 = args1.get("query", "")
        query2 = args2.get("query", "")
        # 使用 Levenshtein 编辑距离计算模糊相似度
        query_similarity = fuzz.token_set_ratio(query1, query2) 
        # print(f'query_sim: {query_similarity}')
        return (
            query_similarity >= fuzzy_text_threshold and
            args1.get("result") == args2.get("result")
        )

    else:
        # 对于未知的动作类型，采取最严格的策略：返回 False
        return False


def _are_steps_similar_optimized(
    step1: StepBehavior,
    step2: StepBehavior,
    idx1: int,
    idx2: int,
    full_trajectory: List[StepBehavior], # 需要完整轨迹来正确访问SSIM列表
    phash_threshold: int,
    ssim_threshold: float,
    # 动作比较所需的参数
    image_width: int,
    image_height: int,
    relative_coord_threshold: float,
    fuzzy_text_threshold: float,
) -> bool:
    """
    【内部辅助-已优化】使用预计算数据快速比较两个步骤是否相似。
    """
    # 1. 快速检查：pHash 和 SSIM
    # a. 检查 pHash 是否已计算
    if step1.phash is None or step2.phash is None:
        return False # 如果任一图像信息缺失，则认为不相似

    # b. pHash 比较 (O(1) 整数减法)
    if (step1.phash - step2.phash) > phash_threshold:
        return False

    # c. SSIM 比较 (O(1) 列表访问)
    # 关键：SSIM值存储在后一个步骤的ssim_list中，索引是前一个步骤的索引
    later_step_idx = max(idx1, idx2)
    earlier_step_idx = min(idx1, idx2)
    
    # 从后一个步骤的 ssim_list 中获取分数
    ssim_score = full_trajectory[later_step_idx].ssim_list[earlier_step_idx]
    
    if ssim_score < ssim_threshold:
        return False

    # 2. 详细检查：动作比较 (只有在图像相似时才执行)
    if not _are_actions_similar(
        step1.action_dict, step2.action_dict,
        image_width, image_height, relative_coord_threshold, fuzzy_text_threshold
    ):
        return False

    # 所有检查都通过
    return True

# ==============================================================================
# 核心循环检测算法
# ==============================================================================
def detect_loop(
    full_trajectory: List[StepBehavior],
    image_width: int = 1920,
    image_height: int = 1080,
    N: int = 3,
    phash_threshold: int = 1,
    ssim_threshold: float = 0.98,
    relative_coord_threshold: float = 0.05,
    fuzzy_text_threshold: float = 75.0,
) -> Tuple[bool, Optional[Dict[str, List[int]]]]:
    """
    基于预计算数据，高效检测是否存在循环模式。
    
    Args:
        full_trajectory (List[StepBehavior]): 包含当前步骤的完整历史。
        image_width (int): 截图的宽度。
        image_height (int): 截图的高度。
        N (int): 要检测的循环步数 (序列长度)。
        phash_threshold (int): 图片 pHash 汉明距离阈值。推荐 0-2。
        ssim_threshold (float): 图片 SSIM 相似度阈值。推荐 0.95-0.99。
        relative_coord_threshold (float): 坐标相似度相对阈值。推荐 0.01-0.05。
        fuzzy_text_threshold (float): Agent query 文本模糊匹配相似度阈值 (0-100)。

    Returns:
        一个元组 (is_loop_detected, loop_info):
        - is_loop_detected (bool): 是否检测到循环。
        - loop_info (Dict | None): 如果检测到循环，返回两个序列的索引。
    """
    L = len(full_trajectory)

    # 1. 检查历史记录长度是否足够进行比较
    if not isinstance(N, int) or N <= 0 or L < 2 * N:
        return False, None

    # 2. 定义当前序列 (最后 N 个步骤)
    # current_sequence_indices = list(range(L - N, L))
    
    # 3. 滑动窗口，从后往前搜索匹配的历史序列
    # 历史序列的起始索引 i，最大不能与当前序列重叠
    # i + N 必须小于 L - N，所以 i 的最大值是 L - 2*N
    max_start_index = L - 2 * N
    for i in range(max_start_index, -1, -1):
        is_potential_match = True
        
        # 4. 逐一对比两个序列中的步骤
        for j in range(N):
            # 获取历史序列和当前序列中对应步骤的索引
            idx_prev = i + j
            idx_curr = (L - N) + j
            
            # 获取步骤对象
            step_prev = full_trajectory[idx_prev]
            step_curr = full_trajectory[idx_curr]
            
            # 使用优化后的比较函数
            if not _are_steps_similar_optimized(
                step_prev, step_curr, idx_prev, idx_curr, full_trajectory,
                phash_threshold, ssim_threshold,
                image_width, image_height, relative_coord_threshold, fuzzy_text_threshold
            ):
                is_potential_match = False
                break
        
        # 5. 如果序列完全匹配，则找到循环
        if is_potential_match:
            previous_sequence_indices = list(range(i, i + N))
            loop_info = {
                "match_sequence_indices": previous_sequence_indices
            }
            # print(f"Loop detected: current sequence (indices {L-N} to {L-1}) matches historical sequence (indices {i} to {i+N-1})")
            return True, loop_info

    # 6. 未找到匹配项
    return False, None


# ==============================================================================
# 示例和测试
# ==============================================================================

def create_mock_image(text: str, size=(800, 600), add_noise=False) -> bytes:
    """创建一个带有文本的模拟图片，并返回其二进制数据。"""
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = None
    draw.text((50, 50), text, fill='black', font=font)
    
    if add_noise:
        pixels = img.load()
        for i in range(int(size[0] * 0.1)):
            for j in range(int(size[1] * 0.1)):
                if np.random.rand() < 0.1: # 10% 的概率添加噪点
                    noise_color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
                    pixels[i, j] = noise_color

    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    return byte_io.getvalue()

# if __name__ == '__main__':
#     # --- 测试环境设置 ---
#     IMG_WIDTH, IMG_HEIGHT = 800, 600
    
#     # --- 创建模拟图片 ---
#     img_A = create_mock_image("页面 A", (IMG_WIDTH, IMG_HEIGHT))
#     img_B = create_mock_image("页面 B", (IMG_WIDTH, IMG_HEIGHT))
#     img_C = create_mock_image("页面 C", (IMG_WIDTH, IMG_HEIGHT))
#     img_D = create_mock_image("页面 D (无关)", (IMG_WIDTH, IMG_HEIGHT))
#     # 创建一个带噪点的图片 A，pHash 可能相似，但 SSIM 会较低
#     img_A_noisy = create_mock_image("页面 A", (IMG_WIDTH, IMG_HEIGHT), add_noise=True)

#     # --- 创建模拟动作 ---
#     action_click_A = {"function": "click", "args": {"x": 100, "y": 200, "button": "left", "clicks": 1}}
#     action_click_A_variant = {"function": "click", "args": {"x": 105, "y": 205, "button": "left", "clicks": 1}} # 坐标微小偏移
#     action_click_A_diff_button = {"function": "click", "args": {"x": 100, "y": 200, "button": "right", "clicks": 1}} # 按键不同
#     action_scroll_down = {"function": "scroll", "args": {"x": 400, "y": 300, "clicks": -5, "shift": False}}
#     action_scroll_up = {"function": "scroll", "args": {"x": 400, "y": 300, "clicks": 5, "shift": False}} # 方向相反
#     action_agent_call_1 = {"function": "call_search_agent", "args": {"query": "如何修复打印机卡纸问题？", "result": True}}
#     action_agent_call_2 = {"function": "call_search_agent", "args": {"query": "怎样修复打印机卡纸问题", "result": True}} # 文本相似
#     action_agent_call_3 = {"function": "call_search_agent", "args": {"query": "如何安装新的墨盒？", "result": True}} # 文本不相似
    
#     print("="*20 + " 场景 1: 检测到清晰的 3 步循环 (坐标有容差) " + "="*20)
#     history_loop: History = [
#         (img_D, action_click_A),                                # 0 (无关)
#         (img_A, action_click_A),                                # 1: 循环序列1开始
#         (img_B, action_scroll_down),                            # 2
#         (img_C, action_agent_call_1),                           # 3: 循环序列1结束
#         (img_A, action_click_A_variant),                        # 4: 循环序列2开始 (点击坐标有微小偏移)
#         (img_B, action_scroll_down),                            # 5
#         (img_C, action_agent_call_2),                           # 6: (Agent query 文本相似)
#     ]
#     is_loop, loop_details = detect_loop(history_loop, IMG_WIDTH, IMG_HEIGHT, N=3)
#     print(f"检测结果: {is_loop}")
#     if is_loop:
#         print(f"循环详情: {loop_details}") # 应为: first: [1,2,3], second: [4,5,6]
#     print("\n")

#     print("="*20 + " 场景 2: 因动作参数不匹配而检测失败 (滚动方向相反) " + "="*20)
#     history_fail_action: History = [
#         (img_A, action_scroll_down), # 0
#         (img_B, action_click_A),     # 1
#         (img_A, action_scroll_up),   # 2 (图片相同，但滚动方向相反)
#         (img_B, action_click_A),     # 3
#     ]
#     is_loop, loop_details = detect_loop(history_fail_action, IMG_WIDTH, IMG_HEIGHT, N=2)
#     print(f"检测结果: {is_loop}") # 应该为 False
#     if is_loop: print(f"循环详情: {loop_details}")
#     print("\n")

#     print("="*20 + " 场景 3: 因 Agent Query 文本差异过大而检测失败 " + "="*20)
#     history_fail_query: History = [
#         (img_C, action_agent_call_1), # 0
#         (img_D, action_click_A),      # 1
#         (img_C, action_agent_call_3), # 2 (Query 文本不相似)
#         (img_D, action_click_A),      # 3
#     ]
#     is_loop, loop_details = detect_loop(history_fail_query, IMG_WIDTH, IMG_HEIGHT, N=2)
#     print(f"检测结果: {is_loop}") # 应该为 False
#     if is_loop: print(f"循环详情: {loop_details}")
#     print("\n")

#     print("="*20 + " 场景 4: 因 SSIM 阈值未通过而检测失败 (图片有噪点) " + "="*20)
#     history_fail_ssim: History = [
#         (img_A, action_click_A),     # 0
#         (img_B, action_scroll_down), # 1
#         (img_A_noisy, action_click_A), # 2 (图片有噪点)
#         (img_B, action_scroll_down), # 3
#     ]
#     # 使用非常严格的 SSIM 阈值
#     is_loop, loop_details = detect_loop(history_fail_ssim, IMG_WIDTH, IMG_HEIGHT, N=2, ssim_threshold=0.99)
#     # 检查一下两张图的相似度
#     phash_sim = _are_images_similar_combined(img_A, img_A_noisy, phash_threshold=2, ssim_threshold=0.01)
#     ssim_sim = _are_images_similar_combined(img_A, img_A_noisy, phash_threshold=10, ssim_threshold=0.99)
#     print(f"图片 A 和带噪点的图片 A 比较:")
#     print(f"  - 仅 pHash 判断是否相似? {'是' if phash_sim else '否'}")
#     print(f"  - 仅 SSIM (阈值0.99) 判断是否相似? {'是' if ssim_sim else '否'}")
#     print(f"循环检测结果: {is_loop}") # 应该为 False，因为 SSIM 不达标
#     if is_loop: print(f"循环详情: {loop_details}")
#     print("\n")

#     print("="*20 + " 场景 5: 历史记录不足 " + "="*20)
#     short_history: History = [(img_A, action_click_A)] * 5 # 5条记录
#     is_loop, loop_details = detect_loop(short_history, IMG_WIDTH, IMG_HEIGHT, N=3) # 需要 2*3=6 条记录
#     print(f"检测结果: {is_loop}") # 应该为 False
#     if is_loop: print(f"循环详情: {loop_details}")
#     print("\n")