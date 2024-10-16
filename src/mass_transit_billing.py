import argparse

from typing import List, Tuple

from src.billing_manager import BillingManager
from src.csv.csv_writer import CSVWriter
from src.csv.data_processor import DataProcessor
from src.journey import JourneyManager
class MassTransitBilling:
    def __init__(self, journey_path: str, zone_path: str, output_path: str):
        self.journey_path = journey_path
        self.zone_path = zone_path
        self.output_path = output_path
        self.data_transaction = None
        self.zone_data = None
        self.billing_manager = BillingManager()
        self.journey_manager = None

    def load_data(self):
        """
        Load transaction and zone data from CSV files.
        """
        self.data_transaction = DataProcessor.read_transaction_from_csv(self.journey_path)
        self.zone_data = DataProcessor.read_zone_map_from_csv(self.zone_path)

        if isinstance(self.data_transaction, str):
            raise ValueError(f"Error reading transaction data: {self.data_transaction}")

        if isinstance(self.zone_data, str):
            raise ValueError(f"Error reading zone data: {self.zone_data}")

    def process_billing(self):
        """
        Initialize JourneyManager and process billing.
        """
        self.journey_manager = JourneyManager(billing_manager=self.billing_manager, zone_cost=self.zone_data)
        billing_data = self.journey_manager.calculate(self.data_transaction)
        return billing_data

    def run(self):
        """
        Execute the billing process.
        """
        try:
            self.load_data()
            billing_data = self.process_billing()

            # Sort the data by user_id alphanumerically
            sorted_data = self.sorted_data(billing_data)

            # Write the sorted data to Output.CSV
            write = CSVWriter(self.output_path)
            write.write_csv(sorted_data, self.output_path)
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def sorted_data(self, billing_data: dict) -> List[Tuple[str, float]]:
        """Sort the billing data by user_id alphanumerically."""
        return sorted(billing_data.items(), key=lambda x: x[0].lower())