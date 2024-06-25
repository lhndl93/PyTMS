import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class AddJobWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["add_job"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Add Job")
        self.window.geometry("400x500")

        def on_close():
            del self.app.open_windows["add_job"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Job ID:").grid(row=0, column=0, padx=5, pady=5)
        self.job_id = ttk.Entry(frame)
        self.job_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Destination:").grid(row=1, column=0, padx=5, pady=5)
        self.destination = ttk.Entry(frame)
        self.destination.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Customer:").grid(row=2, column=0, padx=5, pady=5)
        self.customer = ttk.Combobox(frame, values=[customer['name'] for customer in self.app.data_store.customers])
        self.customer.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Pallets:").grid(row=3, column=0, padx=5, pady=5)
        self.pallets = ttk.Entry(frame)
        self.pallets.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Weight:").grid(row=4, column=0, padx=5, pady=5)
        self.weight = ttk.Entry(frame)
        self.weight.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Collection Date:").grid(row=5, column=0, padx=5, pady=5)
        self.collection_date = DateEntry(frame, date_pattern=self.app.data_store.settings['date_format'])
        self.collection_date.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Collection Time:").grid(row=6, column=0, padx=5, pady=5)
        self.collection_time_hour = ttk.Combobox(frame, values=[f"{i:02}" for i in range(24)], width=3)
        self.collection_time_hour.grid(row=6, column=1, sticky='W', padx=5, pady=5)
        self.collection_time_minute = ttk.Combobox(frame, values=[f"{i:02}" for i in range(60)], width=3)
        self.collection_time_minute.grid(row=6, column=1, sticky='E', padx=5, pady=5)

        ttk.Label(frame, text="Delivery Date:").grid(row=7, column=0, padx=5, pady=5)
        self.delivery_date = DateEntry(frame, date_pattern=self.app.data_store.settings['date_format'])
        self.delivery_date.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Delivery Time:").grid(row=8, column=0, padx=5, pady=5)
        self.delivery_time_hour = ttk.Combobox(frame, values=[f"{i:02}" for i in range(24)], width=3)
        self.delivery_time_hour.grid(row=8, column=1, sticky='W', padx=5, pady=5)
        self.delivery_time_minute = ttk.Combobox(frame, values=[f"{i:02}" for i in range(60)], width=3)
        self.delivery_time_minute.grid(row=8, column=1, sticky='E', padx=5, pady=5)

        ttk.Label(frame, text="Stackable:").grid(row=9, column=0, padx=5, pady=5)
        self.stackable = tk.BooleanVar()
        ttk.Checkbutton(frame, variable=self.stackable).grid(row=9, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Status:").grid(row=10, column=0, padx=5, pady=5)
        self.status = ttk.Combobox(frame, values=["collection", "delivery", "delivered", "on hold", "done"])
        self.status.grid(row=10, column=1, padx=5, pady=5)
        self.status.set("collection")  # Default status

        ttk.Button(frame, text="Add Job", command=self.add_job).grid(row=11, columnspan=2, pady=10)

    def add_job(self):
        try:
            job_id = self.job_id.get().strip()
            destination = self.destination.get().strip()
            customer = self.customer.get().strip()
            pallets = int(self.pallets.get().strip())
            weight = int(self.weight.get().strip())
            collection_date = self.collection_date.get_date()
            collection_time = f"{self.collection_time_hour.get()}:{self.collection_time_minute.get()}"
            delivery_date = self.delivery_date.get_date()
            delivery_time = f"{self.delivery_time_hour.get()}:{self.delivery_time_minute.get()}"
            stackable = self.stackable.get()
            status = self.status.get().strip()

            if not job_id or not destination or not customer or not collection_date or not collection_time or not delivery_date or not delivery_time or not status:
                raise ValueError("Invalid input: All fields are required.")

            job = {
                'id': job_id,
                'destination': destination,
                'customer': customer,
                'pallets': pallets,
                'weight': weight,
                'collection_date': collection_date,
                'collection_time': collection_time,
                'delivery_date': delivery_date,
                'delivery_time': delivery_time,
                'stackable': stackable,
                'status': status
            }

            self.app.data_store.jobs.append(job)
            self.app.data_store.save_data()
            messagebox.showinfo("Success", "Job added successfully")
            self.app.refresh_jobs_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
