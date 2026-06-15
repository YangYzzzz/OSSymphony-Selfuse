"""
Initial Setup: Java environment configuration task
Task ID: osworld_multi_apps_sys_config_007
Domain: os (system configuration)

Creates:
  - JDK 17 at /opt/jdk-17/ (if not present, simulates installation)
  - Maven project at /home/user/projects/java_app/ with pom.xml and source files
  - ~/.bashrc WITHOUT JAVA_HOME or java PATH configuration
  - Ensures Maven is NOT installed
"""

import os
import subprocess
import shutil
import time
import shlex

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_sys_config_007'
SUDO_PASS = 'password'


def sudo_run(cmd_list, **kwargs):
    """Run a command with sudo using the known VM password."""
    full_cmd = f"echo '{SUDO_PASS}' | sudo -S {' '.join(cmd_list)}"
    return subprocess.run(full_cmd, shell=True, **kwargs)


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


def setup_jdk():
    """Ensure JDK 17 exists at /opt/jdk-17/ but is NOT on PATH."""
    jdk_path = '/opt/jdk-17'

    # Check if JDK already exists at /opt/jdk-17/
    if not os.path.isdir(jdk_path):
        # Try to find any existing Java installation and symlink/copy it
        candidates = [
            '/usr/lib/jvm/java-17-openjdk-amd64',
            '/usr/lib/jvm/java-17-openjdk',
            '/usr/lib/jvm/java-17',
        ]
        jdk_found = None
        for c in candidates:
            if os.path.isdir(c):
                jdk_found = c
                break

        if not jdk_found:
            # Install OpenJDK 17 if not found
            print('Installing OpenJDK 17...')
            sudo_run(['apt-get', 'update', '-qq'])
            sudo_run(['apt-get', 'install', '-y', 'openjdk-17-jdk'])
            # Find where it was installed
            for c in candidates:
                if os.path.isdir(c):
                    jdk_found = c
                    break

        if jdk_found:
            # Create symlink so /opt/jdk-17 points to the found JDK
            sudo_run(['ln', '-sfn', jdk_found, jdk_path])
            print(f'Created symlink: {jdk_path} -> {jdk_found}')
        else:
            print('WARNING: Could not find or install JDK 17')
    else:
        print(f'JDK already exists at {jdk_path}')

    # Verify java binary exists
    java_bin = os.path.join(jdk_path, 'bin', 'java')
    if os.path.isfile(java_bin) or os.path.islink(java_bin):
        print(f'Verified: {java_bin} exists')
    else:
        print(f'WARNING: {java_bin} not found, JDK may not be properly set up')


def ensure_maven_not_installed():
    """Remove maven if accidentally installed (initial state requires no maven)."""
    result = subprocess.run(['which', 'mvn'], capture_output=True, text=True)
    if result.returncode == 0:
        print('Maven found, removing for initial state...')
        sudo_run(['apt-get', 'remove', '-y', 'maven'])
        sudo_run(['apt-get', 'autoremove', '-y'])
        print('Maven removed.')
    else:
        print('Maven not installed (correct initial state).')


def setup_bashrc():
    """Configure ~/.bashrc WITHOUT Java environment variables."""
    bashrc_path = os.path.join(WORKDIR, '.bashrc')

    # Read existing .bashrc
    if os.path.isfile(bashrc_path):
        with open(bashrc_path, 'r') as f:
            content = f.read()
    else:
        content = ''

    # Remove any existing JAVA_HOME or java PATH lines that might be there
    lines = content.splitlines(keepends=True)
    filtered_lines = []
    skip_next = False
    for line in lines:
        stripped = line.strip()
        # Skip JAVA_HOME and related PATH additions
        if (stripped.startswith('export JAVA_HOME=') or
                stripped.startswith('JAVA_HOME=') or
                'JAVA_HOME' in stripped or
                '/opt/jdk' in stripped):
            print(f'Removing line from .bashrc: {stripped}')
            continue
        filtered_lines.append(line)

    # Write clean .bashrc (without Java config)
    with open(bashrc_path, 'w') as f:
        f.writelines(filtered_lines)

    print(f'Configured {bashrc_path}: no JAVA_HOME or java PATH entries')


def create_maven_project():
    """Create a realistic Maven Java project at /home/user/projects/java_app/."""
    project_dir = os.path.join(WORKDIR, 'projects', 'java_app')
    src_main_java = os.path.join(project_dir, 'src', 'main', 'java', 'com', 'example')
    src_test_java = os.path.join(project_dir, 'src', 'test', 'java', 'com', 'example')

    os.makedirs(src_main_java, exist_ok=True)
    os.makedirs(src_test_java, exist_ok=True)

    # Create pom.xml
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>java-app</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Java Application</name>
    <description>A sample Java application for environment configuration testing</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
"""
    with open(os.path.join(project_dir, 'pom.xml'), 'w') as f:
        f.write(pom_xml)

    # Create main Java source file
    app_java = """package com.example;

/**
 * Main application entry point.
 * Demonstrates basic Java functionality including data processing
 * and utility operations.
 */
public class App {

    private String appName;
    private int version;

    public App(String appName, int version) {
        this.appName = appName;
        this.version = version;
    }

    public String getAppName() {
        return appName;
    }

    public int getVersion() {
        return version;
    }

    /**
     * Calculates the sum of an integer array.
     *
     * @param numbers array of integers to sum
     * @return sum of all elements
     */
    public static int calculateSum(int[] numbers) {
        int sum = 0;
        for (int num : numbers) {
            sum += num;
        }
        return sum;
    }

    /**
     * Reverses a string.
     *
     * @param input the string to reverse
     * @return reversed string
     */
    public static String reverseString(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        return new StringBuilder(input).reverse().toString();
    }

    /**
     * Checks if a number is prime.
     *
     * @param n the number to check
     * @return true if prime, false otherwise
     */
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        App app = new App("DataProcessor", 1);
        System.out.println("Application: " + app.getAppName() + " v" + app.getVersion());

        int[] data = {10, 25, 38, 42, 17, 93, 56, 81, 29, 64};
        System.out.println("Sum of data: " + calculateSum(data));
        System.out.println("Reversed 'hello': " + reverseString("hello"));
        System.out.println("Is 17 prime? " + isPrime(17));
        System.out.println("Is 20 prime? " + isPrime(20));
    }
}
"""
    with open(os.path.join(src_main_java, 'App.java'), 'w') as f:
        f.write(app_java)

    # Create a utility class
    string_utils_java = """package com.example;

import java.util.ArrayList;
import java.util.List;

/**
 * Utility class for string manipulation operations.
 */
public class StringUtils {

    /**
     * Splits a comma-separated string into a list of trimmed values.
     *
     * @param csv comma-separated string
     * @return list of trimmed strings
     */
    public static List<String> splitCsv(String csv) {
        List<String> result = new ArrayList<>();
        if (csv == null || csv.trim().isEmpty()) {
            return result;
        }
        for (String part : csv.split(",")) {
            result.add(part.trim());
        }
        return result;
    }

    /**
     * Capitalizes the first letter of each word.
     *
     * @param text input text
     * @return title-cased text
     */
    public static String toTitleCase(String text) {
        if (text == null || text.isEmpty()) return text;
        String[] words = text.split("\\\\s+");
        StringBuilder sb = new StringBuilder();
        for (String word : words) {
            if (!word.isEmpty()) {
                sb.append(Character.toUpperCase(word.charAt(0)))
                  .append(word.substring(1).toLowerCase())
                  .append(" ");
            }
        }
        return sb.toString().trim();
    }

    /**
     * Counts word occurrences in text.
     *
     * @param text  the text to analyze
     * @param word  the word to count
     * @return count of occurrences (case-insensitive)
     */
    public static int countOccurrences(String text, String word) {
        if (text == null || word == null || word.isEmpty()) return 0;
        int count = 0;
        String lowerText = text.toLowerCase();
        String lowerWord = word.toLowerCase();
        int index = 0;
        while ((index = lowerText.indexOf(lowerWord, index)) != -1) {
            count++;
            index += lowerWord.length();
        }
        return count;
    }
}
"""
    with open(os.path.join(src_main_java, 'StringUtils.java'), 'w') as f:
        f.write(string_utils_java)

    # Create test file
    app_test_java = """package com.example;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Unit tests for App class.
 */
public class AppTest {

    @Test
    public void testCalculateSum() {
        int[] numbers = {1, 2, 3, 4, 5};
        assertEquals(15, App.calculateSum(numbers));
    }

    @Test
    public void testReverseString() {
        assertEquals("olleh", App.reverseString("hello"));
        assertEquals("", App.reverseString(""));
    }

    @Test
    public void testIsPrime() {
        assertTrue(App.isPrime(17));
        assertFalse(App.isPrime(20));
        assertFalse(App.isPrime(1));
        assertTrue(App.isPrime(2));
    }
}
"""
    with open(os.path.join(src_test_java, 'AppTest.java'), 'w') as f:
        f.write(app_test_java)

    print(f'Maven project created at: {project_dir}')
    print(f'  - {project_dir}/pom.xml')
    print(f'  - {src_main_java}/App.java')
    print(f'  - {src_main_java}/StringUtils.java')
    print(f'  - {src_test_java}/AppTest.java')


def main():
    print('=== Initial Setup: osworld_multi_apps_sys_config_007 ===')

    # 1. Ensure JDK 17 is installed at /opt/jdk-17/
    print('\n[1] Setting up JDK 17 at /opt/jdk-17/...')
    setup_jdk()

    # 2. Ensure Maven is NOT installed (initial state)
    print('\n[2] Ensuring Maven is NOT installed...')
    ensure_maven_not_installed()

    # 3. Configure .bashrc without JAVA_HOME
    print('\n[3] Configuring ~/.bashrc (no JAVA_HOME)...')
    setup_bashrc()

    # 4. Create Maven project
    print('\n[4] Creating Maven project at /home/user/projects/java_app/...')
    create_maven_project()

    # 5. Open a terminal so the agent can work
    print('\n[5] Launching terminal for agent interaction...')
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

    print('\n=== Initial setup complete ===')
    print('State: JDK at /opt/jdk-17/, no JAVA_HOME in .bashrc, Maven not installed')
    print('Maven project ready at /home/user/projects/java_app/')


main()
