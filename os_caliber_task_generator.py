"""
    Task Generator, 在 base_dir 下生成类 OSWorld 任务文件, 
    返回的 dict 如下所示:
    {
        "multi_apps": ["d1acdb87-bb67-4f30-84aa-990e56a09c92"], # 最好带上前缀
        "xxx": ["xxx"]
    }
    
    任务文件格式如下所示:
    {
        "id": "0d8b7de3-e8de-4d86-b9fd-dd2dce58a217", # uuid
        "snapshot": "chrome", # 重要, 标注相应软件
        "instruction": "Browse the natural products database.", # 重要, 对应指令
        "config": [ # 重要, 对应启动脚本
            {
                "type": "launch",
                "parameters": {
                    "command": [
                        "google-chrome",
                        "--remote-debugging-port=1337"
                    ]
                }
            },
            {
                "type": "launch",
                "parameters": {
                    "command": [
                        "socat",
                        "tcp-listen:9222,fork",
                        "tcp:localhost:1337"
                    ]
                }
            },
            {
                "type": "chrome_open_tabs",
                "parameters": {
                    "urls_to_open": [
                        "https://drugs.com"
                    ]
                }
            },
            {
                "type": "activate_window",
                "parameters": {
                    "window_name": "Google Chrome"
                }
            }
        ],
    }
"""
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

# 应用配置字典：定义了应用名称、启动命令、窗口名称, 后续应该还需要有应用的详细功能之类的说明
EXTRA_APP_SETUP_DICT = {
    "pycharm": {
        "commands": [
            [
                "pycharm-community"
            ]
        ]
    },
    "blender": {
        "commands": [
            [
                "blender"
            ]
        ]
    },
    "dbeaver": {
        "commands": [
            [
                "dbeaver-ce"
            ]
        ]
    },
    "wireshark": {
        "commands": [
            [
                "sudo wireshark"
            ]
        ]
    },
    "texstudio": {
        "commands": [
            [
                "texstudio" # ~/Downloads/bare_jrnl.tex
            ]
        ]
    },
    "gitkraken": {
        "commands": [
            [
                "gitkraken"
                ]
        ]
    },
    "scilab": {
        "commands": [
            [
                "scilab"
            ]
        ]
    },
    "audacity": {
        "commands": [
            [
                "audacity"
            ]
        ]
    },
    "librecad": {
        "commands": [
            [
                "librecad"
            ]
        ]
    },
    "drawio": {
        "commands": [
            [
                "drawio"
            ]
        ]
    },
    "filezilla": {
        "commands": [
            [
                "filezilla"
            ]
        ]
    },
    "darktable": {
        "commands": [
            [
                "darktable"
            ]
        ]
    },
    "handbrake": {
        "commands": [
            [
                "handbrake"
            ]
        ]
    },
    "homebank": {
        "commands": [
            [
                "homebank"
            ]
        ]
    },
    "mixxx": {
        "commands": [
            [
                "mixxx"
            ]
        ]
    },
    "inkscape": {
        "commands": [
            [
                "inkscape"
            ]
        ]
    },
    "obs": {
        "commands": [
            [
                "obs"
            ]
        ]
    },
    "meld": {
        "commands": [
            [
                "meld"
            ]
        ]
    },
    "musescore": {
        "commands": [
            [
                "musescore"
            ]
        ]
    },
    "zotero": {
        "commands": [
            [
                "zotero-snap"
            ]
        ]
    },
    "zoom": {
        "commands": [
            [
                "zoom"
            ]
        ]
    },
    "google-earth-pro": {
        "commands": [
            [
                "google-earth-pro"
            ]
        ]
    },
    "sweethome3d": {
        "commands": [
            [
                "sweethome3d"
            ]
        ]
    },
    "kicad": {
        "commands": [
            [
                "kicad"
            ]
        ]
    },
    "spotify": {
        "commands": [
            [
                "spotify"
            ]
        ]
    },
    "calendar": {
        "commands": [
            [
                "gnome-calendar"
            ]
        ]
    },
    "shotcut": {
        "commands": [
            [
                "shotcut"
            ]
        ]
    },
    "krita": {
        "commands": [
            [
                "krita"
            ]
        ]
    },
    "pdfarranger": {
        "commands": [
            [
                "pdfarranger"
            ]
        ]
    },
    "grass": {
        "commands": [
            [
                "grass"
            ]
        ]
    },
}

"""
    需要讨论: 需要哪种程度的初始化? 软件通常与文件挂钩, 如何获取各种文件进行更丰富的初始化与数据采集, 是否是一个idea
    目前列出来的 commands 都默认是执行cli命令, 按理说也可以执行download等下载命令, 比较万能(不一定非得用download操作), 但有待验证
"""
OSWORLD_APP_SETUP_DICT = {
    "chrome": {
        "window_name": "Google Chrome",
        "commands": [
            [
                "google-chrome", 
                "--remote-debugging-port=1337", 
                "--start-maximized" # "https://www.bing.com"
            ],
            [
                "socat", 
                "tcp-listen:9222,fork", 
                "tcp:localhost:1337"
            ]
        ]
    },
    "gimp": {
        "commands": [
            [
                "gimp", # "/path/to/file"
            ]
        ]
    },
    "libreoffice_impress": {
        "window_name": "LibreOffice Impress",
        "commands": [
            [
                "libreoffice",
                "--impress",
                "--nologo",
                "--norestore" # 避免崩溃后启动弹出恢复窗口
                # "/path/to/presentation.odp" # 可选：指定打开的文件
            ]
        ]
    },
    "libreoffice_calc": {
        "window_name": "LibreOffice Calc",
        "commands": [
            [
                "libreoffice",
                "--calc",
                "--nologo",
                "--norestore"
                # "/path/to/spreadsheet.ods" # 可选：指定打开的文件
            ]
        ]
    },
    "libreoffice_writer": {
        "window_name": "LibreOffice Writer",
        "commands": [
            [
                "libreoffice",
                "--writer",
                "--nologo",
                "--norestore"
                # "/path/to/document.odt" # 可选：指定打开的文件
            ]
        ]
    },
    "vscode": {
        "window_name": "Visual Studio Code",
        "commands": [
            [
                "code", 
                "--new-window" # /home/user/project.code-workspace
            ]
        ]
    },
    "terminal": {
        "window_name": "Terminal"
    },
    "thunderbird": {
        "commands": [
            [
                "/usr/bin/thunderbird" # 需要 profile, 可能需要提前下载好
            ]
        ]
    },
    "vlc": {
        "commands": [
            [
                "VLC_VERBOSE=-1",
                "vlc",
                "--no-audio",
                "--no-video-title-show"  # "--play-and-pause" "/home/user/Desktop/Interstellar Movie - Official Trailer.mp4'"
            ]
        ]
    }
}

APP_SETUP_DICT = OSWORLD_APP_SETUP_DICT | EXTRA_APP_SETUP_DICT
class OSCaliberTaskGenerator:
    def __init__(self, rollout_task_dir: str) -> None:
        self.rollout_task_dir = rollout_task_dir

    # 后续需要进一步初始化
    def _generate_config(self, app_name: str) -> List[Dict[str, Any]]:
        """根据 APP_SETUP_DICT 生成标准的 config 列表"""
        app_info = APP_SETUP_DICT.get(app_name)
        if not app_info:
            # 如果没有配置，返回一个空的默认配置或抛出警告
            return []

        config_list = []
        
        # 1. 生成 Launch 命令
        for cmd in app_info.get("commands", []):
            config_list.append({
                "type": "launch",
                "parameters": {
                    "command": cmd
                }
            })
        
        # 2. 生成 Activate Window 命令 (通常需要确保窗口在前台)
        if "window_name" in app_info:
            config_list.append({
                "type": "activate_window",
                "parameters": {
                    "window_name": app_info["window_name"]
                }
            })
            
        return config_list

    def generate_task(self, env: DesktopEnv, agent: CoarseInstructionGenerationAgent, task_nums=10, app_list: List|str = []):
        """
        生成任务文件
        :param task_nums: 总共需要生成的任务数量
        :param app_dict: 指定要生成的应用列表，如果为空则使用 APP_SETUP_DICT 中的所有应用
        :return: (test_file_list, current_base_dir)
        """
        # 如果传入了 app_dict，则只从里面选，否则从全局配置选
        if isinstance(app_list, list):
            available_apps = app_list if app_list else list(APP_SETUP_DICT.keys())
        else:
            # app_list == "all"
            available_apps = list(APP_SETUP_DICT.keys())

        if not available_apps:
            raise ValueError("No apps available to generate tasks.")

        test_file_list = {}
        
        # 随机选择一个应用
        app_name = random.choice(available_apps)
        domain_dir = os.path.join(self.rollout_task_dir, app_name)
        os.makedirs(domain_dir, exist_ok=True)

        task_setup_config = self._generate_config(app_name)
        env.reset(task_config={"config": task_setup_config, "id": "114514", "instruction": "114514"})
        agent.reset()

        obs = env._get_obs()
        task_list = agent.generate(app_name=app_name, observation=obs, task_nums=task_nums)

        for task in task_list:
            # 生成唯一 Task ID
            task_id = str(uuid.uuid4())

            # 构造 JSON 内容
            task_config = {
                "id": task_id,
                "snapshot": app_name, # 对应 domain/app
                "instruction": task["description"], # 目前 Hardcode
                "config": task_setup_config,
                "complexity": task["complexity"],
                "verification": task["verification"]
            }

        
            json_path = os.path.join(domain_dir, f"{task_id}.json")
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(task_config, f, indent=4, ensure_ascii=False)
        
            if app_name not in test_file_list:
                test_file_list[app_name] = []
            test_file_list[app_name].append(task_id)

        return test_file_list

# # --- 使用示例 ---
# if __name__ == "__main__":
#     generator = OSCaliberTaskGenerator()
    
#     # 场景 1: 默认从所有配置中随机生成 5 个任务
#     file_list, base_path = generator.generate_task(task_nums=5)
#     print("Test File List:", json.dumps(file_list, indent=2))
#     print("Base Path:", base_path)
    
#     print("-" * 20)
    
#     time.sleep(3)
#     # 场景 2: 指定只生成 chrome 和 vscode 的任务
#     target_apps = ["chrome", "vscode"]
#     file_list_2, base_path_2 = generator.generate_task(task_nums=3, app_list=target_apps)
#     print("Test File List 2:", json.dumps(file_list_2, indent=2))