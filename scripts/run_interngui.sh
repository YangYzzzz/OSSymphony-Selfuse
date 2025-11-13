# 注意：动作空间的启用目前先通过调整groundingagent里面的装饰器函数，后续更改成使用配置文件动态配置

export http_proxy=http://10.1.8.5:23128; 
export https_proxy=http://10.1.8.5:23128; 
export HTTP_PROXY=http://10.1.8.5:23128; 
export HTTPS_PROXY=http://10.1.8.5:23128; 
export no_proxy=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn; 
export NO_PROXY=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn;
EXP_NAME="interngui-eagermodetest-gpt-5-uitars1.5-step50-20251111"
python run_interngui.py \
  --provider_name "docker" \
  --headless \
  --num_envs 1 \
  --max_steps 2 \
  --domain "all" \
  --test_all_meta_path evaluation_examples/test_gimp.json \
  --tool_config "/nvme/yangbowen/yangbowen/OSWorld/mm_agents/interngui/tool/all_tool_config.yaml" \
  --result_dir "results" \
  --region "us-east-1" \
  --orchestrator_provider "openai" \
  --orchestrator_model "gpt-5" \
  --orchestrator_url "https://api.boyuerichdata.opensphereai.com/v1" \
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
  --coder_model "gpt-5" \
  --coder_url "https://api.boyuerichdata.opensphereai.com/v1" \
  --coder_api_key "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D" \
  --coder_temperature 0.1 \
  --coder_budget 20 \
  --memoryer_provider "openai" \
  --memoryer_model "gpt-5" \
  --memoryer_url "https://api.boyuerichdata.opensphereai.com/v1" \
  --memoryer_api_key "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D" \
  --memoryer_temperature 0.1 \
  --searcher_provider "openai" \
  --searcher_model "gpt-5-mini" \
  --searcher_url "https://api.boyuerichdata.opensphereai.com/v1" \
  --searcher_api_key "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D" \
  --searcher_temperature 0.1 \
  --searcher_type "vlm" \
  --searcher_budget 20\
  --sleep_after_execution 3 \
  --exp_name ${EXP_NAME} \
  --enable_reflection

# bash scripts/remove_all_osworld_container.sh