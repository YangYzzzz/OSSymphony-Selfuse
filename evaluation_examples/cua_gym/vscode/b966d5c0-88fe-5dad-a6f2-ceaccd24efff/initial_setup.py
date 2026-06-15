"""
Initial Setup: Configure Java test coverage by installing the Test Coverage extension
Task ID: vscode_lang_065
Domain: vscode

Creates a Java Maven project with JUnit 5 tests and JaCoCo plugin.
No coverage extension or configuration exists yet.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_065'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_directory(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    # --- Create Maven project structure ---
    src_main = f'{PROJECT_DIR}/src/main/java/com/taskapp/calculator'
    src_test = f'{PROJECT_DIR}/src/test/java/com/taskapp/calculator'

    create_directory(src_main)
    create_directory(src_test)

    # --- pom.xml with JaCoCo Maven plugin ---
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.taskapp</groupId>
    <artifactId>calculator</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Calculator Application</name>
    <description>A calculator library with comprehensive test coverage</description>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <junit.jupiter.version>5.9.3</junit.jupiter.version>
        <jacoco.version>0.8.10</jacoco.version>
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
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <version>${jacoco.version}</version>
                <executions>
                    <execution>
                        <id>prepare-agent</id>
                        <goals>
                            <goal>prepare-agent</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>report</id>
                        <phase>test</phase>
                        <goals>
                            <goal>report</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
        </plugins>
    </build>
</project>
"""
    write_file(f'{PROJECT_DIR}/pom.xml', pom_xml)

    # --- Main Java source: Calculator.java ---
    calculator_java = """package com.taskapp.calculator;

/**
 * A simple calculator class providing basic arithmetic operations
 * and some utility methods for common calculations.
 */
public class Calculator {

    /**
     * Adds two numbers together.
     * @param a first operand
     * @param b second operand
     * @return sum of a and b
     */
    public double add(double a, double b) {
        return a + b;
    }

    /**
     * Subtracts the second number from the first.
     * @param a first operand
     * @param b second operand
     * @return difference of a and b
     */
    public double subtract(double a, double b) {
        return a - b;
    }

    /**
     * Multiplies two numbers.
     * @param a first operand
     * @param b second operand
     * @return product of a and b
     */
    public double multiply(double a, double b) {
        return a * b;
    }

    /**
     * Divides the first number by the second.
     * @param a numerator
     * @param b denominator
     * @return quotient of a divided by b
     * @throws ArithmeticException if b is zero
     */
    public double divide(double a, double b) {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        return a / b;
    }

    /**
     * Calculates the factorial of a non-negative integer.
     * @param n the number to compute factorial for
     * @return factorial of n
     * @throws IllegalArgumentException if n is negative
     */
    public long factorial(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("Factorial is not defined for negative numbers");
        }
        if (n <= 1) {
            return 1;
        }
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    /**
     * Checks if a number is prime.
     * @param n the number to check
     * @return true if n is prime, false otherwise
     */
    public boolean isPrime(int n) {
        if (n <= 1) {
            return false;
        }
        if (n <= 3) {
            return true;
        }
        if (n % 2 == 0 || n % 3 == 0) {
            return false;
        }
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }
        return true;
    }

    /**
     * Computes the greatest common divisor of two integers.
     * @param a first integer
     * @param b second integer
     * @return GCD of a and b
     */
    public int gcd(int a, int b) {
        a = Math.abs(a);
        b = Math.abs(b);
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
}
"""
    write_file(f'{src_main}/Calculator.java', calculator_java)

    # --- Test Java source: CalculatorTest.java ---
    calculator_test_java = """package com.taskapp.calculator;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Nested;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Calculator Tests")
class CalculatorTest {

    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Nested
    @DisplayName("Addition Tests")
    class AdditionTests {

        @Test
        @DisplayName("should add two positive numbers")
        void testAddPositive() {
            assertEquals(5.0, calculator.add(2.0, 3.0), 0.001);
        }

        @Test
        @DisplayName("should add negative numbers")
        void testAddNegative() {
            assertEquals(-5.0, calculator.add(-2.0, -3.0), 0.001);
        }

        @Test
        @DisplayName("should add zero")
        void testAddZero() {
            assertEquals(7.0, calculator.add(7.0, 0.0), 0.001);
        }
    }

    @Nested
    @DisplayName("Subtraction Tests")
    class SubtractionTests {

        @Test
        @DisplayName("should subtract two numbers")
        void testSubtract() {
            assertEquals(2.0, calculator.subtract(5.0, 3.0), 0.001);
        }

        @Test
        @DisplayName("should handle negative result")
        void testSubtractNegativeResult() {
            assertEquals(-3.0, calculator.subtract(2.0, 5.0), 0.001);
        }
    }

    @Nested
    @DisplayName("Multiplication Tests")
    class MultiplicationTests {

        @Test
        @DisplayName("should multiply two numbers")
        void testMultiply() {
            assertEquals(15.0, calculator.multiply(3.0, 5.0), 0.001);
        }

        @Test
        @DisplayName("should multiply by zero")
        void testMultiplyByZero() {
            assertEquals(0.0, calculator.multiply(5.0, 0.0), 0.001);
        }
    }

    @Nested
    @DisplayName("Division Tests")
    class DivisionTests {

        @Test
        @DisplayName("should divide two numbers")
        void testDivide() {
            assertEquals(2.5, calculator.divide(5.0, 2.0), 0.001);
        }

        @Test
        @DisplayName("should throw on division by zero")
        void testDivideByZero() {
            assertThrows(ArithmeticException.class, () -> calculator.divide(5.0, 0.0));
        }
    }

    @Nested
    @DisplayName("Factorial Tests")
    class FactorialTests {

        @Test
        @DisplayName("should compute factorial of 5")
        void testFactorial() {
            assertEquals(120, calculator.factorial(5));
        }

        @Test
        @DisplayName("should return 1 for factorial of 0")
        void testFactorialZero() {
            assertEquals(1, calculator.factorial(0));
        }

        @Test
        @DisplayName("should throw for negative input")
        void testFactorialNegative() {
            assertThrows(IllegalArgumentException.class, () -> calculator.factorial(-1));
        }
    }

    @Nested
    @DisplayName("Prime Check Tests")
    class PrimeTests {

        @Test
        @DisplayName("should identify primes")
        void testIsPrime() {
            assertTrue(calculator.isPrime(7));
            assertTrue(calculator.isPrime(13));
            assertTrue(calculator.isPrime(29));
        }

        @Test
        @DisplayName("should identify non-primes")
        void testIsNotPrime() {
            assertFalse(calculator.isPrime(1));
            assertFalse(calculator.isPrime(4));
            assertFalse(calculator.isPrime(15));
        }
    }

    @Nested
    @DisplayName("GCD Tests")
    class GCDTests {

        @Test
        @DisplayName("should compute GCD")
        void testGCD() {
            assertEquals(6, calculator.gcd(12, 18));
        }

        @Test
        @DisplayName("should handle coprime numbers")
        void testGCDCoprime() {
            assertEquals(1, calculator.gcd(7, 13));
        }
    }
}
"""
    write_file(f'{src_test}/CalculatorTest.java', calculator_test_java)

    # --- .vscode/settings.json for the project (minimal, no coverage config) ---
    vscode_project_dir = f'{PROJECT_DIR}/.vscode'
    create_directory(vscode_project_dir)
    project_settings = {
        "java.configuration.updateBuildConfiguration": "automatic"
    }
    write_file(f'{vscode_project_dir}/settings.json', json.dumps(project_settings, indent=4))

    print(f'Initial Maven project created at: {PROJECT_DIR}')

    # --- Install Java and Maven (required for the task) ---
    print('Installing Java JDK and Maven...')
    subprocess.run(
        'echo "password" | sudo -S apt-get update -qq 2>/dev/null',
        shell=True, capture_output=True, timeout=120
    )
    subprocess.run(
        'echo "password" | sudo -S apt-get install -y -qq default-jdk maven 2>/dev/null',
        shell=True, capture_output=True, timeout=300
    )
    # Verify installation
    mvn_check = subprocess.run(['mvn', '--version'], capture_output=True, text=True)
    print(f'Maven version: {mvn_check.stdout.splitlines()[0] if mvn_check.stdout else "NOT FOUND"}')

    # --- Ensure no coverage extension is installed ---
    # (Don't install any coverage extensions)

    # --- Launch VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
