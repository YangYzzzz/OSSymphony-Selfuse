

# <img src="D:/AILab/Computer Use Framework and RL/InternGUIFramework/assets/logo.jpg" alt="overview" style="width:40%; display: block; margin: 0 auto;" /> OS-Symphony

**Official repository for the paper: [OS-Symphony: Orchestrating Desktop Agents via Reflection and Specialized Tools]()**

[![arXiv](https://img.shields.io/badge/arXiv-2412.19723-b31b1b.svg)]() ![License](https://img.shields.io/badge/License-MIT-blue)[![🌐 Website](https://img.shields.io/badge/Website-🌐-informational)]()

## 🗞️ Updates

- **[2025-12-xx]** 🎉 We have released the initial version of our [paper](), [code](), and [project page]().

## 💡 Overview

We propose **OS-Symphony**, a robust desktop Computer Use Agent (CUA) framework. It organically integrates a central **Orchestrator**, a **Reflection-Memory Agent (RMA)**, and specialized **Tool-Agents** through a unified *Reflection Message Protocol*. This architecture is designed to minimize error accumulation across long-horizon tasks while maximizing overall capability and adaptability.

## 📊 Results

- [ ] **TODO**: Detailed benchmark results will be updated soon.

## 🛠️ Environment & Setup

> **Note:** To ensure reproducibility and stability, we currently **exclusively support Docker-based evaluation**. Other deployment methods may encounter undefined compatibility issues.

### 1. Installation

Set up the runtime virtual environment and install the necessary browser engines:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install
```

### 2. VM Configuration

Configuring the Virtual Machine environments is a critical step. Please strictly follow the instructions in **[SETUP.md](SETUP.md)** to download resources and configure the Golden Images for Linux, Windows, and MacOS.

### 3. Running Evaluation

Launch the evaluation using the provided shell script. You will need to modify the parameters in `crucial_scripts/run_os_symphony.sh` to match your experiments.

```bash
bash crucial_scripts/run_os_symphony.sh
```

**Key Configuration Parameters:**

#### 🖥️ Environment Settings

| Parameter             | Description                                                  |
| :-------------------- | :----------------------------------------------------------- |
| `path_to_vm`          | Path to the VM Golden Image.<br>⚠️ **For MacOSArena:** Must be two paths separated by a space: `"/path/to/mac_hdd_ng.img /path/to/BaseSystem.img"` |
| `searcher_path_to_vm` | Path to the Linux Search Environment image (`/path/to/Ubuntu.qcow2`). |
| `num_envs`            | Number of concurrent processes for parallel evaluation.      |
| `proxy`               | Network proxy URL (Format: `http://<ip>:<port>`). Required for OSWorld and WindowsAgentArena. |
| `client_password`     | VM login password. Use `"password"` for OSWorld and `"1234"` for MacOSArena. |

#### 🤖 Agent Settings

| Parameter                                                   | Description                                                  |
| :---------------------------------------------------------- | :----------------------------------------------------------- |
| `xx_provider，xx_model，xx_url，xx_api_key，xx_temperature` | Configuration for VLM inference (OpenAI-compatible API). We recommend using **vLLM** for open-source models. |
| `coder_budget`, `searcher_budget`                           | Maximum inner-loop iterations for the Coder and Searcher Agents. |
| `searcher_engine`                                           | Search engine provider. We recommend `duckduckgo` over Google to avoid CAPTCHA blocks. |
| `memoryer_max_images`                                       | Maximum number of images retained in the Reflection-Memory Agent. |
| `grounding_smart_resize`                                    | Enable for models requiring smart resizing (e.g., GTA1-32B, ScaleCUA, UI-TARS-1.5). |
| `orchestrator_keep_first_image`                             | Whether to keep the initial screenshot in the context (Default: True). |
| `tool_config`                                               | Configuration for the action space, allowing dynamic assembly of tools. |

#### 🧪 Experiment Settings

| Parameter           | Description                                              |
| :------------------ | :------------------------------------------------------- |
| `exp_name`          | Name of the experiment (defines the results directory).  |
| `enable_reflection` | Whether enable the Reflection-Memory Agent (RMA) module. |
| `max_steps`         | Maximum number of steps allowed per task.                |
| `benchmark`         | Target benchmark: `osworld`, `waa`, or `macosarena`.     |

### 4. Visualization

Results are saved in `results/{exp_name}` and logs in `logs/{exp_name}.log`.

To visualize the execution process and generate statistical reports, run the Gradio interface:

```bash
python gradio/gradio_show_result.py --root_dir results/{exp_name} --port 10000
```

## ✨ Features

1. **Unified Cross-Platform Evaluation:** We decouple the  agent logic from the OS environment, providing a unified interface to  evaluate agents across Linux, Windows, and MacOS seamlessly.
2. **Enhanced Robustness:** We have addressed numerous environment instability issues and bugs found in the original codebases of the supported benchmarks.
3. **Extensibility:** Support for defining custom tasks.
4. **Custom Workflows:** Flexible architecture allowing to customize Agent workflows and tool configurations.

We welcome the community to use our codebase for evaluating your own agents and tasks.

## 😊 Acknowledgement

We express our deepest gratitude to the following excellent projects for their contributions to the Computer Use Agent domain:
 [OSWorld](https://github.com/xlang-ai/OSWorld), [WindowsAgentArena](https://github.com/xlang-ai/OSWorld), [MacOSArena](https://github.com/xlang-ai/OSWorld), [AgentS3](https://github.com/xlang-ai/OSWorld), [UI-TARS](https://github.com/xlang-ai/OSWorld), [GTA1](https://github.com/xlang-ai/OSWorld), [ScaleCUA](https://github.com/xlang-ai/OSWorld) etc. .

## 📃 Citation

If you find this project useful in your research, please cite our paper:

```tex
@article{ossymphony2025,
  title={OS-Symphony: Orchestrating Desktop Agents via Reflection and Specialized Tools},
  author={Author One and Author Two and Author Three},
  journal={arXiv preprint arXiv:2512.xxxxx},
  year={2025}
}
```