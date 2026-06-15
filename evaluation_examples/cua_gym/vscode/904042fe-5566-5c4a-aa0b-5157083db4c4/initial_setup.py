"""
Initial Setup: Set up Java bytecode generator Maven project with empty src directories
Task ID: vscode_gf4_088
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_088'
PROJECT_DIR = f'{WORKDIR}/projects/java-bytecode-generator'

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

def run_cmd(cmd, check=True, timeout=120):
    """Run a shell command with timeout."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if check and result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result

def install_java_maven():
    """Install Java 17 and Maven as user (no root required)."""
    home = os.path.expanduser("~")
    java_home = f"{home}/.local/jdk-17"
    maven_home = f"{home}/.local/apache-maven"

    # Install JDK 17 from Adoptium
    if not os.path.isdir(java_home):
        print("Downloading JDK 17...")
        jdk_url = "https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jdk/hotspot/normal/eclipse?project=jdk"
        run_cmd(f'curl -L -o /tmp/jdk17.tar.gz "{jdk_url}"', timeout=300)
        os.makedirs(f"{home}/.local", exist_ok=True)
        run_cmd(f'tar -xzf /tmp/jdk17.tar.gz -C {home}/.local', timeout=120)
        # Find extracted directory name
        result = run_cmd(f'ls -d {home}/.local/jdk-17*')
        extracted = result.stdout.strip().split('\n')[0]
        if extracted != java_home:
            run_cmd(f'mv "{extracted}" "{java_home}"')
        os.remove('/tmp/jdk17.tar.gz')
        print(f"JDK 17 installed at {java_home}")
    else:
        print(f"JDK 17 already present at {java_home}")

    # Install Maven from Apache
    if not os.path.isdir(maven_home):
        print("Downloading Maven...")
        mvn_url = "https://dlcdn.apache.org/maven/maven-3/3.9.14/binaries/apache-maven-3.9.14-bin.tar.gz"
        run_cmd(f'curl -L -o /tmp/maven.tar.gz "{mvn_url}"', timeout=120)
        run_cmd(f'tar -xzf /tmp/maven.tar.gz -C {home}/.local', timeout=60)
        result = run_cmd(f'ls -d {home}/.local/apache-maven-*')
        extracted = result.stdout.strip().split('\n')[0]
        if extracted != maven_home:
            run_cmd(f'mv "{extracted}" "{maven_home}"')
        os.remove('/tmp/maven.tar.gz')
        print(f"Maven installed at {maven_home}")
    else:
        print(f"Maven already present at {maven_home}")

    # Set up PATH and JAVA_HOME for this session and future shells
    os.environ["JAVA_HOME"] = java_home
    os.environ["PATH"] = f"{java_home}/bin:{maven_home}/bin:" + os.environ.get("PATH", "")

    # Write to bashrc so VSCode terminal also picks it up
    bashrc = f"{home}/.bashrc"
    marker = "# CUA-Gym Java setup"
    with open(bashrc, 'r') as f:
        content = f.read()
    if marker not in content:
        with open(bashrc, 'a') as f:
            f.write(f'\n{marker}\n')
            f.write(f'export JAVA_HOME="{java_home}"\n')
            f.write(f'export PATH="{java_home}/bin:{maven_home}/bin:$PATH"\n')

    # Verify
    result = run_cmd(f"{java_home}/bin/java --version")
    print(f"Java: {(result.stderr.strip() or result.stdout.strip()).split(chr(10))[0]}")
    result = run_cmd(f"{maven_home}/bin/mvn --version")
    print(f"Maven: {result.stdout.strip().split(chr(10))[0]}")

def create_project():
    """Create the Maven project structure with pom.xml."""
    # Create directory structure
    dirs = [
        f'{PROJECT_DIR}/src/main/java/com/bytegen',
        f'{PROJECT_DIR}/src/main/java/com/bytegen/examples',
        f'{PROJECT_DIR}/src/test/java/com/bytegen',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Write pom.xml with Java 17 and ASM 9.x
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.bytegen</groupId>
    <artifactId>java-bytecode-generator</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Java Bytecode Generator</name>
    <description>A library for generating Java classes at runtime using ASM bytecode manipulation</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <asm.version>9.6</asm.version>
        <junit.version>5.10.1</junit.version>
    </properties>

    <dependencies>
        <!-- ASM Core -->
        <dependency>
            <groupId>org.ow2.asm</groupId>
            <artifactId>asm</artifactId>
            <version>${asm.version}</version>
        </dependency>
        <!-- ASM Commons (for convenience adapters) -->
        <dependency>
            <groupId>org.ow2.asm</groupId>
            <artifactId>asm-commons</artifactId>
            <version>${asm.version}</version>
        </dependency>
        <!-- JUnit 5 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
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
                <version>3.2.3</version>
            </plugin>
        </plugins>
    </build>
</project>
"""
    with open(f'{PROJECT_DIR}/pom.xml', 'w') as f:
        f.write(pom_xml.strip() + '\n')
    print(f'Project created at {PROJECT_DIR}')
    print(f'pom.xml written with Java 17, ASM 9.6, JUnit 5.10.1')

def install_java_extension():
    """Install Java Extension Pack for VSCode."""
    print("Installing Java Extension Pack...")
    try:
        run_cmd("code --install-extension vscjava.vscode-java-pack --force", timeout=120)
        print("Java Extension Pack installed")
    except Exception as e:
        print(f"Warning: Extension install failed (may already be installed): {e}")

def main():
    install_java_maven()
    create_project()
    install_java_extension()

    home = os.path.expanduser("~")
    mvn_bin = f"{home}/.local/apache-maven/bin/mvn"

    # Pre-download Maven dependencies (so project is ready)
    print("Downloading Maven dependencies...")
    try:
        result = run_cmd(f"cd {PROJECT_DIR} && {mvn_bin} dependency:resolve -q", timeout=300)
        print("Maven dependencies downloaded")
    except Exception as e:
        print(f"Warning: Maven dependency download had issues: {e}")

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

main()
