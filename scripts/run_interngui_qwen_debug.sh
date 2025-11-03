# Step 1: Complete 2 or more rollouts on either AWS or locally
# 似乎playwright有问题
# 用 proxy_wo_pw_on 代理

export http_proxy=http://10.1.8.5:23128; 
export https_proxy=http://10.1.8.5:23128; 
export HTTP_PROXY=http://10.1.8.5:23128; 
export HTTPS_PROXY=http://10.1.8.5:23128; 
export no_proxy=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn; 
export NO_PROXY=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn;

python run_agents3.py \
  --provider_name "docker" \
  --headless \
  --num_envs 1 \
  --max_steps 20 \
  --domain "all" \
  --test_all_meta_path evaluation_examples/test_docs_debug.json \
  --result_dir "results" \
  --region "us-east-1" \
  --sleep_after_execution 3 \
  --model_provider "vllm" \
  --model "Qwen3-VL-30B-A3B-Instruct" \
  --model_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-cs8ng-1170936-worker-0.yangbowen/8001/v1" \
  --model_api_key "none" \
  --model_temperature 0 \
  --ground_provider "openai" \
  --ground_model "ui-tars-1.5-7b" \
  --ground_api_key "none" \
  --ground_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-65pfw-1176830-worker-0.yangbowen/8000/v1" \
  --grounding_width 1920 \
  --grounding_height 1080 \
  --grounding_smart_resize True \
  --exp_name "debug_memory_agent" \
  --enable_reflection True \
  --enable_rewrite_instruction False \

# bash scripts/remove_all_osworld_container.sh