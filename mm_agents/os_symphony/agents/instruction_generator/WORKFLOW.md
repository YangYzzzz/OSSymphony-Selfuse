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
- 不把生成期的探索摘要、打分详情、preflight 日志塞进最终 task JSON 的顶层字段。
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
- Stage 1 的探索环境初始 `config` 为空，即不做任何初始化。
- Stage 1 proposal 必须生成 `instruction` 和该 proposal 自己的 `config`。
- Stage 1 的奖励/评估字段只写自然语言检查要求，不生成 evaluator code。
- Stage 4 preflight 必须用 candidate/proposal 生成的最终 `config` reset，而不是 Stage 0 的固定初始化。

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
    },
    {
      "path": "/home/user/Desktop/test_files/csv/sales.csv",
      "type": "csv",
      "supported_apps": ["libreoffice_calc", "vscode"]
    }
  ],
  "app_tutorials": {
    "libreoffice_calc": "static tutorial markdown",
    "vscode": "static tutorial markdown"
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
    "libreoffice_calc": "LibreOffice Calc ...",
    "vscode": "VS Code ..."
  },
  "app_open_commands": {
    "libreoffice_calc": [["libreoffice", "--calc"], ["libreoffice", "--calc", "PATH"]]
  },
  "initial_config": [],
  "observation": "desktop_env initial observation object",
  "setup_image": "bytes"
}
```

字段含义：

| 字段 | 阶段来源 | 后续用途 |
|---|---|---|
| `rollout_id` | Stage 0 | sidecar log、debug、无 app fallback key |
| `sampled_apps` | Stage 0 | Stage 1 prompt、Stage 2 筛选、Stage 5 memory update |
| `app_file_support` | Stage 0 | 明确 app 与可加载文件类型对应关系，例如 `libreoffice_calc -> xlsx` |
| `sampled_files` | Stage 0 | Stage 1 探索、proposal `used_files`、最终 `launch_paths` |
| `sampled_files[].path` | Stage 0 | 允许 `open(app, path)` 打开的具体文件路径 |
| `sampled_files[].type` | Stage 0 | evaluator channel hint，例如 `vm_file:xlsx` |
| `sampled_files[].supported_apps` | Stage 0 | 提示模型哪个 app 能打开哪个文件 |
| `app_tutorials` | Stage 0 | Stage 1/3 prompt 静态能力说明 |
| `app_memory` | Stage 0/5 | Stage 1/2 降重和偏置；Stage 5 更新 |
| `app_versions` | Stage 0 | final `related_apps_version` 和提示 |
| `app_open_commands` | Stage 0 | Stage 1 `open` action 内部转为 bash command |
| `initial_config` | Stage 0 | 固定为空；用于探索后 reset 到空初态 |
| `observation` | Stage 0 | 初态观测 |
| `setup_image` | Stage 0 | Stage 1/2/3 image prompt 和最终 `setup_image` 文件 |

### Stage 1 输出：`ExplorationAndProposalResult`

```json
{
  "exploration_summary": {
    "visible_state": "Empty desktop or opened sampled file state summary.",
    "opened_files": [
      {
        "path": "/home/user/Desktop/test_files/xlsx/budget.xlsx",
        "app": "libreoffice_calc",
        "type": "xlsx",
        "summary": "Workbook has sheets Budget and Summary."
      }
    ],
    "file_inventory": [
      {
        "path": "/home/user/Desktop/test_files/xlsx/budget.xlsx",
        "type": "xlsx",
        "supported_apps": ["libreoffice_calc"],
        "exists": true,
        "size": 20480
      }
    ],
    "app_affordances_seen": ["spreadsheet grid", "sheet tabs", "formula bar"],
    "safe_verification_channels": ["vm_file:xlsx", "vm_command_line"],
    "constraints": ["Only sampled files may be opened during exploration"],
    "tool_results": []
  },
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
  ]
}
```

Stage 1 必须生成 exactly requested proposal count，即请求几个 proposal 就返回几个 proposal。

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
    "init_rule_reward": 0.0,
    "passed": true,
    "details": []
  },
  "repair_history": []
}
```

### Stage 5 输出：final task JSON

最终写盘格式保持现有任务格式，不把生成期字段塞入顶层：

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
  "setup_image": "image/<uuid>.png",
  "launch_paths": ["/home/user/Desktop/test_files/xlsx/budget.xlsx"]
}
```

---

## Stage 0: 随机采样

### 目标

随机选择多个软件和多个文件，构建一轮 rollout 的基础上下文。Stage 0 只负责采样和收集提示信息，不负责生成任务初始化。

### 软件采样

输入超参数：

```python
max_apps_per_group: int = n
rollout_app_list: list[str] | None
```

采样流程：

1. 从 `rollout_app_list` 或 `app_config.json` 全量 app 中得到 `available_apps`。
2. 随机采样 `m`，其中 `1 <= m <= n`。
3. 通过 `APP_GRAPH` 从一个随机起点扩展到 `m` 个 app。
4. 如果图邻居不足，可以从剩余 `available_apps` 中补充。
5. 输出 `sampled_apps: list[str]`。

约束：

- 不再产生 `main_app`。
- 不再产生 `apps_for_group` 这种带主从含义的字段。
- 每个 sampled app 地位相同。

### 文件采样

输入：

```python
sampled_apps: list[str]
app_file_support: dict[str, list[str]]
```

采样流程：

1. 令 `m = len(sampled_apps)`。
2. 随机采样文件数 `k`，其中 `k in [0, m + 1]`。
3. `k == 0` 表示本轮允许生成 no-file task。
4. `k == m + 1` 用于支持“单个 APP 操作多个文件”这类任务。
5. 从 `sampled_apps` 支持/可打开的文件类型并集中构造候选文件池。
6. 从候选文件池随机抽取最多 `k` 个具体文件。
7. 如果某些 app/type 没有实际 `PATH` 文件，最终 `len(sampled_files)` 可以小于 `k`。

输出字段：

```python
app_file_support: dict[str, list[str]]
sampled_files: list[dict]
```

其中 `sampled_files[]` 的字段固定为：

```json
{
  "path": "/home/user/Desktop/test_files/xlsx/example.xlsx",
  "type": "xlsx",
  "supported_apps": ["libreoffice_calc", "wps_et"]
}
```

### 环境初始化

Stage 0 的环境初始化状态为空：

```python
initial_config = []
desktop_env.reset(task_config={
    "config": initial_config,
    "id": "init_id",
    "instruction": "init_instruction"
})
```

Stage 0 不再调用旧版 `_generate_config()` 来决定某个 main app 的启动方式、文件路径或 golden path。

---

## Stage 1: Sandbox 探索 + 任务提议

### 目标

给定 Stage 0 采样到的软件、文件路径、APP 教程、APP 动态记忆，在空初始化环境中做最多 10 步探索，然后生成多个任务提议。

输入字段：

```python
sampled_apps
app_file_support
sampled_files
app_tutorials
app_memory
app_versions
app_open_commands
initial_config
setup_image
```

### 探索动作

探索 agent 只允许三个动作，使用 OpenAI-format `tool_schema`：

```json
[
  {
    "type": "function",
    "function": {
      "name": "open",
      "parameters": {
        "type": "object",
        "properties": {
          "app": {"type": "string"},
          "path": {"type": "string"},
          "purpose": {"type": "string"}
        },
        "required": ["app"]
      }
    }
  },
  {"type": "function", "function": {"name": "click"}},
  {"type": "function", "function": {"name": "scroll"}}
]
```

动作语义：

1. `open(app, path)`
   - `app` 必须来自 `sampled_apps`。
   - `path` 必须来自 `sampled_files[].path`，或为空表示打开空 app。
   - 内部通过 `desktop_env.controller.run_bash_script(...)` 执行对应 app command。
2. `click(x, y)`
   - 只用于非破坏性 UI 观察。
   - 禁止点击保存、导出、删除、确认、系统设置、发送、安装、运行脚本等会改变持久状态的控件。
3. `scroll(amount, x=None, y=None)`
   - 只用于观察更多内容。

探索限制：

- 最多 `max_exploration_steps = 10`。
- 不修改文件内容。
- 不保存、不导出、不改变 app setting。
- 不访问不稳定网络资源。
- 探索后的环境不得直接用于 Stage 4 preflight；进入 Stage 2/3/4 前必须 reset 到空初态或 candidate config 初态。

### Proposal schema

每个 proposal 必须包含：

```json
{
  "proposal_id": "p01",
  "instruction": "xxxxx",
  "config": [],
  "related_apps": ["libreoffice_calc"],
  "used_files": ["/home/user/Desktop/test_files/xlsx/example.xlsx"],
  "category": "file_only | app_only | mixed",
  "complexity": "simple | medium | complex",
  "estimated_steps": 20,
  "target_features": ["formula", "formatting"],
  "success_criteria": ["..."],
  "evaluation_requirements_text": ["..."],
  "verification_plan_hint": {
    "preferred": "rule | hybrid",
    "channels": ["vm_file", "vm_command_line"],
    "rationale": "..."
  },
  "risk_notes": []
}
```

字段要求：

- `instruction`：用户可见任务指令，必须满足旧版本所有生成限制：自然、清晰、非破坏性、非单步 trivial、不是 benchmark 描述、不依赖主观视觉判断、目标可验证。
- `config`：该 proposal 自己的初始化配置，由模型自由选择。可以打开某个 app、复制某个文件、打开某个文件、或保持空。不同 proposal 可以有不同 `config`。
- `related_apps`：只列该 proposal 实际需要的软件；不得假设主 APP。
- `used_files`：只列该 proposal 实际使用的 Stage 0 sampled file path。
- `evaluation_requirements_text`：只写自然语言，不写 code；必须非常细粒度，足够 Stage 3 evaluator agent 生成完备 rule function。

文件使用策略：

- 如果 `sampled_files` 非空，应强烈鼓励模型尽可能生成有文件特色的任务。
- Proposal 不需要强制使用全部 sampled files，但应优先利用已准备文件，避免文件采样浪费。
- 如果 proposal 使用文件，必须在 `used_files` 中列出具体路径，并在 `config` 中体现初始化方式。

---

## Stage 2: 任务提议打分与筛选

### 目标

对 Stage 1 proposals 进行多维度打分，筛掉不可执行、不可验证、过于简单或重复的任务。

### 输入字段

```python
GenerationContext
exploration_summary
proposals
app_memory
```

### 打分维度

| Axis | Accept target | Reject reason examples |
|---|---:|---|
| specificity | high | 缺少具体文件、对象、输出位置、数值、格式 |
| realism | high | 像 benchmark 指令，不像真实用户需求 |
| complexity | medium/complex | 单步打开、只输入一句话、只保存 |
| verifiability | high | 结果不可观察、只能主观判断 |
| data fit | high | 没使用 sampled file，或假设不存在文件内容 |
| diversity | high | 与本轮或历史 memory 功能重复 |
| non-destructiveness | required | 删除文件、改系统设置、不可逆操作 |
| rule anchor | required | 没有稳定 rule-based 检查点 |
| config quality | required | proposal 缺少任务专属初始化或初始化与任务不匹配 |

输出字段：

```python
accepted: list[proposal]
rejected: list[dict]
coverage_summary: dict[str, int]
```

如果 accepted 数量不足：

1. 将 rejected reasons 和 suggested repairs 反馈给 Stage 1。
2. 保留当前 exploration summary。
3. 重新生成缺口数量的 proposals。
4. 最多重试 `max_proposal_regen_rounds` 次。
5. 仍不足则本 rollout 可部分成功或失败，并把可复用失败写入 app memory。

---

## Stage 3: Evaluator 代码生成

### 目标

只对 Stage 2 通过的 proposal 生成完整 task candidate 和 evaluator code。

### 输入字段

```python
accepted_proposal
GenerationContext
exploration_summary
app_tutorials
app_memory
```

### 复用当前 evaluator schema

保持现有动态 evaluator 结构：

```python
need_rule_judge: bool
need_vlm_judge: bool
vlm_desc: str
rule_items: list[dict]
```

每个 `rule_item`：

```json
{
  "result_getter": {},
  "expected_getter": {},
  "code": "def call_rule_judge_1(result, expected, **options):\n    ..."
}
```

生成要求：

- 必须使用 proposal 的 `evaluation_requirements_text` 作为 evaluator 覆盖依据。
- 每个最终任务必须至少有一个 rule item。
- 可以同时使用 VLM judge，但 VLM 只能作为补充，不可作为唯一判据。
- evaluator 不应只检查文件存在；必须检查内容、结构、格式、metadata 或可观察状态变化。
- getter path 必须指向 VM 内真实绝对路径。
- `vm_command_line.command` 必须是 list，不允许字符串 shell。
- code 必须定义 `call_rule_judge_*` 函数。
- code 不允许写文件、删文件、访问网络、启动 GUI、调用危险系统命令。

---

## Stage 4: Evaluator 验证、初态 0 检查、修复

### 目标

对 Stage 3 的 task candidate 做静态验证和真实初始化环境 preflight。任一环节失败则进入有限 repair loop。

### 静态验证

检查：

1. JSON 可解析。
2. candidate 必填字段存在：`instruction`、`config`、`related_apps`、`verification`。
3. `need_rule_judge` 必须为 true，且 `rule_items` 非空。
4. 每个 rule item 的 Python code 可 `ast.parse`。
5. 函数名存在且以 `call_rule_judge_` 开头。
6. 函数签名兼容 `(result, expected, **options)`。
7. getter 类型只允许 `vm_file`、`vm_command_line`、`empty`。
8. `vm_file.path` 必须是 VM 内绝对路径。
9. `vm_command_line.command` 必须是 list。
10. code 中不允许危险操作：`subprocess`、`os.system`、`shutil.rmtree`、网络访问、写文件、删除文件等。
11. 不允许 evaluator 只检查文件存在。

### 初态 0 preflight validation

对每个 candidate，在真实 sandbox 初始状态下直接运行 evaluator：

```text
reward(init_state, task_evaluator) == 0
```

执行步骤：

1. 使用 candidate 最终 task JSON 中的 `config` reset `desktop_env`。
2. 确保不复用 Stage 1 探索后的状态。
3. 不执行任何完成任务的 agent action。
4. 注入 candidate evaluator。
5. 调用 `env.evaluate()`。
6. 记录总 reward、异常信息和 failure type。

通过标准：

- rule-only：`preflight_reward == 0.0`。
- rule + VLM：rule 部分必须是 `0.0`；VLM 只作为补充。
- VLM-only：直接失败，必须修复为至少包含一个 rule-based evaluator。

常见失败：

| Failure | 含义 | 修复方向 |
|---|---|---|
| `init_reward_positive` | 初始状态已满足任务或 evaluator 过宽 | 加强成功条件、换输出目标、增加 negative check |
| `getter_failed` | path / dest / command list / 依赖错误 | 修 getter 或 config |
| `code_invalid` | rule code 不可解析 | 只修 code |
| `code_runtime_error` | rule code 运行失败 | 修输入类型、依赖、异常处理 |
| `vlm_only_weak` | 没有 rule anchor | 增加文件/命令类检查或丢弃 |

Repair 规则：

- 每轮 repair 后都必须重新 reset sandbox。
- 默认最多 `max_evaluator_repair_rounds = 2`。
- code invalid 优先只修 code，不改任务意图。
- init reward positive 可以修 instruction、config、success criteria 或 evaluator。
- 修复后仍失败则 reject，并将失败模式写入 app memory。

---

## Stage 5: Finalize task file + APP 动态记忆更新

### 目标

只有通过 Stage 4 的 candidate 才能写成最终任务 JSON，并更新对应 app 的动态 memory。

### Final task 字段来源

| Final 字段 | 来源 |
|---|---|
| `id` | Stage 5 生成 UUID |
| `snapshot` | `related_apps[0]` 或 `sampled_apps[0]` fallback |
| `related_apps` | candidate/proposal `related_apps` 标准化到 internal app name |
| `related_apps_version` | `app_version_lookup(related_app)` |
| `instruction` | candidate/proposal `instruction` |
| `config` | candidate/proposal `config` |
| `complexity` | candidate/proposal `complexity` |
| `estimated_steps` | candidate/proposal `estimated_steps` |
| `category` | candidate/proposal `category` |
| `evaluator` | `build_evaluator_fn(candidate.verification)` |
| `setup_image` | `image/<task_id>.png` |
| `launch_paths` | candidate/proposal `used_files` 与 Stage 0 `sampled_files[].path` 的交集 |

### Sidecar generation log

每个 rollout 写 sidecar log，不影响最终 task schema：

```json
{
  "time": "...",
  "rollout_id": "uuid",
  "sampled_apps": [],
  "app_file_support": {},
  "sampled_files": [],
  "initial_config": [],
  "exploration": {},
  "accepted_count": 0,
  "generated_ids": [],
  "failures": []
}
```

### APP memory schema

路径：

```text
mm_agents/os_symphony/agents/instruction_generator/app_memory/<app>.json
```

内容：

```json
{
  "app": "libreoffice_calc",
  "version": 3,
  "covered_features": {
    "formula": 8,
    "chart": 3
  },
  "recent_tasks": [
    {
      "task_id": "...",
      "feature_tags": ["formula"],
      "category": "file_only",
      "instruction_summary": "...",
      "preflight_passed": true
    }
  ],
  "known_good_verification_channels": ["xlsx via openpyxl"],
  "failure_patterns": [
    {
      "type": "init_reward_positive",
      "lesson": "Do not score only on output file existence."
    }
  ],
  "next_generation_bias": {
    "undercovered_features": ["settings"],
    "overcovered_features": ["formula"]
  },
  "co_use_counts": {
    "vscode": 2
  }
}
```

更新策略：

- 成功 finalization 后更新所有 sampled apps 的 memory。
- 如果某 app 在 final `related_apps` 中，更新其 `covered_features` 和 `recent_tasks`。
- 如果某 app 只是同轮 sampled 但未参与该 task，只更新轻量 `co_use_counts`。
- rejection 只有在失败原因有复用价值时才写入 memory。
- 不把完整 task JSON 塞进 memory，避免 prompt 过长。
- `recent_tasks` 保留最近 30 条。

---

## 推荐实现结构

主要实现文件：

```text
/nvme/yangbowen/yangbowen/OSSymphony/ossymphony2_task_generation.py
/nvme/yangbowen/yangbowen/OSSymphony/mm_agents/os_symphony/agents/instruction_generator/workflow.py
```

`ossymphony2_task_generation.py` 负责：

- 初始化 `desktop_env`。
- 加载 app config、app graph、tutorial。
- Stage 0 采样 `sampled_apps`、`app_file_support`、`sampled_files`。
- 使用空 `initial_config` reset 环境并保存初始 screenshot。
- 构造 `GenerationContext`。
- 调用 `InstructionGenerationWorkflow`。
- 写 `test_all.json`。

`workflow.py` 负责：

- Stage 1 exploration。
- Stage 1 proposal generation。
- Stage 2 proposal critique。
- Stage 3 evaluator synthesis。
- Stage 4 static validation、preflight validation、repair。
- Stage 5 final task 写盘、sidecar log、app memory 更新。

---

## 最小实现里程碑

### Milestone 1: 最小闭环

实现：

```text
Stage 0 -> Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 -> Stage 5
```

最低要求：

- Stage 0 可采样 `1..n` 个 app。
- Stage 0 可采样 `0..m+1` 个文件。
- Stage 1 可用 `open`、`click`、`scroll` 探索最多 10 步。
- Stage 1 proposal 包含 `instruction`、`config`、`evaluation_requirements_text`。
- Stage 3 生成至少一个 rule evaluator。
- Stage 4 能 reject init reward positive 的任务。
- Stage 5 能写最终 task JSON 和 sidecar log。

### Milestone 2: 提升质量

- 更细的 proposal diversity control。
- 更强的 evaluator static validator。
- 更完整的 preflight detail。
- app memory 中加入 verifier channel 成功率。

### Milestone 3: 批量生成稳定性

- 多进程生成。
- 成本汇总。
- 失败统计。
- app/file coverage 报告。
