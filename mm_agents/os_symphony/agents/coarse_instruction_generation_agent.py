"""
    第一阶段粗糙生成指令的Agent
    输入: 软件名 + 初始截图 + 可选文件 PATH + app 教程
    输出: 结构化列表, task_nums 个具体的可被验证的任务
"""
import logging
import textwrap
from typing import Dict, List, Any
import re

from mm_agents.os_symphony.utils.common_utils import call_llm_safe
from mm_agents.os_symphony.core.mllm import LMMAgent

logger = logging.getLogger("desktopenv.coarse_instruction_generation_agent")

INSTRUCTION_SYSTEM_PROMPT_TEMPLATE = textwrap.dedent("""
    You are an expert GUI task generation assistant on the {platform} platform.
    Your goal is to generate specific, diverse, and verifiable tasks for one or more given applications based on their initial UI screenshot, optional launch paths, and documentation.

    You will also design, for each task, a machine-checkable evaluator schema and Python rule-based evaluation functions when needed.

    ## Environment assumptions
    - The user's home directory is "~" (absolute path "/home/user").
    - Unless otherwise specified, any new files you create should be saved under a reasonable subdirectory of "~/Desktop".

    ## Applications
    - You may be given one or more applications in the current environment.
    - In the current setting, you are given exactly ONE application name: {app_name}. You MUST NOT introduce or use any other applications in your tasks.
    - All tasks must be achievable using this single application plus the filesystem under "/home/user".

    ## Task objectives
    You must generate exactly {task_numbers} independent tasks that:
    - Are executable starting from the current UI state shown in the screenshot.
    - Are fully specified and unambiguous (no hidden assumptions about files or settings).
    - Are automatically verifiable by another program based on rules or VLMs.

    Each task must be represented as a JSON object with the following fields:

    - "description" (string): Natural-language description of what the user should achieve.
    - "complexity" (string): One of "simple", "medium", or "complex".
    - "category" (string): One of:
        - "file_only": The task primarily manipulates file contents (creating, editing, organizing files) using the application.
        - "app_only": The task primarily changes application settings, preferences, themes, layouts, or built-in tools, without relying on pre-existing files.
        - "mixed": The task combines file operations and application configuration changes in one workflow.
    - "evaluation" (object):
        - "need_rule_judge" (bool): whether this task must be judged using rule-based Python functions.
        - "need_vlm_judge" (bool): whether this task must be judged using a visual-language model (VLM) from screenshots. At least one of these MUST be true. It is allowed for both to be true.
        - "vlm_desc" (string, optional): when "need_vlm_judge" is true, a concise description of what the final GUI should look like so a VLM can judge success.
        - "rule_items" (array, optional): when "need_rule_judge" is true, an array of independent rule-based checks. Each element MUST be an object with:
            - "result_getter" (object): how to obtain the actual result value to be checked. Exactly one of:
                - {{"type": "vm_file", "path": "/path/inside/vm", "dest": "/path/on/host"}} This means: copy the file at "path" from the VM to a host-side temporary location. The Python function will receive the local path as `result`.
                - {{"type": "vm_command_line", "command": ["arg1", "arg2", ...]}} This means: run the given command list inside the VM shell and pass its textual output as `result`.
            - "expected_getter" (object, optional): how to obtain an optional second value for comparison. Allowed forms are the same as for "result_getter". If you do NOT need a second value, set {{"type": "empty"}} or omit this field.
            - "code" (string): the FULL Python function definition implementing this rule. See the template below for the exact required structure.
              - The function name inside the code MUST use the common prefix "call_rule_judge_".
              - Within each task, you SHOULD conceptually number these functions locally for that task only (e.g. "call_rule_judge_1", "call_rule_judge_2", ...), but you do NOT need to output "function_name" explicitly; the system will extract the function name from the code and construct "function_name" automatically.
    - "estimated_steps" (integer): Approximate number of primitive user actions (mouse clicks, drags, key presses) required to complete the task.

    ## Evaluation design
    For each task, you must also design how it will be evaluated.

    - You MUST prioritize rule-based evaluation whenever it is reasonably possible.
      - If the task's success can be reliably checked using files (vm_file) and/or command outputs (vm_command_line), you SHOULD set "need_rule_judge" = true and "need_vlm_judge" = false.
      - Only when some essential aspect of success CANNOT be reliably checked via files or commands should you set "need_vlm_judge" = true.

    - Use "evaluation.need_rule_judge" and "evaluation.need_vlm_judge" to indicate which mechanisms are required:
        - At least one of them MUST be true.
        - It is allowed that both are true (hybrid judgement), but you SHOULD avoid using "need_vlm_judge" when rule-based checks already fully capture the success conditions.

    - When "evaluation.need_rule_judge" is true, you MUST provide one or more "rule_items" as described above.
      - Rule-based checks SHOULD be as complete and fine-grained as possible for that task, covering all important properties that you reasonably expect to be verifiable.
      - When designing rule-based checks, you SHOULD try to cover as many aspects of the task's goal as possible so that the rule-based component can decide success in most normal cases without relying on VLM.

    - When "evaluation.need_vlm_judge" is true, you MUST provide a clear "vlm_desc" string that describes the final GUI state and, where helpful, key intermediate GUI states during execution, so that a VLM can reliably judge success from screenshots.

    - Rule-based checks MUST follow these principles:
        - Core idea: "everything is a file". For Command-UI-Agent (CUA) style tasks whose goal is to WRITE or transform something, the final result should be reflected in one or more files inside the VM. These files may be:
            - Common formats such as .txt, .md, .pdf, .xlsx, .docx, .pptx, .mp3, .png, .jpg, .json, .mp4, .wav, etc.
                - You can use any reasonable Python packages to read and analyze these files (e.g., `python-docx`/`python-pptx`/`openpyxl`/`pandas` for Office documents, `PyPDF2`/`pdfplumber` for PDFs, `Pillow` for images, and `pydub`/`librosa`/`ffmpeg-python` for audio/video).
            - Less common formats such as .dxf or application-specific project files.
            - Files that are easy to locate (e.g., under "~/Desktop").
            - Files that are deeply hidden (e.g., application config files, caches, or internal state files), maybe they can be accessed via a path or an API.
        - For rule-based checks you MUST rely ONLY on:
            - Files inside the VM filesystem that can be copied out (vm_file), OR
            - Command outputs obtained from the VM shell (vm_command_line), typically via application CLIs or helper tools that expose internal state.
        - You MUST NOT use remote/cloud golden files or any resource that cannot be accessed from inside the VM.
        - Prefer using {{"type": "empty"}} for "expected_getter" when the rule can be fully hard-coded inside the function.

    - Detailed distinction between Rule-based and VLM-based tasks:
        - Rule-based:
            - Tasks whose success can be checked directly using VM files (vm_file) or VM commands (vm_command_line).
            - vm_file outputs are often used by copying common file types directly from the VM to the host and evaluating with Python functions on the host side. For file‑based evaluation, you should prefer this pattern over extracting partial information via VM command‑line tools.
            - vm_command_line outputs are often used to expose complex internal structures (e.g., querying application state or hidden configuration paths).
            - The final answer should be deterministic or only mildly dynamic; the Python rule function should be able to determine success using deterministic logic given the file contents or command output.
        - VLM-based:
            - Tasks whose success depends on information that is deeply hidden and cannot be reliably accessed via files or APIs.
            - Tasks involving uncommon file formats, which it is hard to writing a robust parser.
            - Tasks whose answer is inherently dynamic or visual (e.g., GUI layout, theme, transient UI states) and is best judged by looking at the screen.

    ### Python rule function template (CRITICAL)

    For each rule item, the "code" string MUST contain ONE complete Python function following this template:

    ```python
    import os
    import json
    import re
                                                     
    def call_rule_judge_1(result, expected, **options) -> float:
        \"\"\"Describe in detail what this function checks.

        You SHOULD mention:
        - The task's high-level goal.
        - How `result` is obtained (from vm_file or vm_command_line).
        - How `expected` is obtained (from vm_file or vm_command_line or empty).
        - Why this rule is sufficient to fully or partially verify task success.
        \"\"\"
        try:
            # Example pattern for partial and weighted credit:
            # - Inspect multiple independent conditions or fields in `result`.
            # - For each condition, decide a weight (they do not all need to be equal).
            # - Compute a score as sum of weights for all satisfied conditions, normalized to [0.0, 1.0].
            # - Return that score as a float between 0.0 and 1.0.
            # Below is only a placeholder; you MUST replace it with real verification logic.
            _ = result
            _ = expected
            return 0.0
        except Exception:
            # On ANY error, the function MUST return 0.0 instead of raising.
            return 0.0
    ```

    Requirements:
    - The function name MUST match the "function_name" you provide in the rule item (e.g., "call_rule_judge_1").
    - Within each task, ALL rule-based functions MUST use the common prefix "call_rule_judge_" and be numbered locally for that task only:
        - Example for one task with three rules: "call_rule_judge_1", "call_rule_judge_2", "call_rule_judge_3".
        - Function names MUST NOT be numbered globally across tasks. Each task reuses its own local numbering starting from 1.
    - The signature MUST be exactly: def call_rule_judge_1(result, expected, **options) -> float:
    - The function MUST import any modules it uses at the top of the code string.
    - The function MUST return a float in [0.0, 1.0].
      - You SHOULD design the function to support partial credit when appropriate.
        - Example: if a final file is expected to contain three required fields, you may award ~0.33 for each field that appears correctly, so a partially correct solution gets an intermediate score such as 0.33 or 0.67.
      - You MAY assign different weights to different conditions when some are more important than others (e.g., critical conditions sum to 0.7, secondary conditions sum to 0.3).
      - You SHOULD still use 1.0 only when all critical conditions are satisfied, and 0.0 when none of the important conditions are satisfied.
    - The docstring MUST clearly describe what is being checked and why.

    ## Launch paths and file usage
    You may be given `launch_paths`: a list of absolute file or project paths that are already opened in the application.

    - When `launch_paths` is non-empty:
        - You may and should refer directly to these paths in your tasks.
        - Do NOT assume the existence of additional unnamed files outside the ones given, unless you explicitly create and save them in your task description.

    - When `launch_paths` is empty:
        - You must NOT assume any pre-existing files beyond the application itself.
        - You may still create new files as part of a task, but you must:
            - Explicitly specify their save locations with "~" (e.g., "~/Desktop/project_notes/report.md").
            - Make sure the description and condition clearly say that the file should be saved and not just edited in memory.
        - In this case, prefer "app_only" tasks, or tasks that first create new files and then operate on them within the same task.

    ## Complexity and estimated_steps
    Use these guidelines:

    - "simple":
        - Typically 10–20 user actions.
        - Single-file workflows or small configuration changes.
    - "medium":
        - Typically 20–35 actions.
        - Multi-step workflows, multiple files or views, or a combination of a small settings change plus file editing.
    - "complex":
        - Typically 35–60 actions.
        - Longer workflows involving settings, multiple documents/projects, or non-trivial navigation across several views.

    Choose "estimated_steps" consistent with the complexity level and the actual operations required.

    ## Diversity requirements (CRITICAL)
    Across the {task_numbers} tasks you generate:

    - Vary the difficulty: Include a spread of "simple", "medium", and "complex" tasks.
    - Vary the functional coverage: Use different features or workflows of the application (editing, formatting, searching, filters, views, settings, exports, imports, etc., depending on {app_name}).
    - Avoid generating multiple tasks that are essentially the same goal with only superficial wording changes.

    ## Verifiability and paths (CRITICAL)
    For every task:

    - Any file that is read, edited, or inspected must be identified with a unique, unambiguous "~"-based path. You may reuse paths from `launch_paths`, or introduce new paths under "~/Desktop" or other sensible subdirectories of the home directory.
    - If the task modifies a file, you MUST make it explicit in "description" that the user should save the file before finishing.

    ## Use of application tutorials (if provided)
    If you are given an application-specific markdown tutorial, you may use it to:
        - Discover realistic features and workflows.
        - Ensure tasks align with what the application actually supports.
    You MUST NOT:
        - Copy sentences verbatim from the tutorial.
        - Refer directly to the tutorial in the tasks.

    ## Final output requirements
    Produce a single JSON object with the following shape:

    {{
        "tasks": [
            {{ /* task 1 */ }},
            {{ /* task 2 */ }},
            ... exactly {task_numbers} task objects ...
        ]
    }}

    - The output MUST be valid JSON (no comments, no trailing commas).
    - Do not include any extra text before or after the JSON.
    - Do not wrap the JSON in XML, markdown fences, or any other format.
    """
)

class InstructionGenerationAgent:
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

    def parse_instruction(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM JSON response to extract structured task list."""
        import json

        tasks: List[Dict[str, Any]] = []
        try:
            data = json.loads(response)
            raw_tasks = data.get("tasks", [])
            if not isinstance(raw_tasks, list):
                logger.warning("`tasks` field is not a list in JSON response")
                return tasks

            for idx, t in enumerate(raw_tasks):
                if not isinstance(t, dict):
                    logger.warning(f"Task {idx} is not an object, skipping")
                    continue
                task = self._parse_single_task_json(t)
                if task:
                    tasks.append(task)

            logger.info(f"Successfully parsed {len(tasks)} tasks from JSON")
        except Exception as e:
            logger.error(f"Error parsing instruction JSON response: {e}")
            tasks = []
        return tasks

    def _parse_single_task_json(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single JSON task object into internal task dict format."""
        try:
            description = str(obj.get("description", "")).strip()

            if not description:
                logger.warning("Task missing required description, skipping")
                return {}

            complexity = str(obj.get("complexity", "medium")).strip().lower()
            if complexity not in ["simple", "medium", "complex"]:
                complexity = "medium"

            category = str(obj.get("category", "mixed")).strip().lower()
            if category not in ["file_only", "app_only", "mixed"]:
                category = "mixed"

            evaluation = obj.get("evaluation") or {}

            need_rule = bool(evaluation.get("need_rule_judge", False))
            need_vlm = bool(evaluation.get("need_vlm_judge", False))

            rule_items_raw = evaluation.get("rule_items") or []
            if not isinstance(rule_items_raw, list):
                rule_items_raw = []

            # If both flags are False but there are rule items, default to need_rule = True
            if not need_rule and not need_vlm and rule_items_raw:
                need_rule = True

            # Build normalized rule_items structure
            normalized_rule_items = []

            import ast

            def _extract_function_name_from_code(code: str) -> str | None:
                """Parse the code with AST and extract the first function name starting with 'call_rule_judge_'.

                Returns None when the code is not valid Python or no such function is found.
                """
                try:
                    tree = ast.parse(code)
                except SyntaxError:
                    return None

                for node in tree.body:
                    if isinstance(node, ast.FunctionDef) and node.name.startswith("call_rule_judge_"):
                        return node.name
                return None

            for idx, ri in enumerate(rule_items_raw, start=1):
                if not isinstance(ri, dict):
                    continue

                code_str = ri.get("code") or ""
                if not isinstance(code_str, str):
                    logger.warning("rule_item code is not a string, skipping this rule item")
                    continue

                fn_name = _extract_function_name_from_code(code_str)
                if not fn_name:
                    logger.warning(
                        "Failed to extract function name from rule_item code via AST; expected a valid Python function starting with 'call_rule_judge_'"
                    )
                    continue

                def _norm_getter(g: Any) -> Dict[str, Any]:
                    if not isinstance(g, dict):
                        return {"type": "empty"}
                    g_type = g.get("type")
                    if g_type == "vm_file":
                        return {
                            "type": "vm_file",
                            "path": str(g.get("path", "")),
                            "dest": str(g.get("dest", "")),
                        }
                    if g_type == "vm_command_line":
                        cmd = g.get("command")
                        if isinstance(cmd, list):
                            cmd_list = [str(c) for c in cmd]
                        elif cmd is None:
                            cmd_list = []
                        else:
                            cmd_list = [str(cmd)]
                        return {"type": "vm_command_line", "command": cmd_list}
                    if g_type == "empty":
                        return {"type": "empty"}
                    return {"type": "empty"}

                result_getter = _norm_getter(ri.get("result_getter"))
                expected_getter_raw = ri.get("expected_getter")
                if expected_getter_raw is None:
                    expected_getter = {"type": "empty"}
                else:
                    expected_getter = _norm_getter(expected_getter_raw)

                normalized_rule_items.append(
                    {
                        "function_name": fn_name,
                        "result_getter": result_getter,
                        "expected_getter": expected_getter,
                        "code": code_str,
                    }
                )

            vlm_desc = str(evaluation.get("vlm_desc", "")).strip()
            if vlm_desc and not need_vlm:
                need_vlm = True

            # Ensure at least one of the flags is True. If both are False and
            # we have neither rule items nor vlm_desc, default to VLM-based.
            if not need_rule and not need_vlm:
                if normalized_rule_items:
                    need_rule = True
                elif vlm_desc:
                    need_vlm = True
                else:
                    # Fallback: treat as VLM-only with a generic description
                    need_vlm = True
                    vlm_desc = f"Check carefully."

            estimated_steps_raw = obj.get("estimated_steps", 15)
            try:
                estimated_steps = int(estimated_steps_raw)
            except Exception:
                estimated_steps = 15

            return {
                "description": description,
                "verification": {
                    "need_rule_judge": need_rule,
                    "need_vlm_judge": need_vlm,
                    "rule_items": normalized_rule_items,
                    "vlm_desc": vlm_desc,
                },
                "complexity": complexity,
                "category": category,
                "estimated_steps": estimated_steps,
            }
        except Exception as e:
            logger.warning(f"Failed to parse JSON task object: {e}")
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

        launch_paths: currently opened file/project paths (may be empty).
        app_tutorial_md: optional markdown tutorial content for the app.
        """
        try:
            # 1) Build the base system prompt from template
            system_prompt = INSTRUCTION_SYSTEM_PROMPT_TEMPLATE.format(task_numbers=str(task_nums), app_name=app_name, platform=self.platform)

            # 2) Optionally inject app-specific tutorial markdown
            if app_tutorial_md:
                tutorial_block = (
                    f"\n\nBelow is markdown documentation for {app_name}. "
                    "Use it only as background knowledge to design realistic tasks, "
                    "but do not copy any sentences verbatim and do not mention this documentation explicitly in tasks.\n\n"
                    f"{app_tutorial_md}\n"
                )
                system_prompt = system_prompt + tutorial_block

            self.agent.add_system_prompt(system_prompt=system_prompt)

            # 3) User message: screenshot + known launch paths
            launch_paths_text = "" if not launch_paths else "\n".join(launch_paths)
            user_text = (
                f"This is the current UI screenshot of application '{app_name}'.\n"
                "If there are any currently opened file/project paths (launch_paths), they are listed below, one per line:\n"
                f"{launch_paths_text if launch_paths_text else '(No explicit launch paths are provided in this round)'}\n\n"
                f"Using the system instructions, generate exactly {task_nums} structured tasks for this application that can be executed from the current state."
            )

            # 3.5) Try up to 3 times to obtain structurally valid tasks with syntactically valid rule code
            max_attempts = 3
            last_tasks: List[Dict[str, Any]] = []
            for attempt in range(1, max_attempts + 1):
                self.agent.reset()
                self.agent.add_system_prompt(system_prompt=system_prompt)
                self.agent.add_message(
                    text_content=user_text,
                    image_content=observation.get("screenshot"),
                    role="user",
                )

                logger.info(f"Generating {task_nums} tasks for {app_name}, attempt {attempt}/{max_attempts}")
                response = call_llm_safe(self.agent, temperature=self.temperature)
                pattern = r'^```(?:json)?\s*\n?(.*?)\n?```$'
                match = re.search(pattern, response, re.DOTALL)
                if match:
                    response = match.group(1).strip()

                if not response:
                    logger.error("Empty response from LLM on attempt %s", attempt)
                    continue

                tasks = self.parse_instruction(response)
                last_tasks = tasks

                # Strict validation: if a task has rule_items, all of them must have been parsed successfully
                all_rule_code_valid = True
                for t in tasks:
                    v = t.get("verification") or {}
                    rule_items = v.get("rule_items") or []
                    if not isinstance(rule_items, list):
                        rule_items = []
                    for ri in rule_items:
                        fn = (ri or {}).get("function_name")
                        code_str = (ri or {}).get("code")
                        if not fn or not code_str:
                            all_rule_code_valid = False
                            break
                    if not all_rule_code_valid:
                        break

                if all_rule_code_valid:
                    break
                else:
                    logger.warning(
                        "Rule-based code validation failed on attempt %s; retrying generation (up to %s attempts)",
                        attempt,
                        max_attempts,
                    )

            if not last_tasks:
                return []

            tasks = last_tasks
            if len(tasks) < task_nums:
                logger.warning(f"Requested {task_nums} tasks but only generated {len(tasks)}")

            for i, task in enumerate(tasks):
                logger.info(f"Task {i+1}: {task.get('description', '')[:80]}...")
                if "verification" in task:
                    v = task["verification"]
                    logger.debug(f"  need_rule_judge: {v.get('need_rule_judge')}  need_vlm_judge: {v.get('need_vlm_judge')}")
                    logger.debug(f"  rule_items: {len(v.get('rule_items', []))}  vlm_desc: {bool(v.get('vlm_desc'))}")
                logger.debug(f"  Complexity: {task.get('complexity')}, steps≈{task.get('estimated_steps')}")

            return tasks
        except Exception as e:
            logger.error(f"Error in generate method: {e}", exc_info=True)
            return []
