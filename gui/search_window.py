import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class SearchWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["search"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Search")
        self.window.geometry("800x600")

        def on_close():
            del self.app.open_windows["search"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        # Search by Job ID
        ttk.Label(frame, text="Search by Job ID:").grid(row=0, column=0, padx=5, pady=5)
        self.job_id_entry = ttk.Entry(frame)
        self.job_id_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Search", command=self.search_by_job_id).grid(row=0, column=2, padx=5, pady=5)

        # Search by Customer
        ttk.Label(frame, text="Search by Customer:").grid(row=1, column=0, padx=5, pady=5)
        self.customer_combo = ttk.Combobox(frame, values=[customer['name'] for customer in self.app.data_store.customers])
        self.customer_combo.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Search", command=self.search_by_customer).grid(row=1, column=2, padx=5, pady=5)

        # Results Frame
        self.results_frame = ttk.Frame(frame, padding="10")
        self.results_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)

        # Add Scrollbars
        self.scroll_y = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_x = ttk.Scrollbar(self.results_frame, orient=tk.HORIZONTAL)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.results_tree = ttk.Treeview(self.results_frame, columns=self.app.data_store.settings["job_order"], show='headings', yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.config(command=self.results_tree.yview)
        self.scroll_x.config(command=self.results_tree.xview)
        for col in self.app.data_store.settings["job_order"]:
            self.results_tree.heading(col, text=col.replace('_', ' ').capitalize())
        self.results_tree.pack(fill='both', expand=True)

    def search_by_job_id(self):
        job_id = self.job_id_entry.get().strip()
        if not job_id:
            messagebox.showerror("Error", "Please enter a Job ID to search.")
            return

        results = [job for job in self.app.data_store.jobs if job['id'] == job_id]
        self.display_results(results)

    def search_by_customer(self):
        customer_name = self.customer_combo.get().strip()
        if not customer_name:
            messagebox.showerror("Error", "Please select a Customer to search.")
            return

        results = [job for job in self.app.data_store.jobs if job['customer'] == customer_name]
        self.display_results(results)

    def display_results(self, results):
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        for job in results:
            self.results_tree.insert("", "end", values=[job[col] for col in self.app.data_store.settings["job_order"]])
