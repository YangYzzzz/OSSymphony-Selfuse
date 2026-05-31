from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class GenerationContext:
    rollout_id: str
    sampled_apps: List[str]
    app_file_support: Dict[str, List[str]]
    sampled_files: List[Dict[str, Any]]
    app_tutorials: Dict[str, str]
    app_memory: Dict[str, Any]
    app_versions: Dict[str, str]
    app_open_commands: Dict[str, List[List[str]]]
    observation: Dict[str, Any]
    setup_image: bytes
    initial_config: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def candidate_file_paths(self) -> List[str]:
        paths: List[str] = []
        for item in self.sampled_files:
            if isinstance(item, dict) and item.get("path"):
                paths.append(str(item["path"]))
        return paths
