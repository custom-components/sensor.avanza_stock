"""Constants for avanza_stock."""
__version__ = "1.0.7"

DEFAULT_NAME = "Avanza Stock"

CONF_STOCK = "stock"
CONF_SHARES = "shares"
CONF_PURCHASE_PRICE = "purchase_price"
CONF_CONVERSION_CURRENCY = "conversion_currency"
CONF_INVERT_CONVERSION_CURRENCY = "invert_conversion_currency"

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

CHANGE_PRICE_MAPPING = [
    ("changeOneWeek", "priceOneWeekAgo"),
    ("changeOneMonth", "priceOneMonthAgo"),
    ("changeThreeMonths", "priceThreeMonthsAgo"),
    ("changeSixMonths", "priceSixMonthsAgo"),
    ("changeOneYear", "priceOneYearAgo"),
    ("changeThreeYears", "priceThreeYearsAgo"),
    ("changeFiveYears", "priceFiveYearsAgo"),
    ("changeCurrentYear", "priceAtStartOfYear"),
]

TOTAL_CHANGE_PRICE_MAPPING = [
    ("totalChangeOneWeek", "priceOneWeekAgo"),
    ("totalChangeOneMonth", "priceOneMonthAgo"),
    (
        "totalChangeThreeMonths",
        "priceThreeMonthsAgo",
    ),
    ("totalChangeSixMonths", "priceSixMonthsAgo"),
    ("totalChangeOneYear", "priceOneYearAgo"),
    (
        "totalChangeThreeYears",
        "priceThreeYearsAgo",
    ),
    ("totalChangeFiveYears", "priceFiveYearsAgo"),
    (
        "totalChangeCurrentYear",
        "priceAtStartOfYear",
    ),
]

CHANGE_PERCENT_PRICE_MAPPING = [
    ("changePercentOneWeek", "priceOneWeekAgo"),
    ("changePercentOneMonth", "priceOneMonthAgo"),
    (
        "changePercentThreeMonths",
        "priceThreeMonthsAgo",
    ),
    ("changePercentSixMonths", "priceSixMonthsAgo"),
    ("changePercentOneYear", "priceOneYearAgo"),
    ("changePercentThreeYears", "priceThreeYearsAgo"),
    ("changePercentFiveYears", "priceFiveYearsAgo"),
    ("changePercentCurrentYear", "priceAtStartOfYear"),
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
    "dividend0_amountPerShare",
    "dividend1_amountPerShare",
    "dividend2_amountPerShare",
    "dividend3_amountPerShare",
    "dividend4_amountPerShare",
    "dividend5_amountPerShare",
    "dividend6_amountPerShare",
    "dividend7_amountPerShare",
    "dividend8_amountPerShare",
    "dividend9_amountPerShare",
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
