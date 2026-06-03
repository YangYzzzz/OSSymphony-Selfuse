"""
Initial Setup: Configure TypeScript project with VSCode settings and project references
Task ID: vscode_gf2_044
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_044'
PROJECT_DIR = f'{WORKDIR}/projects/ts-compiler'


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


def create_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "ts-compiler",
        "version": "2.1.0",
        "description": "A TypeScript-based compiler toolkit for domain-specific languages",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "test": "jest",
            "lint": "eslint src/**/*.ts"
        },
        "dependencies": {
            "chalk": "^5.3.0",
            "commander": "^11.1.0",
            "source-map": "^0.7.4"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/node": "^20.10.0",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1",
            "@typescript-eslint/parser": "^6.13.0",
            "@typescript-eslint/eslint-plugin": "^6.13.0",
            "eslint": "^8.55.0"
        },
        "author": "Elena Vasquez",
        "license": "MIT"
    }
    create_file(f'{PROJECT_DIR}/package.json', json.dumps(package_json, indent=2))

    # --- tsconfig.json (basic, does NOT extend base, no composite, no references) ---
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "outDir": "./dist",
            "rootDir": "./src",
            "esModuleInterop": True,
            "skipLibCheck": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    create_file(f'{PROJECT_DIR}/tsconfig.json', json.dumps(tsconfig, indent=2))

    # --- src/types.ts ---
    create_file(f'{PROJECT_DIR}/src/types.ts', '''export interface Token {
  type: TokenType;
  value: string;
  line: number;
  column: number;
}

export enum TokenType {
  Identifier = "IDENTIFIER",
  NumberLiteral = "NUMBER_LITERAL",
  StringLiteral = "STRING_LITERAL",
  Operator = "OPERATOR",
  Keyword = "KEYWORD",
  Punctuation = "PUNCTUATION",
  Whitespace = "WHITESPACE",
  EOF = "EOF",
}

export interface ASTNode {
  kind: string;
  children: ASTNode[];
  token?: Token;
  metadata?: Record<string, unknown>;
}

export interface CompilerOptions {
  sourceMap: boolean;
  optimize: boolean;
  targetVersion: string;
  outputFormat: "js" | "wasm" | "ir";
  maxErrors: number;
  verbose: boolean;
}

export interface CompilationResult {
  success: boolean;
  output: string;
  errors: CompilerError[];
  warnings: CompilerWarning[];
  stats: CompilationStats;
}

export interface CompilerError {
  message: string;
  line: number;
  column: number;
  severity: "error" | "fatal";
}

export interface CompilerWarning {
  message: string;
  line: number;
  column: number;
  code: string;
}

export interface CompilationStats {
  tokenCount: number;
  nodeCount: number;
  parseTimeMs: number;
  codegenTimeMs: number;
  totalTimeMs: number;
}
''')

    # --- src/lexer.ts ---
    create_file(f'{PROJECT_DIR}/src/lexer.ts', '''import { Token, TokenType } from "./types";

const KEYWORDS = new Set([
  "let", "const", "var", "function", "return", "if", "else",
  "while", "for", "class", "import", "export", "from", "type",
  "interface", "enum", "switch", "case", "break", "continue",
  "try", "catch", "finally", "throw", "new", "this", "super",
]);

const OPERATORS = new Set([
  "+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==",
  "<", ">", "<=", ">=", "&&", "||", "!", "&", "|", "^",
  "~", "<<", ">>", ">>>", "+=", "-=", "*=", "/=", "=>",
]);

export class Lexer {
  private source: string;
  private position: number = 0;
  private line: number = 1;
  private column: number = 1;

  constructor(source: string) {
    this.source = source;
  }

  tokenize(): Token[] {
    const tokens: Token[] = [];

    while (this.position < this.source.length) {
      const char = this.source[this.position];

      if (this.isWhitespace(char)) {
        this.skipWhitespace();
        continue;
      }

      if (char === "/" && this.peek() === "/") {
        this.skipLineComment();
        continue;
      }

      if (char === "/" && this.peek() === "*") {
        this.skipBlockComment();
        continue;
      }

      if (this.isDigit(char)) {
        tokens.push(this.readNumber());
        continue;
      }

      if (char === \'"\' || char === "\'") {
        tokens.push(this.readString(char));
        continue;
      }

      if (this.isIdentStart(char)) {
        tokens.push(this.readIdentifier());
        continue;
      }

      if (this.isOperatorChar(char)) {
        tokens.push(this.readOperator());
        continue;
      }

      tokens.push(this.createToken(TokenType.Punctuation, char));
      this.advance();
    }

    tokens.push(this.createToken(TokenType.EOF, ""));
    return tokens;
  }

  private createToken(type: TokenType, value: string): Token {
    return { type, value, line: this.line, column: this.column };
  }

  private advance(): string {
    const char = this.source[this.position];
    this.position++;
    if (char === "\\n") {
      this.line++;
      this.column = 1;
    } else {
      this.column++;
    }
    return char;
  }

  private peek(): string {
    return this.position + 1 < this.source.length
      ? this.source[this.position + 1]
      : "";
  }

  private isWhitespace(char: string): boolean {
    return /\\s/.test(char);
  }

  private isDigit(char: string): boolean {
    return /[0-9]/.test(char);
  }

  private isIdentStart(char: string): boolean {
    return /[a-zA-Z_$]/.test(char);
  }

  private isOperatorChar(char: string): boolean {
    return "+-*/%=<>!&|^~".includes(char);
  }

  private skipWhitespace(): void {
    while (this.position < this.source.length && this.isWhitespace(this.source[this.position])) {
      this.advance();
    }
  }

  private skipLineComment(): void {
    while (this.position < this.source.length && this.source[this.position] !== "\\n") {
      this.advance();
    }
  }

  private skipBlockComment(): void {
    this.advance(); // skip /
    this.advance(); // skip *
    while (this.position < this.source.length - 1) {
      if (this.source[this.position] === "*" && this.source[this.position + 1] === "/") {
        this.advance();
        this.advance();
        return;
      }
      this.advance();
    }
  }

  private readNumber(): Token {
    const start = this.position;
    const startCol = this.column;
    while (this.position < this.source.length && (this.isDigit(this.source[this.position]) || this.source[this.position] === ".")) {
      this.advance();
    }
    return { type: TokenType.NumberLiteral, value: this.source.slice(start, this.position), line: this.line, column: startCol };
  }

  private readString(quote: string): Token {
    const startCol = this.column;
    this.advance(); // skip opening quote
    let value = "";
    while (this.position < this.source.length && this.source[this.position] !== quote) {
      if (this.source[this.position] === "\\\\") {
        this.advance();
      }
      value += this.advance();
    }
    this.advance(); // skip closing quote
    return { type: TokenType.StringLiteral, value, line: this.line, column: startCol };
  }

  private readIdentifier(): Token {
    const start = this.position;
    const startCol = this.column;
    while (this.position < this.source.length && /[a-zA-Z0-9_$]/.test(this.source[this.position])) {
      this.advance();
    }
    const value = this.source.slice(start, this.position);
    const type = KEYWORDS.has(value) ? TokenType.Keyword : TokenType.Identifier;
    return { type, value, line: this.line, column: startCol };
  }

  private readOperator(): Token {
    const startCol = this.column;
    let op = this.advance();
    while (this.position < this.source.length && OPERATORS.has(op + this.source[this.position])) {
      op += this.advance();
    }
    return { type: TokenType.Operator, value: op, line: this.line, column: startCol };
  }
}
''')

    # --- src/parser.ts ---
    create_file(f'{PROJECT_DIR}/src/parser.ts', '''import { Token, TokenType, ASTNode } from "./types";

export class Parser {
  private tokens: Token[];
  private current: number = 0;

  constructor(tokens: Token[]) {
    this.tokens = tokens;
  }

  parse(): ASTNode {
    const program: ASTNode = {
      kind: "Program",
      children: [],
    };

    while (!this.isAtEnd()) {
      const stmt = this.parseStatement();
      if (stmt) {
        program.children.push(stmt);
      }
    }

    return program;
  }

  private parseStatement(): ASTNode | null {
    const token = this.peek();

    if (token.type === TokenType.Keyword) {
      switch (token.value) {
        case "let":
        case "const":
        case "var":
          return this.parseVariableDeclaration();
        case "function":
          return this.parseFunctionDeclaration();
        case "return":
          return this.parseReturnStatement();
        case "if":
          return this.parseIfStatement();
        case "while":
          return this.parseWhileStatement();
      }
    }

    return this.parseExpressionStatement();
  }

  private parseVariableDeclaration(): ASTNode {
    const keyword = this.advance();
    const name = this.expect(TokenType.Identifier);
    this.expectValue("=");
    const initializer = this.parseExpression();
    this.consumeOptional(";");

    return {
      kind: "VariableDeclaration",
      children: [initializer],
      token: name,
      metadata: { declarationType: keyword.value },
    };
  }

  private parseFunctionDeclaration(): ASTNode {
    this.advance(); // consume 'function'
    const name = this.expect(TokenType.Identifier);
    this.expectValue("(");
    const params = this.parseParameterList();
    this.expectValue(")");
    const body = this.parseBlock();

    return {
      kind: "FunctionDeclaration",
      children: [...params, body],
      token: name,
    };
  }

  private parseReturnStatement(): ASTNode {
    const token = this.advance();
    const value = this.isAtEnd() || this.peek().value === "}"
      ? null
      : this.parseExpression();
    this.consumeOptional(";");

    return {
      kind: "ReturnStatement",
      children: value ? [value] : [],
      token,
    };
  }

  private parseIfStatement(): ASTNode {
    const token = this.advance(); // consume 'if'
    this.expectValue("(");
    const condition = this.parseExpression();
    this.expectValue(")");
    const consequent = this.parseBlock();
    const children = [condition, consequent];

    if (!this.isAtEnd() && this.peek().value === "else") {
      this.advance();
      children.push(this.parseBlock());
    }

    return { kind: "IfStatement", children, token };
  }

  private parseWhileStatement(): ASTNode {
    const token = this.advance();
    this.expectValue("(");
    const condition = this.parseExpression();
    this.expectValue(")");
    const body = this.parseBlock();

    return { kind: "WhileStatement", children: [condition, body], token };
  }

  private parseExpressionStatement(): ASTNode {
    const expr = this.parseExpression();
    this.consumeOptional(";");
    return { kind: "ExpressionStatement", children: [expr] };
  }

  private parseExpression(): ASTNode {
    return this.parseBinaryExpression();
  }

  private parseBinaryExpression(): ASTNode {
    let left = this.parsePrimary();

    while (!this.isAtEnd() && this.peek().type === TokenType.Operator) {
      const op = this.advance();
      const right = this.parsePrimary();
      left = {
        kind: "BinaryExpression",
        children: [left, right],
        token: op,
      };
    }

    return left;
  }

  private parsePrimary(): ASTNode {
    const token = this.advance();
    return { kind: "Literal", children: [], token };
  }

  private parseParameterList(): ASTNode[] {
    const params: ASTNode[] = [];
    while (!this.isAtEnd() && this.peek().value !== ")") {
      if (params.length > 0) this.expectValue(",");
      const name = this.expect(TokenType.Identifier);
      params.push({ kind: "Parameter", children: [], token: name });
    }
    return params;
  }

  private parseBlock(): ASTNode {
    this.expectValue("{");
    const statements: ASTNode[] = [];
    while (!this.isAtEnd() && this.peek().value !== "}") {
      const stmt = this.parseStatement();
      if (stmt) statements.push(stmt);
    }
    this.expectValue("}");
    return { kind: "Block", children: statements };
  }

  private peek(): Token {
    return this.tokens[this.current];
  }

  private advance(): Token {
    return this.tokens[this.current++];
  }

  private isAtEnd(): boolean {
    return this.current >= this.tokens.length || this.tokens[this.current].type === TokenType.EOF;
  }

  private expect(type: TokenType): Token {
    const token = this.advance();
    if (token.type !== type) {
      throw new Error(`Expected ${type} but got ${token.type} ("${token.value}") at line ${token.line}:${token.column}`);
    }
    return token;
  }

  private expectValue(value: string): void {
    const token = this.advance();
    if (token.value !== value) {
      throw new Error(`Expected "${value}" but got "${token.value}" at line ${token.line}:${token.column}`);
    }
  }

  private consumeOptional(value: string): void {
    if (!this.isAtEnd() && this.peek().value === value) {
      this.advance();
    }
  }
}
''')

    # --- src/utils/helpers.ts ---
    create_file(f'{PROJECT_DIR}/src/utils/helpers.ts', '''import { CompilerError, CompilerWarning, CompilationStats } from "../types";

export function formatError(error: CompilerError): string {
  const prefix = error.severity === "fatal" ? "FATAL" : "ERROR";
  return `[${prefix}] Line ${error.line}:${error.column} - ${error.message}`;
}

export function formatWarning(warning: CompilerWarning): string {
  return `[WARN ${warning.code}] Line ${warning.line}:${warning.column} - ${warning.message}`;
}

export function formatStats(stats: CompilationStats): string {
  const lines = [
    `Compilation Statistics:`,
    `  Tokens processed: ${stats.tokenCount}`,
    `  AST nodes: ${stats.nodeCount}`,
    `  Parse time: ${stats.parseTimeMs.toFixed(2)}ms`,
    `  Code generation: ${stats.codegenTimeMs.toFixed(2)}ms`,
    `  Total time: ${stats.totalTimeMs.toFixed(2)}ms`,
  ];
  return lines.join("\\n");
}

export function generateSourceMap(
  originalSource: string,
  generatedSource: string,
  mappings: Array<{ originalLine: number; generatedLine: number }>
): string {
  const sourceMap = {
    version: 3,
    sources: ["input.dsl"],
    names: [],
    mappings: mappings
      .map((m) => `${m.generatedLine}:0->${m.originalLine}:0`)
      .join(";"),
  };
  return JSON.stringify(sourceMap);
}

export function measureTime<T>(fn: () => T): [T, number] {
  const start = performance.now();
  const result = fn();
  const elapsed = performance.now() - start;
  return [result, elapsed];
}
''')

    # --- src/index.ts ---
    create_file(f'{PROJECT_DIR}/src/index.ts', '''import { Lexer } from "./lexer";
import { Parser } from "./parser";
import { CompilerOptions, CompilationResult } from "./types";
import { formatError, formatWarning, formatStats, measureTime } from "./utils/helpers";

const DEFAULT_OPTIONS: CompilerOptions = {
  sourceMap: false,
  optimize: false,
  targetVersion: "es2020",
  outputFormat: "js",
  maxErrors: 100,
  verbose: false,
};

export function compile(
  source: string,
  options: Partial<CompilerOptions> = {}
): CompilationResult {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  const errors: import("./types").CompilerError[] = [];
  const warnings: import("./types").CompilerWarning[] = [];

  // Phase 1: Lexical Analysis
  const [tokens, lexTime] = measureTime(() => {
    const lexer = new Lexer(source);
    return lexer.tokenize();
  });

  if (opts.verbose) {
    console.log(`Lexer produced ${tokens.length} tokens in ${lexTime.toFixed(2)}ms`);
  }

  // Phase 2: Parsing
  const [ast, parseTime] = measureTime(() => {
    const parser = new Parser(tokens);
    return parser.parse();
  });

  if (opts.verbose) {
    console.log(`Parser produced AST with ${countNodes(ast)} nodes in ${parseTime.toFixed(2)}ms`);
  }

  // Phase 3: Code Generation (placeholder)
  const [output, codegenTime] = measureTime(() => {
    return generateCode(ast, opts);
  });

  const stats = {
    tokenCount: tokens.length,
    nodeCount: countNodes(ast),
    parseTimeMs: lexTime,
    codegenTimeMs: codegenTime,
    totalTimeMs: lexTime + parseTime + codegenTime,
  };

  if (opts.verbose) {
    console.log(formatStats(stats));
    errors.forEach((e) => console.error(formatError(e)));
    warnings.forEach((w) => console.warn(formatWarning(w)));
  }

  return {
    success: errors.length === 0,
    output,
    errors,
    warnings,
    stats,
  };
}

function countNodes(node: import("./types").ASTNode): number {
  return 1 + node.children.reduce((sum, child) => sum + countNodes(child), 0);
}

function generateCode(
  ast: import("./types").ASTNode,
  options: CompilerOptions
): string {
  // Simplified code generation
  const lines: string[] = [];
  lines.push("// Generated by ts-compiler v2.1.0");
  lines.push(`// Target: ${options.targetVersion}`);
  lines.push("");

  for (const child of ast.children) {
    lines.push(nodeToCode(child));
  }

  return lines.join("\\n");
}

function nodeToCode(node: import("./types").ASTNode): string {
  switch (node.kind) {
    case "VariableDeclaration":
      return `${node.metadata?.declarationType} ${node.token?.value} = ${nodeToCode(node.children[0])};`;
    case "FunctionDeclaration":
      return `function ${node.token?.value}() { /* ... */ }`;
    case "ReturnStatement":
      return `return ${node.children.map(nodeToCode).join("")};`;
    case "Literal":
      return node.token?.value ?? "";
    case "BinaryExpression":
      return `${nodeToCode(node.children[0])} ${node.token?.value} ${nodeToCode(node.children[1])}`;
    default:
      return `/* ${node.kind} */`;
  }
}

// CLI entry point
if (require.main === module) {
  const sampleSource = `
    const message = "Hello, World!";
    function greet(name) {
      return message + " " + name;
    }
  `;

  const result = compile(sampleSource, { verbose: true });
  console.log("\\nCompilation", result.success ? "succeeded" : "failed");
  console.log("Output:\\n", result.output);
}
''')

    # --- .gitignore ---
    create_file(f'{PROJECT_DIR}/.gitignore', '''node_modules/
dist/
*.js.map
.DS_Store
coverage/
''')

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
