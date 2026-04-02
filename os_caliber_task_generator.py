import copy
import logging
import os
import json
import uuid
import random
import time
import shutil
from datetime import datetime
from typing import List, Dict, Tuple, Any
import ast
from desktop_env.osworld.desktop_env import DesktopEnv
from mm_agents.os_symphony.agents.coarse_instruction_generation_agent import InstructionGenerationAgent

logger = logging.getLogger("desktopenv.task_generator")

# APP 初始化信息
APP_CONFIG_PATH = "evaluation_examples/ubuntu_online_rollout/config/app_config.json"
APP_CONFIG_DICT: Dict = json.load(open(APP_CONFIG_PATH, "r"))

APP_SET_CONFIG_DICT = APP_CONFIG_DICT.get("app", {})
EXCLUDED_APP_LIST = APP_CONFIG_DICT.get("excluded", [])
for e in EXCLUDED_APP_LIST:
    if e in APP_SET_CONFIG_DICT:
        del APP_SET_CONFIG_DICT[e]

# For backward compatibility keep a semantic alias
APP_SETUP_DICT = APP_SET_CONFIG_DICT

# Build a directed application graph from config
APP_GRAPH: Dict[str, List[str]] = {}
TYPE_TO_APPS: Dict[str, List[str]] = {}

for app_name, cfg in APP_SETUP_DICT.items():
    # explicit directed edges from related_app
    rel_apps = cfg.get("related_app", []) or []
    APP_GRAPH[app_name] = [a for a in rel_apps if a in APP_SETUP_DICT]

    # index related_type for implicit edges
    rel_types = cfg.get("related_type", []) or []
    for t in rel_types:
        TYPE_TO_APPS.setdefault(t, []).append(app_name)

# add implicit directed edges based on shared related_type
for t, apps in TYPE_TO_APPS.items():
    if len(apps) <= 1:
        continue
    for src in apps:
        for dst in apps:
            if src == dst:
                continue
            if dst not in APP_GRAPH[src]:
                APP_GRAPH[src].append(dst)
                APP_GRAPH[dst].append(src) # 有向图 -> 无向图
# print(f'APP GRAPH: {APP_GRAPH}')

# 预制 URL, 适用于 chrome 软件的初始化
URL_CONFIG_PATH = "evaluation_examples/ubuntu_online_rollout/config/url.json"
URL_LIST: List = json.load(open(URL_CONFIG_PATH, "r"))

ENV_FILE_BASE_DIR = "/home/user/Desktop/test_files"
APP_TUTORIAL_DIR = "evaluation_examples/ubuntu_online_rollout/app_tutorial"

def extract_function_docstring(code_str, function_name=None):
    try:
        mod = ast.parse(code_str)
        # 遍历所有节点，找到函数定义
        for node in ast.walk(mod):
            if isinstance(node, ast.FunctionDef):
                # 如果指定了函数名，则匹配；否则取第一个函数
                if function_name is None or node.name == function_name:
                    return ast.get_docstring(node)
        return ""
    except Exception:
        return ""
    
class OSCaliberTaskGenerator:
    def __init__(
        self,
        rollout_task_dir: str,
        env: DesktopEnv,
        agent: InstructionGenerationAgent,
    ) -> None:
        self.rollout_task_dir = rollout_task_dir
        self.env_file_base_dir = ENV_FILE_BASE_DIR
        self.env = env
        self.agent = agent
        # Cache for auto-generated evaluator functions from coarse agent.
        # Maps function_name -> code string.
        self.generated_evaluators: Dict[str, str] = {}

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

    def _get_abs_file_lists(self, type_lists):
        abs_file_lists: List[str] = []
        for file_type in type_lists:
            if file_type == "url":
                abs_file_lists.extend(URL_LIST)
            else:
                target_dir = os.path.join(self.env_file_base_dir, file_type)
                try:
                    file_lists_for_single_type = self.env.controller.get_file_lists(target_dir)
                except Exception as e:
                    print(f"Warning: Could not list files in {target_dir}: {e}")
                    file_lists_for_single_type = []

                if file_lists_for_single_type and isinstance(file_lists_for_single_type, list):
                    for f in file_lists_for_single_type:
                        abs_file_lists.append(str(os.path.join(target_dir, f)))
        return abs_file_lists
    
    def _sample_app_group(self, max_apps: int, available_apps: List[str]) -> Tuple[str, List[str]]:
        """Sample a main app and a group of related apps up to max_apps using APP_GRAPH.

        Returns (main_app, apps_for_group). The returned list always contains main_app
        and has length between 1 and max_apps, depending on graph connectivity.
        """
        if not available_apps:
            raise ValueError("No apps available to sample.")

        main_app = random.choice(available_apps)

        if max_apps <= 1:
            return main_app, [main_app]

        # target_count = random.randint(1, max_apps)
        target_count = max_apps
        apps_for_group: List[str] = [main_app]
        frontier: List[str] = [main_app]

        while len(apps_for_group) < target_count and frontier:
            candidates: List[str] = []
            for u in frontier:
                for v in APP_GRAPH.get(u, []):
                    if v in available_apps and v not in apps_for_group:
                        candidates.append(v)

            if not candidates:
                # 10% 概率全局随机跳边, 增强多样性
                leftover = [a for a in available_apps if a not in apps_for_group]
                if leftover and random.random() < 0.1:
                    v = random.choice(leftover)
                    apps_for_group.append(v)
                    frontier.append(v)
                    continue
                break

            v = random.choice(candidates)
            apps_for_group.append(v)
            frontier.append(v)

        return main_app, apps_for_group

    def _generate_config(self, app_name: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """根据 APP_SETUP_DICT 生成标准的 config 列表，同时返回实际使用的 PATH 列表。

        commands 结构说明：
        - APP_SETUP_DICT[app_name]["commands"] 是三层列表：
          List[SetupVariant]
          SetupVariant = List[Command]
          Command = List[str]
        - 这里会先随机选择一个 SetupVariant，再对其中每条 Command 做 PATH 替换。
        """
        app_info = APP_SETUP_DICT.get(app_name, {})
        if not app_info:
            return [], []

        config_list: List[Dict[str, Any]] = []
        used_paths: List[str] = []
        abs_file_lists = self._get_abs_file_lists(type_lists=app_info.get("type", []))

        # 取出所有 setup 变体（三层结构），根据 random 字段加权随机选择一个变体
        all_setups = app_info.get("commands", []) or []
        if not all_setups:
            return [], []

        weights = app_info.get("random")
        if isinstance(weights, list) and len(weights) == len(all_setups):
            chosen_setup = random.choices(all_setups, weights=weights, k=1)[0]
        else:
            # 兼容旧配置或 random 配置不匹配时，退回到均匀随机
            chosen_setup = random.choice(all_setups)

        # 深拷贝，避免修改原配置
        raw_commands: List[List[str]] = copy.deepcopy(chosen_setup)

        for cmd in raw_commands:
            for i in range(len(cmd)):
                param = cmd[i]
                if "PATH" in param:
                    if abs_file_lists:
                        selected_file = random.choice(abs_file_lists)

                        # 特殊软件特殊处理, 再往里获取一层
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
        """根据 coarse agent 产出的 verification 字段，构造最终 evaluator。

        目标输出格式：
        {
            "func": str | List[str],
            "conj": "and",
            "result": dict | List[dict],
            "expected": dict | List[dict],
            "code": str | List[str],
            "desc": str | List[str],
            "need_vlm_judge": bool,
            "vlm_desc": str,
            "need_rule_judge": bool,
            "dynamic": true # 即插即用, 评估时动态创建评估函数并执行, 评估结束后立即清理相关评估函数, 全是true就完事了
        }
        """
        verification = task.get("verification") or {}

        need_rule = bool(verification.get("need_rule_judge", False))
        need_vlm = bool(verification.get("need_vlm_judge", False))
        vlm_desc = verification.get("vlm_desc", "")
        rule_items = verification.get("rule_items") or []
        if not isinstance(rule_items, list):
            rule_items = []

        # 如果 coarse agent 给了 rule_items 但两个 flag 都是 False，则默认需要 rule judge
        if rule_items and not need_rule and not need_vlm:
            need_rule = True

        # 如果既不需要 rule 也不需要 vlm，则退化成简单的 vlm 检查
        if not need_rule and not need_vlm:
            need_vlm = True

        # 纯 VLM 任务，不需要 rule-based evaluator 细节
        if not need_rule:
            return {
                "func": "",
                "conj": "and",
                "result": [],
                "expected": [],
                "code": [],
                "desc": [],
                "need_vlm_judge": need_vlm,
                "vlm_desc": vlm_desc,
                "need_rule_judge": False,
                "dynamic": True
            }

        # 需要 rule-based 评估的情况
        funcs: List[str] = []
        results: List[Dict[str, Any]] = []
        expecteds: List[Dict[str, Any]] = []
        codes: List[str] = []
        descs: List[str] = []

        def _norm_getter(g: Any) -> Dict[str, Any]:
            if not isinstance(g, dict):
                return {"type": "empty"}
            g_type = g.get("type")
            if g_type == "vm_file":
                return {
                    "type": "vm_file",
                    "path": str(g.get("path", "")),
                    "dest": str(g.get("dest", "")),
                }
            if g_type == "vm_command_line":
                cmd = g.get("command")
                if isinstance(cmd, list):
                    cmd_list = [str(c) for c in cmd]
                elif cmd is None:
                    cmd_list = []
                else:
                    cmd_list = [str(cmd)]
                return {"type": "vm_command_line", "command": cmd_list}
            if g_type == "empty":
                return {"type": "empty"}
            return {"type": "empty"}

        for idx, item in enumerate(rule_items, start=1):
            if not isinstance(item, dict):
                continue
            fn_name = str(item.get("function_name") or f"call_rule_judge_{idx}").strip()
            result_getter = _norm_getter(item.get("result_getter"))
            expected_getter_raw = item.get("expected_getter")
            if expected_getter_raw is None:
                expected_getter = {"type": "empty"}
            else:
                expected_getter = _norm_getter(expected_getter_raw)

            code_str = item.get("code", "")

            # 解析上述 code_str, 尝试提取其 docstring 作为 check_desc
            check_desc = extract_function_docstring(code_str=code_str)

            funcs.append(fn_name)
            results.append(result_getter)
            expecteds.append(expected_getter)
            codes.append(str(code_str))
            descs.append(check_desc)

        # 如果只有一个 rule item，则压缩为标量，保证 func/result/expected/code/desc 一致
        if len(funcs) == 1:
            func_val = funcs[0]
            result_val = results[0]
            expected_val = expecteds[0]
            code_val = codes[0]
            desc_val = descs[0]
        else:
            func_val = funcs
            result_val = results
            expected_val = expecteds
            code_val = codes
            desc_val = descs

        evaluator = {
            "func": func_val,
            "conj": "and",  # 目前仅支持 and
            "result": result_val,
            "expected": expected_val,
            "code": code_val,
            "desc": desc_val,
            "need_vlm_judge": need_vlm,
            "vlm_desc": vlm_desc,
            "need_rule_judge": True,
            "dynamic": True
        }
        return evaluator

    def generate_task(self, task_nums: int = 10, app_list: List | str = [], max_apps_per_group: int = 1):
        if isinstance(app_list, list) and len(app_list) > 0:
            available_apps = app_list
        else:
            available_apps = list(APP_SETUP_DICT.keys())

        if not available_apps:
            raise ValueError("No apps available to generate tasks.")

        test_file_list: Dict[str, List[str]] = {}

        # 采样主 APP 以及与之相关的一组 APP, 目前只初始化主 APP
        main_app, apps_for_group = self._sample_app_group(max_apps=max_apps_per_group, available_apps=available_apps)
        logger.info(f"Generating tasks for {main_app} with app group: {apps_for_group}...")

        domain_dir = os.path.join(self.rollout_task_dir, main_app)
        os.makedirs(domain_dir, exist_ok=True)

        # 生成配置 + 实际使用的 PATH 列表 (仅主 APP)
        task_setup_config, launch_paths = self._generate_config(main_app)

        self.env.reset(
            task_config={
                "config": task_setup_config,
                "id": "init_id",
                "instruction": "init_instruction",
            }
        )
        time.sleep(20) # Wait for the set up already
        self.agent.reset()

        obs = self.env._get_obs()

        # 注入 app tutorial md (目前仅主 APP)
        app_tutorial_md = self._load_app_tutorial_md(main_app)

        # 让 Agent 生成任务描述（传入 launch_paths 和教程 + 多 APP 上下文）
        task_list = self.agent.generate(
            app_name=main_app,
            observation=obs,
            task_nums=task_nums,
            launch_paths=launch_paths,
            app_tutorial_md=app_tutorial_md,
            allowed_apps=apps_for_group,
        )

        for task in task_list:
            task_id = str(uuid.uuid4())

            json_path = os.path.join(domain_dir, f"{task_id}.json")
            image_base_dir = os.path.join(domain_dir, "image")
            os.makedirs(image_base_dir, exist_ok=True)

            # 每个 task 可以返回自己使用到的 related_apps, 若缺失则默认仅主 APP
            task_related_apps = task.get("related_apps") or [main_app]

            task_config = {
                "id": task_id,
                "snapshot": main_app,
                "related_apps": task_related_apps,
                "instruction": task.get("description"),
                "config": task_setup_config,
                "complexity": task.get("complexity"),
                "estimated_steps": task.get("estimated_steps"),
                "category": task.get("category"),  # file_only / app_only / mixed
                "evaluator": self._build_evaluator_from_verification(task),
                "setup_image": f"image/{task_id}.png" # Rel Path
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(task_config, f, indent=4, ensure_ascii=False)

            # 记录初始化截图
            with open(os.path.join(image_base_dir, f"{task_id}.png"), "wb") as _f:
                _f.write(obs['screenshot'])

            if main_app not in test_file_list:
                test_file_list[main_app] = []
            test_file_list[main_app].append(task_id)

        return test_file_list


if __name__=="__main__":
    """
        给定 root_dir, 子目录为 domain, 解析其子目录的所有 task 文件的 evaluator(可能是一个字典)
    """