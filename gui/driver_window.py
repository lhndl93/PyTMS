import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class DriverWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["view_drivers"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Drivers")
        self.window.geometry("800x600")

        def on_close():
            del self.app.open_windows["view_drivers"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        columns = self.app.data_store.settings["driver_order"]
        self.drivers_tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.drivers_tree.heading(col, text=col.replace('_', ' ').capitalize())
        self.drivers_tree.pack(fill='both', expand=True)

        self.refresh_drivers_list()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Add Driver", command=self.add_driver).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Edit Driver", command=self.edit_selected_driver).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Driver", command=self.delete_selected_driver).pack(side='left', padx=5)

    def refresh_drivers_list(self):
        for row in self.drivers_tree.get_children():
            self.drivers_tree.delete(row)
        for driver in self.app.data_store.drivers:
            self.drivers_tree.insert("", "end", values=[driver[col] for col in self.app.data_store.settings["driver_order"]])

    def add_driver(self):
        if "add_driver" in self.app.open_windows:
            self.app.open_windows["add_driver"].window.lift()
            return
        from .add_driver_window import AddDriverWindow
        AddDriverWindow(self.app)

    def edit_selected_driver(self):
        selected_item = self.drivers_tree.selection()
        if selected_item:
            idx = self.drivers_tree.index(selected_item)
            driver = self.app.data_store.drivers[idx]
            self.edit_driver(driver)
        else:
            messagebox.showerror("Error", "No driver selected. Please select a driver to edit.")

    def edit_driver(self, driver):
        if "edit_driver" in self.app.open_windows:
            self.app.open_windows["edit_driver"].window.lift()
            return
        from .edit_driver_window import EditDriverWindow
        EditDriverWindow(self.app, driver)

    def delete_selected_driver(self):
        selected_item = self.drivers_tree.selection()
        if selected_item:
            idx = self.drivers_tree.index(selected_item)
            driver = self.app.data_store.drivers[idx]
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete driver {driver['name']}?")
            if confirm:
                self.delete_driver(driver)
        else:
            messagebox.showerror("Error", "No driver selected. Please select a driver to delete.")

    def delete_driver(self, driver):
        self.app.data_store.drivers.remove(driver)
        self.app.data_store.save_data()
        self.refresh_drivers_list()
