from __future__ import annotations

import argparse
import ast
import datetime
import json
import logging
import os
import random
import re
import signal
import sys
import time
import uuid
from multiprocessing import Manager, Process, current_process
from queue import Queue
from typing import Any, Dict, List, Tuple

from desktop_env.osworld.desktop_env import DesktopEnv
from mm_agents.os_symphony.agents.instruction_generator.workflow import (
    GenerationContext,
    InstructionGenerationWorkflow,
)
from mm_agents.os_symphony.utils.process_context import set_current_result_dir

if os.path.exists(".env"):
    from dotenv import load_dotenv

    load_dotenv()

logger = logging.getLogger("desktopenv.ossymphony2_task_generation")
active_environments: List[DesktopEnv] = []
processes: List[Process] = []
is_terminating = False

APP_CONFIG_PATH = "evaluation_examples/ubuntu_online_rollout/config/app_config.json"
URL_CONFIG_PATH = "evaluation_examples/ubuntu_online_rollout/config/url.json"
ENV_FILE_BASE_DIR = "/home/user/Desktop/test_files"
APP_TUTORIAL_DIR = "evaluation_examples/ubuntu_online_rollout/app_tutorial"

with open(APP_CONFIG_PATH, "r", encoding="utf-8") as f:
    APP_CONFIG_DICT: Dict[str, Any] = json.load(f)
with open(URL_CONFIG_PATH, "r", encoding="utf-8") as f:
    URL_LIST: List[str] = json.load(f)

APP_SET_CONFIG_DICT: Dict[str, Any] = APP_CONFIG_DICT.get("app", {})
for excluded_app in APP_CONFIG_DICT.get("excluded", []):
    APP_SET_CONFIG_DICT.pop(excluded_app, None)
APP_SETUP_DICT = APP_SET_CONFIG_DICT

APP_GRAPH: Dict[str, List[str]] = {}
TYPE_TO_APPS: Dict[str, List[str]] = {}
for app_name, cfg in APP_SETUP_DICT.items():
    APP_GRAPH[app_name] = [app for app in cfg.get("related_app", []) or [] if app in APP_SETUP_DICT]
    for related_type in cfg.get("related_type", []) or []:
        TYPE_TO_APPS.setdefault(related_type, []).append(app_name)

for apps in TYPE_TO_APPS.values():
    if len(apps) <= 1:
        continue
    for src in apps:
        for dst in apps:
            if src != dst and dst not in APP_GRAPH[src]:
                APP_GRAPH[src].append(dst)

POST_CONFIG = [
    {
        "type": "execute",
        "parameters": {
            "command": [
                "python",
                "-c",
                "import pyautogui; import time; pyautogui.hotkey('ctrl', 's'); time.sleep(0.5);",
            ]
        },
    },
    {"type": "sleep", "parameters": {"seconds": 0.5}},
]


def config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate OSSymphony2 tasks with the multi-stage workflow")
    parser.add_argument("--path_to_vm", type=str, default="/nvme/yangbowen/osworld/docker_vm_data/Ubuntu_write.qcow2")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--action_space", type=str, default="pyautogui")
    parser.add_argument(
        "--observation_type",
        choices=["screenshot", "a11y_tree", "screenshot_a11y_tree", "som"],
        default="screenshot",
    )
    parser.add_argument("--provider_name", type=str, default="docker", choices=["aws", "virtualbox", "vmware", "docker", "azure"])
    parser.add_argument("--region", type=str, default="us-east-1")
    parser.add_argument("--client_password", type=str, default="password")
    parser.add_argument("--screen_width", type=int, default=1920)
    parser.add_argument("--screen_height", type=int, default=1080)
    parser.add_argument("--rollout_base_dir", type=str, default="evaluation_examples/ubuntu_online_rollout/synthesis")
    parser.add_argument("--rollout_task_dir", type=str, default=None)
    parser.add_argument("--rollout_times", type=int, default=10)
    parser.add_argument("--rollout_task_nums", type=int, default=10)
    parser.add_argument("--rollout_max_apps_per_group", type=int, default=2)
    parser.add_argument("--rollout_app_list", nargs="+", default=[])
    parser.add_argument("--num_envs", type=int, default=1)
    parser.add_argument("--exp_name", type=str, default="")
    parser.add_argument("--log_level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")
    parser.add_argument("--provider", type=str, default="openai")
    parser.add_argument("--model", type=str, default="gpt-5")
    parser.add_argument("--generator_model", type=str, default=None)
    parser.add_argument("--scorer_model", type=str, default=None)
    parser.add_argument("--base_url", type=str, default="https://api.boyuerichdata.opensphereai.com/v1")
    parser.add_argument("--api_key", type=str, default="")
    parser.add_argument("--temperature", type=float, default=0.5)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--max_tokens", type=int, default=32768)
    parser.add_argument("--setup_wait_seconds", type=float, default=20.0)
    parser.add_argument("--max_repair_rounds", type=int, default=2)
    parser.add_argument("--exploration_max_actions", type=int, default=10)
    return parser.parse_args()


def setup_logging(log_level: str) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper()))
    handler.setFormatter(
        logging.Formatter(
            fmt="\x1b[1;33m[%(asctime)s \x1b[31m%(levelname)s \x1b[32m%(module)s/%(lineno)d-%(processName)s\x1b[1;33m] \x1b[0m%(message)s"
        )
    )
    handler.addFilter(logging.Filter("desktopenv"))
    root_logger.addHandler(handler)


def extract_function_docstring(code_str: str, function_name: str | None = None) -> str:
    try:
        mod = ast.parse(code_str)
        for node in ast.walk(mod):
            if isinstance(node, ast.FunctionDef) and (function_name is None or node.name == function_name):
                return ast.get_docstring(node) or ""
    except Exception:
        return ""
    return ""


class OSSymphony2TaskGenerator:
    def __init__(
        self,
        rollout_task_dir: str,
        env: DesktopEnv,
        engine_params: Dict[str, Any],
        scorer_engine_params: Dict[str, Any] | None = None,
        platform: str = "linux",
        setup_wait_seconds: float = 20.0,
        max_repair_rounds: int = 2,
        exploration_max_actions: int = 10,
    ) -> None:
        self.rollout_task_dir = rollout_task_dir
        self.env_file_base_dir = ENV_FILE_BASE_DIR
        self.env = env
        self.engine_params = engine_params
        self.scorer_engine_params = scorer_engine_params or engine_params
        self.platform = platform
        self.setup_wait_seconds = setup_wait_seconds
        self.max_repair_rounds = max_repair_rounds
        self.exploration_max_actions = exploration_max_actions

    def generate_task(self, task_nums: int = 10, app_list: List[str] | str | None = None, max_apps_per_group: int = 1) -> Dict[str, List[str]]:
        available_apps = self._available_apps(app_list)
        sampled_apps = self._sample_app_group(max_apps=max_apps_per_group, available_apps=available_apps)
        app_file_support = {app: list(APP_SETUP_DICT.get(app, {}).get("type", []) or []) for app in sampled_apps}
        sampled_files = self._sample_files(sampled_apps, app_file_support)
        rollout_id = str(uuid.uuid4())
        domain_key = "__".join(sampled_apps) if sampled_apps else rollout_id
        domain_dir = os.path.join(self.rollout_task_dir, domain_key)
        rollout_dir = os.path.join(domain_dir, rollout_id)
        os.makedirs(rollout_dir, exist_ok=True)

        logger.info("Generating OSSymphony2 workflow tasks for sampled apps: %s; sampled files: %s", sampled_apps, [f.get("path") for f in sampled_files])
        initial_config: List[Dict[str, Any]] = []
        self.env.reset(task_config={"config": initial_config, "id": "init_id", "instruction": "init_instruction"})
        if self.setup_wait_seconds > 0:
            time.sleep(self.setup_wait_seconds)
        obs = self.env._get_obs()

        context = GenerationContext(
            rollout_id=rollout_id,
            sampled_apps=sampled_apps,
            app_file_support=app_file_support,
            sampled_files=sampled_files,
            app_tutorials={app: self._load_app_tutorial_md(app) for app in sampled_apps},
            app_memory={},
            app_versions={app: APP_SET_CONFIG_DICT.get(app, {}).get("version", app) for app in sampled_apps},
            app_open_commands={app: self._open_command_variants(app) for app in sampled_apps},
            observation=obs,
            setup_image=obs["screenshot"],
            initial_config=initial_config,
        )
        workflow = InstructionGenerationWorkflow(
            rollout_task_dir=self.rollout_task_dir,
            env=self.env,
            engine_params=self.engine_params,
            build_evaluator_fn=self._build_evaluator_from_verification,
            app_version_lookup=lambda app: APP_SET_CONFIG_DICT.get(app, {}).get("version", app),
            platform=self.platform,
            max_repair_rounds=self.max_repair_rounds,
            exploration_max_actions=self.exploration_max_actions,
            scorer_engine_params=self.scorer_engine_params,
        )
        return workflow.run(context=context, task_nums=task_nums, rollout_dir=rollout_dir)

    def _available_apps(self, app_list: List[str] | str | None) -> List[str]:
        if isinstance(app_list, str) and app_list:
            requested = [app_list]
        elif isinstance(app_list, list) and app_list:
            requested = app_list
        else:
            requested = list(APP_SETUP_DICT.keys())
        available_apps = [app for app in requested if app in APP_SETUP_DICT]
        if not available_apps:
            raise ValueError("No apps available to generate tasks.")
        return available_apps

    def _load_app_tutorial_md(self, app_name: str) -> str:
        md_path = os.path.join(APP_TUTORIAL_DIR, f"{app_name}.md")
        if not os.path.exists(md_path):
            return ""
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _get_abs_file_lists(self, type_lists: List[str]) -> List[Dict[str, str]]:
        abs_file_lists: List[Dict[str, str]] = []
        for file_type in type_lists:
            if file_type == "url":
                abs_file_lists.extend({"path": str(url), "type": file_type} for url in URL_LIST)
                continue
            target_dir = os.path.join(self.env_file_base_dir, file_type)
            try:
                file_lists_for_single_type = self.env.controller.get_file_lists(target_dir)
            except Exception as e:
                logger.warning("Could not list files in %s: %s", target_dir, e)
                file_lists_for_single_type = []
            if isinstance(file_lists_for_single_type, list):
                for filename in file_lists_for_single_type:
                    path = os.path.join(target_dir, str(filename))
                    if file_type in {"blend", "tex", "project_folder"} and "." not in os.path.basename(path):
                        path = self._maybe_select_inner_project_file(path)
                    abs_file_lists.append({"path": path, "type": file_type})
        return abs_file_lists

    def _sample_app_group(self, max_apps: int, available_apps: List[str]) -> List[str]:
        max_apps = max(1, min(max_apps, len(available_apps)))
        target_count = random.randint(1, max_apps)
        sampled_apps = [random.choice(available_apps)]
        frontier = list(sampled_apps)
        while len(sampled_apps) < target_count and frontier:
            candidates: List[str] = []
            for app in frontier:
                candidates.extend([neighbor for neighbor in APP_GRAPH.get(app, []) if neighbor in available_apps and neighbor not in sampled_apps])
            if not candidates:
                leftover = [app for app in available_apps if app not in sampled_apps]
                if not leftover:
                    break
                picked = random.choice(leftover)
            else:
                picked = random.choice(candidates)
            sampled_apps.append(picked)
            frontier.append(picked)
        return sampled_apps

    def _sample_files(self, sampled_apps: List[str], app_file_support: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        max_file_count = len(sampled_apps) + 1
        requested_count = random.randint(0, max_file_count)
        if requested_count == 0:
            return []
        supported_types = sorted({file_type for types in app_file_support.values() for file_type in types})
        if not supported_types:
            return []
        file_pool = self._get_abs_file_lists(supported_types)
        if not file_pool:
            return []
        random.shuffle(file_pool)
        sampled: List[Dict[str, Any]] = []
        seen_paths = set()
        for file_info in file_pool:
            if len(sampled) >= requested_count:
                break
            path = file_info.get("path", "")
            file_type = file_info.get("type", "")
            if not path or path in seen_paths:
                continue
            supported_apps = [app for app, types in app_file_support.items() if file_type in types]
            if not supported_apps:
                continue
            sampled.append({"path": path, "type": file_type, "supported_apps": supported_apps})
            seen_paths.add(path)
        return sampled

    def _open_command_variants(self, app_name: str) -> List[List[str]]:
        variants: List[List[str]] = []
        for setup_variant in APP_SETUP_DICT.get(app_name, {}).get("commands", []) or []:
            for command in setup_variant:
                if isinstance(command, list) and command:
                    variants.append([str(part) for part in command])
        return variants

    def _maybe_select_inner_project_file(self, selected_file: str) -> str:
        try:
            sub_files = self.env.controller.get_file_lists(selected_file)
        except Exception as e:
            logger.warning("Error searching inner file in %s: %s", selected_file, e)
            return selected_file
        if not isinstance(sub_files, list):
            return selected_file
        for sub_file in sub_files:
            if sub_file.endswith(".blend") or sub_file.endswith(".tex"):
                return os.path.join(selected_file, sub_file)
        return selected_file

    def _build_evaluator_from_verification(self, task: Dict[str, Any]) -> Dict[str, Any]:
        verification = task.get("verification") or task.get("evaluation") or {}
        need_rule = bool(verification.get("need_rule_judge", False))
        need_vlm = bool(verification.get("need_vlm_judge", False))
        vlm_desc = verification.get("vlm_desc", "")
        rule_items = verification.get("rule_items") or []
        if not isinstance(rule_items, list):
            rule_items = []
        if rule_items:
            need_rule = True
        if not need_rule:
            raise ValueError("OSSymphony2 workflow requires at least one rule-based evaluator.")

        funcs: List[str] = []
        results: List[Dict[str, Any]] = []
        expecteds: List[Dict[str, Any]] = []
        codes: List[str] = []
        descs: List[str] = []
        for idx, item in enumerate(rule_items, start=1):
            if not isinstance(item, dict):
                continue
            code_str = str(item.get("code", ""))
            fn_name = str(item.get("function_name") or self._extract_function_name(code_str) or f"call_rule_judge_{idx}").strip()
            funcs.append(fn_name)
            results.append(self._norm_getter(item.get("result_getter")))
            expecteds.append(self._norm_getter(item.get("expected_getter"), default_empty=True))
            codes.append(code_str)
            descs.append(extract_function_docstring(code_str, fn_name))
        if not funcs:
            raise ValueError("OSSymphony2 workflow requires non-empty rule_items.")

        func_val: str | List[str] = funcs[0] if len(funcs) == 1 else funcs
        result_val: Dict[str, Any] | List[Dict[str, Any]] = results[0] if len(results) == 1 else results
        expected_val: Dict[str, Any] | List[Dict[str, Any]] = expecteds[0] if len(expecteds) == 1 else expecteds
        code_val: str | List[str] = codes[0] if len(codes) == 1 else codes
        desc_val: str | List[str] = descs[0] if len(descs) == 1 else descs
        return {
            "postconfig": POST_CONFIG,
            "func": func_val,
            "conj": "avg",
            "result": result_val,
            "expected": expected_val,
            "code": code_val,
            "desc": desc_val,
            "need_vlm_judge": need_vlm,
            "vlm_desc": vlm_desc,
            "need_rule_judge": True,
            "dynamic": True,
        }

    def _norm_getter(self, getter: Any, default_empty: bool = False) -> Dict[str, Any]:
        if not isinstance(getter, dict):
            return {"type": "empty"} if default_empty else {"type": "empty"}
        getter_type = getter.get("type")
        if getter_type == "vm_file":
            path = str(getter.get("path", ""))
            dest = str(getter.get("dest") or os.path.basename(path) or "result_file")
            return {"type": "vm_file", "path": path, "dest": dest}
        if getter_type == "vm_command_line":
            command = getter.get("command")
            if isinstance(command, list):
                command_list = [str(part) for part in command]
            elif command is None:
                command_list = []
            else:
                command_list = [str(command)]
            return {"type": "vm_command_line", "command": command_list}
        return {"type": "empty"}

    def _extract_function_name(self, code_str: str) -> str:
        try:
            tree = ast.parse(code_str)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    return node.name
        except Exception:
            return ""
        return ""


def build_desktop_env(args: argparse.Namespace) -> DesktopEnv:
    screen_size = (args.screen_width, args.screen_height)
    snapshot_name = None
    if args.provider_name == "aws" and args.region is not None:
        try:
            from desktop_env.osworld.providers.aws.manager import IMAGE_ID_MAP

            snapshot_name = IMAGE_ID_MAP[args.region].get(screen_size, IMAGE_ID_MAP[args.region][(1920, 1080)])
        except Exception as e:
            logger.error("Failed to get snapshot_name from IMAGE_ID_MAP: %s", e)
    return DesktopEnv(
        path_to_vm=args.path_to_vm,
        action_space=args.action_space,
        provider_name=args.provider_name,
        region=args.region,
        snapshot_name=snapshot_name,
        screen_size=screen_size,
        headless=args.headless,
        os_type="Ubuntu",
        require_a11y_tree=args.observation_type in ["a11y_tree", "screenshot_a11y_tree", "som"],
        enable_proxy=True,
        client_password=args.client_password,
    )


def build_engine_params(args: argparse.Namespace, model: str | None = None) -> Dict[str, Any]:
    return {
        "engine_type": args.provider,
        "model": model or args.model,
        "base_url": getattr(args, "base_url", ""),
        "api_key": getattr(args, "api_key", ""),
        "temperature": getattr(args, "temperature", None),
        "top_p": getattr(args, "top_p", None),
        "max_tokens": getattr(args, "max_tokens", None),
        "agent_name": "ossymphony2_instruction_generator",
    }


def run_task_generation(task_queue: Queue, args: argparse.Namespace, task_all_meta: Dict[str, List[str]], lock) -> None:
    env = None
    set_current_result_dir(args.rollout_task_dir)
    try:
        env = build_desktop_env(args)
        env.start()
        active_environments.append(env)
        generator = OSSymphony2TaskGenerator(
            rollout_task_dir=args.rollout_task_dir,
            env=env,
            engine_params=build_engine_params(args, args.generator_model),
            scorer_engine_params=build_engine_params(args, args.scorer_model),
            setup_wait_seconds=args.setup_wait_seconds,
            max_repair_rounds=args.max_repair_rounds,
            exploration_max_actions=args.exploration_max_actions,
        )
        while True:
            try:
                task_queue.get(timeout=5)
            except Exception:
                break
            task_file_list = generator.generate_task(
                task_nums=args.rollout_task_nums,
                app_list=args.rollout_app_list,
                max_apps_per_group=args.rollout_max_apps_per_group,
            )
            with lock:
                for app_group, new_tasks in task_file_list.items():
                    task_all_meta[app_group] = list(task_all_meta.get(app_group, [])) + list(new_tasks)
    except Exception as e:
        logger.error("Process-level error in %s: %s", current_process().name, e, exc_info=True)
    finally:
        try:
            if env:
                env.close()
        except Exception as e:
            logger.error("%s error during environment cleanup: %s", current_process().name, e)


def online_generation(args: argparse.Namespace) -> Dict[str, List[str]]:
    if not args.rollout_task_dir:
        exp_name = args.exp_name or datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
        args.rollout_task_dir = os.path.join(args.rollout_base_dir, f"ossymphony2_{exp_name}")
    os.makedirs(args.rollout_task_dir, exist_ok=True)
    logger.info("OSSymphony2 task output directory: %s", args.rollout_task_dir)
    with open(os.path.join(args.rollout_task_dir, "args.json"), "w", encoding="utf-8") as f:
        json.dump(vars(args), f, indent=4, ensure_ascii=False)

    with Manager() as manager:
        shared_task_meta = manager.dict()
        task_queue = manager.Queue()
        lock = manager.Lock()
        for _ in range(args.rollout_times):
            task_queue.put({})
        local_processes: List[Process] = []
        for idx in range(args.num_envs):
            process = Process(target=run_task_generation, args=(task_queue, args, shared_task_meta, lock), name=f"OSSymphony2TaskGen-{idx + 1}")
            process.daemon = True
            process.start()
            local_processes.append(process)
            processes.append(process)
            logger.info("Started task generation process %s with PID %s", process.name, process.pid)
        try:
            for process in local_processes:
                process.join()
        except KeyboardInterrupt:
            logger.info("Main process received KeyboardInterrupt. Initiating graceful shutdown...")
            raise
        test_all_meta = dict(shared_task_meta)

    with open(os.path.join(args.rollout_task_dir, "test_all.json"), "w", encoding="utf-8") as f:
        json.dump(test_all_meta, f, indent=4, ensure_ascii=False)
    total_tasks = sum(len(tasks) for tasks in test_all_meta.values())
    logger.info("Generated %s app groups with %s total tasks", len(test_all_meta), total_tasks)
    return test_all_meta


def signal_handler(signum, frame) -> None:
    global is_terminating
    if is_terminating:
        return
    is_terminating = True
    logger.info("Received signal %s. Gracefully shutting down...", signum)
    for env in active_environments:
        try:
            env.close()
        except Exception as e:
            logger.error("Error closing environment: %s", e)
    for process in processes:
        if process.is_alive():
            try:
                process.terminate()
            except Exception as e:
                logger.error("Error terminating process: %s", e)
    time.sleep(2)
    for process in processes:
        if process.is_alive():
            try:
                os.kill(process.pid, signal.SIGKILL)
            except Exception as e:
                logger.error("Error force killing process: %s", e)
    sys.exit(0)


def main() -> None:
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    args = config()
    setup_logging(args.log_level)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    try:
        online_generation(args)
    except KeyboardInterrupt:
        logger.info("Main process received KeyboardInterrupt.")
    except Exception as e:
        logger.error("Unexpected error in main process: %s", e, exc_info=True)
        signal_handler(signal.SIGTERM, None)
    finally:
        for env in active_environments:
            try:
                env.close()
            except Exception as e:
                logger.error("Error during final environment cleanup: %s", e)
        for process in processes:
            if process.is_alive():
                try:
                    process.terminate()
                except Exception as e:
                    logger.error("Error terminating process: %s", e)


if __name__ == "__main__":
    main()
