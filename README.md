# sensor.avanza_stock

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Custom component to get stock data from [Avanza](https://www.avanza.se) for
[Home Assistant](https://www.home-assistant.io/)._

## Installation

- The easiest way is to install it with [HACS](https://hacs.xyz/). First install
[HACS](https://hacs.xyz/) if you don't have it yet. After installation you can
find this custom component in the HACS store under integrations.

- Alternatively, you can install it manually. Just copy paste the content of the
`sensor.avanza_stock/custom_components` folder in your `config/custom_components`
directory. As example, you will get the `sensor.py` file in the following path:
`/config/custom_components/avanza_stock/sensor.py`.

## Configuration

key | type | description
:--- | :--- | :---
**platform (Required)**                    | string        | `avanza_stock`
**stock (Required)**                       | number / list | Stock id or list of stocks, see [here](#stock-configuration) and [here](#finding-stock-or-conversion-currency).
**name (Optional)**                        | string        | Name of the sensor. Default `avanza_stock_{stock}`. Redundant if stock is defined as a list.
**shares (Optional)**                      | number        | Number of shar, can be fractional. Redundant if stock is defined as a list.
**purchase_date (Optional)**                | string        | Date when stock was purchased. Redundant if stock is defined as a list. Does not get processed further.
**purchase_price (Optional)**              | number        | Price paid when stock was purchased (per share). Redundant if stock is defined as a list.
**conversion_currency (Optional)**         | number        | Index id used for currency conversion, see [here](#finding-stock-or-conversion-currency).
**monitored_conditions (Optional)**        | list          | Attributes to monitor, see [here](#monitored-conditions).
**invert_conversion_currency (Optional)** | boolean       | Wether or not to invert the conversion currency, default false.
**currency (Optional)**                    | string        | Overwrite currency given by the api.

### Stock configuration

key | type | description
:--- | :--- | :---
**id (Required)**                          | number  | Stock id, see [here](#finding-stock-or-conversion-currency).
**name (Optional)**                        | string  | Name of the sensor. Default `avanza_stock_{stock}`.
**shares (Optional)**                      | number  | Number of shares, can be fractional.
**purchase_date (Optional)**               | string  | Date when stock was purchased. Does not get processed further.
**purchase_price (Optional)**              | number  | Price paid when stock was purchased (per share).
**conversion_currency (Optional)**         | number  | Index id used for currency conversion, see [here](#finding-stock-or-conversion-currency).
**invert_conversion_currency (Optional)** | boolean | Wether or not to invert the conversion currency, default false.
**currency (Optional)**                    | string  | Overwrite currency given by the api.

### Monitored conditions

If no `monitored_conditions` is defined, change, changePercent and name will be tracked. Full list of available attributes, see [here](custom_components/avanza_stock/const.py#L12) (With the new api change only change and changePercent is currently supported.)

### Finding stock or conversion currency

Got to [Avanza](https://www.avanza.se) and search for the stock you want to track. In the resulting url there is a number, this is the stock id needed for the configuration. Even though it is a Swedish bank it is possible to find stocks from the following countries: Sweden, USA, Denmark, Norway, Finland, Canada, Belgium, France, Italy, Netherlands, Portugal and Germany. To find conversion currencies search for example "USD/SEK" and look for the id in the resulting url. If you can not find your conversion try and search the reverse (NOK/SEK instead of SEK/NOK) and use the `invert_conversion_currency` to get your preffered currency.

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

**Configuration with multiple stocks:**

```yaml
sensor:
  - platform: avanza_stock
    stock:
      - id: 5361
        name: Avanza Bank Holding
      - id: 8123
        name: Home Assistant
    monitored_conditions:
      - totalVolumeTraded
      - totalValueTraded
```

**Configuration with conversion currency:**

```yaml
sensor:
  - platform: avanza_stock
    stock:
      - id: 238449
        name: TESLA USD
        shares: 1
        purchase_price: 600
      - id: 238449
        name: TESLA SEK
        shares: 1
        conversion_currency: 19000
        purchase_price: 7000
      - id: 5361
        name: Avanza Bank Holding (NOK)
        conversion_currency: 53293
        invert_conversion_currency: true
```

## Usage

**Automation to send summary at 18:00 using telegram:**

```yaml
# Telegram Stock Summary
- alias: 'Telegram Stock Summary'
  initial_state: true

  trigger:
    - platform: time
      at: '18:00:00'

  action:
    - service: notify.telegram
      data:
        message: '
<b>Stock Summary </b>
<code>
{{ states.sensor.avanza_stock_5361.attributes.name }} : {{ states.sensor.avanza_stock_5361.attributes.changePercent }}
</code>
'
```

## Changelog

- 1.1.1  - Fix historical changes
- 1.1.0  - Use the new api
- 1.0.12 - Add unique id
- 1.0.11 - Rename device state attributes
- 1.0.10 - Safely remove divident attributes
- 1.0.9  - Add purchase date attribute (string manually set by user)
- 1.0.8  - Correct profit/loss when using conversion currency
- 1.0.7  - Overwrite currency given by the api
- 1.0.6  - Correct unit when using conversion currency
- 1.0.5  - Add option to invert conversion currency
- 1.0.4  - Configure conversion currency and define purchase price
- 1.0.3  - Allow to define multiple stocks
- 1.0.2  - Async update
- 1.0.1  - Allow fractional shares, add more change attributes
- 1.0.0  - Add number of shares as optional configuration
- 0.0.10 - Clean up monitored conditions
- 0.0.9  - Compare payment date with today's date, ignore time
- 0.0.8  - Ignore dividend if amount is zero, add resources.json and manfiest.json
- 0.0.7  - Changed to async setup
- 0.0.6  - Make sure dividend payment date has not passed
- 0.0.5  - Add dividends information
- 0.0.4  - Add companny information (description, marketCapital, sector, totalNumberOfShares)
- 0.0.3  - Add key ratios (directYield, priceEarningsRatio, volatility)
- 0.0.2  - Configure monitored conditions
- 0.0.1  - Initial version

[buymecoffee]: https://www.buymeacoffee.com/claha
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/sensor.avanza_stock.svg?style=for-the-badge
[commits]: https://github.com/custom-components/sensor.avanza_stock/commits/master
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/custom-components/sensor.avanza_stock.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Claes%20Hallström%20%40claha-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/sensor.avanza_stock.svg?style=for-the-badge
[releases]: https://github.com/custom-components/sensor.avanza_stock/releases
