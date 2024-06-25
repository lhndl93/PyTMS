import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class EditJobWindow:
    def __init__(self, app, job):
        self.app = app
        self.job = job
        self.app.open_windows["edit_job"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Edit Job")
        self.window.geometry("400x500")

        def on_close():
            del self.app.open_windows["edit_job"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Job ID:").grid(row=0, column=0, padx=5, pady=5)
        self.job_id = ttk.Entry(frame)
        self.job_id.grid(row=0, column=1, padx=5, pady=5)
        self.job_id.insert(0, self.job['id'])

        ttk.Label(frame, text="Destination:").grid(row=1, column=0, padx=5, pady=5)
        self.destination = ttk.Entry(frame)
        self.destination.grid(row=1, column=1, padx=5, pady=5)
        self.destination.insert(0, self.job['destination'])

        ttk.Label(frame, text="Customer:").grid(row=2, column=0, padx=5, pady=5)
        self.customer = ttk.Combobox(frame, values=[customer['name'] for customer in self.app.data_store.customers])
        self.customer.grid(row=2, column=1, padx=5, pady=5)
        self.customer.set(self.job['customer'])

        ttk.Label(frame, text="Pallets:").grid(row=3, column=0, padx=5, pady=5)
        self.pallets = ttk.Entry(frame)
        self.pallets.grid(row=3, column=1, padx=5, pady=5)
        self.pallets.insert(0, self.job['pallets'])

        ttk.Label(frame, text="Weight:").grid(row=4, column=0, padx=5, pady=5)
        self.weight = ttk.Entry(frame)
        self.weight.grid(row=4, column=1, padx=5, pady=5)
        self.weight.insert(0, self.job['weight'])

        ttk.Label(frame, text="Collection Date:").grid(row=5, column=0, padx=5, pady=5)
        self.collection_date = DateEntry(frame, date_pattern=self.app.data_store.settings['date_format'])
        self.collection_date.grid(row=5, column=1, padx=5, pady=5)
        self.collection_date.set_date(self.job['collection_date'])

        ttk.Label(frame, text="Collection Time:").grid(row=6, column=0, padx=5, pady=5)
        collection_time = self.job['collection_time'].split(':')
        self.collection_time_hour = ttk.Combobox(frame, values=[f"{i:02}" for i in range(24)], width=3)
        self.collection_time_hour.grid(row=6, column=1, sticky='W', padx=5, pady=5)
        self.collection_time_hour.set(collection_time[0])
        self.collection_time_minute = ttk.Combobox(frame, values=[f"{i:02}" for i in range(60)], width=3)
        self.collection_time_minute.grid(row=6, column=1, sticky='E', padx=5, pady=5)
        self.collection_time_minute.set(collection_time[1])

        ttk.Label(frame, text="Delivery Date:").grid(row=7, column=0, padx=5, pady=5)
        self.delivery_date = DateEntry(frame, date_pattern=self.app.data_store.settings['date_format'])
        self.delivery_date.grid(row=7, column=1, padx=5, pady=5)
        self.delivery_date.set_date(self.job['delivery_date'])

        ttk.Label(frame, text="Delivery Time:").grid(row=8, column=0, padx=5, pady=5)
        delivery_time = self.job['delivery_time'].split(':')
        self.delivery_time_hour = ttk.Combobox(frame, values=[f"{i:02}" for i in range(24)], width=3)
        self.delivery_time_hour.grid(row=8, column=1, sticky='W', padx=5, pady=5)
        self.delivery_time_hour.set(delivery_time[0])
        self.delivery_time_minute = ttk.Combobox(frame, values=[f"{i:02}" for i in range(60)], width=3)
        self.delivery_time_minute.grid(row=8, column=1, sticky='E', padx=5, pady=5)
        self.delivery_time_minute.set(delivery_time[1])

        ttk.Label(frame, text="Stackable:").grid(row=9, column=0, padx=5, pady=5)
        self.stackable = tk.BooleanVar(value=self.job['stackable'])
        ttk.Checkbutton(frame, variable=self.stackable).grid(row=9, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Status:").grid(row=10, column=0, padx=5, pady=5)
        self.status = ttk.Combobox(frame, values=["collection", "delivery", "delivered", "on hold", "done"])
        self.status.grid(row=10, column=1, padx=5, pady=5)
        self.status.set(self.job['status'])

        ttk.Button(frame, text="Save Changes", command=self.save_changes).grid(row=11, columnspan=2, pady=10)

    def save_changes(self):
        try:
            old_job = self.job.copy()
            self.job['id'] = self.job_id.get().strip()
            self.job['destination'] = self.destination.get().strip()
            self.job['customer'] = self.customer.get().strip()
            self.job['pallets'] = int(self.pallets.get().strip())
            self.job['weight'] = int(self.weight.get().strip())
            self.job['collection_date'] = self.collection_date.get_date()
            self.job['collection_time'] = f"{self.collection_time_hour.get()}:{self.collection_time_minute.get()}"
            self.job['delivery_date'] = self.delivery_date.get_date()
            self.job['delivery_time'] = f"{self.delivery_time_hour.get()}:{self.delivery_time_minute.get()}"
            self.job['stackable'] = self.stackable.get()
            self.job['status'] = self.status.get().strip()

            if not self.job['id'] or not self.job['destination'] or not self.job['customer'] or not self.job['collection_date'] or not self.job['collection_time'] or not self.job['delivery_date'] or not self.job['delivery_time'] or not self.job['status']:
                raise ValueError("Invalid input: All fields are required.")

            new_job = self.job.copy()
            if self.job['id'] not in self.app.data_store.edited_jobs:
                self.app.data_store.edited_jobs[self.job['id']] = []
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.app.data_store.edited_jobs[self.job['id']].append({"old": old_job, "new": new_job, "timestamp": timestamp})
            self.app.data_store.save_data()
            messagebox.showinfo("Success", "Job updated successfully")
            self.app.refresh_jobs_list()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
