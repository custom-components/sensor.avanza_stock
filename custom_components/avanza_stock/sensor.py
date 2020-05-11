"""
Support for getting stock data from avanza.se.

For more details about this platform, please refer to the documentation at
https://github.com/custom-components/sensor.avanza_stock/blob/master/README.md
"""
import logging
from datetime import datetime, timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_MONITORED_CONDITIONS, CONF_NAME
from homeassistant.helpers.entity import Entity

import pyavanza

from custom_components.avanza_stock.const import (
    CONF_STOCK,
    CONF_SHARES,
    MONITORED_CONDITIONS_DEFAULT,
    MONITORED_CONDITIONS,
    DEFAULT_NAME,
    MONITORED_CONDITIONS_KEYRATIOS,
    MONITORED_CONDITIONS_COMPANY,
    MONITORED_CONDITIONS_DIVIDENDS,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=60)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_STOCK): cv.positive_int,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_SHARES): vol.Coerce(float),
        vol.Optional(
            CONF_MONITORED_CONDITIONS, default=MONITORED_CONDITIONS_DEFAULT
        ): vol.All(cv.ensure_list, [vol.In(MONITORED_CONDITIONS)]),
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Avanza Stock sensor."""
    stock = config.get(CONF_STOCK)
    name = config.get(CONF_NAME)
    shares = config.get(CONF_SHARES)
    if name is None:
        name = DEFAULT_NAME + " " + str(stock)
    monitored_conditions = config.get(CONF_MONITORED_CONDITIONS)
    entities = [AvanzaStockSensor(stock, name, shares, monitored_conditions)]
    async_add_entities(entities, True)


class AvanzaStockSensor(Entity):
    """Representation of a Avanza Stock sensor."""

    def __init__(self, stock, name, shares, monitored_conditions):
        """Initialize a Avanza Stock sensor."""
        self._stock = stock
        self._name = name
        self._shares = shares
        self._monitored_conditions = monitored_conditions
        self._icon = "mdi:cash"
        self._state = 0
        self._state_attributes = {}
        self._unit_of_measurement = ""

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._state_attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self):
        """Update state and attributes."""
        data = pyavanza.get_stock(self._stock)
        if data:
            keyRatios = data.get("keyRatios", {})
            company = data.get("company", {})
            dividends = data.get("dividends", [])
            self._state = data["lastPrice"]
            self._unit_of_measurement = data["currency"]
            for condition in self._monitored_conditions:
                if condition in MONITORED_CONDITIONS_KEYRATIOS:
                    self._state_attributes[condition] = keyRatios.get(condition, None)
                elif condition in MONITORED_CONDITIONS_COMPANY:
                    self._state_attributes[condition] = company.get(condition, None)
                elif condition == "dividends":
                    self.update_dividends(dividends)
                else:
                    self._state_attributes[condition] = data.get(condition, None)

                if condition == "change":
                    for (change, price) in [
                        ("changeOneWeek", "priceOneWeekAgo"),
                        ("changeOneMonth", "priceOneMonthAgo"),
                        ("changeThreeMonths", "priceThreeMonthsAgo"),
                        ("changeSixMonths", "priceSixMonthsAgo"),
                        ("changeOneYear", "priceOneYearAgo"),
                        ("changeThreeYears", "priceThreeYearsAgo"),
                        ("changeFiveYears", "priceFiveYearsAgo"),
                        ("changeCurrentYear", "priceAtStartOfYear"),
                    ]:
                        if price in data:
                            self._state_attributes[change] = round(
                                data["lastPrice"] - data[price], 2
                            )
                        else:
                            self._state_attributes[change] = "unknown"

                    if self._shares is not None:
                        for (change, price) in [
                            ("totalChangeOneWeek", "priceOneWeekAgo"),
                            ("totalChangeOneMonth", "priceOneMonthAgo"),
                            ("totalChangeThreeMonths", "priceThreeMonthsAgo",),
                            ("totalChangeSixMonths", "priceSixMonthsAgo"),
                            ("totalChangeOneYear", "priceOneYearAgo"),
                            ("totalChangeThreeYears", "priceThreeYearsAgo",),
                            ("totalChangeFiveYears", "priceFiveYearsAgo"),
                            ("totalChangeCurrentYear", "priceAtStartOfYear",),
                        ]:
                            if price in data:
                                self._state_attributes[change] = round(
                                    self._shares * (data["lastPrice"] - data[price]), 2
                                )
                            else:
                                self._state_attributes[change] = "unknown"

                if condition == "changePercent":
                    for (change, price) in [
                        ("changePercentOneWeek", "priceOneWeekAgo"),
                        ("changePercentOneMonth", "priceOneMonthAgo"),
                        ("changePercentThreeMonths", "priceThreeMonthsAgo",),
                        ("changePercentSixMonths", "priceSixMonthsAgo"),
                        ("changePercentOneYear", "priceOneYearAgo"),
                        ("changePercentThreeYears", "priceThreeYearsAgo"),
                        ("changePercentFiveYears", "priceFiveYearsAgo"),
                        ("changePercentCurrentYear", "priceAtStartOfYear"),
                    ]:
                        if price in data:
                            self._state_attributes[change] = round(
                                100 * (data["lastPrice"] - data[price]) / data[price], 2
                            )
                        else:
                            self._state_attributes[change] = "unknown"

        if self._shares is not None:
            self._state_attributes["shares"] = self._shares
            self._state_attributes["totalValue"] = self._shares * data["lastPrice"]
            self._state_attributes["totalChange"] = self._shares * data["change"]

    def update_dividends(self, dividends):
        """Update dividend attributes."""
        # Create empty dividend attributes, will be overwritten with valid
        # data if information is available
        for dividend_condition in MONITORED_CONDITIONS_DIVIDENDS:
            attribute = "dividend0_{0}".format(dividend_condition)
            self._state_attributes[attribute] = "unknown"

        # Check that each dividend has the attributes needed.
        # Dividends from the past sometimes misses attributes
        # but we are not interested in them anyway.
        for i, dividend in reversed(list(enumerate(dividends))):
            has_all_attributes = True
            for dividend_condition in MONITORED_CONDITIONS_DIVIDENDS:
                if dividend_condition not in dividend:
                    has_all_attributes = False
            if not has_all_attributes:
                del dividends[i]
            elif dividend["amountPerShare"] == 0:
                del dividends[i]

        # Sort dividends by payment date
        dividends = sorted(dividends, key=lambda d: d["paymentDate"])

        # Get todays date
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Loop over data
        i = 0
        for dividend in dividends:
            paymentDate = datetime.strptime(dividend["paymentDate"], "%Y-%m-%d")
            if paymentDate >= today:
                for dividend_condition in MONITORED_CONDITIONS_DIVIDENDS:
                    attribute = "dividend{0}_{1}".format(i, dividend_condition)
                    self._state_attributes[attribute] = dividend[dividend_condition]
                i += 1
