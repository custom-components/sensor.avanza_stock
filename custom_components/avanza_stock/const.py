"""Constants for avanza_stock."""
__version__ = "1.3.0"

DEFAULT_NAME = "Avanza Stock"

CONF_STOCK = "stock"
CONF_SHARES = "shares"
CONF_PURCHASE_DATE = "purchase_date"
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
    "amount",
    "exDate",
    "exDateStatus",
    "paymentDate",
]

MONITORED_CONDITIONS_DEFAULT = [
    "change",
    "changePercent",
    "name",
]

MONITORED_CONDITIONS_QUOTE = [
    "change",
    "changePercent",
]

CHANGE_PRICE_MAPPING = [
    ("changeOneWeek", "oneWeek"),
    ("changeOneMonth", "oneMonth"),
    ("changeThreeMonths", "threeMonths"),
    ("changeOneYear", "oneYear"),
    ("changeThreeYears", "threeYears"),
    ("changeFiveYears", "fiveYears"),
    ("changeTenYears", "tenYears"),
    ("changeCurrentYear", "startOfYear"),
]

TOTAL_CHANGE_PRICE_MAPPING = [
    ("totalChangeOneWeek", "oneWeek"),
    ("totalChangeOneMonth", "oneMonth"),
    (
        "totalChangeThreeMonths",
        "threeMonths",
    ),
    ("totalChangeOneYear", "oneYear"),
    (
        "totalChangeThreeYears",
        "threeYears",
    ),
    ("totalChangeFiveYears", "fiveYears"),
    ("totalChangeTenYears", "tenYears"),
    (
        "totalChangeCurrentYear",
        "startOfYear",
    ),
]

CHANGE_PERCENT_PRICE_MAPPING = [
    ("changePercentOneWeek", "oneWeek"),
    ("changePercentOneMonth", "oneMonth"),
    (
        "changePercentThreeMonths",
        "threeMonths",
    ),
    ("changePercentOneYear", "oneYear"),
    ("changePercentThreeYears", "threeYears"),
    ("changePercentFiveYears", "fiveYears"),
    ("changePercentTenYears", "tenYears"),
    ("changePercentCurrentYear", "startOfYear"),
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
