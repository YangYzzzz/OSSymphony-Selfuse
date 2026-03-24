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
    parser.add_argument("--port", type=int, help="Bind port")
    parser.add_argument("--session-timeout", type=int, help="Session timeout in seconds")
    parser.add_argument("--health-check-interval", type=float, help="Health check interval in seconds")
    parser.add_argument("--heartbeat-timeout", type=float, help="Heartbeat timeout in seconds")

    args = parser.parse_args()

    # Load YAML config
    config = load_config(args.config)

    # CLI overrides
    if args.port is not None:
        config["port"] = args.port
    if args.session_timeout is not None:
        config["session_timeout"] = args.session_timeout
    if args.health_check_interval is not None:
        config["health_check_interval"] = args.health_check_interval
    if args.heartbeat_timeout is not None:
        config["heartbeat_timeout"] = args.heartbeat_timeout

    app = create_app(config=config)
    uvicorn.run(app, host=args.host, port=config["port"], workers=1) # Not sure workers > 1 whether will occur a bug?


if __name__ == "__main__":
    main()
