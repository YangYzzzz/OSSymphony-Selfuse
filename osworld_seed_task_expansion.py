import inspect
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from desktop_env.osworld.evaluators import getters as evaluator_getters
from desktop_env.osworld.evaluators import metrics as evaluator_metrics


DOMAIN_TO_APP = {
    "chrome": "chrome",
    "gimp": "gimp",
    "libreoffice_calc": "libreoffice_calc",
    "libreoffice_impress": "libreoffice_impress",
    "libreoffice_writer": "libreoffice_writer",
    "multi_apps": "multi_apps",
    "os": "os",
    "thunderbird": "thunderbird",
    "vlc": "vlc",
    "vs_code": "vscode",
}


@dataclass
class SeedTaskRecord:
    domain: str
    task_id: str
    instruction: str
    snapshot: str
    related_apps: List[str]
    evaluator: Dict[str, Any]


class OSWorldSeedTaskLibrary:
    def __init__(self, examples_base_dir: str, seed_meta_path: str):
        self.examples_base_dir = examples_base_dir
        self.seed_meta_path = seed_meta_path

    def load(self) -> Dict[str, List[SeedTaskRecord]]:
        with open(self.seed_meta_path, "r", encoding="utf-8") as f:
            seed_meta = json.load(f)

        domain_to_records: Dict[str, List[SeedTaskRecord]] = {}
        for domain, task_ids in seed_meta.items():
            records: List[SeedTaskRecord] = []
            for task_id in task_ids:
                task_path = os.path.join(self.examples_base_dir, domain, f"{task_id}.json")
                if not os.path.exists(task_path):
                    continue
                with open(task_path, "r", encoding="utf-8") as f:
                    task = json.load(f)
                evaluator = task.get("evaluator") or {}
                records.append(
                    SeedTaskRecord(
                        domain=domain,
                        task_id=task_id,
                        instruction=str(task.get("instruction") or "").strip(),
                        snapshot=str(task.get("snapshot") or "").strip(),
                        related_apps=[str(app) for app in (task.get("related_apps") or [])],
                        evaluator=evaluator,
                    )
                )
            if records:
                domain_to_records[domain] = records
        return domain_to_records

    def records(self) -> List[SeedTaskRecord]:
        return [record for records in self.load().values() for record in records]


def _ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _safe_get_source(obj: Any) -> str:
    if obj is None:
        return ""
    try:
        return inspect.getsource(obj).strip()
    except Exception:
        return ""


def _resolve_metric_source(func_name: str) -> str:
    return _safe_get_source(getattr(evaluator_metrics, func_name, None))


def _resolve_getter_source(getter_spec: Any) -> str:
    if not isinstance(getter_spec, dict):
        return ""
    getter_type = getter_spec.get("type")
    # if not getter_type or getter_type in {"rule", "empty", "vm_file", "vm_command_line", "cloud_file"}:
    #     return ""
    getter_name = f"get_{getter_type}"
    return _safe_get_source(getattr(evaluator_getters, getter_name, None))


def summarize_seed_records(records: List[SeedTaskRecord]) -> str:
    chunks: List[str] = []
    for idx, record in enumerate(records, start=1):
        evaluator = record.evaluator
        funcs = _ensure_list(evaluator.get("func"))
        results = _ensure_list(evaluator.get("result"))
        expecteds = _ensure_list(evaluator.get("expected"))

        resolved_checks = []
        for check_idx, func_name in enumerate(funcs, start=1):
            result_spec = results[check_idx - 1] if check_idx - 1 < len(results) else None
            expected_spec = expecteds[check_idx - 1] if check_idx - 1 < len(expecteds) else None
            resolved_checks.append(
                {
                    "func": func_name,
                    "func_source": _resolve_metric_source(str(func_name)) if func_name else "",
                    "result": result_spec,
                    "result_getter_source": _resolve_getter_source(result_spec),
                    "expected": expected_spec,
                    "expected_getter_source": _resolve_getter_source(expected_spec),
                }
            )

        chunk = {
            "seed_id": record.task_id,
            "domain": record.domain,
            "snapshot": record.snapshot,
            "instruction": record.instruction,
            "related_apps": record.related_apps,
            "evaluator": {
                "func": evaluator.get("func"),
                "result": evaluator.get("result"),
                "expected": evaluator.get("expected"),
                "options": evaluator.get("options"),
                "conj": evaluator.get("conj"),
                "resolved_checks": resolved_checks,
            },
        }
        chunks.append(f"Seed {idx}: " + json.dumps(chunk, ensure_ascii=False))
    return "\n".join(chunks)


def build_seed_expansion_requirements(
    seed_records: List[SeedTaskRecord],
    launch_paths: List[str],
    golden_paths: List[str],
    target_app: str,
) -> str:
    seed_summary = summarize_seed_records(seed_records)
    return (
        "Generate new OSWorld-style tasks by close analogical expansion from the single seed task below.\n"
        "Treat this seed as the primary anchor: each generated task should be a near-neighbor of the seed workflow, not a broad creative variant.\n"
        "Preserve the seed's domain family, main application role, feature area, and model capability being tested while changing concrete targets, values, files, or settings enough to avoid copying.\n"
        "Do not introduce a new source application, web context, file type, or cross-application dependency unless it is already required by the seed or visible in the current initialized state.\n"
        "If the seed is an application-configuration task, generate similar configuration tasks in the same capability area; if it is a file edit/export/transformation task, generate similar file-workflow tasks.\n"
        "Use the seed evaluator pattern as strong guidance for observable artifacts, strictness, and success criteria, but do not copy the evaluator object literally.\n"
        "The generated task's related_apps must be app keys from the available application set, not version display names, and must include every app actually required by the instruction.\n"
        f"The selected target app/domain is {target_app}.\n"
        "Here is the single seed task and its evaluator pattern:\n"
        f"{seed_summary}"
    )


def choose_seed_records(
    seed_library: Dict[str, List[SeedTaskRecord]],
    main_app: str,
) -> List[SeedTaskRecord]:
    preferred_domain = None
    for domain, app in DOMAIN_TO_APP.items():
        if app == main_app:
            preferred_domain = domain
            break

    candidate_records = seed_library.get(preferred_domain or "", [])
    if candidate_records:
        return candidate_records

    if not seed_library:
        return []

    fallback_domain = sorted(seed_library.keys())[0]
    return seed_library[fallback_domain]
