"""Avanza Sensor Tests."""


import pytest
from custom_components.avanza_stock.sensor import (
    AvanzaStockSensor, MONITORED_CONDITIONS)


def test_name():
    """Test name."""
    stock = 0
    name = 'Avanza Stock {0}'.format(stock)
    monitored_conditions = []

    sensor = AvanzaStockSensor(stock, name, monitored_conditions)

    assert sensor.name == name


def test_icon():
    """Test icon."""
    stock = 0
    name = 'Avanza Stock {0}'.format(stock)
    monitored_conditions = []

    sensor = AvanzaStockSensor(stock, name, monitored_conditions)

    assert sensor.icon == 'mdi:cash'


def test_state():
    """Test state."""
    stock = 5431
    name = 'Avanza Stock {0}'.format(stock)
    monitored_conditions = []

    sensor = AvanzaStockSensor(stock, name, monitored_conditions)

    sensor.update()

    assert type(sensor.state) == float


def test_unit_of_measurement():
    """Test unit of measurement."""
    stock = 5431
    name = 'Avanza Stock {0}'.format(stock)
    monitored_conditions = []

    sensor = AvanzaStockSensor(stock, name, monitored_conditions)

    sensor.update()

    assert sensor.unit_of_measurement == 'SEK'


def test_no_monitored_conditions():
    """Test unit of measurement."""
    stock = 5431
    name = 'Avanza Stock {0}'.format(stock)
    monitored_conditions = []

    sensor = AvanzaStockSensor(stock, name, monitored_conditions)

    sensor.update()

    assert sensor.device_state_attributes == {}


conditions = MONITORED_CONDITIONS
conditions.remove('dividends')


@pytest.mark.parametrize("condition", conditions)
def test_monitored_condition(condition):
    """Test monitored condition."""
    stock = 5431
    name = 'Avanza Stock {0}'.format(stock)
    monitored_conditions = [condition]

    sensor = AvanzaStockSensor(stock, name, monitored_conditions)

    sensor.update()

    assert condition in sensor.device_state_attributes


def test_dividends():
    """Test dividends."""
    stock = 5431
    name = 'Avanza Stock {0}'.format(stock)
    monitored_conditions = ['dividends']

    sensor = AvanzaStockSensor(stock, name, monitored_conditions)

    sensor.update()

    assert 'dividend0_amountPerShare' in sensor.device_state_attributes
    assert 'dividend0_exDate' in sensor.device_state_attributes
    assert 'dividend0_paymentDate' in sensor.device_state_attributes
