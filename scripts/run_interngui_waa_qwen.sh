export http_proxy=http://10.1.8.5:23128; 
export https_proxy=http://10.1.8.5:23128; 
export HTTP_PROXY=http://10.1.8.5:23128; 
export HTTPS_PROXY=http://10.1.8.5:23128; 
export no_proxy=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn; 
export NO_PROXY=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn;
EXP_NAME="interngui-waa2-qwenvl3-32b-uitars1.5-step15-20251129-ybw"
# enable_rewrite_instruction
python run_interngui.py \
  --provider_name "docker" \
  --path_to_vm "/nvme/yangbowen/vm_stroage/waa_ding/golden" \
  --headless \
  --num_envs 2 \
  --benchmark "waa" \
  --max_steps 15 \
  --domain "all" \
  --test_all_meta_path evaluation_examples/waa/test_all.json \
  --result_dir "results" \
  --region "us-east-1" \
  --tool_config mm_agents/interngui/tool/all_tool_config.yaml \
  --orchestrator_provider "openai" \
  --orchestrator_model "Qwen3-VL-32B-Instruct" \
  --orchestrator_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-dqk5z-2572488-worker-0.yangbowen/8001/v1" \
  --orchestrator_api_key "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D" \
  --orchestrator_temperature 0.1 \
  --orchestrator_keep_first_image \
  --grounder_provider "vllm" \
  --grounder_model "ui-tars-1.5-7b" \
  --grounder_api_key "none" \
  --grounder_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10001/v1" \
  --grounding_width 1920 \
  --grounding_height 1080 \
  --grounding_smart_resize True \
  --coder_provider "openai" \
  --coder_model "Qwen3-VL-32B-Instruct" \
  --coder_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10001/v1" \
  --coder_api_key "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D" \
  --coder_temperature 0.1 \
  --coder_budget 20 \
  --memoryer_provider "openai" \
  --memoryer_model "Qwen3-VL-32B-Instruct" \
  --memoryer_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-dqk5z-2572488-worker-0.yangbowen/8001/v1" \
  --memoryer_api_key "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D" \
  --memoryer_temperature 0.1 \
  --searcher_provider "openai" \
  --searcher_model "Qwen3-VL-32B-Instruct" \
  --searcher_url "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-dqk5z-2572488-worker-0.yangbowen/8001/v1" \
  --searcher_api_key "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D" \
  --searcher_temperature 0.1 \
  --searcher_type "vlm" \
  --searcher_screen_width 1920 \
  --searcher_screen_height 1080 \
  --searcher_budget 20\
  --searcher_path_to_vm "/nvme/yangbowen/vm_stroage/osworld/Ubuntu.qcow2" \
  --sleep_after_execution 3 \
  --exp_name ${EXP_NAME} \
  --enable_reflection \
  --pass_k 1 2>&1 | tee logs/${EXP_NAME}.log

# # logs/${EXP_NAME}.log 2>&1   --enable_rewrite_instruction