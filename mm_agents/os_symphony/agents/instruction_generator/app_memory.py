from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Tuple

from .constants import APP_MEMORY_DIR


class AppMemoryStore:
    def __init__(self, memory_dir: str = APP_MEMORY_DIR):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

    def _path(self, app: str) -> str:
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", app)
        return os.path.join(self.memory_dir, f"{safe_name}.json")

    def load(self, app: str) -> Dict[str, Any]:
        path = self._path(app)
        if not os.path.exists(path):
            return self._default_memory(app)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return self._default_memory(app)
            default = self._default_memory(app)
            default.update(data)
            return default
        except Exception:
            return self._default_memory(app)

    def load_many_summary(self, apps: List[str]) -> Tuple[Dict[str, Any], Dict[str, Dict[str, Any]]]:
        memories = {app: self.load(app) for app in apps}
        summaries = {app: self.summary(memory) for app, memory in memories.items()}
        return summaries, memories

    def save(self, app: str, memory: Dict[str, Any]) -> None:
        path = self._path(app)
        tmp_path = f"{path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)

    def summary(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "covered_features": memory.get("covered_features", {}),
            "known_good_verification_channels": memory.get("known_good_verification_channels", []),
            "failure_patterns": memory.get("failure_patterns", [])[-8:],
            "next_generation_bias": memory.get("next_generation_bias", {}),
            "recent_tasks": memory.get("recent_tasks", [])[-8:],
        }

    def record_finalized_many(self, apps: List[str], memories: Dict[str, Dict[str, Any]], task: Dict[str, Any]) -> None:
        related_apps = task.get("related_apps") if isinstance(task.get("related_apps"), list) else apps
        for app in apps:
            memory = memories.setdefault(app, self._default_memory(app))
            if app in related_apps:
                self._record_finalized(app, memory, task)
            else:
                self._record_couse(memory, related_apps)
            self.save(app, memory)

    def record_failure_many(self, apps: List[str], memories: Dict[str, Dict[str, Any]], failure_type: str, lesson: str) -> None:
        for app in apps:
            memory = memories.setdefault(app, self._default_memory(app))
            failures = memory.setdefault("failure_patterns", [])
            failures.append({"type": failure_type, "lesson": lesson})
            memory["failure_patterns"] = failures[-30:]
            memory["version"] = int(memory.get("version", 1)) + 1
            self.save(app, memory)

    def _record_finalized(self, app: str, memory: Dict[str, Any], task: Dict[str, Any]) -> None:
        feature_tags = task.get("feature_tags") or task.get("target_features") or []
        if not isinstance(feature_tags, list):
            feature_tags = []
        covered = memory.setdefault("covered_features", {})
        for tag in feature_tags:
            tag = str(tag)
            covered[tag] = int(covered.get(tag, 0)) + 1
        recent = memory.setdefault("recent_tasks", [])
        recent.append(
            {
                "task_id": task.get("id"),
                "feature_tags": feature_tags,
                "category": task.get("category"),
                "instruction_summary": str(task.get("instruction") or task.get("description") or "")[:180],
                "preflight_passed": True,
            }
        )
        memory["recent_tasks"] = recent[-30:]
        self._record_couse(memory, task.get("related_apps") or [])
        memory["version"] = int(memory.get("version", 1)) + 1
        self._update_bias(memory)

    def _record_couse(self, memory: Dict[str, Any], related_apps: List[str]) -> None:
        counts = memory.setdefault("co_use_counts", {})
        for app in related_apps:
            app = str(app)
            if app and app != memory.get("app"):
                counts[app] = int(counts.get(app, 0)) + 1

    def _update_bias(self, memory: Dict[str, Any]) -> None:
        covered = memory.get("covered_features", {})
        if not covered:
            memory["next_generation_bias"] = {}
            return
        ordered = sorted(covered.items(), key=lambda item: item[1])
        memory["next_generation_bias"] = {
            "undercovered_features": [k for k, _ in ordered[:5]],
            "overcovered_features": [k for k, _ in ordered[-5:]],
        }

    def _default_memory(self, app: str) -> Dict[str, Any]:
        return {
            "app": app,
            "version": 1,
            "covered_features": {},
            "recent_tasks": [],
            "known_good_verification_channels": [],
            "failure_patterns": [],
            "next_generation_bias": {},
            "co_use_counts": {},
        }
