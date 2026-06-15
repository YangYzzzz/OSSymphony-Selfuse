"""
Reward Script: Rust Game Engine Project Setup in VSCode
Task ID: vscode_gf4_049
Domain: vscode
Scoring:
  Component 1: Cargo.toml has required dependencies (0.20)
  Component 2: src/engine/window.rs exists with winit EventLoop/Window (0.15)
  Component 3: src/engine/renderer.rs has Renderer struct with wgpu fields (0.20)
  Component 4: src/engine/mesh.rs has Mesh struct with vertex/index buffers (0.15)
  Component 5: src/shaders/triangle.wgsl has vertex and fragment shaders (0.10)
  Component 6: src/main.rs initializes engine (mod engine, uses winit/renderer) (0.10)
  Component 7: .vscode/tasks.json has cargo build --release and run tasks (0.10)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_049'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'rust-game-engine')


def verify_task():
    total_score = 0.0

    # Component 1: Cargo.toml has winit, wgpu, cgmath, bytemuck in [dependencies] (0.20 pts)
    try:
        cargo_path = os.path.join(PROJECT_DIR, 'Cargo.toml')
        with open(cargo_path, 'r') as f:
            cargo_content = f.read()

        required_deps = ['winit', 'wgpu', 'cgmath', 'bytemuck']
        found_deps = []
        in_deps = False
        for line in cargo_content.split('\n'):
            stripped = line.strip()
            if stripped == '[dependencies]':
                in_deps = True
                continue
            if stripped.startswith('[') and in_deps:
                in_deps = False
            if in_deps:
                for dep in required_deps:
                    if stripped.startswith(dep + ' ') or stripped.startswith(dep + '='):
                        if dep not in found_deps:
                            found_deps.append(dep)

        if len(found_deps) == 4:
            print(f"PASS: Component 1 — All 4 dependencies found: {found_deps} (0.20 pts)")
            total_score += 0.20
        elif len(found_deps) >= 2:
            partial = 0.10
            print(f"PARTIAL: Component 1 — Found {len(found_deps)}/4 deps: {found_deps} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {len(found_deps)}/4 deps found: {found_deps}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: src/engine/window.rs exists with winit EventLoop and Window (0.15 pts)
    try:
        window_path = os.path.join(PROJECT_DIR, 'src', 'engine', 'window.rs')
        if not os.path.exists(window_path):
            print("FAIL: Component 2 — src/engine/window.rs does not exist")
        else:
            with open(window_path, 'r') as f:
                window_content = f.read()
            has_eventloop = 'EventLoop' in window_content
            has_window = 'Window' in window_content
            has_winit = 'winit' in window_content
            if has_eventloop and has_window and has_winit:
                print(f"PASS: Component 2 — window.rs has EventLoop, Window, winit imports (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Missing: EventLoop={has_eventloop}, Window={has_window}, winit={has_winit}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: src/engine/renderer.rs has Renderer struct with wgpu Device/Queue/Surface/RenderPipeline (0.20 pts)
    try:
        renderer_path = os.path.join(PROJECT_DIR, 'src', 'engine', 'renderer.rs')
        if not os.path.exists(renderer_path):
            print("FAIL: Component 3 — src/engine/renderer.rs does not exist")
        else:
            with open(renderer_path, 'r') as f:
                renderer_content = f.read()
            has_struct = 'struct Renderer' in renderer_content or 'pub struct Renderer' in renderer_content
            has_device = 'Device' in renderer_content
            has_queue = 'Queue' in renderer_content
            has_surface = 'Surface' in renderer_content
            has_pipeline = 'RenderPipeline' in renderer_content
            checks = [has_struct, has_device, has_queue, has_surface, has_pipeline]
            passed = sum(checks)
            if passed == 5:
                print(f"PASS: Component 3 — Renderer struct with Device, Queue, Surface, RenderPipeline (0.20 pts)")
                total_score += 0.20
            elif passed >= 3:
                partial = 0.10
                print(f"PARTIAL: Component 3 — {passed}/5 checks passed (struct={has_struct}, Device={has_device}, Queue={has_queue}, Surface={has_surface}, Pipeline={has_pipeline}) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {passed}/5: struct={has_struct}, Device={has_device}, Queue={has_queue}, Surface={has_surface}, Pipeline={has_pipeline}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: src/engine/mesh.rs has Mesh struct with vertex and index buffers (0.15 pts)
    try:
        mesh_path = os.path.join(PROJECT_DIR, 'src', 'engine', 'mesh.rs')
        if not os.path.exists(mesh_path):
            print("FAIL: Component 4 — src/engine/mesh.rs does not exist")
        else:
            with open(mesh_path, 'r') as f:
                mesh_content = f.read()
            has_mesh_struct = 'struct Mesh' in mesh_content or 'pub struct Mesh' in mesh_content
            has_vertex_buffer = 'vertex_buffer' in mesh_content
            has_index_buffer = 'index_buffer' in mesh_content
            if has_mesh_struct and has_vertex_buffer and has_index_buffer:
                print(f"PASS: Component 4 — Mesh struct with vertex_buffer and index_buffer (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Mesh={has_mesh_struct}, vertex_buffer={has_vertex_buffer}, index_buffer={has_index_buffer}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: src/shaders/triangle.wgsl has vertex and fragment shaders (0.10 pts)
    try:
        shader_path = os.path.join(PROJECT_DIR, 'src', 'shaders', 'triangle.wgsl')
        if not os.path.exists(shader_path):
            print("FAIL: Component 5 — src/shaders/triangle.wgsl does not exist")
        else:
            with open(shader_path, 'r') as f:
                shader_content = f.read()
            has_vertex = '@vertex' in shader_content
            has_fragment = '@fragment' in shader_content
            if has_vertex and has_fragment:
                print(f"PASS: Component 5 — triangle.wgsl has @vertex and @fragment shaders (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — @vertex={has_vertex}, @fragment={has_fragment}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: src/main.rs initializes engine (mod engine, uses renderer/winit) (0.10 pts)
    try:
        main_path = os.path.join(PROJECT_DIR, 'src', 'main.rs')
        with open(main_path, 'r') as f:
            main_content = f.read()
        has_mod_engine = 'mod engine' in main_content
        has_winit_use = 'winit' in main_content
        # The initial main.rs is just "fn main() {}" — no mod engine or winit
        if has_mod_engine and has_winit_use:
            print(f"PASS: Component 6 — main.rs declares mod engine and uses winit (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — mod engine={has_mod_engine}, winit={has_winit_use}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: .vscode/tasks.json has cargo build --release and a run task (0.10 pts)
    try:
        import json
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print("FAIL: Component 7 — .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                tasks_json = json.load(f)
            tasks_list = tasks_json.get('tasks', [])
            has_build_release = False
            has_run = False
            for task in tasks_list:
                cmd = task.get('command', '')
                if 'cargo build' in cmd and '--release' in cmd:
                    has_build_release = True
                if 'cargo run' in cmd:
                    has_run = True
            if has_build_release and has_run:
                print(f"PASS: Component 7 — tasks.json has cargo build --release and cargo run (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — build --release={has_build_release}, run={has_run}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
