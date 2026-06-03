"""
Initial Setup: Configure Java import organization settings in VSCode
Task ID: vscode_lang_059
Domain: libreoffice_calc (actually vscode)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_059'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'java-project')


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


def create_java_project():
    """Create a realistic Java project with unorganized imports."""
    src_dir = os.path.join(PROJECT_DIR, 'src', 'main', 'java', 'com', 'acme', 'inventory')
    os.makedirs(src_dir, exist_ok=True)

    # Main application file with unorganized imports
    main_java = os.path.join(src_dir, 'InventoryManager.java')
    with open(main_java, 'w') as f:
        f.write('''package com.acme.inventory;

import java.util.ArrayList;
import com.acme.inventory.model.Product;
import javax.swing.JFrame;
import java.io.File;
import org.slf4j.Logger;
import java.util.HashMap;
import javax.swing.JPanel;
import com.acme.inventory.service.StockService;
import org.slf4j.LoggerFactory;
import java.util.List;
import javax.swing.JButton;
import java.io.IOException;
import com.acme.inventory.dao.ProductDAO;
import org.apache.commons.lang3.StringUtils;
import java.util.Map;
import javax.swing.JLabel;
import java.text.SimpleDateFormat;

/**
 * Main inventory management application for Acme Corp warehouse system.
 * Handles product tracking, stock levels, and reorder notifications.
 *
 * @author Sarah Chen
 * @version 2.3.1
 */
public class InventoryManager {

    private static final Logger logger = LoggerFactory.getLogger(InventoryManager.class);

    private final Map<String, Product> productCache;
    private final List<String> recentTransactions;
    private final StockService stockService;
    private final ProductDAO productDAO;

    public InventoryManager() {
        this.productCache = new HashMap<>();
        this.recentTransactions = new ArrayList<>();
        this.stockService = new StockService();
        this.productDAO = new ProductDAO();
        logger.info("InventoryManager initialized successfully");
    }

    public void addProduct(String sku, String name, double price, int quantity) {
        if (StringUtils.isBlank(sku) || StringUtils.isBlank(name)) {
            throw new IllegalArgumentException("SKU and name must not be blank");
        }
        Product product = new Product(sku, name, price, quantity);
        productCache.put(sku, product);
        productDAO.save(product);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String timestamp = sdf.format(new java.util.Date());
        recentTransactions.add(String.format("[%s] Added: %s (%s)", timestamp, name, sku));
        logger.info("Product added: {} - {}", sku, name);
    }

    public Product getProduct(String sku) {
        return productCache.getOrDefault(sku, productDAO.findBySku(sku));
    }

    public List<Product> getLowStockProducts(int threshold) {
        List<Product> lowStock = new ArrayList<>();
        for (Product p : productCache.values()) {
            if (p.getQuantity() < threshold) {
                lowStock.add(p);
            }
        }
        return lowStock;
    }

    public void exportInventoryReport(File outputFile) throws IOException {
        logger.info("Exporting inventory report to: {}", outputFile.getAbsolutePath());
        // Report generation logic
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Acme Inventory Manager v2.3.1");
        JPanel mainPanel = new JPanel();
        JButton refreshBtn = new JButton("Refresh Stock");
        JLabel statusLabel = new JLabel("Ready");

        mainPanel.add(refreshBtn);
        mainPanel.add(statusLabel);
        frame.add(mainPanel);
        frame.setSize(800, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);

        InventoryManager manager = new InventoryManager();
        logger.info("Application started");
    }
}
''')

    # Model class
    model_dir = os.path.join(src_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, 'Product.java'), 'w') as f:
        f.write('''package com.acme.inventory.model;

import java.io.Serializable;
import java.time.LocalDateTime;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Column;
import org.apache.commons.lang3.builder.ToStringBuilder;

/**
 * Represents a product in the Acme warehouse inventory system.
 */
@Entity
public class Product implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    private String sku;

    @Column(nullable = false)
    private String name;

    private double price;
    private int quantity;
    private LocalDateTime lastUpdated;

    public Product() {}

    public Product(String sku, String name, double price, int quantity) {
        this.sku = sku;
        this.name = name;
        this.price = price;
        this.quantity = quantity;
        this.lastUpdated = LocalDateTime.now();
    }

    public String getSku() { return sku; }
    public String getName() { return name; }
    public double getPrice() { return price; }
    public int getQuantity() { return quantity; }
    public LocalDateTime getLastUpdated() { return lastUpdated; }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
        this.lastUpdated = LocalDateTime.now();
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this)
            .append("sku", sku)
            .append("name", name)
            .append("price", price)
            .append("quantity", quantity)
            .toString();
    }
}
''')

    # Service class
    service_dir = os.path.join(src_dir, 'service')
    os.makedirs(service_dir, exist_ok=True)
    with open(os.path.join(service_dir, 'StockService.java'), 'w') as f:
        f.write('''package com.acme.inventory.service;

import java.util.List;
import com.acme.inventory.model.Product;
import com.acme.inventory.dao.ProductDAO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Service layer for stock management operations.
 */
public class StockService {

    private static final Logger logger = LoggerFactory.getLogger(StockService.class);
    private final ProductDAO dao;

    public StockService() {
        this.dao = new ProductDAO();
    }

    public boolean checkAvailability(String sku, int requestedQty) {
        Product product = dao.findBySku(sku);
        if (product == null) {
            logger.warn("Product not found: {}", sku);
            return false;
        }
        return product.getQuantity() >= requestedQty;
    }

    public void restock(String sku, int additionalQty) {
        Product product = dao.findBySku(sku);
        if (product != null) {
            product.setQuantity(product.getQuantity() + additionalQty);
            dao.save(product);
            logger.info("Restocked {} by {} units", sku, additionalQty);
        }
    }
}
''')

    # DAO class
    dao_dir = os.path.join(src_dir, 'dao')
    os.makedirs(dao_dir, exist_ok=True)
    with open(os.path.join(dao_dir, 'ProductDAO.java'), 'w') as f:
        f.write('''package com.acme.inventory.dao;

import com.acme.inventory.model.Product;
import java.util.HashMap;
import java.util.Map;

/**
 * Data access object for Product entities.
 * Currently uses in-memory storage; will migrate to JPA in v3.0.
 */
public class ProductDAO {

    private final Map<String, Product> store = new HashMap<>();

    public void save(Product product) {
        store.put(product.getSku(), product);
    }

    public Product findBySku(String sku) {
        return store.get(sku);
    }

    public void delete(String sku) {
        store.remove(sku);
    }
}
''')


def setup_vscode_settings():
    """Set up VSCode with basic settings but NO java import organization."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Add some basic Java development settings (but NOT import organization)
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.renderWhitespace": "boundary",
        "java.home": "/usr/lib/jvm/java-17-openjdk-amd64",
        "java.configuration.updateBuildConfiguration": "automatic",
        "java.debug.settings.hotCodeReplace": "auto",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    # Ensure NO java import organization settings exist
    settings.pop("java.sources.organizeImports.starThreshold", None)
    settings.pop("java.sources.organizeImports.staticStarThreshold", None)
    # Remove any [java] language-specific section with codeActionsOnSave
    settings.pop("[java]", None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written to: {SETTINGS_PATH}')


def main():
    create_java_project()
    print(f'Java project created at: {PROJECT_DIR}')

    setup_vscode_settings()

    # Open VSCode with the Java project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with Java project and DISPLAY=:0')


main()
