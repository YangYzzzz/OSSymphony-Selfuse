from __future__ import annotations

import logging
import os
import subprocess
import time
import json
from typing import Callable, Any, Optional, Tuple
from typing import List, Dict, Union


import gymnasium as gym

logger = logging.getLogger("desktopenv.env")


class DesktopEnv(gym.Env):
    def __init__(
        self
    ):
        
        # 必要(不要更改命名,我在Agent运行时会访问 env.controller) PythonController 用于控制虚拟机执行命令
        self.controller = PythonController(vm_ip="127.0.0.1", server_port=self.server_port)
        
        # 不必要，能想办法完成初始化即可
        self.setup_controller = SetupController(vm_ip="127.0.0.1", server_port=self.server_port, chromium_port=self.chromium_port, cache_dir=self.cache_dir_base)

    # 必要
    def _get_obs(self):
        # 只要返回 screenshot 就行, 其余字段可有可无
        return {
            "screenshot": "字节流类型图片"
        }

    # 必要 重置环境 + 初始化任务
    def reset(self, task_config: Optional[Dict[str, Any]] = None, seed=None, options=None):
        return

    # 必要
    def step(self, action, pause=0.5):
        observation, reward, done, info = "必要", "没用", "必要", "没用"
        return observation, reward, done, info
    
    # 必要
    def evaluate(self):
        score = 1
        return score

    # 必要, 关闭并杀死docker
    def close(self):
        return

