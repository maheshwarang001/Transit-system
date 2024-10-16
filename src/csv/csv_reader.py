import csv


class CSVReader:
    """Class to handle reading CSV files"""



    def read_csv(file_path: str):
        data = []

        try:

            # Open the CSV file in read mode
            with open(file_path, 'r') as file:

                reader = csv.reader(file)

                next(reader, None)

                for row in reader:
                    data.append(row)

            return data

        except FileNotFoundError:
            return f"File Not Found: {file_path}"
        except FileExistsError:
            return f"File Doesn't Exist: {file}"
        except Exception as e:
            return f"An Error Occurred Reading File: {e}"

