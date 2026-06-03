"""
Initial Setup: Next.js development workflow in ~/project
Task ID: vscode_wf_094
Domain: vscode

Creates a basic Next.js 14 project with app/ router.
TypeScript and ESLint are in package.json but NOT configured strictly.
No .eslintrc.json, .prettierrc, .vscode/ directory, or strict tsconfig.
"""

import json
import os
import shlex
import subprocess
import time

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

def create_initial():
    # Create project directory structure
    dirs = [
        os.path.join(PROJECT, 'app'),
        os.path.join(PROJECT, 'app', 'api', 'hello'),
        os.path.join(PROJECT, 'public'),
        os.path.join(PROJECT, 'styles'),
        os.path.join(PROJECT, 'components'),
        os.path.join(PROJECT, 'lib'),
        os.path.join(PROJECT, 'node_modules'),  # simulate installed
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- package.json (TypeScript and ESLint listed but not strictly configured) ---
    package_json = {
        "name": "nextjs-dashboard",
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "14.1.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/react": "^18.2.48",
            "@types/react-dom": "^18.2.18",
            "@types/node": "^20.11.5",
            "eslint": "^8.56.0",
            "eslint-config-next": "14.1.0"
        }
    }
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json (basic, NOT strict) ---
    tsconfig = {
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "esModuleInterop": True,
            "allowSyntheticDefaultImports": True,
            "forceConsistentCasingInFileNames": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
        "exclude": ["node_modules"]
    }
    with open(os.path.join(PROJECT, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- next.config.js (basic) ---
    next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
"""
    with open(os.path.join(PROJECT, 'next.config.js'), 'w') as f:
        f.write(next_config)

    # --- app/layout.tsx ---
    layout_tsx = """import type { Metadata } from 'next'
import '../styles/globals.css'

export const metadata: Metadata = {
  title: 'Dashboard App',
  description: 'Next.js 14 Dashboard Application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
"""
    with open(os.path.join(PROJECT, 'app', 'layout.tsx'), 'w') as f:
        f.write(layout_tsx)

    # --- app/page.tsx ---
    page_tsx = """export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8">Dashboard</h1>
        <p className="text-lg text-gray-600">
          Welcome to the Next.js 14 Dashboard Application.
          This project uses the App Router with TypeScript.
        </p>
      </div>
    </main>
  )
}
"""
    with open(os.path.join(PROJECT, 'app', 'page.tsx'), 'w') as f:
        f.write(page_tsx)

    # --- app/api/hello/route.ts ---
    api_route = """import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({ message: 'Hello from the API' })
}
"""
    with open(os.path.join(PROJECT, 'app', 'api', 'hello', 'route.ts'), 'w') as f:
        f.write(api_route)

    # --- components/Header.tsx ---
    header_tsx = """interface HeaderProps {
  title: string
  subtitle?: string
}

export default function Header({ title, subtitle }: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-gray-500">{subtitle}</p>}
      </div>
    </header>
  )
}
"""
    with open(os.path.join(PROJECT, 'components', 'Header.tsx'), 'w') as f:
        f.write(header_tsx)

    # --- components/Card.tsx ---
    card_tsx = """interface CardProps {
  title: string
  value: string | number
  change?: string
}

export default function Card({ title, value, change }: CardProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <p className="mt-2 text-3xl font-semibold text-gray-900">{value}</p>
      {change && (
        <p className="mt-2 text-sm text-green-600">{change}</p>
      )}
    </div>
  )
}
"""
    with open(os.path.join(PROJECT, 'components', 'Card.tsx'), 'w') as f:
        f.write(card_tsx)

    # --- lib/utils.ts ---
    utils_ts = """export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount)
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date)
}

export function cn(...classes: string[]): string {
  return classes.filter(Boolean).join(' ')
}
"""
    with open(os.path.join(PROJECT, 'lib', 'utils.ts'), 'w') as f:
        f.write(utils_ts)

    # --- styles/globals.css ---
    globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
    to bottom,
    transparent,
    rgb(var(--background-end-rgb))
  ) rgb(var(--background-start-rgb));
}
"""
    with open(os.path.join(PROJECT, 'styles', 'globals.css'), 'w') as f:
        f.write(globals_css)

    # --- styles/Dashboard.module.css ---
    dashboard_css = """.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a2e;
}
"""
    with open(os.path.join(PROJECT, 'styles', 'Dashboard.module.css'), 'w') as f:
        f.write(dashboard_css)

    # --- next-env.d.ts ---
    next_env = """/// <reference types="next" />
/// <reference types="next/image-types/global" />

// NOTE: This file should not be edited
// see https://nextjs.org/docs/basic-features/typescript for more information.
"""
    with open(os.path.join(PROJECT, 'next-env.d.ts'), 'w') as f:
        f.write(next_env)

    print(f'Initial project created at: {PROJECT}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
