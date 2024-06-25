import tkinter as tk
from tkinter import ttk

class ChangesWindow:
    def __init__(self, app, job):
        self.app = app
        self.job = job
        self.app.open_windows["changes"] = self
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.app.root)
        self.window.title(f"Changes for Job {self.job['id']}")
        self.window.geometry("600x400")

        def on_close():
            del self.app.open_windows["changes"]
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill='both', expand=True)

        columns = ["timestamp", "attribute", "old_value", "new_value"]
        self.changes_tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.changes_tree.heading(col, text=col.replace('_', ' ').capitalize())
        self.changes_tree.pack(fill='both', expand=True)

        self.refresh_changes_list()

    def refresh_changes_list(self):
        for row in self.changes_tree.get_children():
            self.changes_tree.delete(row)
        
        job_id = self.job['id']
        if job_id in self.app.data_store.edited_jobs:
            for change in self.app.data_store.edited_jobs[job_id]:
                timestamp = change["timestamp"]
                for key in change["old"]:
                    old_value = change["old"][key]
                    new_value = change["new"][key]
                    if old_value != new_value:
                        self.changes_tree.insert("", "end", values=[timestamp, key, old_value, new_value])
