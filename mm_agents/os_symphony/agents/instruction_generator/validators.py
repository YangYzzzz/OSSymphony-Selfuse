from __future__ import annotations

import ast
from typing import Any, Dict, List

from desktop_env.osworld.desktop_env import DesktopEnv

from mm_agents.os_symphony.agents.instruction_generator.constants import ALLOWED_GETTER_TYPES, DANGEROUS_CALLS, DANGEROUS_IMPORTS


class StaticEvaluatorValidator:
    def validate(self, task: Dict[str, Any]) -> Dict[str, Any]:
        warnings: List[str] = []
        errors: List[str] = []
        verification = task.get("verification") or {}
        need_rule = bool(verification.get("need_rule_judge"))
        need_vlm = bool(verification.get("need_vlm_judge"))
        rule_items = verification.get("rule_items") or []
        if not need_rule and not need_vlm:
            errors.append("no_judge_enabled")
        if not need_rule:
            errors.append("missing_required_rule_judge")
        if need_rule and not rule_items:
            errors.append("missing_rule_items")
        if need_vlm and not str(verification.get("vlm_desc", "")).strip():
            warnings.append("missing_vlm_desc")
        if not isinstance(rule_items, list):
            errors.append("rule_items_not_list")
            rule_items = []
        for idx, item in enumerate(rule_items, start=1):
            self._validate_rule_item(item, idx, errors, warnings)
        return {"passed": not errors, "errors": errors, "warnings": warnings}

    def _validate_rule_item(self, item: Any, idx: int, errors: List[str], warnings: List[str]) -> None:
        if not isinstance(item, dict):
            errors.append(f"rule_{idx}_not_object")
            return
        for key in ("result_getter", "expected_getter"):
            getter = item.get(key) or {"type": "empty"}
            self._validate_getter(getter, f"rule_{idx}_{key}", errors)
        code = item.get("code")
        if not isinstance(code, str) or not code.strip():
            errors.append(f"rule_{idx}_missing_code")
            return
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            errors.append(f"rule_{idx}_code_invalid:{e}")
            return
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        if not functions:
            errors.append(f"rule_{idx}_missing_function")
            return
        fn = functions[0]
        if not fn.name.startswith("call_rule_judge_"):
            errors.append(f"rule_{idx}_bad_function_name")
        if item.get("function_name") and item.get("function_name") != fn.name:
            warnings.append(f"rule_{idx}_function_name_mismatch")
        args = [arg.arg for arg in fn.args.args]
        has_kwargs = fn.args.kwarg is not None and fn.args.kwarg.arg == "options"
        if args[:2] != ["result", "expected"] or not has_kwargs:
            errors.append(f"rule_{idx}_bad_signature")
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name.split(".")[0] for alias in node.names]
                if any(name in DANGEROUS_IMPORTS for name in names):
                    errors.append(f"rule_{idx}_dangerous_import")
                    break
            if isinstance(node, ast.Call):
                call_name = self._call_name(node.func)
                if call_name.split(".")[-1] in DANGEROUS_CALLS or call_name in {"os.system", "subprocess.run", "subprocess.Popen"}:
                    errors.append(f"rule_{idx}_dangerous_call:{call_name}")
                    break

    def _validate_getter(self, getter: Any, label: str, errors: List[str]) -> None:
        if not isinstance(getter, dict):
            errors.append(f"{label}_not_object")
            return
        getter_type = getter.get("type")
        if getter_type not in ALLOWED_GETTER_TYPES:
            errors.append(f"{label}_bad_type:{getter_type}")
            return
        if getter_type == "vm_file" and not str(getter.get("path", "")).startswith("/"):
            errors.append(f"{label}_path_not_absolute")
        if getter_type == "vm_command_line" and not isinstance(getter.get("command"), list):
            errors.append(f"{label}_command_not_list")

    def _call_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            prefix = self._call_name(node.value)
            return f"{prefix}.{node.attr}" if prefix else node.attr
        return ""


class PreflightValidator:
    def validate(self, env: DesktopEnv, task_config: Dict[str, Any]) -> Dict[str, Any]:
        try:
            env.reset(
                task_config={
                    "config": task_config.get("config", []),
                    "id": task_config["id"],
                    "instruction": task_config.get("instruction", ""),
                    "evaluator": task_config.get("evaluator", {}),
                }
            )
        except Exception as e:
            print(f'[PreflightValidator] Reset Exception: {e}')
            return {"passed": False, "init_rule_reward": None, "details": str(e), "failure_type": "reset_failed"}
        try:
            reward = float(env.evaluate())
            print(f'[PreflightValidator] Preflight Evaluate Score: {reward}')
            return {
                "passed": reward <= 1e-6,
                "init_rule_reward": reward,
                "details": "",
                "failure_type": "init_reward_positive" if reward > 1e-6 else None,
            }
        except Exception as e:
            print(f'[PreflightValidator] Evaluate Exception: {e}')
            return {"passed": False, "init_rule_reward": None, "details": str(e), "failure_type": "getter_failed"}
