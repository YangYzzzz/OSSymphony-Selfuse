"""
Initial Setup: Configure Java test runner for JUnit 5 integration tests
Task ID: vscode_lang_071
Domain: vscode

Creates a Java project with both unit tests and integration tests.
VSCode opens with default settings (no test filtering configured).
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_071'
PROJECT_DIR = f'{WORKDIR}/workspace'
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


def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    # --- Maven pom.xml ---
    pom_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>inventory-service</artifactId>
    <version>2.3.1</version>
    <packaging>jar</packaging>

    <name>Inventory Management Service</name>
    <description>Backend service for warehouse inventory tracking and order fulfillment</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <junit.jupiter.version>5.10.2</junit.jupiter.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>${junit.jupiter.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>${junit.jupiter.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-params</artifactId>
            <version>${junit.jupiter.version}</version>
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
        </plugins>
    </build>
</project>
'''
    create_file(f'{PROJECT_DIR}/pom.xml', pom_xml)

    # --- Main application classes ---
    app_java = '''package com.example;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Core inventory management application.
 * Handles product catalog operations and stock level tracking.
 */
public class App {
    private final Map<String, Product> catalog = new HashMap<>();
    private final Map<String, Integer> stockLevels = new HashMap<>();

    public void addProduct(String sku, String name, double price) {
        catalog.put(sku, new Product(sku, name, price));
        stockLevels.put(sku, 0);
    }

    public Optional<Product> findProduct(String sku) {
        return Optional.ofNullable(catalog.get(sku));
    }

    public void updateStock(String sku, int quantity) {
        if (!catalog.containsKey(sku)) {
            throw new IllegalArgumentException("Unknown SKU: " + sku);
        }
        stockLevels.merge(sku, quantity, Integer::sum);
    }

    public int getStockLevel(String sku) {
        return stockLevels.getOrDefault(sku, 0);
    }

    public List<Product> getLowStockProducts(int threshold) {
        List<Product> result = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : stockLevels.entrySet()) {
            if (entry.getValue() < threshold) {
                catalog.get(entry.getKey());
                result.add(catalog.get(entry.getKey()));
            }
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println("Inventory Service v2.3.1 started");
    }
}
'''
    create_file(f'{PROJECT_DIR}/src/main/java/com/example/App.java', app_java)

    product_java = '''package com.example;

/**
 * Represents a product in the inventory catalog.
 */
public record Product(String sku, String name, double price) {

    @Override
    public String toString() {
        return String.format("Product[%s: %s @ $%.2f]", sku, name, price);
    }
}
'''
    create_file(f'{PROJECT_DIR}/src/main/java/com/example/Product.java', product_java)

    order_service_java = '''package com.example;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Handles order processing and fulfillment workflows.
 */
public class OrderService {
    private final App inventory;
    private final List<Order> orderHistory = new ArrayList<>();

    public OrderService(App inventory) {
        this.inventory = inventory;
    }

    public Order placeOrder(String sku, int quantity) {
        int available = inventory.getStockLevel(sku);
        if (available < quantity) {
            throw new IllegalStateException(
                String.format("Insufficient stock for %s: requested %d, available %d",
                    sku, quantity, available));
        }
        inventory.updateStock(sku, -quantity);
        Order order = new Order(UUID.randomUUID().toString(), sku, quantity, LocalDateTime.now());
        orderHistory.add(order);
        return order;
    }

    public List<Order> getOrderHistory() {
        return List.copyOf(orderHistory);
    }

    public record Order(String id, String sku, int quantity, LocalDateTime timestamp) {}
}
'''
    create_file(f'{PROJECT_DIR}/src/main/java/com/example/OrderService.java', order_service_java)

    # --- Unit test files (*Test.java) ---
    app_test_java = '''package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the App inventory management class.
 */
@DisplayName("App Unit Tests")
class AppTest {

    private App app;

    @BeforeEach
    void setUp() {
        app = new App();
        app.addProduct("SKU-001", "Wireless Mouse", 29.99);
        app.addProduct("SKU-002", "Mechanical Keyboard", 89.50);
        app.addProduct("SKU-003", "USB-C Hub", 45.00);
    }

    @Test
    @DisplayName("should add product to catalog successfully")
    void testAddProduct() {
        app.addProduct("SKU-004", "Monitor Stand", 120.00);
        assertTrue(app.findProduct("SKU-004").isPresent());
    }

    @Test
    @DisplayName("should find existing product by SKU")
    void testFindProduct() {
        var product = app.findProduct("SKU-001");
        assertTrue(product.isPresent());
        assertEquals("Wireless Mouse", product.get().name());
    }

    @Test
    @DisplayName("should return empty for unknown SKU")
    void testFindProductNotFound() {
        var product = app.findProduct("UNKNOWN");
        assertTrue(product.isEmpty());
    }

    @Test
    @DisplayName("should update stock levels correctly")
    void testUpdateStock() {
        app.updateStock("SKU-001", 50);
        assertEquals(50, app.getStockLevel("SKU-001"));
        app.updateStock("SKU-001", -10);
        assertEquals(40, app.getStockLevel("SKU-001"));
    }

    @Test
    @DisplayName("should throw when updating stock for unknown SKU")
    void testUpdateStockUnknownSku() {
        assertThrows(IllegalArgumentException.class,
            () -> app.updateStock("INVALID", 10));
    }

    @Test
    @DisplayName("should identify low stock products")
    void testGetLowStockProducts() {
        app.updateStock("SKU-001", 3);
        app.updateStock("SKU-002", 15);
        app.updateStock("SKU-003", 2);
        var lowStock = app.getLowStockProducts(5);
        assertEquals(2, lowStock.size());
    }
}
'''
    create_file(f'{PROJECT_DIR}/src/test/java/com/example/AppTest.java', app_test_java)

    order_service_test_java = '''package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for OrderService.
 */
@DisplayName("OrderService Unit Tests")
class OrderServiceTest {

    private App app;
    private OrderService orderService;

    @BeforeEach
    void setUp() {
        app = new App();
        app.addProduct("SKU-101", "Laptop Stand", 55.00);
        app.updateStock("SKU-101", 20);
        orderService = new OrderService(app);
    }

    @Test
    @DisplayName("should place order and reduce stock")
    void testPlaceOrder() {
        var order = orderService.placeOrder("SKU-101", 3);
        assertNotNull(order.id());
        assertEquals(17, app.getStockLevel("SKU-101"));
    }

    @Test
    @DisplayName("should reject order when insufficient stock")
    void testPlaceOrderInsufficientStock() {
        assertThrows(IllegalStateException.class,
            () -> orderService.placeOrder("SKU-101", 25));
    }

    @Test
    @DisplayName("should maintain order history")
    void testOrderHistory() {
        orderService.placeOrder("SKU-101", 2);
        orderService.placeOrder("SKU-101", 5);
        assertEquals(2, orderService.getOrderHistory().size());
    }
}
'''
    create_file(f'{PROJECT_DIR}/src/test/java/com/example/OrderServiceTest.java', order_service_test_java)

    # --- Integration test files (*IntegrationTest.java) ---
    app_integration_test_java = '''package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Integration tests for the App class.
 * Tests cross-component interactions and end-to-end workflows.
 */
@DisplayName("App Integration Tests")
class AppIntegrationTest {

    private App app;

    @BeforeEach
    void setUp() {
        app = new App();
        // Set up a realistic product catalog
        app.addProduct("WH-1001", "Industrial Shelving Unit", 249.99);
        app.addProduct("WH-1002", "Packing Tape Dispenser", 12.50);
        app.addProduct("WH-1003", "Barcode Scanner", 189.00);
        app.addProduct("WH-1004", "Safety Goggles", 8.75);
        app.addProduct("WH-1005", "Forklift Battery", 450.00);

        // Initialize stock levels
        app.updateStock("WH-1001", 15);
        app.updateStock("WH-1002", 200);
        app.updateStock("WH-1003", 8);
        app.updateStock("WH-1004", 500);
        app.updateStock("WH-1005", 3);
    }

    @Test
    @DisplayName("should handle full inventory lifecycle")
    void testFullInventoryLifecycle() {
        // Add new product
        app.addProduct("WH-2001", "Pallet Jack", 320.00);
        assertEquals(0, app.getStockLevel("WH-2001"));

        // Receive shipment
        app.updateStock("WH-2001", 10);
        assertEquals(10, app.getStockLevel("WH-2001"));

        // Process outgoing orders
        app.updateStock("WH-2001", -3);
        assertEquals(7, app.getStockLevel("WH-2001"));

        // Verify product details persisted
        var product = app.findProduct("WH-2001");
        assertTrue(product.isPresent());
        assertEquals(320.00, product.get().price());
    }

    @Test
    @DisplayName("should correctly identify all low stock items across catalog")
    void testLowStockAcrossCatalog() {
        // WH-1005 has 3 units, WH-1003 has 8 units
        var lowStock = app.getLowStockProducts(10);
        assertEquals(2, lowStock.size());

        // Restock one item
        app.updateStock("WH-1005", 50);
        lowStock = app.getLowStockProducts(10);
        assertEquals(1, lowStock.size());
        assertEquals("Barcode Scanner", lowStock.get(0).name());
    }

    @Test
    @DisplayName("should maintain data integrity under concurrent-style operations")
    void testDataIntegrity() {
        // Simulate rapid stock updates
        for (int i = 0; i < 100; i++) {
            app.updateStock("WH-1002", 1);
        }
        assertEquals(300, app.getStockLevel("WH-1002"));

        // Deplete and verify
        app.updateStock("WH-1002", -300);
        assertEquals(0, app.getStockLevel("WH-1002"));
    }
}
'''
    create_file(f'{PROJECT_DIR}/src/test/java/com/example/AppIntegrationTest.java', app_integration_test_java)

    order_service_integration_test_java = '''package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Integration tests for the OrderService.
 * Verifies order processing with real inventory state.
 */
@DisplayName("OrderService Integration Tests")
class OrderServiceIntegrationTest {

    private App app;
    private OrderService orderService;

    @BeforeEach
    void setUp() {
        app = new App();
        app.addProduct("ORD-501", "Ergonomic Chair", 399.00);
        app.addProduct("ORD-502", "Standing Desk", 650.00);
        app.addProduct("ORD-503", "Desk Lamp", 45.00);
        app.updateStock("ORD-501", 30);
        app.updateStock("ORD-502", 12);
        app.updateStock("ORD-503", 75);
        orderService = new OrderService(app);
    }

    @Test
    @DisplayName("should process multiple orders and update inventory correctly")
    void testMultiOrderProcessing() {
        orderService.placeOrder("ORD-501", 5);
        orderService.placeOrder("ORD-502", 2);
        orderService.placeOrder("ORD-503", 10);

        assertEquals(25, app.getStockLevel("ORD-501"));
        assertEquals(10, app.getStockLevel("ORD-502"));
        assertEquals(65, app.getStockLevel("ORD-503"));
        assertEquals(3, orderService.getOrderHistory().size());
    }

    @Test
    @DisplayName("should prevent overselling across sequential orders")
    void testOversellProtection() {
        // First order succeeds
        orderService.placeOrder("ORD-502", 10);
        assertEquals(2, app.getStockLevel("ORD-502"));

        // Second order should fail - only 2 left
        assertThrows(IllegalStateException.class,
            () -> orderService.placeOrder("ORD-502", 5));

        // Stock unchanged after failed order
        assertEquals(2, app.getStockLevel("ORD-502"));
    }

    @Test
    @DisplayName("should track complete order history with timestamps")
    void testOrderHistoryTracking() {
        orderService.placeOrder("ORD-501", 1);
        orderService.placeOrder("ORD-503", 3);

        var history = orderService.getOrderHistory();
        assertEquals(2, history.size());
        assertNotNull(history.get(0).timestamp());
        assertEquals("ORD-501", history.get(0).sku());
        assertEquals("ORD-503", history.get(1).sku());
    }
}
'''
    create_file(f'{PROJECT_DIR}/src/test/java/com/example/OrderServiceIntegrationTest.java', order_service_integration_test_java)

    # --- Ensure VSCode settings exist but do NOT contain java test filtering ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any java test config if it exists (ensure clean initial state)
    keys_to_remove = [k for k in settings if k.startswith('java.test')]
    for k in keys_to_remove:
        del settings[k]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Settings file: {SETTINGS_PATH}')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
