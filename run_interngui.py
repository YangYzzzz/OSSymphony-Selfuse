import argparse
import copy
import datetime
import json
import logging
import os
import sys
import signal
import time
from multiprocessing import Process, Manager, current_process, Queue
from mm_agents.interngui.agents.interngui import InternGUI
from mm_agents.interngui.agents.os_aci import OSWorldACI
import shutil
import lib_run_single
from desktop_env.desktop_env import DesktopEnv

from dotenv import load_dotenv

load_dotenv()


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

# Set up File Handler
file_handler = logging.FileHandler(filename="log.txt")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
file_handler.addFilter(logging.Filter("desktopenv"))
logger.addHandler(file_handler)

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
    engine_params_for_orchestrator,
    engine_params_for_grounder,
    engine_params_for_coder,
    engine_params_for_memoryer,
    engine_params_for_searcher,
):
    active_environments = []
    env = None
    search_env = None
    try:
        # Use IMAGE_ID_MAP for AWS provider to get snapshot_name
        snapshot_name = None
        region = getattr(args, "region", None)
        if args.provider_name == "aws" and region is not None:
            try:
                from desktop_env.providers.aws.manager import IMAGE_ID_MAP

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
            screen_size=(args.screen_width, args.screen_height),
            headless=args.headless,
            os_type="Ubuntu",
            require_a11y_tree=args.observation_type
            in ["a11y_tree", "screenshot_a11y_tree", "som"],
            enable_proxy=True,
            client_password=getattr(args, "client_password", ""),
        )
        env.start()

        search_env = DesktopEnv(
            path_to_vm=args.path_to_vm,
            action_space=args.action_space,
            provider_name=args.provider_name,
            region=region,
            snapshot_name=snapshot_name,
            screen_size=(args.screen_width, args.screen_height),
            headless=args.headless,
            os_type="Ubuntu",
            require_a11y_tree=args.observation_type
            in ["a11y_tree", "screenshot_a11y_tree", "som"],
            enable_proxy=True,
            client_password=getattr(args, "client_password", ""),
        )

        engine_params_for_ocr = copy.deepcopy(engine_params_for_orchestrator)
        engine_params_for_ocr["agent_name"] = "ocr"
        os_aci = OSWorldACI(
            env=env, # 主环境
            search_env=search_env,
            platform="linux",
            engine_params_for_ocr=engine_params_for_ocr, # 用于OCR总结的VLM使用OrchestratorConfig的配置即可
            engine_params_for_grounder=engine_params_for_grounder,
            engine_params_for_coder=engine_params_for_coder,
            engine_params_for_searcher=engine_params_for_searcher,
            width=args.screen_width,
            height=args.screen_height,
        )
        agent = InternGUI(
            engine_params_for_orchestrator,
            engine_params_for_memoryer,
            os_aci,
            platform="linux",
            max_trajectory_length=args.max_trajectory_length,
            enable_reflection=args.enable_reflection,
            use_search_first=args.use_search_first,
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
                    args.test_config_base_dir, f"examples/{domain}/{example_id}.json"
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
                    lib_run_single.run_single_example(
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
                    # try:
                    #     env.controller.end_recording(
                    #         os.path.join(example_result_dir, "recording.mp4")
                    #     )
                    # except Exception as rec_e:
                    #     logger.error(f"Failed to end recording: {rec_e}")
                    with open(os.path.join(os.path.dirname(example_result_dir), "error.jsonl"), "a") as f:
                        f.write(json.dumps({"Error": f"{domain}/{example_id} - {e}"}))
                        f.write("\n")
                    # with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
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
    parser.add_argument("--screen_width", type=int, default=1920)
    parser.add_argument("--screen_height", type=int, default=1080)
    parser.add_argument("--sleep_after_execution", type=float, default=1.0)
    parser.add_argument("--max_steps", type=int, default=15)

    parser.add_argument("--domain", type=str, default="all")
    parser.add_argument(
        "--test_all_meta_path", type=str, default="evaluation_examples/test_all.json"
    )
    parser.add_argument(
        "--test_config_base_dir", type=str, default="evaluation_examples"
    )
    parser.add_argument("--result_dir", type=str, default="./results")

    parser.add_argument(
        "--region", type=str, default="us-east-1", help="AWS region for the VM"
    )
    parser.add_argument(
        "--client_password", type=str, default="password", help="Client password"
    )

    # agent config
    parser.add_argument("--max_trajectory_length", type=int, default=8)
    parser.add_argument("--enable_reflection", action="store_true", default=False)
    parser.add_argument("--enable_rewrite_instruction", action="store_true", default=False)
    parser.add_argument("--use_search_first", action="store_true", default=False)
    parser.add_argument(
        "--tool_config", 
        type=str, 
        default="/nvme/yangbowen/yangbowen/OSWorld/mm_agents/interngui/tool/all_tool_config.yaml",
        help="The path of tool config yaml, default uses /nvme/yangbowen/yangbowen/OSWorld/Agent-S/gui_agents/interngui/tool/all_tool_config.yaml"
    )

    # generator model config
    parser.add_argument("--orchestrator_provider", type=str, default="openai")
    parser.add_argument("--orchestrator_model", type=str, default="gpt-4o")
    parser.add_argument(
        "--orchestrator_url",
        type=str,
        default="",
        help="The URL of the main orchestrator model API.",
    )
    parser.add_argument(
        "--orchestrator_api_key",
        type=str,
        default="",
        help="The API key of the main orchestrator model.",
    )
    parser.add_argument(
        "--orchestrator_temperature",
        type=float,
        default=None,
        help="Temperature to fix the orchestrator model at (e.g. o3 can only be run with 1.0)",
    )
    parser.add_argument("--orchestrator_keep_first_image", action="store_true", default=False, help="Whether keep the first image(first state) in the orchestrator agent")

    # code model config
    parser.add_argument("--coder_provider", type=str, default="openai")
    parser.add_argument("--coder_model", type=str, default="gpt-4o")
    parser.add_argument(
        "--coder_url",
        type=str,
        default="",
        help="The URL of the coder model API.",
    )
    parser.add_argument(
        "--coder_api_key",
        type=str,
        default="",
        help="The API key of the coder model.",
    )
    parser.add_argument(
        "--coder_temperature",
        type=float,
        default=None,
        help="Temperature to fix the coder model at (e.g. o3 can only be run with 1.0)",
    )
    parser.add_argument(
        "--coder_budget",
        type=int,
        default=20,
        help="Max inner loop steps of coder agent",
    )

    # reflection and memory model config
    parser.add_argument("--memoryer_provider", type=str, default="openai")
    parser.add_argument("--memoryer_model", type=str, default="gpt-4o")
    parser.add_argument(
        "--memoryer_url",
        type=str,
        default="",
        help="The URL of the memoryer model API.",
    )
    parser.add_argument(
        "--memoryer_api_key",
        type=str,
        default="",
        help="The API key of the memoryer model.",
    )
    parser.add_argument(
        "--memoryer_temperature",
        type=float,
        default=None,
        help="Temperature to fix the memoryer model at (e.g. o3 can only be run with 1.0)",
    )
    parser.add_argument(
        "--memoryer_level",
        type=int,
        default=3,
        help="The level of memoryer's output (for ablation study only).",
    )

    # search model config
    parser.add_argument("--searcher_provider", type=str, default="openai")
    parser.add_argument("--searcher_model", type=str, default="gpt-4o")
    parser.add_argument(
        "--searcher_url",
        type=str,
        default="",
        help="The URL of the searcher model API.",
    )
    parser.add_argument(
        "--searcher_api_key",
        type=str,
        default="",
        help="The API key of the searcher model.",
    )
    parser.add_argument(
        "--searcher_temperature",
        type=float,
        default=None,
        help="Temperature to fix searcher model at (e.g. o3 can only be run with 1.0)",
    )
    parser.add_argument(
        "--searcher_type",
        type=str,
        default="vlm",
        help="Type of search agent, vlm/llm(all in search action), default is vlm",
    )
    parser.add_argument(
        "--searcher_budget",
        type=int,
        default=20,
        help="Max inner loop steps of search agent",
    )

    # grounding model config, temperture is 0 with hardcode
    parser.add_argument(
        "--grounder_provider",
        type=str,
        required=True,
        help="The provider for the grounder model",
    )
    parser.add_argument(
        "--grounder_url", type=str, required=True, help="The URL of the grounder model"
    )
    parser.add_argument(
        "--grounder_api_key",
        type=str,
        default="",
        help="The API key of the grounder model.",
    )
    parser.add_argument(
        "--grounder_model",
        type=str,
        required=True,
        help="The model name for the grounder model",
    )
    parser.add_argument(
        "--grounding_width",
        type=int,
        required=True,
        help="Width of screenshot image after processor rescaling",
    )
    parser.add_argument(
        "--grounding_height",
        type=int,
        required=True,
        help="Height of screenshot image after processor rescaling",
    )
    parser.add_argument(
        "--grounding_smart_resize",
        type=bool,
        required=True,
        help="UI-TARS-1.5 and ScaleCUA needs smart resize, if this set, grounding_width and grounding_height is no use.",
    )
    parser.add_argument(
        "--grounder_zoom_in_time",
        type=int,
        default=1,
        help="Zoom-in times for grounder agent, aiming to enhance grounding ability.",
    )


    # 实验名
    parser.add_argument(
        "--exp_name",
        type=str,
        default="",
        help="Experiment Name",
    )

    # 穷逼版 passk 测试
    parser.add_argument(
        "--pass_k",
        type=int,
        default=1,
        help="Pass k parameter, if > 1, run multi times(to save dollar, we only rerun the past error case.)",
    )
    # 将50步测试扩展到100步测试，仅重测已有达到50步但未做对的任务
    parser.add_argument(
        "--step_incremental_test",
        action="store_true", default=False,
        help="Max Steps参数中配置当前需要的最大参数, 当前参数开启后动态查找上一步的最大step, 执行 last_max_step->cur_max_step 的增量式补充测试",
    )

    args = parser.parse_args()

    return args


def test(args: argparse.Namespace, test_all_meta: dict) -> None:
    global processes
    logger.info("Args: %s", args)
    all_tasks = distribute_tasks(test_all_meta)
    logger.info(f"Total tasks: {len(all_tasks)}")

    engine_params_for_orchestrator = {
        "engine_type": args.orchestrator_provider,
        "model": args.orchestrator_model,
        "base_url": getattr(args, "orchestrator_url", ""),
        "api_key": getattr(args, "orchestrator_api_key", ""),
        "temperature": getattr(args, "orchestrator_temperature", None),
        "tool_config": args.tool_config,
        "keep_first_image": args.orchestrator_keep_first_image,
        "agent_name": "orchestrator"
    }


    engine_params_for_grounder = {
        "engine_type": args.grounder_provider,
        "model": args.grounder_model,
        "base_url": getattr(args, "grounder_url", ""),
        "api_key": getattr(args, "grounder_api_key", ""),
        "grounding_width": args.grounding_width,
        "grounding_height": args.grounding_height,
        "grounding_smart_resize": args.grounding_smart_resize,
        "grounder_zoom_in_time": args.grounder_zoom_in_time,
        "agent_name": "grounder"
    }

    engine_params_for_coder = {
        "engine_type": args.coder_provider,
        "model": args.coder_model,
        "base_url": getattr(args, "coder_url", ""),
        "api_key": getattr(args, "coder_api_key", ""),
        "temperature": getattr(args, "coder_temperature", None),
        "budget": args.coder_budget,
        "agent_name": "coder"
    }

    engine_params_for_memoryer = {
        "engine_type": args.memoryer_provider,
        "model": args.memoryer_model,
        "base_url": getattr(args, "memoryer_url", ""),
        "api_key": getattr(args, "memoryer_api_key", ""),
        "temperature": getattr(args, "memoryer_temperature", None),
        "memoryer_level": args.memoryer_level,
        "agent_name": "memoryer"
    }

    engine_params_for_searcher = {
        "engine_type": args.searcher_provider,
        "model": args.searcher_model,
        "base_url": getattr(args, "searcher_url", ""),
        "api_key": getattr(args, "searcher_api_key", ""),
        "temperature": getattr(args, "searcher_temperature", None),
        "budget": args.searcher_budget,
        "type": args.searcher_type,
        "agent_name": "searcher"
    }

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
                args=(
                    task_queue,
                    args,
                    shared_scores,
                    engine_params_for_orchestrator,
                    engine_params_for_grounder,
                    engine_params_for_coder,
                    engine_params_for_memoryer,
                    engine_params_for_searcher
                ),
                name=f"EnvProcess-{i+1}",
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
                            args=(
                                task_queue,
                                args,
                                shared_scores,
                                engine_params_for_orchestrator,
                                engine_params_for_grounder,
                                engine_params_for_coder,
                                engine_params_for_memoryer,
                                engine_params_for_searcher
                            ),
                            name=f"EnvProcess-Restart-{idx+1}",
                        )
                        new_p.daemon = True
                        new_p.start()
                        processes[idx] = new_p
                        logger.info(
                            f"Restarted process {new_p.name} with PID {new_p.pid}"
                        )
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
            logger.info(
                "Main process received KeyboardInterrupt. Initiating graceful shutdown..."
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while waiting for processes: {e}", exc_info=True
            )
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

# 把做错的目前也都视为未完成的
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
                            score = float(f.read())
                        if not incremental_test:
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

    # 执行 Pass k 测试
    for t in range(1, args.pass_k + 1):
        logger.info(f"====================\nPass K: no.{t} turn is started\n====================")
        test_file_list = get_unfinished(
            target_dir=args.result_dir,
            total_file_json=test_all_meta,
            turn=t,
            incremental_test=args.step_incremental_test
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
        logger.info(f"====================\nPass K: no.{t} turn is ended\n====================")
    
    logger.info(f"====================\nExperiment {args.exp_name} is totally ended!\n====================")
