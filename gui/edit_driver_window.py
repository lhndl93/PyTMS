import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime  # Import datetime

class EditDriverWindow:
    def __init__(self, app, driver):
        self.app = app
        self.driver = driver
        self.app.open_windows["edit_driver"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Edit Driver")
        self.window.geometry("400x300")

        def on_close():
            del self.app.open_windows["edit_driver"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Driver ID:").grid(row=0, column=0, padx=5, pady=5)
        self.driver_id = ttk.Entry(frame)
        self.driver_id.grid(row=0, column=1, padx=5, pady=5)
        self.driver_id.insert(0, self.driver['id'])

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name = ttk.Entry(frame)
        self.name.grid(row=1, column=1, padx=5, pady=5)
        self.name.insert(0, self.driver['name'])

        ttk.Label(frame, text="License Number:").grid(row=2, column=0, padx=5, pady=5)
        self.license_number = ttk.Entry(frame)
        self.license_number.grid(row=2, column=1, padx=5, pady=5)
        self.license_number.insert(0, self.driver['license_number'])

        ttk.Button(frame, text="Save Changes", command=self.save_changes).grid(row=3, columnspan=2, pady=10)

    def save_changes(self):
        try:
            old_driver = self.driver.copy()
            self.driver['id'] = self.driver_id.get().strip()
            self.driver['name'] = self.name.get().strip()
            self.driver['license_number'] = self.license_number.get().strip()

            if not self.driver['id'] or not self.driver['name'] or not self.license_number:
                raise ValueError("Invalid input: All fields are required.")

            new_driver = self.driver.copy()
            if self.driver['id'] not in self.app.data_store.edited_drivers:
                self.app.data_store.edited_drivers[self.driver['id']] = []
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.app.data_store.edited_drivers[self.driver['id']].append({"old": old_driver, "new": new_driver, "timestamp": timestamp})
            self.app.data_store.save_data()
            messagebox.showinfo("Success", "Driver updated successfully")
            self.app.open_windows["view_drivers"].refresh_drivers_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
