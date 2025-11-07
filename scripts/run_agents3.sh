# 注意：动作空间的启用目前先通过调整groundingagent里面的装饰器函数，后续更改成使用配置文件动态配置

export http_proxy=http://10.1.8.5:23128; 
export https_proxy=http://10.1.8.5:23128; 
export HTTP_PROXY=http://10.1.8.5:23128; 
export HTTPS_PROXY=http://10.1.8.5:23128; 
export no_proxy=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn; 
export NO_PROXY=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn;
EXP_NAME="agents3-nogdrive-qwen3vl-30ba3b-uitars1.5-step50-20251107-ybw"
# EXP_NAME="agents3-nogdrive-qwen3vl-30ba3b-uitars1.5-testgimp"
python run_agents3.py \
  --provider_name "docker" \
  --headless \
  --num_envs 12 \
  --max_steps 50 \
  --domain "all" \
  --test_all_meta_path evaluation_examples/test_nogdrive.json \
  --result_dir "results" \
  --region "us-east-1" \
  --tool_config "/nvme/yangbowen/yangbowen/OSWorld/Agent-S/gui_agents/interngui/tool/all_tool_config.yaml" \
  --orchestrator_provider "openai" \
  --orchestrator_model "Qwen3-VL-30B-A3B-Instruct" \
  --orchestrator_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10000/v1" \
  --orchestrator_api_key "none" \
  --orchestrator_temperature 0.1 \
  --grounder_provider "openai" \
  --grounder_model "ui-tars-1.5-7b" \
  --grounder_api_key "none" \
  --grounder_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-65pfw-1176830-worker-0.yangbowen/8000/v1" \
  --grounding_width 1920 \
  --grounding_height 1080 \
  --grounding_smart_resize True \
  --coder_provider "openai" \
  --coder_model "Qwen3-VL-30B-A3B-Instruct" \
  --coder_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10000/v1" \
  --coder_api_key "none" \
  --coder_temperature 0.1 \
  --coder_budget 20 \
  --sleep_after_execution 3 \
  --exp_name ${EXP_NAME} \
  --enable_reflection True

# bash scripts/remove_all_osworld_container.sh