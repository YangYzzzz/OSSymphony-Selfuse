# CUA Benchmark 评测与数据采集指南

本仓库统一支持 CUA Benchmark 评测与轨迹数据采集，覆盖以下任务集：

| 类型 | 支持的数据集 |
| --- | --- |
| Benchmark 评测 | OSWorld、OSWorld-V2、WindowsAgentArena、WeaveBench |
| 数据采集 | Any Tasks（自定义任务） |

数据采集流程可以同时执行任务评测。核心入口为 [`os_caliber_rollout_trajectory.py`](../os_caliber_rollout_trajectory.py)。

> [!NOTE]
> 当前对 Claude 和 Qwen 系列模型的支持最完善。其他模型也具备不同程度的兼容性，具体可参考代码中的模型路由实现。

配置任务最重要是以下两个参数：

| 参数 | 说明 |
| --- | --- |
| `--rollout_test_all_meta_path` | 任务 ID 列表 |
| `--rollout_task_dir` | 任务文件所在目录 |

以 OSWorld 为例：

```bash
--rollout_test_all_meta_path evaluation_examples/osworld/test_nogdrive.json \
--rollout_task_dir evaluation_examples/osworld/examples/
```

## OSWorld 及其他标准格式任务

除 OSWorld-V2 外，其余任务均已统一为类 OSWorld 数据格式。

### 统一任务格式

标准格式任务具有以下特点：

1. 每个任务均以 JSON 文件描述。
2. 任务所需的 setup 文件、golden 文件及其他资源均可直接获取：
   - 本地资源可参考 CUA-Gym 任务；
   - 远程资源可参考 OSWorld 任务，首次运行时从 Hugging Face 下载并写入缓存，后续运行无需重复下载。
3. 完成任务配置后即可直接启动采集或评测，无需额外转换。

OSWorld v1 的完整启动示例见 [`start_osworld_v1.sh`](start_osworld_v1.sh)。

> [!IMPORTANT]
> OSWorld 虚拟机镜像需要根据官方说明自行下载。

## OSWorld-V2

与标准 JSON 任务相比，OSWorld-V2 主要有三点差异：

1. 任务以 Python 文件定义，并可包含自定义 `setup`、`evaluate` 等函数。
2. 为降低评测数据泄露风险，setup 等相关资源无法在运行时直接从 Hugging Face 下载，必须提前保存到本机缓存。
3. Benchmark 使用了十余个 Mock 网站。除 GitLab 外，其余网站可直接通过 HKU 部署的公网服务进行评测。

当前代码已支持动态解析 Python 格式任务。启动时增加以下参数即可启用 OSWorld-V2 适配：

```bash
--benchmark "osworld-v2"
```

### 1. 下载 OSWorld-V2 Assets

按照 [OSWorld-V2 官方仓库](https://github.com/xlang-ai/OSWorld-V2)的说明，提前下载任务所需资源：

```bash
# 该文件在OSWorld-v2仓库内
uv run scripts/tools/download_osworld_v2_assets.py \
  --benchmark-release osworld-v2-2026.08.08 \
  --target-dir cache/osworld_v2_assets \
  --clean
```

随后在启动参数中指定缓存目录：

```bash
--cache_dir "cache/osworld_v2_assets"
```

### 2. 配置 GitLab 服务

参考 [Task-Web GitLab 部署仓库](https://github.com/Task-Web/gitlab)自行部署 GitLab，并导出以下环境变量：

```bash
export GITLAB_URL="http://<your-ip>.sslip.io"
export GITLAB_PRIVATE_TOKEN="<your-private-token>"
```

GitLab 仅用于其中两个任务。如果无需运行这两个任务，可以暂不配置。

### 3. 启动评测或采集

OSWorld-V2 的完整启动示例见 [`start_osworld_v2.sh`](start_osworld_v2.sh)。运行前请确认：

- 已按照 OSWorld-V2 官方说明准备虚拟机镜像；
- `--benchmark` 已设置为 `osworld-v2`；
- `--cache_dir` 指向已下载的 Assets；
- 如需执行 GitLab 任务，已正确设置 `GITLAB_URL` 和 `GITLAB_PRIVATE_TOKEN`。

> [!IMPORTANT]
> OSWorld-v2 虚拟机镜像需要根据官方说明自行下载。

> 评估过程中若遇到代理问题，需手动去除一下 `desktop_env/osworld` 下面 Hard Code 的代理配置(可检索**10.1.8.5:23128**)
