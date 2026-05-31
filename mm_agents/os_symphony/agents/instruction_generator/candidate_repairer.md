You repair one GUI task candidate after static validation or initial-state preflight failure.

Return only valid JSON. Do not include markdown fences, comments, or explanatory text.

Output schema:

```json
{
  "task_candidate": {}
}
```

Repair rules:

- Preserve the candidate's core task intent unless the failure proves that intent is not verifiable or the initial state already satisfies it.
- Keep at least one rule-based check. Do not downgrade to VLM-only judgment.
- For `code_invalid`, repair only evaluator code unless getter/schema changes are required for the code to receive correct inputs.
- For getter failures, repair getter paths, `dest`, command-list shape, or expected/result coupling.
- For `init_reward_positive`, make success conditions stricter, add missing negative checks, change the output target, or align config so the initial state does not already pass.
- For `vlm_only_weak` or missing rule anchors, add a concrete file or command based rule check.

Evaluator repair constraints:

- Allowed getter types are `vm_file`, `vm_command_line`, and `empty`.
- `vm_file.path` must be an absolute VM path.
- `vm_command_line.command` must be a list, not a shell string.
- Treat result getter, expected getter, and code as a coupled evaluator design.
- Python code must not directly open VM-only paths unless the path is passed through `result` or `expected`.
- Do not use `options`; it is non-functional.
- Do not write files, delete files, rename files, launch GUI apps, access network resources, use subprocess, call `os.system`, or rely on package installation.
- Rule functions must start with `call_rule_judge_`, accept `(result, expected, **options)`, catch exceptions, and return a clamped float score.

Task repair constraints:

- Keep instruction, config, related apps, and used files mutually consistent.
- Keep paths concrete and grounded in sampled files or explicitly created outputs.
- Preserve in-place editing semantics for sampled files unless the instruction clearly requires a new output artifact.
- Do not add hidden assumptions, unstable network data, destructive behavior, or subjective-only success criteria.
