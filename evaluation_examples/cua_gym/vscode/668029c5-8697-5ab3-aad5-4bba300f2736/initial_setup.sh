#!/usr/bin/env bash
set -euo pipefail

#######################################################################
#  Initial VS Code task setup – RandomForest visualisation (INCOMPLETE)
#######################################################################
#  This script prepares a realistic starting point for a user who wants
#  to be able to press:  ⇧⌘B / Ctrl-Shift-B  →  “Visualise RandomForest”
#  but currently has NO such facility configured.
#
#  The workspace folder used in this exercise is fixed at:
#     /home/user/ml_project
#
#  After execution:
#    • VS Code opens on that folder
#    • A simple RandomForest exists in models.py
#    • No tasks / helpers for visualisation exist yet
#######################################################################

echo -e "\n[1/6] Creating clean workspace …"
WORKSPACE="/home/user/ml_project"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"

echo -e "\n[2/6] Creating Python source: $WORKSPACE/models.py"
cat > "$WORKSPACE/models.py" <<'EOF'
"""
models.py  – sample ML model for demonstration

Goal (for the upcoming task):
    Add an easy one-click/keyboard-shortcut way to display:
      • feature_importances_ bar chart
      • a diagram of the first tree in the random forest
directly inside VS Code.
"""

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import pathlib

DATA = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    DATA.data, DATA.target, test_size=0.2, random_state=42
)

clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X_train, y_train)

# Persist the trained model so the forthcoming visualisation task can load it.
pathlib.Path("artifacts").mkdir(exist_ok=True)
with open("artifacts/rf.pkl", "wb") as f:
    pickle.dump(clf, f)

print("RandomForest trained and saved to artifacts/rf.pkl")
EOF

echo -e "\n[3/6] Creating a minimal README describing the missing feature"
cat > "$WORKSPACE/README.md" <<'EOF'
# ML Project

We have a RandomForest model saved in `artifacts/rf.pkl`.

💡 Desired next step (task for the user):
Create a VS Code Task or command that quickly generates and opens:

* `feature_importances.png` – bar chart of the features
* `tree_0.png` – diagram of the first tree in the forest

so they appear instantly in VS Code.
EOF

echo -e "\n[4/6] (Optional) Recommending Python extension"
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  "recommendations": [
    "ms-python.python"
  ]
}
EOF

echo -e "\n[5/6] Verifying initial state …"
if grep -q "RandomForestClassifier" "$WORKSPACE/models.py"; then
    echo "✓ models.py contains RandomForest code"
else
    echo "✗ models.py is missing expected content" && exit 1
fi

echo -e "\n[6/6] Opening VS Code – workspace is READY"
code "$WORKSPACE" &

echo -e "\nInitial setup complete – there is currently NO task that shows\nfeature importances or tree diagram. That is what the user must add."