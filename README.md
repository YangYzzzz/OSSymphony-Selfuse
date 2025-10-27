# InternGUIFramework

私有开发库，用于存放Agent代码与评测环境代码。

## 开发规范

每个人基于已有code base，在各自的分支上(yang/jin)开发，需要合并时再合并至主分支

## 前提

1. 安装 OS-World 所有依赖：`pip install -r requirements.txt`
2. 可编辑安装Agent-S包, `cd Agent-S`, `pip install -e .`, 这样可以简化agent的导包，同时可以在Agent-S文件夹内动态更改
3. 虚拟机文件位于 `/nvme/yangbowen/osworld/docker_vm_data/Ubuntu.qcow2`(不要更改，不要更改，不要更改)
4. 安装后 执行 `python quickstart.py --provider_name docker --path_to_vm /nvme/yangbowen/osworld/docker_vm_data/Ubuntu.qcow2`，验证OS-World环境是否能够正确启动



## 文件结构说明

* `Agent-S/gui_agents/interngui`：核心Agent代码，主要开发部分
  * `agents`：Agent的核心部件，包括 code_agent，search_agent，grounding_agent 等子模块
    * `grounding.py`：**所有工具在此配置**，当前版本仍采用 `@agent_action` 装饰器配置工具实现动态注入提示词，后续更改为通过配置文件配置工具
  * `core`：LLM引擎，支持快捷方便地创建智能体实例，管理上下文，调用 `generate` 推理
  * `memory`：存放提示词
  * `util`：可能有用的工具如 `smart_resize`，`call_llm_safe`，`call_llm_formatter`
* `desktop_env`：核心环境文件夹，尽量不要更改，除非是代理之类的还有问题。

* `evaluation_examples`：任务文件夹，所有任务元数据位于 `evaluation_examples/examples`内，而最外层 `.json` 文件用于配置测试任务，当前一些配置如下：
  * `test_nogdrive.json`：测试全集，共361个任务
  * `test_nogdrive_diffi_subset.json`：Baseline没做对的困难子集，共187个任务
  * `test_nogdrive_diffi_subset_for_valid.json`：随机选取的用于测试的子集，共62个任务，**这部分后续需要根据case study情况手动筛选出合适的用于快速验证的子集**。

* `scripts`：启动脚本文件夹，一个简单的启动测试例子是 `bash scripts/run_agents3_test.sh`，配置参数参考启动文件
* `results/{exp_name}`：被gitignore了，存放每一个任务事无巨细执行过程的文件夹，**这个文件夹我们可以共用，共享结果，Jin可以创一个软链接链过来**
* `run_agents3.py`，`agents3_lib_run_single.py`：整体评测启动代码 和 单个任务执行代码，`run_agents3.py` 内重要参数如下，其他配置与原先保持一致即可：
  * 通用配置：
    * `--max_steps`: 每个任务的最大步数
    * `--num_envs`: 并行运行的环境数量
    * `--test_all_meta_path`: 任务配置文件的路径
    * `--exp_name`: **实验名称**，和 `--result_dir` 一起确定结果保存路径
  * 智能体配置：
    * `--max_trajectory_length`: 最大上下文轨迹长度。
    * `--enable_reflection`: 是否启用反思机制。
    * `--enable_rewrite_instruction`: 是否启用指令重写机制。
  * 主模型配置
    * `--model_provider`: 主要生成模型的提供商。
    * `--model`: 主要生成模型的名称。
    * `--model_url`: 主要生成模型 API 的 URL。
    * `--model_api_key`: 主要生成模型的 API 密钥。
    * `--model_temperature`: 固定生成模型的温度值。
  * Grounding模型配置
    * `--ground_provider`: **(必需)** 定位模型的提供商。
    * `--ground_url`: **(必需)** 定位模型的 URL。
    * `--ground_api_key`: 定位模型的 API 密钥。
    * `--ground_model`: **(必需)** 定位模型的名称。
    * `--grounding_width`: **(必需)** 处理器缩放后屏幕截图的宽度。
    * `--grounding_height`: **(必需)** 处理器缩放后屏幕截图的高度。
    * `--grounding_smart_resize`: **(必需)** 是否启用智能缩放。
  * Search Agent 先不用管，只要把 search 的 action 注释掉，search agent 就不会运行

## 注意：

1. 如果修改了虚拟机配置，DesktopEnv等，请及时同步
2. 多留备份多留档
3. 实验名称需要规范一下：
   * 参考 `nogdrive-gpt-5-mini-uitars1.5-step50-nocode-20251019-ybw`
   * {任务配置} + {模型配置} + {步数} + {动作配置} + {日期} + {执行人} + {自定义信息}(可选)
4. GoGoGo