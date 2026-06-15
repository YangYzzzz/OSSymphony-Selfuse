"""
Initial Setup: Configure TypeScript project references for Angular project
Task ID: vscode_fix_095
Domain: vscode

Creates an Angular project with tsconfig.json that does NOT reference
tsconfig.app.json or tsconfig.spec.json. Test files show 'Cannot find name
describe' errors because tsconfig.spec.json lacks "types": ["jasmine"].
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_095'
PROJECT_DIR = os.path.join(WORKDIR, 'angular-project')


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
    dirs = [
        os.path.join(PROJECT_DIR, 'src', 'app'),
        os.path.join(PROJECT_DIR, 'src', 'environments'),
        os.path.join(PROJECT_DIR, 'node_modules', '@types', 'jasmine'),
        os.path.join(PROJECT_DIR, 'node_modules', '@types', 'node'),
        os.path.join(PROJECT_DIR, '.vscode'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- tsconfig.json (base) — NO references array ---
    tsconfig_base = {
        "compileOnSave": False,
        "compilerOptions": {
            "baseUrl": "./",
            "outDir": "./dist/out-tsc",
            "forceConsistentCasingInFileNames": True,
            "strict": True,
            "noImplicitOverride": True,
            "noPropertyAccessFromIndexSignature": True,
            "noImplicitReturns": True,
            "noFallthroughCasesInSwitch": True,
            "sourceMap": True,
            "declaration": False,
            "downlevelIteration": True,
            "experimentalDecorators": True,
            "moduleResolution": "node",
            "importHelpers": True,
            "target": "ES2022",
            "module": "ES2022",
            "useDefineForClassFields": False,
            "lib": ["ES2022", "dom"]
        }
        # NOTE: No "references" key — this is what the task asks to add
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig_base, f, indent=2)

    # --- tsconfig.app.json ---
    tsconfig_app = {
        "extends": "./tsconfig.json",
        "compilerOptions": {
            "outDir": "./out-tsc/app",
            "types": []
        },
        "files": [
            "src/main.ts"
        ],
        "include": [
            "src/**/*.d.ts",
            "src/**/*.ts"
        ],
        "exclude": [
            "src/**/*.spec.ts"
        ]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.app.json'), 'w') as f:
        json.dump(tsconfig_app, f, indent=2)

    # --- tsconfig.spec.json — NO "types": ["jasmine"] ---
    tsconfig_spec = {
        "extends": "./tsconfig.json",
        "compilerOptions": {
            "outDir": "./out-tsc/spec"
        },
        "files": [
            "src/test.ts"
        ],
        "include": [
            "src/**/*.spec.ts",
            "src/**/*.d.ts"
        ]
        # NOTE: No "types": ["jasmine"] in compilerOptions — this is what the task asks to add
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.spec.json'), 'w') as f:
        json.dump(tsconfig_spec, f, indent=2)

    # --- package.json ---
    package_json = {
        "name": "angular-project",
        "version": "16.2.0",
        "scripts": {
            "ng": "ng",
            "start": "ng serve",
            "build": "ng build",
            "test": "ng test",
            "lint": "ng lint"
        },
        "private": True,
        "dependencies": {
            "@angular/animations": "^16.2.0",
            "@angular/common": "^16.2.0",
            "@angular/compiler": "^16.2.0",
            "@angular/core": "^16.2.0",
            "@angular/forms": "^16.2.0",
            "@angular/platform-browser": "^16.2.0",
            "@angular/platform-browser-dynamic": "^16.2.0",
            "@angular/router": "^16.2.0",
            "rxjs": "~7.8.0",
            "tslib": "^2.3.0",
            "zone.js": "~0.13.0"
        },
        "devDependencies": {
            "@angular-devkit/build-angular": "^16.2.0",
            "@angular/cli": "^16.2.0",
            "@angular/compiler-cli": "^16.2.0",
            "@types/jasmine": "~4.3.0",
            "@types/node": "~18.16.0",
            "jasmine-core": "~4.6.0",
            "karma": "~6.4.0",
            "karma-chrome-launcher": "~3.2.0",
            "karma-coverage": "~2.2.0",
            "karma-jasmine": "~5.1.0",
            "karma-jasmine-html-reporter": "~2.1.0",
            "typescript": "~5.1.3"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- angular.json ---
    angular_json = {
        "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
        "version": 1,
        "newProjectRoot": "projects",
        "projects": {
            "angular-project": {
                "projectType": "application",
                "root": "",
                "sourceRoot": "src",
                "prefix": "app",
                "architect": {
                    "build": {
                        "builder": "@angular-devkit/build-angular:browser",
                        "options": {
                            "outputPath": "dist/angular-project",
                            "index": "src/index.html",
                            "main": "src/main.ts",
                            "polyfills": ["zone.js"],
                            "tsConfig": "tsconfig.app.json"
                        }
                    },
                    "test": {
                        "builder": "@angular-devkit/build-angular:karma",
                        "options": {
                            "polyfills": ["zone.js", "zone.js/testing"],
                            "tsConfig": "tsconfig.spec.json"
                        }
                    }
                }
            }
        }
    }
    with open(os.path.join(PROJECT_DIR, 'angular.json'), 'w') as f:
        json.dump(angular_json, f, indent=2)

    # --- src/main.ts ---
    with open(os.path.join(PROJECT_DIR, 'src', 'main.ts'), 'w') as f:
        f.write("""import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
""")

    # --- src/test.ts ---
    with open(os.path.join(PROJECT_DIR, 'src', 'test.ts'), 'w') as f:
        f.write("""// This file is required by karma.conf.js and loads recursively all the .spec and framework files
import 'zone.js/testing';
import { getTestBed } from '@angular/core/testing';
import {
  BrowserDynamicTestingModule,
  platformBrowserDynamicTesting
} from '@angular/platform-browser-dynamic/testing';

declare const require: {
  context(path: string, deep?: boolean, filter?: RegExp): {
    <T>(id: string): T;
    keys(): string[];
  };
};

// First, initialize the Angular testing environment.
getTestBed().initTestEnvironment(
  BrowserDynamicTestingModule,
  platformBrowserDynamicTesting(),
);

// Then we find all the tests.
const context = require.context('./', true, /\\.spec\\.ts$/);
// And load the modules.
context.keys().forEach(context);
""")

    # --- src/app/app.module.ts ---
    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'app.module.ts'), 'w') as f:
        f.write("""import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { UserService } from './services/user.service';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
  ],
  imports: [
    BrowserModule,
  ],
  providers: [UserService],
  bootstrap: [AppComponent]
})
export class AppModule { }
""")

    # --- src/app/app.component.ts ---
    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'app.component.ts'), 'w') as f:
        f.write("""import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular-project';
  version = '16.2.0';

  getWelcomeMessage(): string {
    return `Welcome to ${this.title} v${this.version}`;
  }
}
""")

    # --- src/app/app.component.html ---
    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'app.component.html'), 'w') as f:
        f.write("""<div class="app-container">
  <header>
    <h1>{{ getWelcomeMessage() }}</h1>
    <nav>
      <a routerLink="/dashboard">Dashboard</a>
      <a routerLink="/settings">Settings</a>
    </nav>
  </header>
  <main>
    <router-outlet></router-outlet>
  </main>
</div>
""")

    # --- src/app/app.component.css ---
    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'app.component.css'), 'w') as f:
        f.write(""".app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

header {
  background-color: #1976d2;
  color: white;
  padding: 16px 24px;
  border-radius: 4px;
  margin-bottom: 20px;
}

header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
}

nav a {
  color: white;
  text-decoration: none;
  margin-right: 16px;
}
""")

    # --- src/app/app.component.spec.ts (test file that shows errors) ---
    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'app.component.spec.ts'), 'w') as f:
        f.write("""import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'angular-project'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('angular-project');
  });

  it('should render welcome message', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Welcome to angular-project');
  });
});
""")

    # --- Create dashboard component and service for complexity ---
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'app', 'dashboard'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'app', 'services'), exist_ok=True)

    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'dashboard', 'dashboard.component.ts'), 'w') as f:
        f.write("""import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';

interface DashboardMetric {
  label: string;
  value: number;
  trend: 'up' | 'down' | 'stable';
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  metrics: DashboardMetric[] = [];
  lastUpdated: Date = new Date();

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.loadMetrics();
  }

  loadMetrics(): void {
    this.metrics = [
      { label: 'Active Users', value: 1284, trend: 'up' },
      { label: 'Revenue', value: 45230, trend: 'up' },
      { label: 'Bounce Rate', value: 23, trend: 'down' },
      { label: 'Avg Session', value: 342, trend: 'stable' },
    ];
    this.lastUpdated = new Date();
  }

  getFormattedValue(metric: DashboardMetric): string {
    if (metric.label === 'Revenue') {
      return `$${metric.value.toLocaleString()}`;
    }
    if (metric.label === 'Bounce Rate') {
      return `${metric.value}%`;
    }
    if (metric.label === 'Avg Session') {
      return `${metric.value}s`;
    }
    return metric.value.toLocaleString();
  }
}
""")

    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'dashboard', 'dashboard.component.html'), 'w') as f:
        f.write("""<div class="dashboard">
  <h2>Dashboard</h2>
  <p class="updated">Last updated: {{ lastUpdated | date:'medium' }}</p>
  <div class="metrics-grid">
    <div *ngFor="let metric of metrics" class="metric-card" [ngClass]="metric.trend">
      <span class="label">{{ metric.label }}</span>
      <span class="value">{{ getFormattedValue(metric) }}</span>
      <span class="trend-indicator">{{ metric.trend }}</span>
    </div>
  </div>
</div>
""")

    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'dashboard', 'dashboard.component.css'), 'w') as f:
        f.write(""".dashboard { padding: 20px; }
.metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.metric-card { padding: 16px; border-radius: 8px; background: #f5f5f5; }
.metric-card.up { border-left: 4px solid #4caf50; }
.metric-card.down { border-left: 4px solid #f44336; }
.metric-card.stable { border-left: 4px solid #ff9800; }
.label { display: block; font-size: 14px; color: #666; }
.value { display: block; font-size: 28px; font-weight: bold; margin: 8px 0; }
""")

    # --- Dashboard spec file ---
    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'dashboard', 'dashboard.component.spec.ts'), 'w') as f:
        f.write("""import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DashboardComponent } from './dashboard.component';
import { UserService } from '../services/user.service';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DashboardComponent],
      providers: [UserService]
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load metrics on init', () => {
    expect(component.metrics.length).toBe(4);
  });

  it('should format revenue with dollar sign', () => {
    const revenueMetric = component.metrics.find(m => m.label === 'Revenue');
    expect(component.getFormattedValue(revenueMetric!)).toContain('$');
  });

  it('should format bounce rate with percentage', () => {
    const bounceMetric = component.metrics.find(m => m.label === 'Bounce Rate');
    expect(component.getFormattedValue(bounceMetric!)).toContain('%');
  });
});
""")

    # --- User service ---
    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'services', 'user.service.ts'), 'w') as f:
        f.write("""import { Injectable } from '@angular/core';

export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'editor' | 'viewer';
  lastLogin: Date;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private users: User[] = [
    { id: 1, name: 'Sarah Chen', email: 'sarah.chen@company.com', role: 'admin', lastLogin: new Date('2025-03-15') },
    { id: 2, name: 'Marcus Johnson', email: 'marcus.j@company.com', role: 'editor', lastLogin: new Date('2025-03-14') },
    { id: 3, name: 'Elena Rodriguez', email: 'elena.r@company.com', role: 'viewer', lastLogin: new Date('2025-03-13') },
    { id: 4, name: 'David Kim', email: 'david.kim@company.com', role: 'editor', lastLogin: new Date('2025-03-12') },
    { id: 5, name: 'Aisha Patel', email: 'aisha.p@company.com', role: 'viewer', lastLogin: new Date('2025-03-10') },
  ];

  getUsers(): User[] {
    return this.users;
  }

  getUserById(id: number): User | undefined {
    return this.users.find(u => u.id === id);
  }

  getAdmins(): User[] {
    return this.users.filter(u => u.role === 'admin');
  }
}
""")

    # --- User service spec ---
    with open(os.path.join(PROJECT_DIR, 'src', 'app', 'services', 'user.service.spec.ts'), 'w') as f:
        f.write("""import { TestBed } from '@angular/core/testing';
import { UserService } from './user.service';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UserService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should return all users', () => {
    const users = service.getUsers();
    expect(users.length).toBe(5);
  });

  it('should find user by id', () => {
    const user = service.getUserById(1);
    expect(user).toBeDefined();
    expect(user!.name).toBe('Sarah Chen');
  });

  it('should return only admins', () => {
    const admins = service.getAdmins();
    expect(admins.length).toBe(1);
    expect(admins[0].role).toBe('admin');
  });

  it('should return undefined for non-existent user', () => {
    const user = service.getUserById(999);
    expect(user).toBeUndefined();
  });
});
""")

    # --- Stub @types/jasmine (so it looks installed) ---
    jasmine_types = """// Type definitions for Jasmine 4.3
// Project: https://jasmine.github.io/
// Definitions by: Boris Yankov <https://github.com/AJenbo>

declare function describe(description: string, specDefinitions: () => void): void;
declare function fdescribe(description: string, specDefinitions: () => void): void;
declare function xdescribe(description: string, specDefinitions: () => void): void;
declare function it(expectation: string, assertion?: () => void, timeout?: number): void;
declare function fit(expectation: string, assertion?: () => void, timeout?: number): void;
declare function xit(expectation: string, assertion?: () => void, timeout?: number): void;
declare function beforeEach(action: () => void, timeout?: number): void;
declare function afterEach(action: () => void, timeout?: number): void;
declare function beforeAll(action: () => void, timeout?: number): void;
declare function afterAll(action: () => void, timeout?: number): void;
declare function expect<T>(actual: T): jasmine.Matchers<T>;

declare namespace jasmine {
  interface Matchers<T> {
    toBe(expected: T): void;
    toEqual(expected: T): void;
    toBeTruthy(): void;
    toBeFalsy(): void;
    toBeDefined(): void;
    toBeUndefined(): void;
    toBeNull(): void;
    toContain(expected: any): void;
    toThrow(): void;
    toHaveBeenCalled(): void;
  }
}
"""
    with open(os.path.join(PROJECT_DIR, 'node_modules', '@types', 'jasmine', 'index.d.ts'), 'w') as f:
        f.write(jasmine_types)

    jasmine_package = {
        "name": "@types/jasmine",
        "version": "4.3.6",
        "description": "TypeScript definitions for Jasmine",
        "main": "",
        "types": "index.d.ts"
    }
    with open(os.path.join(PROJECT_DIR, 'node_modules', '@types', 'jasmine', 'package.json'), 'w') as f:
        json.dump(jasmine_package, f, indent=2)

    # --- Stub @types/node ---
    with open(os.path.join(PROJECT_DIR, 'node_modules', '@types', 'node', 'index.d.ts'), 'w') as f:
        f.write("// Stub @types/node\ndeclare var process: any;\n")

    with open(os.path.join(PROJECT_DIR, 'node_modules', '@types', 'node', 'package.json'), 'w') as f:
        json.dump({"name": "@types/node", "version": "18.16.19", "types": "index.d.ts"}, f, indent=2)

    # --- src/index.html ---
    with open(os.path.join(PROJECT_DIR, 'src', 'index.html'), 'w') as f:
        f.write("""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AngularProject</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root></app-root>
</body>
</html>
""")

    # --- .vscode/settings.json (workspace settings) ---
    vscode_settings = {
        "typescript.tsdk": "node_modules/typescript/lib",
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "files.exclude": {
            "**/node_modules": True,
            "**/dist": True
        }
    }
    with open(os.path.join(PROJECT_DIR, '.vscode', 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=2)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  tsconfig.json: NO references (task: add them)')
    print(f'  tsconfig.spec.json: NO types jasmine (task: add it)')

    # --- GUI-ready: Open VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
