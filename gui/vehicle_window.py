import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class VehicleWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["view_vehicles"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Vehicles")
        self.window.geometry("800x600")

        def on_close():
            del self.app.open_windows["view_vehicles"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        columns = self.app.data_store.settings["vehicle_order"]
        self.vehicles_tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.vehicles_tree.heading(col, text=col.replace('_', ' ').capitalize())
        self.vehicles_tree.pack(fill='both', expand=True)

        self.refresh_vehicles_list()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Add Vehicle", command=self.add_vehicle).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Edit Vehicle", command=self.edit_selected_vehicle).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Vehicle", command=self.delete_selected_vehicle).pack(side='left', padx=5)

    def refresh_vehicles_list(self):
        for row in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(row)
        for vehicle in self.app.data_store.vehicles:
            self.vehicles_tree.insert("", "end", values=[vehicle[col] for col in self.app.data_store.settings["vehicle_order"]])

    def add_vehicle(self):
        if "add_vehicle" in self.app.open_windows:
            self.app.open_windows["add_vehicle"].window.lift()
            return
        from .add_vehicle_window import AddVehicleWindow
        AddVehicleWindow(self.app)

    def edit_selected_vehicle(self):
        selected_item = self.vehicles_tree.selection()
        if selected_item:
            idx = self.vehicles_tree.index(selected_item)
            vehicle = self.app.data_store.vehicles[idx]
            self.edit_vehicle(vehicle)
        else:
            messagebox.showerror("Error", "No vehicle selected. Please select a vehicle to edit.")

    def edit_vehicle(self, vehicle):
        if "edit_vehicle" in self.app.open_windows:
            self.app.open_windows["edit_vehicle"].window.lift()
            return
        from .edit_vehicle_window import EditVehicleWindow
        EditVehicleWindow(self.app, vehicle)

    def delete_selected_vehicle(self):
        selected_item = self.vehicles_tree.selection()
        if selected_item:
            idx = self.vehicles_tree.index(selected_item)
            vehicle = self.app.data_store.vehicles[idx]
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete vehicle {vehicle['id']}?")
            if confirm:
                self.delete_vehicle(vehicle)
        else:
            messagebox.showerror("Error", "No vehicle selected. Please select a vehicle to delete.")

    def delete_vehicle(self, vehicle):
        self.app.data_store.vehicles.remove(vehicle)
        self.app.data_store.save_data()
        self.refresh_vehicles_list()
