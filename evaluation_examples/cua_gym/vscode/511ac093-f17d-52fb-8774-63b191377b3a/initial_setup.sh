#!/usr/bin/env bash
# ---------------------------------------------------------------
# initial_setup.sh
# Prepares a workspace that is *missing* the pagination utility
# and has no build task.  Learner must:
#   1. Create src/utils/pagination.js with the correct logic
#   2. Add .vscode/tasks.json so Ctrl+Shift+B runs the tests
# ---------------------------------------------------------------
set -euo pipefail

echo "🔧  Preparing initial VS Code pagination task workspace …"

WORKSPACE="$HOME/pagination_task"
VSCODE_DIR="$WORKSPACE/.vscode"

# Start fresh every time the script is run
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src/utils" "$WORKSPACE/tests" "$VSCODE_DIR"

###############################################################################
# 1. Create the failing test --------------------------------------------------
###############################################################################
cat > "$WORKSPACE/tests/pagination.test.js" << 'EOF'
/* Failing test – will pass once learner implements paginate() */
const assert = require('assert');
const { paginate } = require('../src/utils/pagination');

const base = 'https://api.example.com/items';

try {
  // Page 1, 10 items per page
  const r1 = paginate({ page: 1, perPage: 10, baseUrl: base });
  assert.deepStrictEqual(r1, {
    offset: 0,
    limit: 10,
    prev: null,
    next: `${base}?page=2&perPage=10`
  });

  // Page 3, 25 items per page
  const r2 = paginate({ page: 3, perPage: 25, baseUrl: base });
  assert.deepStrictEqual(r2, {
    offset: 50,
    limit: 25,
    prev: `${base}?page=2&perPage=25`,
    next: `${base}?page=4&perPage=25`
  });

  console.log('✅  All pagination tests passed');
} catch (err) {
  console.error('❌  Pagination tests failed: ', err.message);
  process.exit(1);
}
EOF

###############################################################################
# 2. Provide hints / task description ----------------------------------------
###############################################################################
cat > "$WORKSPACE/README.md" << 'EOF'
# Pagination Utility Task

You need to:

1. Create **src/utils/pagination.js** exporting `paginate({page, perPage, baseUrl})`
   that returns: