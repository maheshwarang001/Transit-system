import csv
import os
from typing import List, Dict, Tuple




class CSVWriter:
    """Class to handle writing data to CSV files"""

    def __init__(self, filepath: str):
        """Initialize the CSVWriter with the output file path"""
        self.filepath = filepath


    def write_csv(self, data: List[Tuple[str, float]], filepath: str):
        """Writes a list of tuples to a CSV file."""
        if not data:
            raise ValueError("Data to write is empty")

        # Ensure the directory exists, if not create it
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        try:
            # Open the file in 'w' mode, which overwrites any existing file content
            with open(self.filepath, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['user_id', 'billing_amount'])  # Write the header
                for user_id, billing_amount in data:
                    writer.writerow([user_id,
                                     f"{billing_amount:.2f}"])  # Write each row with billing amount formatted to 2 decimal places

        except FileNotFoundError:
            print(f"File Not Found: {filepath}")
        except PermissionError:
            print(f"Permission Denied: {filepath}")
        except Exception as e:
            print(f"An Error Occurred Writing File: {e}")
