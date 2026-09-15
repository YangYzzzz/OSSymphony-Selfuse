export http_proxy=http://10.1.8.5:23128; 
export https_proxy=http://10.1.8.5:23128; 
export HTTP_PROXY=http://10.1.8.5:23128; 
export HTTPS_PROXY=http://10.1.8.5:23128; 
export no_proxy=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn; 
export NO_PROXY=localhost,127.0.0.1,10.140.52.51,172.17.0.0/16,20.20.20.0/24,0.0.0.0,10.140.60.25,.pjlab.org.cn;

EXP_NAME="claude-opus-5-osworld-ybw-0731"

python os_caliber_rollout_trajectory.py \
  --provider_name "docker" \
  --path_to_vm "/nvme/yangbowen/vm_stroage/osworld/Ubuntu.qcow2" \
  --headless \
  --num_envs 12 \
  --max_steps 100 \
  --sleep_after_execution 3  \
  --model "claude-opus-5" \
  --base_url "xxxxx" \
  --api_key "xxxxx" \
  --temperature 1 \
  --top_p 0.95 \
  --max_image_history_length 10 \
  --input_screen_width 1504 \
  --input_screen_height 832 \
  --rollout_mode "offline" \
  --rollout_test_all_meta_path evaluation_examples/osworld/test_nogdrive.json \
  --rollout_task_dir evaluation_examples/osworld/examples/ \
  --exp_name ${EXP_NAME} >> logs/${EXP_NAME}.log