"""
Initial Setup: Configure Java project with Lombok annotations (pre-task state)
Task ID: vscode_lang_067
Domain: vscode

Creates a Java project with Lombok-annotated source files. Lombok jar is present
in the classpath but the Lombok extension is NOT installed and lombokSupport is
NOT enabled in settings.json. This means the language server will show errors
for @Data, @Builder annotations.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_067'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
SRC_DIR = f'{PROJECT_DIR}/src/main/java/com/acme/inventory'
LIB_DIR = f'{PROJECT_DIR}/lib'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
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


def create_project():
    # Create directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(LIB_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(VSCODE_USER, exist_ok=True)

    # --- Create Java source files with Lombok annotations ---

    # Product.java - uses @Data and @Builder
    product_java = '''\
package com.acme.inventory;

import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
@Builder
public class Product {
    private Long id;
    private String name;
    private String sku;
    private String category;
    private BigDecimal unitPrice;
    private int quantityInStock;
    private int reorderLevel;
    private String warehouseLocation;
    private LocalDate lastRestocked;
    private boolean discontinued;
}
'''
    with open(f'{SRC_DIR}/Product.java', 'w') as f:
        f.write(product_java)

    # Supplier.java - uses @Data and @Builder
    supplier_java = '''\
package com.acme.inventory;

import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
public class Supplier {
    private Long id;
    private String companyName;
    private String contactPerson;
    private String email;
    private String phone;
    private String address;
    private List<String> productCategories;
    private double rating;
    private boolean preferredVendor;
}
'''
    with open(f'{SRC_DIR}/Supplier.java', 'w') as f:
        f.write(supplier_java)

    # InventoryService.java - uses the Lombok-generated methods
    service_java = '''\
package com.acme.inventory;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service class for managing warehouse inventory.
 * Relies on Lombok-generated getters, setters, and builders
 * from Product and Supplier classes.
 */
public class InventoryService {

    private final List<Product> products = new ArrayList<>();
    private final List<Supplier> suppliers = new ArrayList<>();

    public void addProduct(Product product) {
        products.add(product);
    }

    public void addSupplier(Supplier supplier) {
        suppliers.add(supplier);
    }

    /**
     * Find all products below their reorder level.
     */
    public List<Product> getProductsBelowReorderLevel() {
        return products.stream()
                .filter(p -> p.getQuantityInStock() < p.getReorderLevel())
                .collect(Collectors.toList());
    }

    /**
     * Calculate total inventory value across all non-discontinued products.
     */
    public BigDecimal calculateTotalInventoryValue() {
        return products.stream()
                .filter(p -> !p.isDiscontinued())
                .map(p -> p.getUnitPrice().multiply(BigDecimal.valueOf(p.getQuantityInStock())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    /**
     * Get all preferred suppliers for a given category.
     */
    public List<Supplier> getPreferredSuppliers(String category) {
        return suppliers.stream()
                .filter(Supplier::isPreferredVendor)
                .filter(s -> s.getProductCategories().contains(category))
                .collect(Collectors.toList());
    }

    /**
     * Create a sample product using the Builder pattern.
     */
    public static Product createSampleProduct() {
        return Product.builder()
                .id(1001L)
                .name("Industrial Servo Motor XR-500")
                .sku("ISM-XR500-BLK")
                .category("Automation Parts")
                .unitPrice(new BigDecimal("342.50"))
                .quantityInStock(47)
                .reorderLevel(20)
                .warehouseLocation("Aisle 7, Rack B3")
                .lastRestocked(LocalDate.of(2025, 11, 3))
                .discontinued(false)
                .build();
    }
}
'''
    with open(f'{SRC_DIR}/InventoryService.java', 'w') as f:
        f.write(service_java)

    # --- Create a dummy lombok.jar in lib/ (placeholder for classpath) ---
    # In a real project this would be the actual jar; here we create a minimal marker
    with open(f'{LIB_DIR}/lombok-1.18.30.jar', 'wb') as f:
        # Write a minimal ZIP (JAR) header so it looks like a real jar
        import zipfile
        import io
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as zf:
            zf.writestr('META-INF/MANIFEST.MF',
                        'Manifest-Version: 1.0\n'
                        'Implementation-Title: Lombok\n'
                        'Implementation-Version: 1.18.30\n')
        f.write(buf.getvalue())

    # --- Create .vscode/settings.json for the workspace (NO lombokSupport) ---
    workspace_settings = {
        "java.project.referencedLibraries": [
            "lib/**/*.jar"
        ],
        "java.project.sourcePaths": [
            "src/main/java"
        ],
        "editor.formatOnSave": True,
        "java.compile.nullAnalysis.mode": "automatic"
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(workspace_settings, f, indent=4)

    # --- Ensure user-level settings.json exists but does NOT have lombokSupport ---
    user_settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                user_settings = json.load(f)
        except (json.JSONDecodeError, ValueError):
            user_settings = {}

    # Make sure lombokSupport is NOT present
    user_settings.pop('java.jdt.ls.lombokSupport.enabled', None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(user_settings, f, indent=4)

    # --- Make sure Lombok extension is NOT installed ---
    subprocess.run(['code', '--uninstall-extension', 'vscjava.vscode-lombok'],
                   capture_output=True, timeout=30)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Source files: Product.java, Supplier.java, InventoryService.java')
    print(f'Lombok jar: {LIB_DIR}/lombok-1.18.30.jar')
    print(f'Workspace settings: {VSCODE_DIR}/settings.json')

    # --- Launch VSCode with the project folder ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Open the main service file to show errors
    launch_gui(f'code "{SRC_DIR}/InventoryService.java"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()
