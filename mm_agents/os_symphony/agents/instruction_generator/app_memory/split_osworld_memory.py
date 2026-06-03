#!/usr/bin/env python3
"""Split OSWorld app memory into per-app memory files.

The source file is expected to be a mapping from app name to memory payload:

{
  "blender": {
    "covered_features": {...},
    "verification_experience": {...}
  }
}

For each app, this script creates or updates ``{app}.json`` in the same
directory. Existing per-app files keep their existing fields; only
``covered_features`` and ``verification_experience`` are merged from the source.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


APP_MEMORY_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = APP_MEMORY_DIR / "osworld_app_memory.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")

    return data


def dump_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def default_app_memory(app_name: str) -> dict[str, Any]:
    return {
        "app": app_name,
        "covered_features": {},
        "recent_tasks": [],
        "co_use_counts": {},
        "verification_experience": {},
    }


def merge_covered_features(
    existing: dict[str, Any],
    incoming: dict[str, Any],
    *,
    add_counts: bool,
) -> dict[str, Any]:
    merged = dict(existing)

    for feature, value in incoming.items():
        if (
            add_counts
            and feature in merged
            and isinstance(merged[feature], (int, float))
            and isinstance(value, (int, float))
        ):
            merged[feature] += value
        else:
            merged[feature] = value

    return merged


def merge_verification_experience(
    existing: dict[str, Any],
    incoming: dict[str, Any],
) -> dict[str, Any]:
    merged = dict(existing)

    for feature, experience in incoming.items():
        if feature not in merged:
            merged[feature] = experience
            continue

        if isinstance(merged[feature], list) and isinstance(experience, list):
            seen = set()
            deduped = []
            for item in [*merged[feature], *experience]:
                marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if marker not in seen:
                    seen.add(marker)
                    deduped.append(item)
            merged[feature] = deduped
        else:
            merged[feature] = experience

    return merged


def split_memory(source_path: Path, output_dir: Path, *, add_counts: bool) -> list[Path]:
    source = load_json(source_path)
    written_paths: list[Path] = []

    for app_name, app_payload in source.items():
        if not isinstance(app_payload, dict):
            raise ValueError(f"memory entry for {app_name!r} must be a JSON object")

        target_path = output_dir / f"{app_name}.json"
        if target_path.exists():
            target = load_json(target_path)
        else:
            target = default_app_memory(app_name)

        target.setdefault("app", app_name)
        target.setdefault("covered_features", {})
        target.setdefault("recent_tasks", [])
        target.setdefault("co_use_counts", {})
        target.setdefault("verification_experience", {})

        covered_features = app_payload.get("covered_features", {})
        verification_experience = app_payload.get("verification_experience", {})

        if not isinstance(covered_features, dict):
            raise ValueError(f"covered_features for {app_name!r} must be a JSON object")
        if not isinstance(verification_experience, dict):
            raise ValueError(
                f"verification_experience for {app_name!r} must be a JSON object"
            )
        if not isinstance(target["covered_features"], dict):
            raise ValueError(f"{target_path} covered_features must be a JSON object")
        if not isinstance(target["verification_experience"], dict):
            raise ValueError(
                f"{target_path} verification_experience must be a JSON object"
            )

        target["covered_features"] = merge_covered_features(
            target["covered_features"],
            covered_features,
            add_counts=add_counts,
        )
        target["verification_experience"] = merge_verification_experience(
            target["verification_experience"],
            verification_experience,
        )

        dump_json(target_path, target)
        written_paths.append(target_path)

    return written_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split osworld_app_memory.json into per-app memory files."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Source JSON path. Defaults to {DEFAULT_SOURCE}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=APP_MEMORY_DIR,
        help=f"Directory for per-app JSON files. Defaults to {APP_MEMORY_DIR}",
    )
    parser.add_argument(
        "--add-counts",
        action="store_true",
        help=(
            "When a covered feature already exists and both values are numeric, "
            "add the counts instead of replacing the existing value."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    written_paths = split_memory(
        args.source.resolve(),
        args.output_dir.resolve(),
        add_counts=args.add_counts,
    )

    print(f"Wrote {len(written_paths)} app memory files:")
    for path in written_paths:
        print(f"- {path}")


if __name__ == "__main__":
    main()
