import unittest
from datetime import datetime, timedelta

from src.billing_manager import BillingManager


class TestBillingManager(unittest.TestCase):

    def setUp(self):
        """Set up the BillingManager instance before each test"""
        self.billing_manager = BillingManager()
        self.user_id = "test_user"
        self.event_time = datetime.now()


    # Test User Initilization
    def test_initialize_user(self):
        """
        Test initializing multiple users
        Verifies that user IDs are correctly added to user_bill, user_24hour_cap and user_30days_cap dictionaries"""

        self.billing_manager.initialize_user(self.user_id, self.event_time)
        self.billing_manager.initialize_user("test-user2", self.event_time)


        # Validate that both users are correctly initialized
        self.assertEqual(list(self.billing_manager.user_bill.keys())[0], self.user_id)
        self.assertEqual(list(self.billing_manager.user_bill.keys())[1], "test-user2")
        self.assertEqual(list(self.billing_manager.user_24hour_cap.keys())[0], self.user_id)
        self.assertEqual(list(self.billing_manager.user_30days_cap.keys())[0], self.user_id)

    def test_check_initialize_user_value(self):
        """
        Test that the initial values for newly created users are set correctly
        Ensures the bill cost is initialized to 0.0 for both 24-hour and 30-day caps
        """
        self.billing_manager.initialize_user(self.user_id, self.event_time)
        self.billing_manager.initialize_user("test-user2", self.event_time)


        # Validate initial billing values for the user
        self.assertEqual(self.billing_manager.user_bill[self.user_id], 0.0)
        self.assertEqual(self.billing_manager.user_24hour_cap[self.user_id].bill_cost, 0.0)
        self.assertEqual(self.billing_manager.user_30days_cap[self.user_id].bill_cost, 0.0)

    def test_reset_daily_cap(self):
        """ Test resetting the daily cap for a user
        checks that the daily cap is reset to 0.0 and the active time is updated"""
        self.billing_manager.initialize_user(self.user_id, self.event_time)
        self.billing_manager.user_24hour_cap[self.user_id].bill_cost = 10.0
        new_time = self.event_time + timedelta(days=1)
        self.billing_manager.reset_daily_cap(self.user_id, new_time)
        self.assertEqual(self.billing_manager.user_24hour_cap[self.user_id].bill_cost, 0.0)
        self.assertEqual(self.billing_manager.user_24hour_cap[self.user_id].active_time, new_time)

    def test_reset_monthly_cap(self):

        """ Test resetting the monthly cap for a user
        verifies that the monthly cap is reset to 0.0 and the active time is updated """
        self.billing_manager.initialize_user(self.user_id, self.event_time)
        self.billing_manager.user_30days_cap[self.user_id].bill_cost = 100.0
        new_time = self.event_time + timedelta(days=30)
        self.billing_manager.reset_monthly_cap(self.user_id, new_time)

        # Validate that the daily cap has been reset and the active time has been updated
        self.assertEqual(self.billing_manager.user_30days_cap[self.user_id].bill_cost, 0.0)
        self.assertEqual(self.billing_manager.user_30days_cap[self.user_id].active_time, new_time)


    def test_add_penalty(self):
        """ Test adding a penalty to a user’s bill Checks if the penalty is correctly added to the user’s bill, 24-hour cap,
         and 30-day cap
         """
        self.billing_manager.initialize_user(self.user_id, self.event_time)
        self.billing_manager.add_penalty(self.user_id)


        # Validate that the penalty is correctly applied to the user's bill and caps

        self.assertEqual(self.billing_manager.user_bill[self.user_id], 5.00)
        self.assertEqual(self.billing_manager.user_24hour_cap[self.user_id].bill_cost, 5.00)
        self.assertEqual(self.billing_manager.user_30days_cap[self.user_id].bill_cost, 5.00)


    def test_maximise_daily_limit_add_penalty(self):
        """  Test adding a penalty when the daily limit is maximized to £15
          checks that the penalty correctly increases the user's daily and monthly caps to the maximum allowed limit only
          """
        self.billing_manager.initialize_user(self.user_id, self.event_time)

        # add 12.40 to the daily spend
        self.billing_manager.user_bill[self.user_id] = 12.40
        self.billing_manager.user_24hour_cap[self.user_id].bill_cost = 12.40
        self.billing_manager.user_24hour_cap[self.user_id].active_time = self.event_time
        self.billing_manager.user_30days_cap[self.user_id].bill_cost = 12.40
        self.billing_manager.user_30days_cap[self.user_id].active_time = self.event_time

        self.billing_manager.add_penalty(self.user_id)


        # Validate that the penalty has maximized the bill and cap to £15
        self.assertEqual(self.billing_manager.user_bill[self.user_id], 15)
        self.assertEqual(self.billing_manager.user_24hour_cap[self.user_id].bill_cost, 15)
        self.assertEqual(self.billing_manager.user_30days_cap[self.user_id].bill_cost, 15)

    def test_add_journey_cost_valid(self):
        """Test adding a journey cost for a valid user when the cost is within the caps
       makes sure that the journey cost is correctly added to the user's bill and caps
       """
        self.billing_manager.initialize_user(self.user_id, self.event_time)
        self.billing_manager.add_journey_cost(self.user_id, 10.0)
        self.assertEqual(self.billing_manager.user_bill[self.user_id], 10.0)
        self.assertEqual(self.billing_manager.user_24hour_cap[self.user_id].bill_cost, 10.0)
        self.assertEqual(self.billing_manager.user_30days_cap[self.user_id].bill_cost, 10.0)

    def test_calculate_max_addable_amount(self):
        """ Test calculating the maximum addable amount to a user’s bill
       verifies that the correct amount that can still be added without exceeding the caps is calculated
       """

        self.billing_manager.initialize_user(self.user_id, self.event_time)
        self.billing_manager.user_bill[self.user_id] = 12
        self.billing_manager.user_24hour_cap[self.user_id].bill_cost = 12
        self.billing_manager.user_30days_cap[self.user_id].bill_cost = 12

        self.assertEqual(self.billing_manager.calculate_max_addable_amount(self.user_id,5),3)


