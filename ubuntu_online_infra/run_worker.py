#!/usr/bin/env python3
"""Worker startup script."""

import argparse
import sys
from pathlib import Path

# Ensure project root is on sys.path for desktop_env imports
_project_root = str(Path(__file__).resolve().parents[1])
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Ensure ubuntu_online_infra is on sys.path
_infra_root = str(Path(__file__).resolve().parent)
if _infra_root not in sys.path:
    sys.path.insert(0, _infra_root)

import yaml
import uvicorn

from worker.app import create_app, load_config


def main():
    parser = argparse.ArgumentParser(description="OSWorld Worker")
    parser.add_argument(
        "--config", default="config_worker.yaml", help="Path to worker config YAML"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=9100, help="Bind port")
    args = parser.parse_args()

    config = load_config(args.config)
    config["port"] = args.port

    app = create_app(config=config)
    uvicorn.run(app, host=args.host, port=args.port, workers=1)


if __name__ == "__main__":
    main()
