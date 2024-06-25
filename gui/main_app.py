import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog as fd
from datetime import datetime
from data_store import DataStore

class MainApp:
    def __init__(self, root):
        self.root = root
        self.data_store = DataStore()
        self.open_windows = {}
        self.initialize_app()

    def initialize_app(self):
        self.root.title("Trailer Planner")
        self.root.geometry("1365x675")

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)

        # Top frame for Add Job, Edit Job, Delete Job, and History buttons
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(side='top', fill='x', padx=10, pady=10)

        ttk.Button(top_frame, text="Add Job", command=self.add_job_window).pack(side='left', padx=5, pady=5)
        ttk.Button(top_frame, text="Edit Job", command=self.edit_selected_job).pack(side='left', padx=5, pady=5)
        ttk.Button(top_frame, text="Delete Job", command=self.delete_selected_job).pack(side='left', padx=5, pady=5)
        ttk.Button(top_frame, text="Search", command=self.search_window).pack(side='left', padx=5, pady=5)
        ttk.Button(top_frame, text="Changes", command=self.changes_window).pack(side='left', padx=5, pady=5)
        ttk.Button(top_frame, text="Customers", command=self.customer_window).pack(side='left', padx=5, pady=5)
        ttk.Button(top_frame, text="Vehicles", command=self.vehicle_window).pack(side='left', padx=5, pady=5)
        ttk.Button(top_frame, text="Drivers", command=self.driver_window).pack(side='left', padx=5, pady=5)
        ttk.Button(top_frame, text="Assign Driver", command=self.assign_driver_window).pack(side='left', padx=5, pady=5)

        # Filter frame
        filter_frame = ttk.LabelFrame(main_frame, text="Filter Options", padding="10")
        filter_frame.pack(side='top', fill='x', padx=10, pady=10)

        self.status_filter_var = tk.StringVar()
        self.status_filter_var.set("All")
        ttk.Label(filter_frame, text="Status:").pack(side='left', padx=5, pady=5)
        self.status_filter = ttk.Combobox(filter_frame, textvariable=self.status_filter_var)
        self.status_filter['values'] = ["All", "collection", "delivery", "delivered", "on hold", "done"]
        self.status_filter.pack(side='left', padx=5, pady=5)
        self.status_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_jobs_list())

        # Content frame for job list
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Jobs Frame
        jobs_frame = ttk.LabelFrame(content_frame, text="Jobs", padding="10")
        jobs_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = self.data_store.settings["job_order"]
        self.jobs_tree = ttk.Treeview(jobs_frame, columns=columns, show='headings')
        for col in columns:
            self.jobs_tree.heading(col, text=col.replace('_', ' ').capitalize())
        self.jobs_tree.pack(fill='both', expand=True)
        self.jobs_tree.bind("<Double-1>", self.on_job_double_click)
        self.jobs_tree.bind("<Button-3>", self.show_context_menu)

        # Configure tags for coloring
        self.jobs_tree.tag_configure('due_today', background='#90EE90')  # light green
        self.jobs_tree.tag_configure('future', background='#ADD8E6')     # light blue
        self.jobs_tree.tag_configure('late', background='#FFB6C1')       # light red

        self.refresh_jobs_list()

        # Bottom frame for remaining menu buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side='bottom', fill='x', padx=10, pady=10)

        ttk.Button(bottom_frame, text="Settings", command=self.settings_window).pack(side='left', padx=5, pady=5)
        ttk.Button(bottom_frame, text="Export to CSV", command=self.export_to_csv).pack(side='left', padx=5, pady=5)
        ttk.Button(bottom_frame, text="Import", command=self.import_window).pack(side='left', padx=5, pady=5)
        ttk.Button(bottom_frame, text="Exit", command=self.root.quit).pack(side='left', padx=5, pady=5)

        # Context Menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit Job", command=self.edit_selected_job)
        self.context_menu.add_command(label="Delete Job", command=self.delete_selected_job)
        self.context_menu.add_command(label="Change Status", command=self.change_status_window)
        self.context_menu.add_command(label="View Changes", command=self.changes_window)

    def refresh_jobs_list(self):
        for row in self.jobs_tree.get_children():
            self.jobs_tree.delete(row)
        status_filter = self.status_filter_var.get()
        today = datetime.now().date()
        for job in self.data_store.jobs:
            collection_date = job['collection_date'].date()
            if status_filter == "All" or job['status'] == status_filter:
                if collection_date == today:
                    tag = 'due_today'
                elif collection_date > today:
                    tag = 'future'
                else:
                    tag = 'late'
                self.jobs_tree.insert("", "end", values=[job[col] for col in self.data_store.settings["job_order"]], tags=(tag,))

    def on_job_double_click(self, event):
        selected_item = self.jobs_tree.selection()
        if selected_item:
            idx = self.jobs_tree.index(selected_item)
            self.edit_job(self.data_store.jobs[idx])

    def show_context_menu(self, event):
        try:
            self.jobs_tree.selection_set(self.jobs_tree.identify_row(event.y))
            self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def add_job_window(self):
        if "add_job" in self.open_windows:
            self.open_windows["add_job"].lift()
            return
        from .add_job_window import AddJobWindow
        AddJobWindow(self)

    def edit_selected_job(self):
        selected_item = self.jobs_tree.selection()
        if selected_item:
            idx = self.jobs_tree.index(selected_item)
            self.edit_job(self.data_store.jobs[idx])
        else:
            messagebox.showerror("Error", "No job selected. Please select a job to edit.")

    def delete_selected_job(self):
        selected_item = self.jobs_tree.selection()
        if selected_item:
            idx = self.jobs_tree.index(selected_item)
            job = self.data_store.jobs[idx]
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete job {job['id']}?")
            if confirm:
                self.delete_job(job)
        else:
            messagebox.showerror("Error", "No job selected. Please select a job to delete.")

    def change_status_window(self):
        selected_item = self.jobs_tree.selection()
        if selected_item:
            idx = self.jobs_tree.index(selected_item)
            job = self.data_store.jobs[idx]
            self.change_status(job)
        else:
            messagebox.showerror("Error", "No job selected. Please select a job to change status.")

    def change_status(self, job):
        window = tk.Toplevel(self.root)
        window.title("Change Job Status")
        window.geometry("300x200")

        ttk.Label(window, text="Change Status").pack(pady=10)
        status = tk.StringVar(value=job['status'])
        status_combobox = ttk.Combobox(window, textvariable=status)
        status_combobox['values'] = ["collection", "delivery", "delivered", "on hold", "done"]
        status_combobox.pack(pady=10)

        def update_status():
            old_status = job['status']
            new_status = status.get()
            job['status'] = new_status

            # Log the status change
            old_job = job.copy()
            job['status'] = new_status
            new_job = job.copy()
            if job['id'] not in self.data_store.edited_jobs:
                self.data_store.edited_jobs[job['id']] = []
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.data_store.edited_jobs[job['id']].append({"old": old_job, "new": new_job, "timestamp": timestamp})

            self.data_store.save_data()
            self.refresh_jobs_list()
            window.destroy()

        ttk.Button(window, text="Update", command=update_status).pack(pady=10)

    def settings_window(self):
        if "settings" in self.open_windows:
            self.open_windows["settings"].lift()
            return
        from .settings_window import SettingsWindow
        SettingsWindow(self)

    def export_to_csv(self):
        if "export" in self.open_windows:
            self.open_windows["export"].lift()
            return
        from .export_csv_window import ExportCSVWindow
        ExportCSVWindow(self)

    def import_window(self):
        if "import" in self.open_windows:
            self.open_windows["import"].lift()
            return
        from .import_window import ImportWindow
        ImportWindow(self)

    def search_window(self):
        if "search" in self.open_windows:
            self.open_windows["search"].lift()
            return
        from .search_window import SearchWindow
        SearchWindow(self)

    def changes_window(self):
        selected_item = self.jobs_tree.selection()
        if selected_item:
            idx = self.jobs_tree.index(selected_item)
            job = self.data_store.jobs[idx]
            if "changes" in self.open_windows:
                self.open_windows["changes"].lift()
                return
            from .changes_window import ChangesWindow
            ChangesWindow(self, job)
        else:
            messagebox.showerror("Error", "No job selected. Please select a job to view changes.")

    def customer_window(self):
        if "view_customers" in self.open_windows:
            self.open_windows["view_customers"].lift()
            return
        from .customer_window import CustomerWindow
        CustomerWindow(self)

    def vehicle_window(self):
        if "view_vehicles" in self.open_windows:
            self.open_windows["view_vehicles"].lift()
            return
        from .vehicle_window import VehicleWindow
        VehicleWindow(self)

    def driver_window(self):
        if "view_drivers" in self.open_windows:
            self.open_windows["view_drivers"].lift()
            return
        from .driver_window import DriverWindow
        DriverWindow(self)

    def assign_driver_window(self):
        if "assign_driver" in self.open_windows:
            self.open_windows["assign_driver"].lift()
            return
        from .assign_driver_window import AssignDriverWindow
        AssignDriverWindow(self)

    def load_jobs_from_csv(self):
        csv_file = fd.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if csv_file:
            self.data_store.load_jobs_from_csv(csv_file)
            self.refresh_jobs_list()
            messagebox.showinfo("Success", "Jobs loaded successfully")

    def refresh_all_views(self):
        self.refresh_jobs_list()

    def refresh_view(self, window, data, order, edit_command, delete_command):
        for widget in window.winfo_children():
            widget.destroy()

        frame = ttk.Frame(window, padding="10")
        frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(frame, columns=order, show='headings')
        for col in order:
            tree.heading(col, text=col.replace('_', ' ').capitalize())
        tree.pack(fill='both', expand=True)

        for item in data:
            tree.insert("", "end", values=[item[col] for col in order])

        def on_edit():
            selected_item = tree.selection()
            if selected_item:
                idx = tree.index(selected_item)
                edit_command(data[idx])

        def on_delete():
            selected_item = tree.selection()
            if selected_item:
                idx = tree.index(selected_item)
                delete_command(data[idx])

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Edit", command=on_edit).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=on_delete).pack(side='left', padx=5)

    def edit_job(self, job):
        from .edit_job_window import EditJobWindow
        EditJobWindow(self, job)

    def delete_job(self, job):
        self.data_store.jobs.remove(job)
        self.data_store.save_data()
        self.refresh_all_views()
