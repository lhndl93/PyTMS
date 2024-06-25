import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AddVehicleWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["add_vehicle"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Add Vehicle")
        self.window.geometry("400x400")

        def on_close():
            del self.app.open_windows["add_vehicle"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Vehicle ID:").grid(row=0, column=0, padx=5, pady=5)
        self.vehicle_id = ttk.Entry(frame)
        self.vehicle_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Model:").grid(row=1, column=0, padx=5, pady=5)
        self.model = ttk.Entry(frame)
        self.model.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="License Plate:").grid(row=2, column=0, padx=5, pady=5)
        self.license_plate = ttk.Entry(frame)
        self.license_plate.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Driver:").grid(row=3, column=0, padx=5, pady=5)
        self.driver = ttk.Combobox(frame, values=[driver['name'] for driver in self.app.data_store.drivers])
        self.driver.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Vehicle", command=self.add_vehicle).grid(row=4, columnspan=2, pady=10)

    def add_vehicle(self):
        try:
            vehicle_id = self.vehicle_id.get().strip()
            model = self.model.get().strip()
            license_plate = self.license_plate.get().strip()
            driver = self.driver.get().strip()

            if not vehicle_id or not model or not license_plate:
                raise ValueError("Invalid input: All fields except driver are required.")

            vehicle = {
                'id': vehicle_id,
                'model': model,
                'license_plate': license_plate,
                'driver': driver
            }

            self.app.data_store.vehicles.append(vehicle)
            self.app.data_store.save_data()
            messagebox.showinfo("Success", "Vehicle added successfully")
            self.app.open_windows["view_vehicles"].refresh_vehicles_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
