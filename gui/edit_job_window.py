import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class EditJobWindow:
    def __init__(self, app, job):
        self.app = app
        self.job = job
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Edit Job")
        self.window.geometry("400x400")

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        self.collection_date = DateEntry(frame, date_pattern=self.app.data_store.settings['date_format'])
        self.collection_date.set_date(self.job['collection_date'])
        self.collection_date.grid(row=0, column=1, padx=5, pady=5)

        self.delivery_date = DateEntry(frame, date_pattern=self.app.data_store.settings['date_format'])
        self.delivery_date.set_date(self.job['delivery_date'])
        self.delivery_date.grid(row=1, column=1, padx=5, pady=5)

        # Other fields...

        def save_changes():
            self.job['collection_date'] = self.collection_date.get_date()
            self.job['delivery_date'] = self.delivery_date.get_date()
            # Save other fields...

            self.app.data_store.save_data()
            self.app.refresh_jobs_list()
            self.window.destroy()

        ttk.Button(frame, text="Save", command=save_changes).grid(row=10, columnspan=2, pady=10)
