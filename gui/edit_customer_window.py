import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class EditCustomerWindow:
    def __init__(self, app, customer):
        self.app = app
        self.customer = customer
        self.app.open_windows["edit_customer"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Edit Customer")
        self.window.geometry("400x400")

        def on_close():
            del self.app.open_windows["edit_customer"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5)
        self.customer_id = ttk.Entry(frame)
        self.customer_id.grid(row=0, column=1, padx=5, pady=5)
        self.customer_id.insert(0, self.customer['id'])

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name = ttk.Entry(frame)
        self.name.grid(row=1, column=1, padx=5, pady=5)
        self.name.insert(0, self.customer['name'])

        ttk.Label(frame, text="Contact:").grid(row=2, column=0, padx=5, pady=5)
        self.contact = ttk.Entry(frame)
        self.contact.grid(row=2, column=1, padx=5, pady=5)
        self.contact.insert(0, self.customer['contact'])

        ttk.Label(frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.email = ttk.Entry(frame)
        self.email.grid(row=3, column=1, padx=5, pady=5)
        self.email.insert(0, self.customer['email'])

        ttk.Label(frame, text="Address:").grid(row=4, column=0, padx=5, pady=5)
        self.address = ttk.Entry(frame)
        self.address.grid(row=4, column=1, padx=5, pady=5)
        self.address.insert(0, self.customer['address'])

        ttk.Button(frame, text="Save Changes", command=self.save_changes).grid(row=5, columnspan=2, pady=10)

    def save_changes(self):
        try:
            self.customer['id'] = self.customer_id.get().strip()
            self.customer['name'] = self.name.get().strip()
            self.customer['contact'] = self.contact.get().strip()
            self.customer['email'] = self.email.get().strip()
            self.customer['address'] = self.address.get().strip()

            if not self.customer['id'] or not self.customer['name'] or not self.customer['contact'] or not self.customer['email'] or not self.customer['address']:
                raise ValueError("Invalid input: All fields are required.")

            self.app.data_store.save_data()
            messagebox.showinfo("Success", "Customer updated successfully")
            self.app.open_windows["view_customers"].refresh_customers_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
