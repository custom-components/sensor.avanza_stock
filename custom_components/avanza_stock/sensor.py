"""
Support for getting stock data from avanza.se.

For more details about this platform, please refer to the documentation at
https://github.com/custom-components/sensor.avanza_stock/blob/master/README.md
"""
import logging
from datetime import datetime, timedelta

import homeassistant.helpers.config_validation as cv
import pyavanza
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_CURRENCY,
    CONF_ID,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
)
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity

from custom_components.avanza_stock.const import (
    CHANGE_PERCENT_PRICE_MAPPING,
    CHANGE_PRICE_MAPPING,
    CONF_CONVERSION_CURRENCY,
    CONF_INVERT_CONVERSION_CURRENCY,
    CONF_PURCHASE_DATE,
    CONF_PURCHASE_PRICE,
    CONF_SHARES,
    CONF_STOCK,
    CURRENCY_ATTRIBUTE,
    DEFAULT_NAME,
    MONITORED_CONDITIONS,
    MONITORED_CONDITIONS_COMPANY,
    MONITORED_CONDITIONS_DEFAULT,
    MONITORED_CONDITIONS_DIVIDENDS,
    MONITORED_CONDITIONS_KEYRATIOS,
    TOTAL_CHANGE_PRICE_MAPPING,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=60)

STOCK_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ID): cv.positive_int,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_SHARES): vol.Coerce(float),
        vol.Optional(CONF_PURCHASE_DATE): cv.string,
        vol.Optional(CONF_PURCHASE_PRICE): vol.Coerce(float),
        vol.Optional(CONF_CONVERSION_CURRENCY): cv.positive_int,
        vol.Optional(CONF_INVERT_CONVERSION_CURRENCY, default=False): cv.boolean,
        vol.Optional(CONF_CURRENCY): cv.string,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_STOCK): vol.Any(
            cv.positive_int, vol.All(cv.ensure_list, [STOCK_SCHEMA])
        ),
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_SHARES): vol.Coerce(float),
        vol.Optional(CONF_PURCHASE_DATE): cv.string,
        vol.Optional(CONF_PURCHASE_PRICE): vol.Coerce(float),
        vol.Optional(CONF_CONVERSION_CURRENCY): cv.positive_int,
        vol.Optional(CONF_INVERT_CONVERSION_CURRENCY, default=False): cv.boolean,
        vol.Optional(CONF_CURRENCY): cv.string,
        vol.Optional(
            CONF_MONITORED_CONDITIONS, default=MONITORED_CONDITIONS_DEFAULT
        ): vol.All(cv.ensure_list, [vol.In(MONITORED_CONDITIONS)]),
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Avanza Stock sensor."""
    session = async_create_clientsession(hass)
    monitored_conditions = config.get(CONF_MONITORED_CONDITIONS)
    stock = config.get(CONF_STOCK)
    entities = []
    if isinstance(stock, int):
        name = config.get(CONF_NAME)
        shares = config.get(CONF_SHARES)
        purchase_date = config.get(CONF_PURCHASE_DATE)
        purchase_price = config.get(CONF_PURCHASE_PRICE)
        conversion_currency = config.get(CONF_CONVERSION_CURRENCY)
        invert_conversion_currency = config.get(CONF_INVERT_CONVERSION_CURRENCY)
        currency = config.get(CONF_CURRENCY)
        if name is None:
            name = DEFAULT_NAME + " " + str(stock)
        entities.append(
            AvanzaStockSensor(
                hass,
                stock,
                name,
                shares,
                purchase_date,
                purchase_price,
                conversion_currency,
                invert_conversion_currency,
                currency,
                monitored_conditions,
                session,
            )
        )
        _LOGGER.info("Tracking %s [%d] using Avanza" % (name, stock))
    else:
        for s in stock:
            id = s.get(CONF_ID)
            name = s.get(CONF_NAME)
            if name is None:
                name = DEFAULT_NAME + " " + str(id)
            shares = s.get(CONF_SHARES)
            purchase_date = s.get(CONF_PURCHASE_DATE)
            purchase_price = s.get(CONF_PURCHASE_PRICE)
            conversion_currency = s.get(CONF_CONVERSION_CURRENCY)
            invert_conversion_currency = s.get(CONF_INVERT_CONVERSION_CURRENCY)
            currency = s.get(CONF_CURRENCY)
            entities.append(
                AvanzaStockSensor(
                    hass,
                    id,
                    name,
                    shares,
                    purchase_date,
                    purchase_price,
                    conversion_currency,
                    invert_conversion_currency,
                    currency,
                    monitored_conditions,
                    session,
                )
            )
            _LOGGER.info("Tracking %s [%d] using Avanza" % (name, id))
    async_add_entities(entities, True)


class AvanzaStockSensor(Entity):
    """Representation of a Avanza Stock sensor."""

    def __init__(
        self,
        hass,
        stock,
        name,
        shares,
        purchase_date,
        purchase_price,
        conversion_currency,
        invert_conversion_currency,
        currency,
        monitored_conditions,
        session,
    ):
        """Initialize a Avanza Stock sensor."""
        self._hass = hass
        self._stock = stock
        self._name = name
        self._shares = shares
        self._purchase_date = purchase_date
        self._purchase_price = purchase_price
        self._conversion_currency = conversion_currency
        self._invert_conversion_currency = invert_conversion_currency
        self._currency = currency
        self._monitored_conditions = monitored_conditions
        self._session = session
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

    async def async_update(self):
        """Update state and attributes."""
        data = await pyavanza.get_stock_async(self._session, self._stock)
        data_conversion_currency = None
        if self._conversion_currency:
            data_conversion_currency = await pyavanza.get_stock_async(
                self._session, self._conversion_currency
            )
        if data:
            self._update_state(data)
            self._update_unit_of_measurement(data)
            self._update_state_attributes(data)
            if data_conversion_currency:
                self._update_conversion_rate(data_conversion_currency)
            if self._currency:
                self._unit_of_measurement = self._currency

    def _update_state(self, data):
        self._state = data["lastPrice"]

    def _update_unit_of_measurement(self, data):
        self._unit_of_measurement = data["currency"]

    def _update_state_attributes(self, data):
        for condition in self._monitored_conditions:
            if condition in MONITORED_CONDITIONS_KEYRATIOS:
                self._update_key_ratios(data, condition)
            elif condition in MONITORED_CONDITIONS_COMPANY:
                self._update_company(data, condition)
            elif condition == "dividends":
                self._update_dividends(data)
            else:
                self._state_attributes[condition] = data.get(condition, None)

            if condition == "change":
                for (change, price) in CHANGE_PRICE_MAPPING:
                    if price in data:
                        self._state_attributes[change] = round(
                            data["lastPrice"] - data[price], 2
                        )
                    else:
                        self._state_attributes[change] = "unknown"

                if self._shares is not None:
                    for (change, price) in TOTAL_CHANGE_PRICE_MAPPING:
                        if price in data:
                            self._state_attributes[change] = round(
                                self._shares * (data["lastPrice"] - data[price]), 2
                            )
                        else:
                            self._state_attributes[change] = "unknown"

            if condition == "changePercent":
                for (change, price) in CHANGE_PERCENT_PRICE_MAPPING:
                    if price in data:
                        self._state_attributes[change] = round(
                            100 * (data["lastPrice"] - data[price]) / data[price], 2
                        )
                    else:
                        self._state_attributes[change] = "unknown"

        if self._shares is not None:
            self._state_attributes["shares"] = self._shares
            self._state_attributes["totalValue"] = round(
                self._shares * data["lastPrice"], 2
            )
            self._state_attributes["totalChange"] = round(
                self._shares * data["change"], 2
            )

        self._update_profit_loss(data["lastPrice"])

    def _update_key_ratios(self, data, attr):
        key_ratios = data.get("keyRatios", {})
        self._state_attributes[attr] = key_ratios.get(attr, None)

    def _update_company(self, data, attr):
        company = data.get("company", {})
        self._state_attributes[attr] = company.get(attr, None)

    def _update_profit_loss(self, price):
        if self._purchase_date is not None:
            self._state_attributes["purchaseDate"] = self._purchase_date
        if self._purchase_price is not None:
            self._state_attributes["purchasePrice"] = self._purchase_price
            self._state_attributes["profitLoss"] = round(
                price - self._purchase_price, 2
            )
            self._state_attributes["profitLossPercentage"] = round(
                100 * (price - self._purchase_price) / self._purchase_price, 2
            )

            if self._shares is not None:
                self._state_attributes["totalProfitLoss"] = round(
                    self._shares * (price - self._purchase_price), 2
                )

    def _update_conversion_rate(self, data):
        rate = data["lastPrice"]
        if self._invert_conversion_currency:
            rate = 1.0 / rate
        self._state = round(self._state * rate, 2)
        if self._invert_conversion_currency:
            self._unit_of_measurement = data["name"].split("/")[0]
        else:
            self._unit_of_measurement = data["name"].split("/")[1]
        for attribute in self._state_attributes:
            if (
                attribute in CURRENCY_ATTRIBUTE
                and self._state_attributes[attribute] is not None
                and self._state_attributes[attribute] != "unknown"
            ):
                self._state_attributes[attribute] = round(
                    self._state_attributes[attribute] * rate, 2
                )
        self._update_profit_loss(self._state)

    def _update_dividends(self, data):
        dividends = data.get("dividends", [])
        # Create empty dividend attributes, will be overwritten with valid
        # data if information is available
        for key in self._state_attributes:
            if key.startswith("dividend"):
                self._state_attributes.pop(key)
        for dividend_condition in MONITORED_CONDITIONS_DIVIDENDS:
            attribute = "dividend0_{}".format(dividend_condition)
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

        # Get today's date
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Loop over data
        i = 0
        for dividend in dividends:
            paymentDate = datetime.strptime(dividend["paymentDate"], "%Y-%m-%d")
            if paymentDate >= today:
                for dividend_condition in MONITORED_CONDITIONS_DIVIDENDS:
                    attribute = "dividend{}_{}".format(i, dividend_condition)
                    self._state_attributes[attribute] = dividend[dividend_condition]
                i += 1
