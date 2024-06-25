import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AddCustomerWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["add_customer"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Add Customer")
        self.window.geometry("400x400")

        def on_close():
            del self.app.open_windows["add_customer"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5)
        self.customer_id = ttk.Entry(frame)
        self.customer_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name = ttk.Entry(frame)
        self.name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Contact:").grid(row=2, column=0, padx=5, pady=5)
        self.contact = ttk.Entry(frame)
        self.contact.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.email = ttk.Entry(frame)
        self.email.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Address:").grid(row=4, column=0, padx=5, pady=5)
        self.address = ttk.Entry(frame)
        self.address.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Customer", command=self.add_customer).grid(row=5, columnspan=2, pady=10)

    def add_customer(self):
        try:
            customer_id = self.customer_id.get().strip()
            name = self.name.get().strip()
            contact = self.contact.get().strip()
            email = self.email.get().strip()
            address = self.address.get().strip()

            if not customer_id or not name or not contact or not email or not address:
                raise ValueError("Invalid input: All fields are required.")

            customer = {
                'id': customer_id,
                'name': name,
                'contact': contact,
                'email': email,
                'address': address
            }

            self.app.data_store.customers.append(customer)
            self.app.data_store.save_data()
            messagebox.showinfo("Success", "Customer added successfully")
            self.app.open_windows["view_customers"].refresh_customers_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
