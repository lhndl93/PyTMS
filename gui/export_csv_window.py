import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog as fd
import csv

class ExportCSVWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["export"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Export to CSV")
        self.window.geometry("300x200")

        def on_close():
            del self.app.open_windows["export"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Select Destination").pack(pady=10)

        self.filepath = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=self.filepath, width=40)
        entry.pack(pady=5)

        ttk.Button(frame, text="Browse", command=self.browse).pack(pady=5)
        ttk.Button(frame, text="Export", command=self.export).pack(pady=5)

    def browse(self):
        file = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file:
            self.filepath.set(file)

    def export(self):
        filepath = self.filepath.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a destination file")
            return

        try:
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.app.data_store.settings["job_order"])
                for job in self.app.data_store.jobs:
                    writer.writerow([job[col] for col in self.app.data_store.settings["job_order"]])

            messagebox.showinfo("Success", "Data exported successfully")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
