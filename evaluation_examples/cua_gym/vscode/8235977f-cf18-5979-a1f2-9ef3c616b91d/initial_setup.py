"""
Initial Setup: Java Functional Utils Maven Project
Task ID: vscode_gf4_070
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_070'
PROJECT_DIR = f'{WORKDIR}/projects/java-functional-utils'

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
    """Install Java 17 and Maven on the VM."""
    print('Installing Java 17 and Maven...')
    subprocess.run("echo 'password' | sudo -S apt-get update -y", shell=True,
                   capture_output=True, timeout=120)
    result = subprocess.run("echo 'password' | sudo -S apt-get install -y openjdk-17-jdk maven", shell=True,
                   capture_output=True, text=True, timeout=300)
    print(f'Install result: {result.returncode}')
    if result.returncode != 0:
        print(f'Install stderr: {result.stderr[-500:]}')
    # Verify installation
    try:
        result = subprocess.run('java -version', shell=True, capture_output=True, text=True)
        print(f'Java: {result.stderr.strip()}')
    except Exception as e:
        print(f'Java verify: {e}')
    try:
        result = subprocess.run('mvn --version', shell=True, capture_output=True, text=True)
        print(f'Maven: {result.stdout.split(chr(10))[0]}')
    except Exception as e:
        print(f'Maven verify: {e}')

def create_initial():
    install_java_maven()

    # Create project directory structure
    dirs = [
        f'{PROJECT_DIR}/src/main/java/com/functional',
        f'{PROJECT_DIR}/src/main/java/com/functional/stream',
        f'{PROJECT_DIR}/src/test/java/com/functional',
        f'{PROJECT_DIR}/src/test/java/com/functional/stream',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Create pom.xml with Java 17 and JUnit 5
    pom_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.functional</groupId>
    <artifactId>java-functional-utils</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Java Functional Utils</name>
    <description>Functional programming utilities for Java 17</description>

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
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>
        </plugins>
    </build>
</project>
'''
    with open(f'{PROJECT_DIR}/pom.xml', 'w') as f:
        f.write(pom_xml)

    print(f'Project structure created at {PROJECT_DIR}')

    # Install Java Extension Pack if not already installed
    try:
        subprocess.run(['code', '--install-extension', 'vscjava.vscode-java-pack'],
                       capture_output=True, timeout=60)
        print('Java Extension Pack installed')
    except Exception as e:
        print(f'Extension install note: {e}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
