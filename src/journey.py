from datetime import datetime
from typing import Dict, List

from src.billing_manager import BillingManager
from src.model.journey import Journey
from src.model.track_prev_tap import TrackPrevInTap, TimeCap
from src.util.constans import TRIP_CHARGES


class JourneyManager:
    """Manages the journey transactions for billing purposes"""

    def __init__(self, billing_manager: BillingManager, zone_cost: Dict[str, float]):
        self.zone_cost = zone_cost
        self.billing_manager = billing_manager

    def calculate(self, transactions: List[Journey]):
        """Process the list of transactions and calculate the billing for each user"""
        for event in transactions:
            try:
                user_id = event.userId
                direction = event.direction
                station = event.station
                event_time: datetime = event.time

                # Initialize user billing and caps if not present
                if user_id not in self.billing_manager.user_bill:
                    self.billing_manager.initialize_user(user_id, event_time)

                # Check for new day or month and reset caps accordingly
                if self.billing_manager.user_24hour_cap[user_id].active_time.date() != event_time.date():
                    self.billing_manager.reset_daily_cap(user_id, event_time)

                if self.billing_manager.user_30days_cap[user_id].active_time.month != event_time.month:
                    self.billing_manager.reset_monthly_cap(user_id, event_time)

                # Process "IN" and "OUT" journey events
                if direction == "IN":
                    self._handle_in_tap(user_id, station, event_time)
                elif direction == "OUT":
                    self._handle_out_tap(user_id, station, event_time)
                else:
                    raise ValueError(f"Invalid direction '{direction}' for user {user_id} at {event_time}")
            except Exception as e:
                print(f"Error processing transaction for user {user_id} at {event_time}: {e}")

        # Process any pending journeys
        self._handle_incomplete_journey()

        return self.billing_manager.user_bill

    def _handle_incomplete_journey(self):
        """Applies penalties for incomplete journeys """
        for userId in self.billing_manager.track_active_journey:
            try:
                self.billing_manager.add_penalty(userId)
            except Exception as e:
                print(f"Error applying penalty for user {userId}: {e}")

    def _handle_in_tap(self, user_id: str, station: str, event_time: datetime):
        """Handle when the user taps IN"""
        try:
            # If there's already an active journey apply a penalty for missing the previous OUT tap
            if user_id in self.billing_manager.track_active_journey:
                self.billing_manager.add_penalty(user_id)
                self.billing_manager.track_active_journey.pop(user_id)

            # Record the new IN tap and start tracking the journey
            self.billing_manager.track_active_journey[user_id] = TrackPrevInTap(event_time, station)

        except Exception as e:
            print(f"Error handling IN tap for user {user_id} at {event_time}: {e}")

    def _handle_out_tap(self, user_id: str, station: str, event_time: datetime):
        """Handle when the user taps OUT"""
        try:
            # If no active IN tap exists apply a penalty
            if user_id not in self.billing_manager.track_active_journey:
                self.billing_manager.add_penalty(user_id)
            else:
                # Check if the journey spanned multiple days
                in_tap = self.billing_manager.track_active_journey[user_id]
                if in_tap.transaction_time.date() != event_time.date():
                    self.billing_manager.add_penalty(user_id)
                else:
                    # Calculate the cost of the complete journey
                    journey_cost = self._calculate_journey_cost(in_tap.station, station)
                    self.billing_manager.add_journey_cost(user_id, journey_cost)

                # Remove the completed journey
                self.billing_manager.track_active_journey.pop(user_id)

        except Exception as e:
            print(f"Error handling OUT tap for user {user_id} at {event_time}: {e}")
    def _calculate_journey_cost(self, start_station: str, end_station: str) -> float:
        """Calculate the cost of the journey based on zones"""
        try:
            start_zone_cost = self.zone_cost.get(start_station)
            end_zone_cost = self.zone_cost.get(end_station)
            return TRIP_CHARGES + start_zone_cost + end_zone_cost
        except Exception as e:
            print(f"Error calculating journey cost from {start_station} to {end_station}: {e}")
            return 0.0
