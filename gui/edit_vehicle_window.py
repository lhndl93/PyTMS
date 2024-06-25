import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime  # Import datetime

class EditVehicleWindow:
    def __init__(self, app, vehicle):
        self.app = app
        self.vehicle = vehicle
        self.app.open_windows["edit_vehicle"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Edit Vehicle")
        self.window.geometry("400x400")

        def on_close():
            del self.app.open_windows["edit_vehicle"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Vehicle ID:").grid(row=0, column=0, padx=5, pady=5)
        self.vehicle_id = ttk.Entry(frame)
        self.vehicle_id.grid(row=0, column=1, padx=5, pady=5)
        self.vehicle_id.insert(0, self.vehicle['id'])

        ttk.Label(frame, text="Model:").grid(row=1, column=0, padx=5, pady=5)
        self.model = ttk.Entry(frame)
        self.model.grid(row=1, column=1, padx=5, pady=5)
        self.model.insert(0, self.vehicle['model'])

        ttk.Label(frame, text="License Plate:").grid(row=2, column=0, padx=5, pady=5)
        self.license_plate = ttk.Entry(frame)
        self.license_plate.grid(row=2, column=1, padx=5, pady=5)
        self.license_plate.insert(0, self.vehicle['license_plate'])

        ttk.Label(frame, text="Driver:").grid(row=3, column=0, padx=5, pady=5)
        self.driver = ttk.Combobox(frame, values=[driver['name'] for driver in self.app.data_store.drivers])
        self.driver.grid(row=3, column=1, padx=5, pady=5)
        self.driver.set(self.vehicle['driver'])

        ttk.Button(frame, text="Save Changes", command=self.save_changes).grid(row=4, columnspan=2, pady=10)

    def save_changes(self):
        try:
            old_vehicle = self.vehicle.copy()
            self.vehicle['id'] = self.vehicle_id.get().strip()
            self.vehicle['model'] = self.model.get().strip()
            self.vehicle['license_plate'] = self.license_plate.get().strip()
            self.vehicle['driver'] = self.driver.get().strip()

            if not self.vehicle['id'] or not self.vehicle['model'] or not self.vehicle['license_plate']:
                raise ValueError("Invalid input: All fields except driver are required.")

            new_vehicle = self.vehicle.copy()
            if self.vehicle['id'] not in self.app.data_store.edited_vehicles:
                self.app.data_store.edited_vehicles[self.vehicle['id']] = []
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.app.data_store.edited_vehicles[self.vehicle['id']].append({"old": old_vehicle, "new": new_vehicle, "timestamp": timestamp})
            self.app.data_store.save_data()
            messagebox.showinfo("Success", "Vehicle updated successfully")
            self.app.open_windows["view_vehicles"].refresh_vehicles_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
