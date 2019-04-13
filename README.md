# sensor.avanza_stock
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![custom_updater][customupdaterbadge]][customupdater]
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Custom component to get stock data from [Avanza](https://www.avanza.se) for [Home Assistant](https://www.home-assistant.io/)._

## Installation
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `avanza_stock`.
4. Download _all_ the files from the `custom_components/avanza_stock/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add a sensor `- platform: avanza_stock` to your HA configuration.

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/avanza_stock/__init__.py
custom_components/avanza_stock/sensor.py
```

## Configuration
key | type | description
:--- | :--- | :---
**platform (Required)** | string | `avanza_stock`
**stock (Required)** | number | The stock id, see below how to find it.
**name (Optional)** | string | Custom name for the sensor. Default `avanza_stock_{stock}`.
**monitored_conditions (Optional)** | list | Defines the attributes of the sensor, see below.

### Monitored conditions
The following attributes are tracked by default
* change
* changePercent
* name

Full list of available attributes.
* brokerTradeSummary
* change
* changePercent
* country
* currency
* description
* directYield
* dividends
* flagCode
* hasInvestmentFees
* highestPrice
* id
* isin
* lastPrice
* lastPriceUpdated
* loanFactor
* lowestPrice
* marketCapital
* marketList
* marketMakerExpected
* marketPlace
* marketTrades
* morningStarFactSheetUrl
* name
* numberOfOwners
* orderDepthReceivedTime
* priceAtStartOfYear
* priceEarningsRatio
* priceFiveYearsAgo
* priceOneMonthAgo
* priceOneWeekAgo
* priceOneYearAgo
* priceSixMonthsAgo
* priceThreeMonthsAgo
* priceThreeYearsAgo
* pushPermitted
* quoteUpdated
* sector
* shortSellable
* superLoan
* tickerSymbol
* totalNumberOfShares
* totalValueTraded
* totalVolumeTraded
* tradable
* volatility

### Finding stock id
Got to [Avanza](https://www.avanza.se) and search for the stock you want to track. In the resulting url there is a number, this is the stock id needed for the configuration. Even though it is a Swedish bank it is possible to find stocks from the following countries:
* Sweden
* USA
* Denmark
* Norway
* Finland
* Canada
* Belgium
* France
* Italy
* Netherlands
* Portugal
* Germany

## Example
**Configuration with default settings:**
```yaml
sensor:
  - platform: avanza_stock
    stock: 5361
```

**Configuration with custom settings:**
```yaml
sensor:
  - platform: avanza_stock
    name: Avanza Bank Holding
    stock: 5361
    monitored_conditions:
      - totalVolumeTraded
      - totalValueTraded
```

## Usage
**Automation to send summary after stock market closes on workdays using telegram:**
```yaml
# Telegram Stock Summary
- alias: 'Telegram Stock Summary'
  initial_state: true

  trigger:
    - platform: time
      at: '18:00:00'

  condition:
    condition: state
    entity_id: binary_sensor.workday
    state: 'on'

  action:
    - service: notify.telegram
      data:
        message: '
<b>Stock Summary {{ states.sensor.date.state }}</b>
<code>
{{ states.sensor.avanza_stock_5361.attributes.name }} : {{ states.sensor.avanza_stock_5361.attributes.changePercent }}
</code>
'
```
Note: This automation could be further improved by looping over all sensors and checking if their entity_id starts with `sensor.avanza_stock_` and then extract the information.

## Changelog
* 0.0.6 - Make sure dividend payment date has not passed
* 0.0.5 - Add dividends information
* 0.0.4 - Add companny information (description, marketCapital, sector, totalNumberOfShares)
* 0.0.3 - Add key ratios (directYield, priceEarningsRatio, volatility)
* 0.0.2 - Configure monitored conditions
* 0.0.1 - Initial version

[buymecoffee]: https://www.buymeacoffee.com/claha
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/sensor.avanza_stock.svg?style=for-the-badge
[commits]: https://github.com/custom-components/sensor.avanza_stock/commits/master
[customupdater]: https://github.com/custom-components/custom_updater
[customupdaterbadge]: https://img.shields.io/badge/custom__updater-true-success.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/custom-components/sensor.avanza_stock.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Claes%20Hallström%20%40claha-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/sensor.avanza_stock.svg?style=for-the-badge
[releases]: https://github.com/custom-components/sensor.avanza_stock/releases
