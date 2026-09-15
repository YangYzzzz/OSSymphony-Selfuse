from __future__ import annotations
import argparse
import datetime
import json
import logging
import os
import shutil
import sys
import signal
import time
from typing import List
from multiprocessing import Process, Manager
from multiprocessing import current_process
import lib_run_single
from desktop_env.osworld.desktop_env import DesktopEnv as OSWorldDesktopEnv
from desktop_env.waa.desktop_env import DesktopEnv as WindowsAgentArenaDesktopEnv
from desktop_env.macos.desktop_env import DesktopEnv as MacOSArenaDesktopEnv
from mm_agents.qwen3vl_agent import Qwen3VLAgent
from mm_agents.os_symphony.agents.critic_agent import CriticAgent

# Global variables for signal handling
active_environments = []
processes = []
is_terminating = False

# load the environment variables from .env file
if os.path.exists(".env"):
    from dotenv import load_dotenv
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

def config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run end-to-end evaluation on the benchmark (Qwen3VL)"
    )

    # environment config
    parser.add_argument("--path_to_vm", type=str, default=None)
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
    parser.add_argument("--sleep_after_execution", type=float, default=3.0)
    parser.add_argument("--max_steps", type=int, default=15)

    # agent config
    parser.add_argument("--max_trajectory_length", type=int, default=3)
    parser.add_argument(
        "--test_config_base_dir", type=str, default="evaluation_examples"
    )

    # lm config
    parser.add_argument("--model", type=str, default="qwen3-vl")
    parser.add_argument("--base_url", type=str, default=None)
    parser.add_argument("--api_key", type=str, default=None)
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--top_p", type=float, default=0.9)
    parser.add_argument("--max_tokens", type=int, default=32768)
    parser.add_argument("--stop_token", type=str, default=None)
    parser.add_argument(
        "--coord",
        type=str,
        choices=["absolute", "relative"],
        default="relative",
        help="Coordinate system for agent outputs (absolute or relative)",
    )
    parser.add_argument(
        "--add_thought_prefix",
        action="store_true",
        help="Add thought prefix to the response",
    )

    # example config
    parser.add_argument("--domain", type=str, default="all")
    parser.add_argument(
        "--test_all_meta_path", type=str, default="evaluation_examples/test_nogdrive.json"
    )

    # logging related
    parser.add_argument("--result_dir", type=str, default="./results")
    parser.add_argument(
        "--num_envs", type=int, default=1, help="Number of environments to run in parallel"
    )
    parser.add_argument(
        "--log_level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level",
    )

    # provider config
    parser.add_argument(
        "--region", type=str, default="us-east-1", help="AWS region for the VM"
    )
    parser.add_argument(
        "--provider_name",
        type=str,
        default="docker",
        choices=["aws", "virtualbox", "vmware", "docker", "azure", "aliyun"],
        help="Provider name",
    )
    parser.add_argument(
        "--client_password", type=str, default="", help="Client password"
    )
    parser.add_argument(
        "--screen_width", type=int, default=1920, help="Screen width"
    )
    parser.add_argument(
        "--screen_height", type=int, default=1080, help="Screen height"
    )
    parser.add_argument(
        "--benchmark", type=str, default="waa", help="name of experiment"
    )
    parser.add_argument(
        "--exp_name", type=str, default="debug-experiment", help="name of experiment"
    )


    # Critic Model
    parser.add_argument(
        "--critic_model", type=str, default="os-oracle"
    )
    parser.add_argument(
        "--critic_provider", type=str, default="openai"
    )
    parser.add_argument(
        "--critic_api_key", type=str, default=""
    )
    parser.add_argument(
        "--critic_base_url", type=str, default="https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/wzy-proxy-lk85v-151269-worker-0.wuzhenyu/7871"
    )
    parser.add_argument(
        "--critic_times", type=int, default=3
    )

    args = parser.parse_args()
    return args


args = config()  # Get command line arguments first

logger = logging.getLogger()
log_level = getattr(logging, args.log_level.upper())
logger.setLevel(log_level)

datetime_str: str = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")

os.makedirs(os.path.join("logs", args.exp_name), exist_ok=True)
file_handler = logging.FileHandler(
    os.path.join("logs", args.exp_name, "normal-{:}.log".format(datetime_str)), encoding="utf-8"
)
debug_handler = logging.FileHandler(
    os.path.join("logs", args.exp_name, "debug-{:}.log".format(datetime_str)), encoding="utf-8"
)
stdout_handler = logging.StreamHandler(sys.stdout)

file_handler.setLevel(logging.INFO)
debug_handler.setLevel(logging.DEBUG)
stdout_handler.setLevel(log_level)

formatter = logging.Formatter(
    fmt=(
        "\x1b[1;33m[%(asctime)s \x1b[31m%(levelname)s "
        "\x1b[32m%(module)s/%(lineno)d-%(processName)s\x1b[1;33m] "
        "\x1b[0m%(message)s"
    )
)
file_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)

stdout_handler.addFilter(logging.Filter("desktopenv"))

logger.addHandler(file_handler)
logger.addHandler(debug_handler)
logger.addHandler(stdout_handler)

logger = logging.getLogger("desktopenv.experiment")


def distribute_tasks(test_all_meta: dict) -> List[tuple]:
    all_tasks = []
    for domain, examples in test_all_meta.items():
        for example_id in examples:
            all_tasks.append((domain, example_id))
    return all_tasks


def run_env_tasks(
        task_queue, 
        args: argparse.Namespace, 
        shared_scores: list,
        worker_id
        ):
    active_environments = []
    env = None
    try:
        REGION = args.region
        screen_size = (args.screen_width, args.screen_height)
        snapshot_name = "init_state"
        
        if args.benchmark in {"osworld", "weave_bench"}:
            env = OSWorldDesktopEnv(
                path_to_vm=args.path_to_vm,
                action_space=args.action_space,
                provider_name=args.provider_name,
                region=REGION,
                snapshot_name=snapshot_name,
                screen_size=screen_size,
                headless=args.headless,
                os_type="Ubuntu",
                require_a11y_tree=args.observation_type in [
                    "a11y_tree",
                    "screenshot_a11y_tree",
                    "som",
                ],
                enable_proxy=True,
                client_password=args.client_password,
            )
            
            env.start()

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

        active_environments.append(env)

        critic_params = {
            "engine_type": args.critic_provider,
            "api_key": args.critic_api_key,
            "model": args.critic_model,
            "base_url": args.critic_base_url
        }

        if args.critic_times == 1:
            critic_agent = None
        else:
            critic_agent = CriticAgent(
                engine_params=critic_params
            )

        agent = Qwen3VLAgent(
            model=args.model,
            base_url=args.base_url,
            api_key=args.api_key,
            max_tokens=args.max_tokens,
            top_p=args.top_p,
            temperature=args.temperature,
            history_n=args.max_trajectory_length,
            action_space=args.action_space,
            coordinate_type=args.coord,
            add_thought_prefix=args.add_thought_prefix,
            critic_agent=critic_agent, # type: ignore
            critic_times=args.critic_times
        )
        
        logger.info(f"Process {current_process().name} started.")
        while True:
            try:
                item = task_queue.get(timeout=5)
            except Exception:
                break
            domain, example_id = item
            try:
                config_file = os.path.join(
                    args.test_config_base_dir, f"{domain}/{example_id}.json"
                )
                with open(config_file, "r", encoding="utf-8") as f:
                    example = json.load(f)
                logger.info(f"[{current_process().name}][Domain]: {domain}")
                logger.info(f"[{current_process().name}][Example ID]: {example_id}")
                logger.info(f"[{current_process().name}][Instruction]: {example['instruction']}")
                example_result_dir = os.path.join(
                    args.result_dir,
                    domain,
                    example_id,
                )
                os.makedirs(example_result_dir, exist_ok=True)
                try:
                    lib_run_single.run_single_example_qwen3vl(
                        agent,
                        env,
                        example,
                        args.max_steps,
                        example["instruction"],
                        args,
                        example_result_dir,
                        shared_scores,
                    )
                except Exception as e:
                    import traceback
                    logger.error(f"Exception in {current_process().name} {domain}/{example_id}: {e}")
                    logger.error(traceback.format_exc())
                    with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                        f.write(json.dumps({"Error": f"{domain}/{example_id} - {e}"}))
                        f.write("\n")

                    # 处理非连接重置错误的情况
                    is_connection_reset = isinstance(e, ConnectionResetError)
                    if not is_connection_reset or "ConnectionResetError" not in str(e):
                        result_file_path = os.path.join(example_result_dir, "result.txt")
                        # with open(result_file_path, "w", encoding="utf-8") as f:
                        #     f.write("0.0\n")

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
        except Exception as e:
            logger.error(f"{current_process().name} error during environment cleanup: {e}")


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


def test(args: argparse.Namespace, test_all_meta: dict) -> None:
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
                name=f"EnvProcess-{worker_id+1}"
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
                            name=f"EnvProcess-Restart-{idx+1}"
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


def get_unfinished(
    target_dir, total_file_json, turn: int, incremental_test: bool
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
                        with open(os.path.join(example_path, "result.txt"), "r", encoding="utf-8") as f:
                            score = f.read().strip()
                            if score == "False":
                                score = 0.0
                            elif score == "True":
                                score = 1.0
                            else:
                                score = float(score)
                        
                        if not incremental_test:
                            # TODO: 特化一下后面需要修正!!!
                            if score == 0 and turn != 1:
                                # empty all files under example_id
                                shutil.rmtree(path=example_path, ignore_errors=True)
                            else:
                                finished[domain].append(example_id)
                        else:
                            # 增量测试
                            with open(os.path.join(example_path, "traj.jsonl"), "r", encoding="utf-8") as f:
                                lines = f.readlines()
                                non_empty_lines = [line for line in lines if line.strip() != '']
                                cur_step = json.loads(non_empty_lines[-1].strip())["step_num"]
                            # 当前写死了, 最小步数为50步
                            if cur_step == 50 and score == 0:
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

    # 记录总共任务列表
    all_result = []

    for domain, example_id_list in total_file_json.items():
        for example_id in example_id_list:
            example_path = os.path.join(target_dir, domain, example_id)
            if os.path.isdir(example_path):
                if "result.txt" in os.listdir(example_path):
                    # empty all files under example_id
                    try:
                        all_result.append(
                            float(
                                open(
                                    os.path.join(example_path, "result.txt"), "r"
                                ).read()
                            )
                        )
                    except:
                        all_result.append(0.0)
                else:
                    all_result.append(0.0)
            # 确保统计的任务数量总和为 total_file_json 里的任务之和
            else:
                all_result.append(0.0)

    if not all_result:
        print("New experiment, no result yet.")
        return None
    else:
        print("Current Success Rate:", sum(all_result) / len(all_result) * 100, "%")
        return all_result


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    ####### The complete version of the list of examples #######
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    args = config()

    # save args to json in result_dir/action_space/observation_type/model/args.json
    if args.exp_name != "":
        args.result_dir = os.path.join(
            args.result_dir,
            args.exp_name
        )
    else:
        args.result_dir = os.path.join(
            args.result_dir,
            args.action_space,
            args.observation_type,
            args.model
        )

    path_to_args = os.path.join(
        args.result_dir,
        "args.json"
    )
    os.makedirs(os.path.dirname(path_to_args), exist_ok=True)
    with open(path_to_args, "w", encoding="utf-8") as f:
        json.dump(vars(args), f, indent=4)

    with open(args.test_all_meta_path, "r", encoding="utf-8") as f:
        test_all_meta = json.load(f)

    if args.domain != "all":
        test_all_meta = {args.domain: test_all_meta[args.domain]}

    test_file_list = get_unfinished(
        target_dir=args.result_dir,
        total_file_json=test_all_meta,
        turn=1,
        incremental_test=False
    )
    left_info = ""
    for domain in test_file_list:
        left_info += f"{domain}: {len(test_file_list[domain])}\n"
    logger.info(f"Left tasks:\n{left_info}")
    # 获得迄今为止的准确率
    get_result(
        target_dir=args.result_dir,
        total_file_json=test_all_meta
    )
    test(
        args, 
        test_file_list
    )

    
