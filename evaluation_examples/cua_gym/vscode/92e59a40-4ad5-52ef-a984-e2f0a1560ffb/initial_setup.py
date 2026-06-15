"""
Initial Setup: Create a bundled-app project with webpack source maps but no launch.json
Task ID: vscode_td_076
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_076'
PROJECT_DIR = f'{WORKDIR}/projects/bundled-app'

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
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/dist', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/.cache', exist_ok=True)

    # package.json
    package_json = {
        "name": "bundled-app",
        "version": "1.2.0",
        "description": "Customer analytics dashboard with webpack bundling",
        "main": "dist/bundle.js",
        "scripts": {
            "build": "webpack --mode production --devtool source-map",
            "build:dev": "webpack --mode development --devtool source-map",
            "start": "node dist/bundle.js",
            "watch": "webpack --watch --mode development --devtool source-map"
        },
        "author": "Elena Rodriguez <elena.rodriguez@analyticspro.com>",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.2",
            "lodash": "^4.17.21",
            "moment": "^2.29.4",
            "pg": "^8.11.3"
        },
        "devDependencies": {
            "webpack": "^5.89.0",
            "webpack-cli": "^5.1.4"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # webpack.config.js
    webpack_config = '''const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  devtool: 'source-map',
  target: 'node',
  mode: 'production',
  resolve: {
    extensions: ['.js', '.json'],
  },
  module: {
    rules: [
      {
        test: /\\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
    ],
  },
};
'''
    with open(f'{PROJECT_DIR}/webpack.config.js', 'w') as f:
        f.write(webpack_config)

    # src/index.js - main entry point
    index_js = '''const express = require('express');
const { processAnalytics } = require('./analytics');
const { connectDatabase } = require('./database');
const { formatReport } = require('./reporting');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/api/dashboard', async (req, res) => {
  try {
    const db = await connectDatabase();
    const rawData = await db.query('SELECT * FROM customer_metrics WHERE period = $1', [req.query.period || 'monthly']);
    const analytics = processAnalytics(rawData.rows);
    const report = formatReport(analytics);
    res.json({ status: 'success', data: report });
  } catch (error) {
    console.error('Dashboard error:', error.message);
    res.status(500).json({ status: 'error', message: 'Failed to load dashboard data' });
  }
});

app.get('/api/metrics/:customerId', async (req, res) => {
  try {
    const db = await connectDatabase();
    const metrics = await db.query('SELECT * FROM customer_metrics WHERE customer_id = $1', [req.params.customerId]);
    const processed = processAnalytics(metrics.rows);
    res.json({ status: 'success', data: processed });
  } catch (error) {
    console.error('Metrics error:', error.message);
    res.status(500).json({ status: 'error', message: 'Failed to retrieve metrics' });
  }
});

app.post('/api/reports/generate', async (req, res) => {
  const { startDate, endDate, format } = req.body;
  try {
    const db = await connectDatabase();
    const data = await db.query(
      'SELECT * FROM customer_metrics WHERE created_at BETWEEN $1 AND $2',
      [startDate, endDate]
    );
    const analytics = processAnalytics(data.rows);
    const report = formatReport(analytics, format);
    res.json({ status: 'success', report });
  } catch (error) {
    console.error('Report generation failed:', error.message);
    res.status(500).json({ status: 'error', message: 'Report generation failed' });
  }
});

app.listen(PORT, () => {
  console.log(`Analytics dashboard running on port ${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write(index_js)

    # src/analytics.js
    analytics_js = '''const _ = require('lodash');

function processAnalytics(rawData) {
  if (!rawData || rawData.length === 0) {
    return { summary: {}, segments: [], trends: [] };
  }

  const grouped = _.groupBy(rawData, 'segment');
  const segments = Object.entries(grouped).map(([name, records]) => ({
    name,
    totalRevenue: _.sumBy(records, 'revenue'),
    avgOrderValue: _.meanBy(records, 'order_value'),
    customerCount: _.uniqBy(records, 'customer_id').length,
    retentionRate: calculateRetention(records),
  }));

  const trends = calculateTrends(rawData);
  const summary = {
    totalCustomers: _.uniqBy(rawData, 'customer_id').length,
    totalRevenue: _.sumBy(rawData, 'revenue'),
    avgLifetimeValue: _.meanBy(rawData, 'lifetime_value'),
    churnRate: calculateChurnRate(rawData),
  };

  return { summary, segments, trends };
}

function calculateRetention(records) {
  const active = records.filter(r => r.status === 'active').length;
  return records.length > 0 ? (active / records.length) * 100 : 0;
}

function calculateChurnRate(data) {
  const churned = data.filter(r => r.status === 'churned').length;
  return data.length > 0 ? (churned / data.length) * 100 : 0;
}

function calculateTrends(data) {
  const byMonth = _.groupBy(data, r => r.created_at.substring(0, 7));
  return Object.entries(byMonth)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([month, records]) => ({
      month,
      revenue: _.sumBy(records, 'revenue'),
      newCustomers: records.filter(r => r.is_new).length,
    }));
}

module.exports = { processAnalytics };
'''
    with open(f'{PROJECT_DIR}/src/analytics.js', 'w') as f:
        f.write(analytics_js)

    # src/database.js
    database_js = '''const { Pool } = require('pg');

let pool = null;

async function connectDatabase() {
  if (!pool) {
    pool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      database: process.env.DB_NAME || 'analytics_db',
      user: process.env.DB_USER || 'analytics_user',
      password: process.env.DB_PASSWORD || '',
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    });
  }
  return pool;
}

async function closeDatabase() {
  if (pool) {
    await pool.end();
    pool = null;
  }
}

module.exports = { connectDatabase, closeDatabase };
'''
    with open(f'{PROJECT_DIR}/src/database.js', 'w') as f:
        f.write(database_js)

    # src/reporting.js
    reporting_js = '''const moment = require('moment');

function formatReport(analytics, format = 'json') {
  const timestamp = moment().format('YYYY-MM-DD HH:mm:ss');
  const header = {
    generatedAt: timestamp,
    reportType: 'Customer Analytics Summary',
    version: '2.1',
  };

  if (format === 'json') {
    return { ...header, ...analytics };
  }

  if (format === 'csv') {
    return convertToCSV(header, analytics);
  }

  return { ...header, ...analytics };
}

function convertToCSV(header, analytics) {
  const lines = [`Report: ${header.reportType}`, `Generated: ${header.generatedAt}`, ''];

  if (analytics.segments && analytics.segments.length > 0) {
    lines.push('Segment,Total Revenue,Avg Order Value,Customer Count,Retention Rate');
    analytics.segments.forEach(seg => {
      lines.push(`${seg.name},${seg.totalRevenue},${seg.avgOrderValue},${seg.customerCount},${seg.retentionRate}`);
    });
  }

  return lines.join('\\n');
}

module.exports = { formatReport };
'''
    with open(f'{PROJECT_DIR}/src/reporting.js', 'w') as f:
        f.write(reporting_js)

    # dist/bundle.js - simulated minified build output
    bundle_js = '''!function(e,t){"use strict";const r=require("express"),n=require("lodash"),o=require("moment"),a=require("pg");let i=null;async function s(){return i||(i=new a.Pool({host:process.env.DB_HOST||"localhost",port:parseInt(process.env.DB_PORT||"5432"),database:process.env.DB_NAME||"analytics_db",user:process.env.DB_USER||"analytics_user",password:process.env.DB_PASSWORD||"",max:20})),i}function c(e){if(!e||0===e.length)return{summary:{},segments:[],trends:[]};const t=n.groupBy(e,"segment"),r=Object.entries(t).map(([e,t])=>({name:e,totalRevenue:n.sumBy(t,"revenue"),avgOrderValue:n.meanBy(t,"order_value"),customerCount:n.uniqBy(t,"customer_id").length}));return{summary:{totalCustomers:n.uniqBy(e,"customer_id").length,totalRevenue:n.sumBy(e,"revenue")},segments:r,trends:[]}}function l(e,t="json"){const r={generatedAt:o().format("YYYY-MM-DD HH:mm:ss"),reportType:"Customer Analytics Summary"};return"json"===t?{...r,...e}:{...r,...e}}const u=r();u.use(r.json()),u.get("/api/dashboard",async(e,t)=>{try{const r=await s(),n=await r.query("SELECT * FROM customer_metrics WHERE period = $1",[e.query.period||"monthly"]),o=c(n.rows),a=l(o);t.json({status:"success",data:a})}catch(e){t.status(500).json({status:"error",message:"Failed"})}}),u.listen(process.env.PORT||3e3,()=>{console.log("Analytics dashboard running")})}();
//# sourceMappingURL=bundle.js.map
'''
    with open(f'{PROJECT_DIR}/dist/bundle.js', 'w') as f:
        f.write(bundle_js)

    # dist/bundle.js.map - simulated source map
    source_map = {
        "version": 3,
        "file": "bundle.js",
        "sources": [
            "../src/index.js",
            "../src/analytics.js",
            "../src/database.js",
            "../src/reporting.js"
        ],
        "sourcesContent": [None, None, None, None],
        "names": ["express", "require", "lodash", "moment", "pg", "pool", "connectDatabase", "Pool", "processAnalytics", "groupBy", "formatReport", "format", "app", "use", "json", "get", "listen"],
        "mappings": "AAAA,WAAW,GAAG"
    }
    with open(f'{PROJECT_DIR}/dist/bundle.js.map', 'w') as f:
        json.dump(source_map, f)

    # .gitignore
    gitignore = '''node_modules/
dist/
*.log
.env
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # README.md
    readme = '''# Bundled App - Customer Analytics Dashboard

A Node.js analytics dashboard built with Express, bundled via Webpack with source map support.

## Getting Started

```bash
npm install
npm run build
npm start
```

## Development

```bash
npm run build:dev    # Development build with source maps
npm run watch        # Watch mode for auto-rebuilds
```

## API Endpoints

- `GET /api/dashboard?period=monthly` - Dashboard summary
- `GET /api/metrics/:customerId` - Customer-specific metrics
- `POST /api/reports/generate` - Generate analytics report

## Project Structure

```
bundled-app/
  src/
    index.js       - Express server entry point
    analytics.js   - Data processing and analytics
    database.js    - PostgreSQL connection pool
    reporting.js   - Report formatting utilities
  dist/
    bundle.js      - Webpack output (minified)
    bundle.js.map  - Source map for debugging
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Ensure NO .vscode/launch.json exists (the task is to create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(f'{vscode_dir}/launch.json'):
        os.remove(f'{vscode_dir}/launch.json')

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: package.json, webpack.config.js, src/*, dist/bundle.js, dist/bundle.js.map')
    print(f'No .vscode/launch.json present (task requires creating it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
