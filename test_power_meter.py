import inspect
import pytest

from real import PowerMeterE4418B
from fake import FakeE4418B


@pytest.fixture
def meter():
    return PowerMeterE4418B(FakeE4418B())


def test_Identify(meter):
    assert "E4418B" in meter.identify()


def test_ZeroAndCalibrate(meter):
    meter.zeroAndCalibrate()
    assert meter.inst.commands_sent == ["CAL:ZERO:AUTO ONCE", "CAL:AUTO ONCE"]


def test_Frequency(meter):
    meter.setFrequency(1.8e9)
    assert meter.inst.frequency_hz == 1.8e9


def test_measure(meter):
    reading = meter.measureAvgPower()
    assert isinstance(reading, float)
    assert reading == pytest.approx(-12.345)


def test_units_change_the_reading(meter):
    meter.setUnits("W")
    assert meter.measureAvgPower() == 5.888e-05



def test_every_method_runs_without_hardware(meter):
    for name, method in inspect.getmembers(meter, inspect.ismethod):
        if name.startswith("_"):
            continue
        params = list(inspect.signature(method).parameters)
        args = {"hz": 1e9, "units": "DBM"}
        method(*[args[p] for p in params])