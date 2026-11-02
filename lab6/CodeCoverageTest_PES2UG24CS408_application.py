import pytest
from highway_toll import toll_for, toll_charge, pass_advice


def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0

def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100

def test_invalid_axle_count_raises():
    with pytest.raises(ValueError):
        toll_for(1, False, False)

def test_three_axle_base_toll():
    assert toll_for(3, False, False) == 150

def test_four_axle_base_toll():
    assert toll_for(4, False, False) == 250

def test_two_axle_peak():
    assert toll_for(2, True, False) == 125

def test_two_axle_fastag_discount():
    assert toll_for(2, False, True) == 90

def test_three_axle_fastag_discount():
    assert toll_for(3, False, True) == 142.5

def test_two_axle_peak_and_fastag():
    assert toll_for(2, True, True) == 112.5

def test_fire_engine_is_exempt():
    assert toll_charge("fire_engine", 4, True, True) == 0

def test_car_pays_toll():
    assert toll_charge("car", 2, False, False) == 100

def test_non_exempt_invalid_axles_raises():
    with pytest.raises(ValueError):
        toll_charge("car", 1, False, False)

def test_pass_advice_buy_pass():
    assert pass_advice([(False, False)] * 3, 2, 200) == "buy_pass"

def test_pass_advice_pay_per_trip():
    assert pass_advice([(False, False)] * 3, 2, 400) == "pay_per_trip"
