"""
Initial Setup: Configure multi-root workspace with frontend and backend folders
Task ID: vscode_stu_059
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_059'

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
    # Create the webdev directory structure
    frontend_dir = os.path.join(WORKDIR, 'webdev', 'frontend')
    backend_dir = os.path.join(WORKDIR, 'webdev', 'backend')
    os.makedirs(frontend_dir, exist_ok=True)
    os.makedirs(backend_dir, exist_ok=True)

    # --- Frontend project files ---
    # package.json
    with open(os.path.join(frontend_dir, 'package.json'), 'w') as f:
        f.write("""{
    "name": "acme-dashboard-frontend",
    "version": "2.4.1",
    "private": true,
    "description": "Acme Corp internal dashboard - React frontend",
    "scripts": {
        "dev": "vite",
        "build": "tsc && vite build",
        "lint": "eslint src --ext ts,tsx",
        "preview": "vite preview",
        "test": "vitest"
    },
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "react-router-dom": "^6.20.0",
        "axios": "^1.6.2",
        "@tanstack/react-query": "^5.12.0",
        "tailwindcss": "^3.3.6"
    },
    "devDependencies": {
        "@types/react": "^18.2.43",
        "@types/react-dom": "^18.2.17",
        "typescript": "^5.3.2",
        "vite": "^5.0.4",
        "vitest": "^1.0.0"
    }
}
""")

    # src/App.tsx
    src_dir = os.path.join(frontend_dir, 'src')
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'App.tsx'), 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import Sidebar from './components/Sidebar';

function App() {
    return (
        <BrowserRouter>
            <div className="flex h-screen bg-gray-100">
                <Sidebar />
                <main className="flex-1 overflow-y-auto p-6">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/settings" element={<Settings />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    );
}

export default App;
""")

    # src/components/Sidebar.tsx
    comp_dir = os.path.join(src_dir, 'components')
    os.makedirs(comp_dir, exist_ok=True)
    with open(os.path.join(comp_dir, 'Sidebar.tsx'), 'w') as f:
        f.write("""import React from 'react';
import { NavLink } from 'react-router-dom';

const navItems = [
    { path: '/', label: 'Dashboard', icon: 'chart-bar' },
    { path: '/settings', label: 'Settings', icon: 'cog' },
];

export default function Sidebar() {
    return (
        <aside className="w-64 bg-white shadow-md">
            <div className="p-4 border-b">
                <h1 className="text-xl font-bold text-indigo-600">Acme Dashboard</h1>
            </div>
            <nav className="mt-4">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `block px-4 py-2 ${isActive ? 'bg-indigo-50 text-indigo-600' : 'text-gray-700 hover:bg-gray-50'}`
                        }
                    >
                        {item.label}
                    </NavLink>
                ))}
            </nav>
        </aside>
    );
}
""")

    # src/pages/Dashboard.tsx
    pages_dir = os.path.join(src_dir, 'pages')
    os.makedirs(pages_dir, exist_ok=True)
    with open(os.path.join(pages_dir, 'Dashboard.tsx'), 'w') as f:
        f.write("""import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchMetrics } from '../api/metrics';

export default function Dashboard() {
    const { data: metrics, isLoading } = useQuery({
        queryKey: ['metrics'],
        queryFn: fetchMetrics,
    });

    if (isLoading) return <div className="text-center py-8">Loading metrics...</div>;

    return (
        <div>
            <h2 className="text-2xl font-semibold mb-6">Dashboard Overview</h2>
            <div className="grid grid-cols-3 gap-4">
                <div className="bg-white rounded-lg shadow p-4">
                    <p className="text-sm text-gray-500">Total Revenue</p>
                    <p className="text-2xl font-bold">${metrics?.totalRevenue?.toLocaleString()}</p>
                </div>
                <div className="bg-white rounded-lg shadow p-4">
                    <p className="text-sm text-gray-500">Active Users</p>
                    <p className="text-2xl font-bold">{metrics?.activeUsers?.toLocaleString()}</p>
                </div>
                <div className="bg-white rounded-lg shadow p-4">
                    <p className="text-sm text-gray-500">Conversion Rate</p>
                    <p className="text-2xl font-bold">{metrics?.conversionRate}%</p>
                </div>
            </div>
        </div>
    );
}
""")

    # src/api/metrics.ts
    api_dir = os.path.join(src_dir, 'api')
    os.makedirs(api_dir, exist_ok=True)
    with open(os.path.join(api_dir, 'metrics.ts'), 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

export async function fetchMetrics() {
    const response = await axios.get(`${API_BASE}/metrics`);
    return response.data;
}

export async function fetchRevenueHistory(period: string = '30d') {
    const response = await axios.get(`${API_BASE}/metrics/revenue`, {
        params: { period },
    });
    return response.data;
}
""")

    # tsconfig.json
    with open(os.path.join(frontend_dir, 'tsconfig.json'), 'w') as f:
        f.write("""{
    "compilerOptions": {
        "target": "ES2020",
        "useDefineForClassFields": true,
        "lib": ["ES2020", "DOM", "DOM.Iterable"],
        "module": "ESNext",
        "skipLibCheck": true,
        "moduleResolution": "bundler",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "jsx": "react-jsx",
        "strict": true,
        "noUnusedLocals": true,
        "noFallthroughCasesInSwitch": true
    },
    "include": ["src"]
}
""")

    # --- Backend project files ---
    # package.json
    with open(os.path.join(backend_dir, 'package.json'), 'w') as f:
        f.write("""{
    "name": "acme-dashboard-backend",
    "version": "2.4.1",
    "description": "Acme Corp internal dashboard - Express API backend",
    "main": "dist/server.js",
    "scripts": {
        "dev": "tsx watch src/server.ts",
        "build": "tsc",
        "start": "node dist/server.js",
        "test": "jest --coverage",
        "migrate": "prisma migrate dev"
    },
    "dependencies": {
        "express": "^4.18.2",
        "@prisma/client": "^5.7.0",
        "cors": "^2.8.5",
        "helmet": "^7.1.0",
        "jsonwebtoken": "^9.0.2",
        "bcryptjs": "^2.4.3",
        "zod": "^3.22.4",
        "winston": "^3.11.0"
    },
    "devDependencies": {
        "@types/express": "^4.17.21",
        "@types/cors": "^2.8.17",
        "@types/jsonwebtoken": "^9.0.5",
        "typescript": "^5.3.2",
        "tsx": "^4.6.2",
        "jest": "^29.7.0",
        "prisma": "^5.7.0"
    }
}
""")

    # src/server.ts
    backend_src = os.path.join(backend_dir, 'src')
    os.makedirs(backend_src, exist_ok=True)
    with open(os.path.join(backend_src, 'server.ts'), 'w') as f:
        f.write("""import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { metricsRouter } from './routes/metrics';
import { authRouter } from './routes/auth';
import { errorHandler } from './middleware/errorHandler';
import { logger } from './utils/logger';

const app = express();
const PORT = process.env.PORT || 3001;

app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN || 'http://localhost:5173' }));
app.use(express.json());

app.use('/api/auth', authRouter);
app.use('/api/metrics', metricsRouter);

app.use(errorHandler);

app.listen(PORT, () => {
    logger.info(`Server running on port ${PORT}`);
});

export default app;
""")

    # src/routes/metrics.ts
    routes_dir = os.path.join(backend_src, 'routes')
    os.makedirs(routes_dir, exist_ok=True)
    with open(os.path.join(routes_dir, 'metrics.ts'), 'w') as f:
        f.write("""import { Router } from 'express';
import { prisma } from '../utils/db';
import { authenticate } from '../middleware/auth';

export const metricsRouter = Router();

metricsRouter.get('/', authenticate, async (req, res, next) => {
    try {
        const totalRevenue = await prisma.order.aggregate({
            _sum: { amount: true },
            where: { status: 'completed' },
        });
        const activeUsers = await prisma.user.count({
            where: { lastActive: { gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } },
        });
        const totalOrders = await prisma.order.count({ where: { status: 'completed' } });
        const totalVisitors = await prisma.session.count({
            where: { createdAt: { gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } },
        });

        res.json({
            totalRevenue: totalRevenue._sum.amount || 0,
            activeUsers,
            conversionRate: totalVisitors > 0
                ? ((totalOrders / totalVisitors) * 100).toFixed(1)
                : '0.0',
        });
    } catch (error) {
        next(error);
    }
});
""")

    # src/utils/logger.ts
    utils_dir = os.path.join(backend_src, 'utils')
    os.makedirs(utils_dir, exist_ok=True)
    with open(os.path.join(utils_dir, 'logger.ts'), 'w') as f:
        f.write("""import winston from 'winston';

export const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.simple()
            ),
        }),
    ],
});
""")

    # tsconfig.json
    with open(os.path.join(backend_dir, 'tsconfig.json'), 'w') as f:
        f.write("""{
    "compilerOptions": {
        "target": "ES2020",
        "module": "commonjs",
        "lib": ["ES2020"],
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,
        "resolveJsonModule": true,
        "declaration": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist"]
}
""")

    # .env.example in backend
    with open(os.path.join(backend_dir, '.env.example'), 'w') as f:
        f.write("""DATABASE_URL="postgresql://acme:acme_secret@localhost:5432/acme_dashboard"
PORT=3001
CORS_ORIGIN=http://localhost:5173
JWT_SECRET=replace-with-a-secure-random-string
LOG_LEVEL=info
""")

    print(f'Initial directories and files created under {WORKDIR}/webdev/')

    # Make sure no .code-workspace file exists
    workspace_path = os.path.join(WORKDIR, f'{TASK_ID}.code-workspace')
    if os.path.exists(workspace_path):
        os.remove(workspace_path)

    # Launch VSCode with no workspace (just open the app)
    launch_gui('code', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
