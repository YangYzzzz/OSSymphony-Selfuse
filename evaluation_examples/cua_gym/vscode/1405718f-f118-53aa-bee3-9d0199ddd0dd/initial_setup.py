"""
Initial Setup: Configure Tailwind CSS IntelliSense extension settings
Task ID: vscode_we_070
Domain: vscode

Creates a Next.js project workspace and opens VSCode with empty user settings.
The bradlc.vscode-tailwindcss extension should already be installed on the VM image.
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
WORKSPACE = os.path.join(HOME, 'workspace')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_nextjs_project():
    """Create a realistic Next.js project structure."""
    os.makedirs(WORKSPACE, exist_ok=True)

    # package.json
    package_json = {
        "name": "acme-dashboard",
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
            "react-dom": "^18.2.0",
            "tailwindcss": "^3.4.1",
            "autoprefixer": "^10.4.17",
            "postcss": "^8.4.33"
        },
        "devDependencies": {
            "@types/node": "^20.11.5",
            "@types/react": "^18.2.48",
            "typescript": "^5.3.3"
        }
    }
    with open(os.path.join(WORKSPACE, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # tailwind.config.ts
    tailwind_config = '''import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          700: '#1d4ed8',
        },
        accent: '#f59e0b',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
export default config
'''
    with open(os.path.join(WORKSPACE, 'tailwind.config.ts'), 'w') as f:
        f.write(tailwind_config)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "paths": {
                "@/*": ["./src/*"]
            }
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
        "exclude": ["node_modules"]
    }
    with open(os.path.join(WORKSPACE, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # postcss.config.js
    postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''
    with open(os.path.join(WORKSPACE, 'postcss.config.js'), 'w') as f:
        f.write(postcss_config)

    # next.config.js
    next_config = '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
'''
    with open(os.path.join(WORKSPACE, 'next.config.js'), 'w') as f:
        f.write(next_config)

    # Create src directory structure
    src_app = os.path.join(WORKSPACE, 'src', 'app')
    src_components = os.path.join(WORKSPACE, 'src', 'components')
    os.makedirs(src_app, exist_ok=True)
    os.makedirs(src_components, exist_ok=True)

    # src/app/globals.css
    globals_css = '''@tailwind base;
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
'''
    with open(os.path.join(src_app, 'globals.css'), 'w') as f:
        f.write(globals_css)

    # src/app/layout.tsx
    layout_tsx = '''import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Acme Dashboard',
  description: 'Internal analytics dashboard for Acme Corp',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
'''
    with open(os.path.join(src_app, 'layout.tsx'), 'w') as f:
        f.write(layout_tsx)

    # src/app/page.tsx
    page_tsx = '''import Dashboard from '../components/Dashboard'

export default function Home() {
  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <h1 className="text-3xl font-bold text-primary-700 mb-6">
        Acme Dashboard
      </h1>
      <Dashboard />
    </main>
  )
}
'''
    with open(os.path.join(src_app, 'page.tsx'), 'w') as f:
        f.write(page_tsx)

    # src/components/Dashboard.tsx
    dashboard_tsx = '''\'use client\'

import React from 'react'

interface MetricCardProps {
  title: string
  value: string
  change: string
  tw?: string
}

function MetricCard({ title, value, change, tw }: MetricCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <p className="text-2xl font-semibold mt-2">{value}</p>
      <span className={`text-sm ${change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
        {change}
      </span>
    </div>
  )
}

export default function Dashboard() {
  const metrics = [
    { title: 'Total Revenue', value: '$45,231.89', change: '+20.1%' },
    { title: 'Subscriptions', value: '2,350', change: '+180.1%' },
    { title: 'Active Users', value: '12,234', change: '+19%' },
    { title: 'Bounce Rate', value: '23.5%', change: '-4.3%' },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {metrics.map((metric) => (
        <MetricCard key={metric.title} {...metric} />
      ))}
    </div>
  )
}
'''
    with open(os.path.join(src_components, 'Dashboard.tsx'), 'w') as f:
        f.write(dashboard_tsx)

    print(f'Next.js project created at {WORKSPACE}')


def setup_vscode_settings():
    """Set up empty VSCode user settings."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    # Write empty settings (no tailwindCSS configuration yet)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'VSCode settings initialized (empty): {SETTINGS_PATH}')


def main():
    create_nextjs_project()
    setup_vscode_settings()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
