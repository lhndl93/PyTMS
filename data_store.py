import csv
import json
from datetime import datetime

class DataStore:
    def __init__(self):
        self.jobs = []
        self.customers = []
        self.vehicles = []
        self.drivers = []
        self.edited_jobs = {}
        self.settings = {
            "date_format": "dd/MM/yyyy",
            "job_order": ["id", "destination", "customer", "pallets", "weight", "collection_date", "collection_time", "delivery_date", "delivery_time", "stackable", "status"],
        }
        self.load_data()

    def load_data(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                self.jobs = data["jobs"]
                self.customers = data["customers"]
                self.vehicles = data["vehicles"]
                self.drivers = data["drivers"]
                self.edited_jobs = data["edited_jobs"]
                self.settings.update(data["settings"])
            self.parse_dates()
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {
            "jobs": self.jobs,
            "customers": self.customers,
            "vehicles": self.vehicles,
            "drivers": self.drivers,
            "edited_jobs": self.edited_jobs,
            "settings": self.settings,
        }
        with open("data.json", "w") as f:
            json.dump(data, f, default=str, indent=4)

    def parse_dates(self):
        for job in self.jobs:
            job['collection_date'] = datetime.strptime(job['collection_date'], self.settings['date_format']).date()
            job['delivery_date'] = datetime.strptime(job['delivery_date'], self.settings['date_format']).date()
            job['collection_time'] = datetime.strptime(job['collection_time'], "%H:%M:%S").time()
            job['delivery_time'] = datetime.strptime(job['delivery_time'], "%H:%M:%S").time()
