#!/usr/bin/env python3
"""
客户端使用示例 — 演示完整的 acquire → reset → step → evaluate → release 流程。

使用方式:
    python client_example.py --master http://localhost:10000
"""

import argparse
import json
import sys

import httpx


def main():
    parser = argparse.ArgumentParser(description="OSWorld Client Example")
    parser.add_argument(
        "--master", default="http://localhost:10000", help="Master gateway URL"
    )
    args = parser.parse_args()

    base = args.master.rstrip("/")

    with httpx.Client(timeout=300.0) as client:
        # 1. Acquire environment
        print("[1] Acquiring environment...")
        resp = client.post(f"{base}/acquire")
        resp.raise_for_status()
        data = resp.json()
        token = data["token"]
        print(f"    Token: {token}")
        print(f"    VNC port: {data['vnc_port']}")
        print(f"    Worker: {data['worker_url']}")

        try:
            # 2. Reset with a task config
            print("\n[2] Resetting environment...")
            resp = client.post(
                f"{base}/reset",
                json={
                    "token": token,
                    "task_config": {
                        "id": "example-task",
                        "instruction": "Open Firefox and navigate to google.com",
                    },
                },
            )
            resp.raise_for_status()
            obs = resp.json()["observation"]
            print(f"    Instruction: {obs.get('instruction')}")
            print(
                f"    Screenshot: {'present' if obs.get('screenshot_base64') else 'none'}"
                f" ({len(obs.get('screenshot_base64', '') or '')} chars)"
            )

            # 3. Execute a few steps
            actions = [
                "pyautogui.click(960, 540)",
                "pyautogui.typewrite('hello', interval=0.05)",
                "DONE",
            ]
            for i, action in enumerate(actions, 1):
                print(f"\n[3.{i}] Step: {action}")
                resp = client.post(
                    f"{base}/step",
                    json={"token": token, "action": action, "pause": 1.0},
                )
                resp.raise_for_status()
                step_data = resp.json()
                print(f"    Reward: {step_data['reward']}, Done: {step_data['done']}")
                if step_data["done"]:
                    break

            # 4. Evaluate
            print("\n[4] Evaluating...")
            resp = client.post(f"{base}/evaluate", json={"token": token})
            resp.raise_for_status()
            score = resp.json()["score"]
            print(f"    Score: {score}")

        finally:
            # 5. Release
            print("\n[5] Releasing environment...")
            resp = client.post(f"{base}/release", json={"token": token})
            resp.raise_for_status()
            print("    Released successfully.")

    print("\nDone!")


if __name__ == "__main__":
    main()
