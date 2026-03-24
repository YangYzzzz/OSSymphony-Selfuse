import ast
import os, json
import textwrap

root_dir = "/nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/osworld/examples"

"""
root_dir
- domain1
    - task1.json
    - task2.json
    - xxx
- domain2
"""

def collect_type_statistics(root_dir: str):
    stats = {}
    overall = {"expected": {}, "result": {}}

    for domain in os.listdir(root_dir):
        domain_path = os.path.join(root_dir, domain)
        if not os.path.isdir(domain_path):
            continue

        if domain not in stats:
            stats[domain] = {"expected": {}, "result": {}}

        for fname in os.listdir(domain_path):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(domain_path, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            evaluator = data.get("evaluator", {})

            # handle expected (may be list or single object)
            expected = evaluator.get("expected")
            if expected is not None:
                if isinstance(expected, list):
                    expected_items = expected
                else:
                    expected_items = [expected]

                for item in expected_items:
                    if not isinstance(item, dict):
                        continue
                    t = item.get("type")
                    if not isinstance(t, str):
                        continue

                    stats[domain]["expected"][t] = stats[domain]["expected"].get(t, 0) + 1
                    overall["expected"][t] = overall["expected"].get(t, 0) + 1

            # handle result (assume single object or list similar to expected)
            result = evaluator.get("result")
            if result is not None:
                if isinstance(result, list):
                    result_items = result
                else:
                    result_items = [result]

                for item in result_items:
                    if not isinstance(item, dict):
                        continue
                    t = item.get("type")
                    if not isinstance(t, str):
                        continue

                    stats[domain]["result"][t] = stats[domain]["result"].get(t, 0) + 1
                    overall["result"][t] = overall["result"].get(t, 0) + 1

    stats["overall"] = overall

    # compute overall_wo_chrome (exclude 'chrome' domain)
    overall_wo_chrome = {"expected": {}, "result": {}}
    for domain, dr in stats.items():
        if domain in ("overall",):
            continue
        if domain == "chrome":
            continue
        for kind in ("expected", "result"):
            for t, cnt in dr.get(kind, {}).items():
                overall_wo_chrome[kind][t] = overall_wo_chrome[kind].get(t, 0) + cnt

    stats["overall_wo_chrome"] = overall_wo_chrome
    return stats

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
            - "function_name" (string, optional): the Python function name to use for this rule. If omitted, the system will name them sequentially as "call_rule_judge_1", "call_rule_judge_2", etc.                                                                                                           
            - "code" (string): the FULL Python function definition implementing this rule. See the template below for the exact required structure.
    - "estimated_steps" (integer): Approximate number of primitive user actions (mouse clicks, drags, key presses) required to complete the task.
                                                            
    ## Evaluation design                                                                                                                                 
    For each task, you must also design how it will be evaluated.
                                                                                                                                                           
    - Use "evaluation.need_rule_judge" and "evaluation.need_vlm_judge" to indicate which mechanisms are required:                                        
        - At least one of them MUST be true.                                                                                                             
        - It is allowed that both are true (hybrid judgement).                                                                                           
                                                                                                                                                           
    - When "evaluation.need_rule_judge" is true, you MUST provide one or more "rule_items" as described above. Each rule item will be turned into a Python function and a pair of result/expected getters.                                                                                                   
                                                                                                                                                           
    - When "evaluation.need_vlm_judge" is true, you MUST provide a clear "vlm_desc" string that describes the final GUI appearance or layout so that a VLM can decide success from screenshots.
                                                                                                                                                           
    - Rule-based checks MUST follow these principles:     
        - Core idea: "everything is a file". For Command-UI-Agent (CUA) style tasks whose goal is to WRITE or transform something, the final result should be reflected in one or more files inside the VM. These files may be:                                                                              
              - Common formats such as .txt, .md, .pdf, .xlsx, .mp3, .png, .jpg, .json, etc.
              - Less common formats such as .dxf or application-specific project files.                                                                    
              - Files that are easy to locate (e.g., under "~/Desktop").
              - Files that are deeply hidden (e.g., application config files, caches, or internal state files), as long as they can be accessed via a path or an API.                                                                                                                                               
        - For rule-based checks you MUST rely ONLY on:
            - Files inside the VM filesystem that can be copied out (vm_file), OR                                                                        
            - Command outputs obtained from the VM shell (vm_command_line), typically via application CLIs or helper tools that expose internal state.
        - You MUST NOT use remote/cloud golden files or any resource that cannot be accessed from inside the VM.                                         
        - Prefer using {{"type": "empty"}} for "expected_getter" when the rule can be fully hard-coded inside the function.
                                                                                                                                                                                                                                                                                  
    - Detailed distinction between Rule-Base and VLM-Base tasks:
        - Rule-Base:
            - Tasks whose success can be checked directly using VM files (vm_file) or VM commands (vm_command_line).
            - Command outputs are often used to expose complex internal structures (e.g., querying application state or hidden configuration paths).
            - The final answer should be deterministic or only mildly dynamic; the Python rule function should be able to determine success using deterministic logic given the file contents or command output.                                                                                           
        - VLM-Base:                                                                                                                                      
            - Tasks whose success depends on information that is deeply hidden and cannot be reliably accessed via files or APIs.                        
            - Tasks involving non-standard or hard-to-parse file formats, where writing a robust parser is impractical.                                  
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
        - Whether `expected` is used (it may be "empty").
        - Why this rule is sufficient to fully or partially verify task success.                                                                         
        \"\"\"
        try:
            # TODO: implement the rule-based checking logic here, using `result` and `expected`.                                                         
            # - `result` comes from the corresponding result getter (vm_file/vm_command_line).
            # - `expected` comes from the expected getter (usually type="empty").                                                                        
            # Replace the placeholder below with real verification code.
            _ = result                                                                                                                                   
            _ = expected                                                                                                                                 
            return 0.0
        except Exception:                                                                                                                                
            # On ANY error, the function MUST return 0.0 instead of raising.
            return 0.0
    ```

    Requirements:
    - The function name MUST match the "function_name" you provide in the rule item (e.g., "call_rule_judge_1").
    - The signature MUST be exactly: def call_rule_judge_1(result, expected, **options) -> float:
    - The function MUST import any modules it uses at the top of the code string.                                                                        
    - The function MUST return a float in [0.0, 1.0]. In most cases use 0.0 or 1.0.
    - The docstring MUST clearly describe what is being checked and why.                                                                                 
                                                            
    ### Summary
    - For tasks with rule-based judgement (need_rule_judge = true): you MUST provide one or more rule items, each with a Python function in "code".
    - For tasks with only VLM judgement (need_vlm_judge = true and need_rule_judge = false): do NOT provide any rule_items.                              
    - For hybrid tasks (both true): provide both rule_items and a vlm_desc.
                                                                                                                                                           
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
                                                                                                                                                           
    - Vary the categories: Include a mix of "file_only", "app_only", and "mixed" tasks where appropriate for the application.
    - Vary the evaluation.type: Include tasks that are purely "rule_based", purely "vlm_based", and "hybrid" when meaningful.
    - Vary the difficulty: Include a spread of "simple", "medium", and "complex" tasks.
    - Vary the functional coverage: Use different features or workflows of the application (editing, formatting, searching, filters, views, settings, exports, imports, etc., depending on {app_name}).
    - Avoid generating multiple tasks that are essentially the same goal with only superficial wording changes.                                          
                                                            
    ## Verifiability and paths (CRITICAL)
    For every task:

    - Any file that is read, edited, or inspected must be identified with a unique, unambiguous "~"-based path. You may reuse paths from `launch_paths`, or introduce new paths under "~/Desktop" or other sensible subdirectories of the home directory.
    - If the task modifies a file, you MUST:
        - Make it explicit in "description" that the user should save the file before finishing.
                                                                                                                              
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
if __name__ == "__main__":
    # statistics = collect_type_statistics(root_dir)
    # out_path = os.path.join(os.path.dirname(__file__), "osworld_type_statistics.json")
    # with open(out_path, "w", encoding="utf-8") as f:
    #     json.dump(statistics, f, indent=2, ensure_ascii=False)
    # print(f"Statistics written to {out_path}")
    # prompt = INSTRUCTION_SYSTEM_PROMPT_TEMPLATE.format(task_numbers="8", app_name="chrome", platform="Ubuntu")
    # print(repr(prompt))

    
    code_str = "import os\nimport json\nimport re\n\ndef call_rule_judge_1(result, expected, **options) -> float:\n    \"\"\"Verify the user created and saved a new SQL script with a specific header comment.\n\n    High-level goal:\n    - The task asks to open an existing SQL file in DBeaver, add a header line '-- NOTE: Annotated by DBeaver' at the very top, and save it as '~/Desktop/DBeaverTasks/annotated_test.sql'.\n\n    How `result` is obtained:\n    - `result` is the local host path to the copied VM file '/home/user/Desktop/DBeaverTasks/annotated_test.sql'.\n\n    Use of `expected`:\n    - `expected` is unused (type='empty').\n\n    Why sufficient:\n    - If the file exists and its first non-empty line matches the exact expected header, it demonstrates that the user edited the file and saved it to the specified location from DBeaver.\n    \"\"\"\n    try:\n        if not result or not os.path.exists(result):\n            return 0.0\n        with open(result, 'r', encoding='utf-8', errors='ignore') as f:\n            text = f.read()\n        # Normalize possible BOM and leading whitespace/newlines\n        text = text.lstrip('\\ufeff')\n        lines = text.splitlines()\n        first_non_empty = None\n        for ln in lines:\n            if ln.strip() != \"\":\n                first_non_empty = ln\n                break\n        if first_non_empty is None:\n            return 0.0\n        expected_line = \"-- NOTE: Annotated by DBeaver\"\n        if first_non_empty.strip() == expected_line:\n            return 1.0\n        return 0.0\n    except Exception:\n        return 0.0"

    # 解析上述 code_str, 尝试提取其 docstring 作为 check_desc
    check_desc = ""
    def extract_function_docstring(code_str, function_name=None):
        try:
            mod = ast.parse(code_str)
            # 遍历所有节点，找到函数定义
            for node in ast.walk(mod):
                if isinstance(node, ast.FunctionDef):
                    # 如果指定了函数名，则匹配；否则取第一个函数
                    if function_name is None or node.name == function_name:
                        return ast.get_docstring(node)
            return None
        except Exception as e:
            print(str(e))
            return None

    # 使用
    check_desc = extract_function_docstring(code_str)
    print(check_desc)
