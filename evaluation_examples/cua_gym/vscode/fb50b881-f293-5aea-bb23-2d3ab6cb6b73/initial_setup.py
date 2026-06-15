"""
Initial Setup: Fold code to level 2 in VSCode
Task ID: vscode_code_025
Domain: vs_code

Creates /home/user/project/app.js with a JavaScript class containing
nested blocks (class -> methods -> if/try-catch), then opens it in VSCode.
The agent must use Ctrl+K Ctrl+2 to fold to level 2.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_025'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/app.js'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # JavaScript file content — UserService class with nested blocks
    # (class block -> method blocks -> if/try-catch inner blocks)
    # This is the pre-task state: all code is unfolded/visible
    app_js_content = """\
class UserService {
  constructor(db) {
    this.db = db;
    this.cache = new Map();
  }

  async getUser(id) {
    if (this.cache.has(id)) {
      return this.cache.get(id);
    }
    const user = await this.db.findById(id);
    if (user) {
      this.cache.set(id, user);
    }
    return user;
  }

  async deleteUser(id) {
    try {
      await this.db.delete(id);
      this.cache.delete(id);
    } catch (error) {
      console.error('Failed to delete user:', error);
      throw error;
    }
  }
}
"""

    with open(OUTPUT, 'w') as f:
        f.write(app_js_content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the project folder and the target file
    # Use 'code' to open the file directly so it's active in the editor
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: launched VSCode with project and app.js open (DISPLAY=:0)')


create_initial()
