"""
Initial Setup: Set up a protobuf/gRPC development workflow in ~/project on VSCode
Task ID: vscode_wf_085
Domain: vscode

Creates an empty Python gRPC project structure with VSCode open.
No proto files, no .vscode configs, no proto3 extension installed.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/project'

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # Create a basic Python gRPC project (no proto files, no vscode config)
    # requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write("""grpcio==1.62.0
grpcio-tools==1.62.0
protobuf==4.25.3
grpcio-reflection==1.62.0
grpcio-health-checking==1.62.0
pytest==8.0.2
""")

    # Basic server.py skeleton (no gRPC service impl yet)
    with open(os.path.join(PROJECT_DIR, 'src', 'server.py'), 'w') as f:
        f.write('''"""
gRPC Server - Inventory Management Service
"""

import logging
from concurrent import futures

import grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER_PORT = "50051"


def serve():
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # TODO: Add service implementations here after proto compilation
    server.add_insecure_port(f"[::]:{SERVER_PORT}")
    server.start()
    logger.info("gRPC server started on port %s", SERVER_PORT)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
''')

    # Basic client.py skeleton
    with open(os.path.join(PROJECT_DIR, 'src', 'client.py'), 'w') as f:
        f.write('''"""
gRPC Client - Inventory Management Service
"""

import grpc

SERVER_ADDRESS = "localhost:50051"


def run():
    """Connect to the gRPC server and make requests."""
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    # TODO: Create stubs after proto compilation
    print("Client connected to", SERVER_ADDRESS)


if __name__ == "__main__":
    run()
''')

    # __init__.py files
    with open(os.path.join(PROJECT_DIR, 'src', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(PROJECT_DIR, 'tests', '__init__.py'), 'w') as f:
        f.write('')

    # Basic test file
    with open(os.path.join(PROJECT_DIR, 'tests', 'test_server.py'), 'w') as f:
        f.write('''"""
Tests for gRPC server.
"""

import pytest


def test_server_starts():
    """Placeholder test - implement after proto compilation."""
    # TODO: Test server startup after service.proto is compiled
    assert True


def test_client_connection():
    """Placeholder test - implement after proto compilation."""
    # TODO: Test client can connect after service.proto is compiled
    assert True
''')

    # Makefile for project
    with open(os.path.join(PROJECT_DIR, 'Makefile'), 'w') as f:
        f.write('''PROTO_DIR = proto
GEN_DIR = src/generated

.PHONY: install clean test

install:
\tpip install -r requirements.txt

clean:
\trm -rf $(GEN_DIR)/*.py
\tfind . -name "__pycache__" -exec rm -rf {} +

test:
\tpytest tests/ -v
''')

    print(f'Initial project created at: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
