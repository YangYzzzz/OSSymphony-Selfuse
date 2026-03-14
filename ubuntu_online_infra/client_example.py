#!/usr/bin/env python3
"""
客户端并发测试示例 — 演示多个客户端并发执行 acquire → reset → step → evaluate → release 流程。

使用方式:
    python client_example.py --master http://localhost:10000 --concurrency 5
"""

import argparse
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx


# 固定的任务配置
TASK_CONFIG = {
    "id": "0d8b7de3-e8de-4d86-b9fd-dd2dce58a217",
    "instruction": "Browse the natural products database.",
    "config": [
        {
            "type": "launch",
            "parameters": {
                "command": [
                    "google-chrome",
                    "--remote-debugging-port=1337"
                ]
            }
        },
        {
            "type": "launch",
            "parameters": {
                "command": [
                    "socat",
                    "tcp-listen:9222,fork",
                    "tcp:localhost:1337"
                ]
            }
        },
        {
            "type": "chrome_open_tabs",
            "parameters": {
                "urls_to_open": [
                    "https://drugs.com"
                ]
            }
        },
        {
            "type": "activate_window",
            "parameters": {
                "window_name": "Google Chrome"
            }
        }
    ],
    "evaluator": {
        "func": [
            "is_expected_active_tab",
            "is_expected_active_tab"
        ],
        "conj": "or",
        "result": [
            {
                "type": "active_url_from_accessTree",
                "goto_prefix": "https://www."
            },
            {
                "type": "active_url_from_accessTree",
                "goto_prefix": "https://www."
            }
        ],
        "expected": [
            {
                "type": "rule",
                "rules": {
                    "type": "url",
                    "url": "https://www.drugs.com/npc/"
                }
            },
            {
                "type": "rule",
                "rules": {
                    "type": "url",
                    "url": "https://www.drugs.com/npp/"
                }
            }
        ]
    }
}

# 固定的动作序列
ACTIONS = [
    "pyautogui.click(960, 540)",
    "pyautogui.write('hello', interval=0.05)",
    "DONE",
]


class TestClient:
    """测试客户端类，封装单个测试会话"""
    
    def __init__(self, client_id: int, master_url: str):
        self.client_id = client_id
        self.master_url = master_url.rstrip("/")
        self.token = None
        self.worker_url = None
        self.vnc_port = None
        
        # 设置日志格式，带客户端标识
        self._setup_logging()
        
    def _setup_logging(self):
        """为每个客户端设置带标识的日志格式"""
        self.logger = logging.getLogger(f"Client-{self.client_id}")
        self.logger.setLevel(logging.DEBUG)
        
        # 如果已经有处理器，避免重复添加
        if not self.logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            
            # 带客户端ID的格式化器
            formatter = logging.Formatter(
                f'[Client-{self.client_id:03d} %(asctime)s] %(levelname)s: %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
    
    def run(self) -> dict:
        """
        运行完整的测试流程
        
        Returns:
            dict: 测试结果统计
        """
        start_time = time.time()
        result = {
            "client_id": self.client_id,
            "success": False,
            "score": None,
            "steps_executed": 0,
            "error": None,
            "duration": 0
        }
        
        try:
            with httpx.Client(timeout=300.0) as client:
                # 1. Acquire environment
                self.logger.info("步骤1: 获取环境...")
                while not self.token:
                    resp = client.post(f"{self.master_url}/acquire")
                    if resp.status_code == 200:
                        data = resp.json()
                        self.token = data["token"]
                        self.worker_url = data["worker_url"]
                        self.vnc_port = data["vnc_port"]
                        self.logger.info(f"获取成功 - Token: {self.token[:8]}..., VNC端口: {self.vnc_port}")
                        break
                    else:
                        time.sleep(5)
                
                # 2. Reset with task config
                self.logger.info("步骤2: 重置环境并加载任务...")
                resp = client.post(
                    f"{self.master_url}/reset",
                    json={"token": self.token, "task_config": TASK_CONFIG},
                )
                resp.raise_for_status()
                obs = resp.json()["observation"]
                self.logger.info(f"任务加载完成 - 指令: {obs.get('instruction', 'N/A')[:50]}...")
                
                # 3. Execute steps
                self.logger.info(f"步骤3: 执行动作序列 (共{len(ACTIONS)}个动作)...")
                for i, action in enumerate(ACTIONS, 1):
                    self.logger.info(f"  执行动作 {i}/{len(ACTIONS)}: {action[:50]}...")
                    
                    step_start = time.time()
                    resp = client.post(
                        f"{self.master_url}/step",
                        json={"token": self.token, "action": action, "pause": 1.0},
                    )
                    resp.raise_for_status()
                    step_data = resp.json()
                    step_duration = time.time() - step_start
                    
                    self.logger.debug(f"  动作结果 - 奖励: {step_data['reward']}, 完成: {step_data['done']}, 耗时: {step_duration:.2f}s")
                    
                    result["steps_executed"] = i
                    
                    if step_data["done"]:
                        self.logger.info(f"  动作序列提前结束于第{i}步")
                        break
                
                # 4. Evaluate
                self.logger.info("步骤4: 评估任务完成情况...")
                resp = client.post(f"{self.master_url}/evaluate", json={"token": self.token})
                resp.raise_for_status()
                score = resp.json()["score"]
                result["score"] = score
                self.logger.info(f"评估完成 - 得分: {score}")
                
                result["success"] = True
                
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP错误: {e.response.status_code} - {e.response.text}, 需要重新测试"
            self.logger.error(error_msg)
            result["error"] = error_msg
        except httpx.RequestError as e:
            error_msg = f"请求错误: {str(e)}"
            self.logger.error(error_msg)
            result["error"] = error_msg
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            result["error"] = error_msg
        finally:
            # 5. Release
            if self.token:
                self.logger.info("步骤5: 释放环境...")
                try:
                    with httpx.Client() as client:
                        resp = client.post(f"{self.master_url}/release", json={"token": self.token})
                        resp.raise_for_status()
                        self.logger.info("环境释放成功")
                except Exception as e:
                    self.logger.error(f"环境释放失败: {e}")
            
            # 记录总耗时
            result["duration"] = time.time() - start_time
            self.logger.info(f"测试完成 - 状态: {'成功' if result['success'] else '失败'}, 耗时: {result['duration']:.2f}s")
        
        return result


def print_summary(results: list, total_time: float):
    """打印测试结果汇总"""
    print("\n" + "="*80)
    print("测试结果汇总")
    print("="*80)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"总并发数: {len(results)}")
    print(f"成功: {len(successful)}")
    print(f"失败: {len(failed)}")
    print(f"总耗时: {total_time:.2f}s")
    
    if successful:
        avg_score = sum(r["score"] for r in successful if r["score"] is not None) / len(successful)
        avg_duration = sum(r["duration"] for r in successful) / len(successful)
        avg_steps = sum(r["steps_executed"] for r in successful) / len(successful)
        print(f"\n成功客户端统计:")
        print(f"  平均得分: {avg_score:.2f}")
        print(f"  平均耗时: {avg_duration:.2f}s")
        print(f"  平均步数: {avg_steps:.1f}")
    
    if failed:
        print(f"\n失败客户端统计:")
        for i, result in enumerate(failed, 1):
            print(f"  {i}. 客户端 #{result['client_id']}: {result['error']}")
    
    print("="*80)


def main():
    parser = argparse.ArgumentParser(description="OSWorld 并发测试客户端")
    parser.add_argument(
        "--master", default="http://localhost:10001", help="Master gateway URL"
    )
    parser.add_argument(
        "--concurrency", "-n", type=int, default=2, help="并发客户端数量"
    )
    args = parser.parse_args()
    
    print(f"Master URL: {args.master}")
    print(f"并发数: {args.concurrency}")
    print(f"任务指令: {TASK_CONFIG['instruction']}")
    print(f"动作序列: {len(ACTIONS)}个动作")
    print("-" * 60)
    
    # 准备测试客户端
    clients = [
        TestClient(i + 1, args.master)
        for i in range(args.concurrency)
    ]
    
    # 记录开始时间
    overall_start = time.time()
    results = []
    
    # 使用线程池执行并发测试
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        # 提交所有任务
        futures = [executor.submit(client.run) for client in clients]
        
        # 收集结果
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                # 实时输出进度
                print(f"\n[进度] 完成 {len(results)}/{args.concurrency}")
            except Exception as e:
                print(f"任务执行异常: {e}")
    
    overall_duration = time.time() - overall_start
    
    # 打印汇总
    print_summary(results, overall_duration)


if __name__ == "__main__":
    main()