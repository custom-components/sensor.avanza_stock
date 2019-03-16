# sensor.avanza_stock
Custom component to get stock data from Avanza for [Home Assistant](https://www.home-assistant.io/).

## Installation
1. Create a `custom_components` folder in your configuration folder, if you don't already have one.
2. Create a folder named `avanza_stock` inside the `custom_components` folder.
3. Put the `sensor.py` and `__init__.py` file in there (if you copy and paste the code, use [raw version](https://raw.githubusercontent.com/claha/sensor.avanza_stock/master/custom_components/avanza_stock/sensor.py)).
4. Update `configuration.yaml` using the config options below.
5. **You will need to restart after installation for the component to start working.**

## Configuration
key | type | description
:--- | :--- | :---
**platform (Required)** | string | `avanza_stock`
**stock (Required)** | number | The stock id, see below how to find it.
**name (Optional)** | string | Custom name for the sensor. Default `avanza_stock_{stock}`.

### Attributes
The sensor has the following attributes. 
* name
* id
* highestPrice
* lowestPrice
* change
* changePercent
* totalVolumeTraded
* totalValueTraded

There are many more available attributes, check source code, which can be added uppon request. In a future implementation all attributes will be available and it will be possible to configure which ones to track.

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
**Configuration with default name:**
```yaml
sensor:
  - platform: avanza_stock
    stock: 5361
```

**Configuration with custom name:**
```yaml
sensor:
  - platform: avanza_stock
    stock: 5361
    name: Avanza Bank Holding
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
* 0.0.1 - Initial version