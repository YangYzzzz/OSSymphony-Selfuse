import copy
import os
import json
import uuid
import random
import time
import shutil
from datetime import datetime
from typing import List, Dict, Tuple, Any

from desktop_env.osworld.desktop_env import DesktopEnv
from mm_agents.os_symphony.agents.coarse_instruction_generation_agent import CoarseInstructionGenerationAgent

# 基础存储路径
TASK_BASE_DIR = "evaluation_examples/ubuntu_generate"

# --- 配置字典 ---
EXTRA_APP_SETUP_DICT = {
    "pycharm": {
        "type": ["py", "project_folder"],
        "commands": [["pycharm-community", "PATH"]]
    },
    "blender": {
        "type": ["blend"],
        "commands": [["blender", "PATH"]]
    },
    "dbeaver": {
        "type": ["sql"],
        "commands": [["dbeaver-ce", "PATH"]]
    },
    "wireshark": {
        "type": ["pcapng"],
        "commands": [["sudo", "wireshark", "PATH"]] # 建议拆开 sudo 和命令
    },
    "texstudio": {
        "type": ["tex"],
        "commands": [["texstudio", "PATH"]]
    },
    "gitkraken": {
        "type": ["project_folder"],
        "commands": [["gitkraken", "-p", "PATH"]]
    },
    "scilab": {
        "type": ["sci"],
        "commands": [["scilab", "-f", "PATH"]]
    },
    "audacity": {
        "type": ["wav", "mp3"],
        "commands": [["audacity"]]
    },
    "librecad": {
        "type": ["dxf"],
        "commands": [["librecad", "PATH"]]
    },
    "drawio": {
        "type": ["drawio"],
        "commands": [["drawio", "PATH"]]
    },
    "darktable": {
        "type": ["png"],
        "commands": [["darktable", "PATH"]]
    },
    "handbrake": {
        "type": ["mp4"],
        "commands": [["handbrake", "PATH"]]
    },
    "homebank": {
        "type": ["xhb"],
        "commands": [["homebank", "PATH"]]
    },
    "mixxx": {
        "type": ["mp3"],
        "commands": [["mixxx", "-f", "PATH"]]
    },
    "inkscape": {
        "type": ["svg"],
        "commands": [["inkscape", "PATH"]]
    },
    "obs": {
        "commands": [["obs"]]
    },
    "meld": {
        "type": ["py"],
        "commands": [["meld", "PATH", "PATH"]]
    },
    "musescore": {
        "type": ["mscz"],
        "commands": [["musescore", "PATH"]]
    },
    "zotero": {
        "commands": [["zotero-snap"]]
    },
    "zoom": {
        "commands": [["zoom"]]
    },
    "google-earth-pro": {
        # 这里的 lat, lon, range 将在代码中动态替换
        "commands": [
            [
                "google-earth-pro",
                # 使用占位符，方便后续替换
                "lat=LAT_VAL,lon=LON_VAL,range=RANGE_VAL" 
            ]
        ]
    },
    "kicad": {
        "commands": [["kicad"]]
    },
    "spotify": {
        "commands": [["spotify"]]
    },
    "calendar": {
        "commands": [["gnome-calendar"]]
    },
    "shotcut": {
        "type": ["mp4"],
        "commands": [["shotcut", "PATH"]]
    },
    "krita": {
        "type": ["kra"],
        "commands": [["krita", "PATH"]]
    },
    "pdfarranger": {
        "type": ["pdf"],
        "commands": [["pdfarranger", "PATH"]]
    },
    "grass": {
        "commands": [["grass"]]
    },
}

OSWORLD_APP_SETUP_DICT = {
    "chrome": {
        "type": ["url"],
        "window_name": "Google Chrome",
        "commands": [
            ["google-chrome", "--remote-debugging-port=1337", "--start-maximized", "https://www.bing.com"],
            ["socat", "tcp-listen:9222,fork", "tcp:localhost:1337"]
        ]
    },
    "gimp": {
        "type": ["png"],
        "commands": [["gimp", "PATH"]]
    },
    "libreoffice_impress": {
        "type": ["pptx"],
        "window_name": "LibreOffice Impress",
        "commands": [
            [
                "libreoffice",
                "--impress",
                "--nologo",
                "--norestore", # 修复：这里原来漏了逗号
                "PATH"
            ]
        ]
    },
    "libreoffice_calc": {
        "type": ["xlsx"],
        "window_name": "LibreOffice Calc",
        "commands": [
            [
                "libreoffice",
                "--calc",
                "--nologo",
                "--norestore", # 修复：这里原来漏了逗号
                "PATH"
            ]
        ]
    },
    "libreoffice_writer": {
        "type": ["docx"],
        "window_name": "LibreOffice Writer",
        "commands": [
            [
                "libreoffice",
                "--writer",
                "--nologo",
                "--norestore", # 修复：这里原来漏了逗号
                "PATH"
            ]
        ]
    },
    "vscode": {
        "type": ["project_folder", "py"],
        "commands": [["code", "--new-window", "PATH"]]
    },
    "terminal": {
        "window_name": "Terminal"
    },
    "thunderbird": {
        "commands": [["/usr/bin/thunderbird"]]
    },
    "vlc": {
        "type": ["mp4"],
        "commands": [
            [
                "VLC_VERBOSE=-1",
                "vlc",
                "--no-audio",
                "--no-video-title-show",
                "--play-and-pause",
                "PATH"
            ]
        ]
    }
}

APP_SETUP_DICT = OSWORLD_APP_SETUP_DICT | EXTRA_APP_SETUP_DICT
# 为了测试新的app
# APP_SETUP_DICT = EXTRA_APP_SETUP_DICT
ENV_FILE_BASE_DIR = "/home/user/Desktop/test_files"

class OSCaliberTaskGenerator:
    def __init__(self, rollout_task_dir: str, env: DesktopEnv, agent: CoarseInstructionGenerationAgent) -> None:
        self.rollout_task_dir = rollout_task_dir
        self.env_file_base_dir = ENV_FILE_BASE_DIR
        self.env = env
        self.agent = agent

    def _generate_random_coordinates(self) -> Tuple[str, str, str]:
        """生成随机的经纬度和高度范围"""
        # 纬度: -90 到 90
        lat = round(random.uniform(-90.0, 90.0), 6)
        # 经度: -180 到 180
        lon = round(random.uniform(-180.0, 180.0), 6)
        # 高度范围 (Range): 比如 1000米 到 5000000米 (5000km)
        # Google Earth 的 range 参数通常指视点距离地面的高度
        range_val = random.randint(1000, 5000000)
        
        return str(lat), str(lon), str(range_val)

    def _generate_config(self, app_name: str) -> List[Dict[str, Any]]:
        """根据 APP_SETUP_DICT 生成标准的 config 列表"""
        app_info = APP_SETUP_DICT.get(app_name, {})
        if not app_info:
            return []

        config_list = []
        
        # 1. 准备文件列表
        type_lists = app_info.get('type', [])
        file_abs_lists = []
        
        for file_type in type_lists:
            # 跳过 url 类型
            if file_type == "url":
                continue
                
            # 获取该类型下的所有文件
            target_dir = os.path.join(self.env_file_base_dir, file_type)
            # 增加 try-except 或检查路径是否存在是个好习惯
            try:
                file_lists_for_single_type = self.env.controller.get_file_lists(target_dir)
            except Exception as e:
                print(f"Warning: Could not list files in {target_dir}: {e}")
                file_lists_for_single_type = []

            if file_lists_for_single_type and isinstance(file_lists_for_single_type, list):
                for f in file_lists_for_single_type:
                    file_abs_lists.append(str(os.path.join(target_dir, f)))

        # 2. 生成 Launch 命令
        # 必须使用 deepcopy，否则会修改全局的 APP_SETUP_DICT，导致下一次循环时 PATH 已经被替换死了
        raw_commands = copy.deepcopy(app_info.get("commands", []))
        
        for cmd in raw_commands:
            # 处理每一个参数
            for i in range(len(cmd)):
                param = cmd[i]
                
                # 处理 PATH 替换
                if "PATH" in param:
                    if file_abs_lists:
                        selected_file = random.choice(file_abs_lists)
                        cmd[i] = param.replace("PATH", selected_file)
                    else:
                        # 如果该软件需要文件但没有找到文件，可以选择移除该参数，或者保留原样让其打开空软件
                        if param == "PATH":
                            cmd[i] = "" 
                        print(f"Warning: No files found for {app_name}, starting without file.")

                # 处理 Google Earth 的随机经纬度
                if "lat=" in param and "lon=" in param:
                    lat_val, lon_val, range_val = self._generate_random_coordinates()
                    new_param = param.replace("LAT_VAL", lat_val)
                    new_param = new_param.replace("LON_VAL", lon_val)
                    new_param = new_param.replace("RANGE_VAL", range_val)
                    cmd[i] = new_param

            cleaned_cmd = [c for c in cmd if c != ""]

            config_list.append({
                "type": "launch",
                "parameters": {
                    "command": cleaned_cmd
                }
            })
            
        return config_list

    def generate_all(self, task_nums=1):
        available_apps = list(APP_SETUP_DICT.keys())
        test_file_list = {}
        for available_app in available_apps:
            test_file_list = test_file_list | self.generate_task(task_nums=task_nums, app_list=[available_app])
        return test_file_list

    def generate_task(self, task_nums=10, app_list: List|str = []):
        """
        生成任务文件
        """
        if isinstance(app_list, list) and len(app_list) > 0:
            available_apps = app_list
        else:
            available_apps = list(APP_SETUP_DICT.keys())  

        if not available_apps:
            raise ValueError("No apps available to generate tasks.")

        test_file_list = {}
        app_name = random.choice(available_apps)
        domain_dir = os.path.join(self.rollout_task_dir, app_name)
        os.makedirs(domain_dir, exist_ok=True)

        # 生成配置
        task_setup_config = self._generate_config(app_name)
        
        # Reset 环境
        print(f"Generating tasks for {app_name}...")
        self.env.reset(task_config={"config": task_setup_config, "id": "init_id", "instruction": "init_instruction"})
        self.agent.reset()

        obs = self.env._get_obs()
        
        # 让 Agent 生成任务描述
        task_list = self.agent.generate(app_name=app_name, observation=obs, task_nums=task_nums)

        for task in task_list:
            task_id = str(uuid.uuid4())

            task_config = {
                "id": task_id,
                "snapshot": app_name,
                "instruction": task["description"],
                "config": task_setup_config,
                "complexity": task.get("complexity"), # 使用 get 防止 key 不存在
                "verification": task.get("verification")
            }
        
            json_path = os.path.join(domain_dir, f"{task_id}.json")
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(task_config, f, indent=4, ensure_ascii=False)
        
            if app_name not in test_file_list:
                test_file_list[app_name] = []
            test_file_list[app_name].append(task_id)

        return test_file_list
