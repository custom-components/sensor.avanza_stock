# Avanza Stock Integration

This integration allows you to track stock prices and information from Avanza.se in Home Assistant.

## Installation

1. Install this integration via HACS (Home Assistant Community Store)
2. Restart Home Assistant
3. Go to **Settings** → **Devices & Services**
4. Click **+ Add Integration**
5. Search for "Avanza Stock" and select it

## Configuration

### Adding a Stock

1. In the integration setup, enter the **Stock ID** from Avanza.se
2. Optionally provide:
   - **Name**: Custom name for the stock (defaults to "Avanza Stock {ID}")
   - **Number of Shares**: Your current shareholding
   - **Purchase Date**: When you bought the shares
   - **Purchase Price**: Price per share when purchased

### Stock ID

To find the Stock ID:
1. Go to [avanza.se](https://www.avanza.se)
2. Search for your stock
3. The ID is in the URL: `https://www.avanza.se/aktier/om-aktien.html/{ID}`

### Updating Configuration

After adding a stock, you can modify its settings:
1. Go to **Settings** → **Devices & Services**
2. Find your Avanza Stock integration
3. Click **Configure**
4. Update the settings as needed

## Sensors

The integration creates sensors for various stock data including:
- Current price and change
- High/low prices
- Volume and market cap
- Dividend information
- Historical price data

## Features

- Real-time stock data from Avanza.se
- Automatic currency conversion
- Trending indicators
- Comprehensive stock information
- Easy GUI configuration

## Support

For issues and feature requests, please visit the [GitHub repository](https://github.com/custom-components/sensor.avanza_stock).
