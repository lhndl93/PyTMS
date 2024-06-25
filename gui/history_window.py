import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class HistoryWindow:
    def __init__(self, app):
        self.app = app
        self.app.open_windows["history"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title("History")
        self.window.geometry("800x600")

        def on_close():
            del self.app.open_windows["history"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        notebook = ttk.Notebook(frame)
        notebook.pack(fill='both', expand=True)

        # Deleted Jobs Section
        deleted_frame = ttk.Frame(notebook, padding="10")
        notebook.add(deleted_frame, text="Deleted Jobs")

        self.deleted_tree = ttk.Treeview(deleted_frame, columns=self.app.data_store.settings["job_order"], show='headings')
        for col in self.app.data_store.settings["job_order"]:
            self.deleted_tree.heading(col, text=col.replace('_', ' ').capitalize())
        self.deleted_tree.pack(fill='both', expand=True)

        ttk.Button(deleted_frame, text="Reinstate Job", command=self.reinstate_job).pack(pady=10)

        self.refresh_deleted_jobs()

        # Edited Jobs Section
        edited_frame = ttk.Frame(notebook, padding="10")
        notebook.add(edited_frame, text="Edited Jobs")

        self.edited_tree = ttk.Treeview(edited_frame, columns=["id", "field", "old_value", "new_value"], show='headings')
        self.edited_tree.heading("id", text="Job ID")
        self.edited_tree.heading("field", text="Field")
        self.edited_tree.heading("old_value", text="Old Value")
        self.edited_tree.heading("new_value", text="New Value")
        self.edited_tree.pack(fill='both', expand=True)

        self.refresh_edited_jobs()

    def refresh_deleted_jobs(self):
        for row in self.deleted_tree.get_children():
            self.deleted_tree.delete(row)
        for job in self.app.data_store.deleted_jobs:
            self.deleted_tree.insert("", "end", values=[job[col] for col in self.app.data_store.settings["job_order"]])

    def refresh_edited_jobs(self):
        for row in self.edited_tree.get_children():
            self.edited_tree.delete(row)
        for edit in self.app.data_store.edited_jobs:
            for key in edit["old"]:
                if edit["old"][key] != edit["new"][key]:
                    self.edited_tree.insert("", "end", values=[edit["old"]["id"], key, edit["old"][key], edit["new"][key]])

    def reinstate_job(self):
        selected_item = self.deleted_tree.selection()
        if selected_item:
            idx = self.deleted_tree.index(selected_item)
            job = self.app.data_store.deleted_jobs[idx]
            confirm = messagebox.askyesno("Confirm Reinstate", f"Are you sure you want to reinstate job {job['id']}?")
            if confirm:
                self.app.data_store.jobs.append(job)
                self.app.data_store.deleted_jobs.remove(job)
                self.app.data_store.save_data()
                self.refresh_deleted_jobs()
                self.app.refresh_jobs_list()
        else:
            messagebox.showerror("Error", "No job selected. Please select a job to reinstate.")
