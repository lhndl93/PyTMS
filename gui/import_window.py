import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog as fd

class ImportWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["import"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Import Data")
        self.window.geometry("400x200")

        def on_close():
            del self.app.open_windows["import"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Select Data Type:").grid(row=0, column=0, padx=5, pady=5)
        self.data_type = ttk.Combobox(frame, values=["Jobs", "Customers", "Vehicles", "Drivers"])
        self.data_type.grid(row=0, column=1, padx=5, pady=5)
        self.data_type.set("Jobs")

        ttk.Button(frame, text="Browse", command=self.browse_file).grid(row=1, columnspan=2, pady=10)

    def browse_file(self):
        file_path = fd.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.import_data(file_path)

    def import_data(self, file_path):
        data_type = self.data_type.get().lower()
        try:
            if data_type == "jobs":
                self.app.data_store.load_jobs_from_csv(file_path)
            elif data_type == "customers":
                self.app.data_store.load_customers_from_csv(file_path)
            elif data_type == "vehicles":
                self.app.data_store.load_vehicles_from_csv(file_path)
            elif data_type == "drivers":
                self.app.data_store.load_drivers_from_csv(file_path)
            self.app.refresh_all_views()
            messagebox.showinfo("Success", f"{data_type.capitalize()} imported successfully")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while importing {data_type}: {str(e)}")
