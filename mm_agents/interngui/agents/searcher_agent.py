import requests
import logging
from functools import partial
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple
import datetime
from requests.auth import HTTPBasicAuth
from mm_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
from mm_agents.interngui.utils.common_utils import (
    call_llm_safe, 
    split_thinking_response, 
    draw_coordinates, 
    call_llm_formatted,    
    parse_code_from_string,
    split_thinking_response,
    create_pyautogui_code
)
from mm_agents.interngui.core.mllm import LMMAgent
from mm_agents.interngui.agents.grounder_agent import GrounderAgent
import os
import json
from mm_agents.interngui.utils.formatters import (
    SINGLE_ACTION_FORMATTER,
    CODE_VALID_FORMATTER,
)

from desktop_env.desktop_env import DesktopEnv

logger = logging.getLogger("desktopenv.searcher_agent")

# Agent action decorator
def searcher_agent_action(func):
    func.is_searcher_agent_action = True
    return func

# --- Abstract Base Class and Factory ---
class SearcherAgent:
    def __init__(self, engine_params: Dict):
        self.engine_params = engine_params
    
    @staticmethod
    def create(engine_params: Dict, search_env: DesktopEnv, grounder_agent: GrounderAgent, platform: str):
        searcher_type = engine_params.get("searcher_type", "vlm")
        if searcher_type == "vlm":
            return VLMSearcherAgent(engine_params=engine_params, search_env=search_env, grounder_agent=grounder_agent, platform=platform)
        elif searcher_type == "google_ai":
            return GoogleAISearcherAgent(engine_params=engine_params)
        elif searcher_type == "llm":
            return LLMSearcherAgent(engine_params=engine_params)
    
    def search(self, query: str, obs) -> str:
        """
        Args:
            query: Format like "How to xxxx?", must be a detailed subtask
            obs: Current screenshot, 目前不好说要不要加上
        """
        raise NotImplementedError("Subclasses must implement the 'search' method")
    
class VLMSearcherAgent(SearcherAgent):
    """
    需要启动一个全新的虚拟机，并将Chrome作为初始化条件
    """
    def __init__(self, engine_params: Dict, search_env: DesktopEnv, grounder_agent: GrounderAgent, platform: str):
        # 检索智能体父类
        SearcherAgent.__init__(self, engine_params=engine_params)

        self.grounder_agent = grounder_agent
        self.budget = engine_params.get("budget", 20)
        self.platform = platform
        self.max_trajectory_length = 8 # 这部分有待优化，searcher似乎不需要这么多截图?
        self.env: DesktopEnv = search_env

        self.result_dir = ""

        self.use_thinking = engine_params.get("model", "") in [
            "claude-opus-4-20250514",
            "claude-sonnet-4-20250514",
            "claude-3-7-sonnet-20250219",
            "claude-sonnet-4-5-20250929",
        ]

        # 复用OSWorld的初始化脚本，以进行Chrome的初始化, 直接运用谷歌搜索搜索query, query目前可由填充字段代替
        self.task_config = {
            "id": "searcher",
            "instruction": "searcher",
            "config": [
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
                            "GOOGLE_SEARCH_URL"    
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
            "proxy": True
        }
        self.tutorial_notes = []
        self.obs = None

    def reset(self, query):
        # 当调用search函数时, 创建新的智能体, 当第一次调用时再实例化环境, 但是每次都要reset
        # 重置智能体上下文
        self.tutorial_notes = []
        self.tutorial_or_hint = ""
        self.system_prompt = PROCEDURAL_MEMORY.construct_searcher_procedural_memory(
            agent_class=type(self)
        ).replace("CURRENT_OS", self.platform)
        self.searcher_agent = LMMAgent(
            engine_params=self.engine_params,
            system_prompt=self.system_prompt
        )
        # 启动Search环境, 内部逻辑为若已经实例化则直接返回, 交给下面的reset即可
        self.env.start()
        # 配置URL并初始化Search环境
        google_search_url = f"https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
        self.task_config["config"][2]["parameters"]["urls_to_open"][0] = google_search_url
        self.env.reset(task_config=self.task_config)

    def flush_messages(self):
        """Flush messages based on the model's context limits.

        This method ensures that the agent's message history does not exceed the maximum trajectory length.

        Side Effects:
            - Modifies the messages of generator, reflection, and bon_judge agents to fit within the context limits.
        """
        engine_type = self.engine_params.get("engine_type", "")

        # Flush strategy for long-context models: keep all text, only keep latest images
        if engine_type in ["anthropic", "openai", "gemini"]:
            max_images = self.max_trajectory_length
            for agent in [self.searcher_agent]:
                if agent is None:
                    continue
                # keep latest k images
                # @Yang: keep the first main agent image
                img_count = 0
                for i in range(len(agent.messages) - 1, 1, -1):
                    for j in range(len(agent.messages[i]["content"]) - 1, -1, -1):
                        if "image" in agent.messages[i]["content"][j].get("type", ""):
                            img_count += 1
                            if img_count > max_images:
                                del agent.messages[i]["content"][j]

        # Flush strategy for non-long-context models: drop full turns
        else:
            # generator msgs are alternating [user, assistant], so 2 per round
            if len(self.searcher_agent.messages) > 2 * self.max_trajectory_length + 1:
                self.searcher_agent.messages.pop(1)
                self.searcher_agent.messages.pop(1)

    def assign_screenshot(self, obs):
        self.obs = obs

    def _get_search_time(self) -> int:
        """
        查找 self.result_dir 文件夹下的 search_{search_time} 文件夹, 返回当前最大的 search_time + 1。
        """
        search_times: list[int] = []
        
        for item_name in os.listdir(self.result_dir):
            full_path = os.path.join(self.result_dir, item_name)
            
            if os.path.isdir(full_path) and item_name.startswith("search_"):
                try:
                    time_val = int(item_name.split('_', 1)[1])
                    search_times.append(time_val)
                except (ValueError, IndexError):
                    continue

        if not search_times:
            return 1
        
        return max(search_times) + 1
        
    # TODO: @Yang 结合主Agent与Coder Agent实现
    def search(self, query: str, main_obs):
        # search 触发时再创建虚拟机，以防浪费资源
        self.reset(query=query) # 重置
        search_result_dir = os.path.join(self.result_dir, f"search_{self._get_search_time()}")
        os.makedirs(search_result_dir, exist_ok=True)

        obs = self.env._get_obs() # Get the initial observation
        step_idx = 0
        # 系统提示词替换
        self.searcher_agent.add_system_prompt(system_prompt=self.system_prompt.replace("QUERY", query))
        initial_state_text = (
            "This screenshot shows the current visual context of the main GUI Agent you are assisting. "
            "Use this image to understand the application, the current view, and the overall environment. "
            "Your primary goal is to find a tutorial that is highly relevant and well-aligned with this specific context, "
            "ensuring the instructions you find are applicable to what the main agent is currently seeing."
        )
        self.searcher_agent.add_message(
            text_content=initial_state_text, 
            image_content=main_obs["screenshot"], 
            role="user"
        )
        execution_history = []
        completion_reason = ""
        final_answer = ""

        while step_idx < self.budget:
            # 动态更新 system_prompt
            tutorial_notes_str = ""
            if len(self.tutorial_notes) > 0:
                for i, note in enumerate(self.tutorial_notes, 1):
                    tutorial_notes_str += f"Tutorial Note {i}: {note}\n\n"

            if step_idx == self.budget - 1:
                # 最后一舞
                self.system_prompt = PROCEDURAL_MEMORY.construct_searcher_eager_mode_procedural_memory(
                    agent_class=type(self)
                ).replace("CURRENT_OS", self.platform).replace("QUERY", query)
            
            system_prompt = self.system_prompt.replace("TUTORIAL_PLACEHOLDER", tutorial_notes_str)
            self.searcher_agent.add_system_prompt(system_prompt=system_prompt)

            # 开始一轮新的对话
            self.assign_screenshot(obs=obs)
            generator_message = ""

            self.searcher_agent.add_message(
                generator_message, image_content=obs["screenshot"], role="user"
            )
            format_checkers = [
                partial(CODE_VALID_FORMATTER, self, obs),
            ]

            # 生成动作
            plan = call_llm_formatted(
                self.searcher_agent,
                format_checkers,
                temperature=self.engine_params.get("temperture", 0.1),
                use_thinking=self.use_thinking,
            )

            self.searcher_agent.add_message(plan, role="assistant")
            execution_history.append(plan)
            logger.info("SEARCHER PLAN:\n %s", plan)

            plan_code = parse_code_from_string(plan)
            try:
                assert plan_code, "Plan code should not be empty"
                # 此时的exec_code e.g. import pyautogui; pyautogui.click(1, 2);
                exec_code, coords = create_pyautogui_code(self, plan_code, obs)
            except Exception as e:
                logger.error(
                    f"Could not evaluate the following plan code:\n{plan_code}\nError: {e}"
                )
                exec_code = self.wait(
                    1.333
                )  # Skip a turn if the code cannot be evaluated

            self.flush_messages()

            # 执行动作
            action = exec_code
            logger.info("Step %d: %s", step_idx + 1, action)

            # Save screenshot and trajectory information
            with open(os.path.join(search_result_dir, f"step_{step_idx + 1}.png"),
                    "wb") as _f:
                _f.write(obs['screenshot'])

            if coords is not None and isinstance(coords, list):
                draw_coordinates(
                    image_bytes=obs['screenshot'], 
                    coordinates=coords, 
                    save_path=os.path.join(search_result_dir, f"step_{step_idx + 1}_draw.png")
                )
                            
            with open(os.path.join(search_result_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "query": query,
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": {
                        "plan": plan,
                        "plan_code": plan_code,
                        "coordinates": coords
                    },
                    "screenshot_file": f"step_{step_idx + 1}.png"
                }, ensure_ascii=False))
                f.write("\n")
                
            with open(os.path.join(search_result_dir, f"traj_{step_idx+1}.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "query": query,
                    "step_num": step_idx + 1,
                    "action": action,
                    "response": {
                        "plan": plan,
                        "plan_code": plan_code,
                        "coordinates": coords
                    },
                    "screenshot_file": f"step_{step_idx + 1}.png"
                }, f, indent=4, ensure_ascii=False)

            if exec_code in ["DONE", "FAIL"]:
                # 中断循环
                completion_reason = exec_code
                final_answer = self.tutorial_or_hint
                break
            else:
                obs, _, _, _ = self.env.step(action, 5)

            step_idx += 1

        if completion_reason == "":
            completion_reason = "BUDGET_EXHAUSTED"
            final_answer = "Sorry, can't get the useful tutorial about the GUI task you provided."

        return {
            "query": query,
            "completion_reason": completion_reason,
            "tutorial_notes": self.tutorial_notes,
            "execution_history": execution_history,
            "steps_executed": step_idx,
            "budget": self.budget,
            "final_answer": final_answer,
        }
    
    @searcher_agent_action
    def click(
        self,
        element_description: str,
        num_clicks: int = 1,
        button_type: str = "left",
    ):
        """Click on the element
        Args:
            element_description:str, a detailed descriptions of which element to click on. This description should be at least a full sentence.
            num_clicks:int, number of times to click the element
            button_type:str, which mouse button to press can be "left", "middle", or "right"
        """
        coords1 = self.grounder_agent.generate_coords(element_description, self.obs)
        x, y = self.grounder_agent.resize_coordinates(coords1)
        command = "import pyautogui; "
        command += f"""import pyautogui; pyautogui.click({x}, {y}, clicks={num_clicks}, button={repr(button_type)}); """

        # Return pyautoguicode to click on the element
        return (command, [x, y])
    
    @searcher_agent_action
    def type(
        self,
        element_description: Optional[str] = None,
        text: str = "",
        overwrite: bool = True,
        enter: bool = False
    ):
        """Type text/unicode into a specific element
        Args:
            element_description:str, a detailed description of which element to enter text in. This description should be at least a full sentence.
            text:str, the text to type
            overwrite:bool, Default is True, assign it to False if the text should not overwrite the existing text. Using this argument clears all text in an element.
            enter:bool, Assign it to True if the enter key should be pressed after typing the text, otherwise assign it to False.
        """
        commands = [
            "import pyautogui",
            "import pyperclip",
            "import subprocess",
            # 注意：这个安装命令每次执行都会尝试运行，可能效率不高且需要sudo权限
            "subprocess.run('echo \"password\" | sudo -S apt-get install -y xclip xsel', shell=True, check=True, env={\"http_proxy\": \"http://10.1.8.5:23128\", \"https_proxy\": \"http://10.1.8.5:23128\"})",
            # 存储原始剪贴板
            "original_clipboard = pyperclip.paste()"
        ]
        
        click_coords = None
        if element_description is not None:
            coords1 = self.grounder_agent.generate_coords(element_description, self.obs)
            x, y = self.grounder_agent.resize_coordinates(coords1)
            commands.append(f"pyautogui.click({x}, {y})")
            click_coords = [x, y]

        if overwrite:
            # 使用 repr() 来确保 'command' 或 'ctrl' 字符串被正确引用
            hotkey_mod = repr('command' if self.platform == 'darwin' else 'ctrl')
            commands.append(f"pyautogui.hotkey({hotkey_mod}, 'a')")
            commands.append("pyautogui.press('backspace')")


        # 使用剪贴板方法进行输入
        # repr(text) 会正确处理文本中的引号和特殊字符
        commands.append(f"pyperclip.copy({repr(text)})")
        
        if self.platform == 'darwin':
            hotkey_mod = repr('command' if self.platform == 'darwin' else 'ctrl')
            commands.append(f"pyautogui.hotkey({hotkey_mod}, 'v')")
        else:
            # Linux 终端的粘贴
            commands.append("pyautogui.hotkey('shift', 'ctrl', 'v')")

        # 恢复原始剪贴板
        commands.append("pyperclip.copy(original_clipboard)")
        
        if enter:
            commands.append("pyautogui.press('enter')")

        # 最后，将所有命令用分号和空格连接成一个最终的字符串
        final_command = "; ".join(commands)

        if click_coords is not None:
            return (final_command, click_coords)
        else:
            return final_command

    @searcher_agent_action
    def scroll(self, element_description: str, clicks: int, shift: bool = False):
        """Scroll the element in the specified direction
        Args:
            element_description:str, a very detailed description of which element to enter scroll in. This description should be at least a full sentence.
            clicks:int, the number of clicks to scroll can be positive (up) or negative (down).
            shift:bool, whether to use shift+scroll for horizontal scrolling
        """
        coords1 = self.grounder_agent.generate_coords(element_description, self.obs)
        x, y = self.grounder_agent.resize_coordinates(coords1)

        if shift:
            return (f"import pyautogui; import time; pyautogui.moveTo({x}, {y}); time.sleep(0.5); pyautogui.hscroll({clicks})", [x, y])
        else:
            return (f"import pyautogui; import time; pyautogui.moveTo({x}, {y}); time.sleep(0.5); pyautogui.vscroll({clicks})", [x, y])

    @searcher_agent_action
    def hotkey(self, keys: List):
        """Press a hotkey combination (can press a single key as well)
        Args:
            keys:List the keys to press in combination in a list format (e.g. ['ctrl', 'c'], ['enter'])
        """
        # add quotes around the keys
        keys = [f"'{key}'" for key in keys]
        return f"import pyautogui; pyautogui.hotkey({', '.join(keys)})"

    @searcher_agent_action
    def save_to_tutorial_notes(self, text: str):
        """Save high quality and useful information to a long-term knowledge bank for reuse during this search task.
            text:str, the text to save to the tutorial notes
        """
        self.tutorial_notes.append(text)
        return """WAIT"""
    
    @searcher_agent_action
    def wait(self, time: float):
        """Wait for a specified amount of time
        Args:
            time:float the amount of time to wait in seconds
        """
        return f"""import time; time.sleep({time})"""

    @searcher_agent_action
    def done(
        self,
        tutorial: str
    ):
        """End the current task with a success. Use this when you believe the entire task has been fully completed.
        Args:
            tutorial:str, A detailed, step-by-step tutorial compiled from the search results to be passed to the main agent.
        """
        self.tutorial_or_hint = tutorial
        return """DONE"""

    @searcher_agent_action
    def fail(
        self,
        hint: str
    ):
        """End the current task with a failure. Use this when you believe the entire task is impossible to complete.
        Args:
            hint:str, A hint or reason explaining why the search failed, or what kind of information was missing.
        """
        self.tutorial_or_hint = hint
        return """FAIL"""
        

# TODO: @Yang 后续完成
class GoogleAISearcherAgent(SearcherAgent):
    def __init__(self, engine_params: Dict):
        pass

    def search(self):
        pass

class LLMSearcherAgent(SearcherAgent):
    def __init__(self, engine_params: Dict):
        pass

    def search(self):
        pass



if __name__=="__main__":
    query = input("Query: ")
    search_env = DesktopEnv(
        path_to_vm="/nvme/yangbowen/osworld/docker_vm_data/Ubuntu.qcow2",
        action_space="pyautogui",
        provider_name="docker", # 对应 --provider_name "docker"
        region="us-east-1", # 对应 --region "us-east-1"
        snapshot_name="", # 命令行中未提供 snapshot_name，假设为空字符串
        screen_size=(1920, 1080), # 对应 --grounding_width 和 --grounding_height
        headless=True, # 对应 --headless 标志
        os_type="Ubuntu",
        require_a11y_tree="screenshot"
        in ["a11y_tree", "screenshot_a11y_tree", "som"], # 结果为 False
        enable_proxy=True,
        client_password="", # 命令行中未提供 client_password，getattr 返回默认值 ""
    )


    # --- 2. 构建 Grounder 引擎参数 ---
    engine_params_for_grounder = {
        "engine_type": "openai", # 对应 --grounder_provider
        "model": "ui-tars-1.5-7b", # 对应 --grounder_model
        "base_url": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-65pfw-1176830-worker-0.yangbowen/8000/v1", # 对应 --grounder_url
        "api_key": "none", # 对应 --grounder_api_key
        "grounding_width": 1920, # 对应 --grounding_width
        "grounding_height": 1080, # 对应 --grounding_height
        "grounding_smart_resize": True # 对应 --grounding_smart_resize
    }
  
    engine_params_for_searcher = {
        "engine_type": "openai", # 对应 --searcher_provider
        "model": "gpt-5-mini", # 对应 --searcher_model
        "base_url": "https://api.boyuerichdata.opensphereai.com/v1", # 对应 --searcher_url
        "api_key": "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D", # 对应 --searcher_api_key
        "temperature": 0.1, # 对应 --searcher_temperature
        "budget": 20, # 对应 --searcher_budget
        "type": "vlm", # 对应 --searcher_type
        "engine_params_for_grounder": engine_params_for_grounder, # 嵌套上面已定义的 grounder 参数
    }

    searcher_agent = SearcherAgent.create(engine_params=engine_params_for_searcher, search_env=search_env)
    assert isinstance(searcher_agent, VLMSearcherAgent)
    result_dir = f"/nvme/yangbowen/yangbowen/OSWorld/test/searcher_{datetime.time()}"
    searcher_agent.result_dir = result_dir
    # query = "How to make the background of image transparent in GIMP?"

    result = searcher_agent.search(query=query)
    with open(result_dir, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    print(result)