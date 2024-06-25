import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AddDriverWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["add_driver"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Add Driver")
        self.window.geometry("400x300")

        def on_close():
            del self.app.open_windows["add_driver"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Driver ID:").grid(row=0, column=0, padx=5, pady=5)
        self.driver_id = ttk.Entry(frame)
        self.driver_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name = ttk.Entry(frame)
        self.name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="License Number:").grid(row=2, column=0, padx=5, pady=5)
        self.license_number = ttk.Entry(frame)
        self.license_number.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Driver", command=self.add_driver).grid(row=3, columnspan=2, pady=10)

    def add_driver(self):
        try:
            driver_id = self.driver_id.get().strip()
            name = self.name.get().strip()
            license_number = self.license_number.get().strip()

            if not driver_id or not name or not license_number:
                raise ValueError("Invalid input: All fields are required.")

            driver = {
                'id': driver_id,
                'name': name,
                'license_number': license_number
            }

            self.app.data_store.drivers.append(driver)
            self.app.data_store.save_data()
            messagebox.showinfo("Success", "Driver added successfully")
            self.app.open_windows["view_drivers"].refresh_drivers_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
