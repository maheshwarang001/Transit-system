from datetime import time, datetime


# TrackPrevInTap a data class of a user's entry tap at a station with the timestamp
class TrackPrevInTap:

    def __init__(self, transaction_time: datetime, station: str):
        self.transaction_time = transaction_time
        self.station = station


# TimeCap is the time cap for a journey including the time of activity and bill cost
class TimeCap:

    def __init__(self, active_time: datetime, bill_cost: float):
        self.active_time = active_time
        self.bill_cost = bill_cost
