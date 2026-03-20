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
        "commands": [["pycharm-community", "PATH"]],
    },
    "blender": {
        "type": ["blend"],
        "commands": [["blender", "PATH"]],
    },
    "dbeaver": {
        "type": ["sql"],
        "commands": [["dbeaver-ce", "PATH"]],
    },
    "wireshark": {
        "type": ["pcapng"],
        "commands": [["sudo", "wireshark", "PATH"]],
    },
    "texstudio": {
        "type": ["tex"],
        "commands": [["texstudio", "PATH"]],
    },
    "gitkraken": {
        "type": ["project_folder"],
        "commands": [["gitkraken", "-p", "PATH"]],
    },
    "scilab": {
        "type": ["sci"],
        "commands": [["scilab", "-f", "PATH"]],
    },
    "audacity": {
        "type": ["wav", "mp3"],
        "commands": [["audacity", "PATH"]],
    },
    "librecad": {
        "type": ["dxf"],
        "commands": [["librecad", "PATH"]],
    },
    "drawio": {
        "type": ["drawio"],
        "commands": [["drawio", "PATH"]],
    },
    "darktable": {
        "type": ["png"],
        "commands": [["darktable", "PATH"]],
    },
    "handbrake": {
        "type": ["mp4"],
        "commands": [["handbrake", "PATH"]],
    },
    "homebank": {
        "type": ["xhb"],
        "commands": [["homebank", "PATH"]],
    },
    "mixxx": {
        "type": ["mp3"],
        "commands": [["mixxx", "-f", "PATH"]],
    },
    "inkscape": {
        "type": ["svg"],
        "commands": [["inkscape", "PATH"]],
    },
    "obs": {
        "commands": [["obs"]],
    },
    "meld": {
        "type": ["py"],
        "commands": [["meld", "PATH", "PATH"]],
    },
    "musescore": {
        "type": ["mscz"],
        "commands": [["musescore", "PATH"]],
    },
    "zotero": {
        "commands": [["zotero-snap"]],
    },
    "zoom": {
        "commands": [["zoom"]],
    },
    "google-earth-pro": {
        "type": ["kmz"],
        "commands": [["google-earth-pro", "PATH"]],
    },
    "kicad": {
        "commands": [["kicad"]],
    },
    "spotify": {
        "commands": [["spotify"]],
    },
    "calendar": {
        "commands": [["gnome-calendar"]],
    },
    "shotcut": {
        "type": ["mp4"],
        "commands": [["shotcut", "PATH"]],
    },
    "krita": {
        "type": ["kra"],
        "commands": [["krita", "PATH"]],
    },
    "pdfarranger": {
        "type": ["pdf"],
        "commands": [["pdfarranger", "PATH"]],
    },
    "grass": {
        "commands": [["grass"]],
    },
    "notion": {
        "commands": [["notion-desktop"]],
    },
    "foliate": {
        "commands": [["foliate", "PATH"]],
    },
}

OSWORLD_APP_SETUP_DICT = {
    "chrome": {
        "type": ["url"],
        "window_name": "Google Chrome",
        "commands": [
            [
                "google-chrome",
                "--remote-debugging-port=1337",
                "--start-maximized",
                "https://www.bing.com",
            ],
            ["socat", "tcp-listen:9222,fork", "tcp:localhost:1337"],
        ],
    },
    "gimp": {
        "type": ["png"],
        "commands": [["gimp", "PATH"]],
    },
    "libreoffice_impress": {
        "type": ["pptx"],
        "window_name": "LibreOffice Impress",
        "commands": [
            [
                "libreoffice",
                "--impress",
                "--nologo",
                "--norestore",
                "PATH",
            ]
        ],
    },
    "libreoffice_calc": {
        "type": ["xlsx"],
        "window_name": "LibreOffice Calc",
        "commands": [
            [
                "libreoffice",
                "--calc",
                "--nologo",
                "--norestore",
                "PATH",
            ]
        ],
    },
    "libreoffice_writer": {
        "type": ["docx"],
        "window_name": "LibreOffice Writer",
        "commands": [
            [
                "libreoffice",
                "--writer",
                "--nologo",
                "--norestore",
                "PATH",
            ]
        ],
    },
    "vscode": {
        "type": ["project_folder", "py"],
        "commands": [["code", "--new-window", "PATH"]],
    },
    "thunderbird": {
        "commands": [["/usr/bin/thunderbird"]],
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
                "PATH",
            ]
        ],
    },
}

APP_SETUP_DICT = OSWORLD_APP_SETUP_DICT | EXTRA_APP_SETUP_DICT
ENV_FILE_BASE_DIR = "/home/user/Desktop/test_files"
APP_TUTORIAL_DIR = "evaluation_examples/ubuntu_online_rollout/app_tutorial"


class OSCaliberTaskGenerator:
    def __init__(
        self,
        rollout_task_dir: str,
        env: DesktopEnv,
        agent: CoarseInstructionGenerationAgent,
    ) -> None:
        self.rollout_task_dir = rollout_task_dir
        self.env_file_base_dir = ENV_FILE_BASE_DIR
        self.env = env
        self.agent = agent

    def _load_app_tutorial_md(self, app_name: str) -> str:
        """读取对应 app 的 tutorial markdown，如果不存在则返回空字符串。"""
        md_path = os.path.join(APP_TUTORIAL_DIR, f"{app_name}.md")
        if not os.path.exists(md_path):
            return ""
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _generate_random_coordinates(self) -> Tuple[str, str, str]:
        lat = round(random.uniform(-90.0, 90.0), 6)
        lon = round(random.uniform(-180.0, 180.0), 6)
        range_val = random.randint(1000, 5000000)
        return str(lat), str(lon), str(range_val)

    def _generate_config(self, app_name: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """根据 APP_SETUP_DICT 生成标准的 config 列表，同时返回实际使用的 PATH 列表。

        引入 "不带 PATH" 的概率：
        - 概率 0.6: 完全不替换 PATH（即不打开具体文件），launch_paths 为空。
        - 概率 0.4: 按原逻辑从 file_lists 中随机选一个文件替换 PATH。
        """
        app_info = APP_SETUP_DICT.get(app_name, {})
        if not app_info:
            return [], []

        config_list: List[Dict[str, Any]] = []
        used_paths: List[str] = []

        type_lists = app_info.get("type", [])
        file_abs_lists: List[str] = []

        for file_type in type_lists:
            if file_type == "url":
                continue
            target_dir = os.path.join(self.env_file_base_dir, file_type)
            try:
                file_lists_for_single_type = self.env.controller.get_file_lists(target_dir)
            except Exception as e:
                print(f"Warning: Could not list files in {target_dir}: {e}")
                file_lists_for_single_type = []

            if file_lists_for_single_type and isinstance(file_lists_for_single_type, list):
                for f in file_lists_for_single_type:
                    file_abs_lists.append(str(os.path.join(target_dir, f)))

        raw_commands = copy.deepcopy(app_info.get("commands", []))

        # 决定本轮是否使用 PATH
        # 0.6 概率不使用 PATH（launch_paths 为空），0.4 概率使用文件
        no_path_mode = random.random() < 0.6

        for cmd in raw_commands:
            # 如果完全不使用 PATH，直接删除所有纯 "PATH" 占位符参数
            if no_path_mode:
                cleaned_cmd = [c for c in cmd if c != "PATH"]
                if not cleaned_cmd:
                    continue
                config_list.append({"type": "launch", "parameters": {"command": cleaned_cmd}})
                continue

            # 使用文件模式
            for i in range(len(cmd)):
                param = cmd[i]
                if "PATH" in param:
                    if file_abs_lists:
                        selected_file = random.choice(file_abs_lists)

                        if app_name in ["blender", "texstudio"] and "." not in selected_file.split("/")[-1]:
                            try:
                                sub_files = self.env.controller.get_file_lists(selected_file)
                                if sub_files and isinstance(sub_files, list):
                                    for sub_f in sub_files:
                                        if sub_f.endswith(".blend") or sub_f.endswith(".tex"):
                                            selected_file = os.path.join(selected_file, sub_f)
                                            break
                            except Exception as e:
                                print(f"Error searching inner file in {selected_file}: {e}")

                        cmd[i] = param.replace("PATH", selected_file)
                        used_paths.append(selected_file)
                    else:
                        if param == "PATH":
                            cmd[i] = ""
                        print(f"Warning: No files found for {app_name}, starting without file.")

            cleaned_cmd = [c for c in cmd if c != ""]
            if not cleaned_cmd:
                continue
            config_list.append({"type": "launch", "parameters": {"command": cleaned_cmd}})

        used_paths = sorted(list(set(used_paths)))
        return config_list, used_paths

    def _build_evaluator_from_verification(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """根据 coarse agent 产出的新字段，构造 evaluator skeleton。

        输出结构与 DesktopEnv._set_evaluator_info 所需格式对齐：
        - func: metric 名或列表
        - conj: 组合方式（多 metric 时）
        - result / expected: getter 配置
        - options: 额外元信息（这里挂 oscaliber_meta）
        """
        verification = task.get("verification") or {}
        eval_type = (verification.get("evaluation_type") or "rule_based").lower()

        if eval_type == "rule_based":
            func: Any = "oscaliber_rule_based_metric"
            result = [{"type": "oscaliber_rule_based_result", "options": {}}]
            expected = [{"type": "oscaliber_rule_based_expected", "options": {}}]
        elif eval_type == "vlm_based":
            func = "oscaliber_vlm_based_metric"
            result = [{"type": "oscaliber_vlm_based_result", "options": {}}]
            expected = [{"type": "oscaliber_vlm_based_expected", "options": {}}]
        else:  # "hybrid" 或其他
            func = ["oscaliber_rule_based_metric", "oscaliber_vlm_based_metric"]
            result = [
                {"type": "oscaliber_rule_based_result", "options": {}},
                {"type": "oscaliber_vlm_based_result", "options": {}},
            ]
            expected = [
                {"type": "oscaliber_rule_based_expected", "options": {}},
                {"type": "oscaliber_vlm_based_expected", "options": {}},
            ]

        evaluator = {
            "func": func,
            "conj": "and",
            "result": result,
            "expected": expected,
            "options": {
                "oscaliber_meta": {
                    "evaluation_type": eval_type,
                    "evaluation_desc": verification.get("evaluation_desc", ""),
                    "condition": verification.get("condition", ""),
                    "expected_result": verification.get("expected_result", ""),
                    "complexity": task.get("complexity", "medium"),
                    "estimated_steps": task.get("estimated_steps", 0),
                    "category": task.get("category", "mixed"),
                }
            },
        }
        return evaluator

    def generate_all(self, task_nums: int = 1):
        available_apps = list(APP_SETUP_DICT.keys())
        test_file_list: Dict[str, List[str]] = {}
        for available_app in available_apps:
            test_file_list |= self.generate_task(task_nums=task_nums, app_list=[available_app])
        return test_file_list

    def generate_task(self, task_nums: int = 10, app_list: List | str = []):
        if isinstance(app_list, list) and len(app_list) > 0:
            available_apps = app_list
        else:
            available_apps = list(APP_SETUP_DICT.keys())

        if not available_apps:
            raise ValueError("No apps available to generate tasks.")

        test_file_list: Dict[str, List[str]] = {}
        app_name = random.choice(available_apps)
        domain_dir = os.path.join(self.rollout_task_dir, app_name)
        os.makedirs(domain_dir, exist_ok=True)

        # 生成配置 + 实际使用的 PATH 列表
        task_setup_config, launch_paths = self._generate_config(app_name)

        print(f"Generating tasks for {app_name}...")
        self.env.reset(
            task_config={
                "config": task_setup_config,
                "id": "init_id",
                "instruction": "init_instruction",
            }
        )
        self.agent.reset()

        obs = self.env._get_obs()

        # 注入 app tutorial md
        app_tutorial_md = self._load_app_tutorial_md(app_name)

        # 让 Agent 生成任务描述（传入 launch_paths 和教程）
        task_list = self.agent.generate(
            app_name=app_name,
            observation=obs,
            task_nums=task_nums,
            launch_paths=launch_paths,
            app_tutorial_md=app_tutorial_md,
        )

        for task in task_list:
            task_id = str(uuid.uuid4())

            task_config = {
                "id": task_id,
                "snapshot": app_name,
                "related_apps": [app_name],
                "instruction": task.get("description"),
                "config": task_setup_config,
                # 复杂度与估计步数（供后续评估使用）
                "complexity": task.get("complexity"),
                "estimated_steps": task.get("estimated_steps"),
                # 评估信息：rule_based / vlm_based / hybrid + 描述
                "verification": task.get("verification"),
                "category": task.get("category"),  # file_only / app_only / mixed
            }

            # 构造 evaluator skeleton，供 DesktopEnv 使用
            task_config["evaluator"] = self._build_evaluator_from_verification(task)

            json_path = os.path.join(domain_dir, f"{task_id}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(task_config, f, indent=4, ensure_ascii=False)

            if app_name not in test_file_list:
                test_file_list[app_name] = []
            test_file_list[app_name].append(task_id)

        return test_file_list
