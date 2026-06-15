"""
Initial Setup: Create a Playwright project structure without .vscode/launch.json
Task ID: vscode_gf3_057
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_057'
PROJECT_DIR = f'{WORKDIR}/projects/playwright-project'

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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/pages', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/.bin', exist_ok=True)

    # package.json
    package_json = {
        "name": "playwright-project",
        "version": "1.0.0",
        "description": "E2E tests for the customer portal using Playwright",
        "scripts": {
            "test": "playwright test",
            "test:headed": "playwright test --headed",
            "test:debug": "playwright test --debug",
            "report": "playwright show-report"
        },
        "devDependencies": {
            "@playwright/test": "^1.42.0",
            "typescript": "^5.3.3"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # playwright.config.ts
    playwright_config = '''import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
'''
    with open(f'{PROJECT_DIR}/playwright.config.ts', 'w') as f:
        f.write(playwright_config)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "strict": True,
            "esModuleInterop": True,
            "outDir": "./dist",
            "rootDir": "."
        },
        "include": ["tests/**/*.ts", "pages/**/*.ts"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # Sample test file: tests/login.spec.ts
    login_test = '''import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';

test.describe('Login Flow', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('should login with valid credentials', async ({ page }) => {
    await loginPage.fillEmail('admin@example.com');
    await loginPage.fillPassword('SecurePass123!');
    await loginPage.clickSubmit();
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome back');
  });

  test('should show error for invalid password', async ({ page }) => {
    await loginPage.fillEmail('admin@example.com');
    await loginPage.fillPassword('wrongpassword');
    await loginPage.clickSubmit();
    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText('Invalid credentials');
  });

  test('should redirect unauthenticated users to login', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/login');
  });
});
'''
    with open(f'{PROJECT_DIR}/tests/login.spec.ts', 'w') as f:
        f.write(login_test)

    # Sample test file: tests/checkout.spec.ts
    checkout_test = '''import { test, expect } from '@playwright/test';

test.describe('Checkout Process', () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('#email', 'customer@example.com');
    await page.fill('#password', 'CustomerPass456!');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });

  test('should add item to cart and proceed to checkout', async ({ page }) => {
    await page.goto('/products');
    await page.click('[data-product-id="SKU-1042"] .add-to-cart');
    await expect(page.locator('.cart-count')).toContainText('1');

    await page.goto('/cart');
    await expect(page.locator('.cart-item')).toHaveCount(1);
    await page.click('#proceed-checkout');
    await expect(page).toHaveURL('/checkout');
  });

  test('should validate shipping address fields', async ({ page }) => {
    await page.goto('/checkout');
    await page.click('#submit-order');
    await expect(page.locator('.field-error')).toHaveCount(4);
  });
});
'''
    with open(f'{PROJECT_DIR}/tests/checkout.spec.ts', 'w') as f:
        f.write(checkout_test)

    # Page object: pages/login.page.ts
    login_page = '''import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('#email');
    this.passwordInput = page.locator('#password');
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async fillEmail(email: string) {
    await this.emailInput.fill(email);
  }

  async fillPassword(password: string) {
    await this.passwordInput.fill(password);
  }

  async clickSubmit() {
    await this.submitButton.click();
  }
}
'''
    with open(f'{PROJECT_DIR}/pages/login.page.ts', 'w') as f:
        f.write(login_page)

    # Create a placeholder playwright binary in node_modules
    playwright_bin = '''#!/usr/bin/env node
// Playwright Test Runner
const { program } = require('commander');
program.parse(process.argv);
'''
    bin_path = f'{PROJECT_DIR}/node_modules/.bin/playwright'
    with open(bin_path, 'w') as f:
        f.write(playwright_bin)
    os.chmod(bin_path, 0o755)

    # .gitignore
    gitignore = '''node_modules/
test-results/
playwright-report/
blob-report/
dist/
.env
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # README.md
    readme = '''# Customer Portal E2E Tests

End-to-end tests for the customer portal application using Playwright.

## Setup

```bash
npm install
npx playwright install
```

## Running Tests

```bash
npm test                    # Run all tests
npm run test:headed         # Run with browser visible
npm run test:debug          # Run in debug mode
npx playwright test --ui    # Open Playwright UI mode
```

## Project Structure

- `tests/` - Test specifications
- `pages/` - Page Object Models
- `playwright.config.ts` - Playwright configuration
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Project structure created at: {PROJECT_DIR}')

    # NOTE: Do NOT create .vscode/launch.json - that is the task for the agent

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
