# coding: utf-8

import unittest
import datetime
from hours_work import *

class HoursWork(unittest.TestCase):

    def test_string_to_datetime_should_converts_corectly(self):
        time_string = '09:30'
        expected_datetime_obj = datetime.datetime(1900, 1, 1, 9, 30)

        self.assertEqual(string_to_datetime(time_string), expected_datetime_obj)

    def test_calculate_office_hour_should_returns_correctly_data(self):
        arrival_time = datetime.datetime(1900, 1, 1, 9, 0)
        departure_time = datetime.datetime(1900, 1, 1, 18, 30)
        expected_office_hour = '8:00h'

        self.assertEqual(calculate_office_hour(arrival_time, departure_time), expected_office_hour)
