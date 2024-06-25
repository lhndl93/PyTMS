import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CustomerWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["view_customers"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Customers")
        self.window.geometry("800x600")

        def on_close():
            del self.app.open_windows["view_customers"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        columns = self.app.data_store.settings["customer_order"]
        self.customers_tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.customers_tree.heading(col, text=col.replace('_', ' ').capitalize())
        self.customers_tree.pack(fill='both', expand=True)

        self.refresh_customers_list()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Add Customer", command=self.add_customer).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Edit Customer", command=self.edit_selected_customer).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Customer", command=self.delete_selected_customer).pack(side='left', padx=5)

    def refresh_customers_list(self):
        for row in self.customers_tree.get_children():
            self.customers_tree.delete(row)
        for customer in self.app.data_store.customers:
            self.customers_tree.insert("", "end", values=[customer[col] for col in self.app.data_store.settings["customer_order"]])

    def add_customer(self):
        if "add_customer" in self.app.open_windows:
            self.app.open_windows["add_customer"].focus()
            return
        from .add_customer_window import AddCustomerWindow
        AddCustomerWindow(self.app)

    def edit_selected_customer(self):
        selected_item = self.customers_tree.selection()
        if selected_item:
            idx = self.customers_tree.index(selected_item)
            customer = self.app.data_store.customers[idx]
            self.edit_customer(customer)
        else:
            messagebox.showerror("Error", "No customer selected. Please select a customer to edit.")

    def edit_customer(self, customer):
        if "edit_customer" in self.app.open_windows:
            self.app.open_windows["edit_customer"].focus()
            return
        from .edit_customer_window import EditCustomerWindow
        EditCustomerWindow(self.app, customer)

    def delete_selected_customer(self):
        selected_item = self.customers_tree.selection()
        if selected_item:
            idx = self.customers_tree.index(selected_item)
            customer = self.app.data_store.customers[idx]
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete customer {customer['name']}?")
            if confirm:
                self.delete_customer(customer)
        else:
            messagebox.showerror("Error", "No customer selected. Please select a customer to delete.")

    def delete_customer(self, customer):
        self.app.data_store.customers.remove(customer)
        self.app.data_store.save_data()
        self.refresh_customers_list()
