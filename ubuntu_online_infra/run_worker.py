#!/usr/bin/env python3
"""Worker startup script."""

import argparse
import logging
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

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"                                                                             
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
                                                                                                                                            
logging.basicConfig(                                      
    level=logging.INFO,                                                                                                                       
    format=LOG_FORMAT,                                    
    datefmt=DATE_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)],
) 

def main():
    parser = argparse.ArgumentParser(description="OSWorld Worker")
    parser.add_argument(
        "--config", default="config_worker.yaml", help="Path to worker config YAML"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, help="Bind port")
    parser.add_argument("--worker-id", help="Worker ID")
    parser.add_argument("--num-envs", type=int, help="Number of environments")
    parser.add_argument("--master-url", help="Master gateway URL")
    parser.add_argument("--worker-url", help="Worker URL for registration")

    args = parser.parse_args()

    # Load YAML config
    config = load_config(args.config)

    # CLI overrides
    if args.port is not None:
        config["port"] = args.port
    if args.worker_id is not None:
        config["worker_id"] = args.worker_id
    if args.num_envs is not None:
        config["num_envs"] = args.num_envs
    if args.master_url is not None:
        config["master_url"] = args.master_url
    if args.worker_url is not None:
        config["worker_url"] = args.worker_url

    app = create_app(config=config)
    uvicorn.run(app, host=args.host, port=config["port"], workers=1)


if __name__ == "__main__":
    main()
