"""
    这个文件的目的旨在 Scale Ubuntu Desktop, 整体功能其实和测评 OSWorld 没啥区别
    去除 env.evaluate 功能, 转而增加 agent.evaluate() 实现 LLM-AS-A-Judge
    不使用太复杂的框架了, 使用传统Agent即可
"""

from __future__ import annotations
import argparse
import datetime
import json
import logging
import os
from queue import Queue
import shutil
import sys
import signal
import time
from typing import List, Dict
from multiprocessing import Process, Manager
from multiprocessing import current_process
import lib_run_single
from desktop_env.osworld.desktop_env import DesktopEnv
from mm_agents.uitars15_v2 import UITarsAgent
import os
from os_caliber_task_generator import OSCaliberTaskGenerator
from mm_agents.qwen3vl_agent import Qwen3VLAgent
from mm_agents.os_symphony.agents.coarse_instruction_generation_agent import CoarseInstructionGenerationAgent
from mm_agents.anthropic.main import AnthropicAgent
from mm_agents.kimi.kimi_agent import KimiAgent
from mm_agents.glm4v.glm4v_agent import GLM4VAgent
from mm_agents.seed_agent import SeedAgent

# Global variables for signal handling
active_environments = []
processes = []
is_terminating = False

# load the environment variables from .env file
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

#  Logger Configs {{{ #
def config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run end-to-end evaluation on the benchmark"
    )

    # environment config
    parser.add_argument("--path_to_vm", type=str, default="/nvme/yangbowen/osworld/docker_vm_data/Ubuntu_write.qcow2")
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
    
    # evaluation config
    parser.add_argument(
        "--test_config_base_dir", type=str, default="evaluation_examples"
    )

    # lm config
    parser.add_argument("--model", type=str, default="ui-tars-1.5-7b")
    parser.add_argument("--api_key", type=str, default="")
    parser.add_argument("--base_url", type=str, default="https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10001/v1")
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--top_p", type=float, default=0.9)
    parser.add_argument("--max_tokens", type=int, default=32768)
    parser.add_argument("--use_thinking", action="store_true", default=False)
    parser.add_argument("--max_trajectory_length", type=int, default=None, help="The max number of trajectory steps.") # 一般没用, 目前强模型通常选择保留全部文本
    parser.add_argument("--max_image_history_length", type=int, default=5, help="The max number of images in the history.")
    parser.add_argument("--language", type=str, default="Chinese", help="Language for the agent.")

    # logging related
    parser.add_argument("--result_dir", type=str, default="./oscaliber_results")
    parser.add_argument("--num_envs", type=int, default=1, help="Number of environments to run in parallel")  
    parser.add_argument("--log_level", type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                       default='INFO', help="Set the logging level")
    # aws config
    parser.add_argument(
        "--region", type=str, default="us-east-1", help="AWS region for the VM"
    )
    parser.add_argument(
        "--provider_name", type=str, default="aws", choices=["aws", "virtualbox", "vmware", "docker", "azure"], help="Provider name"
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
        "--exp_name", type=str, default="", help="Experiment name"
    )

    # rollout config
    parser.add_argument("--rollout_mode", type=str, default="online rollout / offline rollout") # online: 一边roll指令一边采集轨迹, offline: 类似OSWorld测评, 起始给定任务文件, 再采集轨迹
    parser.add_argument(
        "--rollout_test_all_meta_path", type=str, default="evaluation_examples/osworld/test_all.json" # 当 mode 为 offline 时生效
    )
    parser.add_argument(
        "--rollout_base_dir", type=str, default="evaluation_examples/ubuntu_online_rollout" # 保存的任务文件基目录, 当 mode 为 online 时生效
    )
    parser.add_argument(
        "--rollout_times", type=int, default=10, help="Rollout times" # 也就是随机选择多少次app, 当 mode 为 online 时生效
    )
    parser.add_argument(
        "--rollout_task_nums", type=int, default=10, help="Task numbers per rollout" # 每次roll多少个任务, 当 mode 为 online 时生效
    )
    parser.add_argument(
        "--rollout_app_list", type=str, default="all", help="Rollout application list, default all" # roll的应用列表, 当 mode 为 online 时生效
    )

    # instrction generation model config ig: instrction generation model
    parser.add_argument("--ig_provider", type=str, default="openai")
    parser.add_argument("--ig_model", type=str, default="gpt-5")
    parser.add_argument("--ig_base_url", type=str, default="https://api.boyuerichdata.opensphereai.com/v1")
    parser.add_argument("--ig_api_key", type=str, default="")
    parser.add_argument("--ig_temperature", type=float, default=0.5)
    parser.add_argument("--ig_max_tokens", type=int, default=32768)

    # mode
    parser.add_argument("--enable_self_judge", action="store_true", default=False) # 是否采用 self-judge, TODO: @Yang

    args = parser.parse_args()
    return args

args = config()  # Get command line arguments first

logger = logging.getLogger()
log_level = getattr(logging, args.log_level.upper())
logger.setLevel(log_level)

datetime_str: str = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")

file_handler = logging.FileHandler(
    os.path.join("logs", "normal-{:}.log".format(datetime_str)), encoding="utf-8"
)
debug_handler = logging.FileHandler(
    os.path.join("logs", "debug-{:}.log".format(datetime_str)), encoding="utf-8"
)
stdout_handler = logging.StreamHandler(sys.stdout)

file_handler.setLevel(logging.INFO)
debug_handler.setLevel(logging.DEBUG)
stdout_handler.setLevel(log_level)

formatter = logging.Formatter(
    fmt="\x1b[1;33m[%(asctime)s \x1b[31m%(levelname)s \x1b[32m%(module)s/%(lineno)d-%(processName)s\x1b[1;33m] \x1b[0m%(message)s"
)
file_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)

stdout_handler.addFilter(logging.Filter("desktopenv"))

logger.addHandler(file_handler)
logger.addHandler(debug_handler)
logger.addHandler(stdout_handler)
#  }}} Logger Configs #

logger = logging.getLogger("desktopenv.experiment")


def distribute_tasks(test_all_meta: dict) -> List[tuple]:
    all_tasks = []
    for domain, examples in test_all_meta.items():
        for example_id in examples:
            all_tasks.append((domain, example_id))
    return all_tasks


def process_signal_handler(signum, frame, env_idx):
    """Signal handler for child processes to gracefully shut down their environments."""
    logger.info(f"Process {env_idx + 1} received signal {signum}. Shutting down...")
    
    # Get the active_environments from the caller's frame
    local_vars = frame.f_locals
    active_environments = local_vars.get('active_environments', [])
    
    # Close environment in the current process context
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

def run_env_tasks(task_queue: Queue, args: argparse.Namespace, shared_scores: list):
    active_environments = []
    env = None
    try:
        screen_size = (args.screen_width, args.screen_height)
        region = getattr(args, "region", None)
        snapshot_name = None
        if args.provider_name == "aws" and region is not None:
            try:
                from desktop_env.osworld.providers.aws.manager import IMAGE_ID_MAP

                screen_size = (args.screen_width, args.screen_height)
                snapshot_name = IMAGE_ID_MAP[region].get(
                    screen_size, IMAGE_ID_MAP[region][(1920, 1080)]
                )
            except Exception as e:
                logger.error(f"Failed to get snapshot_name from IMAGE_ID_MAP: {e}")
                snapshot_name = None

        env = DesktopEnv(
            path_to_vm=args.path_to_vm,
            action_space=args.action_space,
            provider_name=args.provider_name,
            region=region,
            snapshot_name=snapshot_name,
            screen_size=screen_size,
            headless=args.headless,
            os_type="Ubuntu",
            require_a11y_tree=args.observation_type in ["a11y_tree", "screenshot_a11y_tree", "som"],
            enable_proxy=True,
            client_password=args.client_password
        )
        env.start()
        active_environments.append(env)

        if "ui" in args.model.lower():
            agent = UITarsAgent(
                model=args.model,
                model_type="qwen25vl",
                base_url=args.base_url,
                api_key=args.api_key,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                temperature=args.temperature,
                max_trajectory_length=args.max_trajectory_length,
                max_image_history_length=args.max_image_history_length,
                use_thinking=args.use_thinking,
                language=args.language
            )
        elif "qwen3" in args.model.lower():
            agent = Qwen3VLAgent(
                model=args.model,
                base_url=args.base_url,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                temperature=args.temperature,
                history_n=8,
                action_space=args.action_space,
                coordinate_type="relative"
            )
        elif "claude" in args.model.lower():
            agent = AnthropicAgent(
                model=args.model,
                base_url=args.base_url,
                api_key=args.api_key,
                max_tokens=args.max_tokens,
            )
        elif "kimi" in args.model.lower():
            # Boyue API only support kimi-k2.5 with temperature 1 and top_p 0.95
            agent = KimiAgent(
                env=env,
                model=args.model,
                base_url=args.base_url,
                api_key=args.api_key,
                max_tokens=args.max_tokens,
                top_p=args.top_p if args.top_p == 0.95 else 0.95,
                temperature=args.temperature if args.temperature == 1 else 1,
                action_space=args.action_space,
                observation_type=args.observation_type,
                screen_size=(args.screen_width, args.screen_height),
                coordinate_type=args.coord,
                max_image_history_length=args.max_image_history_length,
                max_steps=args.max_steps,
                thinking=args.use_thinking,
                password=args.client_password
            )
        elif "glm" in args.model.lower():
            agent = GLM4VAgent(
                model=args.model,
                base_url=args.base_url,
                api_key=args.api_key,
                temperature=args.temperature,
                top_p=args.top_p,
                max_tokens=args.max_tokens,
                max_image_history_length=args.max_image_history_length,
                screen_width=args.screen_width,
                screen_height=args.screen_height
            )
        elif "seed" in args.model.lower():
            agent = SeedAgent(
                model=args.model,
                base_url=args.base_url,
                api_key=args.api_key,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                temperature=args.temperature,
                max_trajectory_length=args.max_trajectory_length,
                history_n=args.max_image_history_length,
                use_thinking=args.use_thinking,
            )
        elif "gemini" in args.model.lower():
            # TODO
            pass
        else:
            raise Exception(f"Not support {args.model} model!")

        logger.info(f"Process {current_process().name} started.")
        while True:
            try:
                item = task_queue.get(timeout=5)
            except Exception:
                break
            domain, example_id = item
            try:
                config_file = os.path.join(
                    args.rollout_task_dir, f"{domain}/{example_id}.json"
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
                    lib_run_single.run_single_example_os_caliber_omni(
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
                    with open(os.path.join(os.path.dirname(example_result_dir), "error.jsonl"), "a") as f:
                        f.write(
                            json.dumps(
                                {"Error": f"{domain}/{example_id} - {e}"}
                            )
                        )
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
        except Exception as e:
            logger.error(f"{current_process().name} error during environment cleanup: {e}")



def signal_handler(signum, frame):
    """Handle termination signals (SIGINT, SIGTERM) to gracefully shutdown environments."""
    global is_terminating, active_environments, processes
    
    # Avoid duplicate handling
    if is_terminating:
        return
    
    is_terminating = True
    logger.info(f"Received signal {signum}. Gracefully shutting down...")
    
    # Close all registered environments in the main process
    for env in active_environments:
        try:
            logger.info(f"Closing environment...")
            env.close()
            logger.info(f"Environment closed successfully")
        except Exception as e:
            logger.error(f"Error closing environment: {e}")
    
    # Send termination signal to all child processes first
    for p in processes:
        if p.is_alive():
            try:
                logger.info(f"Sending termination signal to process {p.name}...")
                p.terminate()
            except Exception as e:
                logger.error(f"Error sending termination signal to process: {e}")
    
    # Allow a short time for processes to handle their own cleanup
    time.sleep(1)
    
    # Forcefully terminate any processes that didn't exit
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

def run_online_rollout(task_queue: Queue, args: argparse.Namespace, task_all_meta: dict, lock):
    active_environments = []
    env = None
    try:
        screen_size = (args.screen_width, args.screen_height)
        region = getattr(args, "region", None)
        snapshot_name = None
        if args.provider_name == "aws" and region is not None:
            try:
                from desktop_env.osworld.providers.aws.manager import IMAGE_ID_MAP

                screen_size = (args.screen_width, args.screen_height)
                snapshot_name = IMAGE_ID_MAP[region].get(
                    screen_size, IMAGE_ID_MAP[region][(1920, 1080)]
                )
            except Exception as e:
                logger.error(f"Failed to get snapshot_name from IMAGE_ID_MAP: {e}")
                snapshot_name = None

        env = DesktopEnv(
            path_to_vm=args.path_to_vm,
            action_space=args.action_space,
            provider_name=args.provider_name,
            region=region,
            snapshot_name=snapshot_name,
            screen_size=screen_size,
            headless=args.headless,
            os_type="Ubuntu",
            require_a11y_tree=args.observation_type in ["a11y_tree", "screenshot_a11y_tree", "som"],
            enable_proxy=True,
            client_password=args.client_password
        )
        env.start()
        active_environments.append(env)

        engine_params = {
            "engine_type": args.ig_provider,
            "model": args.ig_model,
            "base_url": getattr(args, "ig_url", ""),
            "api_key": getattr(args, "ig_api_key", ""),
            "temperature": getattr(args, "ig_temperature", None),
            "agent_name": "coarse_instruction_generator"
        }
        ig_agent = CoarseInstructionGenerationAgent(engine_params=engine_params)
        task_generator = OSCaliberTaskGenerator(rollout_task_dir=args.rollout_task_dir, env=env, agent=ig_agent)

        while True:
            try:
                task_queue.get(timeout=5)
            except Exception:
                break

            task_file_list = task_generator.generate_task(task_nums=args.rollout_task_nums, app_list=args.rollout_app_list)
            with lock:
                for app_name, new_tasks in task_file_list.items():
                    existing_tasks = task_all_meta.get(app_name, [])
                    updated_tasks = existing_tasks + new_tasks
                    task_all_meta[app_name] = updated_tasks
        
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

def offline_test(args: argparse.Namespace, test_all_meta: dict) -> None:
    global processes
    logger.info("Args: %s", args)
    all_tasks = distribute_tasks(test_all_meta)
    logger.info(f"Total tasks: {len(all_tasks)}")
    with Manager() as manager:
        shared_scores = manager.list()
        task_queue = manager.Queue()
        for item in all_tasks:
            task_queue.put(item)
        num_envs = args.num_envs
        processes = []
        for i in range(num_envs):
            p = Process(
                target=run_env_tasks,
                args=(task_queue, args, shared_scores),
                name=f"EnvProcess-{i+1}"
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
                            args=(task_queue, args, shared_scores),
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

def online_test(args: argparse.Namespace):
    """
    Online testing with two-phase concurrency:
    1. Multiple processes concurrently generate tasks (each handles all apps)
    2. All generated tasks are executed concurrently
    """
    # Prepare directories
    args.rollout_task_dir = os.path.join(
        args.rollout_base_dir, 
        f'oscaliber_{args.exp_name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'
    )
    os.makedirs(args.rollout_task_dir, exist_ok=True)
    
    # Phase 1: Concurrent task generation
    logger.info(f"=== PHASE 1: CONCURRENT TASK GENERATION ===")
    
    # Shared dictionary to collect generated tasks from all processes
    with Manager() as manager:
        shared_task_meta = manager.dict()
        task_queue = manager.Queue()
        lock = manager.Lock() 
        for _ in range(args.rollout_times):
            task_queue.put({})

        # Start task generation processes
        processes = []

        for i in range(args.num_envs):
            p = Process(
                target=run_online_rollout,
                args=(task_queue, args, shared_task_meta, lock),
                name=f"TaskGenProcess-{i+1}"
            )
            p.daemon = True
            p.start()
            processes.append(p)
            logger.info(f"Started task generation process {p.name} with PID {p.pid}")
            
        try:
            while True:
                alive_count = 0
                for idx, p in enumerate(processes):
                    if not p.is_alive():
                        logger.warning(f"Process {p.name} died, restarting...")
                        new_p = Process(
                            target=run_online_rollout,
                            args=(task_queue, args, shared_task_meta, lock),
                            name=f"TaskGenProcess-Restart-{idx+1}"
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
        
        # Convert shared dict to regular dict for Phase 2
        test_all_meta = dict(shared_task_meta)
    
    # Phase 1 Summary
    total_tasks = sum(len(tasks) for tasks in test_all_meta.values())
    total_apps = len(test_all_meta)
    logger.info(f"Generated {total_apps} app groups with {total_tasks} total tasks")
    logger.info(f"Output directory: {args.rollout_task_dir}")
    with open(os.path.join(args.rollout_task_dir, "test_all.json"), "w", encoding="utf-8") as f:
        json.dump(test_all_meta, f, indent=4, ensure_ascii=False)

    # Phase 2: Concurrent task execution
    logger.info(f"\n=== PHASE 2: CONCURRENT TASK EXECUTION ===")
    
    # Call offline_test with generated tasks
    offline_test(
        args=args,
        test_all_meta=test_all_meta
    )

if __name__ == "__main__":
    ####### The complete version of the list of examples #######
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    # Register signal handlers for graceful termination
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signal
    
    try:
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

        if args.rollout_mode == "offline":
            with open(args.rollout_test_all_meta_path, "r", encoding="utf-8") as f:
                test_file_list = json.load(f)
            offline_test(args, test_file_list)
        elif args.rollout_mode == "online":
            online_test(args)

    except KeyboardInterrupt:
        logger.info("Main process received KeyboardInterrupt.")
        # Signal handler will take care of cleanup
    except Exception as e:
        logger.error(f"Unexpected error in main process: {e}", exc_info=True)
        # Also trigger cleanup for unhandled exceptions
        signal_handler(signal.SIGTERM, None)
    finally:
        # Final cleanup in case any environments or processes remain
        logger.info("Main process final cleanup...")
        for env in active_environments:
            if env is not None:
                try:
                    logger.info(f"Closing environment in final cleanup...")
                    env.close()
                    logger.info(f"Environment closed successfully in final cleanup")
                except Exception as e:
                    logger.error(f"Error during final environment cleanup: {e}")
        
        # First try gentle termination
        for p in processes:
            if p is not None and p.is_alive():
                try:
                    logger.info(f"Terminating process {p.name}...")
                    p.terminate()
                except Exception as e:
                    logger.error(f"Error terminating process: {e}")
        
        # Wait a moment for processes to terminate
        time.sleep(1)
        
        # Then force kill if needed
        for p in processes:
            if p is not None and p.is_alive():
                try:
                    logger.info(f"Force killing process {p.name}...")
                    os.kill(p.pid, signal.SIGKILL)
                    logger.info(f"Process {p.name} force killed")
                except Exception as e:
                    logger.error(f"Error force killing process: {e}")