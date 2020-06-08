"""Constants for avanza_stock."""
__version__ = "1.0.3"

DEFAULT_NAME = "Avanza Stock"

CONF_STOCK = "stock"
CONF_SHARES = "shares"
CONF_PURCHASE_PRICE = "purchase_price"
CONF_CONVERSION_RATE = "conversion_rate"

MONITORED_CONDITIONS = [
    "change",
    "changePercent",
    "country",
    "currency",
    "dividends",
    "flagCode",
    "hasInvestmentFees",
    "highestPrice",
    "id",
    "isin",
    "lastPrice",
    "lastPriceUpdated",
    "loanFactor",
    "lowestPrice",
    "marketList",
    "marketMakerExpected",
    "marketPlace",
    "marketTrades",
    "morningStarFactSheetUrl",
    "name",
    "numberOfOwners",
    "orderDepthReceivedTime",
    "priceAtStartOfYear",
    "priceFiveYearsAgo",
    "priceOneMonthAgo",
    "priceOneWeekAgo",
    "priceOneYearAgo",
    "priceSixMonthsAgo",
    "priceThreeMonthsAgo",
    "priceThreeYearsAgo",
    "pushPermitted",
    "quoteUpdated",
    "shortSellable",
    "superLoan",
    "tickerSymbol",
    "totalValueTraded",
    "totalVolumeTraded",
    "tradable",
]

MONITORED_CONDITIONS_KEYRATIOS = [
    "directYield",
    "priceEarningsRatio",
    "volatility",
]
MONITORED_CONDITIONS += MONITORED_CONDITIONS_KEYRATIOS

MONITORED_CONDITIONS_COMPANY = [
    "description",
    "marketCapital",
    "sector",
    "totalNumberOfShares",
]
MONITORED_CONDITIONS += MONITORED_CONDITIONS_COMPANY

MONITORED_CONDITIONS_DIVIDENDS = [
    "amountPerShare",
    "exDate",
    "paymentDate",
]

MONITORED_CONDITIONS_DEFAULT = [
    "change",
    "changePercent",
    "name",
]

CURRENCY_ATTRIBUTE = [
    "change",
    "highestPrice",
    "lastPrice",
    "lowestPrice",
    "priceAtStartOfYear",
    "priceFiveYearsAgo",
    "priceOneMonthAgo",
    "priceOneWeekAgo",
    "priceOneYearAgo",
    "priceSixMonthsAgo",
    "priceThreeMonthsAgo",
    "priceThreeYearsAgo",
    "totalValueTraded",
    "marketCapital",
    "amountPerShare",
    "changeOneWeek",
    "changeOneMonth",
    "changeThreeMonths",
    "changeSixMonths",
    "changeOneYear",
    "changeThreeYears",
    "changeFiveYears",
    "changeCurrentYear",
    "totalChangeOneWeek",
    "totalChangeOneMonth",
    "totalChangeThreeMonths",
    "totalChangeSixMonths",
    "totalChangeOneYear",
    "totalChangeThreeYears",
    "totalChangeFiveYears",
    "totalChangeCurrentYear",
    "totalValue",
    "totalChange",
    "profitLoss",
    "totalProfitLoss",
]
