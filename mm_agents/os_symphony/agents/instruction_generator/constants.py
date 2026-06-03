from __future__ import annotations

import os
from typing import Any, Dict, List

APP_MEMORY_DIR = os.path.join(
    "mm_agents",
    "os_symphony",
    "agents",
    "instruction_generator",
    "app_memory",
)

ALLOWED_GETTER_TYPES = {"vm_file", "vm_command_line", "empty"}
DANGEROUS_IMPORTS = {"subprocess", "socket", "requests", "urllib", "httpx", "shutil", "pathlib"}
DANGEROUS_CALLS = {"system", "popen", "remove", "unlink", "rmdir", "removedirs", "rename", "write", "writelines"}

PROPOSAL_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "proposals": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "proposal_id": {"type": "string"},
                    "instruction": {"type": "string"},
                    "config": {"type": "array"},
                    "related_apps": {"type": "array", "items": {"type": "string"}},
                    "used_files": {"type": "array", "items": {"type": "string"}},
                    "category": {"type": "string"},
                    "complexity": {"type": "string"},
                    "estimated_steps": {"type": "integer"},
                    "target_features": {
                        "type": "object",
                        "additionalProperties": {"type": "array", "items": {"type": "string"}},
                    },
                    "success_criteria": {"type": "array", "items": {"type": "string"}},
                    "evaluation_requirements_text": {"type": "array", "items": {"type": "string"}},
                    "dependency_chain": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "step": {"type": "integer"},
                                "source_app": {"type": "string"},
                                "source": {"type": "string"},
                                "operation": {"type": "string"},
                                "target_app": {"type": "string"},
                                "target": {"type": "string"},
                                "verification_anchor": {"type": "string"},
                            },
                        },
                    },
                    "risk_notes": {"type": "array", "items": {"type": "string"}},
                },
                "required": [
                    "proposal_id",
                    "instruction",
                    "config",
                    "related_apps",
                    "used_files",
                    "category",
                    "complexity",
                    "estimated_steps",
                    "target_features",
                    "success_criteria",
                    "evaluation_requirements_text",
                    "dependency_chain",
                    "risk_notes",
                ],
            },
        },
        "generation_notes": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["proposals"],
    "additionalProperties": False,
}

EXPLORATION_PROPOSAL_TOOL_SCHEMA: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "open",
            "description": "Use a sampled application to open a sampled file, or open an empty app window, through desktop_env.controller.run_bash_script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app": {"type": "string", "description": "One app from sampled_apps."},
                    "path": {"type": "string", "description": "One path from sampled_files, or empty for app-only exploration."},
                },
                "required": ["app"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "click",
            "description": "Click a screen coordinate for non-destructive UI inspection.",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}},
                "required": ["x", "y"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scroll",
            "description": "Scroll for non-destructive UI inspection.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "integer", "description": "Positive scrolls up, negative scrolls down."},
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                },
                "required": ["amount"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "done",
            "description": "Finish exploration and return grounded task proposals generated from the full visual trajectory.",
            "parameters": PROPOSAL_SCHEMA,
        },
    },
]
