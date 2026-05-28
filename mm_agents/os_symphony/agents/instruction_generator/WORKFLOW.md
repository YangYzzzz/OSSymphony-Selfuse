# OSSymphony Instruction Generation Workflow

目标是在保留现有核心基底的前提下增强任务质量：仍然随机选择主 app / app graph / 初始化文件与截图，但把“一次性让 LLM 直接生成任务”升级为多阶段、可验证、可迭代的生成流程。

## 可以参考的文件
1. 当前生成指令的核心代码：/nvme/yangbowen/yangbowen/OSSymphony/os_caliber_task_generator.py
2. 指令Agent的核心代码：/nvme/yangbowen/yangbowen/OSSymphony/mm_agents/os_symphony/agents/instruction_generation_agent.py
3. APP 的文档以及config：/nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/ubuntu_online_rollout/config，/nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/ubuntu_online_rollout/app_tutorial
4. 参考的 GUI Action 执行：/nvme/yangbowen/yangbowen/OSSymphony/mm_agents/anthropic/main_with_code.py，这个文件告诉你如何配置Click，Scroll动作
4. 参考的项目：/nvme/yangbowen/yangbowen/OpenComputer（具体的设计已经列在下面了）

## 生成Agent Workflow的额外要求
1. 每个agent调用时都增加成本统计，参考 /nvme/yangbowen/yangbowen/OSSymphony/mm_agents/anthropic/main_with_code.py，统计调用次数等开销
2. 每个agent独立建类，然后最外层框架搭起整个工作流
3. 每个agent用相同的模型 api_key, base_url 即可

## Non-goals

- 不在当前 pipeline 中引入真实 agent rollout。
- 不要求验证黄金状态是否正确。
- 不重写现有 DesktopEnv、OSCaliberTaskGenerator、InstructionGenerationAgent 的核心接口。
- 不强制为每个 app 预先写静态 verifier；继续使用现有动态 evaluator 结构。

## Key ideas borrowed from OpenComputer

1. **Proposal 和 verification 分离**：先让任务围绕 app 能力和真实用户场景发散，再单独审查 evaluator 是否可执行、可判分。
2. **Quality gate**：每个阶段都有结构化输出和 reject reason，不再把 LLM 的一次输出直接当最终任务。
3. **Environment validation before finalization**：任务最终写盘前，先在初始化环境里验证 evaluator 不会误给正分。
4. **Repair without rollout**：当前不跑 agent，但可以修复 task description、evaluator getter/code、初始化 config、文件路径和 app memory。
5. **Lessons / memory feedback loop**：把每个 app 已覆盖功能、失败模式、好用验证通道记录下来，下一轮生成时注入 prompt。

## Proposed stages

```text
Stage 0  Sample base context
Stage 1  Sandbox exploration
Stage 2  Proposal generation
Stage 3  Proposal critique and selection
Stage 4  Evaluator synthesis and static validation
Stage 5  Sandbox preflight validation: init reward must be 0
Stage 6  Repair loop without rollout
Stage 7  Finalize task files and update app memory
```

---

## Stage 0: Sample base context

保留现有基底：

- 从 `app_config.json` 中采样 `main_app`。
- 通过 `APP_GRAPH` 采样 `apps_for_group`。
- 通过 `_generate_config()` 随机选择 app 启动方式和文件路径。
- 创建 `golden_paths`。
- reset 环境并保存初始截图。

现有入口基本对应：

- `os_caliber_task_generator.py::_sample_app_group`
- `os_caliber_task_generator.py::_generate_config`
- `OSCaliberTaskGenerator.generate_task`

建议改动：Stage 0 只产出一个结构化 `generation_context`，不要立刻调用 task generator。

```json
{
  "main_app": "libreoffice_calc",
  "apps_for_group": ["libreoffice_calc", "vscode"],
  "task_setup_config": [...],
  "launch_paths": [...],
  "golden_paths": [...],
  "setup_image": "...png",
  "app_tutorial_md": "...",
  "app_memory": {...}
}
```

---

## Stage 1: Sandbox exploration

这一阶段不是执行任务，而是对初始化环境做轻量探索，给 LLM 更多 grounding，避免只凭 tutorial 和首屏截图生成 naive 任务。

### Allowed exploration

探索阶段允许一个最小动作子集，目标是观察初始环境，而不是完成任务或改变持久状态。

#### Read-only probes

- 截图当前窗口。
- 查询窗口标题、进程、文件是否存在。
- 对 `launch_paths` 做只读 metadata 检查，例如文件大小、扩展名、目录 listing。
- 对文本类 / 表格类 / 代码类文件做只读摘要。
- 对 app 配置目录做只读存在性检查，如 `~/.config/<app>`。
- 对可安全执行的 command-line introspection 做查询，如版本号、MIME、文件结构。

#### Minimal GUI exploration actions

- `click(x, y)`：只允许点击明显的导航、展开、tab、菜单入口或空白区域，用于揭示 UI affordance；不得点击保存、导出、确认、删除、应用设置、运行脚本、发送消息等会改变状态的控件。
- `scroll(dx, dy)`：只允许在当前页面、侧栏、菜单或文档视图内滚动以观察更多内容；不得依赖滚动来完成任务目标。

建议把探索动作限制在很小的步数内，例如每个 candidate context 最多 3-5 个 GUI exploration actions。探索结束后必须 reset 回 Stage 0 的初始化状态，再进入 proposal/evaluator/preflight，避免探索动作污染任务初始状态。

### Disallowed exploration

- 不修改文件内容。
- 不保存、不导出、不改变 app setting。
- 不点击会触发持久写入、确认弹窗、网络提交、删除、安装、运行代码或发送消息的 GUI 控件。
- 不访问不稳定网络资源。

### Output

```json
{
  "visible_state": "The spreadsheet is open on Sheet1 with columns A-D visible...",
  "file_inventory": [
    {"path": "/home/user/Desktop/test_files/xlsx/budget.xlsx", "type": "xlsx", "summary": "3 sheets: Sales, Costs, Summary"}
  ],
  "app_affordances_seen": ["spreadsheet grid", "formula bar", "sheet tabs"],
  "safe_verification_channels": ["vm_file:xlsx via openpyxl", "vm_command_line:python inspect zip/xml"],
  "constraints": ["Only one launch file is open", "No internet required"]
}
```

### Why it helps

当前 prompt 只知道 app、截图、路径和可选 tutorial，容易生成泛泛任务。探索摘要能让模型知道“这个文件里到底有什么、当前 UI 到哪一步、哪些结果能被 rule 检查”。

---

## Stage 2: Proposal generation

复用 `InstructionGenerationAgent` 的 LLM 调用能力，但把输出拆成 proposal，不立刻要求完整 evaluator code。

### Prompt inputs

- Stage 0 context
- Stage 1 exploration summary
- static app tutorial
- dynamic app memory
- current generated-task coverage target

### Proposal schema

```json
{
  "proposal_id": "local_short_id",
  "description": "goal-oriented user request",
  "category": "file_only | app_only | mixed",
  "complexity": "simple | medium | complex",
  "estimated_steps": 20,
  "related_apps": ["libreoffice_calc"],
  "target_features": ["formula", "conditional_formatting", "export_csv"],
  "required_artifacts": ["/home/user/Desktop/test_files/xlsx/budget.xlsx"],
  "success_criteria": [
    "Sheet Summary contains total revenue in B2",
    "Rows with margin below 10% are highlighted red"
  ],
  "verification_plan_hint": {
    "preferred": "rule",
    "channels": ["vm_file"],
    "rationale": "The edited xlsx can be inspected with openpyxl"
  }
}
```

### Generation policy

- 每次 oversample，比如需要 10 个最终任务，先生成 16-20 个 proposal。
- 强制分布覆盖：core content、settings/preferences、layout、import/export、cross-app、file transformation。
- 对已有 memory 中覆盖过多的 feature 降权。
- 不允许只做“打开文件、输入一句话、保存”这种单点操作。

---

## Stage 3: Proposal critique and selection

这一阶段用 LLM 或规则对 proposal 打分，不生成 evaluator code。

### Scoring axes

| Axis | Accept target | Reject reason examples |
|---|---:|---|
| specificity | high | 缺少路径、目标对象、输出位置、精确值 |
| realism | high | 像 benchmark 指令，不像真实用户需求 |
| complexity | medium/complex | 太短、单步、只改一个无意义字段 |
| verifiability | high | 结果不可观察、只能凭主观判断 |
| data fit | high | 与当前 launch file 无关或假设不存在的数据 |
| diversity | high | 与本轮或历史 memory 功能重复 |
| non-destructiveness | required | 删除大量文件、修改系统设置、不可逆 |

### Output

```json
{
  "accepted": [...],
  "rejected": [
    {
      "proposal_id": "p03",
      "reason": "too_simple",
      "suggested_repair": "Combine formula creation with chart/export requirement"
    }
  ],
  "coverage_summary": {
    "formula": 2,
    "chart": 1,
    "settings": 1
  }
}
```

如果 accepted 数量不足，带 rejected reason 回到 Stage 2 重试，最多 2-3 轮。

---

## Stage 4: Evaluator synthesis and static validation

只对 accepted proposals 生成完整 evaluator。

### Evaluator synthesis

复用当前 schema：

- `need_rule_judge`
- `need_vlm_judge`
- `vlm_desc`
- `rule_items`
  - `result_getter`
  - `expected_getter`
  - `code`

但 prompt 要从“生成任务”改为“为已接受 proposal 生成 evaluator”，这样 code 质量会明显更稳定。

### Static validation checks

在不进入真实 rollout 的情况下，先做静态检查：

1. JSON 可解析。
2. 每个 rule item 的 Python code 可 `ast.parse`。
3. 函数名存在且以 `call_rule_judge_` 开头。
4. 函数签名兼容 `(result, expected, **options)`。
5. getter 类型只允许 `vm_file`、`vm_command_line`、`empty`。
6. `vm_file.path` 必须是 VM 内绝对路径。
7. `vm_command_line.command` 必须是 list。
8. 如果 task 描述提到文件路径，evaluator 至少覆盖关键输出路径。
9. 若 task 修改 launch file，优先使用 golden path 做 negative check。
10. code 中不允许危险操作：`subprocess`、`os.system`、网络访问、写文件、删除文件等。

### Output

```json
{
  "task_candidate": {...},
  "static_validation": {
    "passed": true,
    "warnings": []
  }
}
```

---

## Stage 5: Sandbox preflight validation: init reward must be 0

这是当前阶段最关键的新增 gate：不跑 agent，只在初始化后的 sandbox 里直接运行 evaluator。

### Principle

初始化状态一定不能已经满足任务。也就是说：

```text
reward(init_state, task_evaluator) == 0
```

如果初始化状态给了正分，说明任务或 evaluator 有问题：

- 任务太 trivial，初始文件已经满足。
- evaluator 过宽，误判初始状态通过。
- getter 路径错了，读到了 golden 或错误文件。
- rule code 只检查文件存在，没有检查目标修改。
- VLM desc 太宽泛，初始截图也可能被判成功。

### What to run

对每个 task candidate：

1. 使用 Stage 0 的 `task_setup_config` reset sandbox，确保状态等同于最终任务的真实初始化状态。
2. 不执行任何完成任务的 agent action；如果 Stage 1 做过 click/scroll 探索，这里必须重新 reset，而不是复用探索后的环境。
3. 注入 candidate evaluator，保持最终任务 JSON 中将要写入的 evaluator 字段不变。
4. 执行 `env.evaluate()`，只验证初始化环节的 reward。
5. 若 `need_vlm_judge` 为 true，当前阶段不调用 VLM 当最终判据；只做 `vlm_desc` 静态检查或可选 screenshot self-check。
6. 记录 `preflight_reward`、每个 rule 的 result/expected getter 是否成功、以及每个 rule 的 init score。

### Pass criteria

- rule-only：`preflight_reward == 0.0`。
- rule + VLM：rule 部分必须是 `0.0`；VLM 部分只做 prompt 风险检查。
- VLM-only：默认进入 repair，要求补充至少一个 rule-based negative/preflight check；除非这个任务被标记为 `visual_only_allowed`。

### Output

```json
{
  "task_id": "candidate_uuid",
  "preflight": {
    "init_rule_reward": 0.0,
    "passed": true,
    "details": [
      {"rule": "call_rule_judge_1", "score": 0.0, "result_source": "vm_file:/home/user/..."}
    ]
  }
}
```

### Important distinction from golden validation

不要求证明 golden 状态正确，也不要求任务完成后的 reward 为 1。当前只证明“初始化不是成功态”，这是更稳、更便宜、也更适合当前 pipeline 的验证。

---

## Stage 6: Repair loop without rollout

如果 Stage 3-5 失败，不丢弃，先尝试修复。

### Repair classes

| Failure | Likely cause | Repair action |
|---|---|---|
| `init_reward_positive` | evaluator 过宽或任务已满足 | 加强 positive condition、添加 negative check、换输出路径、改任务目标 |
| `getter_failed` | path/command 错 | 修正 getter path、dest、command list |
| `code_invalid` | LLM 生成代码不可执行 | 只修 code，不改任务意图 |
| `description_ambiguous` | success criteria 不可判 | 明确对象、路径、数量、格式 |
| `too_simple` | 初始状态或一步可完成 | 合并多条件目标，提高复杂度 |
| `memory_duplicate` | 功能覆盖重复 | 换 feature 或降低优先级 |
| `vlm_only_weak` | 没有稳定 rule anchor | 增加文件/命令类检查，或降级为候选池 |

### Repair loop

```text
candidate -> diagnose -> repair prompt -> static validation -> preflight validation
```

最多 2 轮。仍失败则 reject，并把原因写入 app memory，避免下次重复。

---

## Stage 7: Finalize and update app memory

只有通过 Stage 5 的 candidate 才写成最终任务 JSON。

### Final task schema

最终写盘格式必须和当前 `OSCaliberTaskGenerator.generate_task()` 输出保持一致：不改名、不删除、不改变现有字段语义，默认也不新增顶层字段。探索摘要、preflight 结果、feature tags、memory version 等生成期信息写到 sidecar log 或 app memory，不塞进最终 task JSON。

```json
{
  "id": "uuid",
  "snapshot": "main_app",
  "related_apps": [...],
  "related_apps_version": [...],
  "instruction": "...",
  "config": [...],
  "complexity": "medium",
  "estimated_steps": 25,
  "category": "file_only",
  "evaluator": {...},
  "setup_image": "image/<uuid>.png",
  "launch_paths": [...]
}
```

### App memory update

每个 app 维护一个动态 memory，类似 tutorial，但它记录的是生成经验，不是静态功能说明。

建议路径：

```text
mm_agents/os_symphony/agents/instruction_generator/app_memory/<app>.json
```

### App memory schema

```json
{
  "app": "libreoffice_calc",
  "version": 3,
  "covered_features": {
    "formula": 8,
    "chart": 3,
    "conditional_formatting": 2,
    "settings": 1
  },
  "recent_tasks": [
    {
      "task_id": "...",
      "feature_tags": ["formula", "chart"],
      "category": "file_only",
      "instruction_summary": "Create margin analysis and chart from budget workbook",
      "preflight_passed": true
    }
  ],
  "known_good_verification_channels": [
    "xlsx via openpyxl",
    "csv via pandas",
    "png via pillow"
  ],
  "failure_patterns": [
    {
      "type": "init_reward_positive",
      "lesson": "Do not score only on output file existence; check content changed from golden file."
    }
  ],
  "next_generation_bias": {
    "undercovered_features": ["settings", "import_export"],
    "overcovered_features": ["formula"]
  }
}
```

### Memory write policy

- append/update only after finalization or rejection with useful failure reason。
- 不把完整 task JSON 塞进 memory，避免 prompt 过长。
- recent_tasks 保留最近 N 条，比如 30。
- covered_features 用计数和衰减都可以；先用简单计数。
- 每轮 generation prompt 注入 summary，而不是整个 memory。
- 这个 memory 和静态 tutorial 分工不同：tutorial 描述 app 能力，app memory 描述本 pipeline 已生成过什么、哪些 verifier 写法容易误判、哪些 feature 应该被降权或补足。

---

## Recommended implementation shape

### New module candidates

```text
instruction_generator/
├── WORKFLOW.md
├── app_memory/
│   └── <app>.json
├── prompts/
│   ├── exploration_summary.md
│   ├── proposal_generation.md
│   ├── proposal_critique.md
│   ├── evaluator_synthesis.md
│   └── repair_candidate.md
└── workflow.py
```

### Minimal integration path

1. 先不改现有 `generate_task()` 的 public behavior。
2. 新增一个 `generate_task_v2()` 或 `InstructionGenerationWorkflow`。
3. 复用：
   - `_sample_app_group()`
   - `_generate_config()`
   - `_build_evaluator_from_verification()`
   - `InstructionGenerationAgent` 的 LLM wrapper / parse utilities。
4. 把 preflight validation 写成独立函数，输入 `env` 和 candidate task config。
5. 通过 CLI 参数选择 v1/v2，便于对比。

### Suggested first implementation milestone

先实现最小闭环：

```text
Stage 0 -> Stage 1(light) -> Stage 2 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7
```

Stage 1 light 版本包含：截图、launch_paths 文件摘要、app memory 注入，以及最多 3-5 步 `click` / `scroll` 的非持久探索。探索后必须 reset，再进行 evaluator synthesis 和 preflight。

第二阶段再把 Stage 3 critique、更完整 exploration、以及更细的 per-app coverage policy 加进去。

## Discussion points

1. VLM-only 任务是否允许进入最终集？建议默认不允许，除非有明确 `visual_only_allowed` 标记。
2. preflight reward 是否要求严格等于 0？建议 rule reward 严格 0；浮点可用 `<= 1e-6`。
3. app memory 是按 app name 还是 app version 区分？建议文件名按 app name，内部记录 version。
4. repair loop 是在同一个 sandbox 反复 validate，还是每轮 reset？建议每轮 reset，避免 evaluator postconfig 改变状态。
5. 多 app 任务的 memory 更新：主 app 必更，related apps 可只增加轻量 co-use count。