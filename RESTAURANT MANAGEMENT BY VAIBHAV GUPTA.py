# Advanced Restaurant Management & POS Billing System
# Python 3.x / Python 3.14 compatible
# Uses standard library modules only: tkinter, json, os, datetime, random.

import datetime
import os
import random
import tkinter as tk
from tkinter import messagebox, ttk

MENU = {
    "Starters": [
        ("Samosa", 20.0),
        ("Paneer Tikka", 80.0),
        ("Chicken Tikka", 100.0),
        ("Veg Pakora", 30.0),
        ("Papdi Chaat", 40.0),
        ("Tomato Soup", 50.0),
        ("Masala Papad", 25.0),
    ],
    "Main Course": [
        ("Butter Chicken", 250.0),
        ("Pasta", 120.0),
        ("Rice", 90.0),
        ("Paneer Masala", 180.0),
        ("Palak Paneer", 160.0),
        ("Dal Makhani", 100.0),
        ("Chole Bhature", 150.0),
    ],
    "Snacks & Drinks": [
        ("Noodles", 80.0),
        ("Aloo Tikki", 40.0),
        ("Dahi Vada", 60.0),
        ("Pav Bhaji", 70.0),
        ("Bhel Puri", 35.0),
        ("Cold Coffee", 60.0),
        ("Masala Chai", 20.0),
    ],
}

TAX_RATE = 0.05  # 5% GST


class AdvancedBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("POS & Restaurant Management System v2.0")
        self.root.geometry("1400x820")
        self.root.minsize(1200, 700)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # State Variables
        self.bill_no = tk.StringVar(value=f"INV-{random.randint(10000, 99999)}")
        self.customer_name = tk.StringVar()
        self.phone = tk.StringVar()
        self.discount_val = tk.DoubleVar(value=0.0)
        self.discount_type = tk.StringVar(value="%")  # '%' or 'Fixed'
        self.order_notes = tk.StringVar()
        self.search_var = tk.StringVar()

        # Cart state: {item_name: {"price": float, "qty": int, "category": str}}
        self.cart = {}

        self.build_ui()
        self.update_totals()

    def configure_styles(self):
        self.root.configure(bg="#1E1E2E")
        
        # Colors
        BG_PRIMARY = "#1E1E2E"
        BG_SECONDARY = "#2B2B3C"
        ACCENT = "#7A52B3"
        TEXT_LIGHT = "#F8F8F2"

        self.style.configure(".", background=BG_PRIMARY, foreground=TEXT_LIGHT, font=("Segoe UI", 10))
        self.style.configure("TLabel", background=BG_PRIMARY, foreground=TEXT_LIGHT)
        self.style.configure("Header.TLabel", font=("Arial Black", 16, "bold"), foreground="#F1FA8C", background=BG_PRIMARY)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 11, "bold"), foreground="#8BE9FD")
        
        self.style.configure("TLabelframe", background=BG_SECONDARY, borderwidth=1, relief="solid")
        self.style.configure("TLabelframe.Label", background=BG_SECONDARY, foreground="#BD93F9", font=("Arial Black", 11, "bold"))
        
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background=ACCENT, foreground="#FFFFFF", borderwidth=0, padding=6)
        self.style.map("TButton", background=[("active", "#6272A4")])

        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, background="#282A36", fieldbackground="#282A36", foreground="#F8F8F2")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#44475A", foreground="#50FA7B")
        self.style.map("Treeview", background=[("selected", "#6272A4")])

    def build_ui(self):
        # Header Banner
        header = ttk.Label(self.root, text="RESTAURANT MANAGEMENT BY VAIBHAV GUPTA ", style="Header.TLabel", anchor="center")
        header.pack(fill="x", pady=(12, 6))

        # Top Bar: Customer Details (Font: Arial Black)
        cust_frame = ttk.LabelFrame(self.root, text=" Customer & Invoice Info ", padding=10)
        cust_frame.pack(fill="x", padx=12, pady=6)

        label_font = ("Arial Black", 10)
        entry_font = ("Arial Black", 10)

        tk.Label(cust_frame, text="Customer Name:", font=label_font, bg="#2B2B3C", fg="#F8F8F2").grid(row=0, column=0, padx=6, sticky="w")
        tk.Entry(cust_frame, textvariable=self.customer_name, font=entry_font, width=22, bg="#1E1E2E", fg="#50FA7B", insertbackground="white").grid(row=0, column=1, padx=6)

        tk.Label(cust_frame, text="Contact No:", font=label_font, bg="#2B2B3C", fg="#F8F8F2").grid(row=0, column=2, padx=6, sticky="w")
        tk.Entry(cust_frame, textvariable=self.phone, font=entry_font, width=18, bg="#1E1E2E", fg="#50FA7B", insertbackground="white").grid(row=0, column=3, padx=6)

        tk.Label(cust_frame, text="Invoice No:", font=label_font, bg="#2B2B3C", fg="#F8F8F2").grid(row=0, column=4, padx=6, sticky="w")
        tk.Entry(cust_frame, textvariable=self.bill_no, font=entry_font, width=16, state="readonly", bg="#1E1E2E", fg="#F1FA8C").grid(row=0, column=5, padx=6)

        # Main Content Layout
        main_pane = ttk.PanedWindow(self.root, orient="horizontal")
        main_pane.pack(fill="both", expand=True, padx=12, pady=6)

        # LEFT PANE: Menu & Search
        menu_container = ttk.LabelFrame(main_pane, text=" Menu Items ", padding=10)
        main_pane.add(menu_container, weight=3)

        # Search Box
        search_frame = ttk.Frame(menu_container)
        search_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(search_frame, text="Search Menu:", style="SubHeader.TLabel").pack(side="left", padx=(0, 6))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial Black", 10), bg="#282A36", fg="#F8F8F2", insertbackground="white")
        search_entry.pack(side="left", fill="x", expand=True)
        self.search_var.trace_add("write", lambda *args: self.filter_menu())

        # Category Tabs
        self.notebook = ttk.Notebook(menu_container)
        self.notebook.pack(fill="both", expand=True)

        self.tab_frames = {}
        for category in MENU:
            tab = ttk.Frame(self.notebook, padding=8)
            self.notebook.add(tab, text=category)
            self.tab_frames[category] = tab
            self.populate_category_tab(tab, category)

        # RIGHT PANE: Interactive Cart & Order Summary
        cart_container = ttk.LabelFrame(main_pane, text=" Current Order ", padding=10)
        main_pane.add(cart_container, weight=2)

        # Cart Table
        columns = ("Item", "Price", "Qty", "Total")
        self.cart_tree = ttk.Treeview(cart_container, columns=columns, show="headings", height=10)
        self.cart_tree.heading("Item", text="Item Name")
        self.cart_tree.heading("Price", text="Price (₹)")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Total", text="Total (₹)")

        self.cart_tree.column("Item", width=140)
        self.cart_tree.column("Price", width=70, anchor="e")
        self.cart_tree.column("Qty", width=50, anchor="center")
        self.cart_tree.column("Total", width=80, anchor="e")

        self.cart_tree.pack(fill="both", expand=True)

        # Item Action Controls
        cart_btn_frame = ttk.Frame(cart_container)
        cart_btn_frame.pack(fill="x", pady=6)
        ttk.Button(cart_btn_frame, text=" + Increase Qty ", command=self.increase_selected).pack(side="left", padx=2)
        ttk.Button(cart_btn_frame, text=" - Decrease Qty ", command=self.decrease_selected).pack(side="left", padx=2)
        ttk.Button(cart_btn_frame, text=" Remove Item ", command=self.remove_selected).pack(side="right", padx=2)

        # Order Modifiers (Discounts & Notes)
        mod_frame = ttk.Frame(cart_container)
        mod_frame.pack(fill="x", pady=6)

        tk.Label(mod_frame, text="Discount:", font=("Arial Black", 9), bg="#2B2B3C", fg="#F8F8F2").grid(row=0, column=0, sticky="w")
        tk.Entry(mod_frame, textvariable=self.discount_val, font=("Arial Black", 9), width=8, bg="#1E1E2E", fg="#F8F8F2", insertbackground="white").grid(row=0, column=1, padx=4)
        
        disc_type_combo = ttk.Combobox(mod_frame, textvariable=self.discount_type, values=["%", "₹"], width=3, state="readonly")
        disc_type_combo.grid(row=0, column=2, padx=2)
        disc_type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_totals())
        self.discount_val.trace_add("write", lambda *args: self.update_totals())

        tk.Label(mod_frame, text="Note:", font=("Arial Black", 9), bg="#2B2B3C", fg="#F8F8F2").grid(row=0, column=3, padx=(10, 2), sticky="w")
        tk.Entry(mod_frame, textvariable=self.order_notes, font=("Arial Black", 9), width=16, bg="#1E1E2E", fg="#F8F8F2", insertbackground="white").grid(row=0, column=4, sticky="we")

        # Summary Display Frame
        self.summary_frame = ttk.Frame(cart_container, padding=6)
        self.summary_frame.pack(fill="x", pady=6)

        self.lbl_subtotal = tk.Label(self.summary_frame, text="Subtotal: ₹0.00", font=("Arial Black", 10), bg="#2B2B3C", fg="#F8F8F2")
        self.lbl_subtotal.pack(anchor="e")
        self.lbl_tax = tk.Label(self.summary_frame, text="GST (5%): ₹0.00", font=("Arial Black", 9), bg="#2B2B3C", fg="#F8F8F2")
        self.lbl_tax.pack(anchor="e")
        self.lbl_discount = tk.Label(self.summary_frame, text="Discount: -₹0.00", font=("Arial Black", 9), bg="#2B2B3C", fg="#FF5555")
        self.lbl_discount.pack(anchor="e")
        self.lbl_grand = tk.Label(self.summary_frame, text="GRAND TOTAL: ₹0.00", font=("Arial Black", 12), bg="#2B2B3C", fg="#50FA7B")
        self.lbl_grand.pack(anchor="e", pady=(4, 0))

        # Bottom Action Bar
        bottom_bar = ttk.Frame(self.root, padding=8)
        bottom_bar.pack(fill="x", padx=12, pady=(0, 10))

        ttk.Button(bottom_bar, text="CLEAR ORDER", command=self.clear_order).pack(side="left", padx=4)
        ttk.Button(bottom_bar, text="SAVE & PRINT RECEIPT", command=self.generate_and_save_receipt).pack(side="right", padx=4)
        ttk.Button(bottom_bar, text="EXIT APP", command=self.root.destroy).pack(side="right", padx=4)

    def populate_category_tab(self, parent, category):
        canvas = tk.Canvas(parent, bg="#2B2B3C", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for item_name, price in MENU[category]:
            item_row = ttk.Frame(scroll_frame, padding=4)
            item_row.pack(fill="x", expand=True, pady=2)

            lbl_text = f"{item_name}  —  ₹{price:.2f}"
            ttk.Label(item_row, text=lbl_text, font=("Segoe UI", 10)).pack(side="left", padx=6)

            btn = ttk.Button(item_row, text="+ Add", command=lambda n=item_name, p=price, c=category: self.add_to_cart(n, p, c))
            btn.pack(side="right", padx=6)

    def filter_menu(self):
        query = self.search_var.get().lower().strip()
        for category, tab_frame in self.tab_frames.items():
            for child in tab_frame.winfo_children():
                if isinstance(child, tk.Canvas):
                    scroll_frame = child.winfo_children()[0]
                    for row in scroll_frame.winfo_children():
                        label = row.winfo_children()[0]
                        text = label.cget("text").lower()
                        if query in text:
                            row.pack(fill="x", expand=True, pady=2)
                        else:
                            row.pack_forget()

    def add_to_cart(self, name, price, category):
        if name in self.cart:
            self.cart[name]["qty"] += 1
        else:
            self.cart[name] = {"price": price, "qty": 1, "category": category}
        self.refresh_cart_tree()

    def refresh_cart_tree(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        for name, data in self.cart.items():
            total = data["price"] * data["qty"]
            self.cart_tree.insert("", "end", iid=name, values=(name, f"{data['price']:.2f}", data["qty"], f"{total:.2f}"))

        self.update_totals()

    def get_selected_cart_item(self):
        selected = self.cart_tree.selection()
        if selected:
            return selected[0]
        return None

    def increase_selected(self):
        item = self.get_selected_cart_item()
        if item and item in self.cart:
            self.cart[item]["qty"] += 1
            self.refresh_cart_tree()

    def decrease_selected(self):
        item = self.get_selected_cart_item()
        if item and item in self.cart:
            if self.cart[item]["qty"] > 1:
                self.cart[item]["qty"] -= 1
            else:
                del self.cart[item]
            self.refresh_cart_tree()

    def remove_selected(self):
        item = self.get_selected_cart_item()
        if item and item in self.cart:
            del self.cart[item]
            self.refresh_cart_tree()

    def update_totals(self):
        subtotal = sum(data["price"] * data["qty"] for data in self.cart.values())
        tax = subtotal * TAX_RATE

        try:
            disc_input = float(self.discount_val.get())
        except ValueError:
            disc_input = 0.0

        if self.discount_type.get() == "%":
            discount_amount = (subtotal * disc_input) / 100.0
        else:
            discount_amount = disc_input

        discount_amount = min(discount_amount, subtotal + tax)
        grand_total = max(0.0, (subtotal + tax) - discount_amount)

        self.lbl_subtotal.config(text=f"Subtotal: ₹{subtotal:.2f}")
        self.lbl_tax.config(text=f"GST (5%): ₹{tax:.2f}")
        self.lbl_discount.config(text=f"Discount: -₹{discount_amount:.2f}")
        self.lbl_grand.config(text=f"GRAND TOTAL: ₹{grand_total:.2f}")

        return subtotal, tax, discount_amount, grand_total

    def generate_and_save_receipt(self):
        name = self.customer_name.get().strip()
        phone = self.phone.get().strip()

        if not name or not phone:
            messagebox.showerror("Missing Information", "Please enter Customer Name and Contact Number.")
            return

        if not self.cart:
            messagebox.showwarning("Empty Order", "Please add at least one item to the order.")
            return

        subtotal, tax, discount, grand_total = self.update_totals()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format Text Receipt with Updated Restaurant Name and Address
        receipt = []
        receipt.append("==========================================")
        receipt.append(" RESTAURANT MANAGEMENT BY VAIBHAV GUPTA  ")
        receipt.append("         VAIBHAVGUPTA2008, CHHATISGARH         ")
        receipt.append("           Phone: +91 XXXXXXXXXX7         ")
        receipt.append("==========================================")
        receipt.append(f"Invoice No : {self.bill_no.get()}")
        receipt.append(f"Date/Time  : {now}")
        receipt.append(f"Customer   : {name}")
        receipt.append(f"Contact    : {phone}")
        if self.order_notes.get().strip():
            receipt.append(f"Notes      : {self.order_notes.get().strip()}")
        receipt.append("------------------------------------------")
        receipt.append(f"{'Item':<18} {'Qty':<4} {'Price':<8} {'Total':<8}")
        receipt.append("------------------------------------------")

        for item_name, data in self.cart.items():
            item_total = data["price"] * data["qty"]
            receipt.append(f"{item_name[:17]:<18} {data['qty']:<4} {data['price']:<8.2f} {item_total:<8.2f}")

        receipt.append("------------------------------------------")
        receipt.append(f"{'Subtotal':<30}: ₹{subtotal:.2f}")
        receipt.append(f"{'GST (5%)':<30}: ₹{tax:.2f}")
        receipt.append(f"{'Discount':<30}: -₹{discount:.2f}")
        receipt.append("==========================================")
        receipt.append(f"{'GRAND TOTAL':<30}: ₹{grand_total:.2f}")
        receipt.append("==========================================")
        receipt.append("        Thank you for dining with us!     ")

        receipt_text = "\n".join(receipt)

        os.makedirs("bills", exist_ok=True)
        filename = f"bills/{self.bill_no.get()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(receipt_text)

        self.show_receipt_popup(receipt_text, filename)

    def show_receipt_popup(self, receipt_text, filename):
        popup = tk.Toplevel(self.root)
        popup.title(f"Receipt - {self.bill_no.get()}")
        popup.geometry("450x600")
        popup.configure(bg="#1E1E2E")

        txt = tk.Text(popup, font=("Consolas", 10), bg="#282A36", fg="#F8F8F2", wrap="none")
        txt.insert("1.0", receipt_text)
        txt.config(state="disabled")
        txt.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(popup, padding=6)
        btn_frame.pack(fill="x")

        ttk.Label(btn_frame, text=f"Saved to {filename}", font=("Segoe UI", 8)).pack(side="left")
        ttk.Button(btn_frame, text="Close & New Order", command=lambda: [popup.destroy(), self.clear_order()]).pack(side="right")

    def clear_order(self):
        self.cart.clear()
        self.customer_name.set("")
        self.phone.set("")
        self.discount_val.set(0.0)
        self.order_notes.set("")
        self.search_var.set("")
        self.bill_no.set(f"INV-{random.randint(10000, 99999)}")
        self.refresh_cart_tree()


def main():
    root = tk.Tk()
    AdvancedBillingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
