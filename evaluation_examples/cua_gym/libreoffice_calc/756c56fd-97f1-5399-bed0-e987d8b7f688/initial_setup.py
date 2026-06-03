"""
Initial Setup: RPG combat system with three bugs, no logging
Task ID: osworld_multi_apps_code_python_game_010
Domain: os (Python code files)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_python_game_010'
RPG_DIR = f'{WORKDIR}/projects/rpg'


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
    # Create the project directory structure
    os.makedirs(RPG_DIR, exist_ok=True)

    # --- main.py ---
    main_py = '''\
"""
RPG Combat System - Main Entry Point
"""
from character import Character
from enemy import Enemy
from combat import run_combat


def main():
    hero = Character(name="Aria", hp=100, max_hp=100, attack=15, defense=5)
    goblin = Enemy(name="Goblin", hp=40, damage=8)

    print(f"Starting combat: {hero.name} vs {goblin.name}")
    result = run_combat(hero, goblin)
    print(f"Combat result: {result}")


if __name__ == "__main__":
    main()
'''

    # --- character.py (BUG 1: heal() can exceed max_hp) ---
    character_py = '''\
"""
Character class for the RPG combat system.
"""


class Character:
    def __init__(self, name: str, hp: int, max_hp: int, attack: int, defense: int):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int):
        """Reduce hp by amount (min 0)."""
        damage = max(0, amount - self.defense)
        self.hp = max(0, self.hp - damage)

    def heal(self, amount: int):
        """Restore hp by amount.
        BUG: No cap at max_hp — can exceed maximum health.
        """
        self.hp += amount  # BUG: should be min(self.hp + amount, self.max_hp)

    def __repr__(self):
        return f"Character({self.name}, hp={self.hp}/{self.max_hp})"
'''

    # --- enemy.py (BUG 2: attack() ignores self.damage, always deals 10) ---
    enemy_py = '''\
"""
Enemy class for the RPG combat system.
"""


class Enemy:
    def __init__(self, name: str, hp: int, damage: int):
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int):
        """Reduce hp by amount (min 0)."""
        self.hp = max(0, self.hp - amount)

    def attack(self, target) -> int:
        """Deal damage to target.
        BUG: Always deals 10 damage ignoring self.damage attribute.
        """
        damage_dealt = 10  # BUG: should be self.damage
        target.take_damage(damage_dealt)
        return damage_dealt

    def __repr__(self):
        return f"Enemy({self.name}, hp={self.hp}, damage={self.damage})"
'''

    # --- combat.py (BUG 3: checks enemy.health but attribute is enemy.hp) ---
    combat_py = '''\
"""
Combat system for the RPG game.
"""


def run_combat(character, enemy) -> str:
    """Run a combat loop between character and enemy.
    Returns "victory" or "defeat".

    BUG: Uses enemy.health instead of enemy.hp to check if enemy is alive.
    Also missing log_combat() function for logging combat actions.
    """
    round_num = 1
    while character.is_alive() and enemy.health > 0:  # BUG: enemy.health should be enemy.hp
        # Character attacks enemy
        dmg = character.attack
        enemy.take_damage(dmg)
        print(f"Round {round_num}: {character.name} deals {dmg} to {enemy.name} (hp={enemy.hp})")

        # Enemy attacks character
        if enemy.health > 0:  # BUG: same bug here
            e_dmg = enemy.attack(character)
            print(f"Round {round_num}: {enemy.name} deals {e_dmg} to {character.name} (hp={character.hp})")

        round_num += 1
        if round_num > 50:
            return "draw"

    if character.is_alive():
        return "victory"
    return "defeat"
'''

    # Write all files
    with open(os.path.join(RPG_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    with open(os.path.join(RPG_DIR, 'character.py'), 'w') as f:
        f.write(character_py)

    with open(os.path.join(RPG_DIR, 'enemy.py'), 'w') as f:
        f.write(enemy_py)

    with open(os.path.join(RPG_DIR, 'combat.py'), 'w') as f:
        f.write(combat_py)

    print(f'RPG project directory created: {RPG_DIR}')
    print('Files created: main.py, character.py, enemy.py, combat.py')
    print('Bugs present:')
    print('  1. character.py heal() has no max_hp cap')
    print('  2. enemy.py attack() always deals 10 damage ignoring self.damage')
    print('  3. combat.py uses enemy.health instead of enemy.hp')

    # GUI-ready startup: open VS Code with the rpg project directory
    launch_gui(f'code "{RPG_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VS Code with DISPLAY=:0')


create_initial()
