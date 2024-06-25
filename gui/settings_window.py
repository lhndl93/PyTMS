import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class SettingsWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["settings"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Settings")
        self.window.geometry("400x300")

        def on_close():
            del self.app.open_windows["settings"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Date Format").grid(row=0, column=0, padx=5, pady=5)
        self.date_format = ttk.Entry(frame)
        self.date_format.grid(row=0, column=1, padx=5, pady=5)
        self.date_format.insert(0, self.app.data_store.settings["date_format"])

        ttk.Label(frame, text="Job Order").grid(row=1, column=0, padx=5, pady=5)
        self.job_order = ttk.Entry(frame)
        self.job_order.grid(row=1, column=1, padx=5, pady=5)
        self.job_order.insert(0, ','.join(self.app.data_store.settings["job_order"]))

        ttk.Button(frame, text="Save", command=self.save_settings).grid(row=2, columnspan=2, pady=10)

    def save_settings(self):
        date_format = self.date_format.get().strip()
        job_order = self.job_order.get().strip().split(',')

        if not date_format or not job_order:
            messagebox.showerror("Error", "All fields are required")
            return

        self.app.data_store.settings["date_format"] = date_format
        self.app.data_store.settings["job_order"] = [col.strip() for col in job_order]
        self.app.data_store.save_data()
        self.app.refresh_all_views()
        messagebox.showinfo("Success", "Settings saved successfully")
        self.window.destroy()
