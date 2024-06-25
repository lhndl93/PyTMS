import os
import json
import csv
from datetime import datetime

class DataStore:
    def __init__(self):
        self.jobs = []
        self.customers = []
        self.vehicles = []
        self.drivers = []
        self.edited_jobs = {}
        self.edited_vehicles = {}
        self.edited_drivers = {}
        self.settings = {
            'date_format': 'dd/MM/yyyy',
            'job_order': ['id', 'destination', 'customer', 'pallets', 'weight', 'collection_date', 'collection_time', 'delivery_date', 'delivery_time', 'stackable', 'status'],
            'customer_order': ['id', 'name', 'contact', 'email', 'address'],
            'vehicle_order': ['id', 'model', 'license_plate', 'driver'],
            'driver_order': ['id', 'name', 'license_number']
        }
        self.load_data()

    def load_data(self):
        if not os.path.exists('data.json'):
            self.save_data()  # Create the file if it doesn't exist
        with open('data.json', 'r') as file:
            data = json.load(file)
            self.jobs = data.get('jobs', [])
            self.customers = data.get('customers', [])
            self.vehicles = data.get('vehicles', [])
            self.drivers = data.get('drivers', [])
            self.edited_jobs = data.get('edited_jobs', {})
            self.edited_vehicles = data.get('edited_vehicles', {})
            self.edited_drivers = data.get('edited_drivers', {})
            self.settings = data.get('settings', self.settings)

        # Convert dates from string to datetime objects
        for job in self.jobs:
            job['collection_date'] = self.parse_date(job.get('collection_date', '01-01-2000'))
            job['delivery_date'] = self.parse_date(job.get('delivery_date', '01-01-2000'))
            job['collection_time'] = job.get('collection_time', '00:00')
            job['delivery_time'] = job.get('delivery_time', '00:00')
            job['status'] = job.get('status', 'collection')  # Default status

    def save_data(self):
        data = {
            'jobs': self.jobs,
            'customers': self.customers,
            'vehicles': self.vehicles,
            'drivers': self.drivers,
            'edited_jobs': self.edited_jobs,
            'edited_vehicles': self.edited_vehicles,
            'edited_drivers': self.edited_drivers,
            'settings': self.settings
        }
        with open('data.json', 'w') as file:
            json.dump(data, file, default=str, indent=4)

    def load_jobs_from_csv(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                collection_date = self.parse_date(row['collection_date'])
                delivery_date = self.parse_date(row['delivery_date'])
                job = {
                    'id': row['id'],
                    'destination': row['destination'],
                    'customer': row['customer'],
                    'pallets': int(row['pallets']),
                    'weight': int(row['weight']),
                    'collection_date': collection_date,
                    'collection_time': row.get('collection_time', '00:00'),
                    'delivery_date': delivery_date,
                    'delivery_time': row.get('delivery_time', '00:00'),
                    'stackable': row['stackable'] == 'True',
                    'status': row.get('status', 'collection')  # Default status
                }
                self.jobs.append(job)
            self.save_data()

    def load_customers_from_csv(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer = {
                    'id': row['id'],
                    'name': row['name'],
                    'contact': row['contact'],
                    'email': row['email'],
                    'address': row['address']
                }
                self.customers.append(customer)
            self.save_data()

    def load_vehicles_from_csv(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                vehicle = {
                    'id': row['id'],
                    'model': row['model'],
                    'license_plate': row['license_plate'],
                    'driver': row['driver']
                }
                self.vehicles.append(vehicle)
            self.save_data()

    def load_drivers_from_csv(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                driver = {
                    'id': row['id'],
                    'name': row['name'],
                    'license_number': row['license_number']
                }
                self.drivers.append(driver)
            self.save_data()

    def parse_date(self, date_str):
        for fmt in ('%d-%m-%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Time data '{date_str}' does not match any known format.")
