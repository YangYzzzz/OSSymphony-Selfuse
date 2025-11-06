import requests
import logging
from functools import partial
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple
from requests.auth import HTTPBasicAuth
from gui_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
from gui_agents.interngui.utils.common_utils import (
    call_llm_safe, 
    split_thinking_response, 
    draw_coordinates, 
    call_llm_formatted,    
    parse_code_from_string,
    split_thinking_response,
    create_pyautogui_code
)

from gui_agents.interngui.agents.searcher_agent import SearcherAgent, VLMSearcherAgent
from gui_agents.interngui.agents.grounder_agent import GrounderAgent
import os
import json
from gui_agents.interngui.utils.formatters import (
    SINGLE_ACTION_FORMATTER,
    CODE_VALID_FORMATTER,
)
import datetime
from desktop_env.desktop_env import DesktopEnv
import pprint, sys, desktop_env
print("--- sys.path ---")
pprint.pprint(sys.path)
print("\n--- desktop_env location ---")
print(desktop_env.__file__) 
if __name__=="__main__":
    
    search_env = DesktopEnv(
        path_to_vm="/nvme/yangbowen/osworld/docker_vm_data/Ubuntu.qcow2",
        action_space="pyautogui",
        provider_name="docker", # 对应 --provider_name "docker"
        region="us-east-1", # 对应 --region "us-east-1"
        snapshot_name="", # 命令行中未提供 snapshot_name，假设为空字符串
        screen_size=(1920, 1080), # 对应 --grounding_width 和 --grounding_height
        headless=True, # 对应 --headless 标志
        os_type="Ubuntu",
        require_a11y_tree="screenshot"
        in ["a11y_tree", "screenshot_a11y_tree", "som"], # 结果为 False
        enable_proxy=True,
        client_password="", # 命令行中未提供 client_password，getattr 返回默认值 ""
    )


    # --- 2. 构建 Grounder 引擎参数 ---
    engine_params_for_grounder = {
        "engine_type": "openai", # 对应 --grounder_provider
        "model": "ui-tars-1.5-7b", # 对应 --grounder_model
        "base_url": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-65pfw-1176830-worker-0.yangbowen/8000/v1", # 对应 --grounder_url
        "api_key": "none", # 对应 --grounder_api_key
        "grounding_width": 1920, # 对应 --grounding_width
        "grounding_height": 1080, # 对应 --grounding_height
        "grounding_smart_resize": True # 对应 --grounding_smart_resize
    }
  
    engine_params_for_searcher = {
        "engine_type": "openai", # 对应 --searcher_provider
        "model": "gpt-5-mini", # 对应 --searcher_model
        "base_url": "https://api.boyuerichdata.opensphereai.com/v1", # 对应 --searcher_url
        "api_key": "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D", # 对应 --searcher_api_key
        "temperature": 0.1, # 对应 --searcher_temperature
        "budget": 20, # 对应 --searcher_budget
        "type": "vlm", # 对应 --searcher_type
        "engine_params_for_grounder": engine_params_for_grounder, # 嵌套上面已定义的 grounder 参数
    }

    grounder_agent = GrounderAgent(engine_params=engine_params_for_grounder, width=1920, height=1080)
    searcher_agent = SearcherAgent.create(engine_params=engine_params_for_searcher, search_env=search_env, platform="linux", grounder_agent=grounder_agent)
    assert isinstance(searcher_agent, VLMSearcherAgent)
    result_dir = os.path.join("/nvme/yangbowen/yangbowen/OSWorld/test/searcher", f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
    os.makedirs(result_dir, exist_ok=True)

    searcher_agent.result_dir = result_dir
    query = "How to globally change font for all slides in an Libreoffice Impress?"

    main_screenshot_path = "/nvme/yangbowen/yangbowen/OSWorld/test/main_screenshot2.png"
    with open(main_screenshot_path, "rb") as image_file:
        image_bytes = image_file.read()
    main_obs = {
        "screenshot": image_bytes
    }
    result = searcher_agent.search(query=query, main_obs=main_obs)
    with open(os.path.join(result_dir, f"results.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    print(result)