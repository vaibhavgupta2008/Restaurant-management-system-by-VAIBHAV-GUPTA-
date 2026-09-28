# 🍽️ Advanced Restaurant Management & POS Billing System

![Python](https://img.shields.io/badge/Python-3.x%20%7C%203.14-blue.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A feature-rich, lightweight, and modern **Point of Sale (POS) & Restaurant Billing Application** built using **Python** and **Tkinter**. This software provides a smooth, fast, and interactive desktop interface for taking customer orders, applying discounts, calculating GST, and generating print-ready receipts without requiring any external dependencies.
---

## 👨‍💻 Developer Brief & Credits

Designed and developed by **Vaibhav Gupta**.

- **Developer**: Vaibhav Gupta
- **Location**: Chhattisgarh, India
- **GitHub**: [@VAIBHAVGUPTA2008](https://github.com/VAIBHAVGUPTA2008)
- **LinkedIn**: [Vaibhav Gupta](https://www.linkedin.com/in/vaibhav-gupta-0819932b0/)
---

## 🌟 Key Highlights & Features

- **🎨 Modern Dark UI Theme**: Custom-styled interface built with `ttk` widgets and `Arial Black` typography.
- **🔍 Real-Time Menu Search**: Instant search filtering across all menu categories as you type.
- **🛒 Interactive Cart Table**: Powered by `Treeview` for real-time quantity adjustments, item removals, and automatic total calculations.
- **💰 Flexible Billing & Discounts**: Supports both percentage (`%`) and fixed amount (`₹`) discounts along with automatic **5% GST** calculation.
- **📝 Custom Order Notes**: Add specific customer requests or dietary notes directly onto the bill.
- **📄 Invoice Generation**: Generates clean, formatted `.txt` receipts saved automatically in the `/bills` folder with timestamp tracking.
- **⚡ Standard Library Only**: Zero external `pip` dependencies required—runs out of the box with built-in modules (`tkinter`, `json`, `os`, `datetime`, `random`).

---

## 🧩 System Architecture & Core Functions

The application is encapsulated within the `AdvancedBillingApp` class, managing GUI elements, state tracking, and billing operations:

### Core Functions Overview
- **`build_ui()`**: Constructs the multi-pane interface including customer details, dynamic menu tabs, search bar, cart table, and summary widgets.
- **`populate_category_tab()`**: Populates category tabs (`Starters`, `Main Course`, `Snacks & Drinks`) dynamically from the menu dictionary.
- **`filter_menu()`**: Real-time filtering function that shows or hides menu items based on current search input.
- **`add_to_cart()`, `increase_selected()`, `decrease_selected()`, `remove_selected()`**: Manages cart updates and keeps the order state synchronized.
- **`update_totals()`**: Auto-calculates Subtotal, 5% GST, applied discounts, and final Grand Total in real-time.
- **`generate_and_save_receipt()`**: Validates input data, formats the textual receipt layout, saves the file locally in `/bills`, and displays a popup preview.

---

## 📂 Project Structure

```text
restaurant-management-system/
│
├── RESTAURANT MANAGEMENT BY VAIBHAV GUPTA.py   # Main Python Application Script
├── README.md                                    # Project Documentation
└── bills/                                       # Auto-created folder for generated receipts (.txt)
