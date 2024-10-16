from datetime import datetime
from typing import Dict

from src.model.track_prev_tap import TimeCap, TrackPrevInTap
from src.util.constans import PENALTY_CHARGES, DAILY_CAP, MONTHLY_CAP


class BillingManager:

    def __init__(self):
        """Initializes the BillingManager with dictionaries to track user bills and caps"""

        # Tracks the total bill for each user
        self.user_bill: Dict[str, float] = {}
        # Stores the current active journey
        self.track_active_journey: Dict[str, TrackPrevInTap] = {}
        # Tracks the 24-hour caps for each user
        self.user_24hour_cap: Dict[str, TimeCap] = {}
        # Tracks the 30-day caps for each user
        self.user_30days_cap: Dict[str, TimeCap] = {}

    def initialize_user(self, user_id: str, event_time: datetime):
        """Initialize user with default billing and cap tracking values"""

        try:
            self.user_bill[user_id] = 0.0
            self.user_24hour_cap[user_id] = TimeCap(event_time, 0.0)
            self.user_30days_cap[user_id] = TimeCap(event_time, 0.0)
        except Exception as e:
            print(f"Error initializing user {user_id} at {event_time}: {e}")

    def reset_daily_cap(self, user_id: str, event_time: datetime):
        """Reset the 24-hour cap for a new day"""
        try:
            if user_id in self.user_24hour_cap:
                self.user_24hour_cap[user_id].active_time = event_time
                self.user_24hour_cap[user_id].bill_cost = 0.0
            else:
                raise KeyError(f"User {user_id} not found in daily cap tracking.")
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(f"Error resetting daily cap for user {user_id} at {event_time}: {e}")


    def reset_monthly_cap(self, user_id: str, event_time: datetime):
        """Reset the 30-day cap for a new month"""
        try:
            if user_id in self.user_30days_cap:
                self.user_30days_cap[user_id].active_time = event_time
                self.user_30days_cap[user_id].bill_cost = 0.0
            else:
                raise KeyError(f"User {user_id} not found in monthly cap tracking.")
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(f"Error resetting monthly cap for user {user_id} at {event_time}: {e}")


    def add_penalty(self, user_id: str):
        """Add penalty for incomplete or invalid journeys"""
        try:
            if user_id not in self.user_bill:
                raise KeyError(f"User {user_id} not initialized.")
            penalty = PENALTY_CHARGES

            # calculate max amount to be added to stay within the daily and monthly limit
            amount_to_add = self.calculate_max_addable_amount(user_id, penalty)

            # Add the amount to the user's bill and caps
            self.user_bill[user_id] += amount_to_add
            self.user_24hour_cap[user_id].bill_cost += amount_to_add
            self.user_30days_cap[user_id].bill_cost += amount_to_add
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(f"Error adding penalty for user {user_id}: {e}")

    def add_journey_cost(self, user_id: str, journey_cost: float):
        """Add the cost of a complete journey if it doesn't exceed daily or monthly caps"""
        try:
            if user_id not in self.user_bill:
                raise KeyError(f"User {user_id} not initialized.")
            amount_to_add = self.calculate_max_addable_amount(user_id, journey_cost)

            # Add the amount to the user's bill and caps
            self.user_bill[user_id] += amount_to_add
            self.user_24hour_cap[user_id].bill_cost += amount_to_add
            self.user_30days_cap[user_id].bill_cost += amount_to_add
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(f"Error adding journey cost for user {user_id}: {e}")


    def calculate_max_addable_amount(self, user_id: str, amount: float) -> float:
        """Calculates the maximum amount that can be added to the user's bill without exceeding the daily and monthly
        caps"""
        try:
            if user_id not in self.user_24hour_cap or user_id not in self.user_30days_cap:
                raise KeyError(f"User {user_id} not initialized.")

            max_daily_charge = DAILY_CAP - self.user_24hour_cap[user_id].bill_cost
            max_monthly_charge = MONTHLY_CAP - self.user_30days_cap[user_id].bill_cost
            return min(amount, max_daily_charge, max_monthly_charge)

        except KeyError as ke:
            print(ke)
            return 0.0
        except Exception as e:
            print(f"Error calculating maximum addable amount for user {user_id}: {e}")
            return 0.0


