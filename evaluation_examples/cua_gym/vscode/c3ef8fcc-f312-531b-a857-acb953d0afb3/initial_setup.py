"""
Initial Setup: JavaScript linting and formatting pipeline in ~/project
Task ID: vscode_wf_042
Domain: vscode

Creates a JavaScript project with ESLint and Prettier npm packages installed.
No config files, no extensions, no VSCode workspace settings.
Opens VSCode with ~/project.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_042'
PROJECT_DIR = os.path.join(WORKDIR, 'project')


def run_cmd(cmd, check=True, timeout=120):
    """Run a shell command and return stdout."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                            timeout=timeout)
    if check and result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result.stdout.strip()


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def install_node():
    """Install Node.js and npm."""
    # Check if node and npm are both available
    try:
        run_cmd("node --version")
        run_cmd("npm --version")
        print("Node.js and npm already installed")
        return
    except Exception:
        pass

    print("Installing Node.js and npm...")
    run_cmd("echo 'password' | sudo -S apt-get install -y nodejs npm", timeout=180)
    print(f"Node version: {run_cmd('node --version')}")
    print(f"npm version: {run_cmd('npm --version')}")


def create_project():
    """Create a JavaScript project with ESLint and Prettier npm packages."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "analytics-dashboard",
        "version": "1.0.0",
        "description": "Sales analytics dashboard for QuarterlyReports",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "echo \"Error: no test specified\" && exit 1"
        },
        "keywords": ["analytics", "dashboard"],
        "author": "Sarah Chen",
        "license": "MIT",
        "devDependencies": {}
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # Create src directory with realistic JS files
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # src/index.js
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write('''const { fetchSalesData } = require('./data/salesApi');
const { generateReport } = require('./reports/reportGenerator');
const { formatCurrency } = require('./utils/formatters');

async function main() {
  try {
    const salesData = await fetchSalesData('2025-Q1');
    const report = generateReport(salesData);

    console.log('=== Quarterly Sales Report ===');
    console.log(`Total Revenue: ${formatCurrency(report.totalRevenue)}`);
    console.log(`Top Product: ${report.topProduct.name}`);
    console.log(`Growth Rate: ${report.growthRate}%`);
  } catch (error) {
    console.error('Failed to generate report:', error.message);
    process.exit(1);
  }
}

main();
''')

    # src/utils/formatters.js
    utils_dir = os.path.join(src_dir, 'utils')
    os.makedirs(utils_dir, exist_ok=True)

    with open(os.path.join(utils_dir, 'formatters.js'), 'w') as f:
        f.write('''function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

function formatPercentage(value) {
  return `${(value * 100).toFixed(1)}%`
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

module.exports = { formatCurrency, formatPercentage, formatDate }
''')

    # src/data/salesApi.js
    data_dir = os.path.join(src_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, 'salesApi.js'), 'w') as f:
        f.write('''const MOCK_DATA = {
  '2025-Q1': {
    products: [
      { id: 'PRD-001', name: 'Cloud Analytics Pro', revenue: 245800, units: 312 },
      { id: 'PRD-002', name: 'DataSync Enterprise', revenue: 189500, units: 156 },
      { id: 'PRD-003', name: 'SecureVault Basic', revenue: 78200, units: 890 },
      { id: 'PRD-004', name: 'APIConnect Standard', revenue: 134600, units: 445 },
      { id: 'PRD-005', name: 'DevOps Pipeline Suite', revenue: 312400, units: 198 }
    ],
    previousQuarterRevenue: 875000
  }
}

async function fetchSalesData(quarter) {
  return new Promise((resolve, reject) => {
    const data = MOCK_DATA[quarter]
    if (!data) {
      reject(new Error(`No data for quarter: ${quarter}`))
      return
    }
    setTimeout(() => resolve(data), 100)
  })
}

module.exports = { fetchSalesData }
''')

    # src/reports/reportGenerator.js
    reports_dir = os.path.join(src_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    with open(os.path.join(reports_dir, 'reportGenerator.js'), 'w') as f:
        f.write('''function generateReport(salesData) {
  const totalRevenue = salesData.products.reduce(
    (sum, product) => sum + product.revenue, 0
  )

  const topProduct = salesData.products.reduce(
    (top, product) => product.revenue > top.revenue ? product : top,
    salesData.products[0]
  )

  const growthRate = (
    (totalRevenue - salesData.previousQuarterRevenue) /
    salesData.previousQuarterRevenue * 100
  ).toFixed(1)

  return {
    totalRevenue,
    topProduct,
    growthRate,
    productCount: salesData.products.length,
    averageRevenue: totalRevenue / salesData.products.length
  }
}

module.exports = { generateReport }
''')

    # Install npm packages (eslint and prettier as devDependencies)
    # ESLint 7.x supports Node 12, Prettier 2.x supports Node 10+
    print("Installing ESLint and Prettier npm packages...")
    run_cmd(f"cd {PROJECT_DIR} && npm install --save-dev eslint@7.32.0 prettier@2.8.8", timeout=180)
    print("npm packages installed")

    # Verify installation
    run_cmd(f"cd {PROJECT_DIR} && npx eslint --version")
    run_cmd(f"cd {PROJECT_DIR} && npx prettier --version")
    print("ESLint and Prettier verified")


def ensure_no_config_files():
    """Make sure no config files exist that would satisfy the task."""
    configs_to_remove = [
        '.eslintrc.json', '.eslintrc.js', '.eslintrc.yml', '.eslintrc',
        '.prettierrc', '.prettierrc.json', '.prettierrc.js', '.prettierrc.yml',
        '.eslintignore', '.prettierignore',
    ]
    for cfg in configs_to_remove:
        path = os.path.join(PROJECT_DIR, cfg)
        if os.path.exists(path):
            os.remove(path)

    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)


def main():
    install_node()
    create_project()
    ensure_no_config_files()

    # Launch VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with ~/project')
    print(f'Initial setup complete for {TASK_ID}')


main()
