"""
Initial Setup: Configure a tasks.json build task for a C++ project
Task ID: vscode_td_013
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_013'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'cpp-game')


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
    src_dir = os.path.join(PROJECT_DIR, 'src')
    bin_dir = os.path.join(PROJECT_DIR, 'bin')
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(bin_dir, exist_ok=True)

    # Create src/main.cpp - a simple game entry point
    main_cpp = os.path.join(src_dir, 'main.cpp')
    with open(main_cpp, 'w') as f:
        f.write('''#include <iostream>
#include <string>
#include "engine.h"

int main(int argc, char* argv[]) {
    std::cout << "=== Stellar Drift - A Space Adventure ===" << std::endl;
    std::cout << std::endl;

    GameEngine engine;
    engine.initialize(800, 600, "Stellar Drift");

    if (!engine.loadAssets()) {
        std::cerr << "Failed to load game assets!" << std::endl;
        return 1;
    }

    std::cout << "Engine initialized successfully." << std::endl;
    std::cout << "Window: " << engine.getWidth() << "x" << engine.getHeight() << std::endl;
    std::cout << "Starting game loop..." << std::endl;

    while (engine.isRunning()) {
        engine.processInput();
        engine.update(0.016f);  // ~60 FPS
        engine.render();
    }

    engine.shutdown();
    std::cout << "Game exited cleanly." << std::endl;
    return 0;
}
''')

    # Create src/engine.h
    engine_h = os.path.join(src_dir, 'engine.h')
    with open(engine_h, 'w') as f:
        f.write('''#ifndef ENGINE_H
#define ENGINE_H

#include <string>
#include <vector>

struct Vector2D {
    float x;
    float y;
    Vector2D(float x = 0.0f, float y = 0.0f) : x(x), y(y) {}
    Vector2D operator+(const Vector2D& other) const {
        return Vector2D(x + other.x, y + other.y);
    }
    Vector2D operator*(float scalar) const {
        return Vector2D(x * scalar, y * scalar);
    }
};

struct Entity {
    std::string name;
    Vector2D position;
    Vector2D velocity;
    float health;
    bool active;
};

class GameEngine {
public:
    GameEngine();
    ~GameEngine();

    void initialize(int width, int height, const std::string& title);
    bool loadAssets();
    void processInput();
    void update(float deltaTime);
    void render();
    void shutdown();

    bool isRunning() const { return running_; }
    int getWidth() const { return width_; }
    int getHeight() const { return height_; }

    void spawnEntity(const std::string& name, float x, float y);
    void removeEntity(const std::string& name);
    size_t getEntityCount() const { return entities_.size(); }

private:
    int width_;
    int height_;
    std::string title_;
    bool running_;
    int frameCount_;
    std::vector<Entity> entities_;

    void updateEntities(float deltaTime);
    void checkCollisions();
    void cleanupInactiveEntities();
};

#endif // ENGINE_H
''')

    # Create src/engine.cpp
    engine_cpp = os.path.join(src_dir, 'engine.cpp')
    with open(engine_cpp, 'w') as f:
        f.write('''#include "engine.h"
#include <iostream>
#include <algorithm>
#include <cmath>

GameEngine::GameEngine()
    : width_(0), height_(0), running_(false), frameCount_(0) {
}

GameEngine::~GameEngine() {
    if (running_) {
        shutdown();
    }
}

void GameEngine::initialize(int width, int height, const std::string& title) {
    width_ = width;
    height_ = height;
    title_ = title;
    running_ = true;
    frameCount_ = 0;

    std::cout << "[Engine] Initialized: " << title_ << " ("
              << width_ << "x" << height_ << ")" << std::endl;
}

bool GameEngine::loadAssets() {
    std::cout << "[Engine] Loading textures..." << std::endl;
    std::cout << "[Engine] Loading sounds..." << std::endl;
    std::cout << "[Engine] Loading level data..." << std::endl;

    // Spawn initial entities
    spawnEntity("player_ship", 400.0f, 500.0f);
    spawnEntity("asteroid_01", 200.0f, 100.0f);
    spawnEntity("asteroid_02", 600.0f, 150.0f);
    spawnEntity("powerup_shield", 350.0f, 250.0f);

    std::cout << "[Engine] Assets loaded. Entities: " << entities_.size() << std::endl;
    return true;
}

void GameEngine::processInput() {
    // Placeholder for input processing
    if (frameCount_ > 300) {  // Auto-exit after ~5 seconds at 60 FPS
        running_ = false;
    }
}

void GameEngine::update(float deltaTime) {
    frameCount_++;
    updateEntities(deltaTime);
    checkCollisions();
    cleanupInactiveEntities();
}

void GameEngine::render() {
    // Placeholder for rendering
}

void GameEngine::shutdown() {
    running_ = false;
    entities_.clear();
    std::cout << "[Engine] Shutdown complete. Total frames: " << frameCount_ << std::endl;
}

void GameEngine::spawnEntity(const std::string& name, float x, float y) {
    Entity e;
    e.name = name;
    e.position = Vector2D(x, y);
    e.velocity = Vector2D(0.0f, 0.0f);
    e.health = 100.0f;
    e.active = true;
    entities_.push_back(e);
}

void GameEngine::removeEntity(const std::string& name) {
    for (auto& entity : entities_) {
        if (entity.name == name) {
            entity.active = false;
            break;
        }
    }
}

void GameEngine::updateEntities(float deltaTime) {
    for (auto& entity : entities_) {
        if (!entity.active) continue;
        entity.position = entity.position + entity.velocity * deltaTime;

        // Wrap around screen edges
        if (entity.position.x < 0) entity.position.x += width_;
        if (entity.position.x > width_) entity.position.x -= width_;
        if (entity.position.y < 0) entity.position.y += height_;
        if (entity.position.y > height_) entity.position.y -= height_;
    }
}

void GameEngine::checkCollisions() {
    for (size_t i = 0; i < entities_.size(); ++i) {
        if (!entities_[i].active) continue;
        for (size_t j = i + 1; j < entities_.size(); ++j) {
            if (!entities_[j].active) continue;
            float dx = entities_[i].position.x - entities_[j].position.x;
            float dy = entities_[i].position.y - entities_[j].position.y;
            float dist = std::sqrt(dx * dx + dy * dy);
            if (dist < 30.0f) {
                // Simple collision response
                entities_[j].health -= 25.0f;
                if (entities_[j].health <= 0) {
                    entities_[j].active = false;
                }
            }
        }
    }
}

void GameEngine::cleanupInactiveEntities() {
    entities_.erase(
        std::remove_if(entities_.begin(), entities_.end(),
            [](const Entity& e) { return !e.active; }),
        entities_.end()
    );
}
''')

    # Ensure NO .vscode folder exists (negative constraint)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/main.cpp: game entry point')
    print(f'  src/engine.cpp: game engine implementation')
    print(f'  src/engine.h: game engine header')
    print(f'  bin/: empty output directory')
    print(f'  .vscode/: does NOT exist (task requires creating it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
