import csv
import tempfile

from src.csv.data_processor import DataProcessor
from src.model.journey import Journey
from src.util.zone_fee_calculator import additional_zone_fee


def test_additional_zone_fee():
    assert additional_zone_fee(1) == 0.80
    assert additional_zone_fee(4) == 0.30
    assert additional_zone_fee(7) == 0.10
