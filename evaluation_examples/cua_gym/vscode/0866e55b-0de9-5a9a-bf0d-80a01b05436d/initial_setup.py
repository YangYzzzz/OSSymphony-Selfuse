"""
Initial Setup: Java Design Patterns Maven Project (empty skeleton)
Task ID: vscode_gf4_036
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_036'
PROJECT_DIR = f'{WORKDIR}/projects/java-design-patterns'


def run_cmd(cmd, timeout=300):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr:
        print(f"WARN: {result.stderr.strip()}")
    return result


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


def install_java_maven():
    """Install Java 17 and Maven via SDKMAN if not present."""
    sdkman_init = f'{WORKDIR}/.sdkman/bin/sdkman-init.sh'

    # Install SDKMAN if needed
    if not os.path.exists(sdkman_init):
        print("Installing SDKMAN...")
        run_cmd(f'export SDKMAN_DIR={WORKDIR}/.sdkman && curl -s "https://get.sdkman.io" | bash')

    # Install Java 17 and Maven
    sdk_cmd = f'bash -c "source {sdkman_init} && '

    # Check if java is available
    result = run_cmd(f'{sdk_cmd} java --version 2>&1"')
    if 'not found' in (result.stderr or '') or result.returncode != 0:
        print("Installing Java 17...")
        run_cmd(f'{sdk_cmd} sdk install java 17.0.13-tem < /dev/null 2>&1"', timeout=300)

    # Check if mvn is available
    result = run_cmd(f'{sdk_cmd} mvn --version 2>&1"')
    if 'not found' in (result.stderr or '') or result.returncode != 0:
        print("Installing Maven...")
        run_cmd(f'{sdk_cmd} sdk install maven < /dev/null 2>&1"', timeout=300)

    print("Java and Maven ready")


def create_initial():
    # Install Java 17 and Maven
    install_java_maven()

    # Create Maven project directory structure
    os.makedirs(f'{PROJECT_DIR}/src/main/java/com/patterns', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/test/java/com/patterns', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # Create pom.xml with JUnit 5 dependencies and Java 17
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.patterns</groupId>
    <artifactId>java-design-patterns</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Java Design Patterns</name>
    <description>Implementation of common design patterns in Java</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <junit.version>5.10.2</junit.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-params</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.12.1</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""
    with open(f'{PROJECT_DIR}/pom.xml', 'w') as f:
        f.write(pom_xml.strip() + '\n')

    # Install Java Extension Pack in VSCode
    run_cmd('code --install-extension vscjava.vscode-java-pack 2>&1 || true', timeout=120)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  pom.xml with JUnit 5 deps')
    print(f'  src/main/java/com/patterns/ (empty)')
    print(f'  src/test/java/com/patterns/ (empty)')

    # Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
