from __future__ import annotations

import argparse
import inspect
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from desktop_env.osworld.evaluators import getters as evaluator_getters
from desktop_env.osworld.evaluators import metrics as evaluator_metrics
from openai import OpenAI

json_path = "/nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/osworld/test_nogdrive.json"
task_meta_dir = "/nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/osworld/examples"
app_memory_dir = "/nvme/yangbowen/yangbowen/OSSymphony/mm_agents/os_symphony/agents/instruction_generator/app_memory"
app_memory_output_path = os.path.join(app_memory_dir, "app_memory_output.json")

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


app_memory_output = {
    "domain1": {
        "covered_features": {
            "xxx": 1,
            "xxx": 1,
            "xxx": 1,
        },
        "verification_experience": {
            "feature1": ["xxxx", "xxxx"],
            "feature2": ["xxxx", "xxxx"],
        },
    }
}


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def safe_get_source(obj: Any) -> str:
    if obj is None:
        return ""
    try:
        return inspect.getsource(obj).strip()
    except Exception:
        return ""


def resolve_metric_source(func_name: Any) -> str:
    if not func_name:
        return ""
    return safe_get_source(getattr(evaluator_metrics, str(func_name), None))


def resolve_getter_source(getter_spec: Any) -> str:
    if not isinstance(getter_spec, dict):
        return ""
    getter_type = getter_spec.get("type")
    if not getter_type:
        return ""
    return safe_get_source(getattr(evaluator_getters, f"get_{getter_type}", None))


def resolve_evaluator(evaluator: Dict[str, Any]) -> Dict[str, Any]:
    funcs = ensure_list(evaluator.get("func"))
    results = ensure_list(evaluator.get("result"))
    expecteds = ensure_list(evaluator.get("expected"))
    resolved_checks = []

    for index, func_name in enumerate(funcs):
        result_spec = results[index] if index < len(results) else None
        expected_spec = expecteds[index] if index < len(expecteds) else None
        resolved_checks.append(
            {
                "func": func_name,
                "func_source": resolve_metric_source(func_name),
                "result": result_spec,
                "result_getter_source": resolve_getter_source(result_spec),
                "expected": expected_spec,
                "expected_getter_source": resolve_getter_source(expected_spec),
            }
        )

    resolved = dict(evaluator)
    resolved["resolved_checks"] = resolved_checks
    del resolved["func"], resolved["result"], resolved["expected"]
    return resolved


def load_task_index(seed_meta_path: str) -> Dict[str, List[str]]:
    with open(seed_meta_path, "r", encoding="utf-8") as f:
        seed_meta = json.load(f)
    if isinstance(seed_meta, dict):
        return {str(domain): [str(task_id) for task_id in ensure_list(task_ids)] for domain, task_ids in seed_meta.items()}
    if isinstance(seed_meta, list):
        return {"": [str(task_id) for task_id in seed_meta]}
    raise ValueError(f"Unsupported seed meta format: {type(seed_meta).__name__}")


def task_path_from_index(base_dir: str, index_domain: str, task_id: str) -> str:
    domain_path = os.path.join(base_dir, index_domain, f"{task_id}.json") if index_domain else ""
    if domain_path and os.path.exists(domain_path):
        return domain_path
    direct_path = os.path.join(base_dir, f"{task_id}.json")
    if os.path.exists(direct_path):
        return direct_path
    raise FileNotFoundError(domain_path or direct_path)


def load_tasks(seed_meta_path: str, base_dir: str) -> List[Dict[str, Any]]:
    tasks = []
    for index_domain, task_ids in load_task_index(seed_meta_path).items():
        for task_id in task_ids:
            task_path = task_path_from_index(base_dir, index_domain, task_id)
            with open(task_path, "r", encoding="utf-8") as f:
                task = json.load(f)
            related_apps = task.get("related_apps") if isinstance(task.get("related_apps"), list) else []
            tasks.append(
                {
                    "index_domain": index_domain,
                    "instruction": str(task.get("instruction") or "").strip(),
                    "related_apps": [str(app) for app in related_apps if app],
                    "evaluator": resolve_evaluator(task.get("evaluator") or {}),
                }
            )
    return tasks


def default_domain_memory() -> Dict[str, Any]:
    return {"covered_features": {}, "verification_experience": {}}


def load_existing_memory(memory_path: str) -> Dict[str, Any]:
    if not os.path.exists(memory_path):
        return {}
    with open(memory_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def write_memory(memory_path: str, memory: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(memory_path), exist_ok=True)
    tmp_path = f"{memory_path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, memory_path)


def build_prompt(task: Dict[str, Any], domain: str, domain_memory: Dict[str, Any]) -> str:
    payload = {
        "domain": domain,
        "existing_covered_features_and_verification_experience": sorted(domain_memory.get("verification_experience") or {}),
        "task": {
            "instruction": task["instruction"],
            "related_apps": task["related_apps"],
            "evaluator": task["evaluator"],
        },
    }
    print(f'[Payload]: {payload}')
    return json.dumps(payload, ensure_ascii=False)

def load_json_response(raw_response):
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_response, re.DOTALL | re.IGNORECASE)
        if match:
            return json.loads(match.group(1).strip())
        raise

def call_llm(client: OpenAI, model: str, task: Dict[str, Any], domain: str, domain_memory: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = (
        "You build compact app-memory from OSWorld tasks. "
        "Given one task instruction and its full evaluator metric/getter source code, identify the app feature(s) covered by this task and concise verification experience. "
        "Prefer reusing feature names from existing_covered_features when they describe the same capability; create a new short feature name only when no existing feature fits. "
        "Verification experience must describe reusable code-verification lessons for this feature class, not human UI steps or one task's exact assertion. "
        "Do not include obvious mechanics such as opening a file, loading JSON, reading an image with PIL, or locating a VM path unless there is a non-obvious caveat. "
        "Do not include task-specific constants, filenames, URLs, reference assets, exact dimensions, expected values, or exact assertion expressions. "
        "Generalize concrete checks into feature-level guidance, such as checking exported image dimensions/content bounds instead of bbox height == 512, inspecting document style attributes instead of one paragraph's exact value, or comparing rendered structure instead of a specific reference filename. "
        "Keep each experience item brief and concrete enough to guide evaluator writing: mention useful getter/metric families, DOM/accessibility-tree properties, config key families, parser capabilities, or comparison strategies. "
        "The features and verification experience you generate must be scoped strictly to the app indicated by the provided domain field. "
        "A task may involve multiple apps, but you only generate features and experience for the explicitly requested app; ignore other apps. "
        "The verification_experience list may be left empty (i.e. \"verification_experience\": []) when no reusable non-obvious verification lesson applies to the feature. "
        "Return strict JSON only with this schema: {\"features\":[{\"name\":\"short feature name\",\"verification_experience\":[\"brief reusable tip\"]}]}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": build_prompt(task, domain, domain_memory)},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    print(f'{response.choices[0].message.content}')
    parsed = load_json_response(response.choices[0].message.content)
    return parsed if isinstance(parsed, dict) else {}


def merge_llm_result(domain_memory: Dict[str, Any], llm_result: Dict[str, Any]) -> None:
    covered_features = domain_memory.setdefault("covered_features", {})
    verification_experience = domain_memory.setdefault("verification_experience", {})
    features = llm_result.get("features") if isinstance(llm_result.get("features"), list) else []
    if features:
        for feature in features:
            if not isinstance(feature, dict):
                continue
            name = str(feature.get("name") or "").strip()
            if not name:
                continue
            covered_features[name] = int(covered_features.get(name, 0)) + 1
            experiences = verification_experience.setdefault(name, [])
            if not isinstance(experiences, list):
                experiences = []
                verification_experience[name] = experiences
            for item in ensure_list(feature.get("verification_experience")):
                tip = " ".join(str(item).strip().split())
                if tip and tip not in experiences:
                    experiences.append(tip)
            verification_experience[name] = experiences


def build_app_memory(
    seed_meta_path: str,
    base_dir: str,
    output_path: str,
    model: str,
    base_url: str,
    api_key: str,
    save_every: int = 10,
) -> Dict[str, Any]:
    if not api_key:
        raise ValueError("OpenAI API key is empty. Set OPENAI_API_KEY or pass --api-key.")
    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url
    client = OpenAI(**client_kwargs)

    memory = load_existing_memory(output_path)
    tasks = load_tasks(seed_meta_path, base_dir)
    processed = 0

    for task in tasks:
        for domain in task["related_apps"]:
            domain_memory = memory.setdefault(domain, default_domain_memory())
            llm_result = call_llm(client, model, task, domain, domain_memory)
            merge_llm_result(domain_memory, llm_result)
            processed += 1
            if save_every > 0 and processed % save_every == 0:
                write_memory(output_path, memory)

    write_memory(output_path, memory)
    return memory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate app_memory from OSWorld seed tasks.")
    parser.add_argument("--json-path", default=json_path)
    parser.add_argument("--task-meta-dir", default=task_meta_dir)
    parser.add_argument("--output-path", default=app_memory_output_path)
    parser.add_argument("--base-url", default=OPENAI_BASE_URL)
    parser.add_argument("--api-key", default=OPENAI_API_KEY)
    parser.add_argument("--model", default=OPENAI_MODEL)
    parser.add_argument("--save-every", type=int, default=10)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_app_memory(
        seed_meta_path=args.json_path,
        base_dir=args.task_meta_dir,
        output_path=args.output_path,
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key,
        save_every=args.save_every,
    )


if __name__ == "__main__":
    main()
