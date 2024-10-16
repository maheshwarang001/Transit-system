from typing import Dict, List

from src.csv.csv_reader import CSVReader
from src.model.journey import Journey
from src.util.zone_fee_calculator import additional_zone_fee


class DataProcessor:
    """Class to process data read from CSV files"""

    # read_transaction_from_csv collects the CSV data from read_csv() and process it to an list with custom object
    def read_transaction_from_csv(file_path: str) -> List[Journey]:
        transaction_record = CSVReader.read_csv(file_path)

        list_journey: List[Journey] = []

        if isinstance(transaction_record, list):

            if len(transaction_record) <= 1:
                print("No transaction data available.")

            for index, record in enumerate(transaction_record):
                try:
                    # Check if the row has exactly 4 fields
                    if len(record) != 4:
                        raise ValueError(f"Row {index + 2} has an incorrect number of fields: {len(record)}")


                    # Unpacking the CSV row into the Journey class
                    journey = Journey(
                        user_id=record[0],
                        station=record[1],
                        direction=record[2],
                        time=record[3]
                    )
                    list_journey.append(journey)

                except ValueError as ve:
                    print(f"Error processing row {index + 2}: {ve}")
                except Exception as e:
                    print(f"An unexpected error occurred at row {index + 2}: {e}")

        return list_journey if list_journey else "No valid transactions found."


    def read_zone_map_from_csv(file_path: str) -> dict[str, float]:
        zone_record = CSVReader.read_csv(file_path)
        zone_map: Dict[str, float] = {}

        if isinstance(zone_record, list):
            if len(zone_record) <= 1:
                print("No zone data available.")
                return zone_map  # Return empty map if no data is available

            for index, record in enumerate(zone_record):
                try:
                    # Check if the row has exactly 2 fields
                    if len(record) != 2:
                        raise ValueError(f"Row {index + 2} has an incorrect number of fields: {len(record)}")

                    # Extract station and cost
                    station = record[0]
                    zone_number: int = int(record[1])
                    zone_entry_exit_cost: float = additional_zone_fee(zone_number)


                    # Add to the dictionary
                    zone_map[station] = zone_entry_exit_cost

                except ValueError as ve:
                    print(f"Error processing row {index + 2}: {ve}")
                except Exception as e:
                    print(f"An unexpected error occurred at row {index + 2}: {e}")

        else:
            print(f"Error: Zone data is not in the expected format.")

        return zone_map


