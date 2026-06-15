"""
Initial Setup: Java Spring Boot project workflow in VSCode
Task ID: vscode_wf_056
Domain: libreoffice_calc (VSCode task)

Creates ~/project with pom.xml, Java 17 and Maven assumed installed.
No Java extensions, no src structure, no .vscode configs.
Opens VSCode with ~/project folder.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')

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

    # Create a realistic pom.xml for a Spring Boot project
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.1</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo</name>
    <description>Spring Boot Demo Project</description>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"""

    pom_path = os.path.join(PROJECT_DIR, 'pom.xml')
    with open(pom_path, 'w') as f:
        f.write(pom_xml.strip() + '\n')
    print(f'Created: {pom_path}')

    # Ensure no .vscode directory exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # Ensure no src directory exists (task requires creating it)
    src_dir = os.path.join(PROJECT_DIR, 'src')
    if os.path.exists(src_dir):
        import shutil
        shutil.rmtree(src_dir)

    print(f'Initial project created at: {PROJECT_DIR}')

    # Uninstall Java Extension Pack if it happens to be installed
    subprocess.run(['code', '--uninstall-extension', 'vscjava.vscode-java-pack'],
                   capture_output=True, text=True)

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
