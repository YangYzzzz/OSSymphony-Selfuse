"""
Initial Setup: Set up Storybook integration in VSCode
Task ID: vscode_web_078
Domain: vscode

Creates a realistic React project with Storybook installed and configured,
with stories in src/components/**/*.stories.tsx. No launch.json or Storybook
extension exists yet. VSCode opens with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_078'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
STORYBOOK_DIR = f'{PROJECT_DIR}/.storybook'
SRC_DIR = f'{PROJECT_DIR}/src'
COMPONENTS_DIR = f'{SRC_DIR}/components'


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


def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    # --- package.json ---
    package_json = {
        "name": "react-app",
        "version": "1.2.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "typescript": "^5.3.3"
        },
        "devDependencies": {
            "@storybook/addon-essentials": "^7.6.10",
            "@storybook/addon-interactions": "^7.6.10",
            "@storybook/addon-links": "^7.6.10",
            "@storybook/blocks": "^7.6.10",
            "@storybook/react": "^7.6.10",
            "@storybook/react-vite": "^7.6.10",
            "@storybook/testing-library": "^0.2.2",
            "@types/react": "^18.2.48",
            "@types/react-dom": "^18.2.18"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject",
            "storybook": "storybook dev -p 6006",
            "build-storybook": "storybook build"
        }
    }
    create_file(f'{PROJECT_DIR}/package.json', json.dumps(package_json, indent=2))

    # --- tsconfig.json ---
    tsconfig = {
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "esModuleInterop": True,
            "allowSyntheticDefaultImports": True,
            "strict": True,
            "forceConsistentCasingInFileNames": True,
            "noFallthroughCasesInSwitch": True,
            "module": "esnext",
            "moduleResolution": "node",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "noEmit": True,
            "jsx": "react-jsx"
        },
        "include": ["src"]
    }
    create_file(f'{PROJECT_DIR}/tsconfig.json', json.dumps(tsconfig, indent=2))

    # --- .storybook/main.ts ---
    storybook_main = '''import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
  ],
  framework: {
    name: "@storybook/react-vite",
    options: {},
  },
  docs: {
    autodocs: "tag",
  },
};
export default config;
'''
    create_file(f'{STORYBOOK_DIR}/main.ts', storybook_main)

    # --- .storybook/preview.ts ---
    storybook_preview = '''import type { Preview } from "@storybook/react";

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
'''
    create_file(f'{STORYBOOK_DIR}/preview.ts', storybook_preview)

    # --- src/index.tsx ---
    index_tsx = '''import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
    create_file(f'{SRC_DIR}/index.tsx', index_tsx)

    # --- src/App.tsx ---
    app_tsx = '''import React from "react";
import { Button } from "./components/Button/Button";
import { Card } from "./components/Card/Card";

function App() {
  return (
    <div className="App">
      <header>
        <h1>Product Dashboard</h1>
      </header>
      <main>
        <Card title="Welcome" description="Get started with our product dashboard." />
        <Button label="Get Started" variant="primary" />
      </main>
    </div>
  );
}

export default App;
'''
    create_file(f'{SRC_DIR}/App.tsx', app_tsx)

    # --- src/components/Button/Button.tsx ---
    button_tsx = '''import React from "react";

export interface ButtonProps {
  label: string;
  variant?: "primary" | "secondary" | "danger";
  size?: "small" | "medium" | "large";
  disabled?: boolean;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  variant = "primary",
  size = "medium",
  disabled = false,
  onClick,
}) => {
  const baseStyles: React.CSSProperties = {
    padding: size === "small" ? "6px 12px" : size === "large" ? "14px 28px" : "10px 20px",
    fontSize: size === "small" ? "12px" : size === "large" ? "18px" : "14px",
    borderRadius: "6px",
    border: "none",
    cursor: disabled ? "not-allowed" : "pointer",
    opacity: disabled ? 0.6 : 1,
    fontWeight: 600,
  };

  const variantStyles: Record<string, React.CSSProperties> = {
    primary: { backgroundColor: "#2563eb", color: "#ffffff" },
    secondary: { backgroundColor: "#6b7280", color: "#ffffff" },
    danger: { backgroundColor: "#dc2626", color: "#ffffff" },
  };

  return (
    <button
      style={{ ...baseStyles, ...variantStyles[variant] }}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
};
'''
    create_file(f'{COMPONENTS_DIR}/Button/Button.tsx', button_tsx)

    # --- src/components/Button/Button.stories.tsx ---
    button_stories = '''import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["primary", "secondary", "danger"],
    },
    size: {
      control: "select",
      options: ["small", "medium", "large"],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    label: "Primary Button",
    variant: "primary",
  },
};

export const Secondary: Story = {
  args: {
    label: "Secondary Button",
    variant: "secondary",
  },
};

export const Danger: Story = {
  args: {
    label: "Delete Item",
    variant: "danger",
  },
};

export const Small: Story = {
  args: {
    label: "Small",
    size: "small",
    variant: "primary",
  },
};

export const Large: Story = {
  args: {
    label: "Large Button",
    size: "large",
    variant: "primary",
  },
};

export const Disabled: Story = {
  args: {
    label: "Disabled",
    variant: "primary",
    disabled: true,
  },
};
'''
    create_file(f'{COMPONENTS_DIR}/Button/Button.stories.tsx', button_stories)

    # --- src/components/Card/Card.tsx ---
    card_tsx = '''import React from "react";

export interface CardProps {
  title: string;
  description: string;
  imageUrl?: string;
  footer?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ title, description, imageUrl, footer }) => {
  return (
    <div
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: "8px",
        overflow: "hidden",
        maxWidth: "360px",
        boxShadow: "0 1px 3px rgba(0,0,0,0.12)",
      }}
    >
      {imageUrl && (
        <img src={imageUrl} alt={title} style={{ width: "100%", height: "200px", objectFit: "cover" }} />
      )}
      <div style={{ padding: "16px" }}>
        <h3 style={{ margin: "0 0 8px 0", fontSize: "18px", fontWeight: 600 }}>{title}</h3>
        <p style={{ margin: 0, color: "#6b7280", fontSize: "14px", lineHeight: 1.5 }}>{description}</p>
      </div>
      {footer && (
        <div style={{ padding: "12px 16px", borderTop: "1px solid #e5e7eb", backgroundColor: "#f9fafb" }}>
          {footer}
        </div>
      )}
    </div>
  );
};
'''
    create_file(f'{COMPONENTS_DIR}/Card/Card.tsx', card_tsx)

    # --- src/components/Card/Card.stories.tsx ---
    card_stories = '''import type { Meta, StoryObj } from "@storybook/react";
import { Card } from "./Card";

const meta: Meta<typeof Card> = {
  title: "Components/Card",
  component: Card,
  tags: ["autodocs"],
};

export default meta;
type Story = StoryObj<typeof Card>;

export const Default: Story = {
  args: {
    title: "Getting Started",
    description: "Learn how to set up your development environment and start building with our component library.",
  },
};

export const WithImage: Story = {
  args: {
    title: "Dashboard Overview",
    description: "Monitor your application metrics and user engagement in real-time.",
    imageUrl: "https://via.placeholder.com/360x200/2563eb/ffffff?text=Dashboard",
  },
};

export const WithFooter: Story = {
  args: {
    title: "Team Updates",
    description: "Sarah Chen pushed 3 commits to the feature/auth-refactor branch.",
  },
};
'''
    create_file(f'{COMPONENTS_DIR}/Card/Card.stories.tsx', card_stories)

    # --- src/components/Header/Header.tsx ---
    header_tsx = '''import React from "react";

export interface HeaderProps {
  title: string;
  subtitle?: string;
  showNav?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ title, subtitle, showNav = true }) => {
  return (
    <header
      style={{
        backgroundColor: "#1e293b",
        color: "#ffffff",
        padding: "16px 24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <div>
        <h1 style={{ margin: 0, fontSize: "22px", fontWeight: 700 }}>{title}</h1>
        {subtitle && <p style={{ margin: "4px 0 0", fontSize: "14px", color: "#94a3b8" }}>{subtitle}</p>}
      </div>
      {showNav && (
        <nav style={{ display: "flex", gap: "16px" }}>
          <a href="#" style={{ color: "#e2e8f0", textDecoration: "none", fontSize: "14px" }}>Dashboard</a>
          <a href="#" style={{ color: "#e2e8f0", textDecoration: "none", fontSize: "14px" }}>Components</a>
          <a href="#" style={{ color: "#e2e8f0", textDecoration: "none", fontSize: "14px" }}>Settings</a>
        </nav>
      )}
    </header>
  );
};
'''
    create_file(f'{COMPONENTS_DIR}/Header/Header.tsx', header_tsx)

    # --- src/components/Header/Header.stories.tsx ---
    header_stories = '''import type { Meta, StoryObj } from "@storybook/react";
import { Header } from "./Header";

const meta: Meta<typeof Header> = {
  title: "Components/Header",
  component: Header,
  tags: ["autodocs"],
};

export default meta;
type Story = StoryObj<typeof Header>;

export const Default: Story = {
  args: {
    title: "Product Dashboard",
    subtitle: "Manage your application components",
    showNav: true,
  },
};

export const WithoutNav: Story = {
  args: {
    title: "Storybook Preview",
    showNav: false,
  },
};

export const MinimalHeader: Story = {
  args: {
    title: "React App",
    subtitle: "v1.2.0",
    showNav: true,
  },
};
'''
    create_file(f'{COMPONENTS_DIR}/Header/Header.stories.tsx', header_stories)

    # --- .vscode/settings.json (basic workspace settings, NO launch config) ---
    vscode_settings = {
        "typescript.tsdk": "node_modules/typescript/lib",
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    }
    os.makedirs(VSCODE_DIR, exist_ok=True)
    create_file(f'{VSCODE_DIR}/settings.json', json.dumps(vscode_settings, indent=2))

    # --- .gitignore ---
    gitignore = '''node_modules/
build/
dist/
.env
.env.local
storybook-static/
'''
    create_file(f'{PROJECT_DIR}/.gitignore', gitignore)

    # --- README.md ---
    readme = '''# React App

A React application with Storybook component library.

## Getting Started

```bash
npm install
npm start
```

## Storybook

```bash
npm run storybook
```

Stories are located in `src/components/**/*.stories.tsx`.

## Project Structure

```
src/
  components/
    Button/
      Button.tsx
      Button.stories.tsx
    Card/
      Card.tsx
      Card.stories.tsx
    Header/
      Header.tsx
      Header.stories.tsx
  App.tsx
  index.tsx
.storybook/
  main.ts
  preview.ts
```
'''
    create_file(f'{PROJECT_DIR}/README.md', readme)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Stories in: {COMPONENTS_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
