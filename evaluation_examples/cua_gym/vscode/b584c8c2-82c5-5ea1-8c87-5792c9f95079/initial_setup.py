"""
Initial Setup: Set up workspace for a Java Spring Boot project
Task ID: vscode_we_088
Domain: vscode

Creates a Spring Boot project structure at ~/projects/spring-api/,
ensures VSCode settings are empty, and opens VSCode with the folder.
No Java extensions installed. No Java/Maven/Spring settings.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_088'

# Paths
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'spring-api')
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


def create_project_structure():
    """Create a realistic Spring Boot project directory structure."""
    # Main directories
    dirs = [
        'src/main/java/com/example/springapi/controller',
        'src/main/java/com/example/springapi/model',
        'src/main/java/com/example/springapi/service',
        'src/main/java/com/example/springapi/repository',
        'src/main/resources',
        'src/test/java/com/example/springapi',
        '.mvn/wrapper',
    ]
    for d in dirs:
        os.makedirs(os.path.join(PROJECT_DIR, d), exist_ok=True)

    # pom.xml
    pom_xml = '''<?xml version="1.0" encoding="UTF-8"?>
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
    <artifactId>spring-api</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>spring-api</name>
    <description>Customer Management REST API</description>
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
'''
    write_file(os.path.join(PROJECT_DIR, 'pom.xml'), pom_xml)

    # Main application class
    app_java = '''package com.example.springapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpringApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringApiApplication.class, args);
    }
}
'''
    write_file(os.path.join(PROJECT_DIR,
        'src/main/java/com/example/springapi/SpringApiApplication.java'), app_java)

    # Customer model
    model_java = '''package com.example.springapi.model;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String firstName;

    @Column(nullable = false)
    private String lastName;

    @Column(unique = true, nullable = false)
    private String email;

    private String phone;
    private LocalDate registrationDate;

    public Customer() {}

    public Customer(String firstName, String lastName, String email) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.registrationDate = LocalDate.now();
    }

    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public LocalDate getRegistrationDate() { return registrationDate; }
    public void setRegistrationDate(LocalDate registrationDate) { this.registrationDate = registrationDate; }
}
'''
    write_file(os.path.join(PROJECT_DIR,
        'src/main/java/com/example/springapi/model/Customer.java'), model_java)

    # Repository
    repo_java = '''package com.example.springapi.repository;

import com.example.springapi.model.Customer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    Optional<Customer> findByEmail(String email);
}
'''
    write_file(os.path.join(PROJECT_DIR,
        'src/main/java/com/example/springapi/repository/CustomerRepository.java'), repo_java)

    # Service
    service_java = '''package com.example.springapi.service;

import com.example.springapi.model.Customer;
import com.example.springapi.repository.CustomerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CustomerService {

    @Autowired
    private CustomerRepository customerRepository;

    public List<Customer> getAllCustomers() {
        return customerRepository.findAll();
    }

    public Optional<Customer> getCustomerById(Long id) {
        return customerRepository.findById(id);
    }

    public Customer createCustomer(Customer customer) {
        return customerRepository.save(customer);
    }

    public void deleteCustomer(Long id) {
        customerRepository.deleteById(id);
    }
}
'''
    write_file(os.path.join(PROJECT_DIR,
        'src/main/java/com/example/springapi/service/CustomerService.java'), service_java)

    # Controller
    controller_java = '''package com.example.springapi.controller;

import com.example.springapi.model.Customer;
import com.example.springapi.service.CustomerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/customers")
public class CustomerController {

    @Autowired
    private CustomerService customerService;

    @GetMapping
    public List<Customer> getAllCustomers() {
        return customerService.getAllCustomers();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Customer> getCustomerById(@PathVariable Long id) {
        return customerService.getCustomerById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Customer createCustomer(@RequestBody Customer customer) {
        return customerService.createCustomer(customer);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCustomer(@PathVariable Long id) {
        customerService.deleteCustomer(id);
        return ResponseEntity.noContent().build();
    }
}
'''
    write_file(os.path.join(PROJECT_DIR,
        'src/main/java/com/example/springapi/controller/CustomerController.java'), controller_java)

    # application.properties
    app_props = '''spring.application.name=spring-api
server.port=8080

# H2 Database Configuration
spring.datasource.url=jdbc:h2:mem:customersdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.h2.console.enabled=true

# JPA Settings
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
'''
    write_file(os.path.join(PROJECT_DIR,
        'src/main/resources/application.properties'), app_props)

    # Test class
    test_java = '''package com.example.springapi;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class SpringApiApplicationTests {

    @Test
    void contextLoads() {
    }
}
'''
    write_file(os.path.join(PROJECT_DIR,
        'src/test/java/com/example/springapi/SpringApiApplicationTests.java'), test_java)

    # .gitignore
    gitignore = '''target/
!.mvn/wrapper/maven-wrapper.jar
*.iml
.idea/
*.class
*.jar
*.war
*.log
.DS_Store
'''
    write_file(os.path.join(PROJECT_DIR, '.gitignore'), gitignore)

    # README
    readme = '''# Spring API - Customer Management

A simple REST API for managing customer records, built with Spring Boot 3.2 and Java 17.

## Endpoints

- `GET /api/customers` - List all customers
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers` - Create new customer
- `DELETE /api/customers/{id}` - Delete customer

## Running

```bash
./mvnw spring-boot:run
```
'''
    write_file(os.path.join(PROJECT_DIR, 'README.md'), readme)

    print(f'Project structure created at {PROJECT_DIR}')


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def setup_empty_vscode_settings():
    """Ensure VSCode user settings is empty {}."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Empty settings.json created at {SETTINGS_PATH}')


def ensure_no_java_extensions():
    """Uninstall any Java extensions if present."""
    result = subprocess.run(['code', '--list-extensions'], capture_output=True, text=True)
    extensions = result.stdout.strip().split('\n') if result.stdout.strip() else []
    java_exts = [e for e in extensions if 'java' in e.lower() or 'spring' in e.lower()]
    for ext in java_exts:
        subprocess.run(['code', '--uninstall-extension', ext], capture_output=True, text=True)
        print(f'Uninstalled: {ext}')
    if not java_exts:
        print('No Java extensions found (clean state)')


def main():
    # 1. Create project structure
    create_project_structure()

    # 2. Ensure empty VSCode settings
    setup_empty_vscode_settings()

    # 3. Ensure no Java extensions
    ensure_no_java_extensions()

    # 4. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print(f'GUI_READY: VSCode opened with {PROJECT_DIR}')


main()
