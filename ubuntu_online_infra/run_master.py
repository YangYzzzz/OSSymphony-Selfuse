#!/usr/bin/env python3
"""Master Gateway startup script."""

import argparse
import sys
from pathlib import Path

# Ensure ubuntu_online_infra is on sys.path
_infra_root = str(Path(__file__).resolve().parent)
if _infra_root not in sys.path:
    sys.path.insert(0, _infra_root)

import yaml
import uvicorn

from gateway.app import create_app


def load_config(path: str):
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="OSWorld Master Gateway")
    parser.add_argument(
        "--config", default="config_master.yaml", help="Path to master config YAML"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=10000, help="Bind port")
    args = parser.parse_args()

    config = load_config(args.config)
    app = create_app(config=config)
    uvicorn.run(app, host=args.host, port=args.port, workers=1)


if __name__ == "__main__":
    main()
