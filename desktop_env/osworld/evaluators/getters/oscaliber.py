from __future__ import annotations
from typing import Any, Dict
import logging

import gymnasium as gym

logger = logging.getLogger("desktopenv.oscaliber.getters")


def get_oscaliber_rule_based_result(env: gym.Env, config: Dict[str, Any]) -> Any:
    """获取用于 rule-based 判定的结果数据的骨架.

    典型可以包括:
      - 某个路径下文件的内容或存在性
      - 终端输出

    具体逻辑可根据 config["options"] 中的信息实现, 这里先留空.
    """
    logger.debug("[get_oscaliber_rule_based_result] config=%s", config)
    # TODO: 从 env.controller 读取文件/终端等, 构造结构化结果
    return None


def get_oscaliber_rule_based_expected(env: gym.Env, config: Dict[str, Any]) -> Any:
    """获取 rule-based 的 expected 数据的骨架.

    可以直接返回 condition/expected_result, 或者从参考文件中读取期望内容.
    目前作为占位实现.
    """
    logger.debug("[get_oscaliber_rule_based_expected] config=%s", config)
    return None


def get_oscaliber_vlm_based_result(env: gym.Env, config: Dict[str, Any]) -> Any:
    """获取 VLM-based 评估所需的结果数据的骨架.

    默认返回当前观测中的 screenshot, 供后续 VLM 使用.
    """
    logger.debug("[get_oscaliber_vlm_based_result] config=%s", config)
    try:
        obs = env._get_obs()
        return obs.get("screenshot")
    except Exception as e:
        logger.warning("[get_oscaliber_vlm_based_result] failed to get screenshot: %s", e)
        return None


def get_oscaliber_vlm_based_expected(env: gym.Env, config: Dict[str, Any]) -> Any:
    """获取 VLM-based 评估的 expected 信息骨架.

    一般可以是自然语言描述 (evaluation_desc + expected_result),
    在真正实现中可由外部组合 meta 后再传入 VLM.
    这里先简单返回 None 作为占位.
    """
    logger.debug("[get_oscaliber_vlm_based_expected] config=%s", config)
    return None
