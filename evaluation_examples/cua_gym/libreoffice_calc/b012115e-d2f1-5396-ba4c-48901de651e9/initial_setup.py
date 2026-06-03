"""
Initial Setup: Write a JUnit 5 test class for Calculator
Task ID: vscode_lang_056
Domain: libreoffice_calc (actually VSCode/Java)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_056'
PROJECT_DIR = f'{WORKDIR}/calculator-project'


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


def run_cmd(cmd, check=True):
    """Run a shell command, print output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")
    return result


def install_java_maven():
    """Install JDK 17 and Maven."""
    print("Installing JDK 17 and Maven...")
    run_cmd("echo 'password' | sudo -S apt-get update -qq", check=False)
    run_cmd("echo 'password' | sudo -S DEBIAN_FRONTEND=noninteractive apt-get install -y -qq openjdk-17-jdk maven", check=True)
    # Verify
    run_cmd("java -version")
    run_cmd("mvn --version")
    print("Java and Maven installed successfully.")


def create_project():
    """Create the Maven project structure with Calculator.java."""

    # Create directory structure
    main_pkg = os.path.join(PROJECT_DIR, 'src', 'main', 'java', 'com', 'example')
    test_pkg = os.path.join(PROJECT_DIR, 'src', 'test', 'java', 'com', 'example')
    os.makedirs(main_pkg, exist_ok=True)
    os.makedirs(test_pkg, exist_ok=True)

    # pom.xml with JUnit 5
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>calculator</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Calculator Project</name>
    <description>A simple calculator with JUnit 5 tests</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <junit.jupiter.version>5.10.1</junit.jupiter.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.jupiter.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.3</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""
    with open(os.path.join(PROJECT_DIR, 'pom.xml'), 'w') as f:
        f.write(pom_xml)

    # Calculator.java
    calculator_java = """package com.example;

/**
 * A simple calculator class providing basic arithmetic operations.
 * Used for demonstrating JUnit 5 testing capabilities.
 */
public class Calculator {

    /**
     * Adds two integers and returns the result.
     *
     * @param a the first operand
     * @param b the second operand
     * @return the sum of a and b
     */
    public int add(int a, int b) {
        return a + b;
    }

    /**
     * Subtracts the second integer from the first and returns the result.
     *
     * @param a the first operand
     * @param b the second operand
     * @return the difference of a and b
     */
    public int subtract(int a, int b) {
        return a - b;
    }

    /**
     * Multiplies two integers and returns the result.
     *
     * @param a the first operand
     * @param b the second operand
     * @return the product of a and b
     */
    public int multiply(int a, int b) {
        return a * b;
    }
}
"""
    with open(os.path.join(main_pkg, 'Calculator.java'), 'w') as f:
        f.write(calculator_java)

    print(f"Project created at {PROJECT_DIR}")
    print(f"  - pom.xml with JUnit 5 dependency")
    print(f"  - Calculator.java with add, subtract, multiply methods")
    print(f"  - Empty test directory at src/test/java/com/example/")


def install_vscode_java_extensions():
    """Install Java extensions for VSCode."""
    extensions = [
        "redhat.java",
        "vscjava.vscode-java-test",
        "vscjava.vscode-maven",
        "vscjava.vscode-java-debug",
    ]
    for ext in extensions:
        print(f"Installing VSCode extension: {ext}")
        run_cmd(f'code --install-extension {ext} --force', check=False)


def configure_vscode():
    """Configure VSCode settings for Java development."""
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)

    # Workspace settings for Java
    import json
    settings = {
        "java.configuration.updateBuildConfiguration": "automatic",
        "java.test.defaultConfig": "default",
        "java.compile.nullAnalysis.mode": "disabled"
    }
    with open(os.path.join(vscode_dir, 'settings.json'), 'w') as f:
        json.dump(settings, f, indent=4)


def setup():
    # Step 1: Install Java and Maven
    install_java_maven()

    # Step 2: Create project
    create_project()

    # Step 3: Install VSCode Java extensions
    install_vscode_java_extensions()

    # Step 4: Configure VSCode
    configure_vscode()

    # Step 5: Pre-download Maven dependencies
    print("Pre-downloading Maven dependencies...")
    run_cmd(f'cd {PROJECT_DIR} && mvn dependency:resolve -q', check=False)
    run_cmd(f'cd {PROJECT_DIR} && mvn compile -q', check=False)

    # Step 6: Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with calculator-project and DISPLAY=:0')


setup()
