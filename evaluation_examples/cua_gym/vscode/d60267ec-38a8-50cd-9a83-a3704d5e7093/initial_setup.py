"""
Initial Setup: Create a VSCode extension project without CI configuration
Task ID: vscode_gf3_017
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_017'
PROJECT_DIR = f'{WORKDIR}/projects/extension-project'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/test', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # NOTE: .github/workflows directory must NOT exist - the task asks to create it

    # package.json - realistic VSCode extension manifest
    package_json = {
        "name": "smart-snippet-manager",
        "displayName": "Smart Snippet Manager",
        "description": "An intelligent code snippet manager for VSCode with context-aware suggestions",
        "version": "0.2.1",
        "publisher": "devtools-collective",
        "engines": {
            "vscode": "^1.85.0"
        },
        "categories": ["Snippets", "Other"],
        "activationEvents": [
            "onCommand:smartSnippets.insertSnippet",
            "onCommand:smartSnippets.saveSnippet",
            "onCommand:smartSnippets.searchSnippets"
        ],
        "main": "./out/extension.js",
        "scripts": {
            "vscode:prepublish": "npm run compile",
            "compile": "tsc -p ./",
            "watch": "tsc -watch -p ./",
            "pretest": "npm run compile",
            "test": "node ./out/test/runTest.js",
            "lint": "eslint src --ext ts"
        },
        "devDependencies": {
            "@types/vscode": "^1.85.0",
            "@types/mocha": "^10.0.6",
            "@types/node": "18.x",
            "@typescript-eslint/eslint-plugin": "^6.15.0",
            "@typescript-eslint/parser": "^6.15.0",
            "@vscode/test-electron": "^2.3.8",
            "eslint": "^8.56.0",
            "glob": "^10.3.10",
            "mocha": "^10.2.0",
            "typescript": "^5.3.3"
        },
        "dependencies": {
            "fuse.js": "^7.0.0"
        },
        "repository": {
            "type": "git",
            "url": "https://github.com/devtools-collective/smart-snippet-manager.git"
        },
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "module": "commonjs",
            "target": "ES2020",
            "outDir": "out",
            "lib": ["ES2020"],
            "sourceMap": True,
            "rootDir": "src",
            "strict": True,
            "noImplicitReturns": True,
            "noFallthroughCasesInSwitch": True,
            "noUnusedParameters": True
        },
        "exclude": ["node_modules", ".vscode-test"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # .vscode/launch.json
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Run Extension",
                "type": "extensionHost",
                "request": "launch",
                "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
                "outFiles": ["${workspaceFolder}/out/**/*.js"],
                "preLaunchTask": "${defaultBuildTask}"
            },
            {
                "name": "Extension Tests",
                "type": "extensionHost",
                "request": "launch",
                "args": [
                    "--extensionDevelopmentPath=${workspaceFolder}",
                    "--extensionTestsPath=${workspaceFolder}/out/test/suite/index"
                ],
                "outFiles": ["${workspaceFolder}/out/**/*.js"],
                "preLaunchTask": "${defaultBuildTask}"
            }
        ]
    }
    with open(f'{PROJECT_DIR}/.vscode/launch.json', 'w') as f:
        json.dump(launch_json, f, indent=2)

    # src/extension.ts - main extension file
    extension_ts = '''import * as vscode from 'vscode';
import { SnippetStorage } from './snippetStorage';
import { SnippetProvider } from './snippetProvider';

let snippetStorage: SnippetStorage;

export function activate(context: vscode.ExtensionContext) {
    console.log('Smart Snippet Manager is now active');

    snippetStorage = new SnippetStorage(context.globalStorageUri);

    const provider = new SnippetProvider(snippetStorage);
    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider('*', provider)
    );

    const insertCmd = vscode.commands.registerCommand(
        'smartSnippets.insertSnippet',
        async () => {
            const snippets = await snippetStorage.getAll();
            const items = snippets.map(s => ({
                label: s.name,
                description: s.language,
                detail: s.description,
                snippet: s,
            }));

            const selected = await vscode.window.showQuickPick(items, {
                placeHolder: 'Select a snippet to insert',
                matchOnDescription: true,
            });

            if (selected && vscode.window.activeTextEditor) {
                const editor = vscode.window.activeTextEditor;
                editor.insertSnippet(
                    new vscode.SnippetString(selected.snippet.body)
                );
            }
        }
    );

    const saveCmd = vscode.commands.registerCommand(
        'smartSnippets.saveSnippet',
        async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor');
                return;
            }

            const selection = editor.document.getText(editor.selection);
            if (!selection) {
                vscode.window.showWarningMessage('No text selected');
                return;
            }

            const name = await vscode.window.showInputBox({
                prompt: 'Snippet name',
                placeHolder: 'e.g., React Component Template',
            });
            if (!name) { return; }

            const description = await vscode.window.showInputBox({
                prompt: 'Snippet description (optional)',
            });

            await snippetStorage.save({
                name,
                body: selection,
                language: editor.document.languageId,
                description: description || '',
                createdAt: new Date().toISOString(),
            });

            vscode.window.showInformationMessage(
                `Snippet "${name}" saved successfully`
            );
        }
    );

    const searchCmd = vscode.commands.registerCommand(
        'smartSnippets.searchSnippets',
        async () => {
            const query = await vscode.window.showInputBox({
                prompt: 'Search snippets',
                placeHolder: 'Type to search...',
            });
            if (!query) { return; }

            const results = await snippetStorage.search(query);
            if (results.length === 0) {
                vscode.window.showInformationMessage('No snippets found');
                return;
            }

            const items = results.map(s => ({
                label: s.name,
                description: s.language,
                detail: s.description,
            }));
            await vscode.window.showQuickPick(items);
        }
    );

    context.subscriptions.push(insertCmd, saveCmd, searchCmd);
}

export function deactivate() {
    // Clean up resources
}
'''
    with open(f'{PROJECT_DIR}/src/extension.ts', 'w') as f:
        f.write(extension_ts)

    # src/snippetStorage.ts
    snippet_storage_ts = '''import * as vscode from 'vscode';
import Fuse from 'fuse.js';

export interface Snippet {
    name: string;
    body: string;
    language: string;
    description: string;
    createdAt: string;
}

export class SnippetStorage {
    private storageUri: vscode.Uri;
    private snippets: Snippet[] = [];
    private fuse: Fuse<Snippet>;

    constructor(storageUri: vscode.Uri) {
        this.storageUri = storageUri;
        this.fuse = new Fuse(this.snippets, {
            keys: ['name', 'description', 'language'],
            threshold: 0.4,
        });
    }

    async getAll(): Promise<Snippet[]> {
        await this.load();
        return [...this.snippets];
    }

    async save(snippet: Snippet): Promise<void> {
        await this.load();
        this.snippets.push(snippet);
        await this.persist();
    }

    async search(query: string): Promise<Snippet[]> {
        await this.load();
        this.fuse.setCollection(this.snippets);
        return this.fuse.search(query).map(r => r.item);
    }

    async delete(name: string): Promise<boolean> {
        await this.load();
        const idx = this.snippets.findIndex(s => s.name === name);
        if (idx === -1) { return false; }
        this.snippets.splice(idx, 1);
        await this.persist();
        return true;
    }

    private async load(): Promise<void> {
        try {
            const fileUri = vscode.Uri.joinPath(this.storageUri, 'snippets.json');
            const data = await vscode.workspace.fs.readFile(fileUri);
            this.snippets = JSON.parse(Buffer.from(data).toString('utf-8'));
        } catch {
            this.snippets = [];
        }
    }

    private async persist(): Promise<void> {
        await vscode.workspace.fs.createDirectory(this.storageUri);
        const fileUri = vscode.Uri.joinPath(this.storageUri, 'snippets.json');
        const data = Buffer.from(JSON.stringify(this.snippets, null, 2), 'utf-8');
        await vscode.workspace.fs.writeFile(fileUri, data);
    }
}
'''
    with open(f'{PROJECT_DIR}/src/snippetStorage.ts', 'w') as f:
        f.write(snippet_storage_ts)

    # src/snippetProvider.ts
    snippet_provider_ts = '''import * as vscode from 'vscode';
import { SnippetStorage } from './snippetStorage';

export class SnippetProvider implements vscode.CompletionItemProvider {
    constructor(private storage: SnippetStorage) {}

    async provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position
    ): Promise<vscode.CompletionItem[]> {
        const snippets = await this.storage.getAll();
        const languageId = document.languageId;

        return snippets
            .filter(s => s.language === languageId || s.language === '*')
            .map(s => {
                const item = new vscode.CompletionItem(
                    s.name,
                    vscode.CompletionItemKind.Snippet
                );
                item.insertText = new vscode.SnippetString(s.body);
                item.detail = `[Smart Snippet] ${s.description}`;
                item.documentation = new vscode.MarkdownString(
                    `**${s.name}**\\n\\n\`\`\`\\n${s.body}\\n\`\`\``
                );
                return item;
            });
    }
}
'''
    with open(f'{PROJECT_DIR}/src/snippetProvider.ts', 'w') as f:
        f.write(snippet_provider_ts)

    # test/suite/index.ts
    os.makedirs(f'{PROJECT_DIR}/test/suite', exist_ok=True)
    test_index_ts = '''import * as path from 'path';
import * as Mocha from 'mocha';
import * as glob from 'glob';

export function run(): Promise<void> {
    const mocha = new Mocha({
        ui: 'tdd',
        color: true,
        timeout: 10000,
    });

    const testsRoot = path.resolve(__dirname, '..');

    return new Promise((resolve, reject) => {
        glob.glob('**/**.test.js', { cwd: testsRoot }).then(files => {
            files.forEach(f => mocha.addFile(path.resolve(testsRoot, f)));
            try {
                mocha.run(failures => {
                    if (failures > 0) {
                        reject(new Error(`${failures} tests failed.`));
                    } else {
                        resolve();
                    }
                });
            } catch (err) {
                reject(err);
            }
        });
    });
}
'''
    with open(f'{PROJECT_DIR}/test/suite/index.ts', 'w') as f:
        f.write(test_index_ts)

    # test/suite/extension.test.ts
    test_extension_ts = '''import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Extension should be present', () => {
        assert.ok(
            vscode.extensions.getExtension('devtools-collective.smart-snippet-manager')
        );
    });

    test('Should register all commands', async () => {
        const commands = await vscode.commands.getCommands(true);
        assert.ok(commands.includes('smartSnippets.insertSnippet'));
        assert.ok(commands.includes('smartSnippets.saveSnippet'));
        assert.ok(commands.includes('smartSnippets.searchSnippets'));
    });
});
'''
    with open(f'{PROJECT_DIR}/test/suite/extension.test.ts', 'w') as f:
        f.write(test_extension_ts)

    # test/runTest.ts
    run_test_ts = '''import * as path from 'path';
import { runTests } from '@vscode/test-electron';

async function main() {
    try {
        const extensionDevelopmentPath = path.resolve(__dirname, '../../');
        const extensionTestsPath = path.resolve(__dirname, './suite/index');
        await runTests({ extensionDevelopmentPath, extensionTestsPath });
    } catch (err) {
        console.error('Failed to run tests');
        process.exit(1);
    }
}

main();
'''
    with open(f'{PROJECT_DIR}/test/runTest.ts', 'w') as f:
        f.write(run_test_ts)

    # .eslintrc.json
    eslintrc = {
        "root": True,
        "parser": "@typescript-eslint/parser",
        "parserOptions": {
            "ecmaVersion": 2020,
            "sourceType": "module"
        },
        "plugins": ["@typescript-eslint"],
        "rules": {
            "@typescript-eslint/naming-convention": "warn",
            "curly": "warn",
            "eqeqeq": "warn",
            "no-throw-literal": "warn",
            "semi": "off"
        }
    }
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # .gitignore
    gitignore_content = """out
dist
node_modules
.vscode-test/
*.vsix
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore_content)

    # README.md
    readme = """# Smart Snippet Manager

An intelligent code snippet manager for Visual Studio Code with context-aware suggestions.

## Features

- **Save Snippets**: Select code and save it as a reusable snippet
- **Insert Snippets**: Quick-pick menu to insert saved snippets
- **Fuzzy Search**: Find snippets by name, description, or language
- **Auto-Complete**: Snippets appear in IntelliSense suggestions

## Usage

1. **Save a snippet**: Select code, run `Smart Snippets: Save Snippet`
2. **Insert a snippet**: Run `Smart Snippets: Insert Snippet`
3. **Search snippets**: Run `Smart Snippets: Search Snippets`

## Development

```bash
npm ci
npm run compile
npm test
```

## License

MIT
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # CHANGELOG.md
    changelog = """# Changelog

## [0.2.1] - 2025-03-20

### Fixed
- Fixed fuzzy search threshold for better matching accuracy
- Resolved issue with snippet persistence across sessions

## [0.2.0] - 2025-02-15

### Added
- Fuzzy search capability using Fuse.js
- Language-specific snippet filtering in auto-complete
- Delete snippet command

### Changed
- Improved snippet storage format for faster loading

## [0.1.0] - 2025-01-10

### Added
- Initial release
- Save, insert, and search snippet commands
- Basic completion provider
"""
    with open(f'{PROJECT_DIR}/CHANGELOG.md', 'w') as f:
        f.write(changelog)

    print(f'Extension project created at: {PROJECT_DIR}')
    print(f'Files created:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        for fname in files:
            fpath = os.path.join(root, fname)
            print(f'  {fpath}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
