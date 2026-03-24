# OSWorld 分布式在线 RL 环境系统

基于 Master-Worker 架构的分布式在线 RL 环境系统。Master 网关暴露 `0.0.0.0:10000`，负责会话管理和请求路由；Worker 节点管理本地 Docker 容器，提供 reset/step/evaluate 操作。

## 架构

```
Client ──► Master Gateway (:10000)
              │  (session + routing)
              ├──► Worker-1 (:9100)  ─── [Env0] [Env1] [Env2] [Env3]
              ├──► Worker-2 (:9100)  ─── [Env0] [Env1] [Env2] [Env3]
              └──► Worker-N (:9100)  ─── [Env0] [Env1] ...
```

- **Master**: 纯 HTTP 路由层，无 Docker 依赖，可运行在任意轻量节点
- **Worker**: 管理本地 N 个 DesktopEnv 实例（Docker 容器），需 KVM + Docker
- **Token 会话**: client acquire → 获得 token → 所有后续操作带 token → 路由到同一 worker/env

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 单机部署

```bash
# 启动 Worker（需要 Docker + KVM）
python run_worker.py --config config_worker.yaml --port 9100 &

# 启动 Master
python run_master.py --config config_master.yaml --port 10000 &
```

### 多机部署

在每个 Worker 节点上:
```bash
# 修改 config_worker.yaml 中的 worker_id 和 master_url
python run_worker.py --config config_worker.yaml --port 9100
```

在 Master 节点上:
```bash
# config_master.yaml 中列出所有 worker
python run_master.py --config config_master.yaml --port 10000
```

Worker 也可通过心跳自动注册到 Master（设置 `master_url`），无需在 Master 配置中静态列出。

### 客户端使用

```bash
python client_example.py --master http://localhost:10000
```

## API 接口

### Master Gateway（:10000）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/acquire` | 获取环境，返回 token |
| POST | `/reset` | 重置环境（需 token） |
| POST | `/step` | 执行动作（需 token） |
| POST | `/evaluate` | 评估当前状态（需 token） |
| POST | `/release` | 释放环境（需 token） |
| POST | `/register` | Worker 心跳注册 |
| GET | `/health` | 健康检查 |
| GET | `/workers` | Worker 列表 |

### 请求/响应示例

**Acquire:**
```bash
curl -X POST http://localhost:10000/acquire
```
```json
{"token": "abc123...", "vnc_port": 5900, "worker_url": "http://worker1:9100"}
```

**Reset:**
```bash
curl -X POST http://localhost:10000/reset \
  -H "Content-Type: application/json" \
  -d '{"token": "abc123...", "task_config": {"id": "task-1", "instruction": "Open Firefox"}}'
```
```json
{
  "observation": {
    "screenshot_base64": "iVBOR...",
    "accessibility_tree": "<tree>...</tree>",
    "terminal": null,
    "instruction": "Open Firefox"
  }
}
```

**Step:**
```bash
curl -X POST http://localhost:10000/step \
  -H "Content-Type: application/json" \
  -d '{"token": "abc123...", "action": "pyautogui.click(960, 540)", "pause": 2.0}'
```
```json
{
  "observation": {"screenshot_base64": "...", ...},
  "reward": 0.0,
  "done": false,
  "info": {}
}
```

**Evaluate:**
```bash
curl -X POST http://localhost:10000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"token": "abc123..."}'
```
```json
{"score": 0.85}
```

**Release:**
```bash
curl -X POST http://localhost:10000/release \
  -H "Content-Type: application/json" \
  -d '{"token": "abc123..."}'
```
```json
{"success": true}
```

### Worker 内部接口（:9100）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/worker/health` | 健康检查 |
| GET | `/worker/status` | 环境状态 |
| POST | `/worker/acquire` | 获取本地环境 |
| POST | `/worker/reset` | 重置指定环境 |
| POST | `/worker/step` | 执行动作 |
| POST | `/worker/evaluate` | 评估 |
| POST | `/worker/release` | 释放环境 |

## 配置说明

### config_worker.yaml

```yaml
worker_id: "worker-0"         # Worker 唯一标识
num_envs: 4                   # 本地环境数量
path_to_vm: "/path/to/Ubuntu.qcow2"  # VM 镜像路径
provider_name: "docker"        # 虚拟化 provider
action_space: "pyautogui"      # 动作空间
screen_size: [1920, 1080]      # 屏幕分辨率
headless: true                 # 是否无头模式
session_timeout: 1800          # 会话超时（秒）
# master_url: "http://master:10000"  # 可选: 心跳注册
```

### config_master.yaml

```yaml
workers:                       # 静态 Worker 列表
  - worker_id: "worker-0"
    url: "http://localhost:9100"
    total_envs: 4
    free_envs: 4

session_timeout: 1800          # Token 过期时间（秒）
health_check_interval: 15.0    # 健康检查间隔（秒）
heartbeat_timeout: 120.0       # 心跳超时（秒）
```

## 测试

```bash
# 运行全部单元测试（无需 Docker）
cd ubuntu_online_infra
pytest tests/ -v -k "not e2e"

# 运行端到端测试（in-process，无需 Docker）
pytest tests/test_e2e.py -v

# 全部测试
pytest tests/ -v
```

## 设计决策

- **不采用 K8S**: OSWorld 需要 KVM 直通 + 每 VM 占 4GB RAM，K8S 管理 Docker-in-Docker + KVM 复杂度过高
- **HTTP 转发**: Master 使用 httpx 异步转发到 Worker，timeout=300s 适配 reset/step 慢操作
- **Token 会话**: 简单的 UUID token，线程安全的内存映射，自动过期清理
- **负载均衡**: 选择 free_envs 最多的健康 Worker，失败自动尝试下一个
- **健康检查**: 每 15s 探测所有 Worker，3 次连续失败标记 unhealthy
