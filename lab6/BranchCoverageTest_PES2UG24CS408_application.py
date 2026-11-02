import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# ---------- Starter tests ----------
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0

def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100


# ---------- toll_for: axle handling ----------
def test_invalid_axle_count_raises():
    with pytest.raises(ValueError):
        toll_for(1, False, False)

def test_zero_axles_raises():
    with pytest.raises(ValueError):
        toll_for(0, False, False)

def test_three_axle_base_toll():
    assert toll_for(3, False, False) == 150

def test_four_axle_base_toll():
    assert toll_for(4, False, False) == 250

def test_five_axle_uses_default_toll():      # axles not in BASE_TOLL -> else: 400
    assert toll_for(5, False, False) == 400

def test_many_axles_default_toll():
    assert toll_for(8, False, False) == 400


# ---------- toll_for: peak hours ----------
def test_two_axle_peak():
    assert toll_for(2, True, False) == 125

def test_three_axle_off_peak_no_surcharge():
    assert toll_for(3, False, False) == 150

def test_default_axle_peak():
    assert toll_for(6, True, False) == 500


# ---------- toll_for: FASTag ----------
def test_two_axle_fastag_discount():          # axles == 2 -> 10% off
    assert toll_for(2, False, True) == 90

def test_three_axle_fastag_discount():        # else branch -> 5% off
    assert toll_for(3, False, True) == 142.5

def test_four_axle_fastag_discount():
    assert toll_for(4, False, True) == 237.5

def test_default_axle_fastag_discount():
    assert toll_for(5, False, True) == 380

def test_two_axle_peak_and_fastag():
    assert toll_for(2, True, True) == 112.5

def test_three_axle_peak_and_fastag():
    assert toll_for(3, True, True) == 178.12   # 150*1.25*0.95 = 178.125 -> rounded


# ---------- toll_charge ----------
def test_fire_engine_is_exempt():
    assert toll_charge("fire_engine", 4, True, True) == 0

def test_exempt_vehicle_skips_axle_validation():
    assert toll_charge("ambulance", 1, False, False) == 0

def test_car_pays_toll():
    assert toll_charge("car", 2, False, False) == 100

def test_truck_peak_fastag():
    assert toll_charge("truck", 4, True, True) == 296.88   # 250*1.25*0.95 = 296.875

def test_non_exempt_invalid_axles_raises():
    with pytest.raises(ValueError):
        toll_charge("car", 1, False, False)


# ---------- pass_advice ----------
def test_pass_advice_buy_pass():              # cost 300 > 200
    trips = [(False, False)] * 3
    assert pass_advice(trips, 2, 200) == "buy_pass"

def test_pass_advice_either():                # cost 300 == 300
    trips = [(False, False)] * 3
    assert pass_advice(trips, 2, 300) == "either"

def test_pass_advice_pay_per_trip():          # cost 300 < 400
    trips = [(False, False)] * 3
    assert pass_advice(trips, 2, 400) == "pay_per_trip"

def test_pass_advice_mixed_trips():           # 125 + 90 + 112.5 = 327.5
    trips = [(True, False), (False, True), (True, True)]
    assert pass_advice(trips, 2, 327.5) == "either"
    assert pass_advice(trips, 2, 300) == "buy_pass"

def test_pass_advice_no_trips_loop_skipped():  # empty loop, cost 0
    assert pass_advice([], 2, 100) == "pay_per_trip"
    assert pass_advice([], 2, 0) == "either"

def test_pass_advice_invalid_axles_raises():
    with pytest.raises(ValueError):
        pass_advice([(False, False)], 1, 100)

