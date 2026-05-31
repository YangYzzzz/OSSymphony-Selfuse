# OSSymphony2 Instruction Generation Workflow

本文档描述新版 OSSymphony2 task generation workflow。目标是在保留现有 app graph 随机采样、真实 `desktop_env` reset/evaluate、动态 evaluator schema 的基础上，把“一次性生成完整任务”拆成可探索、可筛选、可验证、可修复、可积累经验的多阶段流程。

核心优先级：

1. 优先参考新版方案：随机采样 -> 探索 + 任务提议 -> 提议打分 -> 评估代码生成 -> 评估代码验证/修复 -> APP 动态记忆更新。
2. 当前 workflow 必须深度依赖 `desktop_env`，探索、reset、evaluate 都应以真实初始化环境为准。
3. 每个 agent 独立建类，最外层 workflow 只负责调度、状态流转、日志和失败恢复。
4. 每次 LLM / agent 调用都记录成本统计，包括调用次数、模型名、输入输出 token、耗时、成功/失败状态。

---

## Non-goals

- 不在当前 pipeline 中引入真实 task-solving agent rollout。
- 不要求验证 golden 状态一定正确，也不要求完成后 reward 一定为 1。
- 不重写 `DesktopEnv` 的核心接口。
- 不强制为每个 app 预先写静态 verifier；继续使用现有动态 evaluator 结构。
- 不把生成期的探索轨迹、打分详情、preflight 日志塞进最终 task JSON 的顶层字段。
- 不允许 VLM-only 任务进入最终集；最终任务必须至少有一个 rule-based evaluator，可以额外带 VLM judge。

---

## 总体阶段

```text
Stage 0  随机采样
Stage 1  Sandbox 探索 + 任务提议生成
Stage 2  任务提议打分与筛选
Stage 3  Evaluator 代码生成
Stage 4  Evaluator 验证、初态 0 检查、修复
Stage 5  Finalize task file + APP 动态记忆更新
```

关键变化：

- Stage 0 不再区分 `main_app`；所有 sampled apps 地位相同。
- Stage 0 只采样软件、支持文件类型、候选文件；不再生成固定任务初始化。
- Stage 1 的探索环境初始 `config` 为空，即不做任何任务初始化。
- Stage 1 由单个多轮视觉 agent 同时完成安全探索和 proposal 生成，不再把视觉轨迹压缩成 `visible_state` 后交给另一个 proposer。
- Stage 1 的 `done` 动作直接返回 proposal 列表，每个 proposal 必须包含 `instruction`、`config`、`related_apps`、`used_files`、`evaluation_requirements_text` 等完整提议字段。
- Stage 1 的奖励/评估字段只写自然语言检查要求，不生成 evaluator code。
- Stage 4 preflight 必须用 candidate/proposal 生成的最终 `config` reset，而不是 Stage 0 的固定初始化。

## 模型分工与 CLI 参数

`ossymphony2_task_generation.py` 使用无 `ig_` 前缀的 instruction-generation 参数：

```text
--provider
--model
--generator_model
--scorer_model
--base_url
--api_key
--temperature
--top_p
--max_tokens
```

模型分工：

- `generator_model`：用于 `ExplorationProposalAgent`、`EvaluatorSynthesisAgent`。
- `scorer_model`：用于 `ProposalCritiqueAgent`、`EvaluatorCritiqueAgent`。
- 未单独指定 `generator_model` 或 `scorer_model` 时，回退到 `model`。

---

## 代码模块

```text
workflow.py                    # InstructionGenerationWorkflow 调度入口
models.py                      # GenerationContext 等共享数据模型
constants.py                   # tool schema、getter 白名单、危险 import/call 列表等常量
prompts.py                     # prompt loading/cache
base_agent.py                  # WorkflowCostTracker、WorkflowLLMAgent
app_memory.py                  # AppMemoryStore
exploration_proposal_agent.py  # 多轮视觉探索 + proposal 生成 agent
proposal_critic_agent.py       # proposal 筛选 agent
evaluator_agents.py            # evaluator synthesis/critique agents
validators.py                  # static evaluator validation 与 preflight validation
```

---

## 跨阶段数据契约

### 共享运行对象

这些对象只在 Python runtime 中共享，不写入最终 task JSON：

```python
desktop_env: DesktopEnv
cost_tracker: WorkflowCostTracker
app_memory_store: AppMemoryStore
build_evaluator_fn: Callable[[dict], dict]
app_version_lookup: Callable[[str], str]
```

### Stage 0 输出：`GenerationContext`

```json
{
  "rollout_id": "uuid",
  "sampled_apps": ["libreoffice_calc", "vscode"],
  "app_file_support": {
    "libreoffice_calc": ["xlsx", "csv"],
    "vscode": ["txt", "py", "csv"]
  },
  "sampled_files": [
    {
      "path": "/home/user/Desktop/test_files/xlsx/budget.xlsx",
      "type": "xlsx",
      "supported_apps": ["libreoffice_calc"]
    }
  ],
  "app_tutorials": {
    "libreoffice_calc": "static tutorial markdown"
  },
  "app_memory": {
    "libreoffice_calc": {
      "covered_features": {},
      "known_good_verification_channels": [],
      "failure_patterns": [],
      "next_generation_bias": {},
      "recent_tasks": []
    }
  },
  "app_versions": {
    "libreoffice_calc": "LibreOffice Calc ..."
  },
  "app_open_commands": {
    "libreoffice_calc": [["libreoffice", "--calc"], ["libreoffice", "--calc", "PATH"]]
  },
  "initial_config": [],
  "observation": "desktop_env initial observation object",
  "setup_image": "bytes"
}
```

### Stage 1 输入与多轮上下文

`ExplorationProposalAgent.generate(context, env, target_count, feedback=None, screenshot_dir=None)` 维护一个真实多轮 `LMMAgent.messages`：

- 首轮 user message 包含 sampled apps/files、app tutorials、app memory、tool schema、requested proposal count 和初始截图。
- 每个安全探索动作后追加 assistant JSON、compact tool response 和新截图。
- 视觉轨迹保留在同一个 agent 的历史消息中，proposal 生成直接基于该轨迹完成。
- `traj.jsonl`、`traj_<step>.json`、`explore_step_*.png` 只作为 sidecar debug/复现日志，不作为跨 agent 的核心语义摘要。

### Stage 1 动作 schema

```json
{
  "actions": [
    {
      "tool": "open|click|scroll|done",
      "arguments": {},
      "purpose": "why this observation helps grounded task proposal generation"
    }
  ]
}
```

动作约束：

- `open` 只能打开 sampled app 和 sampled file，或打开 sampled app 的空窗口。
- `click` / `scroll` 只能用于非破坏性 UI 观察。
- `done` 结束探索并直接返回 proposals。
- 每轮只能返回一个原子 GUI 动作。
- 探索期间不能保存、编辑、删除、安装、提交表单、发送消息或访问不稳定网络资源。

### Stage 1 输出：`ExplorationProposalResult`

```json
{
  "proposals": [
    {
      "proposal_id": "p01",
      "instruction": "...",
      "config": [],
      "related_apps": ["libreoffice_calc"],
      "used_files": ["/home/user/Desktop/test_files/xlsx/budget.xlsx"],
      "category": "file_only",
      "complexity": "medium",
      "estimated_steps": 20,
      "target_features": ["formula", "formatting"],
      "success_criteria": ["Summary sheet contains ..."],
      "evaluation_requirements_text": ["Check cell B2 equals ...", "Check style/font ..."],
      "verification_plan_hint": {
        "preferred": "rule",
        "channels": ["vm_file", "vm_command_line"],
        "rationale": "The modified xlsx can be inspected with openpyxl."
      },
      "risk_notes": []
    }
  ],
  "generation_notes": [],
  "trajectory": {
    "rollout_id": "uuid",
    "log": "traj.jsonl"
  }
}
```

Stage 1 必须生成 exactly requested proposal count，即请求几个 proposal 就返回几个 proposal。若探索 budget 耗尽但模型未主动 `done`，workflow 会追加一次强制 `done` 请求；失败时返回空 proposals，由重试/筛选逻辑处理不足。

### Stage 2 输出：`ProposalSelectionResult`

```json
{
  "accepted": [
    {
      "proposal_id": "p01",
      "instruction": "...",
      "config": [],
      "related_apps": [],
      "used_files": [],
      "evaluation_requirements_text": []
    }
  ],
  "rejected": [
    {
      "proposal_id": "p03",
      "reason": "too_simple",
      "suggested_repair": "Combine content edit with verifiable formatting."
    }
  ],
  "coverage_summary": {
    "formula": 1,
    "cross_app": 1
  }
}
```

如果 accepted 不足，workflow 会把 rejected feedback 传回 `ExplorationProposalAgent` 再生成缺口数量的 proposals。

### Stage 3 输出：`TaskCandidate`

```json
{
  "instruction": "...",
  "config": [],
  "complexity": "medium",
  "category": "file_only",
  "related_apps": ["libreoffice_calc"],
  "used_files": ["/home/user/Desktop/test_files/xlsx/budget.xlsx"],
  "estimated_steps": 20,
  "feature_tags": ["formula"],
  "verification": {
    "need_rule_judge": true,
    "need_vlm_judge": false,
    "vlm_desc": "",
    "rule_items": [
      {
        "result_getter": {
          "type": "vm_file",
          "path": "/home/user/Desktop/test_files/xlsx/budget.xlsx",
          "dest": "budget.xlsx"
        },
        "expected_getter": {"type": "empty"},
        "code": "def call_rule_judge_1(result, expected, **options):\n    return 0.0"
      }
    ]
  }
}
```

### Stage 4 输出：`ValidationResult`

```json
{
  "passed": true,
  "static_validation": {
    "passed": true,
    "errors": [],
    "warnings": []
  },
  "preflight": {
    "passed": true,
    "init_rule_reward": 0.0,
    "details": []
  }
}
```

Stage 4 做两类检查：

1. Static evaluator validation：检查 getter 类型、路径、rule function 签名、危险 import/call、rule judge 存在性。
2. Preflight validation：用最终 candidate `config` reset，然后立刻 `env.evaluate()`，要求初态 reward 为 0。

失败时 `EvaluatorCritiqueAgent` 根据 failure payload 修复 candidate，最多重试 `max_repair_rounds` 轮。

### Stage 5 输出

每个通过 preflight 的 candidate 写成最终 task JSON：

```json
{
  "id": "uuid",
  "snapshot": "libreoffice_calc",
  "related_apps": ["libreoffice_calc"],
  "related_apps_version": ["LibreOffice Calc ..."],
  "instruction": "...",
  "config": [],
  "complexity": "medium",
  "estimated_steps": 20,
  "category": "file_only",
  "evaluator": {},
  "setup_image": "uuid.png",
  "launch_paths": ["/home/user/Desktop/test_files/xlsx/budget.xlsx"]
}
```

并写入 sidecar 文件：

- `agentworkflow_cost.jsonl`
- `agentworkflow_generation_log.jsonl`
- `traj.jsonl`
- `traj_<step>.json`
- `explore_step_*.png`

---

## 最终任务质量要求

- instruction 必须是目标导向的真实用户请求，而不是逐步教程。
- instruction 必须显式包含 evaluator-critical 约束：对象身份、源/目标、排序关系、数量、格式、范围、文件名、最终可观察状态。
- proposal 若读写文件，必须引用 sampled file 的具体路径，且 config 必须初始化对应 app/file state。
- evaluator 必须至少包含一个 rule-based verification anchor。
- rule check 应验证内容、结构、格式、元数据或可观察状态变化，不能只检查文件存在。
- 多 app 任务必须明确 source object、derived artifact、destination 和 final observable state 的完整关系链。
- 不生成 destructive、网络不稳定、主观视觉目标或单步 trivial 任务。

---

## APP 动态记忆

每个 app 的 memory 记录：

- 已覆盖 feature 与次数。
- 最近成功任务摘要。
- 已知可靠 verification channel。
- 失败模式与修复经验。
- 下次生成偏置，例如 undercovered/overcovered features。

Stage 1 和 Stage 2 使用 memory 降低重复任务概率；Stage 5 在成功或失败后更新 memory。
