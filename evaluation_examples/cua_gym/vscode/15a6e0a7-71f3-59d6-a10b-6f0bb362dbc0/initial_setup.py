"""
Initial Setup: TypeScript dependency graph analyzer project scaffold
Task ID: vscode_gf4_072
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_072'
PROJECT_DIR = f'{WORKDIR}/projects/ts-dependency-graph'
NVM_DIR = f'{WORKDIR}/.nvm'
NODE_BIN = f'{NVM_DIR}/versions/node/v18.20.8/bin'

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

def install_nodejs():
    """Install Node.js 18 via nvm."""
    print('Installing Node.js 18 via nvm...')
    # Install nvm
    subprocess.run(
        'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash',
        shell=True, capture_output=True, text=True, timeout=120
    )
    # Install node 18 using nvm via bash
    result = subprocess.run(
        f'export NVM_DIR="{NVM_DIR}" && . "$NVM_DIR/nvm.sh" && nvm install 18',
        shell=True, capture_output=True, text=True, timeout=120,
        executable='/bin/bash'
    )
    print(f'nvm install: {result.stdout[-200:]}')
    if result.returncode != 0:
        print(f'nvm install error: {result.stderr[-200:]}')

def ensure_nodejs():
    """Ensure Node.js is available, install if needed."""
    if not shutil.which('node'):
        # Check if nvm node exists
        node_path = f'{NODE_BIN}/node'
        if not os.path.exists(node_path):
            install_nodejs()
            # Find the actual installed version path
            versions_dir = f'{NVM_DIR}/versions/node'
            if os.path.exists(versions_dir):
                versions = os.listdir(versions_dir)
                if versions:
                    actual_bin = f'{versions_dir}/{versions[0]}/bin'
                    return actual_bin
        return NODE_BIN
    return None  # node already in PATH

def create_initial():
    node_bin = ensure_nodejs()

    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/fixtures', exist_ok=True)

    # Create fixture files with realistic TypeScript content
    # These have circular and linear dependencies for the analyzer to discover

    # fixtures/types.ts - exports interfaces, imports from index (circular)
    with open(f'{PROJECT_DIR}/fixtures/types.ts', 'w') as f:
        f.write('''// Type definitions for the project
import { AppConfig } from './index';

export interface ModuleInfo {
  name: string;
  path: string;
  size: number;
  lastModified: Date;
}

export interface DependencyEdge {
  source: string;
  target: string;
  type: 'static' | 'dynamic';
}

export interface AnalysisResult {
  modules: ModuleInfo[];
  edges: DependencyEdge[];
  circularDeps: string[][];
  entryPoint: string;
}

export type ReportFormat = 'json' | 'dot' | 'ascii';

export function createDefaultConfig(): AppConfig {
  return { verbose: false, maxDepth: 10, includeNodeModules: false };
}
''')

    # fixtures/utils.ts - utility functions, imports from types (linear)
    with open(f'{PROJECT_DIR}/fixtures/utils.ts', 'w') as f:
        f.write('''// Utility functions for dependency analysis
import { ModuleInfo, DependencyEdge } from './types';

export function normalizePath(filePath: string): string {
  return filePath.replace(/\\\\/g, '/').replace(/\\/+/g, '/');
}

export function extractModuleName(filePath: string): string {
  const parts = filePath.split('/');
  const fileName = parts[parts.length - 1];
  return fileName.replace(/\\.(ts|js|tsx|jsx)$/, '');
}

export function createModuleInfo(path: string): ModuleInfo {
  return {
    name: extractModuleName(path),
    path: normalizePath(path),
    size: 0,
    lastModified: new Date(),
  };
}

export function formatEdge(edge: DependencyEdge): string {
  return `${edge.source} -> ${edge.target} [${edge.type}]`;
}

export function filterByType(
  edges: DependencyEdge[],
  type: 'static' | 'dynamic'
): DependencyEdge[] {
  return edges.filter(e => e.type === type);
}
''')

    # fixtures/index.ts - main entry, imports from utils and types (circular with types)
    with open(f'{PROJECT_DIR}/fixtures/index.ts', 'w') as f:
        f.write('''// Main entry point for fixture project
import { normalizePath, extractModuleName } from './utils';
import { AnalysisResult, ReportFormat, createDefaultConfig } from './types';

export interface AppConfig {
  verbose: boolean;
  maxDepth: number;
  includeNodeModules: boolean;
}

const config: AppConfig = createDefaultConfig();

export function analyzeProject(entryPoint: string): AnalysisResult {
  const normalizedEntry = normalizePath(entryPoint);
  const moduleName = extractModuleName(normalizedEntry);

  console.log(`Analyzing project from entry: ${moduleName}`);

  return {
    modules: [],
    edges: [],
    circularDeps: [],
    entryPoint: normalizedEntry,
  };
}

export function getVersion(): string {
  return '1.0.0';
}

export { config };
''')

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  fixtures/index.ts  (imports utils, types - circular with types)')
    print(f'  fixtures/utils.ts  (imports types)')
    print(f'  fixtures/types.ts  (imports index - circular)')

    # Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
