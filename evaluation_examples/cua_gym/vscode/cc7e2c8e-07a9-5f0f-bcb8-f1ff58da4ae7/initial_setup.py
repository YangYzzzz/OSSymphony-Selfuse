"""
Initial Setup: Create utilities.ts with 5 non-exported function declarations
Task ID: vscode_web_017
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_017'
PROJECT_DIR = f'{WORKDIR}/projects/frontend'
SRC_DIR = f'{PROJECT_DIR}/src/utils'
OUTPUT = f'{SRC_DIR}/utilities.ts'


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
    # Create directory structure
    os.makedirs(SRC_DIR, exist_ok=True)

    # Build a realistic utilities.ts file with 5 function declarations
    # at exactly lines 10, 25, 40, 55, 70 (none exported)
    lines = []

    # Lines 1-9: imports and type definitions
    lines.append('// Utility functions for the frontend application')          # 1
    lines.append('// Author: Sarah Chen')                                       # 2
    lines.append('// Last updated: 2025-11-03')                                 # 3
    lines.append('')                                                            # 4
    lines.append('import { EventEmitter } from "events";')                      # 5
    lines.append('')                                                            # 6
    lines.append('interface FormatOptions {')                                    # 7
    lines.append('  locale?: string;')                                          # 8
    lines.append('  currency?: string;')                                        # 9

    # Line 10: first function declaration (after closing the interface)
    # We need line 10 to start with 'function', so close interface before it
    # Rethink: line 10 must start with 'function'. Let's adjust.

    lines = []
    # Lines 1-9
    lines.append('// Utility functions for the frontend application')          # 1
    lines.append('// Author: Sarah Chen')                                       # 2
    lines.append('// Last updated: 2025-11-03')                                 # 3
    lines.append('')                                                            # 4
    lines.append('import { EventEmitter } from "events";')                      # 5
    lines.append('import type { UserProfile, Transaction } from "../types";')   # 6
    lines.append('')                                                            # 7
    lines.append('const DEFAULT_LOCALE = "en-US";')                             # 8
    lines.append('')                                                            # 9

    # Line 10: function #1
    lines.append('function formatCurrency(amount: number, currency: string = "USD"): string {')  # 10
    lines.append('  const formatter = new Intl.NumberFormat(DEFAULT_LOCALE, {')  # 11
    lines.append('    style: "currency",')                                       # 12
    lines.append('    currency: currency,')                                      # 13
    lines.append('  });')                                                        # 14
    lines.append('  return formatter.format(amount);')                           # 15
    lines.append('}')                                                            # 16
    lines.append('')                                                             # 17

    # Lines 18-24: some code between functions
    lines.append('interface ValidationResult {')                                 # 18
    lines.append('  isValid: boolean;')                                          # 19
    lines.append('  errors: string[];')                                          # 20
    lines.append('}')                                                            # 21
    lines.append('')                                                             # 22
    lines.append('const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;')  # 23
    lines.append('')                                                             # 24

    # Line 25: function #2
    lines.append('function validateEmail(email: string): ValidationResult {')    # 25
    lines.append('  const errors: string[] = [];')                               # 26
    lines.append('  if (!email || email.trim().length === 0) {')                 # 27
    lines.append('    errors.push("Email address is required");')                # 28
    lines.append('  } else if (!EMAIL_REGEX.test(email)) {')                     # 29
    lines.append('    errors.push("Invalid email format");')                     # 30
    lines.append('  }')                                                          # 31
    lines.append('  return { isValid: errors.length === 0, errors };')           # 32
    lines.append('}')                                                            # 33
    lines.append('')                                                             # 34

    # Lines 35-39: code between functions
    lines.append('type DateFormatStyle = "short" | "medium" | "long" | "full";') # 35
    lines.append('')                                                             # 36
    lines.append('const DATE_CACHE = new Map<string, Intl.DateTimeFormat>();')   # 37
    lines.append('')                                                             # 38
    lines.append('// Formats a date according to the specified style')           # 39

    # Line 40: function #3
    lines.append('function formatDate(date: Date, style: DateFormatStyle = "medium"): string {')  # 40
    lines.append('  const key = `${DEFAULT_LOCALE}-${style}`;')                  # 41
    lines.append('  if (!DATE_CACHE.has(key)) {')                                # 42
    lines.append('    DATE_CACHE.set(key, new Intl.DateTimeFormat(DEFAULT_LOCALE, {')  # 43
    lines.append('      dateStyle: style,')                                      # 44
    lines.append('    }));')                                                     # 45
    lines.append('  }')                                                          # 46
    lines.append('  return DATE_CACHE.get(key)!.format(date);')                  # 47
    lines.append('}')                                                            # 48
    lines.append('')                                                             # 49

    # Lines 50-54: code between functions
    lines.append('const DEBOUNCE_TIMERS = new Map<string, NodeJS.Timeout>();')   # 50
    lines.append('')                                                             # 51
    lines.append('// Creates a debounced version of the provided callback')      # 52
    lines.append('// Useful for search inputs and resize handlers')              # 53
    lines.append('')                                                             # 54

    # Line 55: function #4
    lines.append('function debounce<T extends (...args: any[]) => void>(')       # 55
    lines.append('  callback: T,')                                               # 56
    lines.append('  delay: number = 300')                                        # 57
    lines.append('): (...args: Parameters<T>) => void {')                        # 58
    lines.append('  let timeoutId: NodeJS.Timeout;')                             # 59
    lines.append('  return (...args: Parameters<T>) => {')                       # 60
    lines.append('    clearTimeout(timeoutId);')                                 # 61
    lines.append('    timeoutId = setTimeout(() => callback(...args), delay);')   # 62
    lines.append('  };')                                                         # 63
    lines.append('}')                                                            # 64
    lines.append('')                                                             # 65

    # Lines 66-69: code between functions
    lines.append('// Deep clones an object using structured clone algorithm')    # 66
    lines.append('// Falls back to JSON parse/stringify for environments')       # 67
    lines.append('// that do not support structuredClone')                        # 68
    lines.append('')                                                             # 69

    # Line 70: function #5
    lines.append('function deepClone<T>(obj: T): T {')                           # 70
    lines.append('  if (typeof structuredClone === "function") {')               # 71
    lines.append('    return structuredClone(obj);')                              # 72
    lines.append('  }')                                                          # 73
    lines.append('  return JSON.parse(JSON.stringify(obj));')                     # 74
    lines.append('}')                                                            # 75

    content = '\n'.join(lines) + '\n'
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Also create a minimal tsconfig and package.json for realism
    tsconfig = '''{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
'''
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        f.write(tsconfig)

    pkg = '''{
  "name": "frontend-app",
  "version": "1.2.0",
  "description": "Frontend application with utility functions",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "test": "jest"
  }
}
'''
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write(pkg)

    # Create a types file referenced by the import
    types_dir = f'{PROJECT_DIR}/src/types'
    os.makedirs(types_dir, exist_ok=True)
    with open(f'{types_dir}/index.ts', 'w') as f:
        f.write('''export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user" | "viewer";
  createdAt: Date;
}

export interface Transaction {
  id: string;
  amount: number;
  currency: string;
  timestamp: Date;
  status: "pending" | "completed" | "failed";
}
''')

    # Launch VSCode with the project folder, then open the specific file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code --goto "{OUTPUT}:1"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
