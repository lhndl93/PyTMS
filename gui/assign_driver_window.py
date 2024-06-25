import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class AssignDriverWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["assign_driver"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Assign Driver to Vehicle")
        self.window.geometry("400x400")

        def on_close():
            del self.app.open_windows["assign_driver"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Vehicle:").grid(row=0, column=0, padx=5, pady=5)
        self.vehicle_combo = ttk.Combobox(frame, values=[vehicle['id'] for vehicle in self.app.data_store.vehicles])
        self.vehicle_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Driver:").grid(row=1, column=0, padx=5, pady=5)
        self.driver_combo = ttk.Combobox(frame, values=[driver['name'] for driver in self.app.data_store.drivers])
        self.driver_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Assign Driver", command=self.assign_driver).grid(row=2, columnspan=2, pady=10)

    def assign_driver(self):
        try:
            vehicle_id = self.vehicle_combo.get().strip()
            driver_name = self.driver_combo.get().strip()

            if not vehicle_id or not driver_name:
                raise ValueError("Invalid input: Both vehicle and driver must be selected.")

            vehicle = next((v for v in self.app.data_store.vehicles if v['id'] == vehicle_id), None)
            if not vehicle:
                raise ValueError("Vehicle not found.")

            old_driver = vehicle.get('driver', '')
            vehicle['driver'] = driver_name

            if vehicle_id not in self.app.data_store.edited_vehicles:
                self.app.data_store.edited_vehicles[vehicle_id] = []
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.app.data_store.edited_vehicles[vehicle_id].append({"old": old_driver, "new": driver_name, "timestamp": timestamp})
            self.app.data_store.save_data()
            messagebox.showinfo("Success", f"Driver {driver_name} assigned to vehicle {vehicle_id}")
            self.app.open_windows["view_vehicles"].refresh_vehicles_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
