from __future__ import annotations

import logging
import os
import subprocess
import time
import json
from typing import Callable, Any, Optional, Tuple
from typing import List, Dict, Union
from desktop_env.macos.controllers.env import MacOSEnv


import gymnasium as gym

logger = logging.getLogger("desktopenv.env")

def wait_for_ssh(env: MacOSEnv, max_wait: int = 500, interval: int = 5):
    total_waited = 0
    attempt = 1
    while total_waited < max_wait:
        try:
            logger.info(f"[SSH Attempt {attempt}] Trying to connect...")
            env.connect_ssh()
            transport = env.ssh_client.get_transport() if env.ssh_client else None
            if not transport or not transport.is_active():
                raise ConnectionError("SSH transport not active after connect()")
            logger.info("✅ SSH connected successfully.")
            time.sleep(15)
            return
        except Exception as e:
            logger.warning(f"[SSH Attempt {attempt}] Failed: {type(e).__name__}: {e}")
            time.sleep(interval)
            total_waited += interval
            attempt += 1
    raise TimeoutError(f"❌ SSH connection failed after waiting {max_wait} seconds.")

class PythonController:
    def __init__(self, macos_env: MacOSEnv):
        self.macos_env = macos_env
    def run_python_script(self, script: str):
        self.macos_env.execute_python_command(script)
    def run_bash_script(self, script: str, timeout: int = 30, working_dir: Optional[str] = None) -> Optional[Dict[str, Any]]:
        self.macos_env.run_command(script)


class DesktopEnv(gym.Env):
    def __init__(
        self
    ):
        self.macos_env = MacOSEnv()
        # 必要(不要更改命名,我在Agent运行时会访问 env.controller) PythonController 用于控制虚拟机执行命令
        self.controller = PythonController(self.macos_env)
        
        # 不必要，能想办法完成初始化即可
        self.setup_controller = None

    # 必要
    def _get_obs(self):
        
        # 只要返回 screenshot 就行, 其余字段可有可无
        return {
            "screenshot": self.macos_env.get_screenshot()
        }

    # 必要 重置环境 + 初始化任务
    def reset(self, task_config: Optional[Dict[str, Any]] = None, seed=None, options=None):
        self.macos_env._reset_env()
        wait_for_ssh(self.macos_env)
        self.macos_env.init_task(task_json_config=task_config)
        return

    # 必要
    def step(self, action, pause=0.5):
        
        # observation, reward, done, info = "必要", "没用", "必要", "没用"
        return self.macos_env.step(action, pause)
    
    # 必要
    def evaluate(self):
        return self.macos_env.evaluate_task()

    # 必要, 关闭并杀死docker
    def close(self):
        self.macos_env._close_env()
        return


