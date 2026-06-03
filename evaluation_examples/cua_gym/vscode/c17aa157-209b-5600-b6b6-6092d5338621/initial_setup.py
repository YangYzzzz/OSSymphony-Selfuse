"""
Initial Setup: Configure a tasks.json build task for a CMake project
Task ID: vscode_td_028
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_028'
PROJECT_DIR = f'{WORKDIR}/projects/physics-sim'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/include', exist_ok=True)

    # NO .vscode/ folder
    # NO build/ directory

    # CMakeLists.txt at project root
    cmake_content = """cmake_minimum_required(VERSION 3.16)
project(PhysicsSim VERSION 1.2.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Source files
set(SOURCES
    src/main.cpp
    src/particle.cpp
    src/vector3d.cpp
    src/simulation.cpp
    src/renderer.cpp
)

# Header files
set(HEADERS
    include/particle.h
    include/vector3d.h
    include/simulation.h
    include/renderer.h
    include/constants.h
)

add_executable(${PROJECT_NAME} ${SOURCES})
target_include_directories(${PROJECT_NAME} PRIVATE include)

# Find and link OpenGL (optional)
find_package(OpenGL QUIET)
if(OpenGL_FOUND)
    target_link_libraries(${PROJECT_NAME} OpenGL::GL)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAS_OPENGL=1)
endif()

# Math library
target_link_libraries(${PROJECT_NAME} m)

# Compiler warnings
target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic)

message(STATUS "Building PhysicsSim v${PROJECT_VERSION}")
"""
    with open(f'{PROJECT_DIR}/CMakeLists.txt', 'w') as f:
        f.write(cmake_content)

    # include/constants.h
    with open(f'{PROJECT_DIR}/include/constants.h', 'w') as f:
        f.write("""#ifndef CONSTANTS_H
#define CONSTANTS_H

namespace Physics {
    constexpr double GRAVITY = 9.80665;
    constexpr double BOLTZMANN = 1.380649e-23;
    constexpr double TIME_STEP = 0.001;
    constexpr int MAX_PARTICLES = 10000;
    constexpr double DAMPING_FACTOR = 0.98;
}

#endif // CONSTANTS_H
""")

    # include/vector3d.h
    with open(f'{PROJECT_DIR}/include/vector3d.h', 'w') as f:
        f.write("""#ifndef VECTOR3D_H
#define VECTOR3D_H

#include <cmath>
#include <iostream>

class Vector3D {
public:
    double x, y, z;

    Vector3D() : x(0), y(0), z(0) {}
    Vector3D(double x, double y, double z) : x(x), y(y), z(z) {}

    Vector3D operator+(const Vector3D& other) const;
    Vector3D operator-(const Vector3D& other) const;
    Vector3D operator*(double scalar) const;
    double dot(const Vector3D& other) const;
    Vector3D cross(const Vector3D& other) const;
    double magnitude() const;
    Vector3D normalized() const;

    friend std::ostream& operator<<(std::ostream& os, const Vector3D& v);
};

#endif // VECTOR3D_H
""")

    # include/particle.h
    with open(f'{PROJECT_DIR}/include/particle.h', 'w') as f:
        f.write("""#ifndef PARTICLE_H
#define PARTICLE_H

#include "vector3d.h"

class Particle {
public:
    Vector3D position;
    Vector3D velocity;
    Vector3D acceleration;
    double mass;
    double radius;
    bool is_fixed;

    Particle(Vector3D pos, double mass, double radius = 0.1);

    void apply_force(const Vector3D& force);
    void update(double dt);
    double kinetic_energy() const;
    void reset_forces();
};

#endif // PARTICLE_H
""")

    # include/simulation.h
    with open(f'{PROJECT_DIR}/include/simulation.h', 'w') as f:
        f.write("""#ifndef SIMULATION_H
#define SIMULATION_H

#include <vector>
#include <string>
#include "particle.h"

class Simulation {
public:
    std::vector<Particle> particles;
    double total_time;
    int step_count;

    Simulation();

    void add_particle(const Particle& p);
    void step(double dt);
    void run(double duration, double dt);
    double total_energy() const;
    void export_state(const std::string& filename) const;
};

#endif // SIMULATION_H
""")

    # include/renderer.h
    with open(f'{PROJECT_DIR}/include/renderer.h', 'w') as f:
        f.write("""#ifndef RENDERER_H
#define RENDERER_H

#include "simulation.h"

class Renderer {
public:
    int width, height;
    bool headless;

    Renderer(int w = 800, int h = 600, bool headless = false);

    void init();
    void draw_frame(const Simulation& sim);
    void cleanup();
};

#endif // RENDERER_H
""")

    # src/main.cpp
    with open(f'{PROJECT_DIR}/src/main.cpp', 'w') as f:
        f.write("""#include <iostream>
#include <cstdlib>
#include "simulation.h"
#include "renderer.h"
#include "constants.h"

int main(int argc, char* argv[]) {
    std::cout << "PhysicsSim - Particle Physics Simulator" << std::endl;
    std::cout << "========================================" << std::endl;

    bool headless = false;
    if (argc > 1 && std::string(argv[1]) == "--headless") {
        headless = true;
    }

    Simulation sim;

    // Create a grid of particles
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            Vector3D pos(i * 0.5, j * 0.5 + 2.0, 0.0);
            Particle p(pos, 1.0, 0.05);
            sim.add_particle(p);
        }
    }

    // Add a fixed floor particle
    Particle floor(Vector3D(2.5, -1.0, 0.0), 1e6, 5.0);
    floor.is_fixed = true;
    sim.add_particle(floor);

    std::cout << "Particles: " << sim.particles.size() << std::endl;
    std::cout << "Time step: " << Physics::TIME_STEP << " s" << std::endl;

    Renderer renderer(800, 600, headless);
    renderer.init();

    double duration = 5.0;
    double dt = Physics::TIME_STEP;
    int frames = static_cast<int>(duration / dt);

    for (int i = 0; i < frames; ++i) {
        sim.step(dt);
        if (i % 100 == 0) {
            renderer.draw_frame(sim);
            std::cout << "Step " << i << "/" << frames
                      << " Energy: " << sim.total_energy() << std::endl;
        }
    }

    sim.export_state("final_state.csv");
    renderer.cleanup();

    std::cout << "Simulation complete. Total time: " << sim.total_time << " s" << std::endl;
    return 0;
}
""")

    # src/vector3d.cpp
    with open(f'{PROJECT_DIR}/src/vector3d.cpp', 'w') as f:
        f.write("""#include "vector3d.h"

Vector3D Vector3D::operator+(const Vector3D& other) const {
    return Vector3D(x + other.x, y + other.y, z + other.z);
}

Vector3D Vector3D::operator-(const Vector3D& other) const {
    return Vector3D(x - other.x, y - other.y, z - other.z);
}

Vector3D Vector3D::operator*(double scalar) const {
    return Vector3D(x * scalar, y * scalar, z * scalar);
}

double Vector3D::dot(const Vector3D& other) const {
    return x * other.x + y * other.y + z * other.z;
}

Vector3D Vector3D::cross(const Vector3D& other) const {
    return Vector3D(
        y * other.z - z * other.y,
        z * other.x - x * other.z,
        x * other.y - y * other.x
    );
}

double Vector3D::magnitude() const {
    return std::sqrt(x * x + y * y + z * z);
}

Vector3D Vector3D::normalized() const {
    double mag = magnitude();
    if (mag < 1e-12) return Vector3D();
    return *this * (1.0 / mag);
}

std::ostream& operator<<(std::ostream& os, const Vector3D& v) {
    os << "(" << v.x << ", " << v.y << ", " << v.z << ")";
    return os;
}
""")

    # src/particle.cpp
    with open(f'{PROJECT_DIR}/src/particle.cpp', 'w') as f:
        f.write("""#include "particle.h"
#include "constants.h"

Particle::Particle(Vector3D pos, double mass, double radius)
    : position(pos), mass(mass), radius(radius), is_fixed(false) {}

void Particle::apply_force(const Vector3D& force) {
    if (!is_fixed) {
        acceleration = acceleration + force * (1.0 / mass);
    }
}

void Particle::update(double dt) {
    if (is_fixed) return;

    velocity = velocity + acceleration * dt;
    velocity = velocity * Physics::DAMPING_FACTOR;
    position = position + velocity * dt;
    reset_forces();
}

double Particle::kinetic_energy() const {
    double v = velocity.magnitude();
    return 0.5 * mass * v * v;
}

void Particle::reset_forces() {
    acceleration = Vector3D(0, 0, 0);
}
""")

    # src/simulation.cpp
    with open(f'{PROJECT_DIR}/src/simulation.cpp', 'w') as f:
        f.write("""#include "simulation.h"
#include "constants.h"
#include <fstream>

Simulation::Simulation() : total_time(0), step_count(0) {}

void Simulation::add_particle(const Particle& p) {
    particles.push_back(p);
}

void Simulation::step(double dt) {
    // Apply gravity to all particles
    Vector3D gravity(0, -Physics::GRAVITY, 0);
    for (auto& p : particles) {
        p.apply_force(gravity * p.mass);
    }

    // Simple collision detection between particles
    for (size_t i = 0; i < particles.size(); ++i) {
        for (size_t j = i + 1; j < particles.size(); ++j) {
            Vector3D diff = particles[i].position - particles[j].position;
            double dist = diff.magnitude();
            double min_dist = particles[i].radius + particles[j].radius;

            if (dist < min_dist && dist > 1e-12) {
                Vector3D normal = diff.normalized();
                double overlap = min_dist - dist;
                double spring_force = 5000.0 * overlap;
                particles[i].apply_force(normal * spring_force);
                particles[j].apply_force(normal * (-spring_force));
            }
        }
    }

    // Update positions
    for (auto& p : particles) {
        p.update(dt);
    }

    total_time += dt;
    step_count++;
}

void Simulation::run(double duration, double dt) {
    int steps = static_cast<int>(duration / dt);
    for (int i = 0; i < steps; ++i) {
        step(dt);
    }
}

double Simulation::total_energy() const {
    double energy = 0;
    for (const auto& p : particles) {
        energy += p.kinetic_energy();
        energy += p.mass * Physics::GRAVITY * p.position.y;
    }
    return energy;
}

void Simulation::export_state(const std::string& filename) const {
    std::ofstream file(filename);
    file << "id,x,y,z,vx,vy,vz,mass" << std::endl;
    for (size_t i = 0; i < particles.size(); ++i) {
        const auto& p = particles[i];
        file << i << ","
             << p.position.x << "," << p.position.y << "," << p.position.z << ","
             << p.velocity.x << "," << p.velocity.y << "," << p.velocity.z << ","
             << p.mass << std::endl;
    }
}
""")

    # src/renderer.cpp
    with open(f'{PROJECT_DIR}/src/renderer.cpp', 'w') as f:
        f.write("""#include "renderer.h"
#include <iostream>

Renderer::Renderer(int w, int h, bool headless)
    : width(w), height(h), headless(headless) {}

void Renderer::init() {
    if (headless) {
        std::cout << "Renderer: headless mode" << std::endl;
        return;
    }
#ifdef HAS_OPENGL
    std::cout << "Renderer: OpenGL initialized (" << width << "x" << height << ")" << std::endl;
#else
    std::cout << "Renderer: No graphics backend, using text output" << std::endl;
#endif
}

void Renderer::draw_frame(const Simulation& sim) {
    if (headless) return;
    // Placeholder rendering
    (void)sim;
}

void Renderer::cleanup() {
    std::cout << "Renderer: cleanup complete" << std::endl;
}
""")

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# PhysicsSim

A particle-based physics simulation engine written in C++17.

## Features

- 3D particle dynamics with gravity
- Spring-based collision response
- CSV state export for analysis
- Optional OpenGL rendering

## Building

```bash
mkdir -p build
cd build
cmake ..
make -j$(nproc)
```

## Usage

```bash
./PhysicsSim            # with rendering
./PhysicsSim --headless # headless mode
```

## Project Structure

```
physics-sim/
  CMakeLists.txt
  include/         # Header files
  src/             # Source files
  build/           # Build directory (created during build)
```
""")

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'CMakeLists.txt: {PROJECT_DIR}/CMakeLists.txt')
    print(f'Source files in: {PROJECT_DIR}/src/')
    print(f'Headers in: {PROJECT_DIR}/include/')
    print('No .vscode/ folder present')
    print('No build/ directory present')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
