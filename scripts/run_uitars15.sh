#!/bin/bash

PYTHON_SCRIPT_NAME="run_uitars1.5_v2.py" # <--- 请修改为您的 Python 脚本文件名
EXP_NAME="uitars1.5-critic-compare-1120-ybw" # 实验名称，可以自定义


# --- 2. 设置代理环境变量 (如果需要) ---
# 这些变量将为此脚本及其运行的任何子进程（例如 Python 脚本）设置。
# 如果您的环境不需要代理，可以将此部分注释掉。
echo "正在导出代理设置..."
export http_proxy=http://10.1.8.5:23128
export https_proxy=http://10.1.8.5:23128
export HTTP_PROXY=http://10.1.8.5:23128
export HTTPS_PROXY=http://10.1.8.5:23128
export no_proxy="localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn"
export NO_PROXY="localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn"
echo "代理设置已配置。"
echo ""


# --- 3. 运行主 Python 脚本 ---
# 行尾的 '\' 字符允许我们将一个长命令分解为多行，以提高可读性。
echo "正在执行 ${PYTHON_SCRIPT_NAME} 并传入指定参数..."
echo ""

python ${PYTHON_SCRIPT_NAME} \
  --exp_name "${EXP_NAME}" \
  --provider_name "docker" \
  --headless \
  --num_envs 1 \
  --max_steps 50 \
  --sleep_after_execution 3.0 \
  --screen_width 1920 \
  --screen_height 1080 \
  --region "us-east-1" \
  --observation_type "screenshot" \
  --domain "all" \
  --test_all_meta_path "evaluation_examples/test_osoracle.json" \
  --model "ui-tars-1.5-7b" \
  --base_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10001/v1/chat/completions" \
  --model_type "qwen25vl" \
  --temperature 0.6 \
  --max_tokens 3000 \
  --max_image_history_length 5 \
  --language "English" \
  --result_dir "results" \
  --critic_times 3 \
  --critic_model "os-oracle" \
  --critic_api_key "none" \
  --critic_provider "openai" \
  --critic_base_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/wzy-proxy-lk85v-151269-worker-0.wuzhenyu/7871" > logs/${EXP_NAME}.log 2>&1

echo ""
echo "========================================================================"
echo "脚本执行完毕。"
echo "实验结果保存在: results/${EXP_NAME}"
echo "========================================================================"