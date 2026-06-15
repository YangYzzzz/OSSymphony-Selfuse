"""
Initial Setup: Python interpreter project scaffold
Task ID: vscode_gf4_089
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_089'
PROJECT = f'{WORKDIR}/projects/python-interpreter'

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
    os.makedirs(f'{PROJECT}/src', exist_ok=True)
    os.makedirs(f'{PROJECT}/fixtures', exist_ok=True)

    # src/__init__.py (empty, as specified)
    with open(f'{PROJECT}/src/__init__.py', 'w') as f:
        f.write('')

    # fixtures/hello.lang - basic variable and print demo
    with open(f'{PROJECT}/fixtures/hello.lang', 'w') as f:
        f.write("""\
# Simple hello world program
let greeting = "Hello, World!"
print(greeting)

let x = 42
let y = 18
let sum = x + y
print(sum)

# String concatenation
let name = "Alice"
let message = "Welcome, " + name
print(message)
""")

    # fixtures/math.lang - arithmetic and comparison operators
    with open(f'{PROJECT}/fixtures/math.lang', 'w') as f:
        f.write("""\
# Arithmetic operations
let a = 100
let b = 37
let total = a + b
let diff = a - b
let product = a * b
let quotient = a / b

print(total)
print(diff)
print(product)
print(quotient)

# Comparison operators
if a > b
    print("a is greater")
else
    print("b is greater or equal")

let counter = 0
while counter < 5
    print(counter)
    let counter = counter + 1
""")

    # fixtures/functions.lang - function declarations and closures
    with open(f'{PROJECT}/fixtures/functions.lang', 'w') as f:
        f.write("""\
# Function declarations
func add(x, y)
    return x + y

func factorial(n)
    if n <= 1
        return 1
    return n * factorial(n - 1)

let result = add(10, 20)
print(result)

let fact5 = factorial(5)
print(fact5)

# Closures
func make_counter()
    let count = 0
    func increment()
        let count = count + 1
        return count
    return increment

let counter = make_counter()
print(counter())
print(counter())
print(counter())

# Built-in functions
let items = "hello"
print(len(items))
print(type(items))
print(type(42))
""")

    print(f'Initial project created: {PROJECT}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
