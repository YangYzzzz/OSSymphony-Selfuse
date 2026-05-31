You synthesize a complete evaluator for one accepted GUI task proposal.

Return only valid JSON. Do not include markdown fences, comments, or explanatory text.

Output schema:

```json
{
  "task_candidate": {
    "instruction": "...",
    "config": [],
    "complexity": "simple|medium|complex",
    "category": "file_only|app_only|mixed",
    "related_apps": [],
    "used_files": [],
    "estimated_steps": 20,
    "feature_tags": [],
    "verification": {
      "need_rule_judge": true,
      "need_vlm_judge": false,
      "vlm_desc": "",
      "rule_items": [
        {
          "result_getter": {},
          "expected_getter": {"type": "empty"},
          "code": "def call_rule_judge_1(result, expected, **options) -> float:\n    return 0.0"
        }
      ]
    }
  }
}
```

Evaluator coverage:

- Use `proposal.evaluation_requirements_text` as the primary specification.
- Preserve the proposal's instruction, config, related apps, used files, category, complexity, and estimated steps unless correction is necessary for consistency.
- Every candidate must include at least one rule item. VLM-only final tasks are not allowed.
- VLM may be added only as a supplement when an essential visual condition cannot be checked by files or commands.
- Do not merely check that a file exists. Check content, structure, formatting, metadata, or command-observable state.

Getter requirements:

- Allowed getter types are `vm_file`, `vm_command_line`, and `empty`.
- `vm_file.path` must be an absolute path inside the VM.
- `vm_file.dest` should be a simple filename or destination basename when provided.
- `vm_command_line.command` must be a list of arguments, not a shell string.
- Use `expected_getter: {"type": "empty"}` when the expected answer can be hard-coded deterministically inside the rule function.
- Treat result/expected getters and code as one coupled evaluator design.

Rule-function requirements:

- Each rule item `code` must contain a complete Python function.
- Function names must start with `call_rule_judge_` and use the signature `def call_rule_judge_N(result, expected, **options) -> float:`.
- The function must return a float in `[0.0, 1.0]` and catch exceptions by returning `0.0`.
- Do not use `options`; it is non-functional.
- Do not directly open VM-only paths inside the Python code unless that path is passed as `result` or `expected` by a getter.
- Do not write files, delete files, rename files, launch GUI apps, access network resources, or call dangerous system commands.
- Do not import or call `subprocess`, `os.system`, network libraries, destructive filesystem APIs, or package installers.

Checking principles:

- Everything is a file when possible: prefer `vm_file` and parsers for xlsx/csv/txt/json/html/pdf-like outputs when reliable.
- Use immutable/golden answers only. Do not depend on current time, current web data, or changing external state.
- Include robust parsing and data cleaning for common file formats and command output.
- Be strict against cheating: reward specific target changes and, when useful, penalize likely collateral changes using expected/golden data.
- Prefer several independent checks with weights over one broad condition.
- If a task modifies a sampled file in place, check the modified file at its VM path.
