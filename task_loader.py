from __future__ import annotations

import importlib
import importlib.util
import json
import os
import sys
import types
from typing import Any, Optional


def _set_parent_attr(module_name: str) -> None:
    if "." not in module_name:
        return
    parent_name, child_name = module_name.rsplit(".", 1)
    parent = sys.modules.get(parent_name)
    child = sys.modules.get(module_name)
    if parent is not None and child is not None:
        setattr(parent, child_name, child)


def _alias_module(public_name: str, target_name: str) -> None:
    if public_name not in sys.modules:
        sys.modules[public_name] = importlib.import_module(target_name)
    _set_parent_attr(public_name)


def _alias_package(public_name: str, target_name: str, package_dir: str) -> None:
    package = sys.modules.get(public_name)
    if package is None:
        package = types.ModuleType(public_name)
        package.__path__ = [package_dir]
        package.__package__ = public_name
        sys.modules[public_name] = package
    _set_parent_attr(public_name)


def _module_names(package_dir: str) -> list[str]:
    if not os.path.isdir(package_dir):
        return []
    return sorted(
        filename[:-3]
        for filename in os.listdir(package_dir)
        if filename.endswith(".py") and filename != "__init__.py"
    )


def _priority_sort(names: list[str], priority: tuple[str, ...]) -> list[str]:
    order = {name: idx for idx, name in enumerate(priority)}
    return sorted(names, key=lambda name: (order.get(name, len(order)), name))


def _update_package_exports(public_name: str, target_name: str) -> None:
    target = importlib.import_module(target_name)
    public = sys.modules[public_name]
    public.__dict__.update({k: v for k, v in target.__dict__.items() if k not in {"__name__", "__package__"}})
    public.__name__ = public_name
    public.__package__ = public_name


def _install_osworld_v2_import_aliases() -> None:
    compat_root = "desktop_env.osworld.v2_compat"
    compat_dir = os.path.join(os.path.dirname(__file__), "desktop_env", "osworld", "v2_compat")

    _alias_module("desktop_env.task_base", f"{compat_root}.task_base")
    _alias_module("desktop_env.file_source", f"{compat_root}.file_source")
    _alias_module("desktop_env.actions", f"{compat_root}.actions")
    _alias_module("desktop_env.image_utils", f"{compat_root}.image_utils")
    _alias_module("desktop_env.user_simulator", f"{compat_root}.user_simulator")
    _alias_module("desktop_env.desktop_env", "desktop_env.osworld.desktop_env")

    providers_dir = os.path.join(os.path.dirname(__file__), "desktop_env", "osworld", "providers")
    package_aliases = {
        "desktop_env.providers": ("desktop_env.osworld.providers", providers_dir),
        "desktop_env.controllers": (f"{compat_root}.controllers", os.path.join(compat_dir, "controllers")),
        "desktop_env.evaluators": (f"{compat_root}.evaluators", os.path.join(compat_dir, "evaluators")),
        "desktop_env.evaluators.getters": (f"{compat_root}.evaluators.getters", os.path.join(compat_dir, "evaluators", "getters")),
        "desktop_env.evaluators.metrics": (f"{compat_root}.evaluators.metrics", os.path.join(compat_dir, "evaluators", "metrics")),
        "desktop_env.evaluators.backends": (f"{compat_root}.evaluators.backends", os.path.join(compat_dir, "evaluators", "backends")),
        "desktop_env.safety": (f"{compat_root}.safety", os.path.join(compat_dir, "safety")),
    }
    for public_name, (target_name, package_dir) in package_aliases.items():
        _alias_package(public_name, target_name, package_dir)

    # Populate package-level exports used by V2 tasks and evaluator helpers.
    for public_name in (
        "desktop_env.providers",
        "desktop_env.evaluators.getters",
        "desktop_env.evaluators.backends",
        "desktop_env.evaluators.metrics",
        "desktop_env.safety",
    ):
        target_name, _package_dir = package_aliases[public_name]
        _update_package_exports(public_name, target_name)

    task_class_dir = os.path.join(os.path.dirname(__file__), "evaluation_examples", "osworld-v2", "task_class")
    try:
        importlib.import_module("evaluation_examples")
    except ModuleNotFoundError:
        pass
    _alias_package("evaluation_examples.task_class", "evaluation_examples.task_class", task_class_dir)



def _normalize_examples_root(base_dir: Optional[str]) -> Optional[str]:
    if not base_dir:
        return None

    root = os.path.abspath(base_dir)
    basename = os.path.basename(root)
    parent_basename = os.path.basename(os.path.dirname(root))

    if basename in {"examples", "examples_v2", "examples_windows", "task_class"}:
        return os.path.dirname(root)
    if basename == "tasks" and parent_basename == "examples_v2":
        return os.path.dirname(os.path.dirname(root))
    if basename == "examples_v2_backup" and parent_basename == "examples":
        return os.path.dirname(os.path.dirname(root))
    return root


def _add_task_import_roots(task_path: str) -> None:
    current = os.path.abspath(os.path.dirname(task_path))
    while current and current != os.path.dirname(current):
        if os.path.basename(current) == "evaluation_examples":
            root = os.path.dirname(current)
            for path in (root, current, os.path.join(current, "task_class")):
                if path not in sys.path:
                    sys.path.insert(0, path)
            return
        current = os.path.dirname(current)


def _load_task_module(task_path: str) -> Any:
    _install_osworld_v2_import_aliases()
    _add_task_import_roots(task_path)
    module_name = f"osworld_task_{os.path.splitext(os.path.basename(task_path))[0]}"
    spec = importlib.util.spec_from_file_location(module_name, task_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load task module from {task_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _instantiate_task_from_module(module: Any) -> Any:
    if hasattr(module, "get_task") and callable(module.get_task):
        return module.get_task()
    if hasattr(module, "TASK_CLASS"):
        return module.TASK_CLASS()
    if hasattr(module, "Task") and callable(module.Task):
        return module.Task()

    for value in module.__dict__.values():
        if isinstance(value, type) and value.__name__ != "BaseTask":
            if all(hasattr(value, attr) for attr in ("setup", "evaluate")):
                return value()

    raise ValueError("No task class found in module. Expected get_task(), TASK_CLASS, or Task.")


def load_task_from_file(task_path: str) -> Any:
    if task_path.endswith(".py"):
        return _instantiate_task_from_module(_load_task_module(task_path))
    with open(task_path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_task_class_path(
    task_id: Optional[str],
    base_dir: Optional[str],
    domain: Optional[str] = None,
) -> Optional[str]:
    if not task_id or not base_dir:
        return None

    root = _normalize_examples_root(base_dir)
    if not root:
        return None

    candidates: list[str] = []

    def add_candidate(path: str) -> None:
        if path not in candidates:
            candidates.append(path)

    filename = f"{task_id}.py"
    add_candidate(os.path.join(root, "task_class", filename))
    if domain and domain not in {"all", "tasks"}:
        add_candidate(os.path.join(root, "task_class", domain, filename))

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return None


def resolve_task_json_path(
    task_id: Optional[str],
    base_dir: Optional[str],
    benchmark: str = "osworld",
    domain: Optional[str] = None,
    eval_version: Optional[str] = None,
) -> Optional[str]:
    if not task_id or not base_dir:
        return None

    root = _normalize_examples_root(base_dir)
    if not root:
        return None

    candidates: list[str] = []

    def add_candidate(path: str) -> None:
        if path not in candidates:
            candidates.append(path)

    if eval_version == "v2":
        add_candidate(os.path.join(root, "examples_v2", "tasks", f"{task_id}.json"))
    elif domain:
        add_candidate(os.path.join(root, benchmark, "examples", domain, f"{task_id}.json"))
        add_candidate(os.path.join(root, "examples", domain, f"{task_id}.json"))

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    if eval_version == "v2":
        return os.path.join(root, "examples_v2", "tasks", f"{task_id}.json")
    if domain:
        return os.path.join(root, benchmark, "examples", domain, f"{task_id}.json")
    return None


def load_task_config(
    task_id: str,
    base_dir: str,
    benchmark: str = "osworld",
    domain: Optional[str] = None,
    eval_version: Optional[str] = None,
    prefer_class: bool = True,
) -> Any:
    if prefer_class:
        class_path = find_task_class_path(task_id, base_dir, domain)
        if class_path:
            return load_task_from_file(class_path)

    config_file = resolve_task_json_path(task_id, base_dir, benchmark, domain, eval_version)
    if not config_file or not os.path.exists(config_file):
        raise FileNotFoundError(config_file or f"{domain}/{task_id}")
    return load_task_from_file(config_file)
