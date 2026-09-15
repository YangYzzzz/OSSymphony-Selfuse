#!/usr/bin/env bash
set -euo pipefail

export http_proxy=http://yangbowen:CQMCKFKVkQp74ykFKb08xgim5gy67Jox3Y2m2Yzs83qgMvmmq7DQ33W3ECKI@proxy.pjlab.org.cn:23128
export https_proxy=http://yangbowen:CQMCKFKVkQp74ykFKb08xgim5gy67Jox3Y2m2Yzs83qgMvmmq7DQ33W3ECKI@proxy.pjlab.org.cn:23128
export HTTP_PROXY=http://yangbowen:CQMCKFKVkQp74ykFKb08xgim5gy67Jox3Y2m2Yzs83qgMvmmq7DQ33W3ECKI@proxy.pjlab.org.cn:23128
export HTTPS_PROXY=http://yangbowen:CQMCKFKVkQp74ykFKb08xgim5gy67Jox3Y2m2Yzs83qgMvmmq7DQ33W3ECKI@proxy.pjlab.org.cn:23128
export no_proxy=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,10.140.60.25,.pjlab.org.cn,.sslip.io,0.0.0.0
export NO_PROXY=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,10.140.60.25,.pjlab.org.cn,.sslip.io,0.0.0.0
# export no_proxy=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn
# export NO_PROXY=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn
EXP_NAME="ossymphony2-osworldv2-test-0809"

mkdir -p logs

# 配置mock网站参数, GITLAB_URL 需自行部署
export WEBSITE_HOST_SUFFIX="site.hku.icu"
export GITLAB_URL="http://10.140.52.51.sslip.io"
export GITLAB_PRIVATE_TOKEN="osworldv2-yangbowen"
export OSWORLD_FILE_BASE_URL="cache/osworld_v2_assets"

# 配置LLM Eval模型参数
export OSWORLD_EVAL_MODEL_PROVIDER="openai"
export OSWORLD_EVAL_MODEL_NAME="gpt-4o"
export OSWORLD_EVAL_MODEL_API_KEY="xxxxx"
export OSWORLD_EVAL_MODEL_BASE_URL="xxxxx"

# 配置测试模型参数
export MODEL_NAME="claude-opus-4-6"
export API_KEY="xxxxx"
export BASE_URL='xxxxx'

export OSWORLD_USER_SIM_PROVIDER="$OSWORLD_EVAL_MODEL_PROVIDER"
export OSWORLD_USER_SIM_MODEL="$OSWORLD_EVAL_MODEL_NAME"
export OSWORLD_USER_SIM_API_KEY="$OSWORLD_EVAL_MODEL_API_KEY"
export OSWORLD_USER_SIM_BASE_URL="$OSWORLD_EVAL_MODEL_BASE_URL"

python os_caliber_rollout_trajectory.py \
  --path_to_vm "/nvme/yangbowen/vm_stroage/osworld/Ubuntu_osworld-v2.qcow2" \
  --provider_name "docker" \
  --benchmark "osworld-v2" \
  --cache_dir "cache/osworld_v2_assets" \
  --rollout_mode "offline" \
  --headless \
  --num_envs 12 \
  --max_steps 100 \
  --domain "all" \
  --rollout_test_all_meta_path "evaluation_examples/osworld-v2/test_v2.json" \
  --test_config_base_dir "evaluation_examples/osworld-v2" \
  --result_dir "oscaliber_results" \
  --model ${MODEL_NAME} \
  --base_url ${BASE_URL} \
  --input_screen_width 1504 \
  --input_screen_height 832 \
  --max_tokens 10240 \
  --temperature 0.3 \
  --max_trajectory_length 8 \
  --enable_code_tool \
  --exp_name "${EXP_NAME}" > "logs/${EXP_NAME}.log"

echo "${EXP_NAME} is tested over!" 

#  > "logs/${EXP_NAME}.log" 2>&1 --collect_qwen_sft \ --enable_code_tool \ --api_key ${API_KEY} \