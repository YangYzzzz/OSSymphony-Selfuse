from __future__ import annotations
from typing import Any, Dict
import logging

logger = logging.getLogger("desktopenv.oscaliber.metrics")


def oscaliber_rule_based_metric(result: Any, expected: Any, options: Dict[str, Any] | None = None) -> float:
    """Rule-based 版本评估 metric 的骨架.

    - result/expected: 来自 file/terminal 等 getter 的结构化结果
    - options["oscaliber_meta"]: 在生成任务时注入的元数据, 包含
        - evaluation_type
        - evaluation_desc
        - condition
        - expected_result
        - complexity
        - estimated_steps
        - category

    返回值约定:
      - 1.0: 通过
      - 0.0: 未通过
      - 可扩展为 [0,1] 区间的部分得分
    """
    options = options or {}
    meta = options.get("oscaliber_meta", {})
    logger.debug("[oscaliber_rule_based_metric] meta=%s, result=%s, expected=%s", meta, result, expected)

    # TODO: 在这里根据 condition / expected_result + result/expected 实现真正的规则判定
    # 目前作为骨架, 统一返回 0.0
    return 0.0


def oscaliber_vlm_based_metric(result: Any, expected: Any, options: Dict[str, Any] | None = None) -> float:
    """VLM-based 版本评估 metric 的骨架.

    - result: 通常是当前或最终截图, 来自 VLM getter
    - expected: 可能是期望界面的说明或参考图
    - options["oscaliber_meta"]: 评估需要的高层语义信息 (evaluation_desc 等)

    在真正实现时, 一般会把 result/expected/meta 打包送给外部的 VLM 模型进行判定;
    这里仅保留接口和日志.
    """
    options = options or {}
    meta = options.get("oscaliber_meta", {})
    logger.debug("[oscaliber_vlm_based_metric] meta=%s, result_type=%s, expected_type=%s", meta, type(result), type(expected))

    # TODO: 在这里接入图像 VLM 评估逻辑
    return 0.0


def oscaliber_hard_fail_metric(result: Any, expected: Any, options: Dict[str, Any] | None = None) -> float:
    """永远返回 0.0 的占位 metric, 用于标记尚未实现的评估."""
    logger.warning("[oscaliber_hard_fail_metric] called - not implemented")
    return 0.0
