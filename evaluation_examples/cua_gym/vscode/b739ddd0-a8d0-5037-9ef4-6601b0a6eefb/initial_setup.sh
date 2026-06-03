#!/usr/bin/env bash
# -------------------------------------------------------------------
#  VS Code Task :  Fix over-indented lines 10-20 in data_processor.py
#  Script        :  setup_initial.sh  (INITIAL STATE)
# -------------------------------------------------------------------
set -euo pipefail

echo "-----  Preparing INITIAL workspace  -----"

# 1. Create the workspace folder exactly as requested
WORKSPACE="/home/user/scripts"
FILE="$WORKSPACE/data_processor.py"

mkdir -p "$WORKSPACE"

# 2. Create data_processor.py with LINES 10-20 indented FOUR SPACES too far
cat > "$FILE" << 'EOF'
#!/usr/bin/env python3
import json


def load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


    def process_item(item):
        # Simulate heavy processing
        result = {k: v for k, v in item.items()}
        return result

    def save_data(path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def main():
        source = 'input.json'
        target = 'output.json'
        data = load_data(source)
        processed = [process_item(i) for i in data]
        save_data(target, processed)


if __name__ == '__main__':
    main()
EOF

echo "Created file with intentionally incorrect indentation:"
sed -n '8,22p' "$FILE"   # show the problematic region

# 3. Simple verification that the bad indentation EXISTS
if grep -q '^    def process_item' "$FILE"; then
    echo "Verification PASSED: Over-indented lines detected."
else
    echo "Verification FAILED: Expected indentation not found."; exit 1
fi

# 4. Optional hint file for the learner
echo "Lines 10-20 are indented four spaces too far – bring them back!" > "$WORKSPACE/.task_info.txt"

# 5. Open VS Code on the workspace so the user can fix the file
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "-----  INITIAL workspace ready  -----"