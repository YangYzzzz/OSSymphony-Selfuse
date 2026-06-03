"""
Initial Setup: Configure Java compiler settings in VSCode
Task ID: vscode_lang_070
Domain: vscode

Creates a Java 17 Maven project with code using preview features (pattern matching
in switch), but WITHOUT any Java compiler configuration in VSCode settings.
The preview features will show errors until the agent configures them.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_070'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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


def create_project():
    """Create Java Maven project structure."""
    src_dir = f'{PROJECT_DIR}/src/main/java/com/example'
    os.makedirs(src_dir, exist_ok=True)

    # pom.xml - Java 17 but NO --enable-preview
    pom_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>inventory-service</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Inventory Service</name>
    <description>Warehouse inventory management microservice</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.10.1</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>2.0.9</version>
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
        </plugins>
    </build>
</project>
'''
    with open(f'{PROJECT_DIR}/pom.xml', 'w') as f:
        f.write(pom_xml)

    # Main Java file using pattern matching in switch (preview feature)
    app_java = '''package com.example;

import java.util.List;
import java.util.ArrayList;

/**
 * Inventory Service - manages warehouse stock items.
 * Uses Java 17 preview features: pattern matching for switch expressions.
 */
public class App {

    sealed interface InventoryItem permits RawMaterial, FinishedGood, Packaging {}

    record RawMaterial(String sku, String name, double weightKg, String supplier) implements InventoryItem {}
    record FinishedGood(String sku, String name, int quantity, double unitPrice) implements InventoryItem {}
    record Packaging(String sku, String material, int count) implements InventoryItem {}

    /**
     * Calculate the total value of an inventory item.
     * Uses pattern matching for switch (Java 17 preview feature).
     */
    public static double calculateValue(InventoryItem item) {
        return switch (item) {
            case RawMaterial rm -> rm.weightKg() * 12.50;
            case FinishedGood fg -> fg.quantity() * fg.unitPrice();
            case Packaging pk -> pk.count() * 0.35;
        };
    }

    /**
     * Generate a human-readable label for an inventory item.
     * Uses pattern matching for switch (Java 17 preview feature).
     */
    public static String formatLabel(InventoryItem item) {
        return switch (item) {
            case RawMaterial rm -> String.format("[RAW] %s - %.1fkg from %s",
                    rm.name(), rm.weightKg(), rm.supplier());
            case FinishedGood fg -> String.format("[FIN] %s - %d units @ $%.2f",
                    fg.name(), fg.quantity(), fg.unitPrice());
            case Packaging pk -> String.format("[PKG] %s - %d pieces",
                    pk.material(), pk.count());
        };
    }

    /**
     * Categorize items by type and return summary.
     */
    public static String categorySummary(List<InventoryItem> items) {
        int rawCount = 0, finishedCount = 0, packagingCount = 0;
        double totalValue = 0.0;

        for (InventoryItem item : items) {
            switch (item) {
                case RawMaterial rm -> rawCount++;
                case FinishedGood fg -> finishedCount++;
                case Packaging pk -> packagingCount++;
            }
            totalValue += calculateValue(item);
        }

        return String.format(
            "Inventory Summary: %d raw materials, %d finished goods, %d packaging items. Total value: $%.2f",
            rawCount, finishedCount, packagingCount, totalValue
        );
    }

    public static void main(String[] args) {
        List<InventoryItem> inventory = new ArrayList<>();
        inventory.add(new RawMaterial("RM-001", "Steel Sheet", 250.0, "ArcelorMittal"));
        inventory.add(new RawMaterial("RM-002", "Copper Wire", 45.5, "Freeport-McMoRan"));
        inventory.add(new FinishedGood("FG-101", "Circuit Board A", 500, 24.99));
        inventory.add(new FinishedGood("FG-102", "Power Supply Unit", 120, 89.50));
        inventory.add(new Packaging("PK-201", "Cardboard Box Large", 2000));
        inventory.add(new Packaging("PK-202", "Bubble Wrap Roll", 350));

        System.out.println("=== Warehouse Inventory Report ===");
        System.out.println();

        for (InventoryItem item : inventory) {
            System.out.printf("  %s  ->  Value: $%.2f%n", formatLabel(item), calculateValue(item));
        }

        System.out.println();
        System.out.println(categorySummary(inventory));
    }
}
'''
    with open(f'{src_dir}/App.java', 'w') as f:
        f.write(app_java)

    print(f'Java project created at: {PROJECT_DIR}')


def setup_vscode_settings():
    """Set up VSCode settings WITHOUT any Java compiler configuration."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings if any
    settings = {}
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Basic VSCode settings - NO java.configuration.runtimes, NO nullAnalysis
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.renderWhitespace": "selection",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "java.jdt.ls.vmargs": "-Xmx1G",
    })

    # Explicitly remove any Java compiler settings if they exist
    settings.pop("java.configuration.runtimes", None)
    settings.pop("java.compile.nullAnalysis.mode", None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written to: {SETTINGS_PATH}')


def main():
    create_project()
    setup_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
