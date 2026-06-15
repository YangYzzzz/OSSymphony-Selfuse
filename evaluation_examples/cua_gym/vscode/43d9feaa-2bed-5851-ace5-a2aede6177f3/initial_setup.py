"""
Initial Setup: Set up Spring Boot development environment in VSCode
Task ID: vscode_lang_058
Domain: vscode

Creates a Spring Boot Maven project at ~/projects/spring-app/ with:
- pom.xml with Spring Boot starter dependencies
- Main application class with @SpringBootApplication annotation
- Standard Maven directory structure
- NO Spring extensions installed
- NO launch.json (agent must create it)

Opens VSCode with the project folder.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_058'
PROJECT_DIR = f'{WORKDIR}/projects/spring-app'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
SRC_DIR = f'{PROJECT_DIR}/src/main/java/com/example/springapp'
RESOURCES_DIR = f'{PROJECT_DIR}/src/main/resources'
TEST_DIR = f'{PROJECT_DIR}/src/test/java/com/example/springapp'


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
    # Create directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(RESOURCES_DIR, exist_ok=True)
    os.makedirs(TEST_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- pom.xml ---
    pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.4</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>spring-app</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>spring-app</name>
    <description>Employee Management REST API</description>

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
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
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
    with open(f'{PROJECT_DIR}/pom.xml', 'w') as f:
        f.write(pom_xml.strip() + '\n')

    # --- Main Application Class ---
    main_class = """package com.example.springapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpringAppApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAppApplication.class, args);
    }
}
"""
    with open(f'{SRC_DIR}/SpringAppApplication.java', 'w') as f:
        f.write(main_class)

    # --- Employee Entity ---
    employee_entity = """package com.example.springapp;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private String department;
    private double salary;

    public Employee() {}

    public Employee(String firstName, String lastName, String email, String department, double salary) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.department = department;
        this.salary = salary;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getDepartment() { return department; }
    public void setDepartment(String department) { this.department = department; }
    public double getSalary() { return salary; }
    public void setSalary(double salary) { this.salary = salary; }
}
"""
    with open(f'{SRC_DIR}/Employee.java', 'w') as f:
        f.write(employee_entity)

    # --- Employee Repository ---
    employee_repo = """package com.example.springapp;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    List<Employee> findByDepartment(String department);
    List<Employee> findByLastNameContainingIgnoreCase(String lastName);
}
"""
    with open(f'{SRC_DIR}/EmployeeRepository.java', 'w') as f:
        f.write(employee_repo)

    # --- Employee Controller ---
    employee_controller = """package com.example.springapp;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    @Autowired
    private EmployeeRepository employeeRepository;

    @GetMapping
    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployeeById(@PathVariable Long id) {
        return employeeRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Employee createEmployee(@RequestBody Employee employee) {
        return employeeRepository.save(employee);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Employee> updateEmployee(@PathVariable Long id, @RequestBody Employee employee) {
        return employeeRepository.findById(id)
                .map(existing -> {
                    existing.setFirstName(employee.getFirstName());
                    existing.setLastName(employee.getLastName());
                    existing.setEmail(employee.getEmail());
                    existing.setDepartment(employee.getDepartment());
                    existing.setSalary(employee.getSalary());
                    return ResponseEntity.ok(employeeRepository.save(existing));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        if (employeeRepository.existsById(id)) {
            employeeRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }
}
"""
    with open(f'{SRC_DIR}/EmployeeController.java', 'w') as f:
        f.write(employee_controller)

    # --- application.properties ---
    app_properties = """# Spring Boot Application Configuration
spring.application.name=spring-app
server.port=8080

# H2 Database Configuration
spring.datasource.url=jdbc:h2:mem:employeedb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# JPA Configuration
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true

# H2 Console (for development)
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console

# Actuator endpoints
management.endpoints.web.exposure.include=health,info,metrics
"""
    with open(f'{RESOURCES_DIR}/application.properties', 'w') as f:
        f.write(app_properties)

    # --- Test class ---
    test_class = """package com.example.springapp;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class SpringAppApplicationTests {

    @Test
    void contextLoads() {
    }
}
"""
    with open(f'{TEST_DIR}/SpringAppApplicationTests.java', 'w') as f:
        f.write(test_class)

    # --- VSCode settings.json (basic Java settings, NO Spring Boot config) ---
    vscode_settings = {
        "java.configuration.updateBuildConfiguration": "automatic",
        "editor.tabSize": 4,
        "editor.formatOnSave": True
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # Ensure NO Spring extensions are installed (uninstall if present)
    subprocess.run(
        ["code", "--uninstall-extension", "vmware.vscode-boot-dev-pack"],
        capture_output=True, text=True
    )

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Main class: {SRC_DIR}/SpringAppApplication.java')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
