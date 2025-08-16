"""
Support for getting stock data from avanza.se.

For more details about this platform, please refer to the documentation at
https://github.com/custom-components/sensor.avanza_stock/blob/master/README.md
"""
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import pyavanza
import voluptuous as vol
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_CURRENCY,
    CONF_ID,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
)
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from custom_components.avanza_stock.const import (
    ATTR_TRENDING,
    CHANGE_PERCENT_PRICE_MAPPING,
    CHANGE_PRICE_MAPPING,
    CONF_CONVERSION_CURRENCY,
    CONF_INVERT_CONVERSION_CURRENCY,
    CONF_PURCHASE_DATE,
    CONF_PURCHASE_PRICE,
    CONF_SHARES,
    CONF_SHOW_TRENDING_ICON,
    CONF_STOCK,
    CURRENCY_ATTRIBUTE,
    DEFAULT_NAME,
    DEFAULT_SHOW_TRENDING_ICON,
    MONITORED_CONDITIONS,
    MONITORED_CONDITIONS_COMPANY,
    MONITORED_CONDITIONS_DEFAULT,
    MONITORED_CONDITIONS_DIVIDENDS,
    MONITORED_CONDITIONS_KEYRATIOS,
    MONITORED_CONDITIONS_LISTING,
    MONITORED_CONDITIONS_PRICE,
    MONITORED_CONDITIONS_QUOTE,
    PRICE_MAPPING,
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
            CONF_SHOW_TRENDING_ICON, default=DEFAULT_SHOW_TRENDING_ICON
        ): cv.boolean,
        vol.Optional(
            CONF_MONITORED_CONDITIONS, default=MONITORED_CONDITIONS_DEFAULT
        ): vol.All(cv.ensure_list, [vol.In(MONITORED_CONDITIONS)]),
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Avanza Stock sensor."""
    session = async_create_clientsession(hass)
    monitored_conditions = config.get(CONF_MONITORED_CONDITIONS)
    show_trending_icon = config.get(CONF_SHOW_TRENDING_ICON)
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
                show_trending_icon,
            )
        )
        _LOGGER.debug("Tracking %s [%d] using Avanza" % (name, stock))
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
                    show_trending_icon,
                )
            )
            _LOGGER.debug("Tracking %s [%d] using Avanza" % (name, id))
    async_add_entities(entities, True)


class AvanzaStockSensor(SensorEntity):
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
        show_trending_icon,
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
        self._show_trending_icon = show_trending_icon
        self._icon = "mdi:cash"
        self._state = 0
        self._state_attributes = {}
        self._unit_of_measurement = ""
        self._previous_close = None

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
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._state_attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def unique_id(self):
        """Return the unique id."""
        return f"{self._stock}_{self._name}_stock"

    @property
    def state_class(self):
        """Return the state class."""
        return SensorStateClass.MEASUREMENT

    @property
    def device_class(self):
        """Return the device class."""
        return SensorDeviceClass.MONETARY

    async def async_update(self):
        """Update state and attributes."""
        data_conversion_currency = None
        if self._stock == 0:  # Non trackable, i.e. manual
            data = {
                "name": self._name.split(" ", 1)[1],
                "unit_of_measurement": self._currency,
                "quote": {
                    "last": self._purchase_price,
                    "change": 0,
                    "changePercent": 0,
                },
                "historicalClosingPrices": {
                    "oneWeek": self._purchase_price,
                    "oneMonth": self._purchase_price,
                    "threeMonths": self._purchase_price,
                    "oneYear": self._purchase_price,
                    "threeYears": self._purchase_price,
                    "fiveYears": self._purchase_price,
                    "tenYears": self._purchase_price,
                    "startOfYear": self._purchase_price,
                },
                "listing": {
                    "currency": self._currency,
                },
            }
        else:
            data = await pyavanza.get_stock_async(self._session, self._stock)
            if data["type"] == pyavanza.InstrumentType.ExchangeTradedFund:
                data = await pyavanza.get_etf_async(self._session, self._stock)
            if self._conversion_currency:
                data_conversion_currency = await pyavanza.get_stock_async(
                    self._session, self._conversion_currency
                )
        if data:
            # Store previous close price for trending calculation
            if "quote" in data and "last" in data["quote"] and self._stock != 0:
                # Try to get previous close from historical data or use the change to calculate it
                if (
                    "historicalClosingPrices" in data
                    and data["historicalClosingPrices"]
                ):
                    # Use any available historical closing price as reference
                    historical_prices = data["historicalClosingPrices"]
                    for period in ["oneWeek", "oneMonth", "threeMonths", "startOfYear"]:
                        if (
                            period in historical_prices
                            and historical_prices[period] is not None
                        ):
                            # For trending, we'll use current price vs previous close logic
                            # Avanza API provides 'change' which is current - previous close
                            change = data["quote"].get("change", 0)
                            self._previous_close = data["quote"]["last"] - change
                            break
                elif self._previous_close is None and "change" in data["quote"]:
                    # Calculate previous close from current price and change
                    change = data["quote"].get("change", 0)
                    self._previous_close = data["quote"]["last"] - change

            self._update_state(data)
            self._update_unit_of_measurement(data)
            self._update_state_attributes(data)
            self._update_trending_and_icon(data)
            if data_conversion_currency:
                self._update_conversion_rate(data_conversion_currency)
            if self._currency:
                self._unit_of_measurement = self._currency

    def _update_state(self, data):
        self._state = data["quote"]["last"]

    def _update_unit_of_measurement(self, data):
        self._unit_of_measurement = data["listing"]["currency"]

    def _update_state_attributes(self, data):
        for condition in self._monitored_conditions:
            if condition in MONITORED_CONDITIONS_KEYRATIOS:
                self._update_key_ratios(data, condition)
            elif condition in MONITORED_CONDITIONS_COMPANY:
                self._update_company(data, condition)
            elif condition in MONITORED_CONDITIONS_QUOTE:
                self._update_quote(data, condition)
            elif condition in MONITORED_CONDITIONS_LISTING:
                self._update_listing(data, condition)
            elif condition in MONITORED_CONDITIONS_PRICE:
                self._update_price(data, condition)
            elif condition == "dividends":
                self._update_dividends(data)
            elif condition == "id":
                self._state_attributes[condition] = data.get("orderbookId", None)
            else:
                self._state_attributes[condition] = data.get(condition, None)

            if condition == "change":
                for change, price in CHANGE_PRICE_MAPPING:
                    if price in data["historicalClosingPrices"]:
                        self._state_attributes[change] = round(
                            data["quote"]["last"]
                            - data["historicalClosingPrices"][price],
                            5,
                        )
                    else:
                        self._state_attributes[change] = "unknown"

                if self._shares is not None:
                    for change, price in TOTAL_CHANGE_PRICE_MAPPING:
                        if price in data["historicalClosingPrices"]:
                            self._state_attributes[change] = round(
                                self._shares
                                * (
                                    data["quote"]["last"]
                                    - data["historicalClosingPrices"][price]
                                ),
                                5,
                            )
                        else:
                            self._state_attributes[change] = "unknown"

            if condition == "changePercent":
                for change, price in CHANGE_PERCENT_PRICE_MAPPING:
                    if price in data["historicalClosingPrices"]:
                        self._state_attributes[change] = round(
                            100
                            * (
                                data["quote"]["last"]
                                - data["historicalClosingPrices"][price]
                            )
                            / data["historicalClosingPrices"][price],
                            3,
                        )
                    else:
                        self._state_attributes[change] = "unknown"

        if self._shares is not None:
            self._state_attributes["shares"] = self._shares
            self._state_attributes["totalValue"] = round(
                self._shares * data["quote"]["last"], 5
            )
            self._state_attributes["totalChange"] = round(
                self._shares * data["quote"]["change"], 5
            )

        self._update_profit_loss(data["quote"]["last"])

    def _update_key_ratios(self, data, attr):
        key_ratios = data.get("keyRatios", {})
        self._state_attributes[attr] = key_ratios.get(attr, None)

    def _update_company(self, data, attr):
        company = data.get("company", {})
        self._state_attributes[attr] = company.get(attr, None)

    def _update_quote(self, data, attr):
        quote = data.get("quote", {})
        self._state_attributes[attr] = quote.get(attr, None)

    def _update_listing(self, data, attr):
        listing = data.get("listing", {})
        if attr == "marketPlace":
            self._state_attributes[attr] = listing.get("marketPlaceName", None)
        elif attr == "flagCode":
            self._state_attributes[attr] = listing.get("countryCode", None)
        else:
            self._state_attributes[attr] = listing.get(attr, None)

    def _update_price(self, data, attr):
        prices = data.get("historicalClosingPrices", {})
        self._state_attributes[attr] = prices.get(PRICE_MAPPING[attr], None)

    def _update_profit_loss(self, price):
        if self._purchase_date is not None:
            self._state_attributes["purchaseDate"] = self._purchase_date
        if self._purchase_price is not None:
            self._state_attributes["purchasePrice"] = self._purchase_price
            self._state_attributes["profitLoss"] = round(
                price - self._purchase_price, 5
            )
            self._state_attributes["profitLossPercentage"] = round(
                100 * (price - self._purchase_price) / self._purchase_price, 3
            )

            if self._shares is not None:
                self._state_attributes["totalProfitLoss"] = round(
                    self._shares * (price - self._purchase_price), 5
                )

    def _update_conversion_rate(self, data):
        rate = data["quote"]["last"]
        if self._invert_conversion_currency:
            rate = 1.0 / rate
        self._state = round(self._state * rate, 5)
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
                    self._state_attributes[attribute] * rate, 5
                )
        self._update_profit_loss(self._state)

    def _update_dividends(self, data):
        if "keyIndicators" not in data:
            return
        if "dividend" not in data["keyIndicators"]:
            return

        dividend = data["keyIndicators"]["dividend"]
        for dividend_condition in MONITORED_CONDITIONS_DIVIDENDS:
            if dividend_condition not in dividend:
                continue
            attribute = "dividend_{}".format(dividend_condition)
            self._state_attributes[attribute] = dividend[dividend_condition]

    def _calc_trending_state(self) -> str | None:
        """Return the trending state for the stock."""
        if self._state is None or self._previous_close is None:
            return None

        if self._state > self._previous_close:
            return "up"
        if self._state < self._previous_close:
            return "down"

        return "neutral"

    def _update_trending_and_icon(self, data):
        """Update the trending state and icon based on price movement."""
        trending_state = self._calc_trending_state()

        # Set trending attribute if we have a valid state
        if trending_state is not None:
            self._state_attributes[ATTR_TRENDING] = trending_state

        # Set icon based on configuration and trending state
        if trending_state is not None and self._show_trending_icon:
            self._icon = f"mdi:trending-{trending_state}"
        else:
            # Fall back to default cash icon
            self._icon = "mdi:cash"
