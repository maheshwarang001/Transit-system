from datetime import datetime


# Represents a transit journey of a user
class Journey:

    def __init__(self, user_id: str, station: str, direction: str, time: str):
        try:
            # Initialize instance variables with the provided arguments
            self.userId: str = user_id
            self.station: str = station
            self.direction: str = direction
            self.time: datetime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")

        except ValueError:
            raise ValueError(f"Invalid format for journey")


