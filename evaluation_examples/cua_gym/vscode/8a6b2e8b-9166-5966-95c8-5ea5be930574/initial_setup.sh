#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial Setup Script
# Purpose : Create /home/user/scripts/data_cleaner.py where lines 15-25 are
#           indented one level too deep (8 spaces instead of 4).
# Result  : VS Code opens the “broken” workspace ready for the user to fix.
###############################################################################

echo ">>> Preparing initial workspace …"

# --------------------------------------------------------------------
# 1. Create directory structure exactly as requested
# --------------------------------------------------------------------
WORKSPACE="/home/user/scripts"
mkdir -p "$WORKSPACE"

# --------------------------------------------------------------------
# 2. Create Python file with intentional bad indentation (lines 15-25)
# --------------------------------------------------------------------
cat > "$WORKSPACE/data_cleaner.py" << 'EOF'
import pandas as pd
import numpy as np


def clean_dataframe(df):
    # Remove columns with all NaN values
    df = df.dropna(axis=1, how='all')

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include=['object']).columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # Drop duplicate rows
    df = df.drop_duplicates()
        # Convert date columns to datetime
        date_cols = [c for c in df.columns if 'date' in c]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        # Fill remaining NaNs with zeros
        df = df.fillna(0)

        # Reset index
        df = df.reset_index(drop=True)

    return df
EOF
echo ">>> Created file with deliberately mis-indented lines."

# --------------------------------------------------------------------
# 3. Quick verification – show indentation levels for lines 15-25
# --------------------------------------------------------------------
echo ">>> Verifying indentation problem (should start with 8 spaces) …"
awk 'NR>=15 && NR<=25 {gsub(/^ {4}/,"----", $0); print NR":",$0}' "$WORKSPACE/data_cleaner.py"

# --------------------------------------------------------------------
# 4. Open VS Code on the workspace so the user can fix the indentation
# --------------------------------------------------------------------
echo ">>> Launching VS Code at $WORKSPACE"
code "$WORKSPACE" &

echo ">>> Initial setup complete – user needs to dedent lines 15-25 by one tab."