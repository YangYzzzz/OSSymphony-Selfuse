# OS-Caliber Ubuntu Desktop Task Generation and Trajectory Rollout

## 快速开始

执行 `bash scripts/start_os_caliber_trajectory_collector.sh`

## 参数说明

其中关键参数说明如下:

* rollout_mode: roll轨迹的模式
    * `offline` 模式: 类似于OSWorld评测, 此时需要 `rollout_test_all_meta_path` 参数来指定任务文件路径
    * `online` 模式(重点): VLM-Driven 动态生成指令 + 对生成的所有指令采集轨迹, 生成的指令全部保存在 `evaluation_examples/ubuntu_online_rollout/oscaliber_{expname}_{timestamp}` 下, 此时还需要如下参数:
        * rollout_times: roll 指令的次数, 每一次都是独立的随机选择一个已经支持初始化的APP(可在`os_caliber_task_generator.py`内查看所有支持的APP), 给定初始截图(与可能的软件详细描述?), 生成 `rollout_task_nums` 个难度不一且可验证的指令。
        * rollout_task_nums: 每次 rollout 产生多少条指令
        * rollout_app_list: 指定APP范围, 默认为当前支持的全部APP
* ig_provider, ig_model, xxx: 老几位, 用来指定生成指令的模型, 通常需要使用强模型, 默认 GPT-5
* model, base_url, xxx(有待重构): 老几位, 用来指定收集轨迹的模型, 前期用 QWen3VL 测试即可。

其余参数不太用变

## TODO

重要性递减

1. 支持 judge_model etc., VLM-Driven 评估轨迹正误
2. 支持更加丰富的数据(文件), 构造文件类型库 (从现有benchmark中收集)
3. 调整指令生成的提示词, 提高生成的指令质量和可验证性
3. 支持更加丰富的软件
3. 适配Claude, Gemini等强模型的ComputerUse能力