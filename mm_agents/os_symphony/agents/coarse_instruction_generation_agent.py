"""
    第一阶段粗糙生成指令的Agent
    输入: 软件名 + 初始截图 + 可选文件 PATH + app 教程
    输出: 结构化列表, task_nums 个具体的可被验证的任务
"""
import logging
from typing import Dict, List, Any
import re

from mm_agents.os_symphony.memory.procedural_memory import PROCEDURAL_MEMORY
from mm_agents.os_symphony.utils.common_utils import call_llm_safe
from mm_agents.os_symphony.core.mllm import LMMAgent

logger = logging.getLogger("desktopenv.coarse_instruction_generation_agent")


class CoarseInstructionGenerationAgent:
    """A dedicated agent for generating coarse instructions from initial screenshots."""

    def __init__(self, engine_params: Dict, platform: str = "linux"):
        if not engine_params:
            raise ValueError("engine_params cannot be None or empty")

        self.engine_params = engine_params
        self.temperature = engine_params.get("temperature", 0.5)
        self.platform = platform
        self.reset()

    def reset(self):
        logger.debug("Resetting CoarseInstructionGenerationAgent state")
        self.agent = LMMAgent(
            engine_params=self.engine_params,
            system_prompt="",
        )
        self.system_prompt_template = PROCEDURAL_MEMORY.construct_instruction_generation_procedural_memory(
            platform=self.platform
        )

    def parse_instruction(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response to extract structured task list using regex."""
        tasks: List[Dict[str, Any]] = []
        try:
            task_blocks = re.findall(r"<task>(.*?)</task>", response, re.DOTALL)
            if not task_blocks:
                logger.warning("No <task> blocks found in response")
                return tasks

            for block in task_blocks:
                task = self._parse_single_task(block)
                if task:
                    tasks.append(task)

            logger.info(f"Successfully parsed {len(tasks)} tasks from XML")
        except Exception as e:
            logger.error(f"Error parsing instruction response: {e}")
            tasks = []
        return tasks

    def _parse_single_task(self, block: str) -> Dict[str, Any]:
        try:
            desc_match = re.search(r"<description>(.*?)</description>", block, re.DOTALL)
            if not desc_match:
                logger.warning("No description found in task block")
                return {}
            description = desc_match.group(1).strip()

            cond_match = re.search(r"<condition>(.*?)</condition>", block, re.DOTALL)
            if not cond_match:
                logger.warning("No condition found in task block")
                return {}
            condition = cond_match.group(1).strip()

            result_match = re.search(r"<expected_result>(.*?)</expected_result>", block, re.DOTALL)
            expected_result = result_match.group(1).strip() if result_match else "Task completed successfully"

            comp_match = re.search(r"<complexity>(.*?)</complexity>", block, re.DOTALL)
            if not comp_match:
                complexity = "medium"
            else:
                complexity = comp_match.group(1).strip().lower()
                if complexity not in ["simple", "medium", "complex"]:
                    complexity = "medium"

            # 判定方式：rule_based / vlm_based / hybrid
            eval_match = re.search(r"<evaluation_type>(.*?)</evaluation_type>", block, re.DOTALL)
            evaluation_type = eval_match.group(1).strip().lower() if eval_match else "rule_based"
            if evaluation_type not in ["rule_based", "vlm_based", "hybrid"]:
                evaluation_type = "rule_based"

            eval_desc_match = re.search(r"<evaluation_desc>(.*?)</evaluation_desc>", block, re.DOTALL)
            evaluation_desc = eval_desc_match.group(1).strip() if eval_desc_match else ""

            # 任务类型：file_only / app_only / mixed
            cat_match = re.search(r"<category>(.*?)</category>", block, re.DOTALL)
            category = cat_match.group(1).strip().lower() if cat_match else "mixed"
            if category not in ["file_only", "app_only", "mixed"]:
                category = "mixed"

            # 估计步数
            steps_match = re.search(r"<estimated_steps>(.*?)</estimated_steps>", block, re.DOTALL)
            try:
                estimated_steps = int(steps_match.group(1).strip()) if steps_match else 15
            except Exception:
                estimated_steps = 15

            return {
                "description": description,
                "verification": {
                    "condition": condition,
                    "expected_result": expected_result,
                    "evaluation_type": evaluation_type,
                    "evaluation_desc": evaluation_desc,
                },
                "complexity": complexity,
                "category": category,
                "estimated_steps": estimated_steps,
            }
        except Exception as e:
            logger.warning(f"Failed to parse task block: {e}")
            return {}

    def generate(
        self,
        app_name: str,
        observation: Dict,
        task_nums: int = 10,
        launch_paths: List[str] | None = None,
        app_tutorial_md: str | None = None,
    ) -> List[Dict[str, Any]]:
        """Generate coarse-grained task list.

        launch_paths: 当前已打开的文件/工程路径列表（可为空）。
        app_tutorial_md: 对应 app 的 markdown 教程内容（可为空）。
        """
        try:
            # 1) 构造 system prompt（基础程序式记忆）
            system_prompt = self.system_prompt_template.replace("APPNAME", app_name).replace(
                "TASKNUMBERS", str(task_nums)
            )

            # 2) 拼接我们需要的额外约束
            #   - 家目录 ~= /home/user
            #   - 三种任务类型: file_only / app_only / mixed
            #   - Rule-based vs VLM-based 评估
            extra_guidance = f"""
你正在为一个桌面自动化智能体设计任务。

系统环境约束：
- 平台: {self.platform}
- 家目录固定为 "~/home/user"（绝对路径为 "/home/user"）。
- 所有需要保存的新文件，如果没有特别说明，优先保存到 "~/home/user/Desktop" 下的合理子路径中。

任务类型约束（category 字段）：
- file_only: 主要是利用当前软件对一个或多个文件进行内容修改、创建或组织（例如编辑文档、修改代码、合并 PDF 等）。
- app_only: 主要是修改当前软件的自身设置、偏好、主题、插件、窗口布局等，不依赖具体已有文件；可以新建文件但重点是设置变化。
- mixed: 同时包含对文件内容的操作和对软件设置的调整，例如先修改某个配置文件，再在软件设置里启用相关选项。

当本轮任务中 launch_paths 为空（即没有任何已经打开的文件路径）时：
- 只能生成 app_only 或 mixed 中“创建新文件再操作”的任务，不要要求修改某个已经存在但未在 launch_paths 中显式给出的文件。
- 如果需要新建文件，请在描述和验证条件中明确指出要保存到 "~/home/user/Desktop/..." 的具体路径。

评估方式（evaluation_type 字段）：
- rule_based: 任务结果可以通过读取文件内容或结构进行规则判定，例如文本中包含某些关键字、表格单元格的值、某个 Desktop 路径下存在特定文件等。
- vlm_based: 任务结果只能通过观察 GUI 界面的变化判定，例如修改软件深层设置、工具栏布局、颜色主题、某个难以从文件系统直接判断的配置面板。
- hybrid: 同时需要文件内容和 GUI 状态来进行最终判定。

难度和预估步数：
- 最简单的任务也应该需要大约 10 步以上的鼠标/键盘交互；简单任务对应 complexity="simple"，estimated_steps 一般在 10~20 步。
- 中等难度任务 complexity="medium"，estimated_steps 一般在 20~35 步，通常包含多窗口或多文件操作，或简单设置修改 + 文件编辑的组合。
- 困难任务 complexity="complex"，estimated_steps 一般在 35~60 步，往往需要先修改设置、再在多个文件或页面之间来回切换，或者完成一个较长的工作流。

当前软件: {app_name}

如果提供了 launch_paths, 它们表示当前已经通过命令行打开的文件或工程路径，你可以在任务中直接使用这些路径，不要假设存在其他看不见的文件。

对于每个任务，请用如下 XML 结构输出：

<task>
  <description>用自然语言描述具体的用户任务，指出要操作哪些文件或软件设置。</description>
  <condition>用于自动判定任务是否完成的规则，可以包括文件路径、关键字、GUI 状态等。</condition>
  <expected_result>任务完成后的理想状态描述。</expected_result>
  <complexity>simple | medium | complex</complexity>
  <category>file_only | app_only | mixed</category>
  <evaluation_type>rule_based | vlm_based | hybrid</evaluation_type>
  <evaluation_desc>说明为什么选择该评估方式，以及评估时应该关注的文件或界面元素。</evaluation_desc>
  <estimated_steps>一个整数，表示完成任务大约需要多少步操作（鼠标/键盘事件数量量级）。</estimated_steps>
</task>
            """

            # 3) 注入 app 教程 md（如果有）
            tutorial_part = ""
            if app_tutorial_md:
                tutorial_part = (
                    "\n\n下面是当前应用的简要功能说明 (markdown 摘要，可用于帮助你构思任务，但不要逐字照抄)：\n"  # noqa: E501
                    + app_tutorial_md
                )

            full_system_prompt = system_prompt + "\n\n" + extra_guidance + tutorial_part
            self.agent.add_system_prompt(system_prompt=full_system_prompt)

            # 4) user 输入：截图 + 当前已知路径
            launch_paths_text = "" if not launch_paths else "\n".join(launch_paths)
            user_text = (
                f"这里是软件 {app_name} 的当前界面截图。"  # noqa: E501
                "\n如果有当前已打开的文件/工程路径 (launch_paths)，它们如下：\n"
                f"{launch_paths_text if launch_paths_text else '（本轮没有显式提供任何路径）'}\n"
                "请根据这些信息以及系统提示，为该软件生成 "
                f"{task_nums} 个可判定、可执行的复杂任务。"
            )

            self.agent.add_message(
                text_content=user_text,
                image_content=observation.get("screenshot"),
                role="user",
            )

            logger.info(f"Generating {task_nums} tasks for {app_name}")
            response = call_llm_safe(self.agent, temperature=self.temperature)
            if not response:
                logger.error("Empty response from LLM")
                return []

            tasks = self.parse_instruction(response)
            if len(tasks) < task_nums:
                logger.warning(f"Requested {task_nums} tasks but only generated {len(tasks)}")

            for i, task in enumerate(tasks):
                logger.info(f"Task {i+1}: {task.get('description', '')[:80]}...")
                if "verification" in task:
                    logger.debug(f"  Condition: {task['verification'].get('condition', '')[:80]}...")
                    logger.debug(f"  Eval type: {task['verification'].get('evaluation_type', '')}")
                logger.debug(f"  Complexity: {task.get('complexity')}, steps≈{task.get('estimated_steps')}")

            return tasks
        except Exception as e:
            logger.error(f"Error in generate method: {e}", exc_info=True)
            return []
