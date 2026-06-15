"""
Initial Setup: VSCode C++ development environment setup
Task ID: osworld_multi_apps_code_vscode_config_007
Domain: vs-code / multi-apps

Creates:
  - /home/user/projects/cpp_game/main.cpp  (simple C++ game loop, no bugs)

Does NOT create:
  - .vscode/ directory or any JSON config files (task agent must create these)
  - game binary (task agent must build this)
  - C/C++ extension is NOT installed (task agent must install)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/projects/cpp_game'
MAIN_CPP = f'{PROJECT_DIR}/main.cpp'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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

    # Remove .vscode directory if it somehow exists (ensure clean initial state)
    if os.path.exists(VSCODE_DIR):
        import shutil
        shutil.rmtree(VSCODE_DIR)

    # Remove game binary if it somehow exists
    game_binary = f'{PROJECT_DIR}/game'
    if os.path.exists(game_binary):
        os.remove(game_binary)

    # Create a realistic main.cpp with a simple game loop (no bugs)
    main_cpp_content = '''#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>

// Simple text-based adventure game
struct Player {
    std::string name;
    int health;
    int score;
    int level;

    Player(const std::string& n) : name(n), health(100), score(0), level(1) {}
};

void displayStatus(const Player& player) {
    std::cout << "\\n=== " << player.name << " ===" << std::endl;
    std::cout << "Health: " << player.health << "/100" << std::endl;
    std::cout << "Score:  " << player.score << std::endl;
    std::cout << "Level:  " << player.level << std::endl;
}

int rollDice(int sides) {
    return (std::rand() % sides) + 1;
}

bool encounter(Player& player) {
    std::vector<std::string> enemies = {"Goblin", "Orc", "Troll", "Dragon"};
    int enemyIdx = rollDice(enemies.size()) - 1;
    std::string enemy = enemies[enemyIdx];
    int enemyHealth = rollDice(30) + 10;

    std::cout << "\\nA wild " << enemy << " appears! (HP: " << enemyHealth << ")" << std::endl;

    while (enemyHealth > 0 && player.health > 0) {
        int playerAttack = rollDice(15) + 5;
        int enemyAttack = rollDice(10) + 2;

        enemyHealth -= playerAttack;
        std::cout << "You deal " << playerAttack << " damage. Enemy HP: "
                  << (enemyHealth > 0 ? enemyHealth : 0) << std::endl;

        if (enemyHealth > 0) {
            player.health -= enemyAttack;
            std::cout << enemy << " deals " << enemyAttack << " damage. Your HP: "
                      << player.health << std::endl;
        }
    }

    if (player.health > 0) {
        int reward = rollDice(50) + 20;
        player.score += reward;
        std::cout << "Victory! You gained " << reward << " points." << std::endl;
        if (player.score >= player.level * 100) {
            player.level++;
            std::cout << "Level Up! You are now level " << player.level << "!" << std::endl;
        }
        return true;
    } else {
        std::cout << "You were defeated..." << std::endl;
        return false;
    }
}

int main() {
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    std::cout << "=== C++ Text Adventure Game ===" << std::endl;
    std::cout << "Enter your hero\\'s name: ";

    std::string playerName;
    std::getline(std::cin, playerName);

    if (playerName.empty()) {
        playerName = "Hero";
    }

    Player player(playerName);
    std::cout << "Welcome, " << player.name << "! Your adventure begins..." << std::endl;

    bool running = true;
    while (running && player.health > 0) {
        displayStatus(player);
        std::cout << "\\nWhat do you do?" << std::endl;
        std::cout << "1. Explore (fight an enemy)" << std::endl;
        std::cout << "2. Rest (+20 HP)" << std::endl;
        std::cout << "3. Quit" << std::endl;
        std::cout << "Choice: ";

        int choice;
        if (!(std::cin >> choice)) {
            break;
        }

        switch (choice) {
            case 1:
                if (!encounter(player)) {
                    running = false;
                }
                break;
            case 2:
                player.health = std::min(100, player.health + 20);
                std::cout << "You rest. HP restored to " << player.health << std::endl;
                break;
            case 3:
                running = false;
                break;
            default:
                std::cout << "Invalid choice." << std::endl;
        }
    }

    std::cout << "\\n=== Game Over ===" << std::endl;
    std::cout << "Final Score: " << player.score << std::endl;
    std::cout << "Thank you for playing!" << std::endl;

    return 0;
}
'''

    with open(MAIN_CPP, 'w') as f:
        f.write(main_cpp_content)

    print(f'Created: {MAIN_CPP}')
    print(f'Project directory: {PROJECT_DIR}')
    print(f'No .vscode/ directory created (agent task)')
    print(f'No game binary created (agent must build)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with cpp_game project folder (DISPLAY=:0)')


create_initial()
