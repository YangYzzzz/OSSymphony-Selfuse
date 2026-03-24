import datetime
import json
import logging
import os
import time
from PIL import Image, ImageDraw
from wrapt_timeout_decorator import *
import io
from typing import List, Union
from mm_agents.os_symphony.utils.common_utils import draw_coordinates
from mm_agents.os_symphony.utils.process_context import set_current_result_dir
import copy

logger = logging.getLogger("desktopenv.experiment")

def run_single_example(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    set_current_result_dir(example_result_dir)
    
    agent.reset(result_dir=example_result_dir)
    env.reset(task_config=example)
    time.sleep(30) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    # env.controller.start_recording()
    start_time = time.time()
    # 设置线程级别的全局变量, 以便于 call_llm_safe 统计 token 使用情况

    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs,
            step_idx == max_steps - 1 # 与其他Agent的冲突传参 TODO: @Yang
        )
        # 理论上每一轮只会产生一个操作
        for action in actions:
            # Save screenshot and trajectory information
            if "reflection" in response and response["reflection"].get("is_milestone"):
                img_name = f"step_{step_idx + 1}_milestone.png"
            else:
                img_name = f"step_{step_idx + 1}.png"
                
            with open(os.path.join(example_result_dir, img_name),
                      "wb") as _f:
                _f.write(obs['screenshot'])
            if "coordinates" in response and response["coordinates"]:
                draw_coordinates(
                    image_bytes=obs['screenshot'], 
                    coordinates=response["coordinates"], 
                    save_path=os.path.join(example_result_dir, img_name[:-4] + "_draw.png")
                )

            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)
            logger.info("Done: %s", done)

            with open(os.path.join(example_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "instruction": instruction,
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": response,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }))
                f.write("\n")
            with open(os.path.join(example_result_dir, f"traj_{step_idx+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": response,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }, f, indent=4, ensure_ascii=False)
            if done:
                logger.info("The episode is done.")
                time.sleep(60)
                break
        step_idx += 1
    end_time = time.time()
    result = float(env.evaluate())
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")

    with open(os.path.join(example_result_dir, "time.txt"), "w", encoding="utf-8") as f:
        f.write(f"{end_time-start_time:.2f}\n")
    # env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))

def run_single_example_gemini(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    run_single_example_qwen3vl(agent, env, example, max_steps, instruction, args, example_result_dir, scores)
        
def run_single_example_seedvl(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    run_single_example_qwen3vl(agent, env, example, max_steps, instruction, args, example_result_dir, scores)
        
def run_single_example_qwen3vl(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    set_current_result_dir(example_result_dir)
    
    agent.reset()
    env.reset(task_config=example)
    time.sleep(30) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    # env.controller.start_recording()
    start_time = time.time()
    # 设置线程级别的全局变量, 以便于 call_llm_safe 统计 token 使用情况

    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )
        # 理论上每一轮只会产生一个操作
        for action in actions:
            # Save screenshot and trajectory information
            if "reflection" in response and response["reflection"].get("is_milestone"):
                img_name = f"step_{step_idx + 1}_milestone.png"
            else:
                img_name = f"step_{step_idx + 1}.png"
                
            with open(os.path.join(example_result_dir, img_name),
                      "wb") as _f:
                _f.write(obs['screenshot'])
            if "coordinates" in response and response["coordinates"]:
                draw_coordinates(
                    image_bytes=obs['screenshot'], 
                    coordinates=response["coordinates"], 
                    save_path=os.path.join(example_result_dir, img_name[:-4] + "_draw.png")
                )

            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)
            logger.info("Done: %s", done)

            with open(os.path.join(example_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "instruction": instruction,
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": response,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }))
                f.write("\n")
            with open(os.path.join(example_result_dir, f"traj_{step_idx+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": response,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }, f, indent=4, ensure_ascii=False)
            if done:
                logger.info("The episode is done.")
                time.sleep(60)
                break
        step_idx += 1
    end_time = time.time()
    result = float(env.evaluate())
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")

    with open(os.path.join(example_result_dir, "time.txt"), "w", encoding="utf-8") as f:
        f.write(f"{end_time-start_time:.2f}\n")
    # env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))

def run_single_example_ossymphony2(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    set_current_result_dir(example_result_dir)
    
    agent.reset()
    env.reset(task_config=example)
    time.sleep(30) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    # env.controller.start_recording()
    start_time = time.time()
    # 设置线程级别的全局变量, 以便于 call_llm_safe 统计 token 使用情况

    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )
        # 理论上每一轮只会产生一个操作
        for action in actions:
            # Save screenshot and trajectory information
            if "reflection" in response and response["reflection"].get("is_milestone"):
                img_name = f"step_{step_idx + 1}_milestone.png"
            else:
                img_name = f"step_{step_idx + 1}.png"
                
            with open(os.path.join(example_result_dir, img_name),
                      "wb") as _f:
                _f.write(obs['screenshot'])
            if "coordinates" in response and response["coordinates"]:
                draw_coordinates(
                    image_bytes=obs['screenshot'], 
                    coordinates=response["coordinates"], 
                    save_path=os.path.join(example_result_dir, img_name[:-4] + "_draw.png")
                )
            
            if action.startswith("EXEC_CODE"):        # 如果是执行代码，就在这里提前执行好
                print("=" * 60)
                print(" " * 20 + "Executing Code")
                print("=" * 60)
                _, lang, code = action.split("|")
                if lang == "python":
                    result = env.controller.run_python_script(code)
                else:
                    result = env.controller.run_python_script(code)
                action = code

                # 制作code的返回日志
                result_content = ""
                result_content += f"Status: {result.get('status', '')}\n"
                result_content += f"Output: {result.get('output', '')}\n"
                result_content += f"Error: {result.get('error', '')}\n"
                result_content += f"Message: {result.get('message', '')}\n"
                agent.last_code_result = result_content

            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info("Done: %s", done)

            with open(os.path.join(example_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "instruction": instruction,
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": response,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }))
                f.write("\n")
            with open(os.path.join(example_result_dir, f"traj_{step_idx+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": response,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }, f, indent=4, ensure_ascii=False)
            if done:
                logger.info("The episode is done.")
                time.sleep(60)
                break
        step_idx += 1
    end_time = time.time()
    result = float(env.evaluate())
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")

    with open(os.path.join(example_result_dir, "time.txt"), "w", encoding="utf-8") as f:
        f.write(f"{end_time-start_time:.2f}\n")
        
def run_single_example_agents3(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    set_current_result_dir(example_result_dir)
    
    agent.reset()
    env.reset(task_config=example)
    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    # env.controller.start_recording()
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )
        # 理论上每一轮只会产生一个操作
        for action in actions:
            # Capture the timestamp before executing the action

            # Save screenshot and trajectory information
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}.png"),
                      "wb") as _f:
                _f.write(obs['screenshot'])

            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info("Reward: %.2f", reward)
            logger.info("Done: %s", done)
            
            with open(os.path.join(example_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "instruction": instruction,
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "response": response,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}.png"
                }))
                f.write("\n")
            with open(os.path.join(example_result_dir, f"traj_{step_idx+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "response": response,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}.png"
                }, f, indent=4, ensure_ascii=False)
            if done:
                logger.info("The episode is done.")
                break
        step_idx += 1
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    # env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))

def absolute_to_relative_coordinate(coords: list, height, width):
    # [abs_x, abs_y] -> [rel_x, rel_y] (0-1000)
    coords[0] = coords[0] / width * 1000
    coords[1] = coords[1] / height * 1000
    return coords

def run_single_example_os_caliber_omni(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    # Setup logger
    set_current_result_dir(example_result_dir)

    # Reset Environment and Agent
    agent.reset()
    env.reset(task_config=example)
    time.sleep(60)  # Wait for the environment to be ready
    obs = env._get_obs()  # Get the initial observation
    
    done = False
    step_idx = 0
    # Generate timestamp for ID and metadata
    global_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
    
    model_name = agent.model if hasattr(agent, "model") else (agent.model_name if hasattr(agent, "model_name") else "undefined model")
    # Initialize the Meta JSON structure
    meta_json = {
        "trace_id": f"{example['id']}_{global_timestamp}",
        "task_id": example["id"],
        "platform": "Desktop",
        "subdomain": "Ubuntu 22.04",
        "environment_details": {
            "screen_resolution": "1920x1080",
            "related_apps": example.get("related_apps") or [example.get("snapshot")] # 向前兼容, 后续仅通过 related_apps 记录
        },
        "instruction": instruction,
        "agent": model_name,
        "annotation_metadata": {
            "annotator_id": "yangbowen", # 根据实际情况修改或作为参数传入
            "annotation_tool_version": "gradio_v0.1",
            "timestamp": global_timestamp
        },
        # To be populated
        "trajectory": [],
        "trajectory_length": 0,
        "model_judge": {
            "binary_reward": 0,
            "rationale": ""
        }
    }

    while not done and step_idx < max_steps:
        # Agent prediction
        response, actions = agent.predict(
            instruction,
            copy.deepcopy(obs)      # agent loop内部会修改obs的size，如果不传深拷贝后面画图就会收到被resize过的图像
        )
        
        # Iterate through actions (usually one per step)
        raw_response = ""
        thought = ""
        meta_action = []
        action_list = []
        coordinate_1 = None
        coordinate_2 = None
        for i, (action, response_per_action) in enumerate(zip(actions, response)):
            
            # Define current screenshot filename (using step_idx to start from 0)
            current_screenshot_name = f"step_{step_idx}.png"
            current_screenshot_path = os.path.join(example_result_dir, current_screenshot_name)

            # Save screenshot
            if i == 0:
                with open(current_screenshot_path, "wb") as _f:
                    _f.write(obs['screenshot'])

            # Optional: Draw coordinates for debug visualization
            if "coordinate" in response_per_action and isinstance(response_per_action["coordinate"], list):
                coordinates = response_per_action["coordinate"]
                # if "coordinate2" in response_per_action and isinstance(response_per_action["coordinate2"], list):
                #     coordinates += response_per_action["coordinate2"]
                draw_coordinates(
                    image_bytes=obs['screenshot'], 
                    coordinates=coordinates if not isinstance(coordinates[0], list) else coordinates[0] + coordinates[1], # 1 point and 2 point
                    save_path=os.path.join(example_result_dir, f"step_{step_idx}_draw.png")
                )

            raw_response = response_per_action.get("raw_response", "")
            thought = response_per_action.get("thought", "")
            action_list.append(response_per_action.get("action", ""))
            meta_action.append(response_per_action.get("meta_action", None))
            if response_per_action.get("coordinate", None):
                # 目前不确定claude, gemini是否存在单步骤出现超过两个以上坐标
                if "claude" in model_name or "gemini" in model_name:
                    if not isinstance(response_per_action.get('coordinate')[0], list):
                        coordinate_1 = absolute_to_relative_coordinate(response_per_action.get("coordinate"), args.screen_height, args.screen_width) # First coords
                    else:
                        coordinate_2 = [
                            absolute_to_relative_coordinate(response_per_action["coordinate"][0], args.screen_height, args.screen_width),
                            absolute_to_relative_coordinate(response_per_action["coordinate"][1], args.screen_height, args.screen_width)
                        ]
                else:
                    if not coordinate_1:
                        coordinate_1 = absolute_to_relative_coordinate(response_per_action.get("coordinate"), args.screen_height, args.screen_width) # First coords
                    elif not coordinate_2:
                        # Second coords
                        coordinate_2 = [coordinate_1, absolute_to_relative_coordinate(response_per_action.get("coordinate"), args.screen_height, args.screen_width)]
                        coordinate_1 = None

            # Execute Environment Step
            obs, _, done, _ = env.step(action, args.sleep_after_execution)
            
            if done:
                logger.info("The episode is done.")
                break

        # --- Construct Trajectory Step Data ---
        step_data = {
            "step_index": step_idx,
            "screenshot_path": os.path.relpath(
                current_screenshot_path, 
                start=os.path.dirname(example_result_dir)
            ), # Relative path
            "raw_response": raw_response, # Full response
            "thought": thought,  # Thought
            "action": ";".join(action_list), # Action str, not pyautogui
            "coordinate": coordinate_1, # [x, y] or None
            "coordinate2": coordinate_2, # [[x1,y1], [x2,y2]] or None
            "meta_action": meta_action
        }
        
        # Append to trajectory
        meta_json["trajectory"].append(step_data)

        step_idx += 1

    # Update trajectory length
    meta_json["trajectory_length"] = step_idx

    # --- Evaluation ---
    # Check if agent has evaluate method and it is callable
    if args.enable_self_judge:
        try:
            # Passing both instruction and obs as requested
            result = agent.evaluate(instruction, obs)
            
            # Update model_judge in meta_json
            meta_json["model_judge"]["binary_reward"] = result['score']
            meta_json["model_judge"]["rationale"] = result['thought']
            
        except Exception as e:
            logger.error(f"Error during agent evaluation: {e}")
            meta_json["model_judge"]["binary_reward"] = 0
            meta_json["model_judge"]["rationale"] = f"Evaluation failed: {e}"
    else:
        meta_json["model_judge"]["binary_reward"] = 0
        meta_json["model_judge"]["rationale"] = "Not enable agent's self judge."

    scores.append(1) # No use

    # --- Save Meta JSON ---
    meta_json_path = os.path.join(os.path.dirname(example_result_dir), f"meta_{example['id']}.json")
    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(meta_json, f, indent=4, ensure_ascii=False)
        
    logger.info(f"Saved meta.json to {meta_json_path}")



def run_single_example_kimi(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    agent.reset(runtime_logger)
    env.reset(task_config=example)
    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    while not done and step_idx < max_steps:
        response, actions = agent.predict(instruction, obs)
        response = response[0] # Modified by @Yang
        
        logger.info(f"Got Action: {actions}")
        # Break if no actions
        if not actions or len(actions)==0 or actions[0]=="" or actions[0].lower().startswith("error"): 
            break

        for action in actions:
            # Capture the timestamp before executing the action
            logger.info("Step %d: %s", step_idx + 1, action)
            
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info(f"Action {action} executed, reward: {reward}, done: {done}")
            # Save screenshot and trajectory information
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}.png"),
                      "wb") as _f:
                _f.write(obs['screenshot'])

            with open(os.path.join(example_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "step_num": step_idx + 1,
                    "action": action,
                    "natural_language_action": response.get("action"),
                    "response": response,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}.png"
                }, ensure_ascii=False))
                f.write("\n")

            with open(os.path.join(example_result_dir, f"traj_{step_idx+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "step_num": step_idx + 1,
                    "action": action,
                    "natural_language_action": response.get("action"),
                    "response": response,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}.png"
                }, f, indent=4, ensure_ascii=False)

            if done:
                logger.info("The episode is done.")
                break
        step_idx += 1

    time.sleep(30) # Wait for the environment to settle
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")

def run_single_example_uitars15(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)

    agent.reset()
    env.reset(task_config=example)
    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    # env.controller.start_recording()
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )
        # 理论上每一轮只会产生一个操作
        for i, (action, response_per_action) in enumerate(zip(actions, response)):
            # Capture the timestamp before executing the action
            # Save screenshot and trajectory information
            if i == 0:
                with open(os.path.join(example_result_dir, f"step_{step_idx + 1}.png"),
                        "wb") as _f:
                    _f.write(obs['screenshot'])

            if "coords" in response_per_action and isinstance(response_per_action["coords"], list):
                coords = [coord * 1920 if i % 2 == 0 else coord * 1080 for i, coord in enumerate(response_per_action["coords"])]
                draw_coordinates(
                    image_bytes=obs['screenshot'], 
                    coordinates=coords, 
                    save_path=os.path.join(example_result_dir, f"step_{step_idx + 1}_draw.png")
                )

            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            obs, reward, done, info = env.step(action, args.sleep_after_execution)
            
            with open(os.path.join(example_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "instruction": instruction,
                    "step_num": step_idx + 1,
                    "action_num": i + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "response": response_per_action,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}.png"
                }, ensure_ascii=False))
                f.write("\n")

            with open(os.path.join(example_result_dir, f"traj_{step_idx+1}_{i+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "step_num": step_idx + 1,
                    "action_num": i + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "response": response_per_action,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}.png"
                }, f, indent=4, ensure_ascii=False)

            if done:
                logger.info("The episode is done.")
                break
        
        step_idx += 1
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    # env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))
        
def setup_logger(example, example_result_dir):
    runtime_logger = logging.getLogger(f"desktopenv.example.{example['id']}")
    runtime_logger.setLevel(logging.DEBUG)
    runtime_logger.addHandler(logging.FileHandler(os.path.join(example_result_dir, "runtime.log")))
    return runtime_logger

def run_single_example_human(env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    env.reset(task_config=example)
    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    
    # Save initial screenshot
    with open(os.path.join(example_result_dir, "initial_state.png"), "wb") as _f:
        _f.write(obs['screenshot'])
    
    # Save trajectory information
    with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
        f.write(json.dumps({
            "instruction": instruction,
            "initial_state": "initial_state.png"
        }))
        f.write("\n")
    
    # Evaluate the result
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")



def run_single_example_openaicua(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    agent.reset(runtime_logger)
    env.reset(task_config=example)
    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    env.controller.start_recording()
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )

        done = not response.get('state_correct', False)

        for action in actions:
            # Capture the timestamp before executing the action
            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info, step_info = agent.step(action)

            if not done:
                if not response.get('state_correct', False):
                    done = True

            logger.info("Reward: %.2f", reward)
            logger.info("Done: %s", done)
            # Save screenshot and trajectory information
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_{action_timestamp}.png"),
                      "wb") as _f:
                _f.write(obs['screenshot'])

            # Remove pending checks if they exist which will cause issues with json serialization
            if action.get('pending_checks', None):
                del action['pending_checks']

            with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                f.write(json.dumps({
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}_{action_timestamp}.png"
                }))
                f.write("\n")
            if done:
                logger.info("The episode is done.")
                break
        step_idx += 1
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))

def run_single_example_opencua(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    agent.reset(runtime_logger)
    env.reset(task_config=example)
    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    env.controller.start_recording()
    while not done and step_idx < max_steps:
        response, actions, info_dict = agent.predict(instruction, obs)

        logger.info(f"Got Action: {actions}")
        # Breack if no actions
        if not actions or len(actions)==0 or actions[0]=="" or actions[0].lower().startswith("error"): 
            break

        for action in actions:
            # Capture the timestamp before executing the action
            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info(f"Action {action} executed, reward: {reward}, done: {done}")
            # Save screenshot and trajectory information
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_{action_timestamp}.png"),
                      "wb") as _f:
                _f.write(obs['screenshot'])

            with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                f.write(json.dumps({
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "response": response,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}_{action_timestamp}.png"
                }))
                f.write("\n")
            if done:
                logger.info("The episode is done.")
                break
        step_idx += 1

    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))

def run_single_example_glm4v(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    set_current_result_dir(example_result_dir)
    agent.reset()
    env.reset(task_config=example)
    time.sleep(30) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    # env.controller.start_recording()
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )
        # 理论上每一轮只会产生一个操作
        for action in actions:
            img_name = f"step_{step_idx + 1}.png"    
            with open(os.path.join(example_result_dir, img_name),
                      "wb") as _f:
                _f.write(obs['screenshot'])
            # if "coordinates" in response and response["coordinates"]:
            #     draw_coordinates(
            #         image_bytes=obs['screenshot'], 
            #         coordinates=response["coordinates"], 
            #         save_path=os.path.join(example_result_dir, img_name[:-4] + "_draw.png")
            #     )

            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)
            logger.info("Done: %s", done)

            with open(os.path.join(example_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "instruction": instruction,
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": response,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }))
                f.write("\n")
            with open(os.path.join(example_result_dir, f"traj_{step_idx+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": response,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }, f, indent=4, ensure_ascii=False)
            if done:
                logger.info("The episode is done.")
                time.sleep(60)
                break
        step_idx += 1
    result = float(env.evaluate())
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    # env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))
        
def run_single_example_autoglm(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    try:
        agent.reset(runtime_logger)
    except Exception as e:
        agent.reset()

    env.reset(task_config=example)
    
    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    # env.controller.start_recording()
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )
        for action in actions:
            # Capture the timestamp before executing the action
            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info("Reward: %.2f", reward)
            logger.info("Done: %s", done)
            # Save screenshot and trajectory information
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_{action_timestamp}.png"),
                      "wb") as _f:
                _f.write(obs['screenshot'])
            with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                f.write(json.dumps({
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "response": response,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}_{action_timestamp}.png"
                }))
                f.write("\n")
                
            if done:
                logger.info("The episode is done.")
                break
        
        # Invalid Action
        if not actions:
            obs = env._get_obs() # update observation
            
        step_idx += 1
    
    if not done: # not completed the task yet
        env.action_history.append('FAIL')
    
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    # env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))

def run_single_example_mano(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    agent.reset(runtime_logger)
    env.reset(task_config=example)
    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    env.controller.start_recording()
    
    with open(os.path.join(example_result_dir, f"step_0.png"),
      "wb") as _f:
        _f.write(obs['screenshot'])
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )
        if len(actions) > 1:
            if (("pyautogui.hotkey('shift')" in actions[0] or "pyautogui.hotkey('ctrl')" in actions[0]) 
                and "pyautogui.click" in actions[1]):
                hotkey_type = 'shift' if "shift" in actions[0] else 'ctrl'
                action = f"pyautogui.keyDown('{hotkey_type}')\n{actions[1]}\npyautogui.keyUp('{hotkey_type}')"
                actions = [action]  
                
        for action in actions:
            # Capture the timestamp before executing the action
            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info("Reward: %.2f", reward)
            logger.info("Done: %s", done)
            # Save screenshot and trajectory information
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_{action_timestamp}.png"),
                      "wb") as _f:
                _f.write(obs['screenshot'])
            with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                f.write(json.dumps({
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}_{action_timestamp}.png",
                    "response":response
                }))
                f.write("\n")
            if done:
                logger.info("The episode is done.")
                break
        step_idx += 1
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))
    
def run_single_example_uipath(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    runtime_logger = setup_logger(example, example_result_dir)
    try:
        agent.reset(runtime_logger)
    except Exception as e:
        agent.reset()

    env.reset(task_config=example)

    time.sleep(60) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    env.controller.start_recording()
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs,
            args,
            step_idx
        )
        for action in actions:
            # Capture the timestamp before executing the action
            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info("Reward: %.2f", reward)
            logger.info("Done: %s", done)
            # Save screenshot and trajectory information
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_{action_timestamp}.png"),
                      "wb") as _f:
                _f.write(obs['screenshot'])
            with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                f.write(json.dumps({
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "response": response,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}_{action_timestamp}.png"
                }))
                f.write("\n")
            if done:
                logger.info("The episode is done.")
                break
        step_idx += 1
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))


def run_single_example_claude(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    set_current_result_dir(example_result_dir)
    
    agent.reset()
    env.reset(task_config=example)
    time.sleep(30) # Wait for the environment to be ready
    obs = env._get_obs() # Get the initial observation
    done = False
    step_idx = 0
    # env.controller.start_recording()
    start_time = time.time()

    while not done and step_idx < max_steps:
        reasonings, actions = agent.predict(
            instruction,
            obs
        )
        
        # 理论上每一轮只会产生一个操作
        for action in actions:
            # Save screenshot and trajectory information
            
            img_name = f"step_{step_idx + 1}.png"
                
            with open(os.path.join(example_result_dir, img_name),
                      "wb") as _f:
                _f.write(obs['screenshot'])
            
            # claude的不同点：action的返回形式不同于其他
            if "input" in action and "coordinate" in action['input']:
                draw_coordinates(
                    image_bytes=obs['screenshot'], 
                    coordinates=action['input']["coordinate"], 
                    save_path=os.path.join(example_result_dir, img_name[:-4] + "_draw.png")
                )

            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)
            logger.info("Done: %s", done)

            with open(os.path.join(example_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "instruction": instruction,
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": reasonings,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }))
                f.write("\n")
            with open(os.path.join(example_result_dir, f"traj_{step_idx+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": reasonings,
                    "done": done,
                    "info": info,
                    "screenshot_file": img_name
                }, f, indent=4, ensure_ascii=False)
            if done:
                logger.info("The episode is done.")
                time.sleep(60)
                break
        step_idx += 1
    end_time = time.time()
    result = float(env.evaluate())
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")

    with open(os.path.join(example_result_dir, "time.txt"), "w", encoding="utf-8") as f:
        f.write(f"{end_time-start_time:.2f}\n")
