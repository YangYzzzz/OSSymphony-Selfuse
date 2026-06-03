"""
Initial Setup: Create release preparation workflow environment
Task ID: vscode_wf_081
Domain: vscode

Sets up a Node.js project at ~/project with git history (20+ commits),
package.json at version 1.2.3, and no release automation.
VSCode opens with the project folder.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')

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

def run(cmd, cwd=None):
    """Run a shell command."""
    subprocess.run(cmd, shell=True, cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_initial():
    # Clean up if exists
    if os.path.exists(PROJECT):
        import shutil
        shutil.rmtree(PROJECT)

    os.makedirs(PROJECT, exist_ok=True)

    # -- package.json at version 1.2.3 --
    package_json = {
        "name": "data-pipeline-toolkit",
        "version": "1.2.2",
        "description": "A robust data pipeline toolkit for ETL workflows",
        "main": "dist/index.js",
        "scripts": {
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts",
            "build": "tsc && node scripts/post-build.js",
            "test": "jest --coverage",
            "lint": "eslint src/ --ext .ts",
            "format": "prettier --write 'src/**/*.ts'"
        },
        "keywords": ["data", "pipeline", "etl", "streaming"],
        "author": "Elena Rodriguez <elena.rodriguez@datapipeline.io>",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.2",
            "winston": "^3.11.0",
            "dotenv": "^16.3.1",
            "pg": "^8.11.3",
            "redis": "^4.6.10"
        },
        "devDependencies": {
            "typescript": "^5.3.2",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1",
            "eslint": "^8.54.0",
            "@types/node": "^20.10.0",
            "@types/express": "^4.17.21",
            "prettier": "^3.1.0"
        }
    }
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # -- tsconfig.json --
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
    with open(os.path.join(PROJECT, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # -- Source files --
    src_dir = os.path.join(PROJECT, 'src')
    os.makedirs(src_dir, exist_ok=True)

    with open(os.path.join(src_dir, 'index.ts'), 'w') as f:
        f.write('''import { PipelineEngine } from './engine';
import { Config } from './config';
import { Logger } from './logger';

const logger = new Logger('main');

async function main() {
    logger.info('Starting Data Pipeline Toolkit v1.2.3');
    const config = Config.load();
    const engine = new PipelineEngine(config);
    await engine.initialize();
    await engine.run();
    logger.info('Pipeline completed successfully');
}

main().catch((err) => {
    logger.error('Pipeline failed', err);
    process.exit(1);
});
''')

    with open(os.path.join(src_dir, 'engine.ts'), 'w') as f:
        f.write('''import { Config } from './config';
import { Logger } from './logger';
import { DataSource } from './datasource';
import { Transformer } from './transformer';

export class PipelineEngine {
    private config: Config;
    private logger: Logger;
    private sources: DataSource[] = [];
    private transformers: Transformer[] = [];

    constructor(config: Config) {
        this.config = config;
        this.logger = new Logger('PipelineEngine');
    }

    async initialize(): Promise<void> {
        this.logger.info('Initializing pipeline engine');
        for (const sourceConfig of this.config.sources) {
            const source = new DataSource(sourceConfig);
            await source.connect();
            this.sources.push(source);
        }
        for (const transformConfig of this.config.transforms) {
            this.transformers.push(new Transformer(transformConfig));
        }
    }

    async run(): Promise<void> {
        this.logger.info(`Processing ${this.sources.length} sources`);
        for (const source of this.sources) {
            const data = await source.fetch();
            let result = data;
            for (const transformer of this.transformers) {
                result = await transformer.apply(result);
            }
            this.logger.info(`Processed ${result.length} records from ${source.name}`);
        }
    }
}
''')

    with open(os.path.join(src_dir, 'config.ts'), 'w') as f:
        f.write('''import * as dotenv from 'dotenv';
dotenv.config();

export interface SourceConfig {
    name: string;
    type: 'postgres' | 'redis' | 'api';
    connectionString: string;
    batchSize: number;
}

export interface TransformConfig {
    name: string;
    type: 'filter' | 'map' | 'aggregate';
    params: Record<string, unknown>;
}

export class Config {
    sources: SourceConfig[];
    transforms: TransformConfig[];
    outputDir: string;

    private constructor() {
        this.sources = [];
        this.transforms = [];
        this.outputDir = process.env.OUTPUT_DIR || './output';
    }

    static load(): Config {
        const config = new Config();
        config.sources = [
            {
                name: 'user-events',
                type: 'postgres',
                connectionString: process.env.PG_URL || 'postgresql://localhost:5432/events',
                batchSize: 1000,
            },
            {
                name: 'session-cache',
                type: 'redis',
                connectionString: process.env.REDIS_URL || 'redis://localhost:6379',
                batchSize: 500,
            },
        ];
        config.transforms = [
            { name: 'filter-active', type: 'filter', params: { field: 'active', value: true } },
            { name: 'aggregate-daily', type: 'aggregate', params: { groupBy: 'date', metric: 'count' } },
        ];
        return config;
    }
}
''')

    with open(os.path.join(src_dir, 'logger.ts'), 'w') as f:
        f.write('''import * as winston from 'winston';

export class Logger {
    private logger: winston.Logger;

    constructor(context: string) {
        this.logger = winston.createLogger({
            level: process.env.LOG_LEVEL || 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.printf(({ timestamp, level, message }) =>
                    `[${timestamp}] [${context}] ${level}: ${message}`
                )
            ),
            transports: [new winston.transports.Console()],
        });
    }

    info(msg: string) { this.logger.info(msg); }
    warn(msg: string) { this.logger.warn(msg); }
    error(msg: string, err?: Error) {
        this.logger.error(err ? `${msg}: ${err.message}` : msg);
    }
    debug(msg: string) { this.logger.debug(msg); }
}
''')

    with open(os.path.join(src_dir, 'datasource.ts'), 'w') as f:
        f.write('''export interface DataRecord {
    id: string;
    timestamp: Date;
    [key: string]: unknown;
}

export class DataSource {
    name: string;
    private type: string;
    private connectionString: string;
    private batchSize: number;

    constructor(config: { name: string; type: string; connectionString: string; batchSize: number }) {
        this.name = config.name;
        this.type = config.type;
        this.connectionString = config.connectionString;
        this.batchSize = config.batchSize;
    }

    async connect(): Promise<void> {
        // Connection logic per type
    }

    async fetch(): Promise<DataRecord[]> {
        // Fetch records in batches
        return [];
    }
}
''')

    with open(os.path.join(src_dir, 'transformer.ts'), 'w') as f:
        f.write('''import { DataRecord } from './datasource';

export class Transformer {
    private name: string;
    private type: string;
    private params: Record<string, unknown>;

    constructor(config: { name: string; type: string; params: Record<string, unknown> }) {
        this.name = config.name;
        this.type = config.type;
        this.params = config.params;
    }

    async apply(data: DataRecord[]): Promise<DataRecord[]> {
        switch (this.type) {
            case 'filter':
                return this.filterRecords(data);
            case 'map':
                return this.mapRecords(data);
            case 'aggregate':
                return this.aggregateRecords(data);
            default:
                return data;
        }
    }

    private filterRecords(data: DataRecord[]): DataRecord[] {
        const field = this.params.field as string;
        const value = this.params.value;
        return data.filter((r) => r[field] === value);
    }

    private mapRecords(data: DataRecord[]): DataRecord[] {
        return data;
    }

    private aggregateRecords(data: DataRecord[]): DataRecord[] {
        return data;
    }
}
''')

    # -- Test file --
    test_dir = os.path.join(src_dir, '__tests__')
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, 'engine.test.ts'), 'w') as f:
        f.write('''import { PipelineEngine } from '../engine';
import { Config } from '../config';

describe('PipelineEngine', () => {
    it('should initialize without errors', async () => {
        const config = Config.load();
        const engine = new PipelineEngine(config);
        // Basic smoke test
        expect(engine).toBeDefined();
    });

    it('should handle empty sources gracefully', async () => {
        const config = Config.load();
        config.sources = [];
        const engine = new PipelineEngine(config);
        await engine.initialize();
        await engine.run();
    });
});
''')

    # -- .gitignore --
    with open(os.path.join(PROJECT, '.gitignore'), 'w') as f:
        f.write('''node_modules/
dist/
.env
*.log
coverage/
.DS_Store
''')

    # -- README.md --
    with open(os.path.join(PROJECT, 'README.md'), 'w') as f:
        f.write('''# Data Pipeline Toolkit

A robust data pipeline toolkit for ETL workflows, supporting PostgreSQL,
Redis, and REST API data sources with configurable transformation chains.

## Getting Started

```bash
npm install
npm run dev
```

## Architecture

- **Engine**: Core pipeline orchestrator
- **DataSource**: Pluggable data source connectors
- **Transformer**: Chainable data transformation steps
- **Config**: Environment-based configuration

## Testing

```bash
npm test
```
''')

    # -- .env.example --
    with open(os.path.join(PROJECT, '.env.example'), 'w') as f:
        f.write('''PG_URL=postgresql://localhost:5432/events
REDIS_URL=redis://localhost:6379
OUTPUT_DIR=./output
LOG_LEVEL=info
''')

    # -- jest.config.js --
    with open(os.path.join(PROJECT, 'jest.config.js'), 'w') as f:
        f.write('''module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.test.ts'],
  collectCoverageFrom: ['src/**/*.ts', '!src/**/__tests__/**'],
};
''')

    # -- scripts directory (empty, no release automation) --
    scripts_dir = os.path.join(PROJECT, 'scripts')
    os.makedirs(scripts_dir, exist_ok=True)
    with open(os.path.join(scripts_dir, 'post-build.js'), 'w') as f:
        f.write('''const fs = require('fs');
const path = require('path');

// Copy package.json to dist for deployment
const pkg = require('../package.json');
const distPkg = {
    name: pkg.name,
    version: pkg.version,
    main: 'index.js',
    dependencies: pkg.dependencies,
};
fs.writeFileSync(
    path.join(__dirname, '..', 'dist', 'package.json'),
    JSON.stringify(distPkg, null, 2)
);
console.log('Post-build: package.json copied to dist/');
''')

    # -- Create .vscode directory but NO tasks.json --
    vscode_dir = os.path.join(PROJECT, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)

    # -- Initialize git repo with 20+ commits --
    run('git init', cwd=PROJECT)
    run('git config user.email "elena.rodriguez@datapipeline.io"', cwd=PROJECT)
    run('git config user.name "Elena Rodriguez"', cwd=PROJECT)

    # Initial commit
    run('git add .gitignore README.md package.json tsconfig.json jest.config.js .env.example', cwd=PROJECT)
    run('git commit -m "Initial project setup with package.json and config"', cwd=PROJECT)

    # Tag v1.0.0
    run('git tag v1.0.0', cwd=PROJECT)

    # Add source files one by one to create commit history
    commits = [
        ('src/logger.ts', 'Add winston-based logging utility'),
        ('src/config.ts', 'Add environment configuration module'),
        ('src/datasource.ts', 'Add pluggable data source abstraction'),
        ('src/transformer.ts', 'Add data transformation pipeline'),
        ('src/index.ts', 'Add main entry point for pipeline'),
        ('src/engine.ts', 'Add pipeline engine orchestrator'),
        ('src/__tests__/engine.test.ts', 'Add initial test suite for engine'),
        ('scripts/post-build.js', 'Add post-build script for dist packaging'),
    ]

    for filepath, message in commits:
        run(f'git add {filepath}', cwd=PROJECT)
        run(f'git commit -m "{message}"', cwd=PROJECT)

    # Tag v1.1.0
    run('git tag v1.1.0', cwd=PROJECT)

    # Additional commits to reach 20+ since last tag
    additional_commits = [
        ("src/config.ts", "Refactor config to support multiple data sources",
         "s/batchSize: 1000/batchSize: 1000/"),
        ("README.md", "Update README with architecture section", None),
        ("src/engine.ts", "Add error handling to pipeline engine run method", None),
        ("src/logger.ts", "Add debug log level support", None),
        ("src/datasource.ts", "Improve DataSource connection retry logic", None),
        ("src/transformer.ts", "Add aggregate transformer implementation", None),
        ("src/__tests__/engine.test.ts", "Add test for empty sources edge case", None),
        ("jest.config.js", "Update jest config for better coverage reporting", None),
        ("src/index.ts", "Add graceful shutdown handling", None),
        ("src/config.ts", "Add API data source type support", None),
        ("src/engine.ts", "Optimize batch processing in engine", None),
        ("src/transformer.ts", "Add map transformer type", None),
        (".env.example", "Document additional environment variables", None),
        ("src/logger.ts", "Add structured logging format", None),
        ("src/datasource.ts", "Add batch fetch pagination support", None),
    ]

    # We need to make actual file changes for each commit
    # Use simple appends to source files
    change_counter = 0
    for filepath, message, _ in additional_commits:
        full_path = os.path.join(PROJECT, filepath)
        with open(full_path, 'a') as f:
            f.write(f'\n// Update {change_counter}: {message}\n')
        change_counter += 1
        run(f'git add {filepath}', cwd=PROJECT)
        run(f'git commit -m "{message}"', cwd=PROJECT)

    # Tag v1.2.0 partway through
    run('git tag v1.2.0', cwd=PROJECT)

    # A few more commits after v1.2.0 (simulating patch-level work toward 1.2.3)
    late_commits = [
        ("src/engine.ts", "Fix memory leak in long-running pipelines"),
        ("src/config.ts", "Add validation for source configuration"),
        ("src/datasource.ts", "Fix connection pool exhaustion bug"),
        ("src/transformer.ts", "Fix filter comparison for boolean values"),
        ("src/logger.ts", "Fix timestamp timezone handling"),
    ]
    for filepath, message in late_commits:
        full_path = os.path.join(PROJECT, filepath)
        with open(full_path, 'a') as f:
            f.write(f'\n// Fix: {message}\n')
        run(f'git add {filepath}', cwd=PROJECT)
        run(f'git commit -m "{message}"', cwd=PROJECT)

    # Update package.json version to 1.2.3
    with open(os.path.join(PROJECT, 'package.json'), 'r') as f:
        pkg = json.load(f)
    pkg['version'] = '1.2.3'
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump(pkg, f, indent=2)
    run('git add package.json', cwd=PROJECT)
    run('git commit -m "Bump version to 1.2.3"', cwd=PROJECT)

    print(f'Project created at {PROJECT}')
    print('Git repo initialized with 20+ commits')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
