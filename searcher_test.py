import requests
import logging
from functools import partial
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple
from requests.auth import HTTPBasicAuth
import concurrent.futures
from mm_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
from mm_agents.interngui.utils.common_utils import (
    call_llm_safe, 
    split_thinking_response, 
    draw_coordinates, 
    call_llm_formatted,    
    parse_code_from_string,
    split_thinking_response,
    create_pyautogui_code
)
import sys
sys.path.insert(0, "/nvme/yangbowen/yangbowen/OSWorld")
from mm_agents.interngui.agents.searcher_agent import SearcherAgent, VLMSearcherAgent
from mm_agents.interngui.agents.grounder_agent import GrounderAgent
import os
import json
from mm_agents.interngui.utils.formatters import (
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

def run_search_task(task_id: int, query: str, main_obs: dict):
    """
    封装单次搜索任务的函数，将在每个线程中独立执行。

    Args:
        task_id (int): 任务的唯一标识符，用于创建独立的文件夹。
        query (str): 搜索查询语句。
        main_obs (dict): 包含截图等信息的观测数据。

    Returns:
        dict or None: 返回搜索结果，如果发生错误则返回 None。
    """
    print(f"[Task {task_id}] Starting...")
    try:
        # 1. 在任务内部创建Agent实例
        # 这很重要，因为Agent实例通常不是线程安全的，每个线程使用独立的实例可以避免状态冲突
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

        grounder_agent = GrounderAgent(engine_params=engine_params_for_grounder, width=1920, height=1080)
        searcher_agent = SearcherAgent.create(engine_params=engine_params_for_searcher, search_env=search_env, platform="linux", grounder_agent=grounder_agent)
        assert isinstance(searcher_agent, VLMSearcherAgent)

        # 2. 创建该任务专属的结果目录
        # 使用 task_id 确保目录名唯一
        result_dir = os.path.join("/nvme/yangbowen/yangbowen/OSWorld/test/searcher", f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{task_id}')
        os.makedirs(result_dir, exist_ok=True)
        searcher_agent.result_dir = result_dir

        # 3. 执行核心的搜索任务
        result = searcher_agent.search(query=query, main_obs=main_obs)

        # 4. 保存结果到JSON文件
        result_file_path = os.path.join(result_dir, "results.json")
        with open(result_file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        
        print(f"[Task {task_id}] Finished successfully. Results saved to {result_file_path}")
        return result

    except Exception as e:
        print(f"[Task {task_id}] An error occurred: {e}")
        return None
        
if __name__=="__main__":

    # --- 2. 构建 Grounder 引擎参数 ---
    engine_params_for_grounder = {
        "engine_type": "openai", # 对应 --grounder_provider
        "model": "ui-tars-1.5-7b", # 对应 --grounder_model
        "base_url": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10001/v1", # 对应 --grounder_url
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
        "budget": 3, # 对应 --searcher_budget
        "type": "vlm", # 对应 --searcher_type
        "engine_params_for_grounder": engine_params_for_grounder, # 嵌套上面已定义的 grounder 参数
    }
    query = "How to globally change font for all slides in an Libreoffice Impress?"

    main_screenshot_path = "/nvme/yangbowen/yangbowen/OSWorld/test/main_screenshot2.png"
    with open(main_screenshot_path, "rb") as image_file:
        image_bytes = image_file.read()
    main_obs = {
        "screenshot": image_bytes
    }
    num_tasks = 1  # 总共要执行的任务数量
    max_concurrent_workers = 1  # 同一时间最多运行的线程数

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_workers) as executor:
            
        # 提交所有任务到线程池
        # executor.submit会立即返回一个future对象，代表未来的计算结果
        futures = {executor.submit(run_search_task, i, query, main_obs): i for i in range(num_tasks)}

        # --- 处理已完成的任务 ---
        # concurrent.futures.as_completed 会在任何一个future完成时立即yield它
        # 这比等待所有任务都完成后再处理要高效得多
        for future in concurrent.futures.as_completed(futures):
            task_id = futures[future]
            try:
                # .result() 方法会获取任务的返回值
                # 如果任务在执行过程中抛出异常，.result()会重新抛出该异常
                result = future.result()
                if result:
                    print(f"Result received from completed task {task_id}: {result}")
                else:
                    print(f"Task {task_id} completed but returned no result (likely failed).")
            except Exception as exc:
                print(f"Task {task_id} generated an exception: {exc}")

        print("\nAll tasks have been processed.")