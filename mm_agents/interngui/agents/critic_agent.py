import base64
import json
import os
import requests
from typing import Dict
from mm_agents.interngui.core.mllm import LMMAgent

class CriticAgent:
    def __init__(self, engine_params: Dict, platform: str = "desktop") -> None:
        self.engine_params = engine_params
        self.platform = platform
        self.reset()

    def reset(self):
        # 还需要支持 GPT-4O 的Critic测试
        # self.critic_agent = LMMAgent(self.engine_params)
        pass
        
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
            return True

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
