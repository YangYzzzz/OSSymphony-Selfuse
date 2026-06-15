from __future__ import annotations

import json
import os
import re
from typing import Dict, List, Tuple

from mm_agents.os_symphony.agents.instruction_generator.constants import APP_MEMORY_DIR
from mm_agents.os_symphony.agents.instruction_generator.models import AppMemory


class AppMemoryStore:
    def __init__(self, memory_dir: str = APP_MEMORY_DIR):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

    def _path(self, app: str) -> str:
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", app)
        return os.path.join(self.memory_dir, f"{safe_name}.json")

    def load(self, app: str) -> AppMemory:
        path = self._path(app)
        if not os.path.exists(path):
            return AppMemory(app=app)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return AppMemory.from_dict(app, data if isinstance(data, dict) else {})
        except Exception:
            return AppMemory(app=app)

    def load_many_summaries(self, apps: List[str]) -> Tuple[Dict[str, dict], Dict[str, dict], Dict[str, AppMemory]]:
        memories = {app: self.load(app) for app in apps}
        proposal_summaries = {app: memory.proposal_summary() for app, memory in memories.items()}
        evaluator_summaries = {app: memory.evaluator_summary() for app, memory in memories.items()}
        return proposal_summaries, evaluator_summaries, memories

    def save(self, app: str, memory: AppMemory) -> None:
        path = self._path(app)
        tmp_path = f"{path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(memory.to_dict(), f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)

    def record_finalized_many(self, apps: List[str], memories: Dict[str, AppMemory], task: dict) -> None:
        related_apps = task.get("related_apps") if isinstance(task.get("related_apps"), list) else apps
        for app in apps:
            memory = memories.setdefault(app, AppMemory(app=app))
            if app in related_apps:
                memory.record_finalized(task)
            else:
                memory.record_co_use(related_apps)
            self.save(app, memory)
