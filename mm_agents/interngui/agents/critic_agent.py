import base64
import json
import os
import requests
from typing import Dict
from mm_agents.interngui.core.mllm import LMMAgent
from mm_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
from mm_agents.interngui.utils.common_utils import call_llm_safe
class CriticAgent:
    def __init__(self, engine_params: Dict, platform: str = "desktop") -> None:
        self.engine_params = engine_params
        self.platform = platform
        self.reset()

    def reset(self):
        # 还需要支持 GPT-4O 的Critic测试
        critic_system_prompt = PROCEDURAL_MEMORY.CRITIC_SYSTEM_PROMPT
        self.critic_agent = LMMAgent(self.engine_params, system_prompt=critic_system_prompt)
        
        
    def critic(self, task, screenshot, action, history):
        # zhenyu的API, 特殊处理一下
        if self.engine_params["model"] == "os-oracle":
            base_url = self.engine_params["base_url"]
            endpoint = f"{base_url}/critic/predict"
            ak = "5ad34100ee055a4bae66370a5e683bac"
            sk = "607de8249657a3b3bd036dc96d4c0b2f"
            token = base64.b64encode(f"{ak}:{sk}".encode()).decode()
            # 字节流 -> base64
            image_dataurl = f"data:image/png;base64,{base64.b64encode(screenshot).decode('utf-8')}"
            headers = {
                "Authorization": f"Basic {token}",
                "Content-Type": "application/json",
            }
            payload = {
                "platform": self.platform,            # "mobile" or "desktop"（兼容 "dekstop"）
                "action": action,                # ui-tars-1.5 风格动作字符串
                "instruction": task,             # 任务描述
                "history": history,              # 动作历史
                "image_base64": image_dataurl,   # 单张图（多张可用 images_base64: [..]）
            }
            print(f'[Critic Args]: task: {task}, action: {action}, history: {history}')
            resp = requests.post(endpoint, headers=headers, data=json.dumps(payload), timeout=60)
            try:
                result = resp.json()
                print(f'[Critic Result]: {result}')
                return True if result["result"] == "Yes" else False
            except Exception:
                return False

        else:
            # 对于 GPT-4o 等通用模型
            self.reset()

            # 2. 构建用户输入，清晰地组织所有信息
            user_prompt = f"""
                [Goal]
                {task}

                [History]
                {history}

                [Platform]
                {self.platform}

                [Proposed Action]
                {action}
            """
            print(f'[Critic Args]: task: {task}, action: {action}, history: {history}')

            self.critic_agent.add_message(text_content=user_prompt, image_content=screenshot, role="user")
            raw_response = call_llm_safe(self.critic_agent, temperature=0.1)
            print(f"[Critic Raw Response]:\n{raw_response}")

            # 4. 解析结果
            if not raw_response:
                print("[Critic Parsed Result]: No response from model. Defaulting to No.")
                return False

            try:
                # 严格解析最后一行非空字符串
                # .strip() 去除首尾空白
                # .splitlines() 按换行符分割
                # [-1] 取最后一部分
                # .strip() 再次去除可能存在的空白
                last_line = raw_response.strip().splitlines()[-1].strip()
                
                # 判断最后一行是否为 "Yes" (忽略大小写)
                is_accepted = last_line.lower() == 'yes'
                
                print(f'[Critic Parsed Result]: "{last_line}" -> {is_accepted}')
                return is_accepted
            except IndexError:
                # 如果模型返回空字符串或只有空白，则解析失败
                print("[Critic Parsed Result]: Empty or invalid response format. Defaulting to No.")
                return False
# ==============================================================================


if __name__=="__main__":
    # ======== 配置 ========
    FLASK_BASE = "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/wzy-proxy-lk85v-151269-worker-0.wuzhenyu/7871"
    ENDPOINT   = f"{FLASK_BASE}/critic/predict"

    # 与 vLLM 网关一致的 AK/SK -> Basic Auth 头
    AK = "1654781209e1a9651d8c3680e64584c0"
    SK = "7a77dd3f690f14e4a89988f9c53af3be"
    token   = base64.b64encode(f"{AK}:{SK}".encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }

    # ======== 测试样例（你给的参数） ========
    image_path = "/mnt/shared-storage-user/intern7shared/wuzhenyu/Codes/gui_critic_model/data/test_set/ac/images/ep_11840_02.png"
    task       = "Share the news article on Gmail"
    # 假设是手机端（AC 数据），ui-tars 风格动作：点击 (462, 786)
    action     = "click(point='<point>462 786</point>')"
    platform   = "mobile"   # 若要桌面测试：platform = "desktop"
    history    = "None"     # 也可以填多步历史，比如：Step 1: {...}\nStep 2: {...}

    # 读图 -> b64 dataURL
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    image_dataurl = f"data:image/png;base64,{b64}"

    payload = {
        "platform": platform,            # "mobile" or "desktop"（兼容 "dekstop"）
        "action": action,                # ui-tars-1.5 风格动作字符串
        "instruction": task,             # 任务描述
        "history": history,              # 动作历史
        "image_base64": image_dataurl,   # 单张图（多张可用 images_base64: [..]）
    }
    resp = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload), timeout=60)
    try:
        print("[HTTP]", resp.status_code)
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception:
        print(resp.text)
