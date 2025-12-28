# <img src="./assets/logo.jpg" alt="overview" style="width:40%; display: block; margin: 0 auto;" />OS-Symphony

[![arXiv](https://img.shields.io/badge/arXiv-2412.19723-b31b1b.svg)]() ![License](https://img.shields.io/badge/License-MIT-blue)[![🌐 Website](https://img.shields.io/badge/Website-🌐-informational)]()

**论文官方代码库: [OS-Symphony: Orchestrating Desktop Agents via Reflection and Specialized Tools]()**

## 🗞️ Updates

- **[2025-12-xx]** 🎉 我们发布了论文的初版、[代码库](https://poe.com/chat/=sg6buzpq43nnktzho)以及[项目主页](https://poe.com/chat/=sg6buzpq43nnktzho)。

## 💡 Overview

我们提出了 **OS-Symphony**，这是一个鲁棒的桌面端计算机使用智能体框架。该框架通过统一的 *反思消息协议（Reflection Message Protocol）*，有机地集成了中央**编排器（Orchestrator）**、**反思记忆智能体（Reflection-Memory Agent）**以及专用的**工具智能体（Tool-Agents）**。这种设计旨在最大限度地减少长程任务中的误差累积，同时提升系统的整体能力和适应性。

## 📊 Results

- [ ] **TODO**: 详细的评测结果即将更新。

## 🛠️ Environment & Setup

> **注意：** 为了保证评测的可复现性与稳定性，我们目前**仅支持基于 Docker 的评测环境**。其他部署方式可能会存在未知的环境兼容性问题。

### 1. 安装依赖

配置运行时虚拟环境并安装必要的浏览器引擎：

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 下载 Playwright 浏览器内核
playwright install
```

### 2. 虚拟机配置

配置评测虚拟机环境是至关重要的一步。请务必参考 **[SETUP_zh.md](SETUP_zh.md)** 下载资源并完成 Linux、Windows 和 MacOS 黄金镜像（Golden Image）的配置。

### 3. 启动评测

使用提供的 Shell 脚本开启实验。运行前请修改 `crucial_scripts/run_os_symphony.sh` 中的参数以适配您的评测需要。

```bash
bash crucial_scripts/run_os_symphony.sh
```

**关键参数说明：**

#### 🖥️ 环境相关 (Environment)

| 参数名                | 说明                                                         |
| :-------------------- | :----------------------------------------------------------- |
| `path_to_vm`          | 虚拟机黄金镜像路径。<br>⚠️ **MacOSArena 特殊说明：** 需配置两个路径，以空格分隔：`"/path/to/mac_hdd_ng.img /path/to/BaseSystem.img"` |
| `searcher_path_to_vm` | 搜索环境镜像路径，通常为 `/path/to/Ubuntu.qcow2`。           |
| `num_envs`            | 多进程并发评测的数量。                                       |
| `proxy`               | 网络代理地址（格式：`http://<ip>:<port>`），评测 OSWorld 和 WindowsAgentArena 时必需。 |
| `client_password`     | 虚拟机登录密码。OSWorld 为 `"password"`，MacOSArena 为 `"1234"`。 |

#### 🤖 Agent 相关

| 参数名                                                      | 说明                                                         |
| :---------------------------------------------------------- | :----------------------------------------------------------- |
| `xx_provider，xx_model，xx_url，xx_api_key，xx_temperature` | VLM 调用配置（支持 OpenAI 格式 API）。开源模型推荐使用 **vLLM** 部署。 |
| `coder_budget`, `searcher_budget`                           | Coder Agent 和 Searcher Agent 允许的最大内循环次数。         |
| `searcher_engine`                                           | 搜索引擎配置。推荐使用 `duckduckgo`，Google 在高频访问下容易触发验证码拦截。 |
| `memoryer_max_images`                                       | RMA 模块中能容纳的最大图片数量。                             |
| `grounding_smart_resize`                                    | 是否启用智能缩放。GTA1-32B, ScaleCUA, UI-TARS-1.5 等模型需要开启此项。 |
| `orchestrator_keep_first_image`                             | 是否始终保留初始截图在上下文中（默认开启）。                 |
| `tool_config`                                               | 动作空间配置，支持动态装配工具。                             |

#### 🧪 实验相关 (Experiment)

| 参数名              | 说明                                                   |
| :------------------ | :----------------------------------------------------- |
| `exp_name`          | 实验名称，决定了结果的保存路径。                       |
| `enable_reflection` | 是否启用反思记忆智能体（RMA）模块。                    |
| `max_steps`         | 单次评测允许的最大步数。                               |
| `benchmark`         | 评测基准选择，可选：`osworld` / `waa` / `macosarena`。 |

### 4. 结果可视化

实验结果保存在 `results/{exp_name}` 目录下，日志保存在 `logs/{exp_name}.log` 中。

您可以运行以下命令启动 Gradio Web UI，一键生成统计信息并可视化查看执行过程：

```bash
python gradio/gradio_show_result.py --root_dir results/{exp_name} --port 10000
```

## ✨ Features

1. **统一的跨平台评测：** 我们将三个主流 OS 平台（Linux/Windows/MacOS）的评测通过统一接口进行封装，极大简化了跨平台评测流程。
2. **增强的鲁棒性：** 我们修复了原各个评测 Codebase 中存在的诸多环境不稳定与评测 Bug，提供了更稳健的实验环境。
3. **高扩展性：** 支持用户自定义更多的任务。
4. **自定义工作流：** 支持自定义 Agent 工作流与工具配置。

欢迎社区使用我们的代码库进行您的 Agent 任务评测。

## 😊 Acknowledgement

感谢以下出色工作为 Computer Use 领域做出的杰出贡献：
 [OSWorld](https://github.com/xlang-ai/OSWorld), [WindowsAgentArena](https://github.com/xlang-ai/OSWorld), [MacOSArena](https://github.com/xlang-ai/OSWorld), [AgentS3](https://github.com/xlang-ai/OSWorld), [UI-TARS](https://github.com/xlang-ai/OSWorld), [GTA1](https://github.com/xlang-ai/OSWorld), [ScaleCUA](https://github.com/xlang-ai/OSWorld) 等。

## 📃 Citation

如果您觉得本项目对您的研究有帮助，请引用我们的论文：

```tex
@article{ossymphony2025,
  title={OS-Symphony: Orchestrating Desktop Agents via Reflection and Specialized Tools},
  author={Author One and Author Two and Author Three},
  journal={arXiv preprint arXiv:2512.xxxxx},
  year={2025}
}
```
