"""
Support for getting stock data from avanza.se.

Data is fetched from https://www.avanza.se/_mobile/market/stock/{STOCK}

Example configuration

sensor:
  - platform: avanza
    stock: 1000

Example advanced configuration

sensor:
  - platform: avanza
    name: Home Assistant Inc.
    stock: 1000
"""
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

__version__ = '0.0.1'

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Avanza Stock'

CONF_STOCK = 'stock'

SCAN_INTERVAL = timedelta(minutes=60)

MONITORED_CONDITIONS = [
    # 'priceOneYearAgo',
    # 'priceOneWeekAgo',
    # 'priceOneMonthAgo',
    # 'priceSixMonthsAgo',
    # 'priceAtStartOfYear',
    # 'priceThreeYearsAgo',
    # 'priceFiveYearsAgo',
    # 'priceThreeMonthsAgo',
    # 'marketPlace',
    # 'marketList',
    # 'morningStarFactSheetUrl',
    'name',
    'id',
    # 'country',
    # 'currency',
    # 'isin',
    # 'tradable',
    'highestPrice',
    'lowestPrice',
    # 'lastPrice',
    # 'lastPriceUpdated',
    'change',
    'changePercent',
    'totalVolumeTraded',
    'totalValueTraded',
    # 'shortSellable',
    # 'loanFactor',
    # 'tickerSymbol',
    # 'flagCode',
    # 'quoteUpdated',
    # 'hasInvestmentFees',
    # 'keyRatios',
    # 'numberOfOwners',
    # 'superLoan',
    # 'pushPermitted',
    # 'dividends',
    # 'relatedStocks',
    # 'company',
    # 'orderDepthLevels',
    # 'marketMakerExpected',
    # 'orderDepthReceivedTime',
    # 'latestTrades',
    # 'marketTrades',
    # 'annualMeetings',
    # 'companyReports',
    # 'brokerTradeSummary',
    # 'companyOwners',
]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STOCK): cv.positive_int,
    vol.Optional(CONF_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Avanza Stock sensor."""
    stock = config.get(CONF_STOCK)
    name = config.get(CONF_NAME)
    if config.get(CONF_NAME) is None:
        name = DEFAULT_NAME + ' ' + str(stock)
    add_entities([AvanzaStockSensor(stock, name)], True)


class AvanzaStockSensor(Entity):
    """Representation of a Avanza Stock sensor."""

    def __init__(self, stock, name):
        """Initialize a Avanza Stock sensor."""
        self._stock = stock
        self._name = name
        self._icon = "mdi:cash"
        self._state = 0
        self._state_attributes = {}
        self._unit_of_measurement = ''

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
        """Get the latest data from the Avanza Stock API."""
        url = 'https://www.avanza.se/_mobile/market/stock/{}'
        url = url.format(self._stock)
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            data = response.json()
            self._state = data['lastPrice']
            self._unit_of_measurement = data['currency']
            for condition in MONITORED_CONDITIONS:
                self._state_attributes[condition] = data[condition]
