import argparse
import copy
import datetime
import json
import logging
import os
import shutil
import signal
import subprocess
import sys
import time
from multiprocessing import Manager, Process, Queue, current_process

import lib_run_single
from mm_agents.os_symphony2.os_symphony2_agent import OSSymphony2Agent
from desktop_env.osworld.desktop_env import DesktopEnv as OSWorldDesktopEnv
from desktop_env.waa.desktop_env import DesktopEnv as WindowsAgentArenaDesktopEnv
from desktop_env.macos.desktop_env import DesktopEnv as MacOSArenaDesktopEnv
from dotenv import load_dotenv
from mm_agents.os_symphony2.os_symphony2_agent_with_toolcall import OSSymphony2AgentWithToolCall

load_dotenv()

def prepare_worker_vm_paths(base_golden_path: str, worker_idx: int):
    """
    根据 golden 路径和 worker id 准备存储路径。
    例如: /nvme/.../waa/golden -> /nvme/.../waa/storage_0, /nvme/.../waa/storage_0_backup
    """
    # 去除末尾斜杠以确保 dirname 计算正确
    base_golden_path = base_golden_path.rstrip(os.sep)
    
    # 获取父目录 (例如 /nvme/yangbowen/vm_stroage/waa)
    parent_dir = os.path.dirname(base_golden_path)
    
    # 定义该 worker 的路径
    worker_storage_path = os.path.join(parent_dir, f"storage_{worker_idx}")
    worker_backup_path = os.path.join(parent_dir, f"storage_{worker_idx}_backup")
    
    return worker_storage_path, worker_backup_path


def initialize_worker_files(golden_path: str, worker_backup_path: str, worker_storage_path: str):
    """
    初始化 worker 的文件。如果 backup 不存在，从 golden 复制。
    """
    if not os.path.exists(golden_path):
        raise FileNotFoundError(f"Golden VM path not found: {golden_path}")

    # 1. 准备 Backup 目录
    if not os.path.exists(worker_backup_path):
        logger.info(f"Initializing backup for worker from {golden_path} to {worker_backup_path} ...")
        try:
            # 确保目标父目录存在
            os.makedirs(os.path.dirname(worker_backup_path), exist_ok=True)

            if os.path.isdir(golden_path):
                # 如果是目录，使用 cp -r --sparse=always
                # 注意：这里假设 worker_backup_path 是目标目录名，而不是父目录
                subprocess.check_call(['cp', '-r', '--sparse=always', golden_path, worker_backup_path])
            else:
                # 如果是单文件 (如 qcow2)，使用 cp --sparse=always 保持稀疏性
                subprocess.check_call(['cp', '--sparse=always', golden_path, worker_backup_path])
                
            logger.info(f"Backup initialization complete for {worker_backup_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to copy golden image to backup using cp: {e}")
            raise e
    else:
        logger.info(f"Worker backup already exists at {worker_backup_path}, skipping copy.")

    # 2. 准备 Storage 目录
    if not os.path.exists(worker_storage_path):
        os.makedirs(worker_storage_path, exist_ok=True)

#  Logger Configs {{{ #
# 不带任何参数的是Logger的祖先
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

datetime_str: str = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
formatter = logging.Formatter(
    fmt="\x1b[1;33m[%(asctime)s \x1b[31m%(levelname)s \x1b[32m%(module)s/%(lineno)d-%(processName)s\x1b[1;33m] \x1b[0m%(message)s"
)

# Set up Stdout handler
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)
# 过滤器，只有 desktopenv 及其子logger才会输出到控制台上
stdout_handler.addFilter(logging.Filter("desktopenv"))
logger.addHandler(stdout_handler)

# Logger Configs
# 在当前文件里使用的logger，logger内以.来分级结构，产生一条信息时，会一直向上冒泡到根logger
logger = logging.getLogger("desktopenv.experiment")

# Global variables for signal handling
active_environments = []
processes = []
is_terminating = False

def distribute_tasks(test_all_meta: dict) -> list:
    all_tasks = []
    for domain, examples in test_all_meta.items():
        for example_id in examples:
            all_tasks.append((domain, example_id))
    return all_tasks


def process_signal_handler(signum, frame, env_idx):
    logger.info(f"Process {env_idx + 1} received signal {signum}. Shutting down...")
    local_vars = frame.f_locals
    active_environments = local_vars.get("active_environments", [])
    for env in active_environments:
        if env is not None:
            try:
                logger.info(f"Process {env_idx + 1} closing environment...")
                env.close()
                logger.info(f"Process {env_idx + 1} environment closed successfully")
            except Exception as e:
                logger.error(f"Process {env_idx + 1} error closing environment: {e}")
    logger.info(f"Process {env_idx + 1} shutdown complete. Exiting.")
    sys.exit(0)


def run_env_tasks(
    task_queue: Queue,
    args: argparse.Namespace,
    shared_scores: list,
    worker_id: int,
):
    global active_environments
    env = None
    search_env = None
    try:
        # Use IMAGE_ID_MAP for AWS provider to get snapshot_name
        snapshot_name = None
        region = getattr(args, "region", None)

        if args.benchmark == "osworld":
            env = OSWorldDesktopEnv(
                path_to_vm=args.path_to_vm,
                action_space=args.action_space,
                provider_name=args.provider_name,
                region=region,
                snapshot_name=snapshot_name,
                cache_dir=f"cache/{args.exp_name}",
                screen_size=(args.screen_width, args.screen_height),
                headless=args.headless,
                os_type="Ubuntu",
                require_a11y_tree=args.observation_type
                in ["a11y_tree", "screenshot_a11y_tree", "som"],
                enable_proxy=True,
                client_password=getattr(args, "client_password", ""),
            )
            env.start()
            
            platform = "linux"

        elif args.benchmark == "waa":
            parent_dir = os.path.dirname(args.path_to_vm.rstrip(os.sep))
            path_to_vm = os.path.join(parent_dir, f"storage_{worker_id}")
            path_to_vm_backup = os.path.join(parent_dir, f"storage_{worker_id}_backup")
            
            logger.info(f"[{current_process().name}] Worker ID: {worker_id}")
            logger.info(f"[{current_process().name}] Derived VM Storage: {path_to_vm}")
            logger.info(f"[{current_process().name}] Derived VM Backup: {path_to_vm_backup}")
            env = WindowsAgentArenaDesktopEnv(
                path_to_vm=path_to_vm,
                path_to_vm_backup=path_to_vm_backup,
                action_space=args.action_space,
                screen_size=(args.screen_width, args.screen_height),
                headless=args.headless,
                require_a11y_tree=args.observation_type
                                in ["a11y_tree", "screenshot_a11y_tree", "som"],
                provider_name=args.provider_name
            )

            platform = "windows"

        elif args.benchmark == "macosarena":
            path_to_vm = args.path_to_vm.split(" ")[0]
            path_to_base_vm = args.path_to_vm.split(" ")[1]
            # 默认 1920 x 1080，目前不支持修改分辨率
            env = MacOSArenaDesktopEnv(
                path_to_vm=path_to_vm,
                path_to_base_vm=path_to_base_vm,
                action_space=args.action_space,
                provider_name=args.provider_name
            )
            platform = "macos"

        if args.use_tool_call:
            agent = OSSymphony2AgentWithToolCall(
                model=args.model,
                base_url=args.base_url,
                api_key=args.api_key,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                max_trajectory_length=args.max_trajectory_length,
                keep_first_image=args.keep_first_image,
                keep_cot=not args.remove_cot,
                keep_all_text=args.keep_all_text,
                use_thinking=args.use_thinking
            )
        else:
            agent = OSSymphony2Agent(
                model=args.model,
                base_url=args.base_url,
                api_key=args.api_key,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                history_n=args.max_trajectory_length,
                keep_first_image=args.keep_first_image,
                use_thinking=args.use_thinking
            )

        active_environments.append(env)
        active_environments.append(search_env)
        logger.info(f"Process {current_process().name} started.")
        while True:
            try:
                item = task_queue.get(timeout=5)
            except Exception:
                break
            domain, example_id = item
            try:
                config_file = os.path.join(
                    args.test_config_base_dir, f"{args.benchmark}/examples/{domain}/{example_id}.json"
                )
                with open(config_file, "r", encoding="utf-8") as f:
                    example = json.load(f)

                if args.enable_rewrite_instruction and "rewritten_instruction" in example:
                    instruction = example["rewritten_instruction"]
                else:
                    instruction = example["instruction"]
                
                example_result_dir = os.path.join(
                    args.result_dir,
                    domain,
                    example_id
                )
                os.makedirs(example_result_dir, exist_ok=True)
                logger.info(f"[{current_process().name}][Domain]: {domain}")
                logger.info(f"[{current_process().name}][Example ID]: {example_id}")
                logger.info(f"[{current_process().name}][Instruction]: {instruction}")
                try:
                    lib_run_single.run_single_example_ossymphony2(
                        agent,
                        env,
                        example,
                        args.max_steps,
                        instruction,
                        args,
                        example_result_dir,
                        shared_scores,
                    )
                except Exception as e:
                    import traceback

                    logger.error(
                        f"Exception in {current_process().name} {domain}/{example_id}: {e}"
                    )
                    logger.error(traceback.format_exc())

                    with open(os.path.join(os.path.dirname(example_result_dir), "error.jsonl"), "a") as f:
                        f.write(json.dumps({"Error": f"{domain}/{example_id} - {e}"}))
                        f.write("\n")

            except Exception as e:
                logger.error(f"Task-level error in {current_process().name}: {e}")
                import traceback

                logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(f"Process-level error in {current_process().name}: {e}")
        import traceback

        logger.error(traceback.format_exc())
    finally:
        logger.info(f"{current_process().name} cleaning up environment...")
        try:
            if env:
                env.close()
                logger.info(f"{current_process().name} environment closed successfully")
            if search_env:
                search_env.close()
                logger.info(f"{current_process().name} searcher environment closed successfully")
        except Exception as e:
            logger.error(
                f"{current_process().name} error during environment cleanup: {e}"
            )

# 退出函数
def signal_handler(signum, frame):
    global is_terminating, active_environments, processes
    if is_terminating:
        return
    is_terminating = True
    logger.info(f"Received signal {signum}. Gracefully shutting down...")
    for env in active_environments:
        try:
            logger.info(f"Closing environment...")
            env.close()
            logger.info(f"Environment closed successfully")
        except Exception as e:
            logger.error(f"Error closing environment: {e}")
    for p in processes:
        if p.is_alive():
            try:
                logger.info(f"Sending termination signal to process {p.name}...")
                p.terminate()
            except Exception as e:
                logger.error(f"Error sending termination signal to process: {e}")
    time.sleep(1)
    for p in processes:
        if p.is_alive():
            try:
                logger.info(f"Forcefully terminating process {p.name}...")
                import signal as sig

                os.kill(p.pid, sig.SIGKILL)
            except Exception as e:
                logger.error(f"Error forcefully terminating process: {e}")
    logger.info("Shutdown complete. Exiting.")
    sys.exit(0)


def config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run end-to-end evaluation on the benchmark"
    )

    # environment config
    parser.add_argument("--path_to_vm", type=str, default=None)
    parser.add_argument(
        "--provider_name",
        type=str,
        default="vmware",
        help="Virtualization provider (vmware, docker, aws, azure, gcp, virtualbox)",
    )
    parser.add_argument(
        "--headless", action="store_true", help="Run in headless machine"
    )
    parser.add_argument(
        "--action_space", type=str, default="pyautogui", help="Action type"
    )
    parser.add_argument(
        "--observation_type",
        choices=["screenshot", "a11y_tree", "screenshot_a11y_tree", "som"],
        default="screenshot",
        help="Observation type",
    )
    parser.add_argument(
        "--num_envs",
        type=int,
        default=1,
        help="Number of environments to run in parallel",
    )
    parser.add_argument(
        "--sleep_after_execution",
        type=int,
        default=3,
        help="Seconds after each step execution",
    )
    parser.add_argument("--screen_width", type=int, default=1920, help="Main environment's width")
    parser.add_argument("--screen_height", type=int, default=1080, help="Main environment's height")
    parser.add_argument("--max_steps", type=int, default=15)

    parser.add_argument("--benchmark", type=str, default="osworld", help="osworld / waa / macos")

    parser.add_argument("--domain", type=str, default="all")
    parser.add_argument(
        "--test_all_meta_path", type=str, default="evaluation_examples/osworld/test_all.json"
    )
    parser.add_argument(
        "--test_config_base_dir", type=str, default="evaluation_examples"
    )
    parser.add_argument("--result_dir", type=str, default="./results")
    parser.add_argument(
        "--avg",
        type=int,
        default=1,
        help="Number of repeated evaluation runs for aggregate statistics",
    )

    parser.add_argument(
        "--region", type=str, default="us-east-1", help="AWS region for the VM"
    )
    parser.add_argument(
        "--client_password", type=str, default="password", help="Client password"
    )

    parser.add_argument("--max_trajectory_length", type=int, default=8, help="最大图片数量")
    parser.add_argument("--enable_rewrite_instruction", action="store_true", default=False)

    # generator model config
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument(
        "--base_url",
        type=str,
        default="",
        help="The URL of the model API.",
    )
    parser.add_argument(
        "--api_key",
        type=str,
        default="",
        help="The API key of the model.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Temperature to fix the orchestrator model at (e.g. o3 can only be run with 1.0)",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=None,
        help="max tokens",
    )
    parser.add_argument("--use_thinking", action="store_true", default=False)
    parser.add_argument("--keep_first_image", action="store_true", default=False, help="Whether keep the first image(first state) in the orchestrator agent")
    parser.add_argument("--keep_all_text", action="store_true", default=False, help="Whether keep the all text content in the orchestrator agent")
    parser.add_argument("--remove_cot", action="store_true", default=False, help="是否在历史信息内清除历史cot")
    parser.add_argument("--use_tool_call", action="store_true", default=False, help="是否使用vllm自带的tool call来调用llm, 默认关闭（qwen3vl官方的parse response逻辑）")

    # 实验名
    parser.add_argument(
        "--exp_name",
        type=str,
        default="",
        help="Experiment Name",
    )
    args = parser.parse_args()

    return args


def test(args: argparse.Namespace, test_all_meta: dict) -> list[float]:
    global processes
    logger.info("Args: %s", args)
    all_tasks = distribute_tasks(test_all_meta)
    logger.info(f"Total tasks: {len(all_tasks)}")

    num_envs = args.num_envs
    if args.benchmark == "waa":
        logger.info(f"[WindowsAgentArena] Initializing storage for {num_envs} workers from golden image: {args.path_to_vm}")
        for i in range(num_envs):
            s_path, b_path = prepare_worker_vm_paths(args.path_to_vm, i)
            initialize_worker_files(args.path_to_vm, b_path, s_path)

    with Manager() as manager:
        shared_scores = manager.list()
        task_queue = manager.Queue()
        for item in all_tasks:
            task_queue.put(item)
        processes = []
        for worker_id in range(num_envs):
            p = Process(
                target=run_env_tasks,
                args=(task_queue, args, shared_scores, worker_id),
                name=f"EnvProcess-{worker_id+1}",
            )
            p.daemon = True
            p.start()
            processes.append(p)
            logger.info(f"Started process {p.name} with PID {p.pid}")
        try:
            while True:
                alive_count = 0
                for idx, p in enumerate(processes):
                    if not p.is_alive():
                        logger.warning(f"Process {p.name} died, restarting...")
                        new_p = Process(
                            target=run_env_tasks,
                            args=(task_queue, args, shared_scores, idx),
                            name=f"EnvProcess-Restart-{idx+1}",
                        )
                        new_p.daemon = True
                        new_p.start()
                        processes[idx] = new_p
                        logger.info(f"Restarted process {new_p.name} with PID {new_p.pid}")
                    else:
                        alive_count += 1
                if task_queue.empty():
                    logger.info("All tasks finished.")
                    break
                if alive_count == 0:
                    logger.error("All processes died, exiting.")
                    break
                time.sleep(5)
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            logger.info("Main process received KeyboardInterrupt. Initiating graceful shutdown...")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while waiting for processes: {e}", exc_info=True)
            for p in processes:
                if p.is_alive():
                    try:
                        logger.info(f"Terminating process {p.name} due to error...")
                        p.terminate()
                    except Exception as term_e:
                        logger.error(f"Error terminating process {p.name}: {term_e}")
            raise
        scores = list(shared_scores)
    logger.info(f"Average score: {sum(scores) / len(scores) if scores else 0}")
    return scores

# 把做错的目前也都视为未完成的
def get_unfinished(
    target_dir, total_file_json
):

    if not os.path.exists(target_dir):
        return total_file_json

    finished = {}
    for domain in os.listdir(target_dir):
        finished[domain] = []
        domain_path = os.path.join(target_dir, domain)
        if os.path.isdir(domain_path):
            for example_id in os.listdir(domain_path):
                if example_id == "onboard":
                    continue
                example_path = os.path.join(domain_path, example_id)
                if os.path.isdir(example_path):
                    if "result.txt" not in os.listdir(example_path):
                        # empty all files under example_id
                        shutil.rmtree(path=example_path, ignore_errors=True)
                    else:
                        finished[domain].append(example_id)

    if not finished:
        return total_file_json

    for domain, examples in finished.items():
        if domain in total_file_json:
            total_file_json[domain] = [
                x for x in total_file_json[domain] if x not in examples
            ]

    return total_file_json


def get_result(target_dir, total_file_json: dict):
    if not os.path.exists(target_dir):
        print("New experiment, no result yet.")
        return None

    all_result = []
    per_task_result = {}

    for domain, example_id_list in total_file_json.items():
        for example_id in example_id_list:
            example_path = os.path.join(target_dir, domain, example_id)
            score = 0.0
            if os.path.isdir(example_path) and "result.txt" in os.listdir(example_path):
                try:
                    with open(os.path.join(example_path, "result.txt"), "r", encoding="utf-8") as f:
                        score = float(f.read())
                except Exception:
                    score = 0.0
            all_result.append(score)
            per_task_result[(domain, example_id)] = score

    if not all_result:
        print("New experiment, no result yet.")
        return None

    success_rate = sum(all_result) / len(all_result)
    print("Current Success Rate:", success_rate * 100, "%")
    return {
        "scores": all_result,
        "per_task": per_task_result,
        "success_rate": success_rate,
    }


def build_base_result_dir(args: argparse.Namespace) -> str:
    if args.exp_name:
        return os.path.join(args.result_dir, args.exp_name)
    return os.path.join(args.result_dir, args.action_space, args.observation_type, args.model)


def clone_args_with_result_dir(args: argparse.Namespace, result_dir: str, exp_name: str) -> argparse.Namespace:
    run_args = argparse.Namespace(**vars(args))
    run_args.result_dir = result_dir
    run_args.exp_name = exp_name
    return run_args


def summarize_runs(run_summaries: list[dict], total_file_json: dict) -> dict:
    run_rates = [summary["success_rate"] for summary in run_summaries]
    pass_at_k_total = 0.0
    task_count = 0
    for domain, example_ids in total_file_json.items():
        for example_id in example_ids:
            task_count += 1
            best_score = max(
                summary["per_task"].get((domain, example_id), 0.0)
                for summary in run_summaries
            )
            pass_at_k_total += best_score

    avg_success_rate = sum(run_rates) / len(run_rates) if run_rates else 0.0
    variance = 0.0
    if run_rates:
        variance = sum((rate - avg_success_rate) ** 2 for rate in run_rates) / len(run_rates)
    std = variance ** 0.5
    pass_at_k = pass_at_k_total / task_count if task_count else 0.0

    best_run = None
    worst_run = None
    if run_summaries:
        best_summary = max(run_summaries, key=lambda summary: summary["success_rate"])
        worst_summary = min(run_summaries, key=lambda summary: summary["success_rate"])
        best_run = {
            "eval_time": best_summary["eval_time"],
            "success_rate": best_summary["success_rate"],
            "success_count": sum(best_summary["scores"]),
            "result_dir": best_summary["result_dir"],
        }
        worst_run = {
            "eval_time": worst_summary["eval_time"],
            "success_rate": worst_summary["success_rate"],
            "success_count": sum(worst_summary["scores"]),
            "result_dir": worst_summary["result_dir"],
        }

    return {
        "run_success_rates": run_rates,
        "avg_success_rate": avg_success_rate,
        "variance": variance,
        "std": std,
        "pass_at_k": pass_at_k,
        "task_count": task_count,
        "k": len(run_summaries),
        "best_run": best_run,
        "worst_run": worst_run,
    }


def write_summary_report(base_result_dir: str, report: dict) -> str:
    report_path = os.path.join(base_result_dir, "avg_summary.json")
    os.makedirs(base_result_dir, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    return report_path


def format_percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


def print_summary_table(report: dict) -> None:
    run_headers = ["run", "success_rate", "success/total", "result_dir"]
    run_rows = [
        [
            str(run["eval_time"]),
            format_percentage(run["success_rate"]),
            f"{run['success_count']:.2f}/{report['task_count']}",
            run["result_dir"],
        ]
        for run in report["runs"]
    ]

    metric_headers = ["metric", "value"]
    metric_rows = [
        ["task_count", str(report["task_count"])],
        ["avg_success_rate", format_percentage(report["avg_success_rate"])],
        ["variance", f"{report['variance']:.6f}"],
        ["std", f"{report['std']:.6f}"],
        [f"pass@{report['k']}", format_percentage(report["pass_at_k"])],
    ]

    best_worst_headers = ["summary", "run", "success_rate", "success/total", "result_dir"]
    best_worst_rows = []
    if report["best_run"] is not None:
        best_worst_rows.append(
            [
                "best_run",
                str(report["best_run"]["eval_time"]),
                format_percentage(report["best_run"]["success_rate"]),
                f"{report['best_run']['success_count']:.2f}/{report['task_count']}",
                report["best_run"]["result_dir"],
            ]
        )
    if report["worst_run"] is not None:
        best_worst_rows.append(
            [
                "worst_run",
                str(report["worst_run"]["eval_time"]),
                format_percentage(report["worst_run"]["success_rate"]),
                f"{report['worst_run']['success_count']:.2f}/{report['task_count']}",
                report["worst_run"]["result_dir"],
            ]
        )

    def print_table(title: str, headers: list[str], rows: list[list[str]]) -> None:
        widths = [len(header) for header in headers]
        for row in rows:
            for idx, cell in enumerate(row):
                widths[idx] = max(widths[idx], len(cell))

        border = "+-" + "-+-".join("-" * width for width in widths) + "-+"

        print(f"\n{title}")
        print(border)
        print("| " + " | ".join(header.ljust(widths[idx]) for idx, header in enumerate(headers)) + " |")
        print(border)
        for row in rows:
            print("| " + " | ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(row)) + " |")
        print(border)

    print_table("Run Summary", run_headers, run_rows)
    print_table("Aggregate Metrics", metric_headers, metric_rows)
    if best_worst_rows:
        print_table("Best / Worst Runs", best_worst_headers, best_worst_rows)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    args = config()

    base_result_dir = build_base_result_dir(args)

    with open(args.test_all_meta_path, "r", encoding="utf-8") as f:
        test_all_meta = json.load(f)

    if args.domain != "all":
        test_all_meta = {args.domain: test_all_meta[args.domain]}

    run_summaries = []
    for eval_time in range(args.avg):
        result_dir = base_result_dir if args.avg == 1 else f"{base_result_dir}_{eval_time}"
        exp_name = args.exp_name if args.avg == 1 else f"{args.exp_name}_{eval_time}" if args.exp_name else ""
        run_args = clone_args_with_result_dir(args, result_dir, exp_name)

        path_to_args = os.path.join(run_args.result_dir, "args.json")
        os.makedirs(os.path.dirname(path_to_args), exist_ok=True)
        with open(path_to_args, "w", encoding="utf-8") as f:
            json.dump(vars(run_args), f, indent=4)

        test_file_list = get_unfinished(target_dir=run_args.result_dir, total_file_json=copy.deepcopy(test_all_meta))
        left_info = ""
        for domain in test_file_list:
            left_info += f"{domain}: {len(test_file_list[domain])}\n"
        logger.info(f"Run {eval_time + 1}/{args.avg} left tasks:\n{left_info}")

        existing_result = get_result(target_dir=run_args.result_dir, total_file_json=test_all_meta)
        if all(not examples for examples in test_file_list.values()):
            logger.info(f"Run {eval_time + 1}/{args.avg} already finished, reusing existing results.")
            run_summary = existing_result
        else:
            test(run_args, test_file_list)
            run_summary = get_result(target_dir=run_args.result_dir, total_file_json=test_all_meta)

        if run_summary is None:
            run_summary = {
                "scores": [],
                "per_task": {},
                "success_rate": 0.0,
            }
        run_summary["eval_time"] = eval_time
        run_summary["result_dir"] = run_args.result_dir
        run_summaries.append(run_summary)

    report = summarize_runs(run_summaries, test_all_meta)
    report["runs"] = [
        {
            "eval_time": summary["eval_time"],
            "result_dir": summary["result_dir"],
            "success_rate": summary["success_rate"],
            "success_count": sum(summary["scores"]),
        }
        for summary in run_summaries
    ]
    report_path = write_summary_report(base_result_dir, report)
    print_summary_table(report)

    logger.info("Per-run success rates: %s", [round(rate * 100, 2) for rate in report["run_success_rates"]])
    logger.info("Average success rate: %.2f%%", report["avg_success_rate"] * 100)
    logger.info("Success rate variance: %.6f", report["variance"])
    logger.info("pass@%s success rate: %.2f%%", report["k"], report["pass_at_k"] * 100)
    logger.info("Summary report saved to %s", report_path)
    logger.info(f"====================\nExperiment {args.exp_name} is totally ended!\n====================")
