"""
Initial Setup: Configure VSCode to use workspace TypeScript version
Task ID: vscode_fix_054
Domain: vscode

Creates a TypeScript project at ~/ts-project with TypeScript 5.3 in node_modules,
but NO .vscode/settings.json typescript.tsdk configured. VSCode opens the project.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_054'
PROJECT_DIR = f'{WORKDIR}/ts-project'


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


def create_initial():
    # --- Create project directory structure ---
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "analytics-dashboard",
        "version": "2.1.0",
        "description": "Real-time analytics dashboard for marketing metrics",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts",
            "test": "jest --config jest.config.ts",
            "lint": "eslint src/ --ext .ts,.tsx"
        },
        "dependencies": {
            "express": "^4.18.2",
            "chart.js": "^4.4.1",
            "dayjs": "^1.11.10",
            "pg": "^8.11.3"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "@types/node": "^20.10.0",
            "@types/pg": "^8.10.9",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1",
            "ts-node": "^10.9.2",
            "eslint": "^8.54.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "**/*.test.ts"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- src/index.ts ---
    index_ts = '''import express, { Request, Response } from 'express';
import { Pool } from 'pg';
import dayjs from 'dayjs';

interface MetricRecord {
  id: number;
  campaign_name: string;
  impressions: number;
  clicks: number;
  conversions: number;
  spend: number;
  recorded_at: Date;
}

interface DashboardSummary {
  totalImpressions: number;
  totalClicks: number;
  averageCTR: number;
  totalSpend: number;
  topCampaign: string;
  dateRange: { start: string; end: string };
}

const app = express();
const PORT = process.env.PORT || 3200;

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: 'analytics_db',
  user: process.env.DB_USER || 'analyst',
  password: process.env.DB_PASSWORD || '',
});

async function getMetrics(startDate: string, endDate: string): Promise<MetricRecord[]> {
  const query = `
    SELECT id, campaign_name, impressions, clicks, conversions, spend, recorded_at
    FROM campaign_metrics
    WHERE recorded_at BETWEEN $1 AND $2
    ORDER BY recorded_at DESC
  `;
  const result = await pool.query(query, [startDate, endDate]);
  return result.rows;
}

function calculateSummary(metrics: MetricRecord[]): DashboardSummary {
  const totalImpressions = metrics.reduce((sum, m) => sum + m.impressions, 0);
  const totalClicks = metrics.reduce((sum, m) => sum + m.clicks, 0);
  const totalSpend = metrics.reduce((sum, m) => sum + m.spend, 0);

  const campaignPerformance = new Map<string, number>();
  for (const m of metrics) {
    const current = campaignPerformance.get(m.campaign_name) || 0;
    campaignPerformance.set(m.campaign_name, current + m.conversions);
  }

  let topCampaign = '';
  let maxConversions = 0;
  for (const [name, conversions] of campaignPerformance) {
    if (conversions > maxConversions) {
      topCampaign = name;
      maxConversions = conversions;
    }
  }

  return {
    totalImpressions,
    totalClicks,
    averageCTR: totalImpressions > 0 ? (totalClicks / totalImpressions) * 100 : 0,
    totalSpend,
    topCampaign,
    dateRange: {
      start: dayjs(metrics[metrics.length - 1]?.recorded_at).format('YYYY-MM-DD'),
      end: dayjs(metrics[0]?.recorded_at).format('YYYY-MM-DD'),
    },
  };
}

app.get('/api/dashboard', async (req: Request, res: Response) => {
  try {
    const startDate = (req.query.start as string) || dayjs().subtract(30, 'day').format('YYYY-MM-DD');
    const endDate = (req.query.end as string) || dayjs().format('YYYY-MM-DD');
    const metrics = await getMetrics(startDate, endDate);
    const summary = calculateSummary(metrics);
    res.json({ summary, metrics });
  } catch (error) {
    console.error('Dashboard API error:', error);
    res.status(500).json({ error: 'Failed to load dashboard data' });
  }
});

app.listen(PORT, () => {
  console.log(`Analytics dashboard server running on port ${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/src/index.ts', 'w') as f:
        f.write(index_ts)

    # --- src/utils.ts ---
    utils_ts = '''import dayjs from 'dayjs';

export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(amount);
}

export function formatPercentage(value: number, decimals: number = 2): string {
  return `${value.toFixed(decimals)}%`;
}

export function getDateRange(days: number): { start: string; end: string } {
  const end = dayjs();
  const start = end.subtract(days, 'day');
  return {
    start: start.format('YYYY-MM-DD'),
    end: end.format('YYYY-MM-DD'),
  };
}

export function calculateGrowthRate(current: number, previous: number): number {
  if (previous === 0) return current > 0 ? 100 : 0;
  return ((current - previous) / previous) * 100;
}
'''
    with open(f'{PROJECT_DIR}/src/utils.ts', 'w') as f:
        f.write(utils_ts)

    # --- Create fake node_modules/typescript with version 5.3 ---
    ts_module_dir = f'{PROJECT_DIR}/node_modules/typescript'
    ts_lib_dir = f'{ts_module_dir}/lib'
    os.makedirs(ts_lib_dir, exist_ok=True)

    ts_package = {
        "name": "typescript",
        "version": "5.3.3",
        "description": "TypeScript is a language for application scale JavaScript development",
        "main": "lib/typescript.js",
        "typings": "lib/typescript.d.ts",
        "bin": {
            "tsc": "bin/tsc",
            "tsserver": "bin/tsserver"
        }
    }
    with open(f'{ts_module_dir}/package.json', 'w') as f:
        json.dump(ts_package, f, indent=2)

    # Create a minimal tsserverlibrary.js placeholder in lib/ so VSCode recognizes it
    with open(f'{ts_lib_dir}/tsserverlibrary.js', 'w') as f:
        f.write('// TypeScript 5.3.3 server library placeholder\n')

    with open(f'{ts_lib_dir}/typescript.js', 'w') as f:
        f.write('// TypeScript 5.3.3 main library placeholder\n')

    with open(f'{ts_lib_dir}/tsserver.js', 'w') as f:
        f.write('// TypeScript 5.3.3 tsserver placeholder\n')

    # --- Do NOT create .vscode/settings.json with typescript.tsdk ---
    # The task requires the agent to set this, so it must not exist initially.

    print(f'Project created at: {PROJECT_DIR}')
    print(f'TypeScript 5.3.3 in node_modules/typescript/')
    print(f'No .vscode/settings.json with typescript.tsdk')

    # --- Launch VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
